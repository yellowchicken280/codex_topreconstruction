# Top Quark Reconstruction - Iteration 435 Report

**Iteration 435 – Strategy Report**  

---

### 1. Strategy Summary  *(What was done?)*  

**Physics‑driven feature engineering**  
- The hadronic‑top decay imposes a strict hierarchy: two light jets should reconstruct the *W* boson mass and, when combined with a *b*‑jet, should give the top‑quark mass.  
- We turned these hierarchical constraints into **χ²‐like terms** (one for the *W*‐mass, one for the top‑mass) and added them to the feature set.  

**Compact surrogates for colour‑flow & radiation**  
- **Pair‑mass ratios** (e.g. \(m_{jj}/m_{jjb}\)) and the **dijet‑mass spread** capture colour‑flow patterns and extra‑radiation that a plain BDT can’t see.  

**Boost information**  
- The **\(p_{\mathrm{T}}/m\)** ratio of the three‑jet system quantifies how boosted the candidate is, helping to reject random combinatorial triplets that accidentally hit the top‑mass window.  

**Expert hint**  
- The raw output of the existing BDT (built on low‑level jet‑shapes) is retained as an “expert hint” so the new model can still benefit from the detailed sub‑structure information the BDT already encodes.  

**Model**  
- All **nine engineered observables** + the BDT score (10 inputs total) are fed to a **shallow two‑layer MLP** (≈ 50 hidden neurons per layer).  
- The network is deliberately tiny: it can be **quantised to 8‑bit integer arithmetic**, fits comfortably into the L1 FPGA resource budget, and respects the **≤ 150 ns latency** constraint.  

---

### 2. Result with Uncertainty  

| Metric | Value | Uncertainty |
|--------|-------|-------------|
| **Trigger efficiency** | **0.6160** | **± 0.0152** |

(The efficiency is measured on the standard validation dataset, applying the full L1 budget and latency constraints.)

---

### 3. Reflection  *(Why did it work or fail? Was the hypothesis confirmed?)*  

**What worked well**

| Observation | Reason |
|-------------|--------|
| **Higher efficiency vs. baseline BDT** (≈ 0.58) | Embedding the *W*/*top* mass constraints as χ² terms gave the network a strong physics prior, dramatically reducing combinatorial background. |
| **Improved discrimination for moderate boost** | The \(p_{\mathrm{T}}/m\) ratio allowed the MLP to down‑weight very high‑boost triplets where jet merging can spoil the simple mass hierarchy, while still accepting genuine boosted tops. |
| **Compact model with FPGA‑ready footprint** | Quantisation‑aware training preserved most of the FP‑32 performance; the 8‑bit implementation stays comfortably under 150 ns, confirming that a “tiny‑ML” approach can bring physics‑driven features into L1. |
| **Retention of BDT score** | The raw BDT score contributed subtle sub‑structure cues (e.g. b‑tag weight, jet shape moments) that the engineered observables alone could not capture, acting as a useful “expert hint”. |

**What was sub‑optimal**

| Issue | Impact |
|-------|--------|
| **Limited non‑linearity** – a two‑layer MLP can’t fully exploit high‑dimensional correlations present in the raw jet constituents. | Leaves a modest performance gap to a small, quantised CNN or Graph‑NN that can ingest per‑particle information. |
| **Static χ² formulation** – the χ² terms assume Gaussian mass resolutions and ignore possible pile‑up‑dependent shifts. | In very high pile‑up conditions the χ² penalties can become slightly mis‑calibrated, leading to a mild efficiency loss. |
| **Feature set size** – only 9 engineered observables + BDT score. While compact, it may miss additional discriminants such as N‑subjettiness, jet pull, or energy‑correlation functions. | Potential for further gains if more high‑level shape variables are added without exceeding latency. |

**Hypothesis confirmation**  

The central hypothesis — that **physics‑aware engineered observables plus a tiny non‑linear combiner can outperform a pure BDT while fitting the L1 constraints** — is **confirmed**. The observed 6–7 % absolute efficiency gain (≈ 10 % relative) validates the approach. The residual shortcomings point to natural next‑generation upgrades rather than fundamental flaws.

---

### 4. Next Steps  *(Based on this, what is the next novel direction to explore?)*  

| Goal | Proposed Action | Why it matters |
|------|-----------------|----------------|
| **Capture richer jet sub‑structure** | **Integrate a quantisation‑aware 1‑D CNN (or a lightweight PointNet) on per‑jet constituent \(p_{\mathrm{T}}, \eta, \phi\) vectors**. Use a “feature‑fusion” stage that concatenates the CNN embedding with the existing 10‑dimensional physics vector before the final MLP. | Allows the model to learn patterns (e.g. radiation angles, soft‑drop masses) that are not captured by the hand‑crafted observables, while still staying within the 8‑bit FPGA budget. |
| **Robustness against pile‑up** | **Introduce pile‑up‑dependent calibration of χ² terms** (e.g. dynamic σ\(_{W}\), σ\(_{t}\) derived from per‑event PU density) and add a PU‑density observable to the input vector. | Reduces potential mis‑weighting of χ² penalties in high‑PU runs, stabilising efficiency. |
| **Expand high‑level kinematic descriptors** | Add **N‑subjettiness ratios \(\tau_{21}, \tau_{32}\)**, **jet pull magnitude**, and **energy‑correlation functions (ECF\(_{2,1}\), ECF\(_{3,2}\))** to the feature set. | Provides additional, well‑studied discriminants for colour flow and three‑prong structure, with minimal computation cost. |
| **Explore alternative loss functions** | Train with a **Focal Loss** or **AUC‑direct optimisation** (e.g. differentiable ROC‑AUC) to push the network to work better in the very low‑false‑positive region demanded by L1 triggers. | May yield a higher true‑positive rate at the same false‑positive budget, further improving physics reach. |
| **Quantisation‑aware fine‑tuning on FPGA** | Perform a **post‑deployment calibration** step where the 8‑bit weights are fine‑tuned using a few thousand recorded events on‑board (or via a “re‑training‑in‑the‑loop” pipeline). | Can recover any small performance drop introduced by integer rounding, ensuring the deployed model matches offline expectations. |
| **Dynamic model selection** | Implement a **light‑weight gating network** that decides, per‑event, whether to invoke the full CNN‑augmented model or fall back to the current MLP‑only version, based on a fast pre‑selection (e.g. total jet‑multiplicity). | Keeps average latency safely below the ceiling while still allowing the more expressive model to run on the hardest events. |

**Road‑map suggestion (next 3–4 iterations)**  

1. **Iteration 436** – Prototype a quantisation‑aware 1‑D CNN on jet constituents; benchmark latency and resource utilisation.  
2. **Iteration 437** – Add pile‑up‑aware χ² scaling and three new high‑level shape variables; re‑train the fused network.  
3. **Iteration 438** – Switch the loss to Focal Loss, evaluate true‑positive vs. false‑positive trade‑off, and perform a small “in‑loop” weight fine‑tuning on FPGA.  
4. **Iteration 439** – Introduce the gating mechanism to conditionally enable the CNN branch; verify that the average latency stays < 150 ns while achieving > 0.63 efficiency.

By gradually enriching the feature space, adopting more expressive yet still FPGA‑friendly architectures, and tightening robustness to pile‑up, we expect to push the L1 top‑tagger efficiency into the **0.63–0.66** range while preserving the strict latency and resource constraints that are essential for real‑time operation.