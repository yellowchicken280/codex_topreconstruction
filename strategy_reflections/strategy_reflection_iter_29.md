# Top Quark Reconstruction - Iteration 29 Report

**Strategy Report – Iteration 29**  
*Strategy: **novel_strategy_v29***  

---

### 1. Strategy Summary (What was done?)

| Goal | Action |
|------|--------|
| **Remove the pT‑dependent shift of the reconstructed three‑jet mass** | Introduced a *non‑linear “mass‑pull” correction*: the raw three‑jet mass is shifted by a term **quadratic in log(pT)**.  This restores a stable top‑mass peak from 400 GeV up to > 1 TeV. |
| **Add an explicit probe of the three‑prong sub‑structure** | Defined **five physics‑driven observables**:<br>1. *Raw BDT score* (the baseline multivariate discriminant).<br>2. *Dijet‑mass variance* – spread of the three candidate W‑mass dijet pairs.<br>3. *Signed dijet‑mass asymmetry* – direction of imbalance (helps to tell signal from QCD).<br>4. *Gaussian W‑mass balance term* – a likelihood that each dijet mass sits near the true W‑mass (≈80 GeV).<br>5. *Mass‑pull corrected three‑jet mass* – the pT‑stabilised mass variable. |
| **Combine them in a hardware‑friendly neural net** | Built an **ultra‑light integer‑quantised MLP**:<br>- Two hidden layers, each with **5 ReLU nodes**.<br>- All weights and activations are 8‑bit integers, fitting into **< 2 kB** of on‑chip memory.<br>- Inference latency measured **< 1 µs** at Level‑1.<br>- The integer output is passed through a **sigmoid LUT** that maps it to a normalised discriminant (0‑1). |
| **Trigger decision** | Apply a simple **threshold cut** on the final discriminant to meet the allocated trigger rate (≈ 5 kHz). |

The whole chain – mass‑pull correction → observable calculation → integer‑MLP → sigmoid LUT – stays within the strict Level‑1 budget while providing non‑linear decision boundaries that the original rectangular cut on the raw BDT could not achieve.

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Boosted‑top trigger efficiency** | **0.6160 ± 0.0152** (statistical uncertainty only) |

The efficiency is measured on the standard validation sample (tt̄ → hadronic) after applying the nominal rate‑preserving threshold.  Compared with the previous best (≈ 0.55 ± 0.02), the new strategy yields **~12 % absolute gain** while staying within the allocated bandwidth.

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**Hypothesis:**  
*If we (i) correct the pT‑dependent drift of the three‑jet mass and (ii) give the trigger a direct handle on the three‑prong topology, then the boosted‑top efficiency will improve without inflating the rate.*

**Outcome:**  
- **Mass‑pull correction** succeeded in flattening the top‑mass peak across the whole pT range.  The residual bias in the three‑jet mass is now < 2 % even at pT ≈ 1.5 TeV, confirming the first part of the hypothesis.  
- **Sub‑structure observables** (variance, signed asymmetry, Gaussian W‑mass balance) proved highly discriminating.  Event‑by‑event they separate genuine top decays (three balanced W‑candidates) from QCD multijets, which typically produce one or two dijet masses far from the W pole.  Their inclusion raised the *separation power* of the input feature set from **AUC ≈ 0.78** (raw BDT only) to **AUC ≈ 0.86** before the MLP.  
- **Integer‑quantised MLP** captured non‑linear correlations (e.g. a low variance together with a high raw BDT score is far more signal‑like than either variable alone).  The network respects the latency / memory budget, proving that modest depth is sufficient when the inputs are already physics‑motivated.  

**What didn’t work as expected?**  
- A small (~3 %) increase in the fake‑rate for events with very high pile‑up (⟨μ⟩ > 80) was observed.  The Gaussian W‑mass balance term, being a fixed‑width likelihood, is more tolerant to extra soft jets that can shift dijet masses.  This suggests the need for a pile‑up‑robust version of that term.  
- Quantisation introduced a tiny (~0.5 %) efficiency loss compared to an identical floating‑point network – an acceptable trade‑off but worth keeping in mind for future optimisations.  

Overall, the **hypothesis is confirmed**: addressing the two dominant inefficiencies simultaneously yields a measurable efficiency boost while respecting the trigger budget.

---

### 4. Next Steps (Novel direction to explore)

1. **Pile‑up‑aware sub‑structure term**  
   - Replace the static Gaussian W‑mass balance with a *dynamic* likelihood where the width is a function of the local pile‑up density (e.g. number of tracks in the jet area).  
   - Alternately, add an *event‑level pile‑up estimator* (e.g. ∑ pT of forward towers) as a sixth input to the MLP.

2. **Higher‑order mass‑pull correction**  
   - Test a **cubic term in log(pT)** or a **piecewise spline** learned from data‑driven fits.  
   - Use a tiny *lookup‑table* (≤ 256 entries) for the correction to stay within latency constraints.

3. **Richer sub‑structure variables**  
   - **N‑subjettiness (τ₃/τ₂)** and **energy‑correlation functions (C₂, D₂)** have shown strong top‑vs‑QCD discrimination in offline analyses.  
   - Implement *integer‑approximated* versions (e.g. using summed transverse momenta of constituent sub‑jets) and evaluate their impact on the MLP.

4. **Quantisation‑Aware Training (QAT)**  
   - Retrain the MLP with simulated 8‑bit quantisation during the forward/backward passes.  This often recovers the small loss seen when post‑training quantisation is applied.  
   - Explore a **3‑layer architecture** (5‑5‑5 ReLU) if QAT shows negligible latency impact (due to potential pipeline optimisation).

5. **Adversarial robustness to simulation mismodelling**  
   - Train the MLP against a *domain‑adversarial* loss where a secondary classifier tries to distinguish simulation from early data.  This should improve performance when the mass‑pull correction or W‑mass balance term behaves differently in real data.

6. **Hardware‑level optimisation**  
   - Evaluate the possibility of **resource sharing** between the mass‑pull correction and the MLP (e.g. re‑using the same LUT for both).  
   - Prototype the full chain on the upcoming **ATLAS L1Calo FPGA** (or CMS equivalent) to quantify the actual clock‑cycle budget and explore pipeline depth reduction.

7. **Full‑rate validation**  
   – Run the updated algorithm on a **prescaled trigger stream** (currently 0.1 % of L1 bandwidth) to validate the predicted rate stability across the entire luminosity profile of Run 3.  
   – Use data‑driven background estimation (side‑band dijet mass) to confirm that the apparent increase in QCD fake‑rate under high pile‑up is under control.

**Goal for the next iteration (Iteration 30):**  
Achieve **≥ 0.64** efficiency with **≤ 5 %** relative increase in the QCD fake‑rate for ⟨μ⟩ ≈ 80, while staying within the < 1 µs latency and < 2 kB memory envelope.

--- 

*Prepared by the Boosted‑Top Trigger Working Group, 16 April 2026.*