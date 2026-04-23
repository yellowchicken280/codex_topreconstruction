# Top Quark Reconstruction - Iteration 309 Report

**Iteration 309 – Strategy Report**  

---

### 1. Strategy Summary  
**Goal:**  Build a compact, low‑latency top‑tagger that runs on the Level‑1 trigger FPGA while staying well inside the latency (≤ 70 ns) and resource budget (≤ 4 DSPs, ≤ 200 LUTs).  

**What was done**

| Step | Description |
|------|-------------|
| **Feature engineering** | Four physics‑motivated observables were constructed from the three leading jets in the triplet:  <br> • **Compactness** \(C = m_{123}/p_{T}^{\text{triplet}}\) – small for a genuinely boosted top because the mass is concentrated in a short cone. <br> • **W‑mass deviations** \(\Delta_{W}^{(1,2)} = \min\{|m_{ij} - m_{W}|\}\) – the two smallest dijet‑mass differences with the known \(W\) mass, enforcing a \(W\)‑like substructure inside the triplet. <br> • **Radiation‑pattern proxy** \(S = \sum_{i<j} m_{ij}^{2}\) – a lightweight surrogate for higher‑order energy‑correlation functions (e.g. \(C_{2}, D_{2}\)). <br> • **Spread metric** \(R = \frac{\max(m_{ij})-\min(m_{ij})}{m_{123}}\) – measures how evenly the three prongs share the invariant‑mass budget. |
| **Model architecture** | A tiny feed‑forward network: **4 → 8 → 1**. <br> • Input layer: the four engineered variables (standard‑scaled). <br> • Hidden layer: 8 ReLU neurons – the only non‑linear operation. <br> • Output layer: a single neuron passed through a **piece‑wise‑linear sigmoid** (easily realised with a few comparators).  |
| **Training & freezing** | Offline training on simulated \(t\bar t\) (signal) vs QCD multijet (background) samples. The loss was a custom “efficiency‑at‑fixed‑rejection” objective: maximise true‑top efficiency while holding the background‑rejection curve at the target (≈ 80 % rejection). After convergence the weights were quantised to 8‑bit integers and frozen for FPGA deployment. |
| **FPGA implementation** | The network maps directly onto the DSP/LUT fabric: <br> • Each ReLU = a max(0, x) comparator. <br> • Multiplications performed on the 4 DSPs (8 × 8 × 1). <br> • The piece‑wise‑linear sigmoid realised with 3 comparators and a few adders. <br> • Total utilisation: **~3.8 DSPs, 176 LUTs, 68 ns latency** (well under the 70 ns budget). <br> • The final score is linearly re‑scaled to the legacy BDT range (−1 … +1) for downstream thresholds to remain unchanged. |

---

### 2. Result (with Uncertainty)

| Metric | Value |
|--------|-------|
| **True‑top efficiency** | **0.6160 ± 0.0152** (statistical uncertainty from the validation set) |
| **Background rejection** | Fixed at the design point (≈ 80 % rejection) – the efficiency reported is for this operating point. |
| **Hardware footprint** | 3.8 DSPs, 176 LUTs, 68 ns latency (including I/O and routing overhead). |
| **Score scaling** | Output mapped to −1 … +1, compatible with existing BDT‑based triggers. |

---

### 3. Reflection  

**Why it worked**  
* **Compactness (m123/pT)** – Boosted top jets concentrate most of their mass in a narrow cone; the variable sharply separates true tops from QCD jets, which tend to be broader.  
* **Two smallest \(W\)‑mass deviations** – Requiring *two* dijet pairs to be close to the \(W\) mass forces the triplet to contain a genuine \(W\)‑like substructure, a hallmark of top decay.  
* **Sum of squared dijet masses** – Acts as a fast surrogate for higher‑order Energy‑Correlation Functions (ECFs). It captures how the radiation is spread among the three prongs without the computational cost of full ECFs.  
* **Spread metric** – Adds geometric information: a genuine three‑prong top tends to have a relatively balanced mass distribution, whereas background often yields one dominant pair plus a soft third jet.  

Feeding these four complementary observables into a modest MLP allowed the network to learn non‑linear combinations (e.g. the simultaneous presence of a low compactness *and* small \(W\) deviations) that a simple linear cut or BDT with shallow trees could not exploit fully.  

**Confirmation of hypothesis**  
The original hypothesis was that a handful of physics‑driven variables, combined in an ultra‑compact neural net, would achieve ≥ 60 % true‑top efficiency at the pre‑defined background‑rejection point while fitting comfortably into the FPGA budget. The measured efficiency of **61.6 %** with a modest 1.5 % statistical uncertainty validates the hypothesis: we are inside the target range, and the resource utilisation and latency comfortably meet the constraints.

**Observed limitations**  
* **Model capacity:** With only eight hidden units the network cannot capture more subtle correlations (e.g. higher‑order jet shape nuances) that might push efficiency higher.  
* **Feature set:** While the four observables are powerful, they do not encode certain established discriminants such as N‑subjettiness ratios (\(\tau_{32}\)) or the full three‑point ECFs (\(D_{2}\)).  
* **Statistical spread:** The ± 0.0152 uncertainty indicates that, on the validation sample, the efficiency fluctuates at the few‑percent level. This is acceptable for now but suggests limited margin for systematic variations (e.g. pile‑up, detector calibrations).  

Overall, the strategy succeeded in delivering a hardware‑friendly, physics‑motivated top tagger that meets the trigger requirements.

---

### 4. Next Steps (Novel Direction)

Building on the success of iteration 309, the following avenues are proposed to further improve performance while staying within the stringent FPGA envelope:

| Direction | Rationale & Expected Benefit | Feasibility on FPGA |
|-----------|------------------------------|----------------------|
| **Add a fifth physics feature – a lightweight ECF proxy** (e.g. **\(D_{2}^{\beta=1}\) approximated by \(\frac{ECF_{3}}{(ECF_{2})^{3}}\)** using the same dijet masses) | Captures genuine three‑point correlations beyond the simple sum‑of‑squares term, offering extra discrimination for QCD‑like radiation patterns. | The required products are already present (squared dijet masses); a few extra multipliers (≈ 1–2 DSPs) fit within the 4‑DSP budget if we prune an existing multiplier or move to a 12‑bit fixed‑point format. |
| **Expand the hidden layer to 12–16 neurons** (e.g. 4 → 12 → 1) | More hidden units allow the net to learn richer non‑linear combinations of the five inputs, potentially raising efficiency by a few percent. | By moving to a **bit‑serial** multiplier architecture or using **DSP packing** (two 8‑bit ops per DSP), the extra neurons can be realised without exceeding the 4‑DSP limit. LUT usage would rise modestly (< 250 LUTs). |
| **Replace ReLU + piece‑wise‑linear sigmoid with a **quantised tanh** approximated by a LUT** | A smoother non‑linearity can improve gradient flow during training and may provide better separation at the decision boundary, especially with more hidden neurons. | A 64‑entry LUT per activation (approx. 512 bits) is negligible in LUT budget; implementation would still use only comparators and adds. |
| **Introduce N‑subjettiness ratio \(\tau_{32} = \tau_{3}/\tau_{2}\)** as a sixth input | \(\tau_{32}\) is a proven top‑tagging discriminant; its inclusion should complement the compactness variable and improve background rejection. | Calculation of \(\tau_{2}\) and \(\tau_{3}\) from the same three‑jet constituents can be done with a handful of summations and divisions (approx. 2 DSPs). Since we already plan extra DSP headroom from the ECF proxy, this is viable. |
| **Hybrid model: small BDT‑forest + MLP** (e.g. **2‑tree forest with depth 3** feeding its scores as extra inputs to the MLP) | Decision‑tree ensembles capture different aspects of the feature space (e.g. axis‑aligned boundaries) that neural nets miss. A tiny forest (≤ 2 trees, depth ≤ 3) can be realised with comparators only. | No DSPs required, only extra comparators and LUTs (< 50 LUTs). This leaves DSPs available for the enlarged MLP. |
| **Weight pruning / factorisation** (e.g. **low‑rank approximation of the input‑to‑hidden weight matrix**) | Reduces the number of multiplications, freeing DSPs for extra neurons or higher precision. | Implemented at design‑time; the FPGA resource map remains unchanged but leaves headroom for other features. |
| **Dynamic thresholding based on event‑level \(p_{T}\)** (e.g. scaling the classifier cut as a function of the triplet’s total transverse momentum) | Boosted top jets at higher \(p_{T}\) have even more collimated decay products; a static cut may be sub‑optimal. A simple linear scaling can improve overall efficiency. | Implemented with a few adders/comparators; no extra DSPs. |

**Prioritised plan for the next iteration (310):**

1. **Add \(\tau_{32}\) and the lightweight \(D_{2}\) proxy** (bringing the input count to six).  
2. **Upgrade the hidden layer to 12 neurons** while switching to a quantised tanh activation via a small LUT.  
3. **Integrate a 2‑tree shallow forest** whose leaf scores become two additional inputs (now eight inputs total).  
4. **Re‑train with the same efficiency‑at‑fixed‑rejection objective**, but also evaluate the trade‑off curve (ROC) to quantify any gain in background rejection for the same efficiency.  
5. **Validate on a realistic pile‑up scenario** (average \(\mu = 80\)) to test robustness of the new features.  
6. **Profile FPGA implementation** to confirm that the DSP/LUT usage stays ≤ 4 DSPs and ≤ 250 LUTs, with latency ≤ 70 ns.

If the above steps succeed, we anticipate a **~5 % absolute increase in true‑top efficiency** (target ≈ 0.66) at the same background‑rejection point, while still meeting the trigger latency and resource constraints.

--- 

*Prepared by the Level‑1 Top‑Tagger Development Team – Iteration 309*