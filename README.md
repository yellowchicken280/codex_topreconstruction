# ⚛️ Optimizing Hadronic Top Reconstruction via Agentic Strategy Discovery
**Status:** Phase VII Complete | **Verified Peak:** 0.6180 (+18.4% absolute gain)

## 🔬 Project Overview
This project implements an **Autonomous Discovery Loop** for hadronic top-quark reconstruction ($t \to bW \to bjj$). By bridging high-level symbolic reasoning with low-level numerical optimization, we enable an LLM-based agent (GPT-4o/Claude-3.5) to independently design, implement, and benchmark physics selection strategies on NERSC Perlmutter.

## 📈 Discovery Trajectory
The framework navigated four major scientific regimes across 32,000+ trials:

| Phase | Strategy | Verified Eff. | Key Scientific Breakthrough |
| :--- | :--- | :--- | :--- |
| **I: Baseline** | `baseline_bdt` | 0.4340 | Raw XGBoost shape classification. |
| **II: Topology** | `ratio_strat` | 0.5870 | Discovery of the 0.46 $W/t$ mass ratio invariant. |
| **III: Kinematics**| `asymmetric_v3` | 0.6040 | Asymmetric Gaussian mass priors for detector radiation. |
| **IV: Synergy** | `cumulative_v30k`| 0.6135 | Integration of $\eta$-geometry and mass-ratio gating. |
| **VII: Guided** | **v30.7 Breakthrough** | **0.6180** | **Global Beam Search + Spatial Attention Masking.** |

## 🧠 Framework Architecture: The Orchestration Layer
The system uses a multi-layered agentic approach:
1.  **Symbolic Scoping:** The agent designs Python modules that fuse raw kinematics with BDT-likelihoods.
2.  **Differentiable Harness:** Uses `scipy.optimize` inside the discovery loop to fine-tune neural weights.
3.  **Global Solver:** Implements iterative heuristics (Beam Search) to resolve jet-overlap conflicts at the event level.

## 🛠 Lessons in Scientific Integrity
A core finding of this project is that **Interpretability is a Performance Driver.** Our "White-Box" approach allowed us to:
*   Identify and patch an **88% false-breakthrough** caused by truth-label leakage.
*   Enforce **Truth-Blindness** and **Physicality Constraints** directly in the execution harness.
*   Diagnose the **"Metric-Selection Mismatch"**—proving that optimizing for signal separation is not enough; one must optimize for global selection yield.

---
*Autonomous discovery performed using the CBorg API and NERSC Perlmutter resources. Created by Vincent Yao | Berkeley Lab | May 2026*
