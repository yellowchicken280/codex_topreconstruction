# Top Quark Reconstruction - Iteration 525 Report

**Strategy Report – Iteration 525**  
*Strategy name: `novel_strategy_v525`*  

---

### 1. Strategy Summary – What was done?

| Goal | Implementation |
|------|----------------|
| **Exploit the full dijet‑mass information** while keeping the trigger logic FPGA‑friendly. | • For each of the three possible dijet masses \(m_{jj}\) in a jet triplet we assign a **Gaussian weight** \(\exp[-(m_{jj}-m_W)^2/2\sigma_W^2]\) that is maximal when the pair is W‑boson‑like. <br>• Using these weights we compute a **weighted mean** \(\mu\) and a **weighted variance** \(\sigma^2\). A small variance signals that the three jets are consistent with a single W‑like pairing – a hallmark of true hadronic top decays. |
| **Create an energy‑flow proxy** that penalises “one‑jet‑dominant’’ configurations typical of QCD splittings. | • Take the **geometric mean** of the three dijet masses, \(\sqrt[3]{m_{12}\,m_{13}\,m_{23}}\). When one dijet is much larger than the others the geometric mean drops, providing a built‑in rejector for asymmetric QCD three‑jet topologies. |
| **Enforce global top‑mass consistency**. | • Compute the **top‑mass residual** \(|m_{123} - m_t|\) (with \(m_{123}\) the invariant mass of the three‑jet system). Small residuals are required for a genuine top candidate. |
| **Target the boosted regime** where the L1 resolution is optimal. | • Apply a **logistic “boost prior’’** \(\displaystyle f(p_T^{\rm triplet}) = \frac{1}{1+\exp[-k\,(p_T^{\rm triplet} - p_{0})]}\) that up‑weights events with large triplet transverse momentum. |
| **Combine the observables non‑linearly** without sacrificing latency. | • Feed the five engineered variables \(\{\mu,\sigma^2,\mathrm{geom\,mean},|m_{123}-m_t|,f(p_T^{\rm triplet})\}\) into a **tiny two‑layer MLP**: <br> - 4 hidden nodes, sigmoid activation, single output node (combined_score). <br> - All weights and activations are stored in fixed‑point format; the sigmoid is realized with a small LUT and the few required MAC operations fit comfortably into the DSP slice budget. |
| **Decision** | • The MLP output is compared to a single threshold; events above the threshold fire the L1 top trigger. The whole chain was verified to stay well below the 1 µs latency budget. |

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Trigger efficiency** (fraction of true hadronic top events accepted) | **0.6160 ± 0.0152** |

*The quoted uncertainty is statistical (derived from the finite size of the validation sample).*

---

### 3. Reflection – Why did it work (or not)?

**What worked:**

1. **Physics‑driven features** – By weighting each dijet mass with a Gaussian centred on \(m_W\), the algorithm directly measures how “W‑like’’ the jet pairs are, which is a strong discriminator for real top decays.  
2. **Variance as a shape metric** – The weighted variance \(\sigma^2\) captures the spread of the three masses; QCD three‑jet backgrounds typically yield a large spread, while genuine tops give a tight cluster.  
3. **Geometric mean** – This simple proxy penalises configurations where a single dijet dominates, efficiently suppressing one‑jet‑splitting QCD events.  
4. **Boost prior** – The logistic function successfully biases the classifier toward the high‑\(p_T\) regime where the L1 detector resolution is best, improving the signal‑to‑background balance.  
5. **Tiny MLP** – The 4‑node network is sufficient to learn the non‑linear interplay of the five inputs (e.g. a high \(\mu\) together with low \(\sigma^2\) and a strong boost prior) while still meeting strict FPGA resource and latency constraints.

**What limited performance:**

* **Model capacity** – With only four hidden units the network can only capture relatively simple decision boundaries. Some subtle correlations (e.g. between angular separations of jets and the weighted masses) are missed.  
* **Redundancy among variables** – \(\mu\) and the geometric mean are partially correlated, reducing the total information fed to the MLP.  
* **Weight shape** – A pure Gaussian is a convenient approximation but does not reflect the true Breit‑Wigner shape of the W resonance or detector resolution effects.  
* **Absence of flavor information** – No b‑tag or jet‑charge inputs were used, even though a true top decay always contains a b‑quark. This leaves residual QCD background that could be further suppressed.  

**Hypothesis assessment:**  
The original hypothesis – *“Using all dijet‑mass information together with a minimal MLP will give a hardware‑friendly yet powerful top tag at L1”* – is **partially confirmed**. The strategy yields a respectable efficiency (~62 %) while staying comfortably within the latency budget, showing that the physics‑driven observables are indeed valuable. The modest size of the network, however, caps the achievable discrimination; a slightly richer model or additional observables could push the efficiency higher.

---

### 4. Next Steps – Novel direction for the upcoming iteration

Building on the lessons from v525, we propose the following concrete extensions for **Iteration 526**:

| Objective | Proposed Action | Reasoning / Expected Impact |
|-----------|----------------|-----------------------------|
| **Add flavor discrimination** | Incorporate a **b‑tag score** (or a simple binary b‑tag flag) for the jet that is *not* part of the W‑candidate pair. | Real top decays always contain a b‑jet; even a coarse b‑tag can dramatically reduce QCD background without large hardware cost. |
| **Enrich kinematic description** | Compute **ΔR** separations for each jet pair and the **pT ratios** \(p_{T}^{\rm jet}/p_{T}^{\rm triplet}\). Add them as extra MLP inputs. | Angular information is largely uncorrelated with the mass‑based variables and helps to separate collimated W‑decays from wide‑angle QCD splittings. |
| **Refine mass‑weighting scheme** | Replace the Gaussian weight with a **Breit‑Wigner–Gaussian convolution** that better mimics the true W line shape and detector smearing. | Improves the mapping between the weight and the physical likelihood of a jet pair being a W, potentially sharpening \(\mu\) and \(\sigma^2\). |
| **Explore a richer yet still hardware‑friendly model** | Test a **3‑layer MLP** (4 → 6 → 4 hidden nodes) or a **tiny boosted‑decision‑tree (BDT)** with ≤ 8 leaves per tree and ≤ 3 trees. Both can be quantised to 8‑bit fixed point. | Slightly larger capacity should capture the newly added variables’ correlations; BDTs are known to be extremely efficient on FPGA resources when pruned. |
| **Dynamic thresholding** | Instead of a static cut on the MLP output, implement a **pT‑dependent threshold** (e.g. lower threshold for higher triplet pT). | Aligns the decision boundary with the boost prior already used, providing a finer trigger efficiency vs. rate trade‑off. |
| **Hardware‑resource profiling** | Run the updated design through the FPGA synthesis flow to confirm that DSP usage, LUT count, and latency remain < 1 µs. Aim for ≤ 10 % headroom. | Guarantees the new features stay within the hard L1 budget before any physics study. |
| **Full‑simulation validation** | Process the new model on a **high‑statistics sample with realistic pile‑up** (≥ 140 PU) and evaluate both efficiency and fake‑rate curves. | Ensures the improvements survive under the most demanding LHC conditions. |

**Milestones for Iteration 526:**

1. **Week 1‑2:** Implement b‑tag flag, ΔR and pT‑ratio calculations in firmware; generate the new feature set.  
2. **Week 3:** Train the 3‑layer MLP and the 3‑tree BDT on the extended feature set; select the model that best balances performance and quantisation error.  
3. **Week 4:** Synthesise both models on the target FPGA, measure resource usage and latency, pick the one meeting the constraints.  
4. **Week 5‑6:** Run a full‑simulation campaign (including pile‑up) to quantify efficiency, background rejection, and trigger rate.  
5. **Week 7:** Finalise the trigger threshold(s) and write the updated strategy report.

By **adding flavor information, angular observables, and a more realistic mass weight**, while still staying within a modest hardware footprint, we anticipate a **5–10 % absolute gain in efficiency** (targeting ~0.68) and a **noticeable reduction in QCD fake rate**, thereby delivering a more robust L1 top trigger for the high‑luminosity LHC era.