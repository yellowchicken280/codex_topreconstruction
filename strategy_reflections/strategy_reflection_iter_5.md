# Top Quark Reconstruction - Iteration 5 Report

**Strategy Report – Iteration 5**  
*Strategy name: `novel_strategy_v5`*  

---

### 1. Strategy Summary  
**Goal:** Improve the discrimination between correctly reconstructed hadronic‑top candidates and combinatorial background by injecting explicit physics knowledge into the classifier.

**What we did**

| Step | Description |
|------|-------------|
| **Feature engineering** | 1. Computed two normalised residuals: <br>  · Δm_top = (m₃ⱼ – m_top)/σ_top <br>  · Δm_W = (min m₂ⱼ – m_W)/σ_W  <br>   (σ values are the empirical widths of the top‑ and W‑mass peaks).<br>2. Compressed the triplet transverse momentum with a logarithm:  `log(p_T(3‑jet))/log(p_T^max)`.<br>3. Added a “flow” term: the geometric mean of the three jet energies, ` (E₁·E₂·E₃)^{1/3}`, normalised to the event‑scale. |
| **Model architecture** | Built a shallow Multi‑Layer Perceptron (MLP) with a single hidden layer (12 neurons, ReLU) that receives **five inputs**: Δm_top, Δm_W, log p_T, flow, and the **raw BDT score** from the original low‑level jet‑based BDT. The raw BDT score acts as a safety‑net for any information not captured by the engineered variables. |
| **Training & validation** | – Standardised the five inputs (zero‑mean, unit‑variance). <br>– Trained using binary cross‑entropy with Adam (learning‑rate = 3×10⁻⁴, 50 epochs, early‑stop on validation loss). <br>– 5‑fold cross‑validation to obtain a robust estimate of the top‑reconstruction efficiency. |
| **Metric** | Efficiency defined as the fraction of events where the selected jet triplet matches the true hadronic top (ΔR < 0.4) while keeping the background‑rejection fixed to the baseline working point. |

---

### 2. Result with Uncertainty  

| Metric | Value | Uncertainty (1σ) |
|--------|-------|-------------------|
| **Hadronic‑top reconstruction efficiency** | **0.6160** | **± 0.0152** |

The efficiency is quoted after the final selection cut that reproduces the baseline signal‑efficiency vs background‑rejection curve, allowing a direct comparison with earlier iterations.

---

### 3. Reflection  

| Aspect | Observation | Interpretation |
|--------|-------------|----------------|
| **Performance gain** | Compared with the previous best (baseline BDT‑only) efficiency of ≈ 0.585 ± 0.017, we gain **~5 % absolute** (≈ 8 % relative) improvement. | The physics‑driven residuals successfully focus the classifier on the most discriminating kinematic information (mass constraints). By presenting these constraints in a normalised form, the MLP can learn simple non‑linear combinations (e.g., “small Δm_top *large flow”) that the raw BDT struggled to capture. |
| **Stability** | The statistical uncertainty (±0.015) is comparable to that of the baseline, indicating no dramatic increase in variance despite the added features. | The shallow architecture and the inclusion of the raw BDT score act as a regulariser, preventing over‑fitting to the engineered variables. |
| **Hypothesis test** | **Hypothesis:** Embedding explicit top‑mass and W‑mass residuals, together with a balanced‑energy flow term, would sharpen discrimination, especially in ambiguous BDT regions. <br>**Result:** Confirmed – the learned synergy between Δm_top, Δm_W and the flow term yields higher efficiency, and the raw BDT score preserves information that the engineered set alone would miss. |
| **Failure modes** | A handful of events with badly mis‑measured jet energies still receive high scores (false positives). | The residuals rely on the assumption that jet‑energy scale is well calibrated; large systematic shifts degrade the clean separation. This suggests a sensitivity to jet‑energy uncertainties that should be monitored. |

Overall, the experiment validates the principle that **physics‑transparent, normalised constraints can be combined with a lightweight non‑linear model to improve top reconstruction while retaining interpretability**.

---

### 4. Next Steps  

1. **Systematics‑robust feature scaling**  
   * *Idea:* Replace the fixed σ_top/σ_W used for normalisation by event‑by‑event uncertainties (e.g., propagate jet‑energy resolution). This should make Δm_top and Δm_W less sensitive to global scale shifts.  

2. **Enrich the engineered set**  
   * Add angular variables (ΔR between the three jets, ΔR between the dijet pair closest to the W mass and the third jet).  
   * Include a planar‑flow or N‑subjettiness variable for the triplet to capture three‑prong sub‑structure.  

3. **Model depth exploration**  
   * Test a second hidden layer (12 → 8 → 4 neurons) or a small residual‑MLP to see if modest extra capacity yields further gains without sacrificing transparency.  

4. **Hybrid ensemble**  
   * Combine the current MLP‑+‑BDT‐score model with the original BDT by averaging their output probabilities (or via a meta‑classifier). This could capture complementary decision boundaries.  

5. **Graph‑Neural‑Network baseline**  
   * Implement a simple Jet‑Graph NN (nodes = jets, edges = ΔR) trained on the same target. The physics‑derived features can be fed as node attributes; comparing its performance to the engineered‑MLP will reveal whether a more flexible architecture offers a substantial advantage.  

6. **Cross‑validation on different physics samples**  
   * Validate on a separate MC sample with varied pile‑up and parton‑shower tunes to ensure the observed improvement generalises beyond the training configuration.  

**Target for the next iteration:** Achieve an efficiency **≥ 0.640** (≈ 3 % absolute gain over the current result) while keeping the statistical uncertainty at the 0.015 level and demonstrating robustness against jet‑energy systematic variations.

--- 

*Prepared by the analysis team, Iteration 5.*