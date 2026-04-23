# 📊 Poster Presentation Guide: Autonomous Physics Discovery
**Project:** Optimizing Hadronic Top-Quark Reconstruction using Agentic LLM Discovery
**Researcher:** Vincent Yao
**Framework Version:** v18.9 (Production)

---

## 1. Introduction: The Agentic Search for Physics
High-energy physics data analysis is transitioning from manual "cut-and-count" methods to automated discovery. This project presents a **closed-loop autonomous agent** capable of proposing, implementing, and benchmarking physics selection strategies. We demonstrate that an LLM (gpt-oss-120b) can navigate the complex kinematic landscape of $t\bar{t}$ events to match expert-level reconstruction efficiency.

## 2. Motivation: Interpretability vs. Performance
*   **Black-Box ML:** Deep neural networks achieve high scores but offer little physical insight and are difficult to deploy in low-latency environments.
*   **Symbolic Discovery:** Our agent discovers **explicit mathematical formulas** that gate ML scores with physical priors (Mass, Ratios, $\eta$), ensuring both performance and transparency.
*   **Autonomous Iteration:** Surpassing the limit of human-led optimization by evaluating **32,000+ unique candidates**.

## 3. Theory: The 14-Dimensional Feature space
The agent reasons about the hadronic decay $t \to bW \to bjj$ using 14 features:
*   **Kinematic:** $m_{123}$ (Triplet Mass), $m_{W}$ candidates ($m_{ab}, m_{ac}, m_{bc}$).
*   **Invariant Ratios:** $m_{jj}/m_{123}$ (Targeting the $0.46$ $W/t$ ratio).
*   **Angular:** $\Delta R_{ab}, \Delta R_{ac}, \Delta R_{bc}$ (Collimation).
*   **Geometric:** $\eta, \phi$ (Detector position corrections).

## 4. Methodology: The Controlled Search
To ensure scientific truthfulness, we implemented a **Controlled Evaluation Protocol**:
1.  **Search Bench:** Every iteration is evaluated on the **exact same 5,000 events** to eliminate sample variance.
2.  **Stochastic Exploration:** Using **Exponential Probability Decay**, the agent shifts from **Refinement** (Exploitation) to **Radical Mutation** (Exploration) when it hits a performance plateau.
3.  **Cross-Validation:** Breakthroughs are verified on randomized subsets and full datasets to ensure generality.

## 5. Results: The Metric Frontier
The agent autonomously progressed through five distinct phases of understanding.

| Phase | Scientific Milestone | Efficiency | Key Discovery |
| :--- | :--- | :--- | :--- |
| **I** | **Baseline ML** | 0.4340 | Raw XGBoost output. |
| **II** | **Mass Gating** | 0.5870 | Discovered $m_W$ di-jet ratio window. |
| **III** | **Kinematic Priors** | 0.6280 | Implemented Asymmetric Gaussian Top-mass priors. |
| **IV** | **Full Synergy** | **0.6345** | Integrated $\eta$-corrections with $p_T$ scaling. |
| **V** | **Robust Mapping** | 0.6345 | Formalized Trajectory Framework & Action Classes. |

### The "Staircase" Frontier (Discovery Trajectory)
```mermaid
xychart-beta
    title "Efficiency Frontier over 32,000 Trials"
    x-axis [Phase I, Phase II, Phase III, Phase IV, Phase V]
    y-axis "Efficiency" 0 --> 0.7
    line [0.434, 0.587, 0.628, 0.6345, 0.6345]
```

## 6. Action Class Performance (The "Risk vs Reward" Analysis)
We tracked 32k actions to analyze agent "intelligence":
*   **Incremental Tuning:** High success rate, but small gains ($<1\%$).
*   **Within-Component Innovation:** High failure rate ($>80\%$), but responsible for **all major breakthroughs**.
*   **Cross-Component Shift:** Essential for breaking local plateaus (e.g., the move from Mass $\to$ Geometry).

## 7. Challenges & Technical Breakthroughs
*   **Shadowing & Caching:** Solved by forcing **absolute path injection** and purging `__pycache__` to ensure the physics engine executed new code.
*   **The 0.6160 Plateau:** Overcome by increasing sample size to **5,000 events**, reducing noise to **± 0.007** and revealing the "true" efficiency signal.
*   **Code Resilience:** Built a robust **Function Hook** with auto-indentation to handle complex, multi-branching LLM-generated logic.

## 8. Conclusion & Future Work
The framework successfully matched human expert benchmarks autonomously. 
**Next Steps:**
*   **Multi-Agent Debate:** Directing multiple models to peer-review physics hypotheses.
*   **Direct Differentiability:** End-to-end optimization of discovered symbolic logic.

---
*Created by Gemini CLI for Vincent Yao | Berkeley Lab | April 2026*
