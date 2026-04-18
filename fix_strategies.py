import math
import os

path = "/global/u1/v/vinny/projects/topreconstruction/top_reco/src/triplet_ml/select_triplets.py"
with open(path, "r") as f:
    content = f.read()

# 1. Update STRATEGIES tuple (new format)
if "asymmetric_top_exact_v3" not in content:
    content = content.replace(
        'STRATEGIES = ("greedy_disjoint", "top1", "topk", "threshold", "best_pair_avg_disjoint")',
        'STRATEGIES = ("greedy_disjoint", "top1", "topk", "threshold", "best_pair_avg_disjoint", "asymmetric_top_exact_v3")'
    )

# 2. Add implementation blocks
v3_logic = """    if strategy == "asymmetric_top_exact_v3":
        if max_top_per_event <= 0 or len(candidates) == 0:
            return []
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

if 'if strategy == "asymmetric_top_exact_v3":' not in content:
    content = content.replace('    if strategy == "greedy_disjoint":', v3_logic + '\n    if strategy == "greedy_disjoint":')

with open(path, "w") as f:
    f.write(content)
print("Restored.")
