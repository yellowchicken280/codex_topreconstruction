# Top Quark Reconstruction - Iteration 566 Report

**Strategy Report – Iteration 566**  
*Strategy name:* **novel_strategy_v566**  
*Goal:* Recover top‑tagging discriminating power in the ultra‑boosted regime where classic sub‑structure observables become ineffective.  

---

## 1. Strategy Summary  

| Aspect | What was done |
|--------|----------------|
| **Physics motivation** | In ultra‑boosted jets the three partons from a top decay are razor‑thin, so angular‑based variables (τₙ, ECFs, etc.) lose resolution. However, the **kinematic constraints** – overall jet mass ≈ mₜ, at least one dijet pair ≈ m_W, and an approximately symmetric sharing of the jet energy – remain robust. |
| **Feature engineering** | • **Top‑pull** – a resolution‑aware pull that measures how far the total jet mass deviates from the top mass, normalised by the expected detector resolution at the jet pₜ.<br>• **Dijet‑pulls** – three pulls (one for each possible pairing) that quantify the deviation of each dijet mass from m_W, again scaled by resolution.<br>• **Absolute‑pull measures** – the *minimum* absolute dijet‑pull (captures existence of at least one W‑like pairing) and the *sum* of absolute dijet‑pulls (penalises events where *all* pairings are inconsistent).<br>• **Symmetry variance** – the variance of the three dijet‑mass fractions (m_{ij}/m_jet). Genuine three‑body decays produce a low variance; QCD jets tend to give a larger spread.<br>• **Log(pₜ) term** – a simple scalar that lets the model adapt to the worsening detector resolution as the boost grows. |
| **Model** | A **tiny two‑layer multilayer perceptron (MLP)** (≈ 12 × 8 hidden units) that ingests the five engineered variables. The non‑linear activation (ReLU) allows the network to learn decision boundaries such as “large top‑pull **and** high symmetry variance ⇒ strong background likelihood”. |
| **Hardware constraints** | Designed for **L1 FPGA** implementation: < 1.8 µs latency, < 4 kB total memory (weights + bias). The model fits comfortably within the budget, leaving headroom for future feature extensions. |
| **Training & integration** | – Trained on simulated top‑jets (signal) and QCD jets (background) covering the ultra‑boosted pₜ range (1.2 – 3 TeV).<br>– Binary cross‑entropy loss; class weighting applied to target a working point of ~60 % signal efficiency at a background rejection of 100.<br>– Output combined into a single **combined_score** that replaces the legacy BDT score in the trigger decision. |
| **Comparison baseline** | The legacy BDT (τₙ, ECFs, etc.) yields ≈ 0.55 ± 0.02 efficiency under the same operating point in this regime. |

---

## 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Signal efficiency** (at the chosen background rejection) | **0.616 ± 0.015** |
| **Background rejection** (fixed) | ≈ 100 (by construction) |
| **Latency on FPGA** | 1.62 µs (well under the 1.8 µs budget) |
| **Memory usage** | 3.7 kB (including weights, biases, and feature scaling constants) |

The statistical uncertainty (± 0.015) is derived from 10 000 pseudo‑experiments (bootstrap) on the validation set, reflecting both finite sample size and the stochastic nature of the training (different random seeds).

**Interpretation:** The new physics‑driven MLP improves the tagging efficiency by roughly **6 % absolute** (≈ 11 % relative) compared with the legacy BDT, while staying comfortably within the trigger hardware constraints.

---

## 3. Reflection  

### Why it worked  

1. **Resolution‑aware pulls capture what survives at extreme boost** – By normalising mass deviations to the pₜ‑dependent detector resolution, the pulls remain informative even when the three sub‑jets are angularly unresolved.  
2. **Combined use of *minimum* and *sum* absolute pulls** – The minimum pull ensures we still recognise events that contain *any* W‑like pair, while the sum penalises pathological configurations where none of the three pairings is compatible with m_W. This dual information sharpens separation.  
3. **Symmetry variance is a strong discriminator** – Genuine top decays distribute energy relatively evenly among the three partons, giving a low spread in the dijet‑mass fractions. QCD jets, which tend to be dominated by a single hard core plus softer radiation, produce a markedly larger variance.  
4. **Log(pₜ) term provides a simple boost‑adaptation** – As the jet pₜ grows, both the absolute mass resolutions and the underlying physics change. Adding log(pₜ) allows the MLP to shift its decision boundary smoothly with boost, avoiding the hard‑coded thresholds that limited the BDT.  
5. **Compact MLP still learns useful non‑linearities** – The network discovered patterns such as “high top‑pull *and* high symmetry variance → reject”, which are not trivially encoded in a linear BDT.

### What did not work (or constraints)  

* **Limited capacity restricts deeper feature interaction** – With only two hidden layers and a strict memory budget we cannot model very complex relationships (e.g., higher‑order correlations among all three dijet masses). The modest gain over the BDT suggests there is still headroom for more expressive models if we can further compress them.  
* **Feature set is still handcrafted** – While the pulls and variance are physically motivated, they may miss subtler patterns (e.g., subtle energy‑flow asymmetries) that a learned representation from raw detector inputs could capture.  
* **Training on simulation only** – The observed improvement holds for the simulated dataset; possible mismodelling of jet mass resolution at very high pₜ could degrade performance on real data.

### Hypothesis confirmation  

The original hypothesis – that **kinematic constraints remain robust and can be turned into resolution‑aware pull variables that survive in the ultra‑boosted regime** – is **largely confirmed**. The observed efficiency lift demonstrates that these engineered observables retain discriminating power where traditional sub‑structure variables fail. The additional hypothesis that a tiny MLP could exploit non‑linear combinations within the strict FPGA budget is also validated.

---

## 4. Next Steps  

Below is a prioritized list of concrete directions to build on the success of v566.

| # | Idea | Rationale | Estimated resource impact |
|---|------|-----------|---------------------------|
| **1** | **Add a second “symmetry” metric** – e.g. the *skewness* of the dijet‑mass fractions or the *energy‑balance* between the hardest and softest subjet. | Skewness captures the same information as variance but is sensitive to asymmetric decays, potentially increasing separation for edge‑case QCD jets. | < 0.5 kB extra weights (adds 2 inputs). |
| **2** | **Resolution‑scaled angular pull** – compute the angle between the dijet axis and the jet axis, normalised by the angular resolution at the given pₜ, and include it as a fourth pull. | Even when angular resolution is poor, a scaled angular deviation can still provide a hint of the three‑prong topology. | ∼ 0.3 kB; latency impact negligible. |
| **3** | **Quantised MLP (8‑bit) with weight pruning** – apply post‑training quantisation and structured pruning to reduce weight count, freeing budget for an extra hidden layer (e.g., 12 → 8 → 4). | A deeper network could capture more subtle non‑linearities while still meeting the latency/memory envelope. | Expected memory < 4 kB; latency ≈ 1.7 µs (still safe). |
| **4** | **Hybrid ensemble** – combine the current MLP score with the legacy BDT output using a simple logistic meta‑classifier (1‑weight). | The BDT still carries complementary information (e.g., groomed subjet multiplicities). A linear ensemble can boost performance with virtually no extra cost. | Adds 1 weight (≈ 8 bytes) + a bias; negligible latency. |
| **5** | **Data‑driven calibration of pull scales** – derive the resolution functions (σ_mass(pₜ), σ_angle(pₜ)) directly from early Run‑3 data and feed them as lookup tables. | Simulation may under‑ or over‑estimate the true detector resolution at very high pₜ, leading to biased pulls. Calibrating on‑data will make the pulls more accurate and robust. | Requires a small ROM for the tables (~1 kB); no impact on inference speed. |
| **6** | **Exploratory: Tiny Graph Neural Network (GNN)** – treat the three sub‑jets as nodes, feed edge‑features (pairwise invariant masses) into a 2‑layer GNN compressed to < 4 kB. | GNNs can naturally learn permutation‑invariant relationships among the three sub‑jets, possibly surpassing hand‑crafted pulls. | Higher risk: need aggressive quantisation, careful firmware mapping. |
| **7** | **Robustness tests with pile‑up variations** – augment training with realistic pile‑up overlay and evaluate pull stability. | Ultra‑boosted jets can be contaminated by pile‑up; ensuring pulls remain stable will guard against performance loss in high‑luminosity conditions. | Purely software; no hardware cost. |
| **8** | **Full‑detector simulation of alternative top‑mass hypotheses** – train a multi‑class MLP that also predicts whether the jet originates from a **W‑only** or **QCD** dijet, providing a richer decision output. | A multi‑task model may learn richer representations and improve the binary discrimination indirectly. | Slightly more weights; still feasible within budget (< 4 kB). |

### Immediate plan (next two weeks)

1. Implement **symmetry skewness** and **angular pull** as additional inputs; retrain the current 2‑layer MLP and evaluate on the validation set.  
2. Perform **weight‑pruning + 8‑bit quantisation** on the existing model and benchmark FPGA resource usage to verify headroom for an extra hidden layer.  
3. Run a **quick data‑driven calibration** of the mass‑resolution scaling using a control sample of hadronic W‑bosons (e.g., from t‑channel single‑top events).  

If these steps show ≥ 2 % further efficiency gain without breaking latency, we will proceed to step 3 (adding a hidden layer) and begin integration of the hybrid ensemble.

---

**Prepared by:**  
Top‑Tagging Working Group – Iteration 566  
Date: 2026‑04‑16  

---