import os, json, time, math, subprocess, urllib.request, re, random, csv, sys
import pyarrow.parquet as pq
import numpy as np
from scipy.optimize import minimize

# --- CONFIGURATION ---
WORK_DIR = "/global/u1/v/vinny/projects/topreco-agent"
DATA_PATH = f"{WORK_DIR}/artifacts/v20_2k_sample.parquet"
LAB_PATH = f"{WORK_DIR}/labbook.md"
CHAMP_PATH = f"{WORK_DIR}/champion_state.json"
TRAJECTORY_PATH = f"{WORK_DIR}/v20_trajectory.csv"
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = "https://api.cborg.lbl.gov/v1/chat/completions"
MODEL = "lbl/gpt-oss-120b-high"

class V20DiscoveryHarness:
    def __init__(self):
        self.stale_iters = 0
        self.start_time = time.time()
        self.iter_idx = 700
        self.load_data()

    def log(self, msg):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("v20_marathon.log", "a") as f: f.write(f"[{ts}] {msg}\n")
        print(f"[{ts}] {msg}", flush=True)

    def load_data(self):
        self.table = pq.read_table(DATA_PATH)
        self.df = self.table.to_pydict()
        self.n_triplets = len(self.table)
        self.is_truth = np.array(self.df['is_truth'])
        # Save features to a temporary npz for the standalone script to load
        np.savez("temp_features.npz", 
                 m123=np.array(self.df['m123']),
                 pt=np.array(self.df['triplet_pt']),
                 eta=np.array(self.df['triplet_eta']),
                 score_xgb=np.array(self.df['score_xgb']),
                 r_ab=np.array(self.df['mij_over_m123_ab']),
                 dr_ab=np.array(self.df['dr_ab']),
                 is_truth=self.is_truth)

    def call_model(self, prompt):
        data = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.9}).encode("utf-8")
        req = urllib.request.Request(BASE_URL, data=data, headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode())["choices"][0]["message"]["content"]
        except: return None

    def evaluate_architecture(self, discovery_json):
        # 1. Write the STANDALONE AGENT SCRIPT
        with open("discovered_logic.py", "w") as f:
            f.write("import numpy as np\n")
            f.write("def get_scores(w, data):\n")
            # Inject Features
            f.write("    m123, pt, eta, score_xgb, r_ab, dr_ab = data['m123'], data['pt'], data['eta'], data['score_xgb'], data['r_ab'], data['dr_ab']\n")
            # Inject Logic (ensure indentation)
            lines = discovery_json['parametric_formula'].split('\n')
            for l in lines: f.write(f"    {l.strip()}\n")
            f.write("    return final_scores\n\n")
            
            f.write(discovery_json['selection_heuristic'])

        # 2. Optimization using the script
        import discovered_logic
        import importlib
        importlib.reload(discovered_logic)
        
        data = np.load("temp_features.npz")
        
        def objective(w):
            try:
                scores = discovered_logic.get_scores(w, data)
                sig = np.mean(scores[data['is_truth'] == 1])
                bkg = np.mean(scores[data['is_truth'] == 0])
                return -(sig / (bkg + 1e-6))
            except: return 0.0

        initial_w = np.array(discovery_json.get("initial_weights", [1.0]*10))
        opt_res = minimize(objective, initial_w, method='Nelder-Mead', options={'maxiter': 50})
        best_w = opt_res.x

        # 3. Efficiency Calculation
        final_scores = discovered_logic.get_scores(best_w, data)
        
        # Selection Heuristic execution
        # Group by event
        event_triplets = {}
        for i, eid in enumerate(self.df['event_id']):
            if eid not in event_triplets: event_triplets[eid] = []
            event_triplets[eid].append({
                'idx': i, 'jets': frozenset([self.df['i'][i], self.df['j'][i], self.df['k'][i]]),
                'score': float(final_scores[i]), 'is_truth': bool(self.df['is_truth'][i])
            })

        n_correct = 0
        total_truth = sum(1 for v in self.is_truth if v == 1)
        for eid, candidates in event_triplets.items():
            try:
                chosen = discovered_logic.select(candidates)
                for c in chosen:
                    if c['is_truth']: n_correct += 1
            except: pass
        
        return n_correct / total_truth, best_w

    def run(self):
        self.log("=== V20.4: Standalone Module Architecture Search ===")
        while True:
            prompt = """You are a Deep Learning Architect.
TASK: Write two specific Python components.
1. 'parametric_formula': Lines of code defining 'final_scores' (a numpy array). 
   Available: m123, pt, eta, score_xgb, r_ab, dr_ab. Parameters: w[0], w[1], etc.
2. 'selection_heuristic': A function 'def select(candidates):' returning a list of chosen dicts.

Return JSON ONLY:
{
  "parametric_formula": "h1 = np.tanh(...)\\nfinal_scores = ...",
  "selection_heuristic": "def select(candidates):\\n    ...",
  "initial_weights": [1.0, ...],
  "slug": "v20_mod_..."
}
"""
            response = self.call_model(prompt)
            if not response: continue
            
            try:
                match = re.search(r"\{.*\}", response, re.DOTALL)
                discovery = json.loads(match.group())
                eff, weights = self.evaluate_architecture(discovery)
                self.log(f"Round {self.iter_idx}: {discovery['slug']} -> Efficiency: {eff:.4f}")
                
                with open(LAB_PATH, "a") as f:
                    f.write(f"\n#### Round {self.iter_idx}: Module Search ({discovery['slug']})\n- Efficiency: {eff:.4f}\n")
                
                self.iter_idx += 1
            except Exception as e:
                self.log(f"  [Failure] {e}")
                self.iter_idx += 1
            time.sleep(2)

if __name__ == "__main__":
    V20DiscoveryHarness().run()
