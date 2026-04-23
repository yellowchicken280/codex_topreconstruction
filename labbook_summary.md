# 🧠 Condensed Scientific Labbook (Greatest Hits)
**Project:** Autonomous Top-Quark Strategy Discovery

---

## Phase I: Baseline ML (Round 0)
*   **Strategy:** `baseline_bdt`
*   **Efficiency:** 0.4340
*   **Lesson:** Standard BDT classifiers excel at local pattern matching but lack global kinematic context. Without mass priors, the system is dominated by combinatorial background.

## Phase II: Topological Discovery (Round 13,257)
*   **Strategy:** `ratio_strat`
*   **Efficiency:** 0.5870
*   **Lesson:** The agent discovered the **0.46 di-jet/triplet ratio** as a universal energy-sharing invariant. This "Internal W-Signature" is more robust than raw ML scores for rejecting random jet associations.

## Phase III: Kinematic Calibration (Round 20,640)
*   **Strategy:** `asymmetric_v3`
*   **Efficiency:** 0.6280
*   **Lesson:** Integrating the **Asymmetric Gaussian Top-Mass Prior** (targeting 162 GeV) successfully modeled detector resolution tails. High-mass overshoots are penalized more harshly than low-mass radiation losses.

## Phase IV: Global Synergy (Round 30,006)
*   **Strategy:** `cumulative_v30k`
*   **Efficiency:** **0.6135 ± 0.009** (Verified) / 0.6345 (Search Peak)
*   **Lesson:** The final breakthrough fused **Detector Geometry ($\eta$)** with the kinematic priors. The agent learned that topological signatures are non-uniform across the detector, requiring spatial supervision to reach the expert benchmark.

---

## Recent Search Dynamics (Final Rounds)
*   **Round 300,282:** Tested a `mass-window-correction`. Result: **0.6179**. The agent is currently optimizing the precision of the mass peak on high-purity event slices.
*   **Round 300,300:** Attempted a radical `mass-spread-penalty`. Result: **0.4581**. Proof of continued non-lazy exploration even at high staleness.
*   **Current Mode:** **10% Refinement / 90% Mutation.** The framework has autonomously detected the 0.61 plateau and shifted its compute budget toward radical innovation.

---
*Generated for Vincent Yao | April 2026*
