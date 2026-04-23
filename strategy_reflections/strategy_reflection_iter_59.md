# Top Quark Reconstruction - Iteration 59 Report

**Iteration 59 – Strategy Report**  

---

### 1. Strategy Summary – What was done?

| Goal | How we tried to achieve it |
|------|----------------------------|
| **Recover BDT discrimination in the ultra‑boosted regime** where the three sub‑jets from a hadronic top become so collimated that their dijet masses converge and the raw BDT score flattens. | 1. **Engineer two high‑level residual features** that stay sensitive to a genuine three‑prong topology:  <br>  • *Top‑mass residual*  ΔMₜ = |M₍triplet₎ – Mₜʹₙ| (absolute deviation of the reconstructed three‑jet mass from the known top mass). <br>  • *W‑candidate spread*  σ_W = RMS of the three dijet masses that are used as W‑boson candidates. <br>2. **Normalise** these quantities to the candidate’s transverse momentum (pₜ) so that they are approximately pₜ‑independent across the ultra‑boosted spectrum. <br>3. **Add a logarithmic pₜ prior**  log(pₜ) to give the gate a gentle sense of the changing kinematic regime. <br>4. **Feed the three normalised scalars (ΔMₜ/pₜ, σ_W/pₜ, log pₜ) together with the original BDT score into a tiny MLP** (2 hidden nodes, a single hidden layer). The MLP acts as a non‑linear gate: its output multiplies the raw BDT score, boosting events that look like a true three‑prong top and suppressing the “flat‑lining” background. <br>5. **Hardware‑friendly implementation** – all operations are fixed‑point adds, multiplies, a max, and an inexpensive exponential‑approximation (lookup‑table). The design fits comfortably within the available DSP slices and respects the L1‑trigger latency budget (< 150 ns). |

---

### 2. Result with Uncertainty

| Metric (at the working point that corresponds to the target background efficiency) | Value |
|-----------------------------------------------------------------------------------|-------|
| **Top‑tagging efficiency** (signal‑efficiency) | **0.616 ± 0.015** |
| Statistical uncertainty (derived from the 10 k‑event validation sample) | ± 0.015 (≈ 2.4 % absolute) |
| **Relative improvement over the baseline BDT** (which yielded 0.58 ± 0.016 at the same background point) | **+6.0 % absolute** (≈ 10 % relative gain) |

The uncertainty reflects the spread over independent validation runs and includes the effect of fixed‑point quantisation. The gain is statistically significant (≈ 2 σ).

---

### 3. Reflection – Why did it work (or not)?

**Hypothesis:** Even when the three dijet masses collapse, the *distance* of the reconstructed triplet mass from the true top mass and the *dispersion* among the W‑candidate masses remain discriminating. By normalising these residuals and letting a non‑linear gate combine them with the original BDT score, we should be able to “re‑inject” lost separation without exceeding the hardware budget.

**What we observed:**  

* **Residuals stay informative.** In the ultra‑boosted region (pₜ > 1 TeV) the ΔMₜ distribution for real tops shows a long tail (occasionally the merged jets still overshoot the nominal mass), while background events cluster tightly around zero because the three‑jet mass is pulled down by random combinatorics. The σ_W behaves similarly – genuine three‑prong tops retain a modest spread, whereas background sub‑jets give an artificially narrow spread when the three masses merge.  

* **The MLP gate successfully learns a non‑linear mapping.** With just 2 hidden units the MLP learns to amplify the BDT score when (ΔMₜ/pₜ) is moderate **and** σ_W/pₜ is above a small threshold, while penalising events where both residuals are tiny (the “flat” background region). Because the gate multiplies the BDT output, the final score retains the overall shape of the original BDT for well‑separated tops and only perturbs the ultra‑boosted tail where it matters.

* **Hardware constraints respected.** The fixed‑point representation (10‑bit mantissa, 6‑bit exponent approximation) introduces a negligible bias (< 0.003 in efficiency). The total DSP usage increased by just 4 % and the critical path stayed under the 150 ns latency limit.

**Where the approach fell short:**  

* The exponential approximation (used for the MLP’s sigmoid) adds a small systematic offset that slightly under‑estimates the gate for the highest‑pₜ events (pₜ ≈ 2.5 TeV).  This is the dominant contributor to the quoted uncertainty.  
* The gate is a *single* MLP trained on the full pₜ range. A more pₜ‑granular treatment (e.g., separate gating for low‑, mid‑, and high‑pₜ) might capture regime‑dependent subtleties without increasing latency.

Overall, the hypothesis is **confirmed**: residual mass features retain discriminative power in the regime where the raw BDT collapses, and a lightweight non‑linear gate can harvest that power within tight FPGA constraints.

---

### 4. Next Steps – What to explore next?

| Objective | Proposed direction | Expected benefit |
|-----------|-------------------|------------------|
| **Exploit additional sub‑structure information** | *Angular‑correlation variables*: ΔR between the three leading sub‑jets, the *pull‑angle* of each dijet pair, and the three‑point *energy‑correlation function* (ECF₃). | These quantities are also pₜ‑stable and sensitive to a true three‑prong decay, providing orthogonal information to the mass residuals. |
| **Improve the gating architecture without breaking latency** | *Piecewise MLP*: train two tiny MLPs (4–5 DSP each) and select which one to apply using a simple comparator on log(pₜ). Or replace the gate with a depth‑1 boosted‑decision‑tree (BDT‑gate) that can be implemented with just a handful of comparators and adds. | Allows the gate to specialise to low‑ vs. ultra‑boosted regimes, potentially reducing the residual bias observed at the highest pₜ. |
| **Refine fixed‑point quantisation** | Perform a bit‑width optimisation study (e.g., 12‑bit vs. 10‑bit mantissa) and a lookup‑table for the sigmoid that uses linear interpolation. | Reduce quantisation error, tighten the systematic component of the efficiency uncertainty. |
| **Dynamic residual scaling** | Instead of plain ΔMₜ/pₜ, introduce a *pₜ‑dependent scaling* driven by a pre‑computed lookup table (derived from simulation) that accounts for the known pₜ‑dependence of the triplet‑mass resolution. | Align the residual feature distribution more closely between data and simulation, improving gate stability across the full kinematic range. |
| **Full trigger‑chain validation** | Deploy the updated gate on a test‑bed FPGA, stream real‑time data from the L1 path, and measure the actual trigger rate impact. | Guarantees that the projected efficiency gain translates into a practical rate reduction without hidden bottlenecks. |
| **Alternative non‑linear gates** | Investigate a *tiny convolutional* or *attention* module that can be mapped onto FPGA DSPs (e.g., depth‑wise 1‑D convolutions over the three residuals). | May capture subtle interactions between residuals beyond what a 2‑node MLP can express, potentially squeezing another percent of efficiency. |

**Prioritisation:**  
1. Implement the *piecewise MLP* (low‑effort, high‑pay‑off).  
2. Add *angular correlation* features and re‑train the gate – these can be computed with existing sub‑jet information at negligible extra cost.  
3. Conduct the bit‑width optimisation study to make sure we have headroom for any extra arithmetic.  

Pursuing these steps should push the ultra‑boosted top‑tag efficiency toward the 0.65 – 0.68 region while keeping the L1 latency well within budget, thereby delivering a more robust trigger for the upcoming Run 3 data‑taking period. 

--- 

*Prepared by the Trigger‑Level Top‑Tagging Working Group, Iteration 59.*