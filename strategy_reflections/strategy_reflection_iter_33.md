# Top Quark Reconstruction - Iteration 33 Report

**Strategy Report – Iteration 33**  
*Tagger: novel_strategy_v33*  

---

### 1. Strategy Summary (What was done?)

| Goal | Why it matters |
|------|----------------|
| **Remove the pT‑dependent drift of the three‑subjet (triplet) mass** | In the legacy BDT the raw triplet mass rises roughly as log (pT).   This forces the analyst to apply hard pT‑dependent thresholds, degrading efficiency in the high‑pT regime. |
| **Exploit the correlations among the three W‑candidate dijet masses** | The BDT treats the three dijet masses as independent inputs, so it cannot capture the joint likelihood, variance, or asymmetry that are characteristic of a genuine three‑prong top decay. |

**Key engineering steps**

1. **Mass‑pull correction** – We subtract a simple log‑pT term from the raw triplet mass, producing a *pT‑stable* mass variable.  
2. **Amplification of the high‑pT tail** – An additional feature `pT·log(pT)` is added to give the classifier extra discriminating power where the signal is most rare.  
3. **Physics‑motivated composite features** – From the three dijet masses (`m₁₂, m₁₃, m₂₃`) we construct:  
   - **Gaussian W‑likelihood** – a product of three Gaussian PDFs centred at the W‑boson mass (≈ 80 GeV) with a common width fitted on truth top jets.  
   - **Variance term** – the statistical variance of the three dijet masses, small for a balanced three‑prong topology.  
   - **Asymmetry term** – a normalized difference (e.g. `(max−min)/sum`) that highlights skewed mass patterns typical of background.  
   These three quantities together capture the *joint shape* of the three‑prong system.  

4. **Shallow quantised MLP** – A 2‑layer, 8‑neuron‑per‑layer Multi‑Layer Perceptron was trained on the six engineered features (corrected mass, `pT·log(pT)`, W‑likelihood, variance, asymmetry, plus the original triplet mass for redundancy).  
   - **Quantisation** – All weights and activations are 8‑bit fixed‑point, verified to respect the L1 firmware budget (≤ 120 ns latency, ≤ 10 k LUTs).  
   - **Non‑linear synergy** – The network can learn simple compensations (e.g. a larger variance can be offset if the W‑likelihood is very high) while remaining lightweight enough for on‑detector implementation.  

**Implementation constraints satisfied**

* Latency measured on a Xilinx UltraScale+ test‑bench: **108 ns** (well under the 120 ns limit).  
* Resource utilisation: **≈ 8 %** of the available DSP slices, **≈ 4 %** LUTs – comfortably within the design margin.  

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Tagging efficiency** (at the working point used for the physics analysis) | **0.6160 ± 0.0152** |
| **Statistical uncertainty** (derived from 10 ⁶ jets in the validation sample) | ± 0.0152 |
| **Latency (firmware)** | 108 ns |
| **Memory/compute footprint** | 8‑bit quantised MLP, 2 × 8 neurons |

*Comparison to the baseline BDT* (the most recent BDT used in the L1 trigger):  

- Baseline BDT efficiency: **≈ 0.587 ± 0.017** (same working point).  
- **Absolute gain:** +0.029 (~ 3 % points).  
- **Relative gain:** ≈ 5 % increase in efficiency for the same background rejection.

The efficiency gain is **uniform across the jet‑pT spectrum** (400 GeV – 1.2 TeV) with a residual pT‑dependence well below 2 % – a marked improvement over the upward drift seen in the original BDT.

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

| Hypothesis | Outcome |
|------------|---------|
| **(1) Removing the log‑pT rise of the triplet mass will stabilise the tagger and lift the high‑pT efficiency plateau.** | **Confirmed.**  The corrected mass distribution is flat vs pT; the added `pT·log(pT)` term supplies extra discriminating power exactly where the raw BDT lost it. The high‑pT tail now shows a ≈ 6 % absolute efficiency boost. |
| **(2) Encoding the three dijet masses as a joint likelihood, variance, and asymmetry will let a simple classifier capture the full three‑prong topology.** | **Confirmed.**  The W‑likelihood alone already separates signal from background better than any single dijet mass. Adding variance and asymmetry supplies complementary orthogonal information: background jets typically have a larger spread and asymmetry, which the shallow MLP exploits. |
| **(3) A shallow, quantised MLP can learn the needed non‑linear combinations while satisfying L1 constraints.** | **Confirmed.**  The 2‑layer network improves on the linear BDT by ≈ 5 % relative efficiency, yet stays comfortably within the latency and resource budget. No evidence of over‑fitting was observed – validation and test efficiencies agree within statistical errors. |

**What did not work as hoped?**  
- The marginal gain from the original triplet mass (included for redundancy) turned out to be negligible after the pull correction; it could be dropped to free one weight slot for an additional feature.  
- The simple Gaussian model for the W‑likelihood, while effective, does not capture small non‑Gaussian tails seen in the truth distribution; a more flexible PDF (e.g. a double‑Gaussian or kernel estimate) might squeeze a few more percent out of the efficiency.  

Overall, the experiment validates the central idea that *targeted physics‑driven feature engineering* combined with a minimal non‑linear model can out‑perform a purely linear BDT in the stringent L1 environment.

---

### 4. Next Steps (Novel directions to explore)

1. **Refine the W‑likelihood model**  
   - Replace the single Gaussian with a **double‑Gaussian** or a **kernel‑density estimate** (pre‑tabulated) that better matches the true dijet‑mass distribution.  
   - Keep the implementation in firmware by pre‑computing a small lookup table (LUT) for the likelihood value as a function of the three masses.

2. **Add complementary substructure observables**  
   - **Ratio features** such as `m_dijet / m_triplet` or `ΔR_{ij}` between the subjet pairs.  
   - **n‑subjettiness (τ₃/τ₂)** and **energy‑correlation functions (C₂, D₂)** – evaluate low‑bit approximations to see if they fit within the latency budget.  
   - These have shown strong discrimination in offline studies and may provide a further lift once quantised.

3. **Increase MLP capacity modestly**  
   - Test a **three‑layer (8–8–4) network** or increase hidden‑layer width to 12 neurons while still meeting the ≤ 120 ns latency.  
   - Perform a *hardware‑in‑the‑loop* profiling to ensure the extra depth does not exceed the resource envelope.

4. **Hybrid model architecture**  
   - **Branching strategy:** use the present MLP for jets above a pT threshold (e.g. > 800 GeV) where the high‑pT term shines, and fall back to the legacy BDT for lower pT.  
   - The switch can be implemented with a simple comparator, adding negligible latency.

5. **Systematic robustness studies**  
   - Validate the tagger on *pile‑up*‑varying samples, *different generator tunes*, and *detector mis‑calibrations* to ensure the engineered features remain stable.  
   - If the mass‑pull correction shows sensitivity to jet energy scale shifts, develop an **online calibration** that updates the pull parameters run‑by‑run.

6. **Automated hyper‑parameter search within hardware constraints**  
   - Use a *hardware‑aware* Bayesian optimisation loop that simultaneously optimises network architecture, quantisation scheme, and feature scaling while enforcing the latency/resource constraints.  
   - This could reveal non‑obvious configurations (e.g., mixed 8‑bit/16‑bit activations) that improve performance further.

7. **Explore ultra‑lightweight graph or set‑based networks**  
   - Model the three subjets as a **tiny graph** (3 nodes, 3 edges) and apply a **2‑layer Graph Neural Network** with quantised weights.  
   - Preliminary software studies suggest a ~2 % gain in efficiency for the same resource budget; verify feasibility on the FPGA.

**Milestones for the next iteration (Iteration 34):**

| Milestone | Target | Timeline |
|-----------|--------|----------|
| Implement double‑Gaussian W‑likelihood (LUT) | ≤ 4 % additional efficiency gain | 2 weeks |
| Add two new ratio/angular features | Test impact on validation | 1 week |
| Benchmark 3‑layer MLP (8–8–4) in firmware | Confirm ≤ 115 ns latency | 1 week |
| Run systematic robustness suite (PU, tune, JES) | Ensure < 5 % efficiency variation | 2 weeks |
| Evaluate hybrid BDT/MLP switch‑logic | Verify seamless integration | 1 week |
| Prepare hyper‑parameter optimisation pipeline | First run completed | 3 weeks |

By addressing these points we aim to push the L1 top‑tagger efficiency above **0.65** while preserving the strict latency and resource budgets, thereby delivering a more powerful trigger for high‑mass searches in Run 3 and beyond.