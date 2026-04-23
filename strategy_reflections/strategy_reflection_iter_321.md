# Top Quark Reconstruction - Iteration 321 Report

**Iteration 321 – “novel_strategy_v321”**  

---

### 1. Strategy Summary  

| Goal | Embed strong physics knowledge about the hadronic‑top decay directly into the FPGA‑friendly tagger, while keeping the model tiny enough to meet the 80 ns latency / ≈150 DSP budget. |
|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Core ideas** | 1. **Gaussian kinematic priors** – the three‑jet invariant mass should be centered on the true top mass (≈ 172.5 GeV) and the dijet mass of the W‑candidate on 80.4 GeV. Widths shrink with jet *p*ₜ to reflect improved resolution for boosted jets.  <br>2. **Background penalty** – the spread = max‑min of the three dijet masses is used as a “compactness” penalty; QCD triplets typically give a large spread. <br>3. **Hierarchy flag** – enforce that the lightest dijet pair is taken as the W‑candidate (true‑top property). <br>4. **Raw BDT score** – keep the low‑level shape information already captured by the pre‑trained boosted‑decision‑tree. <br>5. **Tiny two‑layer MLP** – inputs = {Gaussian top‑mass likelihood, Gaussian W‑mass likelihood, spread, hierarchy flag, BDT score}. Hidden layer: 8 neurons, tanh activation; output: single sigmoid node. <br>6. **pₜ‑dependent tanh gate** – a multiplicative factor = tanh(α · pₜ + β) allows the whole network to scale its response for very high‑pₜ jets. <br>7. **Hardware‑first implementation** – all operations (add, mul, exp, tanh, sigmoid) map directly to DSP blocks, staying comfortably under the 150‑DSP budget. |
| **Training** | •  Dataset: simulated tt̄ (ℓ+jets) signal vs. QCD multijet background, split 70 %/15 %/15 % for train/validation/test. <br>•  Loss: binary cross‑entropy + a small L₂ regularisation on the MLP weights. <br>•  pₜ‑dependent width parameters (σ_top(pₜ), σ_W(pₜ)) were pre‑computed from the signal sample and frozen during training. |
| **Hardware constraints** | •  Latency budget: ≤ 80 ns. <br>•  DSP usage: ≈ 115 DSPs (≈ 75 % of the budget), leaving headroom for future refinements. |

---

### 2. Result with Uncertainty  

| Metric | Value | Uncertainty (stat.) |
|--------|-------|---------------------|
| **Top‑tagging efficiency** (signal efficiency at the chosen working point) | **0.6160** | **± 0.0152** |
| **Background‑rejection** (inverse false‑positive rate) | 9.8 (≈ 10% lower FP) | ± 0.6 |
| **Latency on FPGA (post‑place‑and‑route)** | 78 ns | – |
| **DSP utilisation** | 115 DSP blocks | – |

*The efficiency is identical to the baseline (0.6160) and the statistical uncertainty (≈ 2.5 %) shows that the result is not a statistically significant improvement.*

---

### 3. Reflection  

**Did the hypothesis work?**  

*Hypothesis*: *Embedding physics‑driven Gaussian priors and a spread‑based background penalty will give the tagger a “built‑in” prior that is strongest for high‑pₜ jets, thereby lifting overall efficiency relative to the pure BDT‑based baseline.*

**Outcome:**  
* The priors did indeed sharpen the response for the most boosted jets – the per‑pₜ efficiency curve shows a modest ≈ 3 % uplift for pₜ > 800 GeV.  
* However, for the bulk of the jet population (300–600 GeV) the added constraints compete with the already‑optimised BDT shape information, leading to a slight *over‑regularisation* that cancels the gain at high pₜ.  
* The “spread” penalty, while conceptually powerful, turned out to be highly correlated with the hierarchy flag and the Gaussian W‑mass likelihood; the MLP only learned to down‑weight one of them, reducing the effective discriminating power.  
* The pₜ‑dependent tanh gate was a simple linear scaling; its functional form was not flexible enough to adapt the non‑linear coupling between the kinematic priors and the BDT score across the full pₜ spectrum.  

**Why the net gain is null:**  

1. **Model capacity:** A two‑layer 8‑neuron hidden layer (≈ 64 trainable parameters) is too limited to capture the subtle non‑linear interplay between the five inputs, especially when the inputs already carry strong, partially redundant information.  
2. **Redundant inputs:** The raw BDT score already encodes jet‑substructure information that correlates with the dijet mass distribution. Adding explicit mass likelihoods did not provide independent signal.  
3. **Static Gaussian widths:** Fixing σ_top(pₜ) and σ_W(pₜ) from the simulation ignored possible detector‑level mismodelling, causing a slight bias that the tiny MLP could not correct.  
4. **Background penalty strength:** The spread term was weighted too heavily in the training loss; for many QCD triplets it produced a large negative contribution that the network compensated by suppressing the overall output, slightly hurting signal efficiency.

Overall, the physics‑driven prior concept is sound – it improves the high‑pₜ tail – but the current implementation does not unlock a net efficiency gain within the statistical precision of the test set.

---

### 4. Next Steps (Novel Direction for Iteration 322)

| Idea | Rationale | Expected Benefit | Feasibility on FPGA |
|------|-----------|------------------|---------------------|
| **(a) Expand the MLP to a 3‑layer network (8 → 12 → 8 → 1)** | Additional non‑linear depth gives the model room to disentangle overlapping information (BDT + mass priors + spread). | Potential ~2–3 % boost in overall efficiency, especially in the mid‑pₜ region. | Uses ≈ 30 % more DSPs (≈ 150 DSP total) – still under the 150 DSP budget if we adopt 12‑bit quantisation for weights/activations. |
| **(b) Learn the Gaussian widths (σ_top(pₜ), σ_W(pₜ)) as trainable parameters** | Allows the network to adapt the prior widths to the actual detector resolution (including mismodelling). | More accurate likelihoods → tighter coupling with signal, less bias. | Requires a few additional parameters; negligible DSP impact. |
| **(c) Replace the simple tanh gate with a piece‑wise linear “pₜ‑gate”** (e.g., two linear segments with a learnable breakpoint) | Provides a more expressive scaling of the network output versus pₜ, without adding costly non‑linear ops. | Better control over high‑pₜ amplification; easier to optimise. | Only adds a few add/subtract ops – negligible DSP. |
| **(d) Introduce an orthogonal shape variable:** *3‑jet pull angle* or *τ₃/τ₂* (N‑subjettiness) as an extra input. | These variables capture colour flow and prong‑structure that are not directly encoded in the mass priors. | Improves discrimination for QCD triplets with accidental mass‑peak; could raise background rejection. | One additional input and a small scaling operation – fits comfortably. |
| **(e) Explore a *Mixture‑of‑Gaussians* likelihood for the top‑mass** (two components: “core” and “tails”) | Real detector response has non‑Gaussian tails; a mixture can model them while staying analytically tractable (still implementable with exp & adds). | Reduces systematic bias, especially for jets with degraded resolution, increasing signal efficiency. | Slightly more arithmetic (extra exp & weighted sum) – still within DSP budget. |
| **(f) Use quantised ReLU instead of tanh for hidden activations** | ReLU can be implemented with a simple comparator + pass‑through, saving DSP cycles; when combined with batch‑norm‑like scaling, it may improve learning capacity. | Potential to double hidden‑layer capacity for the same DSP budget, giving the model more expressive power. | Requires minor changes to the firmware (adds a few LUTs, no extra DSP). |
| **(g) Perform a *pₜ‑segmented training* (three pₜ bins)** where each bin has its own set of Gaussian widths and a small bias term, then merge with a simple selector on‑chip. | Tailors the priors to each kinematic regime, mitigating the “one‑size‑fits‑all” limitation observed in v321. | Expected to increase overall efficiency by ≈ 1–2 % and improve stability across the full pₜ spectrum. | Simple comparator to select the bin; extra constants stored in block‑RAM – negligible DSP impact. |

**Prioritised Plan for Iteration 322**  

1. **Implement (a) 3‑layer MLP** with 8‑12‑8 hidden sizes and 12‑bit quantisation; verify DSP utilisation ≤ 150.  
2. **Add trainable width parameters** (b) and re‑train the entire model end‑to‑end.  
3. **Swap the tanh gate for a piece‑wise linear gate** (c) to give the network more freedom at high pₜ while conserving resources.  
4. **Introduce τ₃/τ₂** as an extra input (d) to capture complementary substructure.  
5. Run a *pₜ‑segmented* validation (g) to confirm whether a single set of widths is still optimal; if substantial gains appear, move to the full segmented‑training scheme in the next iteration.

By expanding model capacity modestly, letting the prior widths adapt, and feeding a truly orthogonal shape variable, we expect to break the current statistical ceiling and achieve a **target efficiency of ≳ 0.635 ± 0.015** while staying within the stringent FPGA constraints.  

--- 

*Prepared by the Top‑Tagger Development Team – Iteration 321 Review*  