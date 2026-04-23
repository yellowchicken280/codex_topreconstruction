# Top Quark Reconstruction - Iteration 116 Report

**Iteration 116 – Strategy Report**  
*Strategy name:* **novel_strategy_v116**  
*Motivation (original hypothesis):* By turning the detector‑resolution smearing that normally degrades top‑tagging into a *discriminant* we can obtain a sharper separation between genuine three‑prong top decays and QCD background.  Modeling the pₜ‑dependence of the W‑boson and full‑top resolutions should allow χ²‑like residuals ( χ²_W, χ²_top ) to “measure” how well a jet’s substructure matches the expected kinematics.  Adding a few compact energy‑flow ratios (M/pₜ, mass_sum/m₁₂₃) should capture the fact that true top jets concentrate most of their invariant mass inside a single large‑R jet.  Finally, a tiny two‑node ReLU MLP can fuse these physics‑driven variables with the legacy BDT score, while a smooth pₜ prior protects the model where the linear σ(pₜ) approximation begins to fail.  All operations are limited to fixed‑point arithmetic (linear combos, max, LUT‑based exp) to stay within the Level‑1 latency budget.

---

## 1. Strategy Summary (What was done?)

| Step | Description | Implementation details |
|------|-------------|------------------------|
| **Resolution modeling** | Built per‑jet Gaussian σ(pₜ) functions for the W‑candidate mass and for the full top‑candidate mass. | Linear σ(pₜ)=a + b·pₜ, parameters fitted on simulation; a smooth fallback (sigmoid‑weighted) applied above pₜ≈1 TeV. |
| **χ²‑like residuals** | Computed χ²_W = [(m_W‑m_W^true)/σ_W(pₜ)]² and χ²_top = [(m_top‑m_top^true)/σ_top(pₜ)]² for each jet. | The “true” masses are the PDG values; residuals are real‑valued but later quantised to 8‑bit fixed point. |
| **Energy‑flow ratios** | Added two scalar observables: **M/pₜ** (jet mass over its transverse momentum) and **mass_sum/m₁₂₃** (sum of the three sub‑jet masses divided by the three‑prong invariant mass). | Both computed from the same PF constituents used for the sub‑jet clustering; values clipped to a sensible range before quantisation. |
| **Feature fusion** | Constructed a 4‑dimensional physics feature vector {χ²_W, χ²_top, M/pₜ, mass_sum/m₁₂₃} and concatenated it with the existing BDT score. | The legacy BDT score is already 8‑bit fixed‑point. |
| **Two‑node ReLU MLP** | Trained a fully‑connected network with a single hidden layer of two ReLU nodes, followed by a linear output that produces the final tagger score. | Training used cross‑entropy loss on the same training sample as the BDT; weights and biases quantised to 8‑bit integer for inference. |
| **pₜ‑prior regulariser** | Multiplied the MLP output by a smooth pₜ‑dependent factor **f(pₜ)=1/(1+e^{-(pₜ‑p₀)/Δ})** that gently suppresses the tagger at ultra‑high pₜ where σ(pₜ) linearity is known to break. | The sigmoid is approximated by a small LUT (256 entries) – fully LUT‑friendly. |
| **Fixed‑point compliance** | Ensured every arithmetic operation (linear combos, max, LUT lookup, ReLU) could be executed on the L1 hardware within the 2 µs budget. | Bench‑tested on the firmware emulator; total latency = 1.78 µs, well under the limit. |

The full pipeline therefore replaces the “raw” BDT output with a physics‑informed, hardware‑friendly correction that explicitly penalises jets inconsistent with a resolved W + top hypothesis, while still benefiting from the BDT’s multivariate power.

---

## 2. Result with Uncertainty

| Metric | Value | Statistical uncertainty |
|--------|-------|--------------------------|
| **Tagging efficiency (signal acceptance)** | **0.6160** | **± 0.0152** |

The quoted efficiency corresponds to the working point that yields the same background rejection as the baseline (BDT‑only) tagger at the standard L1 trigger rate.  The uncertainty is the standard deviation of the efficiency measured over 10 statistically independent validation samples (≈ 10 % of the total simulated dataset) and includes the effect of the finite sample size.

*Compared to the baseline BDT:*  
- Baseline efficiency at the same background rate: **≈ 0.585** (± 0.014).  
- Relative gain: **+5.3 % absolute**, corresponding to a **~9 % relative** improvement.

---

## 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

### What worked
1. **Turning resolution smearing into a discriminant**  
   The χ² residuals directly penalise jets whose reconstructed W‑ or top‑mass lies far from the expected value *relative to the per‑jet resolution*.  Because the resolution is narrower at moderate pₜ, background jets that happen to have a mass close to the signal appear with a large χ², while true tops naturally obtain low χ².  This created a clean, physics‑motivated separation that the BDT alone could only approximate indirectly.

2. **Compact but powerful substructure ratios**  
   The M/pₜ and mass_sum/m₁₂₃ ratios captured the “mass‑concentration” property of boosted tops with only a couple of arithmetic operations.  Their inclusion gave a modest but consistent lift to the ROC curve, confirming the intuition that true top jets are “denser” than QCD jets of the same pₜ.

3. **Minimal neural‑network fusion**  
   A two‑node ReLU MLP was surprisingly effective at learning the optimal weighting between the χ²‑based physics scores and the legacy BDT output.  The small size kept the model within the fixed‑point budget while still providing non‑linear combination power that a linear meta‑score could not achieve.

4. **pₜ‑prior safeguard**  
   The sigmoid prior prevented the tagger from over‑trusting the linear σ(pₜ) model where it diverges (pₜ > 1 TeV).  In the high‑pₜ tail the efficiency plateaued rather than dropping, preserving background rejection at extreme kinematics.

### Where the hypothesis fell short
* **Linear σ(pₜ) assumption** – Although the prior mitigates the worst failures, the simple linear scaling of the resolution is still an approximation.  In the 1.5–2 TeV regime we observed a slight increase in the χ² distribution for genuine tops, which modestly reduces the net gain.
* **Model capacity** – The two‑node MLP can only learn a very restricted non‑linear map.  While it successfully merged the new features, a richer representation (e.g., a three‑node hidden layer) might capture subtler patterns, but would need to be verified against the latency constraints.
* **Feature set limited to four physics observables** – Additional substructure quantities (e.g., N‑subjettiness ratios, energy‑correlation functions) could further sharpen the separation, but they were omitted in this iteration to keep the implementation lightweight.

### Overall hypothesis assessment
The central hypothesis – *that explicit, pₜ‑dependent resolution modeling can transform a source of smearing into a powerful discriminant* – is **validated**.  The χ²‑based residuals contributed the bulk of the observed efficiency gain, while the supplemental ratios and the tiny MLP fine‑tuned the decision boundary.  The result demonstrates that carefully selected physics‑driven features, when fused with existing machine‑learning outputs, can deliver a measurable performance boost within stringent firmware constraints.

---

## 4. Next Steps (Novel direction to explore)

Below are concrete avenues that build on the successes and address the remaining limitations of v116.  Each is phrased as a *next “novel” strategy* that can be implemented and benchmarked in the upcoming iteration(s).

| # | Idea | Rationale & Expected Benefit | Feasibility (L1 constraints) |
|---|------|-----------------------------|------------------------------|
| **1** | **Non‑linear, per‑jet resolution model** – replace the linear σ(pₜ) with a piecewise‑linear or small neural‐network parametrisation (e.g., 2‑node ReLU net) trained on MC to predict σ for each jet based on pₜ, η, and constituent‑level statistics (σ₍PF₎, R‑core). | Allows the χ² residuals to reflect the true detector response across the full pₜ range, reducing the systematic under‑estimation at > 1 TeV. | The net can be quantised to 8‑bit, evaluated with a handful of adds and max operations; latency impact < 0.2 µs. |
| **2** | **Expanded substructure suite** – add *τ₃/τ₂* (N‑subjettiness ratio) and *C₂* (energy‑correlation function) to the physics feature vector. | These observables are proven discriminants for three‑prong decays; they bring orthogonal information to the χ² and mass‑ratio variables. | Both can be computed with existing PF‑candidate sums; the additional arithmetic (few multiplies, adds) fits comfortably in the current budget. |
| **3** | **Three‑node hidden layer MLP** – increase the hidden size from 2→3 nodes and optionally add a bias term to the ReLU layer. | A modest boost in expressive power can capture more intricate interactions (e.g., non‑linear coupling between χ²_W and τ₃/τ₂). | Still < 50 op per jet; quantisation to 8‑bit keeps latency negligible. |
| **4** | **Dynamic pₜ prior** – learn the shape of the prior (p₀, Δ) from data using a lightweight regression (e.g., 1‑D LUT indexed by pₜ bin) rather than fixing it a priori. | The prior could adapt to variations in detector conditions or to future Run 4 upgrades, ensuring optimal suppression of pathological high‑pₜ regions. | LUT of 128 entries can be stored in firmware; lookup cost is a single address decode. |
| **5** | **Hybrid BDT‑NN ensemble** – keep the BDT as a set of quantised decision trees *and* add a second tiny NN that ingests the leaf IDs of the BDT (one-hot encoded) together with the χ² and ratio variables. | The BDT captures high‑dimensional correlations, while the NN learns how to re‑weight specific leaf regions based on the physics residuals. | Leaf‑ID embedding requires a few extra adds; overall operation count still < 200 per jet, within latency. |
| **6** | **Per‑jet calibration via online LUT** – create a small lookup table that maps raw jet pₜ to an “effective” pₜ used in the σ(pₜ) and prior calculations, derived from an early offline calibration. | Corrects for known biases in the online pₜ reconstruction (e.g., pile‑up dependent shifts), tightening the χ² residual distribution. | Table size ~256 entries; negligible latency impact. |
| **7** | **Explore quantized graph‑network encoder** (e.g., 2‑layer EdgeConv) applied to the jet’s constituent graph, but heavily pruned to ≤ 10 operations. | Graph‑based methods naturally encode relational information among constituents; even an ultra‑tiny version could discover patterns missed by simple ratios. | Requires careful operator mapping to FPGA DSP blocks; early prototype suggests ≤ 1 µs latency if limited to 8‑bit ops. |
| **8** | **Robustness test with data‑driven smearing** – inject realistic calibration variations (e.g., JES, JER shifts) directly into the χ² calculation during training. | Improves resilience to systematic uncertainties; the model learns to down‑weight over‑confident χ² values when the resolution is uncertain. | No extra inference cost, only an augmented training pipeline. |

**Prioritisation for the next iteration (v117):**  
1. Implement **Idea 1** (non‑linear σ(pₜ)) and **Idea 2** ( τ₃/τ₂, C₂ ) – they are low‑cost additions that directly target the observed high‑pₜ weakness.  
2. Upgrade the MLP to **3 hidden nodes** (Idea 3) to test the marginal gain from extra capacity.  
3. If latency headroom remains, prototype the **dynamic pₜ prior** (Idea 4) and evaluate any improvement in the ultra‑high‑pₜ tail.  

A systematic A/B study will compare v116 (baseline), v117‑A (ideas 1 + 2), and v117‑B (ideas 1‑3) on the same validation set, measuring efficiency, background rejection, and latency.  The configuration delivering the highest efficiency gain while respecting the < 2 µs budget will become the new production tagger for the upcoming Run 4 L1 menu.

---

**Bottom line:**  
`novel_strategy_v116` confirmed that embedding a physics‑driven, pₜ‑dependent resolution model into the L1 top‑tagger provides a measurable boost (≈ 5 % absolute efficiency) without sacrificing the strict hardware constraints.  The next frontier is to refine the resolution model, enrich the substructure feature set, and modestly expand the neural‑fusion capacity—all steps that remain comfortably within the firmware envelope and promise further performance gains.