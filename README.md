# Top Quark Reconstruction - Agentic Strategy Optimization

This repository contains an autonomous discovery harness for optimizing hadronic top-quark reconstruction. It utilizes high-context reasoning models (lbl/gpt-oss-120b-high) to devise, implement, and evaluate physics-informed selection strategies.

## 🚀 Current Status: MARATHON ACTIVE (The Honest Era)
- **Current Best Efficiency:** **0.6267** (Verified Baseline)
- **Status:** Resumed discovery from Iteration 2000+
- **Architecture:** Harness v8.7 (Truth Mode)

## 🛠 Methodology: Discovery & Verification
The system utilizes an automated discovery loop:
1. **Discovery:** The agent proposes novel physics logic (Type B strategies) using jet energy flow and kinematic correlations.
2. **Evaluation:** Strategies are benchmarked using `real_eval.py` which enforces a strict event-aligned truth denominator.
3. **Engine:** Built on a restored version of the `select_triplets.py` engine with full sub-mass feature support and exact disjoint solving.

## 📈 Breakthroughs (Verified)
| Iteration | Strategy | Efficiency | Key Insight |
| :--- | :--- | :--- | :--- |
| 0 | baseline_bdt | 0.4437 | Raw XGBoost Score |
| 13 | asymmetric_v1 | 0.5975 | Grid search mass priors |
| 3 | asymmetric_v3 | **0.6267** | Asymmetric priors + pT scaling |

## 📂 Project Structure
- `select_triplets.py`: The core physics engine (dynamically patched by the agent).
- `labbook.md`: Detailed log of every attempt and efficiency result.
- `real_eval.py`: The "Ground Truth" evaluator (strict denominator).
- `marathon_harness_v8.py`: The background discovery loop.

---
*Optimizing for the L1 Trigger Latency Budget (<80ns).*
