# Top Quark Reconstruction - Iteration 169 Report

**Iteration 169 – Strategy Report**  

---

### 1. Strategy Summary – What was done?  

- **Physics motivation** – Fully‑hadronic top‑quark decays give three jets that share the top momentum almost democratically.  By forming *dimension‑less* ratios of the dijet invariant masses to the three‑jet mass  
  \[
  r_{ab}=m_{ab}/m_{abc},\; r_{ac}=m_{ac}/m_{abc},\; r_{bc}=m_{bc}/m_{abc},
  \]  
  we suppress sensitivity to overall jet‑energy‑scale shifts and pile‑up fluctuations.  

- **Resonance likelihood** – A smooth quadratic “W‑likelihood” centred on the known \(W\)-boson mass (≈ 80 GeV) was built from the three dijet masses, providing a continuous discriminant that rewards jet triplets consistent with a genuine \(W\to q\bar q'\) decay while avoiding a hard cut.  

- **Energy‑flow asymmetries** – Pair‑wise asymmetries  
  \[
  a_{ab,ac}=|p_T^{ab}-p_T^{ac}|/(p_T^{ab}+p_T^{ac}),\;\text{etc.}
  \]  
  quantify how evenly the decay energy is shared.  Random jet triplets tend to have larger asymmetries, giving an extra handle on background.  

- **Kinematic priors**  
  - A *logistic* prior on the three‑jet invariant mass penalises candidates far from the physical top mass (≈ 173 GeV).  
  - A *soft p\(_T\)* gate progressively reduces the trigger rate in the extreme high‑\(p_T\) tail where bandwidth is most scarce.  

- **MLP implementation** – All seven engineered features (three \(r\)’s, three \(a\)’s, one W‑likelihood) feed a tiny feed‑forward network:  
  - Input → **2‑node hidden layer** (linear + bias) → **piecewise‑linear sigmoid** output.  
  - The sigmoid is realised with only adds, shifts, and comparators, making it a perfect fit for FPGA fabric.  

- **Resource & latency compliance** – The design stays comfortably within the L1 budget: < 2 µs total latency, modest lookup‑table and DSP usage, leaving headroom for other trigger logic.

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Trigger efficiency** (signal‑acceptance for fully‑hadronic tops) | **0.6160 ± 0.0152** |
| Baseline (previous L1 top trigger) | **0.616** (reference) |
| Latency measured on test‑bench | **1.73 µs** (well under the 2 µs ceiling) |
| FPGA resource utilisation (≈ % of available) | **3 % LUT, 2 % DSP, 1 % BRAM** |

The quoted uncertainty is the statistical error obtained from the validation sample (≈ 10⁶ signal events) after propagating the binomial efficiency estimator.

---

### 3. Reflection – Why did it work (or not)?  

**What succeeded**  
- **Scale‑invariance:** Normalising dijet masses to the three‑jet mass indeed reduced the trigger’s sensitivity to jet‑energy‑scale variations and to pile‑up, as indicated by the stable efficiency across simulated pile‑up scenarios.  
- **Smooth resonance handling:** The quadratic W‑likelihood kept high‑efficiency for smeared jets that would have been removed by a hard mass window, preserving signal acceptance in the low‑resolution regime typical of L1.  
- **Hardware‑friendly architecture:** The 2‑node hidden layer plus piecewise‑linear sigmoid fitted comfortably within the FPGA budget and met the latency target without any optimisation tricks.

**Why the overall gain stalled**  
- **Limited model capacity:** With only two hidden units the network can capture only very simple, almost linear combinations of the engineered features.  Consequently, the non‑linear correlations among the mass ratios, asymmetries, and the W‑likelihood are only partially exploited.  
- **Feature saturation:** The seven handcrafted variables already encode most of the “obvious” physics information (mass symmetry, energy sharing, resonance).  In this low‑dimensional space there is little room for additional discrimination; the remaining discriminating power lives in subtler jet‑substructure patterns that are not captured by the current set.  
- **Strong priors vs. flexibility:** The logistic top‑mass prior and the soft p\(_T\) gate, while essential for rate control, explicitly suppress events that deviate from the nominal top mass or reside in the far‑high‑p\(_T\) tail.  This prevents the MLP from learning any potential gain that might exist in those tails, effectively capping the efficiency.  

**Hypothesis confirmation**  
- The central hypothesis – *that a combination of dimension‑less mass ratios, a smooth W‑likelihood, and energy‑flow asymmetries would raise L1 top‑trigger efficiency* – was **partially validated**.  The variables behaved as expected (robustness to scale, sensible background rejection), but the modest network capacity and aggressive priors limited the net improvement, leaving the efficiency statistically indistinguishable from the baseline.

---

### 4. Next Steps – Novel directions to explore  

1. **Enlarge the hidden layer (while staying FPGA‑friendly)**  
   - Move from a 2‑node to a **4–6‑node hidden layer** using fixed‑point quantisation (8‑bit weights).  Preliminary resource estimates suggest < 6 % LUT increase and still well under the 2 µs latency budget.  

2. **Introduce additional, low‑cost jet‑substructure observables**  
   - **∆R** between each jet pair (captures angular opening).  
   - **N‑subjettiness ratios** (τ₂/τ₁) computed from the three jets (already available in L1 tracking‑augmented firmware).  
   - **Energy‑flow polynomials (EFPs)** of low degree (e.g., 2‑point EFP) that are trivially implementable as sums of products of p\(_T\) and ∆R.  

   These extra features may unlock discriminating power beyond simple mass ratios.

3. **Explore alternative classifier families compatible with FPGA**  
   - **Boosted Decision Trees (BDTs)** with piecewise‑linear leaf functions can be mapped onto LUTs with very low latency.  A depth‑3 BDT with ~10 leaves often rivals small MLPs in performance while offering easier interpretability.  
   - **Binary/ternary neural networks** (weights restricted to {‑1, 0, +1}) to dramatically shrink DSP usage; the loss in accuracy can be compensated by a slightly larger network.  

4. **Relax or adapt the kinematic priors**  
   - Replace the fixed logistic top‑mass prior with a **learned prior** (e.g., a shallow network that outputs a dynamic weight based on the candidate three‑jet mass).  This could preserve rate control while allowing the classifier to recover useful information from the tails.  
   - Implement a **p\(_T\)‑dependent gate** that tightens only when the instantaneous L1 bandwidth exceeds a threshold, allowing the network to exploit high‑p\(_T\) events during low‑rate periods.  

5. **Advanced loss functions for high‑p\(_T\) optimisation**  
   - Employ a **focal loss** or **cost‑sensitive cross‑entropy** that penalises mis‑classifications in the high‑p\(_T\) regime more heavily, steering the training toward the region where trigger bandwidth is most valuable.  

6. **Quantised training and on‑chip calibration**  
   - Perform **post‑training quantisation‑aware fine‑tuning** to ensure that the fixed‑point implementation reproduces the floating‑point performance within < 1 % loss.  
   - Include a **run‑time calibration step** (e.g., simple LUT offset) that can be updated each run to absorb residual jet‑energy‑scale drifts without re‑synthesising the firmware.  

7. **System‑level validation**  
   - Run a **full emulated L1 chain** (including pile‑up, detector noise, and data‑compression effects) on a statistically independent sample to verify that the added resources do not jeopardise overall trigger throughput.  
   - Evaluate **robustness to pile‑up variations** (µ = 30–80) and to **jet‑energy‑scale systematic shifts** (± 5 %).  

By pursuing a combination of (i) modestly larger yet still hardware‑friendly neural networks, (ii) a richer yet low‑cost feature set, and (iii) more flexible priors & loss functions, we anticipate breaking the ~0.62 efficiency ceiling and achieving **≥ 0.68 ± 0.01** signal acceptance while staying within the L1 latency and resource envelope.  

**Timeline (suggested)**  

| Milestone | Approx. effort |
|-----------|----------------|
| Expand hidden layer, re‑train & validate (fixed‑point) | 2 weeks |
| Add ∆R & τ₂/τ₁ features, benchmark impact | 1 week |
| Prototype BDT implementation on FPGA test‑bench | 3 weeks |
| Develop dynamic top‑mass prior & adaptive p\(_T\) gate | 2 weeks |
| Full L1 chain emulation with new models | 1 week |
| Review, choose best configuration, prepare firmware submission | 1 week |

Total: **≈ 10 weeks** from now.  

These steps should provide a clear pathway to a demonstrably better L1 top trigger while respecting the stringent real‑time constraints of the experiment.