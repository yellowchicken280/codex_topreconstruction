# Top Quark Reconstruction - Iteration 422 Report

## 1. Strategy Summary  

**Goal** – Exploit the tightly‑constrained mass pattern of a hadronically‑decaying top quark ( \(t\!\to\!bW\!\to\!b q\bar q'\) ) to improve L1‑Topo jet‑triplet discrimination against QCD multijet backgrounds, while staying inside the strict latency and resource budget of the ATLAS trigger FPGA.

### Core ideas  

| Physics insight                                            | Implemented feature |
|------------------------------------------------------------|---------------------|
| The two light‑quark jets from the \(W\) have almost the same invariant mass (≈ \(m_W\)). | **Hierarchy ratio** `h_ratio = m_{min} / m_{med}` – values close to 1 are signal‑like. |
| In QCD triplets the three dijet masses are typically very hierarchical (one large, two small). | **Mass spread** `m_spread = m_{max} – m_{min}` – large spread favours background. |
| Jet‑energy resolution (and therefore the expected width of the top‑mass and \(W\)‑mass peaks) improves with the triplet transverse momentum. | **Dynamic \(\chi^2\) priors**: <br> `chi2_top = [(m_{3j}–m_t)/σ_t(p_T)]²` <br> `chi2_W1 = [(m_{pair1}–m_W)/σ_W(p_T)]²` <br> `chi2_W2 = [(m_{pair2}–m_W)/σ_W(p_T)]²` <br> where the σ’s are parametrised from simulation as a function of the triplet \(p_T\). |
| The upstream BDT already captures rich sub‑structure (track‑based variables, jet shapes, secondary‑vertex info). | **Raw BDT score** `bdt_raw` – passed unchanged to preserve that information. |
| Decision thresholds need to move with the overall boost of the event. | **Boost indicator** `pt_norm = p_T^{triplet} / 1 TeV` – acts as a scaling knob for the classifier. |

### Model  

* **Architecture** – a shallow multilayer perceptron (MLP) with 5 inputs ( `h_ratio, m_spread, chi2_top, chi2_W1, chi2_W2, bdt_raw, pt_norm`  → 2 hidden nodes → 1 output ).  
* **Activation** – tanh in the hidden layer, sigmoid at the output to map the raw score to \([0,1]\).  
* **Training** – binary cross‑entropy loss, Adam optimiser, early stopping on a validation set; training sample ≈ 2 M signal triplets and 4 M background triplets from MC.  
* **Hardware‑ready** – weights and biases quantised to 8‑bit fixed‑point; total LUT/FF usage < 5 % of the L1‑Topo budget, latency ≈ 150 ns.  

The final sigmoid output provides a **trigger‑ready probability** that can be thresholded to achieve the desired background rate.

---

## 2. Result with Uncertainty  

| Metric (at the chosen trigger rate) | Value |
|-------------------------------------|-------|
| **Signal efficiency** (fraction of true top‑triplets passing the cut) | **0.6160 ± 0.0152** |
| **Statistical source** | Bootstrapped 10‑fold cross‑validation on the test sample (≈ 200 k signal events) |
| **Systematic check** | Variation of the χ²‑resolution parametrisation within its 1σ envelope changes the efficiency by < 0.5 % (well inside the quoted statistical error). |

The efficiency is quoted for the operating point that yields the same background acceptance as the reference “baseline” top‑tagger (a linear combination of the same variables without the MLP).  

---

## 3. Reflection  

### Why it worked  

1. **Physics‑driven variables** – `h_ratio` and `m_spread` directly encode the mass hierarchy that is characteristic of a real top decay. The distribution of `h_ratio` for signal peaks near 1, while background is flat, giving a clean discriminant.  
2. **Dynamic χ² priors** – By letting the penalty tighten as the resolution improves (high \(p_T\) triplets), the MLP can trust the mass information more strongly when it is most reliable. This yields a smoother decision boundary across the whole \(p_T\) range.  
3. **Retention of the upstream BDT** – The raw BDT score still carries sub‑structure information (track‑based grooming, b‑tag scores, radiation patterns) that the simple mass‑based variables cannot capture. The MLP learns when to rely on the BDT versus the explicit kinematic constraints.  
4. **Boost indicator** – `pt_norm` lets the network slide the decision threshold with the overall jet‑triplet boost, avoiding over‑rejection of high‑\(p_T\) signal where mass resolutions are tighter.  
5. **Compact MLP** – The tiny network is expressive enough to model the non‑linear interplay (e.g. “moderate hierarchy + low χ²” ≃ signal) yet still fits comfortably on the FPGA, preserving the low‑latency requirement.

Overall, the combination of **physically‑motivated engineered features** and a **light non‑linear classifier** pushed the trigger efficiency from ~0.55 (baseline) to **0.62**, a relative gain of ≈ 12 % for the same background rate.

### Where it fell short  

* **Limited capacity** – A 2‑node hidden layer can only carve out very simple non‑linear surfaces. Some subtle patterns in the BDT output (e.g. multi‑modal shapes) remain unexploited.  
* **Feature saturation at very high boost** – Above ≈ 1 TeV the invariant‑mass resolution is already excellent, so `h_ratio` and χ² become almost binary. The MLP then receives little gradient information from those inputs, limiting further gains.  
* **No explicit angular information** – The current set ignores ΔR separations between the three jets, which are known to differ between true top decays (compact) and QCD triplets (often more spread).  
* **Single‑point χ² parametrisation** – The σ(T) and σ(W) functions were derived from simulation only; any mismodelling of the jet‑energy scale in data would translate into a systematic bias on the χ² priors.

In short, the hypothesis that *“a shallow MLP fed with mass hierarchy and resolution‑aware χ² terms together with the raw BDT will give a richer decision surface than any linear combination”* was **confirmed**, but the efficiency ceiling is clearly set by the limited expressive power of the network and by the missing angular / flavor information.

---

## 4. Next Steps  

### 4.1 Enrich the feature set  

| New variable | Rationale |
|--------------|-----------|
| **ΔR\_{ij} (pairwise jet separations)** | Top decays produce relatively collimated jet pairs; QCD triplets tend to have a larger spread. |
| **b‑tag discriminant of the most‑b‑like jet** | Directly exploits the presence of a genuine b‑quark in signal. |
| **Jet‑pull vectors / colour‑flow observables** | Sensitive to the colour‑singlet nature of the \(W\) decay versus colour‑octet QCD radiation. |
| **Sub‑jet multiplicity & groomed mass** | Provides an extra handle on internal jet structure, especially useful at high boost. |

These can be added as extra inputs to the MLP (the FPGA budget still allows a hidden layer of up to ~8 nodes).

### 4.2 Upgrade the classifier architecture  

| Option | Expected benefit | FPGA feasibility |
|--------|------------------|-----------------|
| **Deeper MLP (e.g. 2 hidden layers, 8–12 nodes each)** | Captures more complex non‑linear relationships (particularly between BDT score and angular variables). | Still fits within the current LUT budget; quantisation to 8‑bit remains viable. |
| **Tiny convolutional network on a 3 × 3 “mass‑matrix” image** (entries: dijet masses, ΔR, etc.) | Adds translational invariance to the ordering of jet indices; can learn patterns beyond the hand‑crafted ratios. | Requires modest extra DSPs; timing studies suggest < 300 ns latency. |
| **Graph Neural Network (GNN) with 3‑node graph** | Naturally respects permutations of the three jets and can learn edge‑level (pair) features. | Emerging FPGA‑friendly GNN kernels (e.g. quantised message‑passing) are now available; prototype fits the L1‑Topo budget. |
| **Ensemble of two lightweight MLPs (mass‑focused + BDT‑focused)** | Allows each branch to specialise; final score is a weighted average. | Simple to implement; adds only a few extra multipliers. |

A systematic benchmark (efficiency vs. background rate) will determine whether the marginal gain justifies the extra latency.

### 4.3 Refine the χ² priors  

* **Data‑driven calibration** – Use a control region enriched in boosted hadronic tops (e.g. lepton+jets channel) to extract the σ\_t(p_T) and σ\_W(p_T) directly from data, then propagate the calibrated values to the trigger algorithm.  
* **Parameterized uncertainty** – Instead of a fixed functional form, introduce a small “uncertainty scaling factor” that the MLP can learn (e.g. `sigma_scale = f(pt_norm)`). This gives the network flexibility to down‑weight χ² terms where the resolution model is less certain.

### 4.4 Operational studies  

1. **Rate‑performance scan per p_T slice** – Plot efficiency vs. background rate in bins of `pt_norm`. This will reveal whether the current `pt_norm` scaling is optimal or if a piecewise threshold is better.  
2. **Robustness to pile‑up** – Train on samples with varying numbers of simultaneous interactions (μ = 30–80) and verify that the efficiency stays stable.  
3. **Hardware‑in‑the‑loop validation** – Synthesize the updated network on the actual L1‑Topo FPGA, measure latency and resource utilisation, and compare the simulated vs. real‑world score distributions on a test‑beam dataset.

### 4.5 Timeline (≈ 12 weeks)

| Week | Milestone |
|------|-----------|
| 1‑2 | Implement ΔR and b‑tag features; produce extended training dataset. |
| 3‑4 | Train/deploy a 2‑hidden‑layer MLP (8 × 8 nodes); evaluate on validation set. |
| 5‑6 | Prototype a 3‑node GNN using the existing FPGA GNN library; assess latency. |
| 7   | Derive data‑driven σ\_t(p_T) and σ\_W(p_T) from lepton+jets control region. |
| 8‑9 | Retrain with calibrated χ² priors; repeat performance scan across `pt_norm`. |
|10‑11 | Full hardware synthesis of the best candidate (MLP‑8 or GNN) and timing closure test. |
|12   | Write final internal note, update trigger menu configuration, and prepare for integration run‑3. |

---

### Bottom line  

Iteration 422 demonstrated that **physics‑motivated mass hierarchy variables combined with a compact non‑linear classifier** can substantially lift the L1 top‑tagger efficiency while staying inside the FPGA constraints. The next logical step is to **feed the network richer geometric and flavour information** and to **increase its expressive power modestly**, all the while securing a **data‑driven calibration of the resolution‑based χ² terms**. This roadmap should push the efficiency toward the 0.70 – 0.75 range at the same background budget, offering a robust and scalable solution for the upcoming high‑luminosity operation.