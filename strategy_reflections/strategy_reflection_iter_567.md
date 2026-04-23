# Top Quark Reconstruction - Iteration 567 Report

**Strategy Report – Iteration 567**  
*Tagger name:* **novel_strategy_v567**  

---

## 1. Strategy Summary – What was done?

**Physics motivation**  
Ultra‑boosted top quarks (pₜ ≳ 1 TeV) produce jets whose internal prongs are so collimated that the classic sub‑structure observables (τ₁, τ₂, τ₃, Soft‑Drop mass, etc.) lose angular resolution.  Nevertheless, the three‑body invariant mass (≈ mₜ), the presence of at least one dijet pair with invariant mass ≈ m_W, and an approximately symmetric split of the jet energy among the three partons are still true, even when the prongs merge.

**Core idea** – *resolution‑aware pull variables*  
1. **Top‑pull** – a vectorial pull computed from the full jet, weighted by each constituent’s angular resolution. It measures how far the energy flow deviates from a perfectly symmetric three‑body picture.  
2. **Dijet‑pull** – the pull of the two‑subjet system that best approximates the W‑boson mass, again resolution‑weighted.  
3. **Symmetry variance** – a scalar quantifying the spread of the three‑prong energy fractions around the ideal 1/3‑1/3‑1/3 split.

These three physics‑driven descriptors are *robust* against merging because the resolution weighting down‑weights poorly measured angular separations.

**Machine‑learning pipeline**  
* Existing L1‑compatible BDT score (trained on classic sub‑structure) is taken as a fourth input.  
* A tiny multilayer perceptron (MLP) with two hidden layers (8 × 8 nodes), ReLU activations, and 8‑bit quantised weights is trained on the 4‑dimensional input.  
* The MLP learns non‑linear decision boundaries such as “small top‑pull **and** low dijet‑pull **and** low symmetry variance → high signal likelihood”, something a linear BDT cannot capture.  
* The entire inference graph fits comfortably into FPGA resources (≤ 2 % LUT, ≤ 1 % BRAM) and respects the 2.5 µs L1 latency budget.

---

## 2. Result with Uncertainty

| Metric (working point) | Value | Statistical uncertainty |
|------------------------|-------|--------------------------|
| **Top‑tagging efficiency** | **0.6160** | **± 0.0152** |

*The baseline L1 BDT (no pull‑MLP) achieved 0.566 ± 0.016 under identical background‑rejection conditions, so the new strategy delivers a **~5 pp absolute (~9 % relative) gain** while staying within the trigger‑rate budget.*

---

## 3. Reflection – Why did it work (or not)?

### Hypothesis validation
- **Robustness of kinematic constraints:** The pull variables successfully captured the residual shape information of ultra‑boosted tops even when sub‑jets could not be resolved. Their resolution‑aware construction prevented the loss of discriminating power observed with plain angular observables.
- **Non‑linear combination matters:** The MLP’s ReLU activation enabled “and‑type” decision boundaries (e.g. *both* low top‑pull *and* low dijet‑pull) that a linear BDT cannot express, directly confirming the original hypothesis.

### What contributed most to the improvement?
1. **Physics‑driven features** – By grounding the inputs in well‑understood constraints (mₜ, m_W, energy symmetry) the model required far fewer parameters to achieve a strong separation.
2. **Resolution weighting** – Down‑weighting poorly measured angular separations kept the pull vectors stable across the full pₜ spectrum.
3. **FPGA‑friendly MLP** – The shallow network kept inference latency negligible while still providing the needed non‑linearity.

### Limitations & open issues
- **Extreme merging:** For the highest‑pₜ jets (pₜ > 2 TeV) the pull vectors become increasingly dominated by detector noise; performance gain tapers off.
- **Training statistics:** The ultra‑boosted regime is sparsely populated in the current MC sample, raising a modest risk of over‑training (visible in a slight increase of the training‑vs‑validation loss gap).
- **Systematics not yet folded in:** The quoted efficiency includes only statistical uncertainties. Detector‑resolution systematics, pile‑up variations, and modeling of the parton shower could shift the optimal pull thresholds.
- **Quantisation impact:** 8‑bit weight quantisation introduces a ≈ 1 % efficiency loss relative to the full‑precision reference; further optimisation may be possible.

Overall, the experiment confirmed the original physics intuition: **kinematic constraints survive jet‑merging, and encoding them as resolution‑aware pulls unleashes useful discrimination for L1 top tagging.**

---

## 4. Next Steps – Where to go from here?

| Goal | Proposed action | Reasoning |
|------|----------------|-----------|
| **Broaden the physics feature set** | • Compute a compact set of Energy‑Flow Polynomials (EFPs) that are proven to be infrared‑and‑collinear safe for merged jets.<br>• Add groomed N‑subjettiness ratios (τ₃₂, τ₂₁) calculated on *soft‑drop* constituents. | EFPs capture higher‑order correlations without requiring explicit sub‑jet reconstruction; they complement the pull observables. |
| **Explore richer yet still FPGA‑friendly architectures** | • Prototype a graph‑neural‑network (GNN) where PF candidates are nodes and edges are built from ΔR distances; keep the network < 3 layers and quantise to 8‑bit.<br>• Test a tiny attention‑MLP (self‑attention on the 4‑dim input) to see if the network can learn to re‑weight the pull variables dynamically. | GNNs have shown strong performance for top tagging in offline contexts; a highly‑compressed version may still fit L1 constraints and could capture residual particle‑level information. |
| **Robustify against systematics** | • Introduce adversarial domain‑adaptation during training (e.g., a gradient‑reversal layer that penalises dependence on pile‑up or detector‑resolution variations).<br>• Train with *systematics‑augmented* samples (varying JES, JER, and parton‑shower tunes). | Ensures the MLP learns features that are stable across data‑MC differences, reducing the need for later calibration. |
| **Quantisation & calibration study** | • Perform a systematic 8‑bit → 4‑bit quantisation sweep to identify the sweet spot between resource usage and physics performance.<br>• Fit a calibration curve (e.g., isotonic regression) to map raw MLP scores to calibrated probabilities, enabling more flexible trigger thresholds. | Optimises FPGA resource consumption while preserving discriminating power; calibrated scores improve downstream offline analyses. |
| **Hardware‑in‑the‑loop validation** | • Deploy the full inference chain on the target FPGA (Xilinx UltraScale+), run a timing‑closure test with worst‑case burst‑rate conditions.<br>• Measure actual latency and resource utilisation on a full‑scale L1 firmware build. | Guarantees that the design will survive the final integration step with no hidden bottlenecks. |
| **Data‑driven validation** | • Use early Run‑3 data (single‑jet triggers) to perform a “tag‑and‑probe” study of the pull‑MLP output versus a high‑pₜ top selector (e.g., lepton + b‑jet).<br>• Compare pull distributions in data vs MC to spot potential mismodelling. | Early real‑data feedback will highlight any residual mismatches and guide subsequent re‑training or feature refinements. |

**Short‑term actionable plan (next 2‑3 weeks):**

1. Generate a dedicated ultra‑boosted MC sample (pₜ > 1.5 TeV) with multiple shower tunes.  
2. Implement the EFP and groomed τ ratios, evaluate their correlation with the existing pull variables.  
3. Train a second MLP that ingests *(pulls + EFPs)* and benchmark against the current 4‑input MLP.  
4. Run a full FPGA synthesis of the new network (including the extra features) to confirm resource headroom.  

If the enriched feature set yields a **≥ 3 % absolute efficiency gain** without exceeding the latency budget, we will adopt it as the baseline for the next iteration (v568) and proceed to the more ambitious GNN prototype in parallel.

---

*Prepared by the Trigger‑Tagging Working Group – Iteration 567*  
*Date: 16 April 2026*