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
CHAMP_PATH = f"{WORK_DIR}/champion_state.json"
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = "https://api.cborg.lbl.gov/v1/chat/completions"
MODEL = "lbl/gpt-oss-120b-high"

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("adaptive_discovery.log", "a") as f:
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
    iter_idx = 50000 

    log("=== Top Reconstruction Marathon Harness v13.0 (TRUE ADAPTIVE) ===")

    while (time.time() - start_time) < (MAX_HOURS * 3600):
        # 1. Load current Champion
        with open(CHAMP_PATH, "r") as f:
            champ = json.load(f)
        
        log(f"--- STARTING ITERATION {iter_idx} (Baseline: {champ['efficiency']:.4f}) ---")
        
        prompt = f"""You are a physicist. 
GOAL: Break the current efficiency record.
CURRENT BEST EFFICIENCY: {champ['efficiency']:.4f}
CURRENT BEST LOGIC:
{champ['logic']}

TASK: Propose a code block that replaces the logic above to achieve HIGHER efficiency.
You have access to: t.score, t.triplet_mass, t.triplet_pt, t.triplet_eta, t.ratio_ab, t.ratio_ac, t.ratio_bc, t.dr_ab, t.dr_ac, t.dr_bc.

RULES:
- You MUST define the variable 'combined_score'.
- Use math.exp, math.tanh, etc.
- No print statements.

Return JSON only: {{ "slug": "adaptive_v50000", "logic": "...", "motivation": "..." }}
"""
        response = call_model([{"role": "user", "content": prompt}])
        if not response: 
            iter_idx += 1; time.sleep(10); continue
        
        try:
            json_text = re.search(r"\{.*\}", response, re.DOTALL).group()
            discovery = json.loads(json_text)
            strat_slug = discovery["slug"].replace(" ", "_").replace("-", "_")
            raw_logic = discovery["logic"].replace('\u2011', '-').replace('\u2013', '-')
            cleaned_lines = [l.strip() for l in raw_logic.split('\n') if 'print(' not in l and l.strip()]
            strat_logic = "\n".join(["            " + l for l in cleaned_lines])
        except: 
            iter_idx += 1; time.sleep(10); continue

        # 2. Reset Engine to the patched baseline
        subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/reset_and_feature_patch.py", shell=True)
        
        # 3. Surgical Injection
        with open(CODE_PATH, "r") as f: content = f.read()
        
        # Replace the STRATEGIES tuple line completely to avoid pollution
        content = re.sub(r'STRATEGIES = \(.*?\)', f'STRATEGIES = ("greedy_disjoint", "top1", "topk", "threshold", "best_pair_avg_disjoint", "{strat_slug}")', content)
        
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
        
        # 4. Evaluation
        if subprocess.run(f"agent_kit/.venv/bin/python3 -m py_compile {CODE_PATH}", shell=True).returncode == 0:
            subprocess.run(f"PYTHONPATH={PIPELINE_DIR}/top_reco/src /global/homes/v/vinny/.conda/envs/topml/bin/python -m triplet_ml select_triplets --inference {PIPELINE_DIR}/artifacts/run_prof/infer_eval/inference_test_xgb.parquet --strategy {strat_slug} --output-dir artifacts/iter{iter_idx}_eval --min-score 0.0 --max-top-per-event 4 --no-progress", shell=True)
            res = subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/real_eval.py artifacts/iter{iter_idx}_eval/selected_triplets.parquet 0 2000", shell=True, capture_output=True, text=True)
            
            if "Efficiency: " in res.stdout:
                p = float(res.stdout.split("Efficiency: ")[1].split("\n")[0].strip())
                log(f"Result: {p:.4f}")
                
                if p > champ["efficiency"]:
                    log(f"*** NEW CHAMPION! {p:.4f} > {champ['efficiency']:.4f} ***")
                    champ["efficiency"] = p
                    champ["slug"] = strat_slug
                    champ["logic"] = raw_logic
                    with open(CHAMP_PATH, "w") as f:
                        json.dump(champ, f, indent=2)
                    with open(LAB_PATH, "a") as f:
                        f.write(f"\n#### Iteration {iter_idx}: {strat_slug} (NEW BEST)\n- Efficiency: {p:.4f}\n- Motivation: {discovery['motivation']}\n")
                else:
                    with open(LAB_PATH, "a") as f:
                        f.write(f"\n#### Iteration {iter_idx}: {strat_slug}\n- Efficiency: {p:.4f}\n- Motivation: {discovery['motivation']}\n")
        
        iter_idx += 1
        time.sleep(1)

if __name__ == "__main__":
    main()
