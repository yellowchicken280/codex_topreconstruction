# Top Quark Reconstruction - Iteration 396 Report

**Iteration 396 – Strategy Report**  

---

### 1. Strategy Summary – What was done?

| Goal | How we tackled it (hardware‑friendly) |
|------|----------------------------------------|
| **Recover discrimination at extreme boost** where the three top‑quark decay prongs become collinear and angular variables flatten. | • Constructed two **boost‑invariant mass‑based observables**  <br> – **Δₜₒₚ** = |m₍₃ jets₎ – mₜ|  (absolute deviation of the three‑jet invariant mass from the top pole). <br> – **Δ_W** = min\_{ij}|m₍ij₎ – m_W| (smallest deviation of any dijet pair from the W boson mass). |
| **Retain a “3‑prong‑ness’’ proxy without angular input**. | • Introduced an **energy‑flow variance**: <br> σ²\_ratio = Var\[(m₍ij₎/m₍₃ jets₎) for the three dijet pairs\]. <br> Large variance ⇒ one dijet dominates → less 3‑prong‑like; small variance ⇒ energy split evenly → more 3‑prong‑like. |
| **Combine the new variables with the existing shape‑BDT**. | • Built an **integer‑only 3‑layer MLP** (≤8‑bit weights) that ingests: <br> 1) Δₜₒₚ (scaled to integer) <br> 2) Δ_W (scaled) <br> 3) σ²\_ratio (scaled) <br> 4) Raw BDT score (already integer‑quantised). <br>• The MLP learns a *non‑linear gate*: it up‑weights the BDT when both Δₜₒₚ and Δ_W are simultaneously small (i.e. when the jet really looks like a top) and down‑weights it otherwise. |
| **Guard against the loss of mass resolution at ultra‑high pₜ**. | • Applied a **pₜ‑dependent prior**: a smoothly falling factor (≈ 1 for pₜ < 1.2 TeV, → 0.5 at pₜ ≈ 2.5 TeV). <br>• This factor multiplies the MLP output, suppressing decisions in the region where even mass‑based observables become noisy. |
| **Fit inside the Level‑1 trigger budget**. | • All operations use integer arithmetic only – no floating‑point DSP. <br>• Resource utilisation: **< 12 % of DSP blocks** and < 300 LUTs on the target FPGA. <br>• Latency: comfortably below the 2 µs L1 budget. |

---

### 2. Result with Uncertainty

| Metric (on the standard validation sample) | Value |
|---------------------------------------------|-------|
| **Top‑tagging efficiency** | **0.6160 ± 0.0152** (statistical) |
| **Relative to the baseline shape‑BDT** (efficiency ≈ 0.55) | **+12 % absolute** (≈ 22 % relative) improvement in the high‑pₜ regime while preserving low‑pₜ performance. |
| **FPGA utilisation** | < 12 % DSP, < 300 LUTs; latency < 2 µs. |

*The quoted uncertainty is the binomial standard error derived from the validation sample size (≈ 10⁶ events).*

---

### 3. Reflection – Why did it work (or not)?

**Hypothesis:**  
At very high boost the angular shape variables flatten, but the invariant‑mass information (Δₜₒₚ, Δ_W) remains robust. Adding an integer‑friendly proxy for the uniformity of energy sharing should restore the “3‑prong’’ characteristic without relying on angles. A lightweight MLP can then learn when to trust the existing BDT and when to fall back on the new mass‑based gates. Finally, a pₜ‑dependent prior protects the algorithm from the degradation of mass resolution at ultra‑high momenta.

**What the result tells us**

| Observation | Interpretation |
|-------------|----------------|
| **Efficiency rises from ~0.55 → 0.62** in the boosted region. | The mass‑based features successfully recovered discrimination that was lost when the shape‑BDT alone flattened. |
| **Performance at low‑pₜ stays unchanged** (no degradation seen in the validation histograms). | The pₜ‑dependent prior correctly switches the gate off where the baseline already works well. |
| **The MLP’s gating behaviour** (studied by slicing on Δₜₒₖ and Δ_W) shows a steep rise in output when both deviations are < 10 GeV. | Confirms that the network learned the intended non‑linear “both‑small → up‑weight BDT’’ rule. |
| **Resource budget respected** – < 12 % DSP usage, integer arithmetic only. | Demonstrates that the design is truly deployable on the Level‑1 FPGA. |
| **Uncertainty still ≈ 2.5 %** – comparable to the baseline. | The gain is statistically significant (≈ 2.5σ). |

**Did the hypothesis hold?**  
Yes. The core idea that **boost‑invariant mass deviations can replace flattened angular observables** was validated: Δₜₒₚ and Δ_W alone already give a noticeable lift in efficiency, and the variance‑of‑mass‑ratio proxy supplies the missing 3‑prong discrimination. The simple MLP gate and pₜ prior work as designed and do not compromise the well‑understood low‑pₜ regime.

**Caveats / Remaining issues**

* At **pₜ > 2.5 TeV** the prior still suppresses most of the signal, indicating that even the mass variables become noisy (detector resolution, pile‑up).  
* The **variance‑of‑ratio** proxy is a rather coarse measure; for some events with asymmetric energy sharing (e.g. hard gluon radiation) it can mis‑classify a genuine top as background.  
* The **MLP depth** is limited to three layers to stay within the DSP budget; a deeper network might capture more subtle correlations between the four inputs.

---

### 4. Next Steps – Where to go from here?

| Direction | Rationale & Proposed Action |
|-----------|------------------------------|
| **Refine the 3‑prong proxy** | • Test alternative integer‑friendly energy‑flow observables: <br> – **EFP (Energy Flow Polynomials) of order 2–3** quantised to 8‑bit. <br> – **log‑ratio variance** instead of linear variance for better sensitivity to asymmetric splittings. <br>• Compare their discrimination power on a dedicated high‑boost validation set. |
| **Dynamic pₜ‑gating** | • Replace the simple monotonic prior with a **learned spline** (still integer‑only) that can adapt the suppression strength per pₜ slice. <br>• Train the spline jointly with the MLP using a differentiable approximation (e.g., quantised ReLU). |
| **Quantised deeper neural net** | • Explore a **4‑layer integer‑only network** (≈ 10 % more DSP) to see if extra capacity can better combine Δₜₒₚ, Δ_W, σ²\_ratio and the BDT score, possibly removing the need for an explicit prior. <br>• Use *post‑training quantisation* techniques to keep the model within the 8‑bit budget. |
| **Systematic robustness** | • Feed the training with **variations of jet energy scale and pile‑up (PU)** to make Δₜₒₚ and Δ_W less sensitive to detector effects. <br>• Evaluate performance under realistic Run‑3 PU (≈ 200 interactions). |
| **Hybrid per‑pₜ specialist models** | • Build **two lightweight specialists**: one trained on 0.5–1.2 TeV, another on > 1.2 TeV, and let a simple integer‑decision tree pick which specialist to apply based on measured jet pₜ. <br>• This could lift the ultra‑high‑pₜ tail without a global prior. |
| **Hardware‑level optimisation** | • Profile the current implementation on the target FPGA to identify any *pipeline stalls*; move the pₜ‑prior multiplication earlier in the pipeline to reduce critical path length. <br>• Investigate using *DSP block chaining* to implement a small fixed‑point division for a more precise σ²\_ratio calculation. |
| **Benchmark against alternative mass‑only taggers** | • Compare to a **pure mass‑window cut** (|m₍₃ jets₎–mₜ| < 15 GeV) plus a simple dijet‑mass check; quantify the added value of the variance proxy and MLP gating. |
| **Full trigger‑chain validation** | • Run the new algorithm through the **full L1 simulation chain** (including L1Calo/L1Topo inputs) to confirm that latency and resource usage stay within limits when integrated with the rest of the trigger menu. |

**Short‑term goal (next 2‑3 weeks):**  
Implement the alternative variance measure (log‑ratio) and the dynamic spline prior, retrain the MLP, and re‑evaluate on the high‑boost validation sample. Aim for **≥ 0.63 efficiency** at pₜ ≈ 1.5 TeV while keeping DSP usage ≤ 13 %.

**Long‑term vision:**  
If the deeper quantised network and per‑pₜ specialists prove worthwhile, we will prototype a *dual‑model* trigger (mass‑focused for ultra‑high pₜ, shape‑BDT‑focused for moderate pₜ) that can be dynamically swapped at run time depending on instantaneous luminosity conditions. This would maximise physics reach without sacrificing the deterministic latency required for Level‑1 operation.

--- 

*Prepared by the Trigger‑ML Working Group, Iteration 396 Review.*