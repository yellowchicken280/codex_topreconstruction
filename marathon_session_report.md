# Top Reconstruction Marathon — Deep Session Report
**Updated:** 2026-04-20 12:21:32
**Current Best Efficiency:** 0.6345
**Champion Strategy Slug:** cumulative_v30006

## Champion Physics Motivation
No motivation provided.

## Champion Selection Logic
```python
    best_w = min([t.mij_ab, t.mij_ac, t.mij_bc], key=lambda m: abs(m - 80.4))
    top_prior = math.exp(-0.5 * ((t.triplet_mass - 162.0) / (18.0 if t.triplet_mass >= 162.0 else 25.0))**2)
    w_prior = math.exp(-0.5 * ((best_w - 80.4) / 18.0)**2)
    pt_scaling = (max(t.triplet_pt, 1.0) / 200.0) ** 0.2
    base_score = max(t.score, 1e-6) * top_prior * w_prior * pt_scaling
    
    # The Winning Correction (v30006)
    ratio_factor = (math.exp(-((t.ratio_ab - 0.46)**2)/0.02) + math.exp(-((t.ratio_ac - 0.46)**2)/0.02) + math.exp(-((t.ratio_bc - 0.46)**2)/0.02))/3.0
    eta_factor = 1.0 + 0.05 * math.tanh(1.5 - abs(t.triplet_eta))
    combined_score = base_score * ratio_factor * eta_factor
```

## Session Progress Notes
The harness is currently iterating on refined strategies and wild mutations. 
Strategies focus on breaking the 0.6345 plateau using asymmetric Gaussian priors, kinematic correlations, and jet-geometry vetos.

---
*Report generated automatically by Marathon Harness v14.3*
