import pyarrow.parquet as pq
import os
import sys

truth_path = "/global/u1/v/vinny/projects/topreconstruction/artifacts/run_10000/dataset_prepare/test.parquet"
n_total_truth = 1026 # verified for first 2000 events

def evaluate(selected_path):
    if not os.path.exists(selected_path):
        return 0.0
    
    # Load truth (first 2000 events)
    truth_table = pq.read_table(truth_path, columns=["event_id", "i", "j", "k", "is_truth"])
    eids = truth_table["event_id"].to_pylist()
    is_truth = truth_table["is_truth"].to_pylist()
    ii = truth_table["i"].to_pylist()
    jj = truth_table["j"].to_pylist()
    kk = truth_table["k"].to_pylist()
    
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
            truth_by_event.setdefault(eid, set()).add(frozenset([int(ii[idx]), int(jj[idx]), int(kk[idx])]))

    # Load selected
    try:
        sel_table = pq.read_table(selected_path, columns=["event_id", "i", "j", "k"])
        sel_eids = sel_table["event_id"].to_pylist()
        sel_i = sel_table["i"].to_pylist()
        sel_j = sel_table["j"].to_pylist()
        sel_k = sel_table["k"].to_pylist()
    except:
        return 0.0

    n_correct = 0
    for idx in range(len(sel_eids)):
        eid = int(sel_eids[idx])
        if eid not in truth_by_event: continue
        triplet = frozenset([int(sel_i[idx]), int(sel_j[idx]), int(sel_k[idx])])
        if triplet in truth_by_event[eid]:
            n_correct += 1
            
    return n_correct / n_total_truth

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        eff = evaluate(path)
        print(f"Efficiency: {eff:.4f}")
    else:
        print("Usage: python real_eval.py <path_to_selected_triplets.parquet>")
