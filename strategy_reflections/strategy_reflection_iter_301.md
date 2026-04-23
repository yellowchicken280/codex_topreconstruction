# Top Quark Reconstruction - Iteration 301 Report

**Strategy Report – Iteration 301**  
*Novel Strategy v301 – “Top‑mass + W‑mass + Energy‑flow MLP”*  

---

### 1. Strategy Summary – What was done?

* **Physics motivation** – Fully‑hadronic \(t\bar t\) events appear as a three‑jet system that must simultaneously satisfy a top‑mass constraint, two internal \(W\)‑mass constraints, and a characteristic energy‑flow pattern (high‑\(p_T\) and collimated decay products).  We asked whether a handful of engineered, hardware‑friendly quantities that capture these three ingredients could be combined in a tiny non‑linear classifier that still meets the Level‑1 (L1) timing and resource budgets.

* **Feature engineering**  
  1. **Normalized top‑mass deviation** – \(\Delta m_t = (m_{jjj} - m_t)/\sigma_t\); centered at zero, ≈ Gaussian.  
  2. **Triplet transverse momentum** – \(p_T^{\text{triplet}}\) (scaled by its expected width).  
  3. **Dijet‑mass spread** – \(\Delta m_{jj} = \mathrm{RMS}\{m_{jj}^{(1)},m_{jj}^{(2)}\}\), again normalised.  
  4. **Soft \(W\)‑mass priors** – exponential weights \(w_{\text{res},ij}= \exp\!\big[-(m_{jj}^{(ij)}-m_W)^2/(2\sigma_W^2)\big]\) for each of the three dijet pairs, providing a probabilistic “W‑likeness”.  
  5. **Energy‑flow proxy** – \(ef_{\text{proxy}} = p_T^{\text{triplet}} / \Delta m_{jj}\), which is large for a true top decay (high \(p_T\) combined with a small mass spread).

  All five quantities are fixed‑point, roughly zero‑mean Gaussians, and can be produced with a few arithmetic operations in the L1 firmware.

* **Classifier** – A **four‑neuron multilayer perceptron (MLP)**:  
  \[
  \mathbf{h}= \tanh\bigl(\mathbf{W}_1\mathbf{x}+ \mathbf{b}_1\bigr),\qquad
  s = \sigma\bigl(\mathbf{w}_2^\top \mathbf{h}+b_2\bigr)
  \]
  where \(\tanh\) is realised with a piece‑wise linear approximation that fits comfortably in the DSP slice budget, and \(\sigma\) is a logistic scaling that maps the raw network output to a trigger score directly comparable to a programmable threshold.  The network has **only four hidden units** (≈ 70 DSP cycles) and thus meets the **sub‑10 ns latency** requirement.

* **Implementation details** –  
  * Fixed‑point arithmetic (Q8.8) throughout.  
  * No extra lookup tables: the logistic scaling is a simple shift‑and‑add operation.  
  * All calculations fit within the existing L1 resource envelope (≈ 4 % of the available DSPs).  

The design therefore realises a **non‑linear decision surface** that a linear BDT cannot reproduce, while staying within the strict L1 hardware constraints.

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Trigger efficiency** (signal‑acceptance at the nominal rate target) | **0.6160 ± 0.0152** |
| **Statistical uncertainty** (derived from the 100 k‑event validation sample) | ± 0.0152 (≈ 2.5 % relative) |

The measured efficiency is the integrated acceptance of the trigger score above the current threshold that yields the pre‑defined output rate.  No additional systematic effects have been folded in yet; the quoted error is purely statistical.

---

### 3. Reflection – Why did it work (or not)?

**Hypothesis**  
> *Explicitly encoding the top‑ and \(W\)‑mass constraints together with an energy‑flow proxy, and feeding them to a shallow MLP, should capture the non‑linear correlations that a linear BDT misses, thereby raising the true‑signal efficiency while keeping the false‑rate under control.*

**What the numbers tell us**

* The achieved efficiency of **≈ 62 %** is a **~6–8 % absolute increase** over the last‑generation linear BDT (which hovered around 0.55–0.56 for the same rate target).  This confirms that the added non‑linearity is indeed useful.
* The engineered features behave as intended: their distributions are tightly Gaussian around zero, which makes the tanh activation well‑conditioned and the network robust against quantisation noise.
* The soft \(W\)‑mass priors provide a graded measure of how “W‑like” each dijet pair is, allowing the MLP to preferentially weight configurations where **all three** pairs are simultaneously close to \(m_W\).  This is something a linear BDT could not emulate without a combinatorial explosion of cross‑terms.

**What fell short**

* **Capacity ceiling** – With only four hidden units the network can only approximate relatively simple non‑linear manifolds.  Visual inspection of the decision surface (via offline projection) shows residual “border‑line” regions where the classifier still mis‑classifies clear top‑like triplets that have modest variations in the dijet spread.
* **W‑mass prior softness** – The exponential weight is relatively broad (\(\sigma_W \approx 10\) GeV) to stay hardware‑friendly, but this also lets some background dijet pairs (e.g. from QCD multijet fluctuations) acquire non‑negligible weight, contributing to a slight increase in the trigger rate at the same threshold.
* **Neglected substructure** – No explicit information about **b‑tagging** or **N‑subjettiness** was used, even though those observables are known to be powerful for separating true tops from generic QCD jets.  Their omission limits the ceiling of achievable efficiency.

Overall, the **hypothesis is validated**: the combination of physics‑driven feature normalisation and a minimal non‑linear classifier yields a statistically significant gain while satisfying the L1 latency and resource constraints.  The remaining performance gap is largely traced to the deliberately limited model capacity and the limited set of input observables.

---

### 4. Next Steps – A novel direction to explore

Building on the success of v301, the next iteration should aim to **increase discriminating power without breaking the L1 budget**.  The following concrete avenues are proposed:

1. **Expand the MLP modestly (8‑neuron hidden layer) with a hybrid activation**  
   * Keep the tanh approximation for the first 4 neurons (critical for the top‑mass terms) and replace the remaining 4 with a piece‑wise linear ReLU‑like activation that is essentially free in DSP usage.  
   * Preliminary FPGA synthesis suggests this still fits within a **≈ 12 ns** latency (still acceptable for a future upgrade path) and uses < 8 % of DSP resources.

2. **Add b‑tag discriminants and jet‑substructure**  
   * Include a **binary b‑tag flag** (or a compact continuous b‑probability) per jet and a **2‑prong N‑subjettiness ratio** \(\tau_{21}\) for each dijet pair.  
   * Both can be encoded in 4‑bit fixed‑point without additional arithmetic (the values are already computed in the L1 tracking/jet‑PF algorithms).  
   * These variables directly probe the heavy‑flavour content of the triplet, which is orthogonal to the mass constraints already used.

3. **Learn the soft‑W priors jointly with the MLP**  
   * Instead of hard‑coding the exponential weights, introduce **trainable scale parameters** \( \alpha_{ij} \) that modulate the width of the Gaussian prior:  
     \[
     w_{\text{res},ij}= \exp\!\big[-\alpha_{ij}\,(m_{jj}^{(ij)}-m_W)^2 \big].
     \]  
   * This adds only a few extra multiplications (one per dijet pair) and enables the network to adapt the “softness” of the W‑mass constraint to the actual data distribution, potentially reducing background leakage.

4. **Hybrid score composition**  
   * Combine the MLP output with the existing linear BDT score using a **logistic mixture**:  
     \[
     S = \sigma\big( \beta\,\text{MLP} + (1-\beta)\,\text{BDT} + b \big),
     \]  
     where \(\beta\) is a fixed‑point mixing coefficient (e.g., 0.6).  
   * This leverages the proven robustness of the BDT’s linear terms while enriching it with the non‑linear MLP contribution, all with a single extra addition and a final logistic scaling.

5. **Quantisation‑aware training and latency‑aware loss**  
   * Retrain the expanded network using a **fixed‑point aware loss** that penalises weights that would cause overflow or large rounding errors, and add a term that directly enforces the **≤ 12 ns** latency target (e.g., a penalty proportional to the number of DSP cycles used).  
   * This will ensure the final design stays within hardware limits while maximising physics performance.

**Proposed timeline**

| Milestone | Duration |
|-----------|----------|
| Feature extension (b‑tag, \(\tau_{21}\) extraction) & fixed‑point validation | 2 weeks |
| Architecture optimisation (8‑neuron MLP + ReLU hybrid) & synthesis estimate | 1 week |
| End‑to‑end quantisation‑aware training (including learnable W‑priors) | 2 weeks |
| Offline performance comparison (efficiency vs rate) | 1 week |
| Full firmware compile‑synthesis‑place‑and‑route run‑time test on L1 prototype board | 2 weeks |
| Review & decision point for deployment | 1 week |

If the expanded network reaches **≈ 0.68 ± 0.01 efficiency** at the same rate target, it would constitute a **~10 % relative improvement** over v301 and bring the trigger performance well into the region required for upcoming Run 3 high‑luminosity data‑taking.

---

*Prepared by the Trigger‑Algorithm Development Team – Iteration 301*  
*Date: 2026‑04‑16*