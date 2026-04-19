import os

path = "/global/u1/v/vinny/projects/topreconstruction/top_reco/src/triplet_ml/select_triplets.py"

# 1. Reset to Origin
import subprocess
subprocess.run(f"cd /global/u1/v/vinny/projects/topreconstruction && git checkout top_reco/src/triplet_ml/select_triplets.py", shell=True)

with open(path, "r") as f:
    content = f.read()

# 2. Add Solver
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
if "_solve_exact_disjoint" not in content:
    content = content.replace("def _apply_strategy(", solver + "\ndef _apply_strategy(")

# 3. Add Dataclass Features
if "ratio_ab: float" not in content:
    content = content.replace("    triplet_mass: float", "    triplet_mass: float\n    mij_ab: float\n    mij_ac: float\n    mij_bc: float\n    dr_ab: float\n    dr_ac: float\n    dr_bc: float\n    ratio_ab: float\n    ratio_ac: float\n    ratio_bc: float")

# 4. Add Column Loading
if '"mij_ab"' not in content:
    content = content.replace('        "is_truth",', '        "is_truth",\n        "mij_ab", "mij_ac", "mij_bc", "dr_ab", "dr_ac", "dr_bc", "mij_over_m123_ab", "mij_over_m123_ac", "mij_over_m123_bc",')

# 5. Add Instantiation
if 'ratio_ab=float(payload["mij_over_m123_ab"][idx])' not in content:
    content = content.replace('triplet_mass=float(payload["m123"][idx]),', 'triplet_mass=float(payload["m123"][idx]),\n                    mij_ab=float(payload["mij_ab"][idx]),\n                    mij_ac=float(payload["mij_ac"][idx]),\n                    mij_bc=float(payload["mij_bc"][idx]),\n                    dr_ab=float(payload["dr_ab"][idx]),\n                    dr_ac=float(payload["dr_ac"][idx]),\n                    dr_bc=float(payload["dr_bc"][idx]),\n                    ratio_ab=float(payload["mij_over_m123_ab"][idx]),\n                    ratio_ac=float(payload["mij_over_m123_ac"][idx]),\n                    ratio_bc=float(payload["mij_over_m123_bc"][idx]),')

with open(path, "w") as f:
    f.write(content)
