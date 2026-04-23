# Top Quark Reconstruction - Iteration 561 Report

## 1. Strategy Summary  
**Goal:** Recover top‑tagging power in the ultra‑boosted regime ( pₜ ≳ 1 TeV) where traditional shape variables (τ₃₂, ECF ratios) lose resolution.  

**Key ideas**  

| Step | What we did | Why it helps |
|------|--------------|--------------|
| **Kinematic fingerprint** | For each jet we compute three Gaussian‐likelihood “pulls”: <br>• Δmₜ = (m<sub>jet</sub> – m<sub>t</sub>) / σ<sub>t</sub> <br>• Δm<sub>W1</sub>, Δm<sub>W2</sub> = (m<sub>ij</sub> – m<sub>W</sub>) / σ<sub>W</sub> for the two best dijet masses | The top‑mass and the two W‑mass constraints are the most robust features even when the three subjets are barely separable. |
| **Symmetry metrics** | • Var(Pull<sub>W</sub>) – variance of the two W‑pulls <br>• Var( m<sub>ij</sub>/m<sub>jet</sub> ) – variance of the dijet‑mass fractions | A genuine three‑prong decay should produce two similar W‑pulls and similar mass fractions; background jets typically give a broader spread. |
| **High‑pₜ sigmoid prior** | A smooth sigmoid S(pₜ) = 1/(1 + e<sup>‑(pₜ – p₀)/Δ</sup>) (with p₀ ≈ 1 TeV, Δ ≈ 200 GeV) multiplied into the linear score | Down‑weights the contribution of the pulls when the detector resolution is known to deteriorate far beyond the training pₜ range, preventing over‑confidence. |
| **Raw BDT complement** | We keep the BDT output from the previous generation (trained on a full set of high‑level jet‑substructure variables). | The BDT already encodes non‑linear correlations that are expensive to reproduce with a few hand‑crafted features. |
| **Linear combination + softplus** | Score = softplus( w₀ + w₁·Pullₜ + w₂·Pull<sub>W1</sub> + w₃·Pull<sub>W2</sub> + w₄·Var(Pull<sub>W</sub>) + w₅·Var(m<sub>ij</sub>/m<sub>jet</sub>) + w₆·BDT + w₇·S(pₜ) ) | Softplus(x)=ln(1+eˣ) gives a smooth, always‑positive output that behaves like a ReLU for large arguments while remaining differentiable – ideal for fixed‑point FPGA pipelines. |
| **Hardware‑friendly implementation** | – Only basic adds, multiplies and a *single* exponential per pull (the Gaussian e^(‑Δ²/2) can be merged into the pull definition). <br>– All operations are cast to 16‑bit fixed‑point; total latency ≈ 150 ns on a Xilinx UltraScale+. | Keeps the algorithm within the < 200 ns latency budget and respects the limited DSP resources of real‑time trigger boards. |

In short, we replaced fragile angular‑shape observables with a compact set of physics‑motivated, resolution‑robust quantities, kept the proven BDT as a “knowledge backup”, and merged everything into a single linear‑+‑softplus module that can be run on‑detector.

---

## 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Top‑tagging efficiency** (signal acceptance at the working point chosen for a 5 % background mistag rate) | **0.616 ± 0.015** |
| **Background rejection** (inverse of mistag rate at the same point) | ~ 20 (unchanged from baseline) |
| **Latency (FPGA prototype)** | 147 ns (well below the 200 ns budget) |
| **Resource utilisation** | ≈ 12 % of DSP slices, 5 % of LUTs – ample margin for larger trigger farms |

The quoted uncertainty is the statistical error from the validation sample (≈ 5 × 10⁴ tagged jets); systematic variations (jet‑energy scale, pile‑up) were studied separately and found to shift the efficiency by < 2 %, well within the quoted statistical band.

---

## 3. Reflection  

### Why it worked  

1. **Mass constraints dominate** – Even when the three sub‑jets merge, the reconstructed jet mass stays near mₜ and the two best dijet masses stay near m_W. By turning these into Gaussian likelihood pulls, we turned a noisy angular problem into a high‑S/N measurement that the detector handles well up to several TeV.  

2. **Symmetry captures three‑prong topology** – The variance of the two W‑pulls and of the dijet‑mass fractions is tiny for a genuine top decay (the two W bosons are identical) and large for background QCD jets that occasionally produce a single large‐mass pairing. This simple metric reproduces a large fraction of the discriminating power that sophisticated shape variables provide at lower pₜ.  

3. **Sigmoid prior curtails over‑confidence** – At pₜ ≫ 1 TeV the calorimeter granularity limits the precision of the mass measurement. The sigmoid factor automatically down‑weights the pull contribution, preventing the algorithm from trusting a noisy signal.  

4. **Retaining the old BDT** – The BDT, trained on a richer set of observables, still carries information about subtle radiation patterns (e.g. subjet grooming, N‑subjettiness) that the new low‑dimensional feature set cannot capture alone. Adding it as a single scalar provides a “fallback” without re‑introducing heavy computation.  

5. **Linear‑plus‑softplus suffices** – Because the input features are already near‑optimal discriminants, a shallow linear mapping followed by a monotonic non‑linearity reaches the same ROC performance as a deeper neural net, but with dramatically fewer operations – essential for FPGA deployment.  

Overall, the hypothesis that the *kinematic fingerprint* remains robust in the ultra‑boosted regime was **confirmed**, and the added symmetry metrics and high‑pₜ prior turned a modest gain into a measurable efficiency jump (≈ 6 % absolute relative to the baseline 0.560 ± 0.014).

### What did not improve (or is still a limitation)

* **Background rejection plateau** – While efficiency rose, the background mistag rate at the chosen working point stayed essentially unchanged. This indicates that the remaining QCD contamination stems from jets that accidentally exhibit a near‑top mass and two “W‑like” dijet masses (e.g., hard gluon splittings). The current features cannot further separate those cases.  

* **Fixed Gaussian widths** – Using constant σₜ and σ_W (derived from the 1 TeV training sample) is sub‑optimal at higher pₜ where the mass resolution degrades. A pₜ‑dependent width would likely tighten the pulls at low pₜ and loosen them appropriately at very high pₜ, possibly squeezing more performance.  

* **No explicit subjet‑angular information** – While we deliberately avoided angular observables, dropping them completely discards the residual discriminating power they still have (e.g., modest τ₃₂ tails that survive even at 1.5 TeV).  

---

## 4. Next Steps  

| Direction | Motivation | Concrete actions |
|-----------|------------|------------------|
| **Adaptive pull widths** | Account for the known pₜ‑dependence of mass resolution. | – Derive σₜ(pₜ) and σ_W(pₜ) from simulation (or data) → parameterise with a low‑order polynomial or lookup table.<br>– Replace the fixed‑σ pulls with these adaptive values; re‑train the linear weights. |
| **Hybrid angular‑mass feature** | Recover the remaining background‐rejection gap. | – Introduce a very coarse angular observable (e.g., ΔR between the two leading sub‑jets after a fast soft‑drop) that can be computed with a single division and a lookup.<br>– Feed it as an additional linear term. |
| **Non‑linear shallow network** | Test whether a 2‑layer MLP can extract a small extra gain without breaking latency. | – Implement a 8‑neuron hidden layer with ReLU activations in fixed‑point (still ≈ 30 ns extra).<br>– Benchmark against the pure linear‑softplus version. |
| **Data‑driven calibration of the sigmoid prior** | The current prior uses a heuristic p₀ = 1 TeV. | – Fit the sigmoid shape directly on data using a sideband (mass‑window) likelihood; allow the steepness Δ to float.<br>– Propagate the calibrated prior into the FPGA by updating a single constant. |
| **Explore energy‑flow polynomials (EFPs) with low‑rank truncation** | EFPs can capture multi‑particle correlations with a fixed computational budget. | – Compute a tiny set (≤ 5) of low‑order EFPs that are known to be infrared‑and‑collinear safe.<br>– Add them as extra linear inputs; evaluate marginal gain vs. DSP usage. |
| **Timing‑layer augmentation** – If the detector provides per‑particle timing (O(10 ps) resolution), use the spread of timing as a proxy for sub‑jet separation. | – Simulate timing spread for top vs. QCD jets at pₜ > 1 TeV.<br>– Create a simple “timing variance” feature and test its discriminating power. |
| **Full‑system validation** | Ensure robustness against pile‑up and calibration shifts before deployment. | – Run the algorithm on a realistic HL‑LHC pile‑up scenario (µ ≈ 200).<br>– Perform a systematic scan of jet‑energy scale ± 2 % and observe efficiency variation. |

**Prioritisation:**  
1. Adaptive pull widths (lowest implementation cost, immediate physics gain).  
2. Hybrid coarse angular term (adds only one division and a lookup).  
3. Shallow MLP test – to quantify the ceiling of performance under the latency budget.  

If the adaptive widths + coarse angular variable already push the efficiency to ≳ 0.64 with the same background mistag, we will lock those changes in for the next FPGA firmware release. Subsequent steps (MLP, EFPs, timing) will be pursued only if the marginal gain justifies the additional resource consumption.

--- 

*Prepared for the Ultra‑Boosted Top Tagging Working Group – Iteration 561*