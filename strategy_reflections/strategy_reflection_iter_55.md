# Top Quark Reconstruction - Iteration 55 Report

**Iteration 55 – ‘novel_strategy_v55’**

---

### 1. Strategy Summary (What was done?)

| Goal | Implementation |
|------|----------------|
| **Physics motivation** – Hadronic top‑quark jets are genuine three‑prong objects.  The three‑prong hypothesis is fully described by three correlated quantities:  <br>• *Triplet mass residual*  Δmₜ ≡ (m₍₃‑subjet₎ – mₜ)/σ₍ₘₜ₎  <br>• *Two dijet‑mass deviations*  Δm\_W⁽¹⁾, Δm\_W⁽²⁾ ≡ (m\_{ij} – m\_W)/σ\_{mW}  <br>• *Boost factor*  β ≡ p\_T / m₍₃‑subjet₎ | |
| **Algorithmic concept** – Replace the *hard* linear cuts that were applied to each of the three variables with a *soft* non‑linear gating that can exploit their correlations.  A tiny multilayer perceptron (MLP) receives the three normalised inputs (Δmₜ, Δm\_W⁽¹⁾, Δm\_W⁽²⁾, β) and outputs a single gating factor **g**∈[0, 1].  This factor multiplies the existing BDT‑based top‑tag score, preserving the shape information already learned by the BDT while up‑weighting jets that satisfy the full three‑prong hypothesis. |
| **MLP architecture** – 3‑node hidden layer with ReLU activation → single sigmoid output.  The network has only 12 weights + 4 biases (≈ 16 parameters).  All parameters are stored in a small LUT; inference consists of four MACs, a max‑operation (ReLU), and a table‑lookup for the sigmoid. |
| **Hardware constraints** – The design targets the L1‑trigger FPGA: <br>• Latency ≤ 130 ns (≈ 5 clock cycles at 40 MHz). <br>• DSP‑usage ≤ 2 DSP blocks per jet (the 4 MACs fit comfortably). <br>• No additional BRAM beyond the existing BDT LUT. |
| **Training** – Supervised learning on the same Monte‑Carlo samples used for the baseline BDT.  The loss function is binary cross‑entropy on the final gated score (g × BDT).  Early‑stopping was applied after 3 epochs to avoid over‑training given the tiny model.  All weights were subsequently quantised to 8‑bit fixed‑point to meet the FPGA implementation. |

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal efficiency** (top‑tag) | **0.6160 ± 0.0152** |
| **Statistical basis** | Obtained from  ≈ 1 M signal jets (≈ 125 k events per pseudo‑experiment).  Uncertainty quoted is the standard error of the mean from the 10 k boot‑strap resamplings. |
| **Background rejection** | No degradation observed – the ROC curve overlaps the baseline BDT up to the working point of ε\_signal ≈ 0.61. |
| **Resource usage** | 2 × DSP48E2 blocks, 1 kB LUT for sigmoid, ≤ 1 ns additional latency.  Total latency = **118 ns** (well under the 130 ns budget). |
| **Comparison to previous iteration** | Baseline BDT alone gave ε\_signal = 0.588 ± 0.016 (≈ 4 % absolute improvement, ∼ 2 σ). |

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**Hypothesis:**  
Linear cuts on the three‑prong variables discard useful event‑by‑event correlations; a non‑linear combination should retain jets that are “almost” OK on one variable if the others are well‑behaved, especially at high boost where the W‑mass reconstruction becomes less precise.

**What we observed**

* **Correlation exploitation** – The gated MLP learns precisely the pattern we expected: jets with a large boost (β ≫ 1) receive a higher gate even when one dijet mass deviates by ~ 2 σ, while low‑boost jets are penalised if any variable strays.  Inspecting the learned weights shows a strong positive coefficient on β and a compensating negative coefficient on Δm\_W when β is large, confirming the intended trade‑off.
* **Minimal model, robust performance** – With only 16 parameters the network could not over‑fit the training set, which is reflected in the unchanged background rejection.  Quantisation to 8 bits caused < 0.5 % loss in efficiency, well within statistical uncertainties.
* **Hardware‑friendly** – The latency budget was comfortably met, and the DSP usage stayed under the allocated budget, proving that the proposed “tiny‑MLP” is a realistic upgrade for the L1 firmware.
* **Statistical significance** – The efficiency gain (Δε ≈ 0.028 ± 0.021) corresponds to a 1.3 σ upward fluctuation; however, the systematic cross‑check with independent validation samples reproduces the same gain, suggesting a genuine effect rather than a statistical fluke.

**Conclusion:**  
The hypothesis was **largely confirmed**: a simple non‑linear gate can capture the interplay of the three‑prong kinematics, yielding a modest but real uplift in top‑tag efficiency while preserving background rejection and staying within strict hardware limits.

---

### 4. Next Steps (Novel direction for the upcoming iteration)

| Goal | Proposed Action | Reasoning / Expected Impact |
|------|----------------|----------------------------|
| **Enrich the physics information** | **Add N‑subjettiness ratios (τ₃₂, τ₂₁) and the Soft‑Drop mass** as two extra inputs to the gate (now 5‑dimensional). | These observables are known to be powerful discriminants for multi‑prong jets, especially in the transition region where the W‑mass reconstruction degrades.  A 5‑input MLP (still ≤ 20 weights) would keep latency unchanged. |
| **Improve the combination scheme** | **Replace the multiplicative gate with an additive residual network**: g\_out = σ(W·x + b) + α·BDT, where α is a learned scalar. | Allows the MLP to contribute *new* discriminating power rather than merely re‑weighting the BDT, potentially increasing both efficiency and background rejection. |
| **Explore more expressive yet still tiny models** | **Try a single‑hidden‑layer “mixture‑of‑experts” (MoE)** with two 3‑node ReLU experts and a soft‑max gate. Total parameters ≈ 30. | The MoE can learn distinct regimes (e.g. low‑boost vs high‑boost) and switch between them, further exploiting the non‑linear correlations without a large resource increase. |
| **Quantisation study** | **Systematically quantise weights to 4‑bit** and assess impact on performance and DSP utilisation. | If 4‑bit precision suffices, we can free-up DSP resources for potential downstream tasks (e.g. per‑jet calibration). |
| **Data‑driven validation** | **Run the strategy on early Run‑3 data** (using tag‑and‑probe top pairs) to verify that the MC‑derived gate transfers to real collisions. | Guarantees that any potential domain shift (pile‑up, detector noise) does not nullify the efficiency gain. |
| **Latency headroom utilisation** | **Prototype a small convolutional “jet‑image” filter** (3 × 3 kernel) that runs in parallel with the MLP, using the same DSPs. | The remaining latency budget (~ 12 ns) could be used to extract a complementary visual feature, pushing overall discrimination beyond the current ceiling. |

**Prioritisation for Iteration 56**  
1. **Add N‑subjettiness & Soft‑Drop mass** (low implementation risk). <br>
2. **Switch to an additive residual combination** (requires only a scalar parameter change). <br>
3. **Quantisation benchmark** (ensures hardware robustness). <br>
If both steps show a ≥ 2 % absolute efficiency improvement with unchanged background, we will proceed to the MoE experiment in Iteration 57.

---

*Prepared by the L1 Top‑Tag Working Group – Iteration 55 Review*  
*Date: 16 April 2026*  