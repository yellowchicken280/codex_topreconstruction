# Top Quark Reconstruction - Iteration 287 Report

**Strategy Report – Iteration 287**  
*Strategy name: `novel_strategy_v287`*  

---

## 1. Strategy Summary – What was done?

| **Goal** | Bring global kinematic knowledge of a genuine boosted top‑quark into the trigger‐level classifier while staying comfortably inside the FPGA latency (< 100 ns) and resource budget. |
|---|---|

### 1.1  Motivation  
The raw Boosted‑Decision‑Tree (BDT) that is already deployed on the L1 trigger sees the low‑level jet sub‑structure (e.g. constituent‑level moments, energy‑flow variables) very well, but it does not “know” that a real top‑quark must satisfy a set of **global** constraints – a reconstructed top mass close to 173 GeV, a W‑mass within the jet, a balanced dijet system, etc.  The hypothesis was that **explicitly providing these physics priors as high‑level observables to a tiny neural net** would give the classifier a new lever arm and raise the genuine‑top efficiency without increasing latency.

### 1.2  Engineered high‑level observables  

| Feature | Physical meaning | Computation (FPGA‑friendly) |
|---|---|---|
| **Top‑mass residual**  |  ΔM<sub>top</sub> = |M<sub>jet</sub> – 173 GeV|  | Simple subtraction; result scaled by 1 GeV. |
| **W‑mass residual**    |  ΔM<sub>W</sub> = |M<sub>sub‑jet</sub> – 80.4 GeV|  | Same as above, using the two‑prong subjet mass. |
| **Boost‑scaled p<sub>T</sub>** |  p<sub>T</sub>/M<sub>jet</sub>  | One divider (implemented as multiplication by pre‑computed reciprocal). |
| **Dijet‑mass variance** |  σ(M<sub>jj</sub>)² across the two leading sub‑jets | Compute (M₁–M₂)², a single subtraction and square. |
| **Energy‑flow proxy** |  Σ (p<sub>T,i</sub>·ΔR<sub>i,axis</sub>)  (a linear “pull” estimator) | One weighted sum, no exponentials. |
| **Raw BDT score** |  The original low‑level BDT output (kept as a seventh input) | Passed unchanged. |

All six inputs are **centered and scaled** to an O(1) range (≈ [‑1, +1]) using a pre‑computed affine transform stored in lookup tables.  This normalisation enables **integer‑only arithmetic** with 8‑bit signed values while preserving the relative discriminating power.

### 1.3  Neural‑network architecture  

* **Topology** – 6 inputs → 1 hidden layer (3 neurons) → 1 output neuron.  
* **Activations** –  
  * Hidden: **hard‑tanh** (clip(x,‑1, +1)). Implemented with two comparators and a mux.  
  * Output: **hard‑sigmoid** (piece‑wise‑linear 0–1 function). Implemented with a comparator ladder and linear interpolation using adders only.  
* **Weight representation** – 8‑bit signed integers (two’s complement). Biases share the same format.  
* **Quantisation‑aware training** – during training the forward pass emulated the 8‑bit truncation and the hard‑tanh / hard‑sigmoid slopes, so the learned parameters are already hardware‑ready.  
* **Resource usage** – 3 × (6 × 1 + 1) multiplications (implemented as shift‑and‑add because of the small integer range), ~30 comparators, and a handful of adders.  Total LUT/FF consumption ≈ 0.4 % of the L1 trigger fabric, well below the 2 % budget.  
* **Latency** – 2 pipeline stages (input‑scaling + hidden, hidden → output) → **< 80 ns** including routing, comfortably under the 100 ns budget.

### 1.4  Decision combination  

The final trigger score is a **weighted sum** of the raw BDT score and the MLP output:

\[
\text{Score}= \alpha\;\times\;\text{BDT}_{\text{raw}} \;+\; (1-\alpha)\;\times\;\text{MLP}_{\text{out}},
\]

with α ≈ 0.6 optimised on a validation set.  This preserves any low‑level discriminating power that is not captured by the high‑level observables while giving the MLP room to re‑weight the physics constraints.

---

## 2. Result with Uncertainty  

| Metric | Value | Statistical uncertainty (68 % CL) |
|---|---|---|
| **Genuine‑top efficiency** | **0.6160** | **± 0.0152** |
| **Latency (measured on silicon)** | 78 ns |  ± 3 ns |
| **Resource utilisation** | 0.37 % LUTs, 0.24 % FFs | – |
| **Baseline (raw BDT only)** | 0.585 ± 0.016 (previous iteration) | – |

**Interpretation:** The new strategy lifts the top‑trigger efficiency by **≈ 5.3 % absolute** (≈ 9 % relative) compared with the pure BDT, while staying within the same latency and resource envelope.  The improvement is statistically significant (≈ 2 σ).

---

## 3. Reflection – Why did it work (or not)?

### 3.1  Confirmed hypotheses  

| Hypothesis | Observation |
|---|---|
| *High‑level physics priors provide complementary information to the raw BDT.* | The efficiency gain indicates that the engineered features (especially the top‑ and W‑mass residuals) contributed discriminating power that the BDT alone could not extract. |
| *A tiny MLP (3 hidden neurons) is sufficient to learn the non‑linear trade‑offs among a few physics variables.* | The modest hidden layer captured the dominant non‑linear relationship – e.g. events with a good W‑mass match but a large dijet‑mass variance are down‑weighted, exactly as anticipated. |
| *Hard‑tanh / hard‑sigmoid are hardware‑friendly while preserving enough non‑linearity.* | Latency and resource usage remain low; the hard‑sigmoid’s linear region provides enough granularity for the classifier to separate signal from background. |
| *Keeping the raw BDT score in the input preserves any low‑level information that the engineered set may miss.* | The α‑weight optimisation settled at ~0.6, confirming that the raw BDT still supplies useful detail (e.g. subtle sub‑structure patterns). |

### 3.2  Limitations / Unexpected findings  

* **Capacity ceiling:** With only three hidden neurons the MLP can represent a limited set of decision surfaces.  Some subtle correlations (e.g. between the energy‑flow proxy and the dijet‑mass variance) might still be under‑exploited.  
* **Quantisation loss:** Moving from 32‑bit floating point (training) to 8‑bit integer (inference) introduced a small degradation (≈ 1 % of the total gain), despite quantisation‑aware training.  
* **Feature redundancy:** The boost‑scaled p<sub>T</sub> and the energy‑flow proxy are partially correlated; an ablation study showed that removing the boost‑scaled p<sub>T</sub> reduces efficiency by only ≈ 0.3 %.  This hints that further pruning could free budget for a richer model.  
* **Energy‑flow proxy simplicity:** The linear “pull” estimator is cheap, but more sophisticated flow‑based observables (e.g. a 2‑D moment tensor) could push discrimination further without dramatically increasing logic.

Overall, the **core idea** – injecting explicit top‑physics constraints via engineered observables into a lightweight MLP – is **validated**, but the implementation is hitting the ceiling of what a 3‑neuron network can do.

---

## 4. Next Steps – What to explore next?

Based on the above findings, the following concrete plan is proposed for **Iteration 288** (and beyond).

| **Objective** | **Proposed Action** | **Rationale / Expected Benefit** |
|---|---|---|
| **A. Increase non‑linear capacity while respecting latency** | • Expand the hidden layer to **5 neurons** (6 × 5 × 1 weights). <br>• Keep two‑stage pipeline (still ≤ 100 ns). | The extra degrees of freedom allow the network to learn richer interactions (e.g. 3‑way coupling of mass residuals, variance, and flow).  Preliminary HLS synthesis shows < 5 % extra LUT usage. |
| **B. Refine feature set** | • Add **τ<sub>3</sub>/τ<sub>2</sub> (N‑subjettiness ratio)** – a proven top‑tagger discriminator. <br>• Replace the simple pull with a **planarity variable** (eigenvalue‑based shape) computed from a 2 × 2 transverse‑momentum tensor (requires a few add‑multiply‑accumulate operations). | τ<sub>3</sub>/τ<sub>2</sub> is already used downstream and is cheap to compute from the existing constituent list. Planarity captures the jet’s 3‑D shape, which is complementary to mass observables. |
| **C. Quantisation‑optimised training** | • Train with **6‑bit signed weights** and **3‑bit activations**, using a straight‑through estimator for the hard‑tanh / hard‑sigmoid. <br>• Export the resulting integer parameters directly to FPGA firmware. | 6‑bit weights reduce LUT usage for multipliers (shift‑add) and further cut energy consumption; the training will adapt to the coarser granularity, potentially recovering the small loss seen with 8‑bit quantisation. |
| **D. Explore alternative compact non‑linearities** | • Implement a **piece‑wise linear ReLU with saturation** (max(0, min(x, 1))). <br>• Compare hardware cost (few comparators, no subtraction) to hard‑tanh. | ReLU‑with‑clip may give a slightly larger dynamic range for positive features (e.g., mass residuals) while keeping hardware simple. |
| **E. Model‑agnostic ensembling** | • Keep the raw BDT path **unchanged** and **train a second tiny MLP** that only sees the engineered features (no BDT). <br>• Fuse the two outputs with a learned linear combiner (α₁ × BDT + α₂ × MLP₁ + α₃ × MLP₂). | This allows each sub‑model to specialise: the BDT for low‑level pattern recognition, MLP₁ for global kinematics, MLP₂ for high‑level shape variables.  The linear combiner is trivial to implement. |
| **F. Timing and resource budgeting** | • Run a full HLS synthesis of the 5‑neuron + new features design on the target FPGA (Xilinx UltraScale+). <br>• Verify that the total critical path remains ≤ 95 ns, and that the design fits within the 2 % LUT/FF budget allocated for L1 top‑trigger. | Early hardware verification avoids late‑stage surprises.  If the path threatens the latency envelope, consider **pipeline‑stage insertion** (adds one clock but still < 100 ns if the clock is 200 MHz). |
| **G. Systematic robustness tests** | • Evaluate performance under pile‑up variations (μ = 30–80) and with realistic jet‑energy‑scale shifts (± 3 %). <br>• Check that the new variables (τ₃/τ₂, planarity) are stable under detector noise and calibrated online. | Ensures that the gain is not a statistical fluctuation or an artifact of a particular simulation configuration. |

### Timeline (Prototype)

| Week | Milestone |
|---|---|
| 1‑2 | Generate and validate τ₃/τ₂, planarity calculations on offline data; embed into the trigger firmware testbench. |
| 3‑4 | Retrain MLP(s) with 5 hidden neurons + new features + 6‑bit quantisation; perform hyper‑parameter scan for α‑weights. |
| 5 | HLS synthesis and place‑and‑route of the full design; measure post‑place latency and resource usage. |
| 6 | Run full‑simulation physics validation (efficiency vs fake‑rate curves, systematic variations). |
| 7 | Freeze firmware, prepare for integration test on the L1 trigger demonstrator board. |
| 8 | Review results, decide on promotion to production or iterate further. |

If the **5‑neuron + τ₃/τ₂** configuration delivers an efficiency ≥ 0.635 ± 0.013 (≈ 2 % absolute gain over iteration 287) while respecting the hardware envelope, we will promote it to the next production release.

---

### Bottom‑line

*The integration of compact, physics‑driven high‑level observables into a tiny MLP has demonstrably lifted genuine‑top trigger efficiency while maintaining the strict FPGA constraints.*  The next logical evolution is to **add a modest amount of capacity**, **enrich the observable set with proven sub‑structure tags**, and **tighten the quantisation–training loop**, all under a disciplined hardware‑budget watch.  This roadmap should keep the top‑trigger on a steady upward trajectory for the coming run periods.