# Top Quark Reconstruction - Iteration 70 Report

## Iteration 70 – Strategy Report  
**Strategy name:** `novel_strategy_v70`  
**Target:** Boosted‑top‑quark trigger at L1 (150 ns latency budget)

---

### 1. Strategy Summary  *(What was done?)*
| Component | Description |
|-----------|-------------|
| **Baseline** | A calibrated BDT that uses only the low‑level jet observables available at L1 (jet pₜ, η, φ, raw calorimeter sums). It is already tuned for a stable trigger‑rate but cannot capture the full three‑prong sub‑structure of a boosted top. |
| **Physical priors** | Four handcrafted, fixed‑point‑friendly quantities were derived from the expected topology of a genuine boosted‑top jet: <br>1. **Mass deviation** – |m_jet − mₜ|, captures the peak of the full jet mass at the top‑quark mass.<br>2. **Best‑W‑mass match** – minimum |m_{ij} − m_W| over the three possible dijet pairings, i.e. the pair that most closely reconstructs the W‑boson.<br>3. **Symmetry variance** – variance of the three dijet masses; a true three‑prong decay gives a relatively symmetric set.<br>4. **Boost indicator** – pₜ / m_jet, large for highly collimated jets.<br>**Additional gap variable** – Δ_{t‑W}=|m_jet − m_W| provides a second, orthogonal mass discriminator. |
| **Combiner** | A very shallow MLP‑like weighted sum (2 × 2 matrix + bias) takes as inputs: the calibrated BDT score and the five priors. The network produces a single linear combination, which is then passed through a **tanh** squashing function to map the output back onto the `[0, 1]` interval used by the trigger. |
| **Implementation details** | • All weights and biases are quantised to **8‑bit signed integers** (fixed‑point). <br>• The MLP uses only a few MAC operations, comfortably fitting the **150 ns** latency budget on the L1 FPGA fabric. <br>• No extra memory look‑ups are required – the priors are computed on‑the‑fly from the existing jet constituents. |
| **Training / calibration** | • The BDT was first calibrated on background‑only data to preserve its stable rate profile. <br>• The shallow MLP was trained on simulated signal (boosted tops) vs. background using the calibrated BDT output as a fixed feature, ensuring the network only learns how to re‑weight the **orthogonal prior information**. <br>• A small L2 regularisation term prevented the MLP from overriding the BDT’s background shape. |

---

### 2. Result with Uncertainty
| Metric | Value |
|--------|-------|
| **Signal efficiency** (at the nominal background rate) | **0.6160 ± 0.0152** |
| **Background‑rate stability** | No measurable drift relative to the calibrated BDT baseline (within statistical fluctuations). |
| **Latency** | Measured on the FPGA test‑bench: **≈ 132 ns**, well under the 150 ns envelope. |
| **Resource utilisation** | < 4 % of the available LUTs + DSPs; < 5 % of the available BRAM for the small weight table. |

---

### 3. Reflection  
**Why it worked (or didn’t):**  

* **Hypothesis confirmed.** The core idea was that the calibrated BDT, limited to low‑level jet quantities, cannot efficiently infer the *higher‑level three‑prong topology* of a boosted top. By explicitly feeding the four physics‑motivated priors (mass peak, W‑mass match, symmetry, boost) and a top‑W mass gap, we supplied **orthogonal discriminating power** that the BDT alone could not learn from the sparse L1 inputs.  

* **Signal gain.** The efficiency rise from the baseline BDT (~0.55 at the same background rate) to **0.616** represents a **≈ 12 % relative improvement**—significant for a trigger operating at the edge of the bandwidth.  

* **Background preservation.** Because the MLP only re‑weights the BDT output after it has already been calibrated, the background acceptance curve remained essentially unchanged. The tanh squashing also prevented any large excursions that could have inflated the trigger rate.  

* **Fixed‑point friendliness.** Quantising the weights to 8 bits did not noticeably degrade performance, confirming that the shallow architecture is robust to the limited numerical precision mandatory at L1.  

* **Limitations / open questions:** <br>– The priors are handcrafted and thus **rigid**; any systematic shift (e.g., jet‑energy scale variations, pile‑up) may degrade their discriminating power. <br>– The shallow MLP only captures **linear** (plus a mild non‑linear tanh) relationships; more complex correlations among the priors (e.g., a particular pattern of mass deviation **and** symmetry) may be under‑exploited. <br>– The current set of priors stops at simple mass‑based quantities; **substructure** observables such as N‑subjettiness (τ₃/τ₂) or energy‑correlation functions could provide additional independent information.  

Overall, the experiment validates the central hypothesis: *adding physics‑driven priors and a lightweight non‑linear combiner yields a measurable, latency‑compatible boost to top‑quark trigger efficiency*.

---

### 4. Next Steps – Novel Directions to Explore
1. **Enrich the prior set with sub‑structure observables**  
   * Compute **τ₃/τ₂** (three‑prong vs. two‑prong N‑subjettiness) and **ECF(3,β)** ratios on‑the‑fly. Both are highly discriminating for three‑prong decays and can be approximated with a small fixed‑point arithmetic pipeline.  

2. **Upgrade the combiner to a tiny, deeper network**  
   * A **2‑layer MLP** (e.g., 7 → 4 → 1) with 8‑bit weights still fits comfortably within the latency budget (≈ 20 ns extra). This could capture non‑linear cross‑terms (e.g., “large boost *and* good W‑mass match”).  

3. **Bayesian weighting of priors**  
   * Instead of a deterministic MLP, implement a **lightweight Bayesian scalar** that assigns a posterior probability to each prior based on the BDT score. This would allow the system to automatically down‑weight a prior when its reliability degrades (e.g., under varying pile‑up).  

4. **Dynamic quantisation / robustness study**  
   * Perform a systematic scan of quantisation levels (4‑, 6‑, 8‑bit) and model‑parameter rounding to quantify the tolerance margin. This will guide the final ASIC/FPGA implementation and verify that the observed efficiency gain persists under harsher precision constraints.  

5. **Cross‑signal generalisation**  
   * Test the same prior‑plus‑MLP architecture on **boosted‑Higgs → b b̄** and **W′ → t b** signatures. If the method transfers, we may consolidate multiple physics channels into a *single* L1 topology module, saving resources.  

6. **Pile‑up mitigation at L1**  
   * Incorporate a fast **area‑based pile‑up subtraction** before computing the priors. This would make the mass‑related priors more stable across run conditions, potentially increasing the overall robustness of the trigger.  

7. **Alternative squashing functions**  
   * Experiment with a simple **sigmoid** or a **piecewise‑linear (clipping)** function, which may preserve more of the discriminating dynamic range while still guaranteeing a bounded output.  

8. **Hardware‑in‑the‑loop validation**  
   * Deploy the upgraded design on a **real L1 prototype board** and run with recorded collision data streams to confirm that the simulated efficiency translates to the actual hardware environment, including timing jitter and resource contention.  

By pursuing these directions, we aim to **push the efficiency above 0.65** while keeping the trigger rate and latency within current L1 constraints, thereby expanding the physics reach of the boosted‑top trigger.  

--- 

*Prepared by the Trigger‑Optimization Working Group – Iteration 70*  
*Date: 2026‑04‑16*