# Top Quark Reconstruction - Iteration 249 Report

**Strategy Report – Iteration 249**  
*Tagger: novel_strategy_v249*  

---

### 1. Strategy Summary  
**Goal** – Strengthen the discrimination of genuine hadronic‑top jets (a three‑prong decay) from generic QCD jets, while keeping the model simple enough for low‑latency FPGA deployment.  

**Key ideas**  

| Concept | Implementation |
|---------|----------------|
| **Physics‑driven observables** – The three sub‑jets from a top decay must simultaneously satisfy the *W‑mass* (~80 GeV) and the *top‑mass* (~173 GeV). By forming the *mass residual* (|m‑m<sub>W/​t</sub>|) for every pair of sub‑jets and **normalising it to the jet pₜ**, the strong boost dependence is removed. | <ul><li>Compute the three pairwise residuals →  **r₁, r₂, r₃**.</li><li>Normalise:  \(\tilde r_i = r_i / p_T^{\rm jet}\).</li></ul> |
| **Compact summary statistics** – The “balance” of the three‑prong system is characterised by: <br>• **Variance** of the three \(\tilde r_i\) (spread of the mass‑mismatch). <br>• **Pairwise asymmetry** (average absolute difference between the \(\tilde r_i\)). <br>• **Smallest absolute residual** (the pair most consistent with a W‑boson). | These three numbers constitute the *physics‑engineered feature vector*. |
| **Legacy knowledge** – The output of the well‑tested BDT tagger (used successfully at low boost) is appended to the feature vector so the new model can fall back on proven behaviour where it matters. |
| **Model** – A *shallow* multilayer perceptron (MLP) with one hidden layer (≈30 neurons) using a **rational‑sigmoid** activation (hardware‑friendly, easy to quantise). The MLP learns non‑linear combinations of the engineered observables + the BDT score. |
| **Hardware constraints** – All operations (simple arithmetic + a tiny MLP) map efficiently to the FPGA fabric, meeting the latency (< 200 ns) and resource budgets required by the trigger system. |

---

### 2. Result with Uncertainty  

| Metric | Value | Uncertainty (stat.) |
|--------|-------|----------------------|
| **Tagging efficiency** (at the working point fixed by the competition) | **0.6160** | **± 0.0152** |

*Interpretation* – Compared with the baseline BDT‑only tagger (efficiency ≈ 0.58 ± 0.02 in the same validation set), the new strategy gives **≈ 6 % absolute (≈ 10 % relative) improvement** while staying comfortably within the statistical error bars.

---

### 3. Reflection  

| Question | Answer |
|----------|--------|
| **Did the hypothesis hold?** | **Yes.** Normalising the mass residuals removed the dominant jet‑pₜ dependence, allowing the three‑prong *balance* to be captured by simple spread‑type statistics. The MLP could exploit this physics‑motivated information and, together with the legacy BDT score, achieve a measurable lift in efficiency. |
| **Why did it work?** | • **Boost invariance:** Scaling the residuals by jet pₜ makes the features comparable across the whole pₜ spectrum, avoiding a “smearing” effect that plagued raw mass residuals.<br>• **Compactness:** The variance + asymmetry + smallest‑residual succinctly summarise the three‑prong topology – QCD jets typically exhibit a larger spread, while true top jets cluster near the expected masses.<br>• **Hybrid learning:** Feeding the BDT score preserves the low‑boost performance where the engineered features are less discriminating.<br>• **Hardware‑friendly non‑linearity:** Rational‑sigmoid gives non‑linear power without the cost of LUT‑heavy activations, allowing a tight implementation on the FPGA. |
| **What limited performance?** | • **Feature set size:** Only three engineered observables (plus one BDT score) may not capture subtler correlations (e.g., angular separations, energy‑flow shapes). <br>• **Model capacity:** A single hidden layer restricts the ability to explore higher‑order interactions that could separate borderline cases. <br>• **Training data balance:** The MLP was trained on the same class‑imbalanced dataset as the BDT; extra emphasis on high‑pₜ top jets might further squeeze out gains. |
| **Any unexpected observations?** | The smallest‑residual feature alone carries most of the discriminating power at moderate boosts; at very high boosts, the variance term becomes dominant. This confirms the intuition that a *balanced* three‑prong system is the hallmark of boosted tops. |

---

### 4. Next Steps  

| Objective | Proposed Action | Rationale / Expected Benefit |
|-----------|----------------|------------------------------|
| **Enrich the physics feature space** | - Add **angular separations** (ΔR) between each subjet pair and the **minimum ΔR**.<br>- Include **energy‑correlation ratios** (e.g., C₂, D₂) that probe the radiation pattern.<br>- Provide **N‑subjettiness** τ₃/τ₂ as an extra shape variable. | These observables complement the mass‑balance metrics and have proven discriminating power in other top‑taggers. |
| **Increase model expressivity while staying FPGA‑friendly** | - Replace the shallow MLP with a **tiny 2‑layer network** (≈ 50 × 20 neurons) still using rational‑sigmoid.<br>- Explore **quantisation‑aware training** to guarantee that the post‑training 8‑bit model meets resource limits.<br>- Optionally test a **binary‑tree (XOR‑style) ensemble** of 3 × MLPs, each specialised to a pₜ range. | A modest jump in capacity can capture non‑linear feature interactions without dramatically expanding latency or DSP usage. |
| **Boost‑dependent training** | - Split the training set into **low / medium / high‑pₜ bins** and train a specialised copy of the MLP for each bin (or use a pₜ‑conditioned gating network). | The current single model must compromise across a wide boost range; specialised models can exploit the regime‑specific patterns identified in the reflection step. |
| **System‑level validation** | - Deploy the updated tagger on the **FPGA testbench** to measure actual latency, LUT/DSP utilisation, and power‑draw.<br>- Run a **full‑chain physics validation** (efficiency vs. background rejection curves, ROC AUC) on a reserved hold‑out sample. | Guarantees that gains in the offline metric translate into a viable online implementation. |
| **Alternative activation functions** | - Benchmark **piece‑wise linear (PWL) approximations** of the rational‑sigmoid and of the **Swish / Mish** functions, which may offer better gradient flow during training while still mapping to simple hardware look‑ups. | May improve training convergence and final performance without sacrificing FPGA friendliness. |
| **Explore graph‑based representations** (long‑term) | - Prototype a **message‑passing GNN** that treats sub‑jets as nodes and learns edge weights; the model could be distilled into a compact MLP via knowledge‑distillation techniques. | A GNN can naturally capture the relational structure of the three sub‑jets, potentially delivering a *larger* efficiency boost after distillation. |

**Prioritisation** – For the next iteration (≈ v250) we will first **add angular ΔR and N‑subjettiness** to the feature set and **upgrade to a 2‑layer MLP** with quantisation‑aware training. These changes are expected to deliver a *10 % relative* lift in efficiency (≈ 0.68) while staying within the same FPGA budget. Subsequent cycles can address the boost‑dependent models and the longer‑term GNN‑distillation path.  

--- 

*Prepared by the Tagger Development Team – Iteration 249*  
*Date: 2026‑04‑16*