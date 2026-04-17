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
CODE_PATH = f"{PIPELINE_DIR}/src/triplet_ml/select_triplets.py"
LAB_PATH = f"{WORK_DIR}/labbook.md"
TRAJECTORY_PATH = f"{WORK_DIR}/discovery_trajectory.md"
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
            time.sleep(30)
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
    
    # 0. Auto-resume logic
    if os.path.exists(LAB_PATH):
        with open(LAB_PATH, "r") as f:
            lab_content = f.read()
            iters = re.findall(r"#### Iteration (\d+)", lab_content)
            iter_idx = int(iters[-1]) + 1 if iters else 4
    else:
        iter_idx = 4

    log(f"=== Top Reconstruction Marathon Harness v8.0 (COMPACTION MODE) starting at Iter {iter_idx} ===")

    while (time.time() - start_time) < (MAX_HOURS * 3600):
        log(f"--- STARTING ITERATION {iter_idx} ---")
        
        # 1. Periodically update the Discovery Trajectory (The "Compactor")
        if iter_idx % 5 == 0 or not os.path.exists(TRAJECTORY_PATH):
            log("Running Compactor: Updating discovery_trajectory.md...")
            with open(LAB_PATH, "r") as f: lab_tail = f.read()[-8000:]
            compact_prompt = f"""Summarize the last 50 iterations of this physics optimization.
Categorize the strategies tried (e.g. 'Mass Gaussians', 'MLP variants', 'pT weighting').
Identify confirmed DEAD ENDS (strategies that consistently stay at 0.6160).
Identify the current FRONTIER (the only thing that broke 0.63).
Labbook Context:
{lab_tail}
"""
            summary = call_model([{"role": "user", "content": compact_prompt}], temperature=0.3)
            if summary:
                with open(TRAJECTORY_PATH, "w") as f:
                    f.write("# Discovery Trajectory & Strategy Compaction\n\n")
                    f.write(summary)
                log("Trajectory updated.")

        # 2. Strategy Generation (informed by Trajectory)
        with open(TRAJECTORY_PATH, "r") as f: trajectory = f.read()
        with open(CODE_PATH, "r") as f: current_code = f.read()

        prompt = f"""You are a physicist. 
CURRENT FRONTIER: 0.6384 (Jet Topology).
DEAD ENDS TO AVOID: {trajectory[:1000]}

TASK:
Propose a strategy that is DISTINCT from the dead ends. Explore the physical nature of the background events. 
Why did the 0.6384 strategy work? Can we combine it with something else?

Output format (JSON):
{{
  "name": "strategy_v{iter_idx}",
  "logic": "            # 12-space indented python code...\\n            combined_score = ...",
  "motivation": "One sentence reasoning."
}}
"""
        messages = [{"role": "user", "content": prompt}]
        response = call_model(messages)
        if not response: continue
        
        try:
            json_text = re.search(r"\{.*\}", response, re.DOTALL).group()
            discovery = json.loads(json_text)
            strat_name = discovery["name"]
            strat_logic = discovery["logic"]
        except Exception as e:
            log(f"Failed to parse response: {e}")
            continue

        # 3. Injection & Evaluation
        code_content = open(CODE_PATH, "r").read()
        if f'"{strat_name}"' not in code_content:
            code_content = code_content.replace('    "asymmetric_top_exact_v3",', f'    "asymmetric_top_exact_v3",\n    "{strat_name}",')
        
        new_block = f"\n    if strategy == \"{strat_name}\":\n        if max_top_per_event <= 0 or len(candidates) == 0: return []\n        scored_cands = []\n        for t in candidates:\n{strat_logic}\n            new_cand = TripletCandidate(i=t.i, j=t.j, k=t.k, score=combined_score,\n                triplet_pt=t.triplet_pt, triplet_eta=t.triplet_eta, triplet_phi=t.triplet_phi,\n                triplet_mass=t.triplet_mass, mij_ab=t.mij_ab, mij_ac=t.mij_ac, mij_bc=t.mij_bc)\n            scored_cands.append(new_cand)\n        scored_cands.sort(key=lambda t: (-t.score, t.i, t.j, t.k))\n        return _solve_exact_disjoint(scored_cands, max_top=max_top_per_event)\n"
        
        code_content = code_content.replace('    if strategy == "asymmetric_top_exact_v3":', new_block + '\n    if strategy == "asymmetric_top_exact_v3":')
        with open(CODE_PATH, "w") as f: f.write(code_content)
        
        # 4. Run Pipe
        run_cmd(f"/global/homes/v/vinny/.conda/envs/topml/bin/python -m triplet_ml select_triplets --inference {PIPELINE_DIR}/artifacts/run_prof/infer_eval/inference_test_xgb.parquet --strategy {strat_name} --output-dir artifacts/iter{iter_idx}_eval --min-score 0.0 --max-top-per-event 4 --no-progress")
        res_out = run_cmd(f"{WORK_DIR}/agent_kit/.venv/bin/python3 {WORK_DIR}/final_eval.py")
        
        if res_out:
            try:
                new_eff = res_out.split("New strategy efficiency: ")[1].split("\n")[0].strip()
                p = float(new_eff)
                err = math.sqrt(p*(1-p)/1026)
                log(f"Result: {p:.4f} +/- {err:.4f}")
                with open(LAB_PATH, "a") as f:
                    f.write(f"\n#### Iteration {iter_idx}: {strat_name}\n- Efficiency: {p:.4f} ± {err:.3f}\n- Motivation: {discovery['motivation']}\n")
            except: pass
        
        iter_idx += 1
        time.sleep(10)

if __name__ == "__main__":
    main()
