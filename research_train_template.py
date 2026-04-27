import os, sys, math, json
import numpy as np
import pyarrow.parquet as pq
from scipy.optimize import minimize

DATA_PATH = "artifacts/v20_2k_sample.parquet"

def get_final_scores(w, f):
# [SCORING_LOGIC_HERE]
    return final_scores

def select_triplets(candidates):
# [SELECTION_LOGIC_HERE]
    return chosen

def run_benchmark():
    table = pq.read_table(DATA_PATH)
    df = table.to_pydict()
    f = {
        'm123': np.array(df['m123']), 'pt': np.array(df['triplet_pt']),
        'eta': np.array(df['triplet_eta']), 'score_xgb': np.array(df['score_xgb']),
        'm_ab': np.array(df['mij_ab']), 'm_ac': np.array(df['mij_ac']), 'm_bc': np.array(df['mij_bc']),
        'r_ab': np.array(df['mij_over_m123_ab']), 'r_ac': np.array(df['mij_over_m123_ac']), 'r_bc': np.array(df['mij_over_m123_bc']),
        'dr_ab': np.array(df['dr_ab']), 'dr_ac': np.array(df['dr_ac']), 'dr_bc': np.array(df['dr_bc'])
    }
    is_truth = np.array(df['is_truth'])
    
    def objective(w):
        try:
            scores = get_final_scores(w, f)
            sig = np.mean(scores[is_truth == 1])
            bkg = np.mean(scores[is_truth == 0])
            return -(sig / (bkg + 1e-6))
        except: return 0.0
    
    opt = minimize(objective, np.array([1.0]*15), method='Nelder-Mead', options={'maxiter': 5})
    final_scores = get_final_scores(opt.x, f)
    
    event_map = {}
    for i in range(len(df['event_id'])):
        eid = df['event_id'][i]
        if eid not in event_map: event_map[eid] = []
        event_map[eid].append({'jets': {df['i'][i], df['j'][i], df['k'][i]}, 'score': float(final_scores[i]), 'truth': bool(is_truth[i])})
    
    n_correct = 0
    for eid, cands in event_map.items():
        try:
            chosen = select_triplets(cands)
            used = set()
            for c in chosen:
                if not (c['jets'] & used):
                    if c['truth']: n_correct += 1
                    used.update(c['jets'])
        except: pass
    
    print(f"METRIC_EFFICIENCY: {n_correct / sum(is_truth):.4f}")

if __name__ == "__main__":
    run_benchmark()
