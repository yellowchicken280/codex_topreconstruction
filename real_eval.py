import pyarrow.parquet as pq
import os
import sys
import math

truth_path = "/global/u1/v/vinny/projects/topreconstruction/artifacts/run_10000/dataset_prepare/test.parquet"

def evaluate(selected_path, event_slice_start=0, event_slice_count=2000):
    if not os.path.exists(selected_path):
        return 0.0, 0.0
    
    # 1. Determine the specified event ID slice
    truth_table_all = pq.read_table(truth_path, columns=["event_id"])
    all_eids = truth_table_all["event_id"].to_pylist()
    
    unique_eids = []
    seen = set()
    for eid in all_eids:
        if eid not in seen:
            seen.add(eid)
            unique_eids.append(eid)
    
    eval_eids_slice = unique_eids[event_slice_start : event_slice_start + event_slice_count]
    eval_eids_set = set(eval_eids_slice)
    
    # 2. Get truth triplets
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
        return 0.0, 0.0

    n_correct = 0
    for idx in range(len(sel_eids)):
        eid = int(sel_eids[idx])
        if eid in truth_by_event:
            triplet = frozenset([int(sel_i[idx]), int(sel_j[idx]), int(sel_k[idx])])
            if triplet in truth_by_event[eid]:
                n_correct += 1
                
    if n_total_truth == 0: return 0.0, 0.0
    
    eff = n_correct / n_total_truth
    # Standard Binomial Error: sqrt(p(1-p)/N)
    err = math.sqrt((eff * (1 - eff)) / n_total_truth)
    
    return eff, err

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python real_eval.py <path> [start] [count]")
        sys.exit(1)
    path = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    
    eff, err = evaluate(path, start, count)
    print(f"Efficiency: {eff:.4f} +/- {err:.4f}")
