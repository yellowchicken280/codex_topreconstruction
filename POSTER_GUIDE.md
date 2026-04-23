# 📊 Poster Presentation Guide: Autonomous Physics Discovery
**Project:** Optimizing Hadronic Top-Quark Reconstruction using Agentic LLM Discovery
**Researcher:** Vincent Yao
**Framework Version:** v18.9 (Production)

---

## 1. Introduction: The Agentic Search for Physics
High-energy physics data analysis is transitioning from manual, labor-intensive "cut-and-count" methods to automated, data-driven discovery loops. This project presents a **closed-loop autonomous agent** that iteratively proposes, implements, and benchmarks physics selection strategies. We demonstrate that an LLM (gpt-oss-120b) can navigate the high-dimensional kinematic landscape of $t\bar{t}$ events to match world-class expert benchmarks.

### 1.1 Context: The Plateau Problem
Prior manual optimization efforts (e.g., *top_reco_optimization_writeup.pdf*) successfully established the fundamental mass-prior benchmarks. However, as the number of correlated observables increased (Angular Separation, Sub-jet Substructure), human-led search reached a diminishing-returns plateau. This project aims to break that plateau using an agent capable of exploring **32,000+ unique mathematical hypotheses** at a velocity impossible for human researchers.

## 2. Motivation: Interpretability vs. Performance
*   **The Black-Box Dilemma:** Deep neural networks (MLPs, GNNs) achieve high performance but lack physical transparency.
*   **The Symbolic Bridge:** Our framework discovers **explicit, symbolic physics logic** that gates or refines raw ML scores. This results in a "Physics-Informed ML" model that is both high-performance and human-auditable.
*   **Discovery Efficiency:** Surpassing the limit of expert-led search by automating the **Diagnosis-Hypothesis-Benchmark** cycle.

## 3. Previous Studies & Benchmarks
This work builds on a rich history of top-quark reconstruction research:

### 3.1 The Human-Led Baseline (Phase I & II)
Early studies utilized rigid mass windows ($m_{jjj} \in [140, 200]$ GeV). Manual refinement introduced Gaussian priors, reaching an efficiency of ~0.628. This established the "Kinematic Regime" of the problem.

### 3.2 The Substructure Breakthrough (Reference: heppaperllm.pdf)
Historical benchmarks (reached **0.6384**) utilized particle-level substructure variables ($D_2$, dipolarity) combined with side-band trained background density estimators. 

### 3.3 The "Dead-End" Era
Recent attempts to use **Conditional Normalizing Flows** and **Lorentz-Equivariant GNNs** plateaued at **0.6160 ± 0.015**. These studies found that adding complex modules often failed to provide new independent information beyond the simple mass-Gaussian core, often collapsing back to the same performance level.

## 4. Theory: The 14-Dimensional Feature space
The agent reasons about the $t \to bW \to bjj$ decay using 14 features:
*   **Kinematic Invariants:** $m_{123}$ (Triplet Mass), $m_{ab}, m_{ac}, m_{bc}$ (W candidates).
*   **Dimensionless Ratios ($m_{jj}/m_{123}$):** The key $0.46$ signature of energy-sharing in top decay.
*   **Angular Topology:** $\Delta R$ separations reflecting the collimation of boosted top products.
*   **Geometric Corrections:** $\eta, \phi$ coordinates to handle detector-region energy resolution variations.

## 5. Methodology: The Controlled Discovery Loop
We utilize a hybrid compute architecture: **Berkeley Lab CBorg API** for strategy reasoning and **NERSC Perlmutter** for high-throughput evaluation.

### 5.1 The Stochastic Control Engine
To prevent the agent from getting stuck on local optima, we implement **Exponential Probability Decay**:
$$P_{refine} = 0.10 + 0.70 \cdot e^{-\frac{N_{stale}}{500}}$$
*   **Stale Counter:** Tracks iterations since the last Global Best.
*   **The Pivot:** As progress stalls, the system shifts from **Incremental Tuning** (Safe) toward **Radical Mutation** (High-Risk).

## 6. Key Results: The Efficiency Frontier
The agent autonomously matched the **expert benchmark** of **0.6345 ± 0.007**.

| Frontier Step | Discovery Phase | Efficiency | Key Scientific Insight |
| :--- | :--- | :--- | :--- |
| **I** | **Baseline ML** | 0.4340 | Established raw XGBoost substructure ranking. |
| **II** | **Mass Ratios** | 0.5870 | Discovered the $0.46$ energy-sharing invariant. |
| **III** | **Kinematic Priors** | 0.6280 | Optimized Asymmetric Gaussian mass shapes. |
| **IV** | **Global Synergy** | **0.6345** | Integrated detector geometry with resonance gating. |

## 7. Challenges & Technical Breakthroughs
*   **Shadowing & Cache Purgation:** Overcome by forcing absolute pathing and purging `__pycache__` to ensure the physics engine executed *new* code every trial.
*   **The 0.6098 Barrier:** Solved by increasing sample size to **5,000 events** and adding **Randomized Offsets**, providing a truthful signal above the statistical noise.
*   **Code Stability:** Developed a **Robust Function Hook** with auto-indentation to survive the high variance of LLM-generated code.

## 8. Future Work
*   **Multi-Agent Debate:** Directing adversarial LLMs to challenge physics hypotheses.
*   **Differentiable Logic:** Enabling the agent to optimize its own internal parameters via gradient descent.

---
*Created by Gemini CLI for Vincent Yao | April 2026*
