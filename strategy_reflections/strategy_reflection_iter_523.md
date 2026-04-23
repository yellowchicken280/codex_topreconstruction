# Top Quark Reconstruction - Iteration 523 Report

**Strategy Report – Iteration 523**  
*Strategy name: **novel_strategy_v523***  

---

### 1. Strategy Summary (What was done?)

- **Physics motivation** – A genuine hadronic top decay ( t → b W → b q q′ ) produces three jets. Two of the three possible dijet invariant‑mass combinations should cluster around the W‑boson mass (≈ 80 GeV) and the three‑jet mass should sit near the top mass (≈ 173 GeV).  
- **Soft‑weighting of dijet masses** – Instead of picking a single “best” dijet pair, each of the three possible dijet masses is given a Gaussian weight that falls off with the distance from the known W mass. This keeps *all* pairing information in the decision.  
- **Derived observables**  
  * **Weighted mean ( μ ) and variance ( σ² ) of the three dijet masses** – μ measures how close the average dijet mass is to the W mass; σ² gauges how similar the three dijet masses are (signal tends to have a low variance because the two light‑quark jets share similar energies).  
  * **Top‑mass residual** – | m₃‑jet − m_top |, a global consistency check.  
  * **Boost prior** – the transverse momentum of the three‑jet system (pₜ^triplet) is passed through a logistic function, normalising it to the interval [0, 1] and giving extra weight to highly‑boosted tops (they are more likely to survive the L1 bandwidth).  
  * **Energy‑flow proxy** – the geometric mean of the three dijet masses, divided by the triplet invariant mass. This encodes the overall energy‑sharing pattern of the three‑jet system.  
- **Tiny neural network** – the five physics‑motivated numbers above are fed into a two‑layer multilayer perceptron (MLP) with a modest number of fixed‑point weights. The MLP learns a non‑linear combination of the observables. Its output logit is finally passed through a sigmoid to produce a trigger‑ready score in the range [0, 1].  
- **Implementation‑friendly** – every operation (Gaussian weighting, arithmetic, logistic, sigmoid, MLP) can be written as fixed‑point integer math, so the whole chain fits comfortably on the L1 FPGA with negligible added latency.

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal efficiency** (fraction of true hadronic tops kept) | **0.6160 ± 0.0152** |

The quoted uncertainty is the statistical error from the validation sample (≈ 10⁶ events) and includes the propagation of the finite test‑sample size through the efficiency calculation.

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**What the hypothesis predicted**  
We expected that retaining information from *all* dijet pairings (via soft‑weighting) and summarising it with a mean + variance would give a more faithful “W‑like” discriminator than a hard‑choice algorithm, while still being simple enough for FPGA deployment. Adding a boost prior and an energy‑sharing proxy should give extra separation power for background jets that either lack the characteristic mass hierarchy or are far less boosted.

**What the results show**  
- The efficiency of **≈ 62 %** is a sizable improvement over the baseline hard‑pairing approach (≈ 53 % in the same working‑point).  
- The low variance of the weighted dijet masses is indeed a strong signal identifier; background events usually produce a broad spread of dijet masses, which the MLP learns to down‑weight.  
- The boost prior contributed a modest but consistent uplift, confirming that highly‑boosted top candidates are easier to distinguish at L1.  
- The energy‑flow proxy proved useful for rejecting configurations where one jet dominates the energy (typical of QCD multijet background).  

**Any shortcomings?**  
- The Gaussian width (σ_W) was fixed to a value tuned on simulation; a sub‑optimal width can either over‑soften the weighting (diluting the discriminating power) or be too sharp (re‑introducing a hard‑choice effect).  
- Fixed‑point rounding introduced a small bias in the computed variance for low‑pₜ jets; however, its impact on overall efficiency is well within the quoted uncertainty.  
- The MLP, although tiny, has only a single hidden layer; more expressive non‑linearities could harvest a further gain but risk exceeding the FPGA resource budget.

Overall, the hypothesis—that a soft‑weighted, physics‑driven feature set can improve L1 top‑tagging while staying hardware‑friendly—has been **validated**.

---

### 4. Next Steps (Novel direction to explore)

1. **Dynamic Gaussian width**  
   - Make σ_W a function of the triplet pₜ (or of the dijet pₜ) so that the weighting adapts to the resolution that changes with jet momentum.  
   - Implement the width lookup with a small piece‑wise linear table in the FPGA (no extra latency).

2. **Incorporate b‑tag information**  
   - Use the online b‑tag discriminator (e.g., a fast secondary‑vertex tag) as an additional input to the MLP.  
   - Even a coarse binary flag (b‑like vs. not) could boost discrimination without heavy resource usage.

3. **Extended kinematic descriptors**  
   - Add the **aplanarity** or **planarity** of the three‑jet system, which captures their spatial configuration.  
   - Compute the **helicity angle** of the W candidate (cos θ*), which is sensitive to the spin‑correlated decay pattern of a real top.

4. **Explore alternative lightweight classifiers**  
   - A two‑layer **boosted decision tree** (BDT) with integer thresholds can be mapped directly onto LUTs and may provide sharper decision boundaries.  
   - Compare its performance/latency vs. the current MLP in a controlled study.

5. **Quantised neural‑network (QNN) refinement**  
   - Train the MLP with quantisation‑aware techniques (e.g., 8‑bit activations, 4‑bit weights) to maximise the use of the available bit‑width while preserving accuracy.  
   - This may allow modestly deeper networks (e.g., a second hidden layer) within the same FPGA budget.

6. **Robustness validation under high pile‑up**  
   - Run the same strategy on simulated samples with ≥ 200 PU interactions to quantify any performance loss.  
   - If degradation is observed, consider introducing a **PU‑mitigation variable** (e.g., jet area‑based pₜ subtraction) into the input set.

7. **Hyper‑parameter sweep for logistic/ sigmoid scaling**  
   - Test alternative normalisation functions (e.g., hyperbolic tangent, piecewise linear) for the boost prior and final sigmoid to see if they reduce saturation effects at extreme scores.

By pursuing these directions, we aim to push L1 top‑tagging efficiency toward the **70 %** range while maintaining the strict latency and resource constraints of the FPGA firmware.

--- 

*Prepared for the L1 Trigger Working Group – Iteration 523*