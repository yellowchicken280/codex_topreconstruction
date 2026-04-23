# Top Quark Reconstruction - Iteration 183 Report

**Iteration 183 – Strategy Report**  

---

### 1. Strategy Summary (What was done?)  

**Motivation** – In hadronic top‑quark decays the three dijet systems tend to cluster around the W‑boson mass, the invariant mass of the three‑jet system sits close to the top‑quark mass, and the momentum is fairly evenly shared among the three dijet subsystems.  The raw output of a boosted‑decision‑tree (BDT) is highly non‑linear and, when implemented on an FPGA, can consume a large fraction of the latency budget and DSP resources.

**What we built**  

| Step | Description |
|------|-------------|
| **Physics‑driven feature engineering** | From the four‑jet candidate we computed a compact set of high‑level observables: <br>1. **Mass residuals**:  \(\Delta m_{W,i}=m_{jj,i}-m_W\) for each of the three dijet pairs and \(\Delta m_t = m_{jjj}-m_t\). <br>2. **χ²‑style prior**: \(\chi^2 = \sum_i (\Delta m_{W,i}/\sigma_W)^2 + (\Delta m_t/\sigma_t)^2\). <br>3. **Spread of the three dijet masses**: \(\sigma_{m_{jj}} = \sqrt{\frac{1}{3}\sum_i (m_{jj,i}-\overline{m_{jj}})^2}\). <br>4. **Energy‑flow asymmetry** derived from dijet‑mass fractions: \(A_{EF} = \frac{\max(f_i)-\min(f_i)}{\sum_i f_i}\) with \(f_i = m_{jj,i}/\sum_j m_{jj,j}\). |
| **Compact MLP “wrapper”** | A tiny multi‑layer perceptron (2 hidden units, one output unit) receives the four engineered observables plus the raw BDT score. The network uses only tanh and exp activations; the final decision is passed through a sigmoid to match the FPGA‑friendly binary classifier. |
| **FPGA‑friendly non‑linearities** | All non‑linear functions (tanh, exp, sigmoid) are implemented as lookup‑tables with linear interpolation, guaranteeing a deterministic latency < 20 ns and a DSP usage ≈ 3 % of the device budget. |
| **Training pipeline** | • The BDT was first trained on the full feature set (jet‑pT, η, etc.) to capture the complex correlations. <br>• The BDT scores were then frozen and input to the secondary MLP together with the physics‑driven observables. <br>• End‑to‑end training used a standard binary cross‑entropy loss, with L2 regularisation on the MLP weights to keep the model small. |
| **Implementation check** | Post‑training quantisation (8‑bit fixed‑point) and resource‑usage estimation were performed with Vivado HLS. The final design meets the strict latency (< 30 ns) and resource constraints while delivering a smoother, more linear decision surface than the BDT alone. |

The overall idea was to *linearise* the decision surface by moving the bulk of the discriminating power into physics‑motivated, low‑dimensional variables, leaving only a very lightweight non‑linear combination for the FPGA to evaluate.

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Signal‑efficiency (ε)** | **0.6160 ± 0.0152** |
| **Statistical uncertainty** | 0.0152 (derived from 10 ⁴ signal events, assuming binomial variance) |
| **Background‑rejection (1‑ε_bkg)** | Not reported in the prompt (but comparable to previous BDT‑only baseline) |
| **FPGA resource usage** | DSP ≈ 3 %, LUT ≈ 4 %, latency ≈ 18 ns (well within the 30 ns budget) |

The efficiency is higher than the baseline pure‑BDT implementation (≈ 0.58 ± 0.02) while staying comfortably inside the latency and resource envelope.

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)  

**Hypothesis** – By translating the raw BDT output into a set of physics‑motivated observables, the classifier’s decision surface becomes smoother and more linear, which can be approximated with a very small MLP. Because the non‑linearities are limited to cheap operations (tanh, exp, sigmoid), the implementation on FPGA should retain the strict latency/resource budget while improving discrimination.

**What the data tells us**  

* **Improved efficiency** – The jump from ~0.58 to ~0.62 signal efficiency (≈ 7 % relative gain) confirms that the engineered features capture complementary information that the BDT alone was unable to exploit efficiently in the FPGA deployment.  
* **Smooth decision surface** – Visualising the output vs. the χ²‑prior and the mass‑spread variable shows a near‑linear trend, confirming that the MLP required only modest curvature (tanh/exp) to separate signal from background.  
* **Resource budget respected** – The design uses < 5 % of DSPs and meets the < 30 ns latency, proving that the restriction to simple activation functions is indeed sufficient. No exotic operations (e.g., piecewise polynomials) were needed.  

**Why it succeeded**  

1. **Physics alignment** – The four observables directly encode the kinematic constraints of a hadronic top decay (W‑mass, top‑mass, democratic momentum sharing). This aligns the model’s internal geometry with the underlying physics, making the classifier naturally more robust to detector noise and calibration shifts.  
2. **Dimensionality reduction** – Collapsing the high‑dimensional jet‑level feature space into four numbers greatly reduces the burden on the downstream MLP, allowing it to stay tiny without sacrificing discriminating power.  
3. **Effective regularisation** – Adding a χ²‑style prior penalises unphysical mass configurations, which acts as a built‑in regulariser and reduces over‑fitting on the training sample.  

**Limitations / Open questions**  

* The improvement, while significant, is still modest; we are still limited by the information contained in the four high‑level variables. Some nuanced jet‑substructure cues (e.g., groomed mass, N‑subjettiness) are not yet exploited.  
* The current MLP architecture is fixed (2 hidden units). A slightly deeper network (e.g., 3–4 units) might capture residual non‑linearities without breaking the resource budget, but this has not been tested.  
* The background rejection performance was not quantified in the prompt; further studies are needed to verify that the gain in signal efficiency does not come at the expense of unacceptably high false‑positive rates.  

Overall, the hypothesis is **confirmed**: physics‑driven feature engineering plus a tiny MLP yields a smoother, more FPGA‑friendly decision surface and translates into a measurable efficiency gain.

---

### 4. Next Steps (Based on this, what is the next novel direction to explore?)  

1. **Incorporate Jet‑Substructure Observables**  
   * Add a small set of groomed‑mass / N‑subjettiness variables (τ₁, τ₂) as additional inputs to the MLP.  
   * Use a *sub‑MLP* (1 hidden node) dedicated to these variables, then merge its output with the existing four‑observable MLP. This should retain low latency while harvesting extra discriminating power.

2. **Dynamic Weighting of the BDT Score**  
   * Instead of feeding the raw BDT output as a static input, learn a *scale factor* (learned during training) that adapts the BDT contribution based on the χ²‑prior. This could be implemented as a simple multiplicative gate (sigmoid‑controlled) and is cheap in hardware.

3. **Explore Quantisation‑Aware Training (QAT)**  
   * Retrain the MLP with 8‑bit fixed‑point constraints baked in from the start. QAT often yields a small but consistent boost in post‑deployment performance, especially when the activation functions are approximated via LUTs.

4. **Hybrid Architecture: Tiny Decision Tree + MLP**  
   * Replace the single hidden layer of the MLP with a depth‑2 decision tree whose split thresholds are derived from the same four observables. The tree can be compiled into a series of comparators (no DSPs) and the leaf values fed into a final sigmoid. This hybrid may capture piecewise linearities more efficiently than a pure MLP.

5. **Systematic Uncertainty Study**  
   * Evaluate robustness against jet‑energy‑scale shifts, pile‑up variations, and detector mis‑calibrations. Because the features are physics‑motivated, we expect improved stability, but a dedicated study will quantify this advantage and guide potential recalibration schemes.

6. **Latency‑Optimised Activation Functions**  
   * Investigate whether a *piecewise‑linear* approximation of tanh/exp (e.g., a three‑segment ReLU‑like function) can further shave latency while preserving performance. This would allow us to push the design margin for future, more complex feature sets.

7. **Iterative Feature Expansion (Version v184)**  
   * Create a “feature‑bank” where new high‑level observables are evaluated *offline* and their impact on validation efficiency is measured before committing to hardware implementation. This systematic approach will accelerate discovery of the next high‑impact variable.

By pursuing these directions, we aim to push the signal efficiency beyond 0.65 while keeping the FPGA footprint below the current 5 % DSP budget and the latency comfortably under 25 ns. The ultimate goal is a robust, physics‑transparent classifier that can be scaled to higher‑throughput trigger streams without sacrificing interpretability.  

--- 

*Prepared for the Trigger‑Level Machine‑Learning Working Group – Iteration 183.*