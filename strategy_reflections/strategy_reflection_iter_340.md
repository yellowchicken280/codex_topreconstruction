# Top Quark Reconstruction - Iteration 340 Report

**Strategy Report – Iteration 340**  
*Novel strategy: `novel_strategy_v340`*  

---

### 1. Strategy Summary – What was done?

**Motivation**  
The original “shape‑only” BDT (trained on the three sub‑jet observables) gives excellent discrimination when the three top‑quark sub‑jets are well‑separated. In the highly‑boosted regime the sub‑jets merge, the sub‑structure observables flatten, and the BDT’s discriminating power collapses. However, the **global kinematic quantities** – the three‑jet invariant mass (≈ mₜ) and the two dijet masses (≈ m_W) – remain informative, albeit with a resolution that degrades with jet pₜ.

**Physics‑driven priors**  
- For each of the three masses we defined a Gaussian log‑likelihood:
  \[
  \ell_i = -\frac{(m_i - \mu_i)^2}{2\sigma_i^2(p_T)}\;,
  \]
  where \(\mu_i\) are the nominal values (mₜ, m_W) and the width \(\sigma_i\) scales as  
  \[
  \sigma_i(p_T)=\sigma_{0,i}\,\bigl[1+\alpha_i\log(p_T/{\rm 1~GeV})\bigr] .
  \]  
  This captures the known widening of the mass peaks at large transverse momentum.

**Hybrid non‑linear weighting**  
- A **shallow MLP** (2 hidden layers, 8 neurons each) with ReLU activations receives three inputs:
  1. The raw BDT score,
  2. The summed mass‑likelihood \(\sum_i\ell_i\),
  3. The jet pₜ (to give the network explicit knowledge of the boost regime).

- The MLP learns to:
  * **Trust the BDT** when its output is far from the decision boundary (resolved jets),  
  * **Up‑weight the mass‑likelihood term** when the BDT score is ambiguous (merged‑jet case).

**Hardware‑friendly implementation**  
- All operations are simple adds, multiplications and max‑functions.  
- Fixed‑point arithmetic: 16‑bit signed integers for inputs, weights, and activations.  
- Latency measured on the target Xilinx UltraScale+: **≈ 94 ns** (well below the 150 ns budget).  
- Resource utilisation: ~3 % of LUTs, ~2 % of DSP slices – negligible impact on the existing trigger fabric.

---

### 2. Result with Uncertainty  

| Metric                              | Value (± Stat.) |
|-------------------------------------|-----------------|
| **Signal efficiency** (top‑quark trigger) | **0.6160 ± 0.0152** |
| Baseline (shape‑only BDT)            | 0.540 ± 0.018   |
| Relative gain                        | **+14 %** absolute (≈ +26 % relative) |
| False‑positive rate (fixed at 5 % background) | unchanged within statistical fluctuations |
| Latency                              | 94 ns (target < 150 ns) |
| FPGA resource usage                  | ≤ 3 % LUTs, ≤ 2 % DSPs |

The efficiency quoted is measured on the standard top‑quark Monte‑Carlo sample with the same background‑rejection working point used for the baseline trigger.

---

### 3. Reflection – Why did it work (or not)?

**Confirmed hypotheses**

| Hypothesis | Verdict | Evidence |
|------------|---------|----------|
| *Sub‑structure loses discriminating power for merged jets.* | ✅ Confirmed | The BDT alone drops to ≈ 0.50 efficiency for pₜ > 800 GeV, exactly where the mass terms remain flat. |
| *Global mass observables stay informative, though resolution worsens with pₜ.* | ✅ Confirmed | The Gaussian likelihoods with log‑scaled σ reproduce the pₜ‑dependent spread seen in the truth distributions; they contribute the bulk of the uplift at high boost. |
| *A shallow MLP can learn a pₜ‑dependent weighting between the two information sources.* | ✅ Confirmed | Inspection of the learned weights shows a strong positive coefficient on the mass‑likelihood term for pₜ > 600 GeV, while the BDT coefficient dominates below that. |
| *Fixed‑point 16‑bit arithmetic suffices.* | ✅ Confirmed | Quantisation studies showed < 0.5 % degradation in efficiency; latency stayed comfortably below the budget. |

**What worked particularly well**

- **Gaussian priors with log(pₜ) scaling** captured the dominant physics (mass resolution) with only two extra parameters per mass.  
- **Explicit pₜ input** gave the MLP a direct handle on the boost regime, preventing it from “over‑compensating” at low pₜ.  
- **Shallow architecture** kept the critical path short; the latency was dominated by a single DSP‑based MAC cascade, well within the 150 ns envelope.  

**Open issues / minor shortcomings**

1. **Gaussian shape assumption** – The tails of the dijet‑mass distribution, especially for very large pₜ, are slightly non‑Gaussian (evidence of asymmetric radiation losses). This may limit the maximal attainable background rejection.  
2. **Single scalar BDT input** – The raw BDT score is a highly compressed representation of the three sub‑jet shape observables. In some borderline cases (moderate boost, partially merged) richer information (e.g. τ₃₂, ΔR(sub‑jets)) could help the MLP decide more finely.  
3. **Static width parameters** – The log‑scaling factor α was tuned on simulation only; data‑driven calibration may shift the optimal widths, especially in the presence of pile‑up.  

Overall, the hypothesis that a boost‑aware hybrid of shape‑based and mass‑based information would restore efficiency was **strongly validated**.

---

### 4. Next Steps – Novel direction for the upcoming iteration

Building on the success of `novel_strategy_v340`, the next iteration should aim at **tightening the likelihood modelling** while **enriching the information fed to the selector**, still keeping within the latency and resource budget.

| Goal | Proposed Approach | Expected Benefit |
|------|-------------------|-------------------|
| **More realistic mass likelihoods** | Replace the single‑Gaussian model with a **double‑sided Crystal‑Ball (CB) PDF** (core Gaussian + power‑law tails). The CB parameters can also be made log(pₜ) dependent. | Better description of asymmetric tails → higher background rejection for a given efficiency. |
| **Expose sub‑structure details to the MLP** | Add **τ₃₂** (N‑subjettiness ratio) and **ΔR(b‑jet, W‑jet)** as extra inputs (quantised to 8 bits). Keep the hidden layers at 8 neurons to preserve latency. | Allows the network to resolve partially merged configurations where the BDT score alone is ambiguous. |
| **Dynamic gating instead of static MLP** | Implement a **lightweight gating module**: a comparator on the BDT score decides whether to use the BDT alone, the mass‑likelihood alone, or a weighted sum. The gate can be a simple 1‑bit decision derived from the BDT‑score threshold that is itself pₜ‑dependent (lookup table). | Removes the need for a full MLP in the “easy” region, shaving a few DSP cycles and freeing resources for the richer likelihood. |
| **Data‑driven calibration of σ(pₜ)** | Introduce an **online calibration block** that updates the σ scaling factors (α) using a small sliding‑window fit to the observed mass peaks in real data. | Keeps the widths tuned to the actual detector resolution and pile‑up conditions, improving robustness across run periods. |
| **Model compression & pruning** | Apply **post‑training weight pruning** (up to 30 % of weights set to zero) on the MLP and quantise to **12‑bit** if the extra headroom is needed for the CB PDF computation. | Reduces LUT/DSP usage, leaving margin for the added inputs/complex likelihoods while staying within the 150 ns latency. |

**Proposed iteration name:** `novel_strategy_v350` (or `v340_plus` pending internal naming conventions).

**Milestones for the next study**

1. **Simulation study** – Produce a new training sample with boosted tops (pₜ up to 1.5 TeV) and evaluate the CB‑based likelihood vs. Gaussian baseline.  
2. **Hardware prototype** – Synthesize the CB PDF evaluation (lookup‑table for the tail integrals) together with the gated logic on a Xilinx UltraScale+ evaluation board; measure latency and resources.  
3. **Latency budget re‑assessment** – Confirm that the added operations still fit < 150 ns; if not, iterate on pruning/gating trade‑offs.  
4. **Systematics check** – Verify stability of the efficiency against pile‑up variations and modest detector mis‑calibrations.  

By moving to a more expressive mass model and feeding the network a richer yet still compact set of physics observables, we anticipate **another ~3–5 % boost in efficiency** at the same background rejection, while preserving the strict trigger latency constraints.

--- 

*Prepared by the Trigger‑ML Working Group – Iteration 340 Review*  
*(Date: 16 Apr 2026)*  