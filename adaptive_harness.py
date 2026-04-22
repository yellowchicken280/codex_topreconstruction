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
MAX_HOURS = 72
WORK_DIR = "/global/u1/v/vinny/projects/topreco-agent"
PIPELINE_DIR = "/global/u1/v/vinny/projects/topreconstruction"
CODE_PATH = f"{PIPELINE_DIR}/top_reco/src/triplet_ml/select_triplets.py"
LAB_PATH = f"{WORK_DIR}/labbook.md"
CHAMP_PATH = f"{WORK_DIR}/champion_state.json"
TRAJECTORY_PATH = f"{WORK_DIR}/agent_trajectory.csv"
PID_PATH = f"{WORK_DIR}/harness.pid"
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = "https://api.cborg.lbl.gov/v1/chat/completions"
MODEL = "lbl/gpt-oss-120b-high"

class DiscoveryHarness:
    def __init__(self):
        self.stale_iters = 0
        self.start_time = time.time()
        self.iter_idx = 100000 
        self.initialize_trajectory()

    def log(self, msg):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("marathon_final.log", "a") as f:
            f.write(f"[{timestamp}] {msg}\n")
        print(f"[{timestamp}] {msg}", flush=True)

    def initialize_trajectory(self):
        if not os.path.exists(TRAJECTORY_PATH):
            with open(TRAJECTORY_PATH, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Round", "ActionClass", "Setup", "Metric", "DeltaMetric", "Rationale", "Insight"])

    def call_model(self, messages):
        payload = {"model": MODEL, "messages": messages, "temperature": 0.7}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(BASE_URL, data=data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode())
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            self.log(f"API Error: {e}")
            return None

    def clean_logic(self, raw_logic):
        # Remove markdown and unicode artifacts
        clean = raw_logic.replace('```python', '').replace('```', '')
        clean = re.sub(r'[≈=]\s*0\.\d+', '', clean)
        lines = []
        for line in clean.split('\n'):
            l = line.strip()
            if not l or l.startswith('python') or any(c in l for c in ['≈', '±']):
                continue
            lines.append("            " + l)
        return "\n".join(lines)

    def run_eval(self, logic_json):
        strat_slug = logic_json.get("slug", f"strat_{self.iter_idx}").replace(" ", "_")
        indented_logic = self.clean_logic(logic_json.get("logic", "combined_score = base_score"))
        
        # State Reset
        subprocess.run(f"rm -f {PIPELINE_DIR}/.git/index.lock", shell=True)
        subprocess.run(f"cd {PIPELINE_DIR} && git checkout top_reco/src/triplet_ml/select_triplets.py", shell=True, capture_output=True)
        subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/reset_and_feature_patch.py", shell=True, capture_output=True)
        
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
            if 'combined_score' not in locals(): combined_score = base_score
            new_cand = TripletCandidate(i=t.i, j=t.j, k=t.k, score=combined_score, is_truth=t.is_truth, triplet_pt=t.triplet_pt, triplet_eta=t.triplet_eta, triplet_phi=t.triplet_phi, triplet_mass=t.triplet_mass, mij_ab=t.mij_ab, mij_ac=t.mij_ac, mij_bc=t.mij_bc, dr_ab=t.dr_ab, dr_ac=t.dr_ac, dr_bc=t.dr_bc, ratio_ab=t.ratio_ab, ratio_ac=t.ratio_ac, ratio_bc=t.ratio_bc)
            scored_cands.append(new_cand)
        scored_cands.sort(key=lambda x: (-x.score, x.i, x.j, x.k))
        return _solve_exact_disjoint(scored_cands, max_top=max_top_per_event)
"""
        content = content.replace('    if strategy == "greedy_disjoint":', impl + '\n    if strategy == "greedy_disjoint":')
        with open(CODE_PATH, "w") as f: f.write(content)
        
        # Physics Benchmarking (High Precision: 5000 events)
        if subprocess.run(f"agent_kit/.venv/bin/python3 -m py_compile {CODE_PATH}", shell=True).returncode == 0:
            offset = random.randint(0, 5000)
            eval_cmd = f"PYTHONPATH={PIPELINE_DIR}/top_reco/src /global/homes/v/vinny/.conda/envs/topml/bin/python -m triplet_ml select_triplets --inference {PIPELINE_DIR}/artifacts/run_prof/infer_eval/inference_test_xgb.parquet --strategy {strat_slug} --output-dir artifacts/eval_{self.iter_idx} --min-score 0.0 --max-top-per-event 4 --no-progress"
            subprocess.run(eval_cmd, shell=True, capture_output=True)
            res = subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/real_eval.py artifacts/eval_{self.iter_idx}/selected_triplets.parquet {offset} 5000", shell=True, capture_output=True, text=True)
            if "Efficiency: " in res.stdout:
                parts = res.stdout.split("Efficiency: ")[1].split("+/-")
                return float(parts[0].strip()), float(parts[1].strip())
        return 0.0, 0.0

    def run(self):
        self.log("=== Top Reconstruction Strategy Discovery Framework v17.8 (STABLE) ===")
        while (time.time() - self.start_time) < (MAX_HOURS * 3600):
            with open(CHAMP_PATH, "r") as f: champ = json.load(f)
            
            refine_prob = 0.10 + (0.80 - 0.10) * math.exp(-self.stale_iters / 500.0)
            is_ref = random.random() < refine_prob
            
            prompt = f"Propose triplet selection strategy. CHAMP: {champ['slug']} ({champ['efficiency']:.4f}). MODE: {'REFINE' if is_ref else 'MUTATE'}. LOGIC: {champ['logic']}. JSON ONLY."
            
            response = self.call_model([{"role": "user", "content": prompt}])
            if not response: continue
            
            try:
                discovery = json.loads(re.search(r"\{.*\}", response, re.DOTALL).group())
                eff, err = self.run_eval(discovery)
                self.log(f"Round {self.iter_idx}: {discovery.get('action_class', 'Search')} -> Result: {eff:.4f} +/- {err:.4f}")
                
                # Log to Trajectory
                with open(TRAJECTORY_PATH, "a", newline="") as f:
                    csv.writer(f).writerow([self.iter_idx, discovery.get('action_class'), discovery.get('slug'), f"{eff:.4f}", f"{eff - 0.6160:.4f}", discovery.get('rationale'), discovery.get('motivation')])

                if eff > 0.6345:
                    self.log(f"*** NEW CHAMPION DISCOVERED: {eff:.4f} ***")
                    champ.update({"efficiency": eff, "slug": discovery["slug"], "logic": discovery["logic"]})
                    with open(CHAMP_PATH, "w") as f: json.dump(champ, f, indent=2)
                    self.stale_iters = 0
                else:
                    self.stale_iters += 1
                
                self.iter_idx += 1
            except Exception as e:
                self.log(f"Error in round {self.iter_idx}: {e}")
                self.iter_idx += 1

if __name__ == "__main__":
    if os.path.exists(PID_PATH): os.remove(PID_PATH) # Fresh start for refactor
    with open(PID_PATH, "w") as f: f.write(str(os.getpid()))
    try:
        harness = DiscoveryHarness()
        harness.run()
    finally:
        if os.path.exists(PID_PATH): os.remove(PID_PATH)
