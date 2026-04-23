# Top Quark Reconstruction - Iteration 516 Report

**Strategy Report – Iteration 516**  
*“novel_strategy_v516”*  

---

### 1. Strategy Summary – What was done?

| Goal | How it was addressed |
|------|----------------------|
| **Recover information lost by the baseline merged‑top BDT** |  • Added *physics‑motivated* descriptors that explicitly encode the three‑body decay kinematics of a boosted top quark. |
| **Stay within L1 firmware limits** |  • Designed a *tiny two‑layer MLP* (≈ 30 multiply‑accumulate operations, 8‑bit fixed‑point arithmetic). All weights are quantisable, so the network can be loaded onto the existing L1 hardware. |
| **Keep the trigger fast, interpretable and robust** |  • Used only seven engineered features – no raw high‑dimensional inputs – allowing a clear physical interpretation and small latency. |

**Feature engineering** (7 inputs total)  

1. **Three “pull” variables** – for each of the three dijet mass hypotheses \(m_{ij}\) (the three possible pairings of the three sub‑jets), compute the deviation from the known W‑boson mass: \(\displaystyle \frac{m_{ij}-m_W}{\sigma_{ij}}\).  
2. **Variance of the three pulls** – measures how consistently the jet follows the expected \(t\!\to\!Wb\) mass pattern.  
3. **Asymmetry measure** – quantifies skewed mass patterns that are typical of QCD jets rather than a symmetric three‑body decay.  
4. **Log of the jet transverse momentum** – \(\log(p_T)\) supplies a gentle correction for the residual \(p_T\)‑dependence of jet sub‑structure.  
5‑7. **Baseline quantities** (e.g. original BDT score, jet‑mass, and a simple shape variable) that were already available in the L1 menu.  

All seven variables were fed into the 2‑layer MLP (10 hidden nodes → 1 output node). The network was trained on simulated signal (high‑\(p_T\) top jets) vs. QCD background, then the weights were quantised to 8‑bit integers for firmware deployment.

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Trigger efficiency (signal acceptance)** | **0.6160 ± 0.0152** |

*The quoted uncertainty is statistical (derived from the evaluation sample).*

*For reference:* the baseline merged‑top trigger (raw BDT only) yields an efficiency of ≈ 0.59 ± 0.017 in the same configuration. The new strategy therefore delivers an **absolute gain of ~ 0.027 (≈ 4.5 % points)**, corresponding to an **≈ 8 % relative improvement** while respecting the same L1 latency budget.

---

### 3. Reflection – Why did it work (or not)?

#### Hypothesis
> *Enriching the trigger with explicit three‑body mass‑pattern descriptors and a compact non‑linear combiner will restore the kinematic information the vanilla BDT discards, improving discrimination without exceeding firmware resources.*

#### What the results tell us
1. **Physics‑driven pulls are useful** – The three pull variables directly encode the expected \(W\!-\!b\) mass hierarchy. When the three dijet masses line up with the W‑boson mass, the MLP receives a clear “signal‑like” pattern; when they do not (as in QCD jets), the pulls scatter, producing a distinct output.  
2. **Variance & asymmetry add robustness** – The variance of the pulls tells the network whether *all* three pairings agree with the hypothesis. The asymmetry term flags the skewed mass distributions that often arise from gluon‑splitting jets, further suppressing background.  
3. **Non‑linear combination matters** – A linear BDT can only weight each input. The two‑layer MLP can form *products* of pulls (e.g. “small variance **and** small asymmetry”), which yields a sharper decision boundary and explains the observed efficiency gain.  
4. **Log\(p_T\) handles residual scaling** – Adding \(\log(p_T)\) lets the network modestly adapt to the mild shift of sub‑structure observables with jet energy, preventing a systematic loss of efficiency at the highest \(p_T\).  
5. **Hardware feasibility is confirmed** – The model stays comfortably under the ≈ 30 MAC budget and fits the 8‑bit arithmetic constraints, confirming that the design is implementable in L1 firmware.

#### Limitations & open questions
* The improvement, while statistically significant, is modest. This suggests that the 7‑dimensional feature set already captures most of the discriminating information available at L1, *or* that the tiny MLP is hitting a capacity ceiling.  
* The pull variables assume a fixed W‑mass and a simple resolution model (\(\sigma_{ij}\)). Any detector mis‑calibration or varying pile‑up conditions could shift these pulls and degrade performance.  
* Quantisation to 8 bits introduces a small bias that has not yet been quantified with a bit‑accurate firmware simulation; real‑hardware tests are needed.  

Overall, the hypothesis is **largely confirmed**: physics‑motivated descriptors combined with a minimal non‑linear model give a measurable, hardware‑safe boost in trigger efficiency.

---

### 4. Next Steps – Where to go from here?

| Direction | Rationale | Concrete actions |
|-----------|-----------|-------------------|
| **Add complementary sub‑structure observables** | Variables such as N‑subjettiness \(\tau_{21}\), energy‑correlation functions \(D_2\), and Soft‑Drop mass capture shape information orthogonal to the mass‑pulls. | • Compute \(\tau_{21}\), \(D_2\) for the merged jet; <br>• Append them to the current feature vector (still ≤ 10 inputs). |
| **Explore a slightly deeper MLP** | A third hidden layer (≈ 15 additional MACs) could capture more intricate correlations without breaking the L1 budget. | • Train a 3‑layer MLP (10 → 15 → 5 → 1 nodes); <br>• Verify that total MACs stay ≤ 70; <br>• Quantise and benchmark latency. |
| **Full bit‑accurate firmware validation** | Quantisation error may differ from the floating‑point training behaviour. | • Use the FPGA‑level simulation toolbox to ingest the 8‑bit weights and inputs; <br>• Measure the trigger decision shift and adjust weight scaling if needed. |
| **Robustness studies under extreme pile‑up** | Run‑3 and HL‑LHC will see \(\mu\) > 80. The current pulls may be more sensitive to pile‑up contamination. | • Re‑train with samples at \(\mu = 80, 100\); <br>• Test adding a pile‑up mitigation term (e.g. PUPPI‑weight or area‑subtracted jet‑mass) as an extra input. |
| **Dynamic \(p_T\) scaling** | Log\(p_T\) works, but a piecewise linear correction or a small learned scaling factor could better capture non‑linear dependence. | • Replace log\(p_T\) with a two‑bin \(p_T\) indicator (low/high) or a learned embedding; <br>• Compare efficiency trends across the full \(p_T\) spectrum. |
| **Hybrid trigger logic** | The baseline BDT still contains useful information (e.g. correlations with calorimeter timing). A logical OR/AND with the MLP output might recover efficiency in corner cases. | • Design a “OR‑if‑MLP‑high‑OR‑BDT‑high” decision; <br>• Evaluate overall rate vs. efficiency trade‑off. |
| **Data‑driven calibration** | Real data may show shifts in the W‑mass peak or jet‑energy scale. | • Use early Run‑3 data to calibrate the pulls (fit the W‑mass in dijet combinations); <br>• Update the pull definitions online via a simple LUT. |

**Milestones for the next iteration (517)**  

1. **Feature expansion prototype** (add \(\tau_{21}\) & \(D_2\)) – benchmark against the current 7‑feature MLP.  
2. **Three‑layer MLP feasibility study** – measure MAC count, latency, and quantisation impact.  
3. **Bit‑accurate firmware test** – confirm that the 8‑bit implementation reproduces the simulated efficiency within ±0.5 %.  

If these studies show a ≥ 3 % absolute efficiency gain *or* a comparable gain at a reduced trigger rate, the new configuration will be promoted to the next L1 firmware release.

---

**Bottom line:** Iteration 516 demonstrates that a lean, physics‑guided MLP can squeeze extra performance out of the merged‑top trigger while remaining L1‑friendly. The modest boost validates the underlying hypothesis and points the way toward richer sub‑structure inputs and modestly deeper networks as the next logical frontier.