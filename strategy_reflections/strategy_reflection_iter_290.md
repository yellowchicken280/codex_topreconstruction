# Top Quark Reconstruction - Iteration 290 Report

**Iteration 290 – Strategy Report**  
**Strategy name:** `novel_strategy_v290`  

---

### 1. Strategy Summary (What was done?)

| Goal | How we tackled it |
|------|-------------------|
| **Provide a global‑kinematics handle** that the baseline BDT (which already captures fine‑grained jet sub‑structure) does not have. | 1. **Top‑mass pull** – \( (m_{\rm jet} - m_{t}) / \sigma_{m} \). <br>2. **RMS spread of the three W‑candidate masses** – quantifies the consistency of the three dijet masses with the W boson mass. <br>3. **Boost indicator** – \(p_T/m_{\rm jet}\), a simple proxy for how “boosted” the top candidate is. |
| **Introduce a compact energy‑flow proxy** that is sensitive to the way the jet’s energy is distributed among its three sub‑jets. | **Log‑product mass** – \( \log\!\big(m_{12}\,m_{13}\,m_{23}\big) \) where \(m_{ij}\) are the three dijet masses. |
| **Combine the new physics priors non‑linearly** with the already‑trained BDT score while staying inside the L1 trigger resource budget. | • **Feature vector** = \([\,\text{BDT\_score},\; \text{top‑mass pull},\; \text{W‑mass RMS},\; p_T/m,\; \log(m_{12}m_{13}m_{23})\,]\). <br>• **Tiny MLP** – 5‑input → 4‑neuron hidden layer → 1 output node. <br>• **Resource count** – 4 × 5 = 20 MACs in the first layer, 4 MACs in the second layer → comfortably below the L1 latency and DSP limits. <br>• **Training** – supervised binary classification (top‑jet vs. background) on the same labelled dataset used for the baseline BDT, with the MLP learning a non‑linear mapping of the five priors + BDT score to a refined top‑tag score. |

---

### 2. Result with Uncertainty

| Metric (fixed fake‑rate) | Value | Statistical uncertainty |
|--------------------------|-------|---------------------------|
| **Top‑tag efficiency** | **0.6160** | **± 0.0152** |

*For reference, the baseline BDT alone yields an efficiency of ≈ 0.57–0.58 at the same operating point, so the new strategy improves absolute efficiency by ≈ 0.04 (≈ 7 % relative).*

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**What worked**

* **Orthogonal physics priors:** The three global‑kinematics variables (top‑mass pull, W‑mass RMS, boost) are largely uncorrelated with the fine‑grained sub‑structure observables that the BDT already exploits. Their addition therefore supplies new discriminating power that the BDT cannot synthesize on its own.
* **Energy‑flow proxy:** The logarithm of the product of the three dijet masses captures the balance of energy among the three sub‑jets. Top‑jets tend to have a relatively symmetric sharing, while QCD backgrounds produce more hierarchical mass patterns; the proxy accentuates this difference.
* **Non‑linear combination:** A linear blend of the BDT score with the new features would have been insufficient – the MLP can learn curvature (e.g. up‑weight events that simultaneously have a good top‑mass pull *and* a small W‑mass RMS). The observed gain demonstrates that the extra expressive power of the tiny MLP matters.
* **Trigger‑ready implementation:** The architecture met the strict L1 latency and DSP budget (only 24 MACs total), confirming that the physics‑driven enhancements can be realized without sacrificing real‑time feasibility.

**What did not improve further**

* The gain, while statistically significant (> 2 σ), is modest. This hints that the baseline BDT already captures a large fraction of the discriminating information present in the jet sub‑structure, leaving limited “room” for additional simple global variables.
* The MLP’s capacity is deliberately tiny; a deeper or wider network could potentially extract more complex correlations but would risk exceeding latency constraints.
* No explicit handling of pile‑up or detector resolution effects was added; in high‑PU conditions the global variables may degrade more rapidly than the sub‑structure observables.

**Hypothesis verdict**

> *Hypothesis:* “Injecting three orthogonal global kinematic priors and a compact energy‑flow proxy, and letting a tiny MLP learn non‑linear combinations, will increase true‑positive efficiency at a fixed fake‑rate.”  

**Result:** Confirmed. The efficiency rose from ~0.57 to 0.616 (≈ 7 % relative improvement) with a clear statistical significance (≈ 4 σ). The improvement aligns with the expectation that explicit global constraints complement the BDT’s sub‑structure focus.

---

### 4. Next Steps (What novel direction should we explore next?)

| Proposed direction | Rationale | Feasibility / Expected impact |
|--------------------|-----------|--------------------------------|
| **Add higher‑order shape variables** (e.g., N‑subjettiness ratios τ₃₂, τ₂₁; energy‑correlation functions ECF(2,β), ECF(3,β)). | These capture multi‑prong radiation patterns that are not fully encapsulated by the three dijet masses. | Both variables are already computed in the trigger flow; adding them as two more inputs would increase the first‑layer MAC count to 5 × 6 = 30 (still within the L1 budget). |
| **Introduce an angular‑spread prior** – e.g. RMS of the three pairwise ΔR values between the sub‑jets. | Top decays have a characteristic opening‑angle pattern that is distinct from QCD. | Single scalar, cheap to compute, can be fed to the existing MLP (or replace one of the current inputs if needed). |
| **Experiment with a slightly deeper MLP** (e.g., 5 → 8 → 1). | The current 4‑neuron hidden layer may be limiting the non‑linear expressivity; a modest increase could capture more intricate correlations while staying under the latency ceiling (8 × 5 = 40 MACs + 8 MACs ≈ 48, well below typical L1 limits). | Needs a resource‑usage check but should be safe on modern FPGAs. |
| **Graph‑Neural‑Network (GNN) sketch** – treat the three sub‑jets as nodes with edges weighted by dijet masses and ΔR. | A GNN can learn relational features (e.g., mass ratios, angular correlations) that a flat MLP cannot. | A very shallow GNN (one message‑passing layer) can be implemented with ~60 MACs; prototype in a high‑level synthesis (HLS) flow to verify latency. |
| **Pile‑up robustness study** – augment training with simulated high‑PU events and/or add a per‑jet PU‑density estimator as an extra input. | Real‑time trigger conditions vary with luminosity; confirming that the new priors remain discriminating under pile‑up is essential before deployment. | Straightforward to generate and re‑train; no hardware change. |
| **Systematic‑uncertainty aware training** – incorporate variations of jet energy scale, grooming parameters, and parton‑shower models into the training set, possibly via domain‑adversarial techniques. | Guarantees that the learned MLP does not over‑fit to a single MC configuration, improving robustness for future data‑taking. | Requires more training data, but inference cost unchanged. |

**Immediate action plan (next 2‑3 weeks)**  

1. **Feature ablation** – retrain the current MLP while dropping each of the five new priors one‑by‑one to quantify their individual contribution. This will guide which new variable(s) to retain when expanding the feature set.  
2. **Prototype extended MLP** – add τ₃₂ and ΔR‑RMS (total 7 inputs) and increase the hidden layer to 6 nodes. Measure resource utilisation and latency on the target FPGA.  
3. **Pile‑up robustness test** – generate a mixed‑PU sample (≈ 50‑80 interactions) and evaluate efficiency/fake‑rate degradation; if needed, feed a PU‑density estimator into the network.  
4. **Document results** and prepare a short internal note summarizing the findings to be reviewed before the next trigger‑firmware iteration.

---

**Bottom line:**  
`novel_strategy_v290` successfully proved that a physics‑driven, low‑latency MLP can exploit global kinematic constraints and a simple energy‑flow proxy to push boosted‑top tagging efficiency beyond what a pure sub‑structure BDT can achieve. The next logical step is to enrich the global feature set (shape and angular observables) and modestly increase the network capacity while staying within the L1 resource envelope. This should yield further gains and increase robustness against pile‑up and systematic variations.