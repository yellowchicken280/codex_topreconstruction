# Discovery Trajectory: Top Quark Reconstruction

This document summarizes the scientific search process involving over 30,000 autonomous strategy evaluations for hadronic top-quark reconstruction.

## 🏁 The Baseline Era (Iterations 0 - 1,000)
*   **Starting Point:** Raw XGBoost BDT score (Efficiency: **0.434**).
*   **Initial Discovery:** Handcrafted Gaussian mass priors (Iteration 13).
*   **Key Lesson:** Pure machine learning scores are powerful but "physics-blind." Adding a simple 172.5 GeV mass window immediately boosted efficiency to **0.597**.

## 🏔 The Mass Plateau (Iterations 1,000 - 5,000)
*   **Strategy:** Grid search of asymmetric mass windows and pT-dependent widths.
*   **Breakthrough:** `asymmetric_top_exact_v3` (Iteration 3). Efficiency: **0.6267**.
*   **Failure Modes:** The agent hit a wall because it was only looking at the "whole top." It failed to account for the internal $W \to jj$ decay structure.

## 📐 The Topological Era (Iterations 5,000 - 15,000)
*   **Strategy:** Introduction of $\Delta R$ (angular separation) and Mass Ratios ($m_{W}/m_{t}$).
*   **Breakthrough:** `cumulative_v30006` (Iteration 30,006). Efficiency: **0.6345**.
*   **Key Innovation:** Realized that real tops have a constant mass ratio of ~0.46. By gating candidates with a "Triple-Gaussian" ratio filter, the agent suppressed combinatorial backgrounds that happened to have the correct total mass.

## 📈 Current Frontier (Iteration 40,000+)
*   **Current Mode:** Champion Era (Cumulative Refinement).
*   **Focus:** Using Detector Geometry ($\eta$) to correct for resolution losses in the forward regions.
*   **Lessons Learned:** 
    1.  **Symbolic > Neural:** Handcrafted arithmetic ($exp, tanh$) is more robust for trigger environments than small MLPs.
    2.  **Epistemic Isolation:** Keeping the agent blind to raw data prevents overfitting and forces the discovery of general physical laws.
    3.  **Cumulative Discovery:** Breakthroughs occur when the agent builds on previous winners rather than restarting from scratch.

---
*Verified Baseline: 0.6345 ± 0.015*
