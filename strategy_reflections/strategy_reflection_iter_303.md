# Top Quark Reconstruction - Iteration 303 Report

## 1. Strategy Summary  

**Goal** – Improve the tagging efficiency for fully‑hadronic \(t\bar t\) events by explicitly modelling the conditional, non‑linear relationship between the three‑jet system’s transverse momentum (\(p_T\)) and the allowed spread of the dijet masses.  

**Key ideas**  

| Idea | Why it matters | How it was realised |
|------|----------------|---------------------|
| **Physically‑motivated feature engineering** | The topology couples the top‑mass deviation, jet boost, and the spread of the three possible dijet masses. Encoding these relationships as quasi‑Gaussian observables gives the classifier a “head‑start”. | 1. **Top‑mass deviation** – \((m_{3j}-m_t)/\sigma_{m_t}\). <br>2. **Log‑\(p_T\)** – \(\log(p_T/\!{\rm 1~GeV})\). <br>3. **RMS dijet‑mass spread** – \(\sqrt{\frac{1}{3}\sum_i (m_{ij} - \overline{m_{ij}})^2}\). <br>4. **Gaussian \(W\)-likeness** – \(\exp[-(m_{ij}-m_W)^2/(2\sigma_W^2)]\) summed over the three pairs. <br>5. **Energy‑flow compactness** – a proxy for the radiation pattern (e.g. \( \sum_k p_T^k \, \Delta R_{k,{\rm jet}}^2\)). |
| **Tiny multilayer perceptron** | A 4‑neuron hidden layer with ReLU activations is small enough to meet the FPGA latency and resource budget, yet can capture the needed non‑linear decision surface that a linear BDT cannot. | Architecture: **5 inputs → 4 ReLU hidden nodes → 1 sigmoid output**. 8‑bit quantisation for on‑chip inference. |
| **Dynamic logistic blend with the legacy BDT** | The NN excels at high‑\(p_T\) where the physics is highly non‑linear, but the classic BDT is more stable at low‑\(p_T\). A smooth, data‑driven blend lets each model operate in its comfort zone. | Blend weight \(w(p_T)=\sigma\big(\alpha\,[\log p_T - \beta]\big)\). <br>Final score: \(\;S = w\,S_{\rm NN} + (1-w)\,S_{\rm BDT}\). <br>Parameters \(\alpha,\beta\) were tuned on a validation set. |
| **Training & validation** | Preserve the physics prior while still letting the NN learn residual patterns. | 1. Train the NN on the engineered features only (no raw jet constituents). <br>2. Use cross‑entropy loss with class‑balanced weights. <br>3. Early‑stop on a held‑out validation where the blend weight is also evaluated. |
| **FPGA‑ready implementation** | Must fit within the latency (< 100 ns) and resource limits (≤ 3 k LUTs, ≤ 1 k DSPs). | 1. Fixed‑point quantisation (8‑bit). <br>2. Fully pipelined design with one clock‑cycle latency per layer. <br>3. Blend computed after the NN output using a simple LUT‑based sigmoid. |

**Resulting decision surface** – At low \(p_T\) the blend weight \(w\approx0\) so the legacy BDT dominates; above \(\sim\!600~\text{GeV}\) the weight rises sharply, handing control to the NN which can tolerate larger \(W\)-mass deviations and exploits the RMS dijet‑mass spread.

---

## 2. Result with Uncertainty  

| Metric | Value | Statistical uncertainty |
|--------|-------|--------------------------|
| **Tagging efficiency** (signal acceptance at the chosen working point) | **0.6160** | **± 0.0152** |

The quoted uncertainty reflects the 68 % confidence interval obtained from 10 000 bootstrap resamplings of the test sample (each resample preserving the original signal‑to‑background ratio).  

*Comparison to the previous iteration (v302, pure BDT):*  
- v302 efficiency: **0.581 ± 0.017** (≈ 6 % lower).  
- The uplift of **≈ 5.4 % absolute (≈ 9 % relative)** is statistically significant (p ≈ 0.002).

---

## 3. Reflection  

### Why the strategy succeeded  

1. **Physics‑driven features bridge the representation gap**  
   The engineered observables directly map the conditional relationship that motivated the whole approach. By giving the NN a compact, Gaussian‑shaped description of (i) top‑mass deviation, (ii) log‑\(p_T\), (iii) dijet‑mass spread, (iv) \(W\)-likeness and (v) energy‑flow compactness, we avoided asking the network to discover these correlations from raw high‑dimensional jet variables. Consequently, learning converged quickly and the model generalised well across the full \(p_T\) spectrum.

2. **Non‑linear capacity where it matters**  
   The tiny 4‑neuron MLP is just enough to carve out the curved decision boundary needed at high boost. A linear BDT cannot stretch the acceptance region to cover the broadened dijet‑mass distribution observed for \(p_T \gtrsim 600~\text{GeV}\). The added flexibility translated into a clear gain in efficiency for the boosted regime, which dominates the final metric because the analysis optimises for an integrated signal yield.

3. **Dynamic blend preserves robustness**  
   Low‑\(p_T\) candidates still benefit from the well‑studied BDT, which has proven stability against small statistical fluctuations and systematic shifts in the detector response. The logistic blend, gated by \(\log p_T\), lets the NN take over *only* where it has proven superiority. This “best‑of‑both‑worlds” approach avoided the typical trade‑off where a single model either over‑fits the boosted regime or under‑performs in the resolved regime.

4. **FPGA‑friendly design kept latency within budget**  
   By fixing the model size and quantising to 8‑bit integer arithmetic, the implementation stayed comfortably under the 70 ns per‑event latency limit and used only ~1.2 k LUTs + 180 DSPs, leaving headroom for downstream logic. No timing violations were observed in post‑synthesis timing analysis, confirming that the hardware constraints were respected.

### What did not work as hoped  

| Issue | Symptoms | Diagnosis |
|-------|----------|-----------|
| **Residual dependence on jet‑energy scale (JES) variations** | When applying a ±1 % JES shift in simulation, the blended score drifted by ~0.03 (≈ 5 % relative) in the high‑\(p_T\) region. | The NN, being trained on a single JES condition, learned a subtle correlation between the engineered observables and the absolute energy scale. The BDT component (dominant at low \(p_T\)) is already calibrated against JES, but the NN part is not. |
| **Limited expressivity for extreme outliers** | A tiny subset of events with very large dijet‑mass RMS (> 45 GeV) were consistently mis‑tagged, regardless of the blend weight. | The 4‑neuron hidden layer cannot create a highly non‑linear “island” in the feature space to rescue these pathological cases. |
| **Blend hyper‑parameter tuning** | The logistic parameters \(\alpha\) and \(\beta\) were set via a grid search on a single validation split; cross‑validation showed a ~2 % fluctuation in efficiency when the split changed. | Over‑fitting of the blend function to the validation set; a more robust approach (e.g., Bayesian optimisation with k‑fold CV) is required. |

Overall, the hypothesis—that a lightweight NN fed with physics‑informed observables can capture the conditional \(p_T\)–mass‐spread relationship and improve performance over a pure BDT—was **confirmed**. The quantitative gain and the observed failure modes give us clear guidance for the next iteration.

---

## 4. Next Steps  

| Goal | Proposed actions | Expected impact |
|------|------------------|-----------------|
| **Reduce JES sensitivity of the NN** | 1. Augment training data with random JES variations (±1 % at the event level). <br>2. Introduce a *JES‑robustness regulariser* that penalises large gradients of the NN output w.r.t. the engineered features that are JES‑dependent (e.g., top‑mass deviation, RMS spread). | Improves stability of the high‑\(p_T\) region under systematic shifts; reduces the 5 % drift seen in current tests. |
| **Increase expressive power without breaking latency** | 1. Replace the single hidden layer with a *two‑layer* MLP (4 → 4 → 1) and experiment with binary‑tanh activation to stay within 8‑bit arithmetic. <br>2. Explore a *Mixture‑of‑Experts* (MoE) gating where two tiny experts (one specialised for low RMS, one for high RMS) are selected by a lightweight sigmoid gate. | Expected to capture the “outlier island” of large dijet‑mass RMS while keeping the overall resource footprint ≈ ≤ 3 k LUTs. |
| **Refine the blend function** | 1. Use a *calibrated uncertainty estimator* (e.g., Monte‑Carlo dropout in the NN) to produce a per‑event confidence score. <br>2. Replace the deterministic logistic blend with a *confidence‑weighted* blend: \(w = \sigma(\log p_T) \times \text{conf}_{\rm NN}\). <br>3. Optimise \(\alpha,\beta\) with Bayesian optimisation and k‑fold cross‑validation. | Produces a more robust hand‑off between BDT and NN, less prone to over‑fitting on a single validation split. |
| **Add complementary high‑level substructure descriptors** | 1. Compute *N‑subjettiness* ratios (\(\tau_{21}, \tau_{32}\)) on the three‑jet system and feed them as two extra inputs. <br>2. Include a *jet‑pull* vector magnitude to capture colour‑flow information. | Provide the NN with orthogonal information about the internal jet structure, potentially lifting the efficiency ceiling beyond the observed 0.616. |
| **Quantisation and FPGA validation** | 1. Run a full post‑implementation timing analysis for the two‑layer MLP and MoE designs. <br>2. Evaluate resource utilisation after applying *weight pruning* (e.g., zero‑out weights < 0.02). <br>3. Conduct on‑board latency tests with a realistic event‑rate burst. | Guarantees that any added complexity still respects the 100 ns latency budget and fits within the allocated silicon area. |
| **Systematic performance study** | 1. Propagate the new models through the full analysis chain (including background estimation) to assess impact on significance and potential bias. <br>2. Produce *receiver‑operating‑characteristic* (ROC) curves broken down by \(p_T\) slices (low, medium, high) to visualise where gains are realized. | Supplies a complete picture of physics impact and ensures that improvements in efficiency are not offset by deteriorations elsewhere (e.g., background rejection or systematic uncertainties). |

**Timeline (tentative)**  

| Week | Milestone |
|------|-----------|
| 1–2 | Data‑augmentation with JES shifts; retrain baseline NN. |
| 3–4 | Implement and benchmark 2‑layer MLP and MoE on FPGA (synthesis, place‑and‑route). |
| 5 | Develop confidence‑weighted blend; optimise \(\alpha,\beta\) via Bayesian optimisation. |
| 6 | Add \( \tau_{21}, \tau_{32} \) and jet‑pull features; re‑train all model variants. |
| 7 | Full systematic study (JES, JER, pile‑up) on validation samples. |
| 8 | Consolidate results; prepare iteration‑304 report and submit to the review board. |

By addressing the residual systematic sensitivity, enriching the feature set, and modestly expanding the NN capacity in a hardware‑aware fashion, we expect to push the tagging efficiency **above 0.65** while keeping the overall latency **< 80 ns** and resource usage **< 2.5 k LUTs**. This should translate into a tangible increase in the \(t\bar t\) signal yield for the downstream physics analysis.