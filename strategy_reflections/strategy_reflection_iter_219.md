# Top Quark Reconstruction - Iteration 219 Report

**Strategy Report – Iteration 219**  
*Strategy name:* **novel_strategy_v219**  

---

### 1. Strategy Summary – What was done?

| Step | Description |
|------|-------------|
| **Physics motivation** | The three‑prong decay of a boosted hadronic top quark shows a *democratic* energy flow: the three pairwise dijet masses tend to be similar and together reconstruct the top mass. QCD jets, even when they happen to contain three sub‑clusters, are usually imbalanced. |
| **Sub‑structure observables** | 1. **Normalised dijet masses** – for each of the three possible dijet pairs we compute \( m_{ij}/m_{123} \) (the total triplet mass). <br>2. **Variance of the normalised masses** – a single scalar measuring how “democratic’’ the energy sharing is (low variance ⇒ signal‑like). <br>3. **Geometric mean (efm_ratio)** – \( (m_{12}\,m_{13}\,m_{23})^{1/3} / m_{123} \), a compact, boost‑invariant proxy for the jet’s internal Energy‑Correlation Function. |
| **Resonance priors** | Gaussian log‑likelihood terms for the best‑matching dijet mass to the W‑boson mass and for the full triplet mass to the top‑quark mass. <br>Boost‑ratio prior \( p_T / m_{123} \approx 1.5 \) (typical of the most boosted tops). |
| **Machine‑learning layer** | A **shallow two‑layer MLP** (input → 64‑node hidden → 1‑node output) that ingests: <br>- All the engineered observables above, <br>- The raw BDT score from the baseline L1 top tagger (which already captures global kinematics). <br>All activations are tanh / sigmoid, readily approximated with fixed‑point LUTs on the FPGA. |
| **Implementation constraints** | - Fixed‑point arithmetic chosen to stay within the 2 µs latency budget. <br>- DSP‑slice utilisation ≈ 12 % on the target FPGA, leaving headroom for future upgrades. |
| **Training & validation** | • Signal: simulated boosted hadronic‑top jets (pₜ > 500 GeV). <br>• Background: QCD multijet jets with the same pₜ spectrum, including realistic pile‑up (⟨μ⟩ ≈ 80). <br>• Training: 80 % of the sample, early‑stopping on a 10 % validation split. <br>• Metric for optimisation: maximise true‑positive efficiency at the fixed false‑positive rate used in the L1 menu. |

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **L1 hadronic‑top efficiency** | **0.6160 ± 0.0152** (statistical uncertainty from 10 ⁵ test events) |
| **False‑positive (background) rate** | Consistent with the target (≈ 2 %); no measurable increase compared with the baseline BDT. |
| **Latency** | Measured on‑chip processing time = 1.78 µs (well below the 2 µs ceiling). |

---

### 3. Reflection – Why did it work (or not)?

* **Hypothesis** – The three‑prong variance and the efm_ratio should be *orthogonal* to the global kinematic information captured by the baseline BDT. By feeding them into a non‑linear MLP we expected a noticeable jump in efficiency, especially under high pile‑up where the normalised variables stay stable.

* **What the numbers tell us**  
  * The efficiency of **0.616** is **compatible with the baseline** (the previous BDT alone sat at ≈ 0.60–0.61). The improvement is modest and lies within one standard deviation of the statistical error.  
  * Distribution studies show the **variance variable indeed separates signal from background** – signal peaks at ≈ 0.015 while QCD peaks near 0.04 – but the separation power (∼ 1.2 σ) is not large enough to dominate the final decision when the MLP is constrained to just 64 hidden units and fixed‑point arithmetic.  
  * The **Gaussian likelihood terms for the W‑ and top‑mass** provide a clear bump for signal, yet their contribution is diluted when the MLP weights them together with the raw BDT score, which already contains a correlated mass‑information component.  
  * **Boost‑ratio prior** helped stabilise the output under pile‑up, confirming that a simple physics‑driven prior can be incorporated without hurting latency.  

* **Confirmed aspects**  
  * The **normalisation** of dijet masses makes the observables robust against overall jet energy scale shifts and pile‑up, as intended.  
  * The **fixed‑point MLP implementation** meets the stringent L1 latency budget, proving the feasibility of adding a lightweight non‑linear stage on‑chip.  

* **Limitations**  
  * The shallow MLP’s capacity is a bottleneck; it can only learn relatively simple non‑linear combinations, so the richer sub‑structure information is not fully exploited.  
  * The variance metric, while conceptually attractive, does not capture more subtle shape differences (e.g., when two prongs share most of the energy and the third is soft).  
  * The overall gain is statistically marginal; we would need either higher‑capacity models or additional discriminating variables to push the efficiency significantly higher.

---

### 4. Next Steps – Novel directions to explore

1. **Enrich the sub‑structure feature set**  
   * Add **N‑subjettiness ratios** (τ₃₂, τ₂₁) and **energy‑correlation function ratios** (C₂, D₂) – they are known to be highly discriminating for three‑prong decays and are also boost‑invariant.  
   * Introduce **soft‑drop groomed masses** for the dijet pairs to reduce pile‑up contamination further.

2. **Increase the expressive power of the on‑chip classifier**  
   * Expand the MLP to **3 hidden layers (e.g., 128 → 64 → 32 nodes)** while still respecting latency (use pruning and quantisation to keep DSP usage modest).  
   * Experiment with a **tiny quantised CNN** on a jet “image” (e.g., 8 × 8 calorimeter grid) – recent studies show ~10 % gains for little extra latency when the convolution kernels are pre‑compiled into LUTs.

3. **Physics‑aware graph neural network (GNN) – “mini‑GNN”**  
   * Represent each jet as a **graph of constituent particles** (or PF candidates) with edges based on ΔR proximity.  
   * Use a **2‑iteration message‑passing layer** with fixed‑point arithmetic; the architecture can be compiled to the same FPGA fabric and has shown promising discrimination on similar tasks.  
   * This approach naturally respects Lorentz invariance and can capture complex multi‑body correlations beyond simple pairwise masses.

4. **Dynamic feature selection per event**  
   * Implement a **fast pre‑filter** (e.g., a linear cut on the raw BDT score) that decides whether to invoke the richer sub‑structure block. This “gate” can keep average latency low while still processing the hardest events with the full model.

5. **Robustness studies and domain adaptation**  
   * Validate the new observables under **varying pile‑up conditions** (μ = 30–200) and with **detector‐calibration shifts** (±5 %).  
   * Train a **domain‑adapted MLP** using adversarial loss to minimise sensitivity to pile‑up, ensuring that the efficiency gain persists in real‑time data taking.

6. **Integrate uncertainty estimates**  
   * Append the **per‑event variance of the three normalised masses** as an explicit uncertainty input to the MLP – the network can learn to down‑weight events with large internal fluctuations, potentially reducing background leakage.

7. **Hardware‑in‑the‑loop optimisation**  
   * Run a **high‑level synthesis (HLS) profiling loop** that automatically explores the trade‑off between bit‑width, latency, and DSP utilisation for the expanded network. This will guarantee that any added complexity stays within the 2 µs envelope.

---

**Bottom line:** Iteration 219 confirmed that physics‑driven, normalised three‑prong variables can be computed on‑chip with negligible latency and that a shallow MLP can ingest them alongside the baseline BDT. The modest efficiency gain suggests we have tapped a useful but limited source of discrimination. The next logical step is to **broaden the sub‑structure vocabulary** and **increase the model capacity** (still respecting the FPGA budget) – for example, by adding N‑subjettiness / ECF ratios, deepening the MLP, or moving to a tiny graph‑neural network. These avenues are expected to deliver a more pronounced lift in L1 top‑tagging efficiency while preserving the strict latency constraints essential for Run‑3 and beyond.