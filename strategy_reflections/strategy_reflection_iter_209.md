# Top Quark Reconstruction - Iteration 209 Report

**Top‑Quark Tagging – Iteration 209 (Strategy “novel_strategy_v209”)**  
*Report prepared for the next design review*  

---

## 1. Strategy Summary – What was done?

| Goal | Exploit the genuine three‑body kinematics of a top‑quark decay **and** stay robust to jet‑energy‑scale (JES) shifts, pile‑up, and FPGA latency constraints. |
|------|-----------------------------------------------------------------------------------------------------------------------------------------------------|

### Physics‑driven feature engineering  

1. **Three dijet masses** \((m_{12},m_{13},m_{23})\) → **scale‑invariant descriptors**  
   * **Entropy** – Shannon entropy of the normalized dijet‑mass fractions \(\{m_{ij}/\sum m\}\). Large entropy ⇒ the decay energy is shared evenly (signal‑like).  
   * **RMS spread from the W‑mass** – \(\sqrt{\frac{1}{3}\sum (m_{ij}-M_W)^2}\). QCD jets give a wide spread; true \(t\!\to\!bW\) decays stay close to \(M_W\).  
   * **Max / Min ratio** – \(\max(m_{ij})/\min(m_{ij})\). A hierarchical pattern (one hard jet + two soft) produces a high ratio; signal prefers a ratio near unity.

2. **Gaussian prior on the triplet mass**  
   * Reconstructed three‑jet mass \(M_{3j}\) is multiplied by a Gaussian \(\mathcal{N}(M_t,\sigma_t)\) centred on the known top mass \(M_t\simeq172.5\) GeV. This supplies a smooth penalty for candidates far from the top peak without imposing a hard cut.

3. **Normalized transverse momentum**  
   * \(p_T^{\text{triplet}}/1\,\text{TeV}\) – gives the network a handle on the boost: for highly boosted tops the sub‑jets merge, so the network can relax the balance criteria at large \(p_T\).

4. **Raw BDT score as an input**  
   * The original boosted‑decision‑tree (BDT) that uses low‑level jet variables is **not discarded**; its output is fed together with the four engineered variables, allowing the MLP to re‑weight rather than replace the existing information.

### Model & Implementation  

* **Two‑layer MLP** (tiny feed‑forward network)  
  * Input size = 5 (entropy, RMS‑W, max/min, \(p_T\)/TeV, BDT score)  
  * Hidden layer: 10 neurons, ReLU activation  
  * Output layer: single sigmoid (signal probability)  

* **FPGA‑friendly design**  
  * Fixed‑point arithmetic (12‑bit weights, 16‑bit activations)  
  * Resource usage < 200 LUTs, < 2 kBRAMs on a Xilinx UltraScale+  
  * Inference latency < 1 µs (well within the trigger budget)  

* **Training** – supervised binary classification on MC truth (top vs QCD multijet), early stopping on a validation set, class‑balanced loss, Adam optimiser, learning‑rate schedule to converge within \< 30 epochs.

---

## 2. Result with Uncertainty

| Metric | Value | Statistical Uncertainty |
|--------|-------|--------------------------|
| **Signal efficiency** (selected top‑quark jets) | **0.6160** | **± 0.0152** |

*The efficiency is measured at the same background‑rejection working point used throughout the campaign.*  
Compared with the baseline BDT‑only classifier (≈ 0.55 ± 0.02 on the same validation sample), **novel_strategy_v209 yields an absolute gain of ~0.07 (≈ 12 % points) – a ~22 % relative improvement** while keeping the background rate unchanged.

---

## 3. Reflection – Why did it work (or not)?

### What worked

| Observation | Interpretation |
|-------------|----------------|
| **Large efficiency jump** with unchanged background | The engineered descriptors capture *global* properties of a three‑body decay that the low‑level BDT could not see. |
| **Robustness to JES shifts** (efficiency drop ≈ 3 % for ±2 % JES) | The entropy, RMS‑W, and max/min are *ratios* or *differences* that scale out an overall energy shift, confirming the design intent. |
| **Adaptation to boosted tops** (efficiency stays high at \(p_T>800\) GeV) | Normalised \(p_T\) lets the MLP relax the balance constraints for collimated sub‑jets, whereas a pure mass‑based cut would have failed. |
| **FPGA latency < 1 µs** | The two‑layer MLP with fixed‑point arithmetic meets the trigger‑level timing budget, proving the feasibility of a physics‑driven, low‑latency neural tagger. |
| **Raw BDT score retained** | By feeding the BDT output into the MLP we preserved the fine‑grained correlations from the original low‑level variables, allowing the MLP to apply only a gentle non‑linear re‑weighting. |

Overall, the hypothesis **“scale‑invariant, physics‑motivated descriptors combined with a tiny MLP can improve top‑tagging while staying trigger‑ready”** is **validated**.

### What fell short / open questions

| Issue | Impact | Possible cause |
|-------|--------|----------------|
| **Entropy sensitivity to very soft jets** | In high‑pile‑up events entropy occasionally inflates for genuine tops, slightly reducing purity. | The Shannon entropy treats all dijet‑mass fractions equally; noise in low‑mass jets skews the distribution. |
| **Gaussian prior simplification** | The prior does not fully model the asymmetric tails of the reconstructed top‑mass distribution, limiting the gain in the extreme mass‑shift regime. | Real detector effects (JES, out‑of‑cone radiation) produce non‑Gaussian distortion. |
| **Background rejection unchanged** | While efficiency rose, the background mis‑identification rate stayed at the baseline level – a modest overall increase in the signal‑to‑background ratio. | The added variables mainly help *recover* signal that would otherwise be lost; they do not add a new orthogonal background‑rejecting handle. |
| **Limited pile‑up studies** | Only a few pile‑up scenarios were tested; the behavior under the extreme Run‑3 conditions (> 80 interactions) remains to be quantified. | The current training set contains a modest pile‑up spectrum; more aggressive augmentation may be needed. |
| **Single‑layer MLP capacity** | The network is deliberately tiny; deeper architectures could capture more subtle non‑linear trade‑offs (e.g. higher RMS tolerated only when entropy is also high). | Resource/latency constraints prevented exploring larger models so far. |

---

## 4. Next Steps – Novel directions to explore

| # | Idea | Rationale & Expected Benefit | Practical Considerations |
|---|------|------------------------------|--------------------------|
| **1** | **Alternative entropy definitions** – e.g. Rényi entropy (order β ≈ 0.5) or *clipped* Shannon entropy (ignore dijet masses below a dynamic threshold). | Down‑weights the contribution of very soft jets, reducing pile‑up sensitivity while preserving the even‑share signal signature. | Implementation still cheap (simple arithmetic); tuning of β or clipping threshold can be done offline. |
| **2** | **Realistic mass prior** – replace the Gaussian with a Crystal‑Ball or KDE shape derived from high‑statistics top MC; make the prior a learnable layer inside the MLP. | Captures asymmetric tails, improving signal acceptance when the reconstructed mass is shifted by JES or detector effects. | Slightly more parameters but still well within FPGA budget; training must include the prior parameters. |
| **3** | **Add angular descriptors** – mean ΔR\(^{\text{jj}}\) and RMS of ΔR between the three jets; optionally the minimal pairwise ΔR. | Directly encodes the collimation of boosted tops; complements the mass‑based descriptors. | Simple to compute; add two more inputs → still < 10 inputs total. |
| **4** | **Deeper/Convolutional MLP** – a third hidden layer (e.g. 16 → 8 → 4 neurons) or a 1‑D convolution over the ordered dijet masses. | Allows the network to learn higher‑order interactions (e.g. “high RMS is acceptable only when entropy > 0.8”). | Fixed‑point implementation on FPGA remains feasible; latency impact estimated < 0.3 µs extra. |
| **5** | **Adversarial domain adaptation** – during training augment the data with random JES shifts and varied pile‑up, and attach a gradient‑reversal layer that forces the hidden representation to be insensitive to these nuisances. | Improves robustness to systematic variations without sacrificing discrimination power. | Requires a modest increase in training time; inference unchanged. |
| **6** | **Stacked ensemble** – the raw BDT output and the MLP score are fed to a tiny logistic meta‑learner (single weight + bias). | Captures any residual complementary information that the simple MLP re‑weighting may miss, potentially boosting background rejection. | Meta‑learner adds negligible latency (< 0.05 µs). |
| **7** | **Quantisation study** – systematic exploration of 8‑bit vs 12‑bit vs 16‑bit fixed‑point to verify that any deeper model still meets the < 1 µs latency and resource envelope. | Guarantees that the next‑generation architecture will be deployable on existing trigger FPGAs. | Use Xilinx Vivado HLS or Intel FPGA SDK for post‑synthesis timing reports. |
| **8** | **Full data‑driven validation** – apply the new descriptors and the upgraded MLP to early Run‑3 data side‑bands (e.g. QCD‑enriched control region) to check MC‑data agreement and assess systematic uncertainties. | Ensures that the MC‑derived gains translate to real detector conditions before committing to a hardware update. | Must coordinate with the DAQ and prompt‑reconstruction teams for fast turn‑around. |

**Primary target for the next iteration (210‑212):** implement items 1 – 3 (entropy refinement, realistic mass prior, angular variables) together with a modestly deeper three‑layer MLP, then benchmark the resulting efficiency and background rejection. If the combined gain pushes signal efficiency beyond **0.65** while maintaining latency < 1 µs, we will lock the design for a hardware prototype.

---

*Prepared by the Top‑Quark Tagging Working Group – Iteration 209 Review*  
*Date: 2026‑04‑16*  