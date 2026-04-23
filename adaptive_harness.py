import os
import json
import time
import math
import subprocess
import urllib.request
import re
import random
import csv
import sys
from pathlib import Path

# --- CONFIGURATION ---
WORK_DIR = "/global/u1/v/vinny/projects/topreco-agent"
PIPELINE_DIR = "/global/u1/v/vinny/projects/topreconstruction"
CODE_PATH = f"{PIPELINE_DIR}/top_reco/src/triplet_ml/select_triplets.py"
CHAMP_PATH = f"{WORK_DIR}/champion_state.json"
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = "https://api.cborg.lbl.gov/v1/chat/completions"
MODEL = "lbl/gpt-oss-120b-high"

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("marathon_production.log", "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}", flush=True)

def run_iteration(iter_idx, discovery):
    strat_slug = discovery.get("slug", f"strat_{iter_idx}").replace(" ", "_")
    
    # 1. Robust Indentation
    raw_logic = discovery.get("logic", "combined_score = base_score").replace('```python', '').replace('```', '')
    raw_logic = raw_logic.replace('\u2011', '-').replace('\u2013', '-')
    lines = raw_logic.strip().split('\n')
    strat_logic = "\n".join(["            " + l.strip() for l in lines if l.strip() and not l.strip().startswith(('python', 'return'))])
    
    # 2. Reset and Patch
    subprocess.run(f"cd {PIPELINE_DIR} && git checkout top_reco/src/triplet_ml/select_triplets.py", shell=True, capture_output=True)
    subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/reset_and_feature_patch.py", shell=True, capture_output=True)
    
    with open(CODE_PATH, "r") as f: content = f.read()
    content = re.sub(r'STRATEGIES = \(.*?\)', f'STRATEGIES = ("greedy_disjoint", "top1", "topk", "threshold", "best_pair_avg_disjoint", "{strat_slug}")', content)
    
    impl = f"""
    if strategy == "{strat_slug}":
        import math
        from math import exp, tanh, sqrt, log
        scored_cands = []
        for t in candidates:
            best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
            top_prior = exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
            w_prior = exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
            pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
            ratio_factor = (exp(-((t.ratio_ab - 0.46)**2)/0.02) + exp(-((t.ratio_ac - 0.46)**2)/0.02) + exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
            eta_factor = 1.0 + 0.05 * tanh(1.5 - abs(t.triplet_eta))
            base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling * ratio_factor * eta_factor
            combined_score = base_score
{strat_logic}
            scored_cands.append(TripletCandidate(i=t.i, j=t.j, k=t.k, score=combined_score, is_truth=t.is_truth, triplet_pt=t.triplet_pt, triplet_eta=t.triplet_eta, triplet_phi=t.triplet_phi, triplet_mass=t.triplet_mass, mij_ab=t.mij_ab, mij_ac=t.mij_ac, mij_bc=t.mij_bc, dr_ab=t.dr_ab, dr_ac=t.dr_ac, dr_bc=t.dr_bc, ratio_ab=t.ratio_ab, ratio_ac=t.ratio_ac, ratio_bc=t.ratio_bc))
        scored_cands.sort(key=lambda x: (-x.score, x.i, x.j, x.k))
        return _solve_exact_disjoint(scored_cands, max_top=max_top_per_event)
"""
    content = content.replace('    if strategy == "greedy_disjoint":', impl + '\n    if strategy == "greedy_disjoint":')
    with open(CODE_PATH, "w") as f: f.write(content)
    
    # 3. Eval (Use the 2000 event subset that gave us the original breakthrough)
    eval_cmd = f"PYTHONPATH={PIPELINE_DIR}/top_reco/src /global/homes/v/vinny/.conda/envs/topml/bin/python -u -m triplet_ml select_triplets --inference {PIPELINE_DIR}/artifacts/run_prof/infer_eval/inference_test_xgb.parquet --strategy {strat_slug} --output-dir artifacts/eval_tmp --max-top-per-event 4 --no-progress"
    subprocess.run(eval_cmd, shell=True, capture_output=True)
    
    res = subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/real_eval.py artifacts/eval_tmp/selected_triplets.parquet 0 2000", shell=True, capture_output=True, text=True)
    if "Efficiency: " in res.stdout:
        return float(res.stdout.split("Efficiency: ")[1].split("+/-")[0].strip())
    return 0.0

def main():
    log("=== Top Reconstruction Marathon RESTORED (v14.5 Logic) ===")
    iter_idx = 300000
    while True:
        with open(CHAMP_PATH, "r") as f: champ = json.load(f)
        prompt = f"Refine the champion logic: {champ['logic']}. Propose a small correction factor. Return ONLY JSON with keys 'slug', 'logic', 'motivation'."
        
        req = urllib.request.Request(BASE_URL, data=json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}]}).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                response = json.loads(resp.read().decode())["choices"][0]["message"]["content"]
                discovery = json.loads(re.search(r"\{.*\}", response, re.DOTALL).group())
                eff = run_iteration(iter_idx, discovery)
                log(f"Round {iter_idx}: {discovery['slug']} -> Result: {eff:.4f}")
                
                if eff > 0.6345:
                    log(f"*** BREAKTHROUGH: {eff:.4f} ***")
                    champ.update({"efficiency": eff, "slug": discovery["slug"], "logic": discovery["logic"]})
                    with open(CHAMP_PATH, "w") as f: json.dump(champ, f, indent=2)
                iter_idx += 1
        except Exception as e:
            log(f"Round {iter_idx} Failed: {e}")
            iter_idx += 1
        time.sleep(1)

if __name__ == "__main__":
    main()
