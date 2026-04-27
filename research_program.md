# Scientific Directive: Hadronic Top Reconstruction
**Framework:** Autonomous Agentic Search (v26.0)

## 1. Mission Overview
Surpass the state-of-the-art 0.6135 reconstruction efficiency on the verified 2,000-event benchmark. The core challenge is combinatorial background rejection.

## 2. Professor's Directives
*   **Redo BDT Scoring:** Replace the fixed XGBoost `score_xgb` with a **Deep Symbolic Neural Architecture**. You are encouraged to explore **Deep Sets** (to handle jet permutation symmetry), **Graph-inspired fusions**, and **Self-Attention** mechanisms. Use hierarchical non-linearities to capture synergies between the 14 kinematic features.
*   **Global Optimization:** Move beyond the "Greedy Disjoint" default. Design **Heuristic Selection Algorithms** (e.g., Beam Search, Branch-and-Prune, or Monte Carlo Tree Search) to maximize the total event-level score.

## 3. Constraints
*   **Physical Validity:** Every selection must be disjoint (no two chosen triplets can share the same jet index).
*   **Dimensional Integrity:** All features must be used with consistent units (GeV for masses).
*   **Efficiency Metric:** The primary goal is to maximize `METRIC_EFFICIENCY` reported by `research_train.py`.

## 4. Evaluation Loop
The orchestrator will:
1.  Read this program.
2.  Modify the code sections in `research_train.py`.
3.  Execute and record the efficiency in `research_log.md`.
4.  Hypothesize the next architectural shift.
