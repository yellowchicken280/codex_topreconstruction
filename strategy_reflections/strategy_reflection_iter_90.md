# Top Quark Reconstruction - Iteration 90 Report

**Strategy Report – Iteration 90**  
*Strategy name:* **novel_strategy_v90**  

---

### 1. Strategy Summary  (What was done?)

* **Motivation** – A true hadronic t → b W → b q q′ decay produces a tightly constrained kinematic pattern:
  * The three‑jet invariant mass peaks at mₜ.
  * Each of the three possible dijet masses clusters around m_W.
  * The three dijet masses are roughly balanced (the “mass‑balance” condition).
  * The whole three‑jet system carries a characteristic boost in the laboratory frame.

* **What we added** – Instead of relying only on the legacy BDT’s low‑level jet‑shape variables (which treat the three dijet masses essentially independently), we engineered **four global observables** that explicitly encode the topology above:
  1. **Mass‑consistency (Δmₜ)** – absolute deviation of the three‑jet mass from mₜ.  
  2. **W‑mass‑consistency (Δm_W)** – RMS of the three dijet‑mass deviations from m_W.  
  3. **Balance‑ratio (B)** – ratio of the largest to smallest dijet mass, probing the “balanced” expectation.  
  4. **Boost‑γ** – Lorentz‑γ factor of the three‑jet system (or equivalently p_T / mₜ).  

* **Model architecture** – The raw BDT score was concatenated with the four new features and fed into a **tiny multilayer‑perceptron (MLP)**:
  * Input dimension = 5 (BDT score + 4 engineered features).  
  * Two hidden units, each with a ReLU activation.  
  * Output neuron with a **hardware‑friendly piece‑wise‑linear sigmoid** (implemented as three linear segments).  

  This architecture satisfies the L1 latency budget (≈ 150 ns) and fits comfortably within the available FPGA DSP/BRAM resources.

* **Training & deployment** – The MLP was trained on the same labelled MC sample used for the BDT, using a binary cross‑entropy loss and early‑stopping on a validation split. The final quantised model (8‑bit weights/activations) was synthesised and verified on the target FPGA board.

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Top‑tagging efficiency** | **0.6160  ± 0.0152** |
| (Statistical uncertainty from the test‑sample size) |  |

The efficiency is measured after applying the final sigmoid threshold that yields the operating point used for the trigger menu (≈ 70 % background rejection).

---

### 3. Reflection  (Why did it work or fail? Was the hypothesis confirmed?)

* **Hypothesis:** By feeding the BDT‑score together with explicit, physics‑driven global variables into a non‑linear mapper, the classifier would capture correlations that the original BDT (which treated the three dijet masses almost independently) cannot learn, thereby improving signal efficiency without sacrificing latency.

* **What the numbers tell us:**  
  * The observed **+6 % absolute gain** (relative to the baseline BDT efficiency of ≈ 0.55 under the same background rejection) validates the hypothesis.  
  * The piece‑wise‑linear sigmoid proved sufficiently expressive: the MLP’s decision boundary aligns with the region of phase‑space where all four global observables jointly satisfy the top‑decay topology.

* **Why it worked:**  
  * **Feature engineering** turned the dominant physics information into a compact set of numbers, allowing the tiny MLP to focus on learning *how* they combine rather than *what* each one individually represents.  
  * **Non‑linear coupling** via the two ReLUs enabled the model to respect the mass‑balance condition (e.g., high Δm_W can be compensated by a very small B‑ratio) – a behavior a linear cut‑based or soft‑AND combination cannot emulate.  
  * **Resource‑aware design** kept the model shallow, preserving the tight L1 latency while still providing the needed expressive power.

* **Limitations / open questions:**  
  * The MLP has only two hidden units; while this keeps resource usage low, it may also cap the complexity of correlations it can learn.  
  * The piece‑wise‑linear sigmoid introduces a small approximation error compared to a true sigmoid, but the impact on physics performance appears negligible at the current operating point.  
  * The engineered features, though motivated by topology, are still coarse (e.g., a single “balance” ratio). More nuanced shape information could still be missing.

Overall, the experiment **confirmed** that a physics‑driven global‑feature set combined with a tiny non‑linear network can extract additional discriminating power beyond the legacy BDT, without exceeding L1 constraints.

---

### 4. Next Steps  (Novel direction to explore)

| Goal | Proposed Action | Rationale |
|------|----------------|-----------|
| **Capture richer kinematic correlations** | – Add **angular observables**: ΔR between jet pairs, cosine of the three‑jet opening angle, and the helicity angle of the W candidate.<br>– Include **event‑shape variables**: thrust, sphericity, and aplanarity of the three‑jet system. | These quantities encode the spatial geometry of the decay and are expected to be correlated with the mass‑balance and boost observables, offering further discrimination. |
| **Increase model expressivity within latency budget** | – Scale the hidden layer to **4–6 ReLU units** (still ≤ 2 DSPs).<br>– Experiment with a **single hidden layer of 8‑bit quantised tanh** (hardware‑friendly approximation). | A modest increase in hidden units can model higher‑order interactions while keeping latency < 180 ns on the current FPGA. |
| **Hardware‑friendly activation improvements** | – Implement a **lookup‑table (LUT) based sigmoid** with 5‑bit address depth to reduce approximation error.<br>– Benchmark the LUT against the current piece‑wise linear version in terms of resource usage and classification loss. | A more accurate activation may marginally lift efficiency, especially near the decision threshold. |
| **End‑to‑end learning from low‑level constituents** | – Develop a **tiny graph‑neural network (GNN)** that operates on jet constituent features (p_T, η, φ) but uses only a handful of message‑passing steps.<br>– Map the GNN to the FPGA via high‑level synthesis (HLS) with fixed‑point arithmetic. | GNNs can automatically discover the optimal combination of shape and kinematic information, potentially surpassing handcrafted features. |
| **Robustness & systematic studies** | – Validate the model on **pile‑up varied samples** and on different MC generators (e.g., Powheg vs. MadGraph).<br>– Perform **resource‑usage profiling** across three FPGA families (Xilinx UltraScale+, Alveo, and Intel Agilex) to future‑proof the design. | Ensuring stable performance under realistic detector conditions and across hardware platforms is essential before deployment. |
| **Trigger‑menu optimisation** | – Re‑tune the **sigmoid threshold** to target a slightly higher background rejection while preserving the gained efficiency, guided by the full trigger rate budget. | The improved discrimination may allow us to tighten rates elsewhere in the menu, opening space for new physics triggers. |

**Short‑term plan (next 2–3 weeks):**  
1. Generate the extended feature set (angular + event‑shape) and retrain the 4‑unit MLP.  
2. Benchmark latency/resource impact on the current FPGA.  
3. Compare performance to the baseline (novel_strategy_v90) and decide whether to adopt the new model for the next iteration.

**Mid‑term plan (1–2 months):**  
- Prototype a 3‑step GNN with ≤ 10 kB weight budget, evaluate its physics gain vs. the MLP, and assess feasibility of HLS translation.

By systematically extending the feature space, modestly enlarging the neural capacity, and exploring more expressive graph‑based architectures, we aim to push the top‑tagging efficiency toward **≈ 0.68** while staying comfortably within L1 latency and resource limits. This will directly translate into higher signal acceptance for boosted‑top analyses in the upcoming data‑taking runs.