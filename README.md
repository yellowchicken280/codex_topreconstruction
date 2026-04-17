# Top Quark Reconstruction - Agentic Strategy Optimization

This repository contains an autonomous discovery harness for optimizing hadronic top-quark reconstruction. It utilizes high-context reasoning models (lbl/gpt-oss-120b-high) to devise, implement, and evaluate physics-informed selection strategies.

## 🚀 Current Status: MARATHON ACTIVE
- **Current Best Efficiency:** **0.6412** (Breaking the 0.63 plateau)
- **Total Iterations:** 645+
- **Architecture:** Harness v8.0 (Discovery Compaction Mode)

## 🛠 Methodology: Discovery Compaction
To avoid redundant strategies, the system utilizes a "Compactor" logic:
1. **Discovery:** The agent proposes novel physics logic based on jet topology, energy fractions, and kinematic correlations.
2. **Evaluation:** Strategies are injected directly into `select_triplets.py` and benchmarked against 2,000 truth-matched events.
3. **Synthesis:** Every 5 iterations, a master `discovery_trajectory.md` is updated to categorize "Dead Ends" and redefine the "Physics Frontier."
4. **Context Injection:** Future iterations read the trajectory to ensure genuinely new exploratory directions.

## 📈 Breakthroughs
| Iteration | Strategy | Efficiency | Key Insight |
| :--- | :--- | :--- | :--- |
| 0 | baseline_bdt | 0.4437 | Raw XGBoost Score |
| 3 | asymmetric_v3 | 0.6160 | Asymmetric mass windows + pT scaling |
| 11 | topology_v3 | 0.6384 | Energy fraction variance weighting |
| 638 | jet_veto_v1 | **0.6412** | Multi-stage kinematic vetoes |

## 📂 Project Structure
- `select_triplets.py`: The core physics engine (dynamically patched by the agent).
- `labbook.md`: Detailed log of every attempt and efficiency result.
- `discovery_trajectory.md`: Living summary of the scientific search space.
- `marathon_harness.py`: The background discovery loop.

---
*Optimizing for the L1 Trigger Latency Budget (<80ns).*
