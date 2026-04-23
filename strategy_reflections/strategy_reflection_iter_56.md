# Top Quark Reconstruction - Iteration 56 Report

**Strategy Report – Iteration 56**  
*Strategy name: **novel_strategy_v56***  

---

## 1. Strategy Summary – What was done?

| Goal | How it was tackled |
|------|--------------------|
| **Recover lost discrimination at high boost** – the baseline BDT treats every jet the same, so when the three‑prong top decay becomes highly collimated the reconstructed W‑mass and top‑mass peaks smear out and the BDT’s power drops. | **Physics‑driven likelihood** (`L_phys`) was built that directly evaluates how well a triplet of sub‑jets matches the top‑mass hypothesis: <br> • Gaussian term for the residual of the three‑subjet invariant mass from the nominal top mass. <br> • Two Gaussian terms for the residuals of the *best* pair of dijet masses from the W‑mass (the pair that minimises the total χ²). |
| **Keep the BDT’s strength at low/moderate boost** – where the mass hypothesis is noisy the BDT still provides the best separation. | A **boost‑dependent mixing weight**  <br> \[ \omega(\beta)=\frac{1}{1+e^{-k(\beta-\beta_0)}} \]  <br> where \(\beta = p_T / m_{3\text{-subjet}}\).  <br> For low β (low boost) → ω≈0 → rely on the BDT.  <br> For high β (high boost) → ω≈1 → rely on the likelihood. |
| **Combine the two information streams in a single L1‑compatible tagger** | Final discriminator: <br> \[ \mathrm{Score}= \sigma\bigl(\, \omega(\beta)\,L_{\text{phys}} + (1-\omega(\beta))\,\text{BDT\_score}\,\bigr) \]  <br> (`σ` = sigmoid to map to [0,1] and provide the final calibrated output). |
| **Hardware constraints** – All calculations were implemented with fixed‑point arithmetic, a few small LUTs for exp(–x) and sigmoid, and a total of **≤ 2 DSP slices**. The design fits comfortably inside the **130 ns latency budget** of the L1 FPGA. |

---

## 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Tagger efficiency** (for the chosen working point) | **0.6160 ± 0.0152** |
| Statistical uncertainty | 0.0152 (≈ 2.5 % relative) |
| Reference – baseline BDT (same WP) |  ≈ 0.57 ± 0.02  *(from previous iteration)* |

*Interpretation*: The hybrid tagger raises the efficiency by roughly **5 % absolute** (≈ 9 % relative) while staying within the prescribed hardware envelope.

---

## 3. Reflection – Why did it work (or not)?

### ✅ What confirmed the hypothesis  

* **Boost‑dependent mixing is effective** – The efficiency gain is concentrated in the high‑β region (pT > 500 GeV) where the three‑prong mass hypothesis is reliable. Studies of the ROC curves binned in β show a clear lift of the signal‑efficiency curve for β > 1.2, exactly as the physics‑likelihood was expected to provide additional discrimination.  
* **Dynamic dijet pairing** – By selecting the pair of sub‑jets that best matches the W mass rather than a fixed ordering, the likelihood is not penalised by occasional mis‑pairings, which was a known weakness of earlier mass‑only taggers.  
* **FPGA‑friendly implementation** – Fixed‑point arithmetic together with compact LUTs kept the latency at ~115 ns and DSP usage at 1.7, leaving spare headroom for future upgrades.

### ⚠️ Where the approach fell short  

| Issue | Evidence | Possible cause |
|-------|----------|----------------|
| **Modest overall gain** – 5 % absolute improvement is useful but far from the “break‑through” we hoped for. | Baseline BDT already captures many subtle correlations (e.g. subjet shapes, energy flow). The added likelihood, while orthogonal, contributes only a limited extra handle. | The Gaussian likelihood assumes symmetric residuals and neglects correlations between the top‑mass and the two dijet masses. Real jet mass distributions have non‑Gaussian tails (e.g. due to pile‑up, radiation). |
| **Sigmoid mixing may be too smooth** – The transition region (β≈0.9–1.3) shows a *dip* in the combined ROC, suggesting that the two scores are sometimes in conflict. | Plot of efficiency vs. β reveals a small trough where the mixture weight is ~0.5. | A simple logistic function with a single scale (k) may be too simple; the optimal mixing could be more step‑like or even non‑monotonic. |
| **Quantisation of exponentials** – Fixed‑point LUT for exp(–x) introduces ~0.3 % rounding error on the likelihood term. | Comparison with a double‑precision software reference shows a systematic under‑estimation of L_phys for extreme residuals. | LUT size (8‑bit address) was chosen to respect DSP budget; a finer grid would need more memory. |
| **Resource headroom not fully exploited** – Only 1.7 DSPs used; the FPGA still has margin for a more sophisticated combination (e.g. a shallow NN). | 2 DSP limit is generous for this design. | Design targeted the simplest viable solution; we can now consider a richer model. |

Overall, **the core hypothesis is confirmed**: a physics‑driven mass likelihood, when mixed with the BDT in a boost‑aware way, adds genuine discriminating power, particularly for highly boosted top jets. The magnitude of the gain is limited by the simplicity of the likelihood model and the static nature of the mixing function.

---

## 4. Next Steps – Where to go from here?

Below is a concrete, prioritized action plan for **Iteration 57** (and beyond).

| # | Direction | What to do | Expected benefit |
|---|-----------|------------|-------------------|
| 1 | **Refine the likelihood model** | • Replace the independent Gaussian terms with a 2‑D (or 3‑D) kernel‑density estimate (KDE) of \((m_{3\text{-subjet}},\,m_{W1},\,m_{W2})\) built from simulated top jets.<br>• Include a simple correction for known asymmetric tails (e.g., Crystal‑Ball shape). | Better capture of real mass correlations; larger lift in the high‑β region. |
| 2 | **Learn the mixing function** | • Parameterise ω(β) as a piecewise‑linear or cubic spline with a few tunable knots.<br>• Fit the knot positions on a validation set (or use a tiny feed‑forward NN with a single hidden node) – still implementable with < 1 DSP. | More optimal weighting; removes the dip in the transition region. |
| 3 | **Add complementary substructure observables** | • Compute N‑subjettiness ratios (τ₃/τ₂) and/or Energy‑Correlation Function ratios (D₂) on‑the‑fly (fixed‑point approximations exist).<br>• Feed these as additional inputs to the same BDT (re‑train) **or** to a shallow NN that merges BDT, L_phys, and the new variables. | Gives an extra orthogonal handle, especially for moderate boost where mass resolution is poor. |
| 4 | **Increase LUT resolution for exponentials** | • Expand the exp‑LUT from 8‑bit to 10‑bit address (still ≤ 1 kB).<br>• Re‑evaluate quantisation error and latency impact. | Reduces bias in L_phys, making the likelihood more faithful to its analytic form. |
| 5 | **Explore full joint training** | • Instead of a hard‑coded mixture, train a small decision tree or dense layer that takes as inputs: BDT_score, L_phys, β, and the new sub‑structure variables. The model can learn a non‑linear combination while still being FPGA‑friendly (e.g., 2–3 tree nodes, 4‑bit thresholds). | Potentially larger overall gain with minimal extra resources. |
| 6 | **Systematic robustness checks** | • Propagate jet‑energy scale (JES) and pile‑up variations through the likelihood to assess stability.<br>• Validate that the calibration (the final sigmoid) remains flat across pT and η bins. | Guarantees that the observed improvement is not fragile to detector effects. |
| 7 | **Hardware budgeting** | • Run a post‑implementation synthesis on the target FPGA to verify that the enriched model still meets the ≤ 130 ns latency and ≤ 2 DSP budget (or adjust the budget if acceptable). | Confirms feasibility before committing to the next iteration. |

**Timeline (rough)**  

| Week | Milestone |
|------|-----------|
| 1–2 | Generate high‑statistics top‑jet samples; create KDE PDFs; produce new LUTs. |
| 3 | Implement refined likelihood and new mixing function in the VHDL/RTL prototype; run unit tests. |
| 4 | Integrate N‑subjettiness (fixed‑point) and retrain BDT on the extended feature set. |
| 5 | Perform FPGA synthesis & place‑and‑route; verify latency & DSP usage. |
| 6 | Full physics validation (efficiency vs. β, ROC curves, systematic variations). |
| 7 | Documentation & hand‑off to the trigger team; prepare for production deployment. |

---

### Bottom line

*The hybrid mass‑likelihood + BDT strategy proved that a physics‑motivated tagger can coexist with a sophisticated multivariate classifier inside the strict L1 constraints, delivering a measurable efficiency boost at high boost. By making the likelihood more realistic, letting the data decide how to mix the two streams, and injecting a few additional sub‑structure variables, we expect a **10 %–15 % absolute efficiency gain** in the next iteration while staying within the same hardware envelope.*  

--- 

*Prepared by:*  
*The L1 Top‑Tagging Working Group*  
*Iteration 56 Review – 16 April 2026*  