import os, json, time, math, subprocess, re, random, csv, sys
import pyarrow.parquet as pq
import numpy as np
from scipy.optimize import minimize

# --- CONFIGURATION ---
WORK_DIR = "/global/u1/v/vinny/projects/topreco-agent"
DATA_PATH = f"{WORK_DIR}/artifacts/v20_2k_sample.parquet"
LAB_PATH = f"{WORK_DIR}/labbook.md"
CHAMP_PATH = f"{WORK_DIR}/champion_state.json"
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = "https://api.cborg.lbl.gov/v1/chat/completions"
MODEL = "lbl/gpt-oss-120b"
LOCAL_BENCHMARK = 0.6151

class EndToEndDiscoveryEngine:
    def __init__(self):
        self.iter_idx = 700000
        self.load_data()

    def log(self, msg):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("marathon_v24.log", "a") as f: f.write(f"[{ts}] {msg}\n"); f.flush()
        print(f"[{ts}] {msg}", flush=True)

    def load_data(self):
        self.table = pq.read_table(DATA_PATH)
        self.df = self.table.to_pydict()
        self.is_truth = np.array(self.df['is_truth'])
        self.n_triplets = len(self.table)
        self.eids = np.array(self.df['event_id'])
        self.jets = [frozenset([self.df['i'][i], self.df['j'][i], self.df['k'][i]]) for i in range(self.n_triplets)]
        self.features = {
            'm123': np.array(self.df['m123']), 'pt': np.array(self.df['triplet_pt']),
            'eta': np.array(self.df['triplet_eta']), 'score_xgb': np.array(self.df['score_xgb']),
            'r_ab': np.array(self.df['mij_over_m123_ab']), 'dr_ab': np.array(self.df['dr_ab'])
        }

    def call_model(self, prompt):
        payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.8}
        cmd = ["curl", "-s", "-X", "POST", BASE_URL, "-H", "Content-Type: application/json", "-H", f"Authorization: Bearer {API_KEY}", "-d", json.dumps(payload), "--max-time", "120"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(res.stdout)["choices"][0]["message"]["content"]
        except: return None

    def evaluate_end_to_end(self, logic):
        # 1. OPTIMIZE FOR EFFICIENCY DIRECTLY
        def get_eff(w):
            ns = {'np': np, 'math': math, 'w': w}; ns.update(self.features)
            try:
                exec(logic, ns)
                scores = ns.get('final_scores')
                if scores is None: return 0.0
                
                # --- FAST INTERNAL SELECTION ---
                n_correct = 0
                # Group triplets by event (pre-cached for speed in real implementation)
                # For optimization, we use a greedy approach inside the objective
                used_jets = {}
                indices = np.argsort(scores)[::-1]
                for idx in indices:
                    eid = self.eids[idx]
                    if eid not in used_jets: used_jets[eid] = set()
                    t_jets = self.jets[idx]
                    if not (t_jets & used_jets[eid]):
                        if self.is_truth[idx]: n_correct += 1
                        used_jets[eid].update(t_jets)
                return -(n_correct / sum(self.is_truth)) # Minimize negative efficiency
            except: return 0.0

        opt_res = minimize(get_eff, np.array([1.0]*10), method='Nelder-Mead', options={'maxiter': 20})
        return -opt_res.fun, opt_res.x

    def run(self):
        self.log("=== v24.0: End-to-End Efficiency Optimization ===")
        while True:
            prompt = """You are a HEP Architect. 
TASK: Design a multi-layer scoring logic (final_scores) that maximizes selection efficiency.
Features: m123, pt, eta, score_xgb, r_ab, dr_ab.
Return JSON ONLY: {"scoring_logic": "...", "slug": "v24_..."}"""
            
            response = self.call_model(prompt)
            if not response: continue
            try:
                discovery = json.loads(re.search(r"\{.*\}", response, re.DOTALL).group())
                eff, weights = self.evaluate_end_to_end(discovery['scoring_logic'])
                self.log(f"Round {self.iter_idx}: {discovery['slug']} -> Efficiency: {eff:.4f}")
                
                if eff > LOCAL_BENCHMARK:
                    self.log(f"*** BREAKTHROUGH: {eff:.4f} surpasses champion! ***")
                    # (Verification logic...)
                
                self.iter_idx += 1
            except: self.iter_idx += 1

if __name__ == "__main__":
    EndToEndDiscoveryEngine().run()
