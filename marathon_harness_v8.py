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
    iter_idx = 2000 # "The Honest Era"

    log("=== Top Reconstruction Marathon Harness v8.7 (TRUTH MODE) ===")

    while (time.time() - start_time) < (MAX_HOURS * 3600):
        log(f"--- STARTING ITERATION {iter_idx} ---")
        
        # 1. Strategy Generation
        prompt = """You are a physicist. 
CURRENT TRUTH: The baseline efficiency is 0.6267. 
TASK: Devise a NOVEL strategy to break 0.64.
RULES:
- Use 'math.exp', 'math.log', 'math.tanh'.
- Object 't' has: score, triplet_mass, triplet_pt, mij_ab, mij_ac, mij_bc.
- Define 'combined_score'.

Output JSON only:
{
  "slug": "honest_phys_v2000",
  "logic": "combined_score = t.score * ...",
  "motivation": "..."
}
"""
        messages = [{"role": "user", "content": prompt}]
        response = call_model(messages)
        if not response: continue
        
        try:
            json_text = re.search(r"\{.*\}", response, re.DOTALL).group()
            discovery = json.loads(json_text)
            strat_name = discovery["slug"].replace(" ", "_").replace("-", "_")
            raw_logic = discovery["logic"].replace('\u2011', '-').replace('\u2013', '-')
            logic_lines = [line.strip() for line in raw_logic.split('\n') if line.strip()]
            strat_logic = "\n".join(["            " + line for line in logic_lines])
        except: continue

        # 2. Reset and Inject
        subprocess.run(f"cd {PIPELINE_DIR} && git checkout top_reco/src/triplet_ml/select_triplets.py", shell=True)
        subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/final_patch.py", shell=True)
        
        with open(CODE_PATH, "r") as f: code_content = f.read()
        code_content = code_content.replace('best_pair_avg_disjoint", "asymmetric_top_exact_v3")', 
                                         f'best_pair_avg_disjoint", "asymmetric_top_exact_v3", "{strat_name}")')
        
        new_block = f"""
    if strategy == "{strat_name}":
        if max_top_per_event <= 0 or len(candidates) == 0:
            return []
        scored_cands = []
        for t in candidates:
            import math
{strat_logic}
            new_cand = TripletCandidate(i=t.i, j=t.j, k=t.k, score=combined_score,
                is_truth=t.is_truth,
                triplet_pt=t.triplet_pt, triplet_eta=t.triplet_eta, triplet_phi=t.triplet_phi,
                triplet_mass=t.triplet_mass, mij_ab=t.mij_ab, mij_ac=t.mij_ac, mij_bc=t.mij_bc)
            scored_cands.append(new_cand)
        scored_cands.sort(key=lambda t: (-t.score, t.i, t.j, t.k))
        return _solve_exact_disjoint(scored_cands, max_top=max_top_per_event)
"""
        code_content = code_content.replace('    if strategy == "asymmetric_top_exact_v3":', 
                                         new_block + '\n    if strategy == "asymmetric_top_exact_v3":')
        with open(CODE_PATH, "w") as f: f.write(code_content)
        
        check = subprocess.run(f"agent_kit/.venv/bin/python3 -m py_compile {CODE_PATH}", shell=True, capture_output=True)
        if check.returncode != 0:
            log(f"Syntax error in '{strat_name}'. skipping.\n{check.stderr.decode()}")
            continue

        # 3. Evaluation
        eval_cmd = f"PYTHONPATH={PIPELINE_DIR}/top_reco/src /global/homes/v/vinny/.conda/envs/topml/bin/python -m triplet_ml select_triplets --inference {PIPELINE_DIR}/artifacts/run_prof/infer_eval/inference_test_xgb.parquet --strategy {strat_name} --output-dir artifacts/iter{iter_idx}_eval --min-score 0.0 --max-top-per-event 4 --no-progress"
        run_cmd(eval_cmd)
        
        res_out = run_cmd(f"agent_kit/.venv/bin/python3 {WORK_DIR}/real_eval.py artifacts/iter{iter_idx}_eval/selected_triplets.parquet")
        if res_out:
            try:
                new_eff = res_out.split("Efficiency: ")[1].split("\n")[0].strip()
                p = float(new_eff)
                err = math.sqrt(p*(1-p)/1026)
                log(f"Result: {p:.4f} +/- {err:.4f}")
                with open(LAB_PATH, "a") as f:
                    f.write(f"\n#### Iteration {iter_idx}: {strat_name}\n- Efficiency: {p:.4f} ± {err:.3f}\n- Motivation: {discovery['motivation']}\n")
            except: pass
        
        iter_idx += 1
        time.sleep(5)

if __name__ == "__main__":
    main()
