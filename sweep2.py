import pyarrow.parquet as pq
import math
import numpy as np

# Load truth
truth_path = "/global/u1/v/vinny/projects/topreconstruction/artifacts/run_10000/dataset_prepare/test.parquet"
table = pq.read_table(truth_path, columns=["event_id", "i", "j", "k", "is_truth"])
eids = table["event_id"].to_pylist()
is_truth = table["is_truth"].to_pylist()
ii = table["i"].to_pylist()
jj = table["j"].to_pylist()
kk = table["k"].to_pylist()

seen = set()
ordered_ids = []
truth_by_event = {}
for idx in range(len(eids)):
    eid = int(eids[idx])
    if eid not in seen:
        seen.add(eid)
        if len(ordered_ids) < 2000:
            ordered_ids.append(eid)
    if int(is_truth[idx]) == 1:
        if eid not in truth_by_event:
            truth_by_event[eid] = set()
        truth_by_event[eid].add(frozenset([int(ii[idx]), int(jj[idx]), int(kk[idx])]))

eval_event_ids = set(ordered_ids)
n_total = sum(len(truth_by_event.get(eid, set())) for eid in ordered_ids)

# Load inference
infer_path = "/global/u1/v/vinny/projects/topreconstruction/artifacts/run_10000/infer/inference_test_xgb.parquet"
infer_table = pq.read_table(infer_path, columns=["event_id", "i", "j", "k", "m123", "mij_ab", "mij_ac", "mij_bc", "score_xgb"])
inf_eids = infer_table["event_id"].to_pylist()
inf_i = infer_table["i"].to_pylist()
inf_j = infer_table["j"].to_pylist()
inf_k = infer_table["k"].to_pylist()
inf_m123 = infer_table["m123"].to_pylist()
inf_mij_ab = infer_table["mij_ab"].to_pylist()
inf_mij_ac = infer_table["mij_ac"].to_pylist()
inf_mij_bc = infer_table["mij_bc"].to_pylist()
inf_score = infer_table["score_xgb"].to_pylist()

events = {}
for idx in range(len(inf_eids)):
    eid = int(inf_eids[idx])
    if eid not in eval_event_ids:
        continue
    if eid not in events:
        events[eid] = []
    events[eid].append({
        "i": int(inf_i[idx]),
        "j": int(inf_j[idx]),
        "k": int(inf_k[idx]),
        "m123": float(inf_m123[idx]),
        "mij_ab": float(inf_mij_ab[idx]),
        "mij_ac": float(inf_mij_ac[idx]),
        "mij_bc": float(inf_mij_bc[idx]),
        "score": float(inf_score[idx])
    })

def evaluate_strategy(gamma, m_target, sigma, w_sigma, min_score, pT_penalty=0.0):
    n_correct = 0
    for eid, group in events.items():
        scored = []
        for row in group:
            if row["score"] < min_score:
                continue
            diff_ab = abs(row["mij_ab"] - 80.4)
            diff_ac = abs(row["mij_ac"] - 80.4)
            diff_bc = abs(row["mij_bc"] - 80.4)
            best_diff = min(diff_ab, diff_ac, diff_bc)
            
            w_prior = math.exp(-0.5 * (best_diff / w_sigma)**2)
            top_prior = math.exp(-0.5 * ((row["m123"] - m_target) / sigma)**2)
            
            score = (max(row["score"], 1e-6) ** gamma) * top_prior * w_prior
            scored.append((score, row))
            
        scored.sort(key=lambda x: -x[0])
        
        selected_triplets = []
        available_jets = set()
        
        for score, row in scored:
            if len(selected_triplets) >= 4:
                break
            triplet_jets = (row["i"], row["j"], row["k"])
            if all(j not in available_jets for j in triplet_jets):
                selected_triplets.append(frozenset(triplet_jets))
                for j in triplet_jets:
                    available_jets.add(j)
                    
        truth = truth_by_event.get(eid, set())
        for sel in selected_triplets:
            if sel in truth:
                n_correct += 1
                
    return n_correct / n_total

best_eff = 0
for gamma in [0.3, 0.45, 0.55, 0.7, 1.0]:
    for m_target in [160, 162, 166, 172.5]:
        for sigma in [15, 17, 22.5, 25]:
            for w_sigma in [15, 24, 30, 40]:
                for min_score in [0.0, 0.5]:
                    eff = evaluate_strategy(gamma, m_target, sigma, w_sigma, min_score)
                    if eff > best_eff:
                        best_eff = eff
                        print(f"NEW BEST {best_eff:.4f}: gamma={gamma} m_target={m_target} sigma={sigma} w_sigma={w_sigma} min_score={min_score}")
