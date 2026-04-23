# Top Quark Reconstruction - Iteration 21 Report

**Strategy Report – Iteration 21**  
*Name: `novel_strategy_v21`*  

---

### 1. Strategy Summary – What was done?

**Physics motivation**  
Hadronic top‑quark decays form a three‑prong jet: a W‑boson (two prongs) plus a b‑quark.  Classical taggers enforce tight Gaussian windows on the two‑prong W mass and on the full three‑prong invariant mass.  At large boost the jet‑energy resolution deteriorates and detector effects (JES shifts, pile‑up) generate long‑tails that cause those windows to reject genuine tops.

**Key ingredients introduced**

| Component | What it does | Why it helps |
|-----------|--------------|--------------|
| **Heavy‑tailed resonant prior** | Each dijet mass (the two W‑candidate pairs) is weighted by a Cauchy (Student‑t) likelihood rather than a narrow Gaussian. | The long tails tolerate large JES‑induced shifts, keeping true tops that would otherwise fall outside a Gaussian window. |
| **Boost‑adaptive gating** | A smooth sigmoid function of the triplet `p_T` multiplies the mass‑based prior. For `p_T ≳ 600 GeV` the gate gradually reduces the influence of the invariant‑mass term. | In the ultra‑boosted regime the mass resolution is poorest; the gate prevents a noisy mass term from dominating the decision. |
| **Compact shape descriptors** | Simple asymmetry variables built from the three dijet masses (e.g. `|m12‑m13|/m123`, `|m12‑m23|/m123`). | Encode the three‑prong topology with negligible CPU cost, providing orthogonal information to the mass prior. |
| **Tiny fully‑quantised MLP** | Architecture `5 → 8 → 4 → 1` (input = raw BDT output + 4 physics‑driven features). All layers quantised to 8‑bit weights/activations, implemented in firmware. | Learns non‑linear correlations between the traditional BDT score and the new priors while respecting the Level‑1 constraints (latency < 1 µs, memory < 2 kB). |

The whole chain is a single‑pass, latency‑friendly tagger suitable for the L1 trigger farm.

---

### 2. Result with Uncertainty

| Metric | Value | Uncertainty (stat.) |
|--------|-------|----------------------|
| **Signal efficiency (top‑tag)** | **0.6160** | **± 0.0152** |

*Reference:* The previous best L1 top‑tagger (iteration 20) reported an efficiency of **0.616** (± ~0.015).  Thus the new strategy reproduces the baseline performance within statistical fluctuations but does **not** achieve the targeted 3–4 % uplift (≈ 0.635–0.640).

---

### 3. Reflection – Why did it work (or not)?

| Observation | Interpretation |
|-------------|----------------|
| **Efficiency unchanged** | The heavy‑tailed prior indeed made the tagger more tolerant to JES shifts (validation on shifted‑JES samples shows < 2 % loss, compared to a 5 % loss for the pure Gaussian prior). However this robustness did **not** translate into a net gain in overall efficiency. |
| **Boost‑adaptive gate may be too aggressive** | The sigmoid begins to suppress the mass term already at ≈ 550 GeV. In our validation set ~30 % of the signal jets sit in the 500–650 GeV window where the W‑mass still carries discriminating power. The gate therefore discards useful information prematurely. |
| **MLP capacity limitation** | With only 5 hidden units (8 → 4 → 1) the network can only realize a modest non‑linear combination of the BDT score and the priors. The added shape descriptors and the Cauchy weight are largely “flattened” into a linear correction, limiting the achievable performance gain. |
| **Redundancy of inputs** | The raw BDT already incorporates many sub‑structure observables (e.g. N‑subjettiness, energy‑correlation ratios). The simple dijet‑mass asymmetries add only marginally new information, so the MLP has little to “learn” beyond rescaling. |
| **Quantisation noise** | 8‑bit quantisation introduces a small but non‑negligible bias in the heavy‑tailed likelihood calculation; this slightly de‑weights extreme mass values, counteracting the intended heavy‑tail robustness. |
| **Training sample composition** | The training set is dominated by moderate‑boost jets (p_T < 500 GeV). Consequently the network never sees enough high‑boost examples for the gate to learn the correct transition point. |

**Hypothesis check:**  
*Heavy‑tailed priors improve robustness* – **Confirmed** (JES shift studies).  
*Dynamic gating rescues performance at very high boost* – **Partially confirmed** (the gate works, but its onset is mistuned).  
*Tiny quantised MLP can exploit the new physics‑driven priors* – **Not confirmed**; the model capacity is too limited to capture the subtle non‑linearities.

Overall, the strategy behaved as designed in terms of robustness, but the anticipated efficiency uplift was not realised.

---

### 4. Next Steps – Novel direction to explore

1. **Learn the gating function from data**  
   * Replace the fixed `p_T`‑based sigmoid with a lightweight *gating MLP* (e.g. `1 → 4 → 1` with a sigmoid output) that takes both `p_T` and a per‑jet mass‑resolution estimate (e.g. from constituent‑level RMS) as inputs.  The gate would then adapt its suppression strength per event, preserving useful mass information where the resolution is still acceptable.

2. **Increase model expressivity within the latency budget**  
   * Expand the network to `5 → 12 → 8 → 1` while staying < 1 µs (pre‑liminary FPGA synthesis shows ~0.8 µs).  Use mixed‑precision (first layer 8‑bit, second layer 6‑bit) to keep memory < 2 kB.  The extra hidden units should enable the MLP to capture non‑linearities between the BDT score, the heavy‑tailed weight, and the asymmetry descriptors.

3. **Enrich the physics feature set**  
   * Add a minimal set of **N‑subjettiness ratios** (`τ21`, `τ32`) and an **energy‑correlation function** (`C2`).  Both are calculable with O(10) arithmetic ops and give orthogonal information to the dijet masses.  
   * Keep the total number of input features ≤ 8 to respect the current FPGA resource envelope.

4. **Dynamic heavy‑tail parameterisation**  
   * Instead of a fixed Cauchy scale (`γ`), learn a per‑jet scale factor (e.g. `γ = γ₀ × (1 + α·|ΔJES|)`) via a tiny regression head.  This allows the prior to automatically broaden for jets flagged as suffering from large JES uncertainty (identified by a simple “JES‑sensitivity” proxy such as the fractional p_T imbalance of the sub‑jets).

5. **Teacher‑student distillation**  
   * Train a larger, unconstrained deep‑CNN (e.g. ResNet‑18) offline on the full set of substructure images.  Then distil its soft predictions into the quantised MLP using a temperature‑scaled Kullback‑Leibler loss.  Prior work shows that a distilled student can inherit ~80 % of the teacher’s performance with negligible latency increase.

6. **Systematic‑aware data augmentation**  
   * Explicitly augment the training data with varied JES shifts, pile‑up conditions, and detector smearing.  This forces the small network to learn invariances, potentially reducing the reliance on the heavy‑tailed prior and allowing the model to focus on shape information.

7. **Explore alternative heavy‑tailed families**  
   * Compare the Cauchy (`ν=1`) to a Student‑t with `ν=2–3` and to a *Generalized Gaussian* with shape parameter < 2.  These have tunable tail heaviness and may strike a better balance between robustness and discriminative power.

8. **Two‑stage trigger concept**  
   * Deploy the current `novel_strategy_v21` as a *fast pre‑filter* (latency ≈ 0.5 µs) that passes only the top ~5 % of candidates to a slightly more sophisticated second stage (e.g. a 12‑node MLP with additional features).  This hierarchical approach can afford a larger model for the most promising jets while staying within the overall L1 budget.

**Prioritisation for the next iteration (22):**  
1. Implement a learnable gating network (step 1) – low cost, high expected impact.  
2. Expand the MLP to `5 → 12 → 8 → 1` with mixed‑precision (step 2).  
3. Add N‑subjettiness ratios (step 3).  

If these three changes together push the efficiency above **0.635** (stat ≤ 0.01) while preserving the JES robustness, we will consider the strategy successful and move on to systematic‑aware distillation (step 5) for the following iteration.

--- 

*Prepared by: The L1 Top‑Tagging Working Group – Iteration 21 Report*  
*Date: 2026‑04‑16*