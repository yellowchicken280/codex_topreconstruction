import pyarrow.parquet as pq
import os
import sys

truth_path = "/global/u1/v/vinny/projects/topreconstruction/artifacts/run_10000/dataset_prepare/test.parquet"

def evaluate(selected_path):
    if not os.path.exists(selected_path):
        return 0.0
    
    # 1. Determine the first 2000 event IDs
    truth_table_all = pq.read_table(truth_path, columns=["event_id"])
    all_eids = truth_table_all["event_id"].to_pylist()
    
    seen_eids = set()
    first_2k_ordered = []
    for eid in all_eids:
        if eid not in seen_eids:
            seen_eids.add(eid)
            first_2k_ordered.append(eid)
            if len(first_2k_ordered) >= 2000:
                break
    
    eval_eids_set = set(first_2k_ordered)
    
    # 2. Get truth triplets and denominator for these 2000 events
    truth_table = pq.read_table(truth_path)
    tr_eids = truth_table["event_id"].to_pylist()
    tr_truth = truth_table["is_truth"].to_pylist()
    tr_i = truth_table["i"].to_pylist()
    tr_j = truth_table["j"].to_pylist()
    tr_k = truth_table["k"].to_pylist()
    
    truth_by_event = {}
    n_total_truth = 0
    for idx in range(len(tr_eids)):
        eid = int(tr_eids[idx])
        if eid in eval_eids_set and int(tr_truth[idx]) == 1:
            truth_by_event.setdefault(eid, set()).add(frozenset([int(tr_i[idx]), int(tr_j[idx]), int(tr_k[idx])]))
            n_total_truth += 1
            
    # 3. Evaluate selections
    try:
        sel_table = pq.read_table(selected_path)
        sel_eids = sel_table["event_id"].to_pylist()
        sel_i = sel_table["i"].to_pylist()
        sel_j = sel_table["j"].to_pylist()
        sel_k = sel_table["k"].to_pylist()
    except:
        return 0.0

    n_correct = 0
    for idx in range(len(sel_eids)):
        eid = int(sel_eids[idx])
        if eid in truth_by_event:
            triplet = frozenset([int(sel_i[idx]), int(sel_j[idx]), int(sel_k[idx])])
            if triplet in truth_by_event[eid]:
                n_correct += 1
                
    if n_total_truth == 0: return 0.0
    return n_correct / n_total_truth

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        eff = evaluate(path)
        print(f"Efficiency: {eff:.4f}")
    else:
        print("Usage: python real_eval.py <path_to_selected_triplets.parquet>")
