import os
import json
import time
import math
import subprocess
import urllib.request
import re
from pathlib import Path

# --- Configuration ---
MAX_HOURS = 72
WORK_DIR = "/global/u1/v/vinny/projects/topreco-agent"
PIPELINE_DIR = "/global/u1/v/vinny/projects/topreconstruction"
CODE_PATH = f"{PIPELINE_DIR}/top_reco/src/triplet_ml/select_triplets.py"
LAB_PATH = f"{WORK_DIR}/labbook.md"
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = "https://api.cborg.lbl.gov/v1/chat/completions"
MODEL = "lbl/gpt-oss-120b-high"

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    with open("marathon_harness.log", "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

def call_model(messages, temperature=0.7):
    payload = {"model": MODEL, "messages": messages, "temperature": temperature}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE_URL, data=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}, method="POST")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                result = json.loads(resp.read().decode())
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            log(f"API Attempt {attempt+1} failed: {e}")
            time.sleep(15)
    return None

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return res.stdout
    except subprocess.CalledProcessError as e:
        log(f"Command failed.\nSTDERR: {e.stderr}")
        return None

def main():
    start_time = time.time()
    iter_idx = 7000 

    log("=== Top Reconstruction Marathon Harness v9.5 (FINAL RATIO) ===")

    while (time.time() - start_time) < (MAX_HOURS * 3600):
        log(f"--- STARTING ITERATION {iter_idx} ---")
        
        prompt = """You are a physicist. 
GOAL: Break the 0.6277 plateau.
PHYSICS: Real top quarks have a W-boson where: Mass_Ratio (dijet/triplet) approx 0.46.

AVAILABLE ATTRIBUTES:
- t.score (BDT), t.triplet_mass, t.triplet_pt
- t.mij_ab, t.mij_ac, t.mij_bc (Sub-masses)
- t.dr_ab, t.dr_ac, t.dr_bc (DeltaR)
- t.ratio_ab, t.ratio_ac, t.ratio_bc (Mass Ratios)

MANDATORY: You MUST define a variable named 'combined_score'. 
Use arithmetic only (math.exp, math.tanh, math.sqrt).

Return JSON only: { "slug": "ratio_v7000", "logic": "combined_score = ...", "motivation": "..." }
"""
        messages = [{"role": "user", "content": prompt}]
        response = call_model(messages)
        if not response: 
            iter_idx += 1
            continue
        
        try:
            json_text = re.search(r"\{.*\}", response, re.DOTALL).group()
            discovery = json.loads(json_text)
            strat_slug = discovery["slug"].replace(" ", "_").replace("-", "_")
            raw_logic = discovery["logic"].replace('\u2011', '-').replace('\u2013', '-')
            logic_lines = [line.strip() for line in raw_logic.split('\n') if line.strip()]
            strat_logic = "\n".join(["            " + line for line in logic_lines])
        except: 
            iter_idx += 1
            continue

        # 1. Reset
        subprocess.run(f"cd {PIPELINE_DIR} && git checkout top_reco/src/triplet_ml/select_triplets.py", shell=True)
        
        # 2. Patch
        with open(CODE_PATH, "r") as f: content = f.read()
        
        solver_code = """
def _solve_exact_disjoint(candidates: Sequence[TripletCandidate], max_top: int) -> List[TripletCandidate]:
    subset = candidates[:30]
    best_sum = -1.0
    best_set: List[TripletCandidate] = []
    def search(idx, sel, cur_sum, used):
        nonlocal best_sum, best_set
        if cur_sum > best_sum:
            best_sum, best_set = cur_sum, list(sel)
        if len(sel) >= max_top or idx >= len(subset): return
        for i in range(idx, len(subset)):
            c = subset[i]; jts = {c.i, c.j, c.k}
            if not (jts & used): search(i + 1, sel + [c], cur_sum + c.score, used | jts)
    search(0, [], 0.0, set())
    return best_set
"""
        content = content.replace("def _apply_strategy(", solver_code + "\ndef _apply_strategy(")
        content = content.replace("    triplet_mass: float", "    triplet_mass: float\n    mij_ab: float\n    mij_ac: float\n    mij_bc: float\n    dr_ab: float\n    dr_ac: float\n    dr_bc: float\n    ratio_ab: float\n    ratio_ac: float\n    ratio_bc: float")
        content = content.replace('        "is_truth",', '        "is_truth",\n        "mij_ab", "mij_ac", "mij_bc", "dr_ab", "dr_ac", "dr_bc", "mij_over_m123_ab", "mij_over_m123_ac", "mij_over_m123_bc",')
        content = content.replace('triplet_mass=float(payload["m123"][idx]),', 'triplet_mass=float(payload["m123"][idx]),\n                    mij_ab=float(payload["mij_ab"][idx]),\n                    mij_ac=float(payload["mij_ac"][idx]),\n                    mij_bc=float(payload["mij_bc"][idx]),\n                    dr_ab=float(payload["dr_ab"][idx]),\n                    dr_ac=float(payload["dr_ac"][idx]),\n                    dr_bc=float(payload["dr_bc"][idx]),\n                    ratio_ab=float(payload["mij_over_m123_ab"][idx]),\n                    ratio_ac=float(payload["mij_over_m123_ac"][idx]),\n                    ratio_bc=float(payload["mij_over_m123_bc"][idx]),')
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
        
        # Check
        check = subprocess.run(f"agent_kit/.venv/bin/python3 -m py_compile {CODE_PATH}", shell=True, capture_output=True)
        if check.returncode != 0:
            iter_idx += 1
            continue

        # Eval
        run_cmd(f"PYTHONPATH={PIPELINE_DIR}/top_reco/src /global/homes/v/vinny/.conda/envs/topml/bin/python -m triplet_ml select_triplets --inference {PIPELINE_DIR}/artifacts/run_prof/infer_eval/inference_test_xgb.parquet --strategy {strat_slug} --output-dir artifacts/iter{iter_idx}_eval --min-score 0.0 --max-top-per-event 4 --no-progress")
        res_out = run_cmd(f"agent_kit/.venv/bin/python3 {WORK_DIR}/real_eval.py artifacts/iter{iter_idx}_eval/selected_triplets.parquet")
        
        if res_out:
            try:
                new_eff = res_out.split("Efficiency: ")[1].split("\n")[0].strip()
                p = float(new_eff)
                err = math.sqrt(p*(1-p)/1026)
                log(f"Result: {p:.4f} +/- {err:.4f}")
                with open(LAB_PATH, "a") as f:
                    f.write(f"\n#### Iteration {iter_idx}: {strat_slug}\n- Efficiency: {p:.4f} ± {err:.3f}\n- Motivation: {discovery['motivation']}\n")
            except: pass
            
        iter_idx += 1
        time.sleep(5)

if __name__ == "__main__":
    main()
