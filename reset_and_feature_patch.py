import os
import subprocess
import re

path = "/global/u1/v/vinny/projects/topreconstruction/top_reco/src/triplet_ml/select_triplets.py"

# Reset to Origin
subprocess.run(f"cd /global/u1/v/vinny/projects/topreconstruction && git checkout top_reco/src/triplet_ml/select_triplets.py", shell=True)

with open(path, "r") as f:
    content = f.read()

# REMOVE ALL OLD AGENT BLOCKS (Strict Reset)
# We look for the start of _apply_strategy and the start of greedy_disjoint
start_marker = "candidates = _sorted_candidates(triplets)"
end_marker = 'if strategy == "greedy_disjoint":'

parts = content.split(start_marker)
tail_parts = parts[1].split(end_marker)
content = parts[0] + start_marker + "\n\n    " + end_marker + tail_parts[1]

# Re-inject solver and features
solver = """
def _solve_exact_disjoint(candidates, max_top):
    subset = candidates[:30]
    best_sum = -1.0
    best_set = []
    def search(idx, sel, cur_sum, used):
        nonlocal best_sum, best_set
        if cur_sum > best_sum:
            best_sum, best_set = cur_sum, list(sel)
        if len(sel) >= max_top or idx >= len(subset): return
        for i in range(idx, len(subset)):
            c = subset[i]; jts = {c.i, c.j, c.k}
            if not (jts & used): search(i + 1, sel + [c], cur_sum + c.score, used | jts)
    search(0, [], 0.0, set())
    return best_set
"""
content = content.replace("def _apply_strategy(", solver + "\ndef _apply_strategy(")
content = content.replace("    triplet_mass: float", "    triplet_mass: float\n    mij_ab: float\n    mij_ac: float\n    mij_bc: float\n    dr_ab: float\n    dr_ac: float\n    dr_bc: float\n    ratio_ab: float\n    ratio_ac: float\n    ratio_bc: float")
content = content.replace('        "is_truth",', '        "is_truth",\n        "mij_ab", "mij_ac", "mij_bc", "dr_ab", "dr_ac", "dr_bc", "mij_over_m123_ab", "mij_over_m123_ac", "mij_over_m123_bc",')
content = content.replace('triplet_mass=float(payload["m123"][idx]),', 'triplet_mass=float(payload["m123"][idx]),\n                    mij_ab=float(payload["mij_ab"][idx]),\n                    mij_ac=float(payload["mij_ac"][idx]),\n                    mij_bc=float(payload["mij_bc"][idx]),\n                    dr_ab=float(payload["dr_ab"][idx]),\n                    dr_ac=float(payload["dr_ac"][idx]),\n                    dr_bc=float(payload["dr_bc"][idx]),\n                    ratio_ab=float(payload["mij_over_m123_ab"][idx]),\n                    ratio_ac=float(payload["mij_over_m123_ac"][idx]),\n                    ratio_bc=float(payload["mij_over_m123_bc"][idx]),')

# Ensure STRATEGIES is clean
content = re.sub(r'STRATEGIES = \(.*?\)', 'STRATEGIES = ("greedy_disjoint", "top1", "topk", "threshold", "best_pair_avg_disjoint")', content)

with open(path, "w") as f:
    f.write(content)
