import pyarrow.parquet as pq
import math
from itertools import combinations

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
n_total_events = sum(1 for eid in ordered_ids if eid in truth_by_event)

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

def evaluate_strategy_exact(gamma, m_target, sigma, w_sigma, min_score, size_penalty):
    n_correct_events = 0
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
            scored.append((score, frozenset([row["i"], row["j"], row["k"]])))
            
        # Top 30 triplets to reduce complexity
        scored.sort(key=lambda x: -x[0])
        scored = scored[:30]
        
        best_sum_score = -1.0
        best_set = []
        
        # Try finding the set of mutually disjoint triplets that maximizes the sum of scores
        # We can just use a recursive search
        def find_best_subset(current_idx, current_disjoint, current_score):
            nonlocal best_sum_score, best_set
            
            # Penalize size if we want to prefer fewer triplets with higher scores, or reward size
            penalized_score = current_score + len(current_disjoint) * size_penalty
            
            if penalized_score > best_sum_score:
                best_sum_score = penalized_score
                best_set = list(current_disjoint)
                
            if len(current_disjoint) >= 4 or current_idx >= len(scored):
                return
                
            for i in range(current_idx, len(scored)):
                score, triplet = scored[i]
                
                # Check disjoint
                is_disjoint = True
                for sel in current_disjoint:
                    if not triplet.isdisjoint(sel):
                        is_disjoint = False
                        break
                        
                if is_disjoint:
                    find_best_subset(i + 1, current_disjoint + [triplet], current_score + score)
                    
        find_best_subset(0, [], 0.0)
                    
        truth = truth_by_event.get(eid, set())
        matched = False
        for sel in best_set:
            if sel in truth:
                matched = True
                break
        if matched:
            n_correct_events += 1
                
    return n_correct_events / n_total_events

eff1 = evaluate_strategy_exact(0.45, 162.0, 22.5, 24.0, 0.0, 0.0)
eff2 = evaluate_strategy_exact(0.45, 162.0, 22.5, 24.0, 0.0, 0.5)
print(f"Exact disjoint: {eff1:.4f} (size_penalty 0.0)")
print(f"Exact disjoint: {eff2:.4f} (size_penalty 0.5)")

