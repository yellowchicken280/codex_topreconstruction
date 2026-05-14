import os, sys, math, json
import numpy as np
import pyarrow.parquet as pq
from scipy.optimize import minimize

# --- DATA CONFIGURATION ---
DATA_PATH = "artifacts/v20_2k_sample.parquet"

def load_data():
    table = pq.read_table(DATA_PATH)
    df = table.to_pydict()
    return df

def get_final_scores(w, f):
    target = 162.0
    sigma = 18.0 if np.all(f['m123'] >= target) else 25.0
    m_prior = np.exp(-0.5 * ((f['m123'] - target)/sigma)**2)
    r_dev = (np.abs(f['r_ab'] - 0.46) + np.abs(f['r_ac'] - 0.46) + np.abs(f['r_bc'] - 0.46)) / 3.0
    r_prior = np.exp(-(r_dev**2) / 0.02)
    
    # ADVANCED GEOMETRIC SUPERVISION (Phase VII Round 5)
    # w[0-4] are from the previous round baseline
    # w[5-7] are the new Geometric Attention weights
    
    # 1. Base MLP synergy
    h1 = np.tanh(w[0]*f['triplet_pt']/200.0 + w[1]*f['score_xgb'])
    
    # 2. Spatial Gating (The Tanh "Step" discovered earlier, now optimized)
    # Learns where to trust the classifier based on |eta|
    spatial_gate = 1.0 + w[5] * np.tanh(w[6] - np.abs(f['triplet_eta']))
    
    # 3. Final Multiplicative Fusion
    final_scores = f['score_xgb'] * m_prior * r_prior * np.maximum(1e-6, h1 + w[4]) * spatial_gate
    return final_scores

def select_triplets(candidates):
    sorted_cands = sorted(candidates, key=lambda x: x['score'], reverse=True)
    beams = [([], set(), 0.0)]
    for cand in sorted_cands[:30]:
        new_beams = []
        for chosen, used, total_score in beams:
            new_beams.append((chosen, used, total_score))
            if not (cand['jets'] & used):
                new_beams.append((chosen + [cand], used | cand['jets'], total_score + cand['score']))
        new_beams.sort(key=lambda x: x[2], reverse=True)
        beams = new_beams[:5]
    return beams[0][0]

def run_benchmark():
    df = load_data()
    i_arr, j_arr, k_arr = np.array(df['i']), np.array(df['j']), np.array(df['k'])
    all_f = {
        'm123': np.array(df['m123']), 'triplet_pt': np.array(df['triplet_pt']),
        'triplet_eta': np.array(df['triplet_eta']), 'score_xgb': np.array(df['score_xgb']),
        'r_ab': np.array(df['mij_over_m123_ab']), 'r_ac': np.array(df['mij_over_m123_ac']), 'r_bc': np.array(df['mij_over_m123_bc']),
    }
    is_truth = np.array(df['is_truth'])
    eids = np.array(df['event_id'])
    
    # Use larger training sample for Round 5 (200 events)
    train_mask = np.isin(eids, np.unique(eids)[:200])
    
    def objective(w):
        f_sub = {k: v[train_mask] for k, v in all_f.items()}
        scores = get_final_scores(w, f_sub)
        eids_sub = eids[train_mask]
        truth_sub = is_truth[train_mask]
        i_sub, j_sub, k_sub = i_arr[train_mask], j_arr[train_mask], k_arr[train_mask]
        
        n_correct = 0
        ev_map = {}
        for idx in range(len(scores)):
            eid = eids_sub[idx]
            if eid not in ev_map: ev_map[eid] = []
            ev_map[eid].append({'jets': {int(i_sub[idx]), int(j_sub[idx]), int(k_sub[idx])}, 'score': float(scores[idx]), 'truth': bool(truth_sub[idx])})
        
        for eid, cands in ev_map.items():
            chosen = select_triplets(cands)
            for c in chosen:
                if c['truth']: n_correct += 1
        return -n_correct

    print("Running Spatial Attention Optimization (v30.7)...")
    # Seeding with the successful baseline weights
    initial_w = np.array([1.0, 0.1, -0.1, 0.5, 1.0, 0.05, 1.5, 1.0])
    opt = minimize(objective, initial_w, method='Nelder-Mead', options={'maxiter': 15})
    
    # FULL EVALUATION
    final_scores = get_final_scores(opt.x, all_f)
    n_correct = 0
    event_map = {}
    for idx in range(len(eids)):
        eid = eids[idx]
        if eid not in event_map: event_map[eid] = []
        event_map[eid].append({'jets': {int(i_arr[idx]), int(j_arr[idx]), int(k_arr[idx])}, 'score': float(final_scores[idx]), 'truth': bool(is_truth[idx])})
    
    for eid, cands in event_map.items():
        chosen = select_triplets(cands)
        used = set()
        for c in chosen:
            if not (c['jets'] & used):
                if c['truth']: n_correct += 1
                used.update(c['jets'])
    
    print(f"METRIC_EFFICIENCY: {n_correct / sum(is_truth):.4f}")

if __name__ == "__main__":
    run_benchmark()
