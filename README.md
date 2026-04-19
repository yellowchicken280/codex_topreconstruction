# Optimizing Hadronic Top-Quark Reconstruction using Physics-Informed Agentic Strategy Discovery

## Abstract
Recent work by Gendreau-Distler et al. demonstrated that LLM-based agents can automate components of high-energy physics data analysis within structured reproducible pipelines. We extend this approach to an autonomous strategy discovery framework in which a high-context model (gpt-oss-120b) accessed via the Berkeley Lab CBorg API iteratively proposes, implements, and evaluates triplet selection strategies built on a pre-trained XGBoost classifier operating on ttbar simulation. Across more than 10,000 autonomous strategy evaluations, the agent autonomously progressed from a raw-score greedy baseline of 0.434 reconstruction efficiency to a verified best of 0.628 ± 0.015, achieved by combining score-compressed Gaussian top-mass and W-mass kinematic priors with an exact global disjoint subset optimizer, a result that matched the efficiency of expert-designed strategies from prior human-led optimization. At each iteration the agent diagnosed failure modes by inspecting events where true triplets were obscured by high-scoring false positives, formed an explicit physics hypothesis before implementing any change, and reflected on whether the outcome confirmed or contradicted that hypothesis. Agent actions were classified into three functional categories: incremental parameter tuning, within-component strategy innovation, and cross-component attention shifts, with the largest efficiency gains arising exclusively from within-component innovations in the selection stage. While individual strategy outcomes are reproducible given a fixed evaluation set, the agent's discovery trajectory is fundamentally stochastic and history-dependent. Consequently, this framework functions less as a deterministic algorithm and more as an open-ended scientific search process.

## 🚀 Marathon Status: ACTIVE (The Honest Era)
- **Current Best Efficiency:** **0.628 ± 0.015** (Verified Baseline)
- **Total Iterations:** 12,500+ 
- **Methodology:** 72-hour autonomous discovery marathon using the LBL CBorg API.
- **Hardware Target:** FPGA L1 Trigger (<80ns latency budget).

## 📈 Key Breakthroughs (Verified)
| Iteration | Era | Strategy | Efficiency | Innovation |
| :--- | :--- | :--- | :--- | :--- |
| 0 | Baseline | `baseline_bdt` | 0.434 | Raw XGBoost Score |
| 3 | Mass | `asymmetric_v3` | **0.628** | Asymmetric mass priors + pT scaling |
| 7306 | Ratio | `ratio_strat` | 0.587 | Mass fraction $m_{W}/m_{t}$ signature |

## 🛠 Project Structure
- `top_reco/src/triplet_ml/select_triplets.py`: The core physics engine (dynamically patched).
- `labbook.md`: Detailed log of 12,500+ attempts and physics motivations.
- `real_eval.py`: The "Era of Truth" evaluator (strict event-aligned denominator).
- `marathon_harness_v8.py`: The background discovery loop (Harness v9.5).

---
*Autonomous discovery performed on the LBL CBorg API cluster.*
