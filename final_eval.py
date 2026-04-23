import pyarrow.parquet as pq
import math

# Paths for run_prof eval
truth_path = "/global/u1/v/vinny/projects/topreconstruction/artifacts/run_10000/dataset_prepare/test.parquet"
infer_path = "/global/u1/v/vinny/projects/topreconstruction/artifacts/run_prof/infer_eval/inference_test_xgb.parquet"

# Load truth (first 2000 events only)
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
n_total_truth = sum(len(truth_by_event.get(eid, set())) for eid in ordered_ids)
print(f"Total truth triplets in test set (first 2000 events): {n_total_truth}")

# Load inference
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

def evaluate_greedy(gamma, m_target, sigma, w_sigma):
    n_correct = 0
    for eid, group in events.items():
        scored = []
        for row in group:
            diff_ab = abs(row["mij_ab"] - 80.4)
            diff_ac = abs(row["mij_ac"] - 80.4)
            diff_bc = abs(row["mij_bc"] - 80.4)
            best_diff = min(diff_ab, diff_ac, diff_bc)
            
            w_prior = math.exp(-0.5 * (best_diff / w_sigma)**2)
            top_prior = math.exp(-0.5 * ((row["m123"] - m_target) / sigma)**2)
            
            score = (max(row["score"], 1e-6) ** gamma) * top_prior * w_prior
            scored.append((score, frozenset([row["i"], row["j"], row["k"]])))
            
        scored.sort(key=lambda x: -x[0])
        
        selected_triplets = []
        used_jets = set()
        
        for score, triplet in scored:
            if len(selected_triplets) >= 4:
                break
            if used_jets.isdisjoint(triplet):
                selected_triplets.append(triplet)
                used_jets.update(triplet)
                
        truth = truth_by_event.get(eid, set())
        for sel in selected_triplets:
            if sel in truth:
                n_correct += 1
                
    return n_correct / n_total_truth
def evaluate_new_strategy():
    n_correct = 0
    for eid, group in events.items():
        scored = []
        for row in group:
            diff_ab = abs(row["mij_ab"] - 80.4)
            diff_ac = abs(row["mij_ac"] - 80.4)
            diff_bc = abs(row["mij_bc"] - 80.4)
            best_diff = min(diff_ab, diff_ac, diff_bc)
            
            # Asymmetric top prior
            if row["m123"] >= 162.0:
                top_prior = math.exp(-0.5 * ((row["m123"] - 162.0) / 20.0)**2)
            else:
                top_prior = math.exp(-0.5 * ((row["m123"] - 162.0) / 30.0)**2)
                
            w_prior = math.exp(-0.5 * (best_diff / 20.0)**2)
            
            score = (max(row["score"], 1e-6) ** 1.0) * top_prior * w_prior
            scored.append((score, frozenset([row["i"], row["j"], row["k"]])))
            
        scored.sort(key=lambda x: -x[0])
        
        selected_triplets = []
        used_jets = set()
        
        for score, triplet in scored:
            if len(selected_triplets) >= 4:
                break
            if used_jets.isdisjoint(triplet):
                selected_triplets.append(triplet)
                used_jets.update(triplet)
                
        truth = truth_by_event.get(eid, set())
        for sel in selected_triplets:
            if sel in truth:
                n_correct += 1
                
    return n_correct / n_total_truth


def evaluate_exact(gamma, m_target, sigma, w_sigma):
    n_correct = 0
    for eid, group in events.items():
        scored = []
        for row in group:
            diff_ab = abs(row["mij_ab"] - 80.4)
            diff_ac = abs(row["mij_ac"] - 80.4)
            diff_bc = abs(row["mij_bc"] - 80.4)
            best_diff = min(diff_ab, diff_ac, diff_bc)
            
            w_prior = math.exp(-0.5 * (best_diff / w_sigma)**2)
            top_prior = math.exp(-0.5 * ((row["m123"] - m_target) / sigma)**2)
            
            score = (max(row["score"], 1e-6) ** gamma) * top_prior * w_prior
            scored.append((score, frozenset([row["i"], row["j"], row["k"]])))
            
        scored.sort(key=lambda x: -x[0])
        scored = scored[:30]
        
        best_sum_score = -1.0
        best_set = []
        
        def find_best_subset(current_idx, current_disjoint, current_score):
            nonlocal best_sum_score, best_set
            if current_score > best_sum_score:
                best_sum_score = current_score
                best_set = list(current_disjoint)
            
            if len(current_disjoint) >= 4 or current_idx >= len(scored):
                return
                
            for i in range(current_idx, len(scored)):
                score, triplet = scored[i]
                if all(triplet.isdisjoint(sel) for sel in current_disjoint):
                    find_best_subset(i + 1, current_disjoint + [triplet], current_score + score)
                    
        find_best_subset(0, [], 0.0)
        
        truth = truth_by_event.get(eid, set())
        for sel in best_set:
            if sel in truth:
                n_correct += 1
                
    return n_correct / n_total_truth

# Professor's suggested parameters from feedback
gamma = 0.45
m_target = 162.0
sigma_top = 22.5
w_sigma = 24.0

eff_greedy = evaluate_greedy(gamma, m_target, sigma_top, w_sigma)
print(f"Greedy disjoint efficiency on 30k events: {eff_greedy:.4f}")

eff_exact = evaluate_exact(gamma, m_target, sigma_top, w_sigma)
print(f"Exact disjoint efficiency on 30k events: {eff_exact:.4f}")

eff_new = evaluate_new_strategy()
print(f"New strategy efficiency: {eff_new:.4f}")
