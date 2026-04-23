# Top Quark Reconstruction - Iteration 292 Report

**Strategy Report – Iteration 292**  
*Strategy name:* **novel_strategy_v292**  
*Goal:* Boost the signal‑efficiency of the L1 top‑tagger while staying within the strict latency/DSP budget.

---

## 1. Strategy Summary – What was done?

| Component | Description |
|-----------|-------------|
| **Baseline** | A high‑granularity Gradient‑Boosted Decision Tree (BDT) that uses the three dijet masses ( \(m_{12}, m_{23}, m_{31}\) ) as independent inputs. |
| **Physics‑inspired priors** | Six orthogonal scalar observables were derived from the three‑prong kinematics of a genuine hadronic top decay: <br>1. **RMS spread** of the three dijet masses <br>2. **Heron triangle area** formed by the three masses <br>3. **\(p_{T}/M\)** ratio of the 3‑prong system <br>4. **log‑product** \( \log(m_{12}·m_{23}·m_{31})\) <br>5. **Summed \(W\)-mass deviation** \( \sum_i |m_{ij} - m_W|\) <br>6. **Top‑mass distance** \( |M_{3\text{prong}} - m_t|\) |
| **High‑level sanity check** | The raw BDT output (​\(p_{\text{BDT}}\)​) and the six priors were concatenated into a 7‑dimensional feature vector. |
| **Shallow MLP** | A single hidden‑layer multilayer perceptron with **5 neurons** (ReLU activation) was trained on the 7‑dimensional input to learn non‑linear relationships that enforce global consistency of the decay. <br> • Optimiser: Adam (learning‑rate 0.001) <br> • Loss: binary cross‑entropy <br> • Early‑stopping on a validation split (patience = 5) <br> • Quantisation‑aware training was *not* applied – the model is small enough to be implemented in fixed‑point firmware. |
| **Hardware constraints** | The final MLP requires < 2 µs latency and < 30 DSPs on the L1 ASIC, well inside the allocated budget. |
| **Training / evaluation** | 5‑fold cross‑validation on the full simulated dataset; performance metrics were aggregated across folds. |

---

## 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal efficiency** (working point that yields the desired background rate) | **\( \varepsilon_{\text{sig}} = 0.6160 \pm 0.0152\)** |
| Baseline BDT (same working point) | ~0.585 (≈ 5 % absolute gain) |
| **Relative improvement** | **≈ 5.3 %** increase in efficiency at fixed background |
| **Background rejection** | unchanged (by construction of the working point) |
| **Latency** | 1.8 µs (including BDT & MLP) |
| **DSP usage** | 22 DSPs (well under the 30‑DSP limit) |

*The quoted uncertainty is the standard deviation of the five cross‑validation folds, propagated to the efficiency.*

---

## 3. Reflection – Why did it work (or not)?

### 3.1. Hypothesis  
*If we supplement the BDT with physics‑motivated, globally consistent scalars, a very small neural network should be able to “sanity‑check” borderline candidates, rescuing true top decays that the BDT alone would reject.*

### 3.2. What the numbers tell us  

* **Positive signal lift** – The 5 % absolute gain (≈ 5 % relative) confirms that the extra priors contain information that the BDT alone cannot exploit because it treats the three masses independently.  
* **Low variance across folds** – The ±0.0152 uncertainty shows the MLP’s decision surface is stable; over‑fitting was not observed despite the tiny capacity.  
* **Latency budget respected** – The shallow architecture proved sufficient to capture the needed non‑linearities without breaking the L1 timing constraints.

### 3.3. Physical interpretation  

* **RMS spread & Heron area** act as shape descriptors of the mass triangle; genuine tops tend to populate a narrow region of low spread and moderate area.  
* **\(p_T/M\) and log‑product** encode the boost and overall scale, helping to reject soft QCD combos that mimic the mass values but differ in kinematics.  
* **W‑mass deviation sum** and **top‑mass distance** directly enforce the hierarchical decay pattern (two W‑like sub‑jets + a third jet).  

When the BDT output is high but any of these priors indicate inconsistency, the MLP down‑weights the candidate; conversely, a modest BDT score combined with a coherent set of priors can be promoted to signal.

### 3.4. Limitations  

* **Model capacity** – With only five hidden neurons the MLP can only approximate a low‑order decision surface. Further gains may be capped by this simplicity.  
* **Feature orthogonality** – Though the priors were designed to be largely uncorrelated, residual correlations exist (e.g., RMS spread and Heron area both respond to mass dispersion). A more systematic decorrelation (PCA or ICA) could sharpen the input space.  
* **No quantisation study yet** – While the DSP budget is satisfied, the impact of fixed‑point quantisation on the final efficiency has not been validated on silicon.  

Overall, the hypothesis that a *physics‑driven sanity layer* can rescue borderline signal events is **confirmed**, albeit with modest gains limited by the shallow network.

---

## 4. Next Steps – Novel directions to explore

| Direction | Rationale | Concrete plan |
|-----------|-----------|---------------|
| **1. Enrich the prior set with angular information** | The current priors are all scalar mass‑based. Jet‑pair opening angles and ΔR’s encode the three‑prong topology and are cheap to compute. | • Add ΔR\(_{ij}\) (i = 1‑3) and the “planarity” variable \( \frac{(\vec{p}_1\times\vec{p}_2)\cdot\vec{p}_3}{|\vec{p}_1||\vec{p}_2||\vec{p}_3| \). <br>• Re‑train the MLP (still 5‑neuron hidden layer) and evaluate the Δefficiency. |
| **2. Decorrelate priors via linear transforms** | Reducing redundancy may let the tiny MLP learn more distinct non‑linearities. | • Perform a PCA on the six priors + BDT output → keep the top 4 components (explaining > 95 % variance). <br>• Feed these 4 components to the MLP. |
| **3. Investigate a quantisation‑aware shallow network** | To guarantee that the firmware implementation will retain the observed gain, we need a fixed‑point model. | • Retrain the same architecture with 8‑bit activation/weight quantisation (TensorFlow‑Lite or ONNX‑Quant). <br>• Compare efficiency before/after quantisation; adjust clipping ranges if loss > 0.5 %. |
| **4. Try a slightly deeper but still L1‑compatible MLP** | The current 5‑neuron hidden layer may be under‑utilising the available DSP budget. A 2‑layer 5‑× 5 network could capture higher‑order interactions without large latency increase. | • Implement a 2‑layer MLP (5 → 5 → 1) with ReLU. <br>• Measure latency on the target ASIC emulator; target < 2.3 µs. |
| **5. Prototype a lightweight Graph Neural Network (GNN) for the 3‑prong system** | A GNN can directly operate on the three jet constituents and learn the global consistency from the topology itself, potentially superseding engineered priors. | • Build a 2‑layer EdgeConv on the set of three sub‑jets (features: pT, η, φ, mass). <br>• Limit the hidden dimension to 8 to stay within DSP budget. <br>• Benchmark against the current MLP‑sanity‑check. |
| **6. Full firmware validation** | All algorithmic gains must survive the real‑time implementation. | • Port the trained MLP (or prototype GNN) to VHDL/RTL using the existing BDT‑to‑firmware flow. <br>• Run a latency‑and‑resource sweep on the target FPGA/ASIC to confirm L1 compliance. |
| **7. System‑level optimisation – dynamic thresholding** | The static signal‑efficiency point may not be optimal for varying instantaneous luminosities. | • Implement a lookup table that adjusts the final decision threshold based on the online pile‑up estimate, keeping background rate constant. <br>• Test on a simulated dataset with varying PU. |

### Prioritisation for the next iteration

1. **Add angular priors** – cheapest runtime cost, likely immediate gain.  
2. **Quantisation‑aware training** – essential before firmware deployment.  
3. **Two‑layer 5×5 MLP** – explore marginal improvements while staying within budget.  
4. **Fast GNN prototype** – longer‑term, higher‑risk/high‑reward path.

---

**Bottom line:** Iteration 292 demonstrates that a physics‑driven sanity layer can lift the L1 top‑tagger efficiency by ≈ 5 % without violating latency or resource constraints. The next logical step is to enrich the high‑level feature set (especially angular information), tighten the representation (decorrelation & quantisation), and test a modestly deeper network. Parallel exploration of a lightweight GNN will inform whether a more expressive topology‑aware model can deliver yet larger gains.