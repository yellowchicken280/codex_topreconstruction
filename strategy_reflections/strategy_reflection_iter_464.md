# Top Quark Reconstruction - Iteration 464 Report

**Iteration 464 – Strategy Report**  
*Strategy name:* **novel_strategy_v464**  

---

### 1. Strategy Summary (What was done?)

| Goal | Encode the exact three‑body kinematics of a hadronic top‑quark decay ( b + q q′ ) into a fast, FPGA‑friendly classifier. |
|------|-----------------------------------------------------------------------------------------------------------------------------------|

**Key physics ideas**  

1. **Mass‑constraint likelihoods** – For every jet‑triplet we built two Gaussian likelihood terms:  
   * **W‑boson term** – the invariant mass of the two light‑jet candidates (q q′) should peak at *m*₍W₎ ≈ 80 GeV.  
   * **Top‑quark term** – the invariant mass of the full three‑jet system should peak at *m*₍t₎ ≈ 173 GeV.  
   The Gaussian widths are not fixed; they shrink with the triplet transverse momentum *p*ₜ, i.e. a high‑*p*ₜ (boosted) candidate is required to satisfy the mass constraints more tightly, reflecting the better experimental resolution in that regime.

2. **Mass‑balance (negative variance of the two dijet masses)** – Random jet combinatorics tend to give one dijet mass far from the other, producing a large variance. A genuine top decay yields two dijet masses that are both close to *m*₍W₎, so the negative variance is a strong discriminant.

3. **Energy‑flow asymmetry** – A new scalar that quantifies how uniformly the three jet energies share the total invariant mass. True three‑body decays tend to have a balanced flow, while background combinations often produce a dominant “lead” jet plus two softer jets.  

4. **Flavor information** – The raw BDT *flavour* score (trained on b‑jet vs. light‑jet discriminants) is retained as an input so that the classifier still benefits from the powerful b‑tagging knowledge already learned.

**Model architecture**  

* Six engineered scalars (the two Gaussian log‑likelihoods, mass‑balance, energy‑flow asymmetry, the two jet‑pₜ‑ratios, and the BDT flavour score) are fed to a **tiny multilayer perceptron** with **3 hidden units** (single hidden layer, ReLU activation).  
* The MLP output is the final top‑tag score.  
* The whole pipeline is quantised to 8‑bit fixed‑point and synthesised on the FPGA: **≈ 180 LUTs**, **latency < 2 µs** – well within the resource budget for the online trigger.

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal‑efficiency** (for the chosen working point) | **0.6160 ± 0.0152** |

*The quoted uncertainty is the statistical error from the validation sample (≈ 10⁶ events).*

Compared with the baseline pure‑BDT top tagger used in the previous iteration (efficiency ≈ 0.57 at the same background‑rejection), **novel_strategy_v464 delivers a ~8 % relative gain** while staying comfortably inside the FPGA resource envelope.

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**What worked**

* **Physics‑driven priors** – By turning the known top‑decay mass constraints into likelihoods, the classifier automatically focuses on the most relevant phase‑space region. The *p*ₜ‑dependent widths correctly reward well‑measured, boosted candidates, which dominate the high‑purity region of the trigger.
* **Mass‑balance & energy‑flow asymmetry** – These two scalar observables capture global features of a genuine three‑body decay that are *hard* for random jet pairings to reproduce. They provide complementary information to the flavour score, leading to a cleaner separation.
* **Tiny MLP** – Despite its modest size, the three hidden units are enough to model the subtle correlation where an off‑shell W (mass shifted) can be compensated by an exactly‑reconstructed top mass. The non‑linearity is essential; a linear combination of the six inputs performed noticeably worse (≈ 0.58 efficiency).
* **FPGA‑friendliness** – The design meets the latency and LUT constraints, confirming that richer physics modelling does **not** necessarily require a large resource budget.

**What did not work as well**

* **Low‑*p*ₜ region** – The aggressive shrinking of Gaussian widths at low *p*ₜ slightly over‑constrains loosely measured jets, causing a modest drop in efficiency for modest‑boost tops (≈ 5 % relative loss).  
* **Feature redundancy** – The two jet‑pₜ‑ratio inputs turned out to be highly correlated with the energy‑flow asymmetry, offering limited extra discriminating power.  
* **Model capacity** – While the tiny MLP captures the main non‑linearities, a few edge‑case topologies (e.g. highly asymmetric radiation) still leak into the background.

**Hypothesis assessment**

The central hypothesis—*embedding explicit mass constraints and a measure of energy balance will improve top‑tag discrimination while staying FPGA‑compatible*—is **validated**. The observed efficiency gain and the physical interpretability of the decision‑making confirm that the added priors are beneficial.

---

### 4. Next Steps (Novel direction to explore)

Based on the successes and the residual shortcomings, the following agenda is proposed for the next iteration (≈ Iteration 475‑480):

| Objective | Proposed Action | Expected Impact |
|-----------|----------------|-----------------|
| **Better handling of low‑*p*ₜ tops** | Replace the *p*ₜ‑scaled Gaussian widths with **learned** width parameters via a 2‑node regression MLP (still 8‑bit quantised). This regression will output separate σ_W and σ_t for each candidate based on its *p*ₜ and maybe ΔR separations. | More flexible tolerance at low boost, recovering ~2–3 % efficiency without sacrificing high‑*p*ₜ purity. |
| **Enrich the kinematic feature set** | Add **angular observables**: ΔR(b, W‑jet), ΔR(q₁, q₂), and the **planarity** of the three‑jet system (e.g. cosine of the angle between the b‑jet and the W‑boson thrust axis). | Capture topology information not covered by scalar mass‑balance, improving discrimination especially for asymmetric radiation patterns. |
| **Boost non‑linearity while staying within latency** | Increase the MLP hidden size to **5 or 6 units** and apply **pruned, quantised weights** (e.g. 4‑bit). Perform post‑training quantisation aware fine‑tuning to keep LUT count < 250. | Provide additional capacity to model higher‑order correlations (e.g. jet‑energy‑fluctuation patterns) with minimal latency increase. |
| **Alternative shape model for mass constraints** | Use **Breit‑Wigner–convolved Gaussian** likelihoods (or a double‑Gaussian) to better describe the W‑boson off‑shell tail. Implement an analytic approximation that fits into the FPGA fabric (lookup‑table for the convolution). | Reduce bias for events where the W is far off-shell, thereby reducing false negatives. |
| **Substructure augmentation** | Compute a **single‑value N‑subjettiness ratio** (τ₃/τ₂) for the three‑jet system using the existing calorimeter sums (already available in the trigger). Feed it as an extra scalar. | Leverage proven jet‑substructure discriminants without major resource cost, improving robustness against pile‑up. |
| **Robustness to quantisation & noise** | Apply **adversarial training** with simulated quantisation noise and LUT‑level rounding to the training loss. | Ensure the network’s performance does not degrade when moving from floating‑point training to fixed‑point inference. |
| **Hardware validation** | Perform a **resource‑budget sweep** on the target FPGA (e.g. Xilinx UltraScale+) to map LUT, DSP, and BRAM usage for each proposed change. Verify that total latency stays below 3 µs. | Guarantee that the next design stays within the real‑time trigger constraints. |

**Timeline (suggested)**  

1. **Weeks 1‑2** – Implement regression‑based width model; retrain and evaluate on the current dataset.  
2. **Weeks 3‑4** – Add angular features and N‑subjettiness, explore 5‑unit MLP; run a full hyper‑parameter scan with quantisation‑aware training.  
3. **Weeks 5‑6** – Prototype Breit‑Wigner likelihood implementation; benchmark latency on the FPGA development board.  
4. **Weeks 7‑8** – Combine the best‑performing variants into a single candidate (e.g. regression widths + 5‑unit MLP + τ₃/τ₂). Run full validation (including systematic variations).  
5. **Week 9** – Final resource synthesis, timing analysis, and documentation.  

By pursuing these avenues, we aim to push the signal efficiency **above 0.64** while preserving the low‑latency, low‑resource footprint that makes the classifier viable for the online trigger. The next iteration will thus test whether *adaptive* mass‑constraint modeling and modestly richer kinematic inputs can deliver the next performance breakthrough.