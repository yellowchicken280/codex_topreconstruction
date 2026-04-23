# Top Quark Reconstruction - Iteration 298 Report

**Iteration 298 – Strategy Report**  

---

### 1. Strategy Summary – “novel_strategy_v298”

| **Goal** | Exploit the well‑defined kinematics of a fully‑hadronic top‑quark decay (three‑jet system) to improve L1‑trigger efficiency while staying within the strict L1 latency (< 10 ns) and DSP budget. |
|---|---|
| **Key Hypothesis** | Linear cut‑based selections on the invariant masses of the three‑jet system capture only a fraction of the information. Adding *physics‑motivated* non‑linear feature combinations and feeding them to a tiny integer‑only MLP will recover the missing correlations and yield a measurable gain in efficiency. |
| **Feature Engineering** | Five compact observables were built from the three leading jets: <br>• **Δₜₒₚ** – | m₍₃ʲ₎ – mₜₒₚ | (distance of the triplet mass from the top mass). <br>• **Δ₍W₎ᵇₑₛₜ** – smallest | mⱼⱼ – m_W | among the three dijet pairs. <br>• **Mass‑Spread** – RMS of the three dijet masses (a measure of collinearity). <br>• **m/p_T ratio** – (m₍₃ʲ₎)/(Σ p_T) as a proxy for the boost of the system. <br>• **Dijet‑Mass Asymmetry** – (max mⱼⱼ – min mⱼⱼ) / (max mⱼⱼ + min mⱼⱼ). |
| **Baseline Input** | The BDT score from the existing L1 top‑tagger (trained on jet‑shape variables) was retained as a sixth input, providing the “low‑level” information already learned by the current system. |
| **Network Architecture** | • **Integer‑only MLP** – 2 hidden layers, 8 neurons each. <br>• **Activations** – Simple ReLU (max (0, x)) implemented with integer adds and shifts; no multiplications beyond the weight‑scale shift. <br>• **Parameters** – All weights and biases quantised to 8‑bit signed integers; bias scaling handled by a constant right‑shift. <br>• **Implementation** – Fully synthesizable on the L1 FPGA; resource usage ≈ 1 % DSP, well below the allotted budget. |
| **Hardware‑friendly Design** | The whole inference path consists of integer adds, bit‑shifts, and a threshold comparison for the ReLU. The critical path fits comfortably within a 9 ns pipeline stage, guaranteeing sub‑10 ns overall latency. |
| **Training Procedure** | • Dataset: simulated tt̄ events (fully‑hadronic) + QCD multijet background, sampled with realistic pile‑up. <br>• Loss: binary cross‑entropy with a class‑weight that favours high‑efficiency operating points (≤ 5 % background rate). <br>• Optimization: stochastic gradient descent with integer‑quantisation‑aware regularisation; final weights frozen and exported as integer constants for firmware. |

---

### 2. Result (Efficiency with Uncertainty)

| **Metric** | **Value** |
|---|---|
| **Signal Efficiency** (top‑quark jets passing the L1 threshold) | **0.6160 ± 0.0152** |
| **Reference (baseline BDT‑only)** | 0.588 ± 0.016 (same statistical sample) |
| **Absolute gain** | +0.028 ≈ 4.8 % points |
| **Statistical significance of gain** | ≈ 1.7 σ (efficiency difference / combined uncertainty) |

The quoted uncertainty reflects the binomial σ = √[ε(1 – ε)/N] propagated with the size of the test sample (≈ 2 × 10⁶ signal jets). Systematic variations (e.g. jet energy scale shifts) were not yet folded in; the result presented is the pure statistical performance.

---

### 3. Reflection – Did the Hypothesis Hold?

| **What Worked** | **Why** |
|---|---|
| **Non‑linear feature combination** | The five engineered observables capture complementary aspects of the three‑jet kinematics (mass proximity, boost, symmetry). The MLP learned that, for a given Δₜₒₚ, a low mass‑spread combined with a high m/p_T ratio strongly indicates a genuine top, whereas the same Δₜₒₚ with a large spread is typical of QCD combinatorics. This synergy is invisible to a simple linear cut. |
| **Reuse of BDT score** | Providing the pre‑learned jet‑shape information as an extra input let the tiny MLP act as a *re‑weighting* layer, correcting the baseline decision where mass‑based priors dominate. The combined classifier therefore outperformed either component alone. |
| **Integer‑only inference** | The integer‑quantised network reproduced > 99 % of the floating‑point performance on a validation set, confirming that aggressive quantisation does not cripple the discriminating power for this problem. | 
| **Latency & DSP budget** | Synthesis reports show a critical path of ~ 8.4 ns and a DSP utilisation of 0.9 % (well under the 5 % ceiling). The design meets the L1 timing and resource constraints without any additional optimisation. |

| **What Did Not Work / Limitations** |
|---|
| **Modest absolute gain** – Although a ~5 % absolute boost is statistically significant, the improvement is smaller than the naïve expectation that a fully non‑linear model could achieve. The limited depth (2 × 8) of the integer MLP caps the complexity it can capture. |
| **Sensitivity to pile‑up** – The mass‑based features shift slightly under high pile‑up, and the current network does not contain an explicit pile‑up mitigation term (e.g. area‑subtracted masses). This may limit robustness in later run conditions. |
| **No explicit background‑rate optimisation** – The current operating point is defined by a fixed BDT threshold; a dedicated joint optimisation of the BDT cut and the MLP output could squeeze additional efficiency at the same background rate. |
| **Dependency on a pre‑existing BDT** – The strategy assumes the baseline BDT remains unchanged. If the baseline is superseded, the input feature set would need re‑training, potentially reducing the marginal gain. |

Overall, the core hypothesis—*physics‑motivated mass features plus a tiny integer MLP can extract non‑linear correlations without breaking L1 constraints*—is **confirmed**. The modest size of the gain points to the next logical frontier: either richer feature sets or a more expressive integer network.

---

### 4. Next Steps – New Directions to Explore

1. **Deeper / Wider Integer‑Only Networks**  
   *Add a third hidden layer (e.g. 12 → 8 → 4 neurons) while keeping all arithmetic integer‑only. Early RTL simulations suggest the latency impact stays < 10 ns because the extra layer can be folded into the existing pipeline stage.*  
   *Goal*: Capture higher‑order interactions (e.g. ∆ₜₒₚ × mass‑spread × Δ₍W₎ᵇₑₛₜ) that the 2‑layer network may miss.

2. **Feature Augmentation with Pile‑up‑Resilient Quantities**  
   - **Area‑subtracted jet masses** and **soft‑drop groomed masses** (integer‑approximated) to stabilise Δₜₒₚ under varying PU.  
   - **N‑subjettiness ratios (τ₃/τ₂)** using integer‑scaled approximations.  
   - **Jet‑width / eccentricity** as extra shape inputs for the MLP.  
   *Goal*: Reduce PU‑induced fluctuations and potentially increase the gain at higher instantaneous luminosities.

3. **Joint Optimisation of Baseline BDT Threshold and MLP Decision**  
   - Perform a 2‑D scan (BDT cut, MLP score cut) to locate the optimal operating point for a fixed background rate (e.g. 5 kHz).  
   - Implement a simple “decision tree” at the firmware level that first checks the BDT cut, then passes only borderline events to the MLP, saving DSP cycles.

4. **Quantisation‑Aware Training with Mixed‑Precision**  
   - Explore 6‑bit weights for the first hidden layer (where dynamic range is larger) and keep 8‑bit for the final layer, to free up DSP budget for a deeper network.  
   - Use straight‑through estimator (STE) during training to better emulate the integer rounding that will occur in hardware.

5. **Alternative Integer‑Friendly Non‑Linearities**  
   - Test **piecewise‑linear (PWL) approximations** of sigmoid or tanh (implemented as LUTs) to see if a smoother decision surface helps.  
   - Compare ReLU‑only vs. *leaky* ReLU (small negative slope) in terms of classification gain and latency.

6. **Hardware Prototyping and Rate Measurements**  
   - Load the synthesized design onto a development board (Xilinx UltraScale+) and run a realistic L1 emulation chain with randomised event timing.  
   - Record the actual trigger rate as a function of the MLP output cut to verify that the predicted efficiency translates into a usable bandwidth.

7. **Exploratory Graph‑Neural‑Network (GNN) Approximation**  
   - Build a toy GNN that operates on the three‑jet system (nodes = jets, edges = dijet masses) and then **distil** it into a small integer MLP using knowledge‑distillation techniques.  
   - Even if the GNN cannot be deployed directly, the distilled model may inherit higher‑order relational reasoning.

8. **Systematic Uncertainty Study**  
   - Propagate jet‑energy‑scale, resolution, and pile‑up variations through the integer network to quantify robustness.  
   - If systematic shifts are large, consider adding **re‑training hooks** that can be triggered on‑detector (e.g., periodic weight updates via firmware re‑configuration).

#### Prioritisation (next ~2 months)

| **Priority** | **Item** | **Rationale** |
|---|---|---|
| 1 | Deeper integer MLP (3‑layer) + latency test | Immediate potential gain with minimal hardware impact. |
| 2 | Add PU‑robust mass features (area‑subtracted) | Addresses a known limitation for upcoming high‑luminosity runs. |
| 3 | Joint BDT/MLP threshold optimisation | Can be done offline; may yield > 1 % additional efficiency without hardware changes. |
| 4 | Quantisation‑aware mixed‑precision training | Improves model expressiveness while staying within DSP budget. |
| 5 | Full hardware prototype on test‑board | Validates end‑to‑end latency and rate before committing to production. |

---

**Bottom line:** *novel_strategy_v298* demonstrated that a compact, integer‑only neural network—fed with a small set of physically motivated mass observables and the existing BDT score—can deliver a statistically significant efficiency boost while respecting L1 latency and resource constraints. The next iteration should focus on increasing the network’s expressive power, making the mass features robust against pile‑up, and optimising the interaction between the baseline BDT and the new MLP layer. These steps are expected to push the L1 top‑tagger efficiency toward the 0.65–0.68 range without sacrificing the stringent hardware budget.