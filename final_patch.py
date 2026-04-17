import os

path = "/global/u1/v/vinny/projects/topreconstruction/top_reco/src/triplet_ml/select_triplets.py"
with open(path, "r") as f:
    content = f.read()

# 1. Solver logic
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

# 2. Asymmetric logic
v3_logic = """    if strategy == "asymmetric_top_exact_v3":
        if max_top_per_event <= 0 or len(candidates) == 0:
            return []
        import math
        scored_cands = []
        for t in candidates:
            best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
            if t.triplet_mass >= 162.0:
                top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / 18.0)**2)
            else:
                top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / 25.0)**2)
            w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
            pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
            s = max(t.score, 1e-6)
            combined_score = (s ** 1.0) * top_prior * w_prior * pt_scaling
            new_cand = TripletCandidate(i=t.i, j=t.j, k=t.k, score=combined_score,
                is_truth=t.is_truth,
                triplet_pt=t.triplet_pt, triplet_eta=t.triplet_eta, triplet_phi=t.triplet_phi,
                triplet_mass=t.triplet_mass, mij_ab=t.mij_ab, mij_ac=t.mij_ac, mij_bc=t.mij_bc)
            scored_cands.append(new_cand)
        scored_cands.sort(key=lambda t: (-t.score, t.i, t.j, t.k))
        return _solve_exact_disjoint(scored_cands, max_top=max_top_per_event)
"""

# Apply patches
if "_solve_exact_disjoint" not in content:
    content = content.replace("def _apply_strategy(", solver_logic + "\ndef _apply_strategy(")

if "asymmetric_top_exact_v3" not in content:
    content = content.replace('STRATEGIES = ("greedy_disjoint", "top1", "topk", "threshold", "best_pair_avg_disjoint")',
                            'STRATEGIES = ("greedy_disjoint", "top1", "topk", "threshold", "best_pair_avg_disjoint", "asymmetric_top_exact_v3")')

if 'strategy == "asymmetric_top_exact_v3"' not in content:
    content = content.replace('    if strategy == "greedy_disjoint":', v3_logic + '\n    if strategy == "greedy_disjoint":')

# Dataclass and loading
if "mij_ab: float" not in content:
    content = content.replace("    triplet_mass: float", "    triplet_mass: float\n    mij_ab: float\n    mij_ac: float\n    mij_bc: float")
if '"mij_ab"' not in content:
    content = content.replace('        "is_truth",', '        "is_truth",\n        "mij_ab",\n        "mij_ac",\n        "mij_bc",')
if 'mij_ab=float(payload["mij_ab"][idx])' not in content:
    content = content.replace('triplet_mass=float(payload["m123"][idx]),', 
                             'triplet_mass=float(payload["m123"][idx]),\n                    mij_ab=float(payload["mij_ab"][idx]),\n                    mij_ac=float(payload["mij_ac"][idx]),\n                    mij_bc=float(payload["mij_bc"][idx]),')

with open(path, "w") as f:
    f.write(content)
