import os, json, time, math, subprocess, urllib.request, re, random, csv, sys
from pathlib import Path

WORK_DIR = "/global/u1/v/vinny/projects/topreco-agent"
PIPELINE_DIR = "/global/u1/v/vinny/projects/topreconstruction"
SCRIPT_PATH = f"{PIPELINE_DIR}/top_reco/src/triplet_ml/select_triplets.py"
CHAMP_PATH = f"{WORK_DIR}/champion_state.json"
TRAJECTORY_PATH = f"{WORK_DIR}/agent_trajectory.csv"
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = "https://api.cborg.lbl.gov/v1/chat/completions"
MODEL = "lbl/gpt-oss-120b-high"
LOCAL_BENCHMARK = 0.6151

class DiscoveryHarness:
    def __init__(self):
        self.stale_iters = 0
        self.iter_idx = 300300 # Resume from current high range

    def log(self, msg):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

    def call_model(self, prompt, is_mutation=False):
        temp = 1.0 if is_mutation else 0.7
        data = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": temp}).encode("utf-8")
        req = urllib.request.Request(BASE_URL, data=data, headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode())["choices"][0]["message"]["content"]
        except: return None

    def run_eval(self, discovery):
        subprocess.run(f"cd {PIPELINE_DIR} && git checkout top_reco/src/triplet_ml/select_triplets.py", shell=True, capture_output=True)
        with open(SCRIPT_PATH, "r") as f: content = f.read()
        
        slug = discovery["slug"]
        clean = discovery["logic"].replace('\\n', '\n').replace('\\', '').replace('```python', '').replace('```', '')
        logic_body = "\n".join(["                " + l.strip() for l in clean.split('\n') if l.strip()])
        
        content = re.sub(r'STRATEGIES = \(.*?\)', f'STRATEGIES = ("greedy_disjoint", "top1", "topk", "threshold", "best_pair_avg_disjoint", "{slug}")', content)
        
        impl = f"""
    if strategy == "{slug}":
        print(f"[VERIFIED] Executing Logic ID: {slug}")
        import math
        from math import exp, tanh, sqrt, log
        scored_cands = []
        for t in candidates:
            combined_score = -9.9
            try:
{logic_body}
            except Exception: combined_score = 0.0
            scored_cands.append(TripletCandidate(i=t.i, j=t.j, k=t.k, score=combined_score, is_truth=t.is_truth, triplet_pt=t.triplet_pt, triplet_eta=t.triplet_eta, triplet_phi=t.triplet_phi, triplet_mass=t.triplet_mass, mij_ab=t.mij_ab, mij_ac=t.mij_ac, mij_bc=t.mij_bc, dr_ab=t.dr_ab, dr_ac=t.dr_ac, dr_bc=t.dr_bc, ratio_ab=t.ratio_ab, ratio_ac=t.ratio_ac, ratio_bc=t.ratio_bc))
        return _solve_exact_disjoint(scored_cands, max_top=max_top_per_event)
"""
        new_content = content.replace('candidates = _sorted_candidates(triplets)', f'candidates = _sorted_candidates(triplets)\n{impl}')
        with open(SCRIPT_PATH, "w") as f: f.write(new_content)

        cmd = f"PYTHONPATH={PIPELINE_DIR}/top_reco/src /global/homes/v/vinny/.conda/envs/topml/bin/python -u -m triplet_ml select_triplets --inference {PIPELINE_DIR}/artifacts/run_prof/infer_eval/inference_test_xgb.parquet --strategy {slug} --output-dir artifacts/eval_stable --max-top-per-event 4 --no-progress"
        res_run = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if "[VERIFIED]" not in res_run.stdout: return 0.0
        
        res = subprocess.run(f"agent_kit/.venv/bin/python3 {WORK_DIR}/real_eval.py artifacts/eval_stable/selected_triplets.parquet 0 5000", shell=True, capture_output=True, text=True)
        return float(res.stdout.split("Efficiency: ")[1].split("+/-")[0].strip()) if "Efficiency" in res.stdout else 0.0

    def run(self):
        self.log("=== Top Reconstruction Marathon v18.9.1 (RESTORED STABLE HOOK) ===")
        while True:
            with open(CHAMP_PATH, "r") as f: champ = json.load(f)
            refine_prob = 0.10 + (0.80 - 0.10) * math.exp(-self.stale_iters / 500.0)
            is_ref = random.random() < refine_prob
            
            if is_ref:
                prompt = f"Refine logic: {champ['logic']}. JSON ONLY."
            else:
                prompt = f"Propose RADICAL new scoring logic. Features: t.triplet_mass, t.ratio_ab, t.dr_ab. DO NOT use 'base_score'. JSON ONLY."

            response = self.call_model(prompt, is_mutation=(not is_ref))
            if not response: 
                time.sleep(10)
                continue
            
            try:
                discovery = json.loads(re.search(r"\{.*\}", response, re.DOTALL).group())
                eff = self.run_eval(discovery)
                self.log(f"Round {self.iter_idx}: Result: {eff:.4f}")
                if eff > LOCAL_BENCHMARK:
                    self.log(f"*** Breakthrough: {eff:.4f} ***")
                    champ.update({"efficiency": eff, "slug": discovery["slug"], "logic": discovery["logic"]})
                    with open(CHAMP_PATH, "w") as f: json.dump(champ, f, indent=2)
                    self.stale_iters = 0
                else: self.stale_iters += 1
                self.iter_idx += 1
            except: self.iter_idx += 1

if __name__ == "__main__":
    DiscoveryHarness().run()
