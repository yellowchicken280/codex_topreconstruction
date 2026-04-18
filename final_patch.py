import os

path = "/global/u1/v/vinny/projects/topreconstruction/top_reco/src/triplet_ml/select_triplets.py"
with open(path, "r") as f:
    content = f.read()

# 1. Update Dataclass (Add Ratios)
if "ratio_ab: float" not in content:
    content = content.replace(
        "    dr_bc: float", 
        "    dr_bc: float\n    ratio_ab: float\n    ratio_ac: float\n    ratio_bc: float"
    )

# 2. Update Solver
solver_logic = """
def _solve_exact_disjoint(candidates: Sequence[TripletCandidate], max_top: int) -> List[TripletCandidate]:
    \"\"\"Find the mutually disjoint set of triplets that maximizes the sum of combined_scores.\"\"\"
    subset = candidates[:30]
    best_sum = -1.0
    best_set: List[TripletCandidate] = []
    
    def search(idx: int, current_selected: List[TripletCandidate], current_sum: float, used_jets: set[int]):
        nonlocal best_sum, best_set
        if current_sum > best_sum:
            best_sum = current_sum
            best_set = list(current_selected)
        if len(current_selected) >= max_top or idx >= len(subset):
            return
        for i in range(idx, len(subset)):
            cand = subset[i]
            jets = {cand.i, cand.j, cand.k}
            if not (jets & used_jets):
                search(i + 1, current_selected + [cand], current_sum + cand.score, used_jets | jets)

    search(0, [], 0.0, set())
    return best_set
"""
if "_solve_exact_disjoint" not in content:
    content = content.replace("def _apply_strategy(", solver_logic + "\ndef _apply_strategy(")

# 3. Update Column List (Add Ratio columns)
if '"mij_over_m123_ab"' not in content:
    content = content.replace(
        '        "dr_bc",',
        '        "dr_bc",\n        "mij_over_m123_ab",\n        "mij_over_m123_ac",\n        "mij_over_m123_bc",'
    )

# 4. Update Instantiation
if 'ratio_ab=float(payload["mij_over_m123_ab"][idx])' not in content:
    content = content.replace(
        'dr_bc=float(payload["dr_bc"][idx]),',
        'dr_bc=float(payload["dr_bc"][idx]),\n                    ratio_ab=float(payload["mij_over_m123_ab"][idx]),\n                    ratio_ac=float(payload["mij_over_m123_ac"][idx]),\n                    ratio_bc=float(payload["mij_over_m123_bc"][idx]),'
    )

with open(path, "w") as f:
    f.write(content)
