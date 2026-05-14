import os, json, time, math, subprocess, re, random, csv, sys, traceback, ast
import pyarrow.parquet as pq
import numpy as np
from scipy.optimize import minimize
from multiprocessing import Process, Queue

# --- CONFIGURATION ---
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = "https://api.cborg.lbl.gov/v1/chat/completions"
MODEL = "openai/gpt-4o"
DATA_PATH = "artifacts/v20_2k_sample.parquet"
LAB_PATH = "research_log.md"

def selection_wrapper(select_func, cands, result_queue):
    try:
        chosen = select_func(cands)
        if chosen is None: chosen = []
        result_queue.put(list(chosen))
    except:
        result_queue.put([])

class ActionRouterHarness:
    def __init__(self):
        self.iter_idx = 1
        self.load_data()

    def log(self, msg):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LAB_PATH, "a") as f: f.write(msg + "\n"); f.flush()
        print(f"[{ts}] {msg}", flush=True)

    def load_data(self):
        print(f"[INIT] Loading benchmark data...", flush=True)
        table = pq.read_table(DATA_PATH)
        df = table.to_pydict()
        self.f = {
            'm123': np.array(df['m123']), 'pt': np.array(df['triplet_pt']),
            'eta': np.array(df['triplet_eta']), 'score_xgb': np.array(df['score_xgb']),
            'm_ab': np.array(df['mij_ab']), 'm_ac': np.array(df['mij_ac']), 'm_bc': np.array(df['mij_bc']),
            'r_ab': np.array(df['mij_over_m123_ab']), 'r_ac': np.array(df['mij_over_m123_ac']), 'r_bc': np.array(df['mij_over_m123_bc']),
            'dr_ab': np.array(df['dr_ab']), 'dr_ac': np.array(df['dr_ac']), 'dr_bc': np.array(df['dr_bc'])
        }
        self.is_truth = np.array(df['is_truth'])
        self.event_ids = np.array(df['event_id'])
        self.triplets = [{'jets': frozenset([df['i'][i], df['j'][i], df['k'][i]]), 'truth': bool(self.is_truth[i])} for i in range(len(self.is_truth))]

    def call_model(self, prompt):
        print("[API] Requesting architecture...", flush=True)
        payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.5}
        cmd = ["curl", "-s", "-X", "POST", BASE_URL, "-H", "Content-Type: application/json", "-H", f"Authorization: Bearer {API_KEY}", "-d", json.dumps(payload), "--max-time", "180"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(res.stdout)
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[API ERROR] {e}", flush=True)
            return None

    def evaluate(self, discovery):
        logic = discovery.get("scoring_logic", "final_scores = 1.0")
        heuristic = discovery.get("selection_heuristic", "def select_triplets(c): return sorted(c, key=lambda x: x['score'], reverse=True)[:1]")
        slug = discovery.get('slug', 'arch_v30_3')
        
        # --- v30.3 PHYSICS MANDATE ---
        # 1. We pre-calculate the Champion Logic (162 GeV peak, 0.46 ratio)
        # 2. We force the agent's logic to MULTIPLY this baseline.
        logic_base = """
# Mandatory Physics Layer (0.6135 Baseline)
target = 162.0
sigma = 18.0 if np.all(f['m123'] >= target) else 25.0 # simplified but representative
m_prior = np.exp(-0.5 * ((f['m123'] - target)/sigma)**2)
r_dev = (np.abs(f['r_ab'] - 0.46) + np.abs(f['r_ac'] - 0.46) + np.abs(f['r_bc'] - 0.46)) / 3.0
r_prior = np.exp(-(r_dev**2) / 0.02)
base_prior = f['score_xgb'] * m_prior * r_prior
"""
        logic_fortified = logic_base + "\n" + logic + "\nfinal_scores = base_prior * np.maximum(1e-6, final_scores)"

        print(f"[TRAIN] Optimizing {slug}...", flush=True)
        sub_mask = np.random.choice([True, False], size=len(self.is_truth), p=[0.2, 0.8])
        def objective(w):
            ns = {'np': np, 'math': math, 'w': w, 'f': {k: v[sub_mask] for k, v in self.f.items()}}
            try:
                exec(logic_fortified, ns)
                fs = ns.get('final_scores')
                return -np.mean(fs[self.is_truth[sub_mask] == 1]) / (np.mean(fs[fs >= 0]) + 1e-6)
            except: return 0.0
        
        # Optimize on top of baseline
        initial_w = np.array([1.0]*15)
        opt_res = minimize(objective, initial_w, method='Nelder-Mead', options={'maxiter': 10})
        
        print("[SELECT] Scoring...", flush=True)
        ns_eval = {'np': np, 'math': math, 'w': opt_res.x, 'f': self.f}; exec(logic_fortified, ns_eval)
        final_scores = np.nan_to_num(ns_eval.get('final_scores'), nan=-9.9)

        event_map = {}
        for i, eid in enumerate(self.event_ids):
            if eid not in event_map: event_map[eid] = []
            cand = self.triplets[i].copy(); cand['score'] = float(final_scores[i])
            event_map[eid].append(cand)

        ns_sel = {'sorted': sorted, 'set': set, 'frozenset': frozenset, 'np': np, 'math': math}
        try: 
            exec(heuristic, ns_sel)
            select_func = ns_sel.get('select_triplets')
        except: select_func = None

        n_correct = 0
        for eid, cands in event_map.items():
            chosen = []
            if select_func:
                q = Queue(); p = Process(target=selection_wrapper, args=(select_func, cands, q))
                p.start(); p.join(timeout=0.1)
                if p.is_alive(): p.terminate(); chosen = []
                else: chosen = q.get() if not q.empty() else []
            if not isinstance(chosen, list): chosen = []
            if not chosen:
                used = set()
                for c in sorted(cands, key=lambda x: x['score'], reverse=True):
                    if not (c['jets'] & used): chosen.append(c); used.update(c['jets'])
            for c in chosen:
                if isinstance(c, dict) and c.get('truth'): n_correct += 1
        return n_correct / sum(self.is_truth)

    def run(self):
        print(f"=== v30.3 Physics-Mandated Engine (LOCKED IN) ===", flush=True)
        while True:
            try:
                with open("prompt_system.md", "r") as f: system = f.read()
                with open("prompt_problem.md", "r") as f: problem = f.read()
                prompt = f"{system}\n\n{problem}\n\nTASK: Propose Scoring and Selection. JSON ONLY."
                response = self.call_model(prompt)
                if not response: continue
                
                match = re.search(r"\{.*\}", response, re.DOTALL)
                if not match: continue
                ld = {}
                exec(f"discovery = {match.group()}", {}, ld)
                discovery = ld['discovery']
                
                eff = self.evaluate(discovery)
                self.log(f"### Step {self.iter_idx}\n- Action Class: {discovery.get('action_class', 'Search')}\n- Efficiency: {eff:.4f}\n- Rationale: {discovery.get('rationale', 'None')}\n")
                self.iter_idx += 1
            except Exception:
                print(f"[CRITICAL ERROR]\n{traceback.format_exc()}", flush=True)
                self.iter_idx += 1
            time.sleep(10)

if __name__ == "__main__":
    ActionRouterHarness().run()
