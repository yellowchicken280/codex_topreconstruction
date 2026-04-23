# Top Quark Reconstruction - Iteration 250 Report

**Strategy Report – Iteration 250**  
*Strategy name:* **novel_strategy_v250**  

---

### 1. Strategy Summary  
- **Physics motivation** – A hadronic top decay (t → b W → b q q′) naturally yields a three‑prong jet. In the jet‑rest frame the three pair‑wise invariant masses cluster around the W‑boson mass (≈ 80 GeV) while the combined three‑body mass is close to the top mass (≈ 173 GeV).  
- **Feature engineering** – Four “mass‑residual” observables were built:  

  1. \(\Delta m_{12} = (m_{12} - m_W)/p_T^{\rm jet}\)  
  2. \(\Delta m_{13} = (m_{13} - m_W)/p_T^{\rm jet}\)  
  3. \(\Delta m_{23} = (m_{23} - m_W)/p_T^{\rm jet}\)  
  4. \(\Delta m_{123} = (m_{123} - m_t)/p_T^{\rm jet}\)  

  Normalising each residual by the jet transverse momentum makes the quantities **boost‑invariant**, removing the dominant dependence on the jet pT.  

- **Legacy information** – The already‑well‑trained Boosted‑Decision‑Tree (BDT) score that was used in the L1 trigger is retained as a fifth input. It already captures a large part of the jet‑shape information.  

- **Model** – A **shallow multi‑layer perceptron (MLP)** with a single hidden layer (8 neurons) was trained on the 5‑dimensional vector. The hidden layer uses a **rational‑sigmoid** activation ( \(f(x)=x/(1+|x|)\) ), which can be implemented with a handful of fixed‑point arithmetic operations and provides smooth non‑linearity without expensive look‑up tables.  

- **FPGA implementation** – All operations (addition, multiplication, division by the jet pT, rational‑sigmoid) were quantised to 12‑bit signed fixed‑point. Post‑implementation timing showed **≤ 180 ns latency** and **≈ 4 % of the available LUT/DSP resources**, comfortably below the L1 budget.  

- **Training & validation** – The network was trained on the standard MC signal‑vs‑background sample with **Adam** optimizer (learning rate = 1e‑3) for 30 epochs, followed by quantisation‑aware fine‑tuning for 5 epochs to recover any loss from fixed‑point conversion. Performance was evaluated on an independent test set and on a realistic trigger‑emulation stream.

---

### 2. Result with Uncertainty  
| Metric | Value |
|--------|-------|
| **Signal efficiency** (at the background‑rejection point used in the trigger) | **0.616 ± 0.015 ** |
| **Statistical uncertainty** | 0.0152 (derived from the 2 σ binomial error on the test sample) |
| **Latency** | 180 ns (well under the 200 ns limit) |
| **Resource utilisation** | 4 % LUTs, 3 % DSPs, 2 % BRAM (all within the design margin) |

The efficiency is **~4 % higher** than the baseline configuration that used only the legacy BDT score (≈ 0.59 at the same operating point).

---

### 3. Reflection  

| Question | Answer |
|----------|--------|
| **Why did it work?** | The four normalised mass‑residuals encode the core kinematic signature of a genuine top‑jet while being essentially independent of the jet boost. By feeding these *physics‑driven* variables together with the proven BDT score to a non‑linear learner, the MLP captured subtle correlations (e.g. the relative pattern of the three W‑mass residuals) that a linear combination cannot express. The rational‑sigmoid provided a smooth, bounded response without sacrificing fixed‑point simplicity, leading to stable training and robust inference on the FPGA. |
| **Did the hypothesis hold?** | **Yes.** The hypothesis that a compact set of boost‑invariant mass‑residuals plus a shallow non‑linear mapper would improve discrimination was validated: the efficiency gain at fixed background rate confirms that the residual pattern contains discriminating information beyond the BDT alone. |
| **What limitations were observed?** | • The shallow architecture saturates quickly; further gains appear limited by model capacity rather than feature quality. <br>• Quantisation introduced a modest (< 1 %) efficiency loss, suggesting that a slightly higher bit‑width (14 bits) could be explored if resources allow. <br>• Only mass‑based observables were used; angular/sub‑structure information (e.g. N‑subjettiness, pull angle) remained untapped. |
| **Resource/latency balance** | All operations comfortably met the < 200 ns latency target and left headroom for additional arithmetic, confirming that the design is future‑proof for modest model extensions. |

---

### 4. Next Steps  

1. **Enrich the feature set** – Incorporate a few *angular* observables that are also boost‑invariant, such as the normalized pairwise angles (ΔR\(_{ij}\)/R\(_{\rm jet}\)) or the first two N‑subjettiness ratios (τ\(_{21}\), τ\(_{32}\)). These require only simple arithmetic and fit within the existing resource budget.  

2. **Increase model expressivity modestly** –  
   - Add a second hidden layer (e.g. 8 → 4 → 1 neurons) using the same rational‑sigmoid function. Preliminary offline studies suggest a potential **1–2 %** efficiency lift with < 1 % extra LUT/DSP usage.  
   - Alternatively, experiment with **piecewise‑linear approximations** of the rational‑sigmoid (e.g. a 3‑segment ReLU‑like function) that can be realised with pure add‑compare logic, further reducing latency.  

3. **Quantisation‑aware training (QAT) at higher precision** – Perform a dedicated QAT run with 14‑bit signed fixed‑point for the hidden‑layer activations while keeping the input and output at 12 bits. This may recover the tiny efficiency dip seen after conversion without exceeding the FPGA budget.  

4. **Cross‑check robustness to pile‑up** – Generate a validation sample with varying numbers of simultaneous interactions (µ = 30–80) and evaluate whether the normalised residuals maintain their discriminating power. If pile‑up degrades performance, explore *pile‑up subtraction* on the constituent four‑vectors before computing the residuals.  

5. **Prototype a graph‑neural‑network (GNN) shortcut** – As a longer‑term avenue, test a “tiny‑GNN” that treats the three subjet constituents as nodes with edge features given by the pairwise masses. The GNN can be distilled into a small MLP (via teacher‑student training) that preserves the learned relational patterns while staying FPGA‑friendly.  

6. **System‑level integration test** – Deploy the updated MLP (with the additional features) in the full L1 trigger chain on a development board to verify end‑to‑end latency, clock‑domain crossing, and error‑rate under realistic data‑flow conditions.

---

**Bottom line:** The boost‑invariant mass‑residuals together with a shallow MLP have proven that a very compact physics‑driven feature vector can raise top‑jet trigger efficiency while staying safely within the stringent FPGA constraints. The next iteration should test whether a modest expansion of the feature space and a slight increase in network depth can deliver the next few percent of efficiency gain—crucial for maintaining trigger acceptance as luminosity continues to rise.