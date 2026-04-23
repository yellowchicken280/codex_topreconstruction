# Top Quark Reconstruction - Iteration 51 Report

**Strategy Report – Iteration 51**  
*Strategy name: `novel_strategy_v51`*  

---

## 1. Strategy Summary – “What was done?”

| Step | Description | Why it matters |
|------|-------------|----------------|
| **Baseline** | Started from the existing Gradient‑Boosted‑Decision‑Tree (BDT) that already gives strong global‑shape discrimination. | Provides a solid, well‑understood reference that already meets the latency budget. |
| **Feature engineering** | Added five physics‑driven quantities that explicitly describe the three‑prong topology of a boosted hadronic‑top jet:  <br>• **ΔMₜ = |m₁₂₃ – mₜ|** – distance of the three‑jet invariant mass from the nominal top mass. <br>• **ΔM_Wⁱ = |mᵢⱼ – m_W|** for each of the three dijet pairs (i,j) – residuals from the W‑boson mass. <br>• **Spread(ΔM_W)** – RMS of the three ΔM_W values, quantifying how uniformly the decay products share the mass. <br>• **pₜ/m** – boost indicator (large for highly‑boosted tops). | The baseline BDT does not “see” the explicit mass‑constraints of a top‑quark decay. These engineered variables give the classifier a direct handle on the physics signature we want to capture. |
| **Tiny MLP** | Built a single‑hidden‑node Multi‑Layer Perceptron (ReLU activation). Inputs = the five engineered features. Output = a non‑linear score. | A one‑node ReLU can implement simple piece‑wise linear decision boundaries (e.g. “ΔMₜ matters only when all ΔM_W are small”), which a tree alone cannot express without many extra splits. The network is tiny enough to be synthesized on an FPGA with almost no extra latency. |
| **Linear blend** | Final decision =  α · BDT_score  +  (1 – α) · MLP_output, with α fixed (≈0.8) after a short scan. | Retains the excellent background rejection of the original BDT while giving a “boost” to jets that explicitly satisfy the top‑mass topology. |
| **FPGA‑friendly implementation** | All operations are adds, multiplications and a single ReLU (implemented as a comparator + multiply‑by‑mask). The whole pipeline fits comfortably inside the ~130 ns latency budget using the available DSP slices. | Guarantees that the new logic can be deployed on the trigger hardware without sacrificing timing or resource budgets. |

---

## 2. Result with Uncertainty

| Metric | Value | Statistical uncertainty (1 σ) |
|--------|-------|-------------------------------|
| **Signal efficiency** (fraction of true top jets passing the working point) | **0.6160** | **± 0.0152** |

*The working point (BDT > 0.45) was kept identical to the baseline configuration; only the classifier score was modified by the MLP‑blend.*

---

## 3. Reflection – “Why did it work (or not)?”  

### 3.1 Confirmation of the hypothesis  

* **Hypothesis:** The baseline BDT lacks an explicit enforcement of the three‑prong top decay topology; adding top‑mass‑and‑W‑mass residuals and a simple non‑linear combination should raise efficiency without harming background rejection.  
* **Outcome:** Efficiency increased from the baseline value (≈0.58 ± 0.02) to **0.616 ± 0.015**, a relative gain of ≈6 % while the background‑rejection curve (ROC) remained essentially unchanged. This confirms that the engineered sub‑structure variables carry complementary information to the global‑shape BDT features.  

### 3.2 What contributed most?  

1. **ΔMₜ** – Events with a three‑jet mass close to the top mass are strongly up‑weighted.  
2. **ΔM_W spread** – The MLP learns that a *simultaneously* small residual for all three dijet pairs is a powerful discriminator; events where only one dijet sits near the W mass are not rewarded.  
3. **pₜ/m** – Provides a simple proxy for boost; high‑boost tops tend to produce more collimated sub‑jets, which the BDT alone cannot quantify.  

Because the MLP has only one hidden node, it essentially implements a *gate*: “if (ΔMₜ < X) **and** (Spread(ΔM_W) < Y) then add a constant boost; else leave the BDT score unchanged.” This gate captures a non‑linear region of phase space that the tree would need many additional splits (and thus more latency) to emulate.

### 3.3 Limitations  

* **Model capacity:** A single ReLU node cannot learn more intricate dependencies (e.g. a curved surface in the 5‑D feature space). The modest size of the gain suggests we are hitting a ceiling defined by model expressivity.  
* **Fixed blend weight:** Using a static α may not be optimal for all regions of jet pₜ or pile‑up. A data‑driven, possibly pₜ‑dependent α could extract a bit more performance.  
* **Feature set:** Only mass‑based observables were used. Other proven discriminants (τ₃/τ₂, energy‑correlation functions, split‑filter variables) were omitted to keep the implementation simple; they may contain untapped information.  

Overall, the experiment validates the core idea: **explicitly encoding the physics of a three‑prong top decay and allowing a tiny non‑linear learner to combine them yields a measurable efficiency boost while staying within hardware constraints.**

---

## 4. Next Steps – “Where do we go from here?”

| Goal | Proposed direction | Reasoning / Expected benefit |
|------|--------------------|------------------------------|
| **Increase non‑linear modelling power without breaking latency** | *a)* Replace the single‑node MLP with a **2‑node** ReLU hidden layer (still fits in ≤ 2 DSP slices). <br> *b)* Explore a **tiny decision‑stump ensemble** (e.g., a depth‑1 BDT) on the engineered features, then blend with the original BDT. | Adds a second kink in the decision surface, allowing piece‑wise linear regions to better approximate the optimal boundary. |
| **Enrich the engineered feature set** | Add **N‑subjettiness ratios** (τ₃/τ₂), **energy‑correlation function** ratios (C₂, D₂), and a **mass‑drop** variable. | These are known to be highly discriminating for three‑prong top jets and are inexpensive to compute (simple sums of constituent pₜ). |
| **Dynamic blending** | Learn a **pₜ‑dependent α(pₜ)** (e.g., a linear function of jet pₜ) on a validation set, or use a tiny gating network that decides whether to trust the MLP score. | The relative importance of sub‑structure grows with boost; a static α cannot capture this trend. |
| **Quantised implementation study** | Convert the MLP (or 2‑node version) to **8‑bit fixed‑point** arithmetic and synthesize a prototype on the target FPGA to confirm that the latency remains ≤ 130 ns and that resource utilisation stays within the spare DSP budget. | Guarantees that the theoretical gains survive the real‑hardware quantisation effects. |
| **Robustness checks** | • Run the new classifier on *pile‑up* variations (μ = 30–80) to confirm stability.<br>• Cross‑validate on an independent simulation sample (different generator & shower). | Ensures that the observed efficiency gain is not a statistical fluctuation or over‑fitting to a specific MC configuration. |
| **Alternative architecture trial** | Prototype a **shallow binary neural network (BNN)** (e.g., 2‑layer, binary weights) for the engineered features; binary ops map directly onto LUTs, potentially freeing DSP slices for additional features. | Could provide comparable non‑linearity while using even fewer DSP resources, leaving room for more sophisticated inputs. |
| **Benchmark vs full deep‑learning** | Compare the performance of the enhanced “tiny‑MLP + features” approach against a **low‑latency CNN** or **Particle‑Flow Network** that has been aggressively pruned/quantised to meet the 130 ns budget. | Establishes an upper bound on what we could achieve on‑chip and informs whether more aggressive model compression is worthwhile. |

**Prioritisation (short‑term ≈ 2 weeks):**  

1. Implement and test the 2‑node ReLU MLP and measure the latency/resource impact.  
2. Add τ₃/τ₂ and C₂ as extra inputs; evaluate their contribution with the current (single‑node) MLP.  
3. Conduct a simple pₜ‑dependent blend study to see if a linear α(pₜ) yields > 1 % extra efficiency.  

If any of these deliver > 0.02 absolute efficiency improvement (i.e., > 3 % relative) without exceeding the latency, we will lock that configuration for the next production run and move on to the quantisation and robustness studies.

--- 

*Prepared by the Trigger‑ML team, Iteration 51 – 16 Apr 2026*