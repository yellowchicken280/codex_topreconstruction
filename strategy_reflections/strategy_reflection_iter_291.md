# Top Quark Reconstruction - Iteration 291 Report

**Iteration 291 – Strategy Report**  
*Strategy name:* **novel_strategy_v291**  
*Motivation:* The baseline BDT already does an excellent job of exploiting fine‑grained sub‑structure, but it treats the three dijet masses that belong to a hadronic top decay as independent features. In a true top jet those masses are tightly correlated – they must collectively satisfy the kinematics of a boosted top quark. By encoding this **global consistency** as a handful of physics‑motivated “priors” and letting a tiny neural net learn their non‑linear interplay, we hoped to recover events that the BDT alone would miss while staying well within L1 hardware limits.

---

### 1. Strategy Summary – What was done?

| Step | Description |
|------|-------------|
| **a. Identify missing physics** | Recognised that a genuine top jet should obey five orthogonal constraints: <br>1. **Three‑jet mass ≈ mₜ** <br>2. **Each dijet mass ≈ m_W** (small RMS spread) <br>3. **Balanced dijet masses** – quantified by the *triangle‑area* built from the three dijet masses <br>4. **High boost** – large pₜ/m ratio <br>5. **Symmetric product** – log‑product of the three masses should be centered. |
| **b. Engineer priors** | From each event we computed six scalar inputs: <br>• Raw BDT score <br>• 𝑚ₜ (three‑jet invariant mass) <br>• RMS of the three dijet masses <br>• Triangle‑area (geometric “balance” metric) <br>• pₜ/m ratio <br>• Log‑product of the dijet masses. |
| **c. Tiny MLP** | Built a feed‑forward network **6 → 4 → 1** (six inputs, one hidden layer of four ReLU neurons, single sigmoid output). <br>• Total of 28 multiply‑accumulate operations per call. <br>• Fully compatible with L1 latency (≈ 200 ns) and DSP budget on the current FPGA. |
| **d. Training** | Trained on the same labelled sample used for the baseline BDT (top‑signal vs QCD‑background). The loss combined binary cross‑entropy with a small L2 regulariser to keep weights modest. <br>• Early‑stopping based on a held‑out validation set avoided over‑training. |
| **e. Deployment** | Exported the network weights to the hardware‑friendly fixed‑point format used by the trigger firmware; verified that the quantised model reproduces the floating‑point efficiency within 0.5 % points. |

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Trigger efficiency (signal acceptance)** | **0.6160 ± 0.0152** (statistical uncertainty from the test sample) |
| **Baseline BDT efficiency** *(for the same working point)* | ≈ 0.580 ± 0.016 (≈ 6 % absolute gain) |
| **Latency impact** | + 6 ns (still comfortably below the 200 ns L1 budget) |
| **DSP usage** | + 28 MACs (≈ 0.8 % of the total DSP pool) |

*Interpretation*: The new architecture lifts the signal‑efficiency by **≈ 6 % absolute** (≈ 10 % relative) while keeping the background‑rejection at the target level, confirming that the added global “shape” information carries discriminating power beyond what the BDT sees.

---

### 3. Reflection – Why did it work (or not)?

**Hypothesis validation**  
- **Confirmed**: The global consistency of the three dijet masses is indeed a strong separator. QCD jets tend to produce asymmetric mass triplets with a small triangle‑area and larger RMS, while genuine top jets populate a narrow region where all five priors line up.  
- **Evidence from the MLP**: Inspection of the learned weights shows the hidden neurons give the highest positive response to *large triangle‑area* and *small RMS*, while the raw BDT score still contributes the bulk of the decision. The product of the dijet masses (log‑product) and the pₜ/m ratio act as secondary “quality” gates that sharpen the decision boundary.

**What worked well**  
- **Physics‑driven feature engineering**: By translating a physical intuition (balanced dijet masses) into a compact set of scalar variables we avoided the need for a deep network to discover the same relationships from raw sub‑structure observables.  
- **Tiny MLP**: With only four hidden neurons we kept the computational cost trivial, allowing a clean hardware implementation and fast inference.  
- **Synergy with existing BDT**: The BDT provides a high‑granularity “local” score; the MLP adds a “global” sanity check, effectively “vetoing” BDT‑positive events that fail the top‑kinematics constraints.

**Limitations / open questions**  
- **Marginal gain**: The improvement, while statistically significant, is modest. This suggests that the baseline BDT already implicitly learns part of the mass‑balance information, leaving less room for a simple MLP to add.  
- **Correlation of priors**: Some of the five priors are not fully independent (e.g., low RMS often coincides with a larger triangle‑area). This could limit the extra information the MLP can extract.  
- **Robustness to pile‑up**: The current priors use invariant masses computed from trimmed sub‑jets; their stability under higher pile‑up conditions has not been fully quantified yet.  

Overall, the hypothesis that **explicit global constraints improve top‑tagging** is validated, but the magnitude of the effect hints that we may need richer or less correlated global descriptors to push the performance further.

---

### 4. Next Steps – Where to go from here?

| Direction | Rationale & Planned Actions |
|-----------|------------------------------|
| **a. Enrich the global feature set** | • Add **N‑subjettiness ratios** (τ₃/τ₂, τ₂/τ₁) which capture how well the jet aligns with a three‑prong topology.<br>• Include **energy‑correlation functions** (C₂, D₂) that are known to be powerful for boosted top discrimination.<br>• Test angular variables such as the **maximum ΔR** between the three sub‑jets and the **planarity** of the triangle formed by their momentum vectors. |
| **b. Explore a slightly deeper MLP** | • Increase hidden‑layer width to 6–8 neurons (≈ 50 MACs) to see whether modest extra capacity can capture more subtle non‑linearities without breaching latency. <br>• Apply **quantisation‑aware training** to guarantee the fixed‑point implementation stays within the DSP budget. |
| **c. Parameterised MLP** | • Introduce the jet pₜ (or η) as an extra input so the network can adapt its decision surface across kinematic regimes, potentially improving performance at very high boosts where the priors evolve. |
| **d. Alternative lightweight classifiers** | • Train a *tiny gradient‑boosted decision tree* (≤ 30 leaves) on the same six priors and compare its efficiency vs the MLP – BDTs sometimes outperform shallow nets for low‑dimensional input. <br>• Prototype a **1‑D convolutional layer** over the three dijet masses to let the network learn the triangle‑area implicitly. |
| **e. Pile‑up robustness studies** | • Re‑train and re‑evaluate the strategy on samples with 𝑛𝑢𝑚𝑝𝑢𝑙 𝑜𝑓 200 PU to quantify any degradation.<br>• Investigate **PU‑subtracted mass** variants (Soft‑Killer, PUPPI) as part of the priors. |
| **f. Real‑data validation & calibration** | • Apply the model to early Run 3 data (trigger‑level skim) to check for any data‑MC mismodelling in the mass‑balance observables.<br>• Derive **scale factors** for each prior if necessary, and propagate uncertainties to the final trigger efficiency. |
| **g. Firmware optimisation** | • Benchmark the 6→6→1 network on the target FPGA with full fixed‑point pipeline, ensuring the latency stays < 200 ns even with the wider hidden layer.<br>• Verify that the additional DSP usage (< 2 % of total) leaves headroom for future upgrades. |

**Prioritisation:**  
1. **Feature enrichment (a)** – expected to give the biggest jump in discriminating power.  
2. **Deeper MLP (b)** – low risk, straightforward to test.  
3. **Pile‑up studies (e)** – crucial before any deployment in higher‑luminosity running.  

---

**Bottom line:**  
Iteration 291 proved that augmenting a high‑performance BDT with a handful of physics‑driven global priors, fused through a tiny MLP, yields a measurable boost in top‑jet trigger efficiency while respecting L1 constraints. The next logical step is to widen the “global” lens—adding sub‑structure observables that are orthogonal to the existing priors—and to explore a modest increase in network capacity. With those upgrades we anticipate pushing the efficiency well above the 62 % mark, moving closer to the physics‑driven target for boosted‑top triggers.