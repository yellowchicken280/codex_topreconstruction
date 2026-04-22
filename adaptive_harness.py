import os
import json
import time
import math
import subprocess
import urllib.request
import re
import random
import csv
from pathlib import Path

# --- CONFIGURATION ---
MAX_HOURS = 72
WORK_DIR = "/global/u1/v/vinny/projects/topreco-agent"
PIPELINE_DIR = "/global/u1/v/vinny/projects/topreconstruction"
CODE_PATH = f"{PIPELINE_DIR}/top_reco/src/triplet_ml/select_triplets.py"
LAB_PATH = f"{WORK_DIR}/labbook.md"
CHAMP_PATH = f"{WORK_DIR}/champion_state.json"
TRAJECTORY_PATH = f"{WORK_DIR}/agent_trajectory.csv"
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = "https://api.cborg.lbl.gov/v1/chat/completions"
MODEL = "lbl/gpt-oss-120b-high"

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("adaptive_discovery.log", "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def call_model(messages):
    payload = {"model": MODEL, "messages": messages}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE_URL, data=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        log(f"API Error: {e}")
        return None

def initialize_trajectory():
    if not os.path.exists(TRAJECTORY_PATH):
        with open(TRAJECTORY_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Round", "ActionClass", "Setup", "Metric", "DeltaMetric", "Rationale", "Insight"])

def log_trajectory(round_id, action_class, setup, metric, delta, rationale, insight):
    with open(TRAJECTORY_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([round_id, action_class, setup, f"{metric:.4f}", f"{delta:.4f}", rationale, insight])

def run_iteration(iter_idx, logic_json):
    strat_slug = logic_json.get("slug", f"strat_{iter_idx}").replace(" ", "_")
    raw_logic = logic_json.get("logic", "combined_score = base_score")
    
    # HEAVY CLEANING: remove markdown blocks and other artifacts
    raw_logic = raw_logic.replace('```python', '').replace('```', '')
    raw_logic = raw_logic.replace('\u2011', '-').replace('\u2013', '-')
    
    # Robust Indentation
    lines = raw_logic.strip().split('\n')
    indented_logic = ""
    for line in lines:
        l = line.strip()
        if not l or l.startswith('python'): continue
        indented_logic += "            " + l + "\n"
    
    subprocess.run(f"rm -f {PIPELINE_DIR}/.git/index.lock", shell=True)
    subprocess.run(f"cd {PIPELINE_DIR} && git checkout top_reco/src/triplet_ml/select_triplets.py", shell=True)
    subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/reset_and_feature_patch.py", shell=True)
    
    with open(CODE_PATH, "r") as f: content = f.read()
    content = re.sub(r'STRATEGIES = \(.*?\)', f'STRATEGIES = ("greedy_disjoint", "top1", "topk", "threshold", "best_pair_avg_disjoint", "{strat_slug}")', content)
    
    impl = f"""
    if strategy == "{strat_slug}":
        if max_top_per_event <= 0 or len(candidates) == 0: return []
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
{indented_logic}
            new_cand = TripletCandidate(i=t.i, j=t.j, k=t.k, score=combined_score,
                is_truth=t.is_truth, triplet_pt=t.triplet_pt, triplet_eta=t.triplet_eta, triplet_phi=t.triplet_phi,
                triplet_mass=t.triplet_mass, mij_ab=t.mij_ab, mij_ac=t.mij_ac, mij_bc=t.mij_bc,
                dr_ab=t.dr_ab, dr_ac=t.dr_ac, dr_bc=t.dr_bc,
                ratio_ab=t.ratio_ab, ratio_ac=t.ratio_ac, ratio_bc=t.ratio_bc)
            scored_cands.append(new_cand)
        scored_cands.sort(key=lambda x: (-x.score, x.i, x.j, x.k))
        return _solve_exact_disjoint(scored_cands, max_top=max_top_per_event)
"""
    content = content.replace('    if strategy == "greedy_disjoint":', impl + '\n    if strategy == "greedy_disjoint":')
    with open(CODE_PATH, "w") as f: f.write(content)
    
    if subprocess.run(f"agent_kit/.venv/bin/python3 -m py_compile {CODE_PATH}", shell=True).returncode == 0:
        subprocess.run(f"PYTHONPATH={PIPELINE_DIR}/top_reco/src /global/homes/v/vinny/.conda/envs/topml/bin/python -m triplet_ml select_triplets --inference {PIPELINE_DIR}/artifacts/run_prof/infer_eval/inference_test_xgb.parquet --strategy {strat_slug} --output-dir artifacts/iter{iter_idx}_eval --min-score 0.0 --max-top-per-event 4 --no-progress", shell=True)
        res = subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/real_eval.py artifacts/iter{iter_idx}_eval/selected_triplets.parquet 0 2000", shell=True, capture_output=True, text=True)
        if "Efficiency: " in res.stdout:
            return float(res.stdout.split("Efficiency: ")[1].split("\n")[0].strip())
    return 0.0

def main():
    start_time = time.time()
    iter_idx = 91000 
    stale_iters = 0
    initialize_trajectory()

    log("=== Top Reconstruction Marathon Harness v17.1 (STABLE TRAJECTORY) ===")

    while (time.time() - start_time) < (MAX_HOURS * 3600):
        with open(CHAMP_PATH, "r") as f:
            champ = json.load(f)
        
        refine_prob = 0.10 + (0.80 - 0.10) * math.exp(-stale_iters / 500.0)
        is_refinement = random.random() < refine_prob
        
        prompt = f"""You are an autonomous physics agent.
CURRENT CHAMPION: {champ['slug']} (Efficiency: {champ['efficiency']:.4f})
TASK: Propose the next optimization step.
{ 'ACTION: INCREMENTAL TUNING' if is_refinement else 'ACTION: INNOVATION / SHIFT' }

RULES:
- NO markdown formatting (no ```). 
- Use ONLY Python math functions (exp, tanh, sqrt, log).
- Define 'combined_score'.
- 'base_score' is already defined.

OUTPUT JSON FORMAT:
{{
  "slug": "unique_id",
  "action_class": "Incremental Tuning" | "Within-Component Innovation" | "Cross-Component Attention Shift",
  "rationale": "Reason for action class choice.",
  "logic": "correction = 1.0\\ncombined_score = base_score * correction",
  "motivation": "Physics insight."
}}
"""
        response = call_model([{"role": "user", "content": prompt}])
        if not response: iter_idx += 1; continue
        
        try:
            json_text = re.search(r"\{.*\}", response, re.DOTALL).group()
            discovery = json.loads(json_text)
        except: iter_idx += 1; continue

        eff = run_iteration(iter_idx, discovery)
        delta = eff - champ["efficiency"]
        
        log(f"Iter {iter_idx}: {discovery.get('action_class')} -> Result: {eff:.4f} (Delta: {delta:.4f})")
        log_trajectory(iter_idx, discovery.get('action_class'), discovery.get('slug'), eff, delta, discovery.get('rationale'), discovery.get('motivation'))

        if eff > champ["efficiency"]:
            log(f"*** NEW GLOBAL CHAMPION! {eff:.4f} ***")
            champ.update({"efficiency": eff, "slug": discovery["slug"], "logic": discovery["logic"]})
            with open(CHAMP_PATH, "w") as f: json.dump(champ, f, indent=2)
            stale_iters = 0 
        else:
            stale_iters += 1

        with open(LAB_PATH, "a") as f:
            f.write(f"\n#### Round {iter_idx}: {discovery.get('action_class')}\n- Setup: {discovery.get('slug')}\n- Metric: {eff:.4f}\n- Delta: {delta:.4f}\n- Rationale: {discovery.get('rationale')}\n- Insight: {discovery.get('motivation')}\n")
        
        iter_idx += 1
        time.sleep(1)

if __name__ == "__main__":
    main()
