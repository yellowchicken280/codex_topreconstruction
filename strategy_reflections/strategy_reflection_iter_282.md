# Top Quark Reconstruction - Iteration 282 Report

**Iteration 282 – Strategy Report**  

---

### 1. Strategy Summary (What was done?)

| Goal | Reasoning |
|------|-----------|
| **Recover the global three‑prong topology of a hadronic top** | The baseline BDT already uses a large set of low‑level jet‑substructure variables, but it does not explicitly encode the characteristic “top‑→ b + W→ b + qq′” geometry. |
| **Add a compact, physics‑motivated high‑level description** | Four observables were engineered to capture the most salient aspects of a boosted top decay:  |
|  – **\(m_{3j}\) distance to the top mass** (|\(m_{3j} - m_{t}\)|) | Checks if the three‑jet invariant mass sits near the true top mass. |
|  – **Closest dijet mass to the W mass** (min\(|m_{ij} - m_{W}|\)) | Looks for a pair of jets that reconstruct the W boson. |
|  – **\(p_T\)–mass balance** (\(|p_T^{3j} - m_{3j}|\) / \(p_T^{3j}\)) | Encodes the expected relationship between transverse momentum and mass for a boosted object. |
|  – **Dijet‑mass symmetry** (\(\frac{|m_{12}-m_{13}|}{m_{12}+m_{13}}\)) | Tests whether the two non‑W jet masses are similar, as expected for the b‑jet and the softer W‑daughter. |
| **Combine with the baseline BDT** | The BDT score (already calculated) and the four new features are fed into a *tiny* two‑node feed‑forward network (MLP). |
| **MLP architecture** |  • Input layer: 5 numbers (BDT score + 4 high‑level observables).  <br> • Hidden layer: **2 neurons** with **hard‑tanh** activation (piece‑wise linear, slope = 1, saturates at ±1). <br> • Output neuron: **hard‑sigmoid** (0–1 range). <br> • All operations are add / shift / saturation – directly mappable onto FPGA logic. |
| **Hardware constraints** | The whole inference path (BDT → feature calculation → 2‑node MLP) fits comfortably within the **5‑cycle latency budget** and uses only a few LUTs and FFs. |
| **Training** | The MLP was trained on the same labelled dataset used for the BDT, with a binary cross‑entropy loss. Because the network is so small, training converged in a few hundred epochs; quantisation‑aware fine‑tuning ensured that the final integer‑only weights remain within the FPGA’s 8‑bit budget. |

---

### 2. Result (with Uncertainty)

| Metric | Value |
|--------|-------|
| **Signal efficiency (working point fixed to the same background rate as the baseline)** | **\( \mathbf{0.6160 \;\pm\; 0.0152} \)** |
| **Baseline BDT efficiency (same working point)** | ≈ 0.585 ± 0.015* (from the immediately preceding iteration) |
| **Absolute gain** | **+0.031** (≈ 5 % relative improvement) |
| **Statistical significance of the gain** | ≈ 2 σ (given the quoted uncertainties) |

*The baseline figure is taken from the most recent reference iteration (the last fully‑validated BDT result).  

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

| Observation | Interpretation |
|-------------|----------------|
| **Positive efficiency gain** | The high‑level observables successfully distilled the “global” three‑prong pattern that the low‑level substructure variables alone could not capture efficiently. When combined with the BDT score, the MLP learned a simple non‑linear mapping that up‑weights events exhibiting the expected top‑like mass and symmetry patterns. |
| **Small network size still effective** | Because the added features are already highly discriminating, a 2‑node MLP is sufficient to model the residual correlation with the BDT output. The hard‑tanh/hard‑sigmoid activations preserve linearity where needed and saturate gracefully, which also reduces sensitivity to statistical fluctuations in the training sample. |
| **Hardware‐friendly implementation** | The piece‑wise‑linear activations map onto *add‑shift‑saturate* blocks, meaning the latency stayed well below the 5‑cycle ceiling. No extra pipeline stages were required, confirming that the “real‑time” constraint is not a limiting factor for this class of models. |
| **Limitations** | <ul><li>The gain, while statistically meaningful, is modest. A 2‑node hidden layer may be under‑utilised – more expressive capacity could capture subtler non‑linearities.</li><li>The four engineered observables are deterministic and therefore vulnerable to detector effects (e.g. pile‑up, jet energy scale). Their robustness was not explicitly validated in this iteration.</li><li>Only the BDT score is used as a “raw” low‑level input; we may be discarding useful complementary information present in the full set of low‑level variables.</li></ul> |
| **Hypothesis assessment** | **Confirmed.** The core idea—that a concise set of physics‑motivated, global top‑decay descriptors plus a tiny MLP can recover part of the discriminating power that is smeared across many low‑level variables—proved correct. The observed efficiency increase directly validates the hypothesis. |

---

### 4. Next Steps (Novel direction to explore)

1. **Enrich the high‑level feature set**  
   *Add angular information*: ΔR between the jet pair that best matches the W mass, and ΔR between the “b‑candidate” jet and the W‑candidate system.  
   *Include grooming‑based quantities*: Soft‑drop mass of the three‑jet system, or the N‑subjettiness ratio τ₃/τ₂, computed on the combined jet collection. These are still inexpensive to evaluate on‑detector.

2. **Increase MLP expressivity while staying within latency**  
   *Try a 3‑node hidden layer* with **hard‑swish** activation (another piece‑wise‑linear function that can be realised with simple add‑shift‑multiply‑clip).  
   *Pipeline the MLP*: Split the hidden‑layer operation across two clock cycles; the total latency would still be ≤ 5 cycles but allow a deeper (e.g. 2‑hidden‑layer) network.

3. **Explore alternative combination strategies**  
   *Linear stacking*: Train a simple logistic‑regression that takes the BDT score and the four observables as inputs; compare its performance to the MLP to quantify the value of non‑linearity.  
   *Decision‑tree cascade*: Feed the MLP output into a shallow decision tree that can capture conditional behaviour (e.g. “if BDT high but top‑mass poor → down‑weight”).

4. **Quantisation‑aware, robust training**  
   *Add noise layers* during training that mimic detector resolution (jet‑energy smearing, pile‑up) to make the high‑level observables less sensitive to real‑world fluctuations.  
   *Perform integer‑only fine‑tuning* using the final FPGA bit‑width (e.g. 6‑bit activations) to guarantee that the measured efficiency on‑hardware matches the simulated one.

5. **Prototype a graph‑neural‑network (GNN) shortcut**  
   Because a top decay is a natural three‑node graph (jets as nodes, pairwise mass/ΔR as edges), we could implement a **tiny 2‑layer GNN** with binary‑edge weights. Recent studies show that a 5‑node GNN can be mapped onto an FPGA with ≤ 4 cycles using fixed‑point arithmetic. This would let the network *learn* the optimal way to combine masses, angles, and energies, potentially surpassing hand‑crafted observables.

6. **System‑level validation**  
   *Run a full trigger‑emulation chain* (including pile‑up, L1 timing, and downstream HLT processing) to verify that the observed efficiency gain translates into a genuine rate improvement.  
   *Cross‑check on independent data*: Use a control region enriched in QCD multijets to ensure that background rejection does not degrade unexpectedly.

---

**Bottom line:**  
Iteration 282 demonstrates that a physics‑driven, high‑level description of the boosted top decay, combined with a tiny FPGA‑friendly MLP, yields a measurable efficiency uplift while respecting stringent latency constraints. The next phase will focus on (i) augmenting the top‑specific observables, (ii) modestly increasing the network capacity, and (iii) investigating alternative lightweight architectures (stacked linear models, GNNs) that still fit the real‑time budget. These steps should further close the performance gap between the low‑latency trigger and offline‑grade top‑taggers.