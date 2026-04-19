import os
import json
import time
import math
import subprocess
import urllib.request
import re
from pathlib import Path

# --- CONFIGURATION ---
MAX_HOURS = 72
WORK_DIR = "/global/u1/v/vinny/projects/topreco-agent"
PIPELINE_DIR = "/global/u1/v/vinny/projects/topreconstruction"
CODE_PATH = f"{PIPELINE_DIR}/top_reco/src/triplet_ml/select_triplets.py"
LAB_PATH = f"{WORK_DIR}/labbook.md"
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = "https://api.cborg.lbl.gov/v1/chat/completions"
MODEL = "lbl/gpt-oss-120b-high"
GLOBAL_BEST = 0.6277

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    # THE ONLY LOG FILE WE CARE ABOUT
    with open("stable_marathon.log", "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def call_model(messages):
    payload = {"model": MODEL, "messages": messages, "temperature": 0.7}
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

def main():
    start_time = time.time()
    iter_idx = 20000 # The Final Era

    log("=== Top Reconstruction Marathon Harness v11.0 (ULTRA-STABLE) ===")

    while (time.time() - start_time) < (MAX_HOURS * 3600):
        log(f"--- STARTING ITERATION {iter_idx} ---")
        
        prompt = """You are a senior physicist. GOAL: Break 0.6277.
FEATURES: Mass Ratios (t.ratio_ab), Angles (t.dr_ab), Detector Geometry (t.triplet_eta).
MANDATORY: Define 'combined_score' using math functions and 't' attributes.
Use math.exp, math.tanh, etc.

Return JSON only: { "slug": "final_v20000", "logic": "combined_score = ...", "motivation": "..." }
"""
        response = call_model([{"role": "user", "content": prompt}])
        if not response: 
            iter_idx += 1; time.sleep(10); continue
        
        try:
            json_text = re.search(r"\{.*\}", response, re.DOTALL).group()
            discovery = json.loads(json_text)
            strat_slug = discovery["slug"].replace(" ", "_")
            raw_logic = discovery["logic"].replace('\u2011', '-').replace('\u2013', '-')
            cleaned_lines = [l.strip() for l in raw_logic.split('\n') if 'print(' not in l and l.strip()]
            strat_logic = "\n".join(["            " + l for l in cleaned_lines])
        except: 
            iter_idx += 1; time.sleep(10); continue

        # 1. Reset
        subprocess.run(f"cd {PIPELINE_DIR} && git checkout top_reco/src/triplet_ml/select_triplets.py", shell=True)
        subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/final_patch.py", shell=True)
        
        # 2. Inject
        with open(CODE_PATH, "r") as f: content = f.read()
        content = content.replace('best_pair_avg_disjoint")', f'best_pair_avg_disjoint", "{strat_slug}")')
        impl = f"""
    if strategy == "{strat_slug}":
        if max_top_per_event <= 0 or len(candidates) == 0: return []
        scored_cands = []
        for t in candidates:
            import math
{strat_logic}
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
        
        # 3. Eval
        if subprocess.run(f"agent_kit/.venv/bin/python3 -m py_compile {CODE_PATH}", shell=True).returncode == 0:
            subprocess.run(f"PYTHONPATH={PIPELINE_DIR}/top_reco/src /global/homes/v/vinny/.conda/envs/topml/bin/python -m triplet_ml select_triplets --inference {PIPELINE_DIR}/artifacts/run_prof/infer_eval/inference_test_xgb.parquet --strategy {strat_slug} --output-dir artifacts/iter{iter_idx}_eval --min-score 0.0 --max-top-per-event 4 --no-progress", shell=True)
            res = subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/real_eval.py artifacts/iter{iter_idx}_eval/selected_triplets.parquet 0 2000", shell=True, capture_output=True, text=True)
            
            if "Efficiency: " in res.stdout:
                p = float(res.stdout.split("Efficiency: ")[1].split("\n")[0].strip())
                log(f"Result: {p:.4f}")
                with open(LAB_PATH, "a") as f:
                    f.write(f"\n#### Iteration {iter_idx}: {strat_slug}\n- Efficiency: {p:.4f}\n- Motivation: {discovery['motivation']}\n")
        
        iter_idx += 1
        time.sleep(5)

if __name__ == "__main__":
    main()
