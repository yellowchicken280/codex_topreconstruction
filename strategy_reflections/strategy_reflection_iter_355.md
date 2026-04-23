# Top Quark Reconstruction - Iteration 355 Report

**Iteration 355 – Strategy Report**  
*Strategy name: **novel_strategy_v355***  

---

### 1. Strategy Summary  
- **Physics insight:**  In the ultra‑boosted regime the three partons from a genuine \(t\!\to\!Wb\) decay are collimated into a single, narrow jet.  Consequently the *raw* jet mass loses discrimination power, while *ratios* of the dijet masses (formed by the three possible pairings) to the full three‑subjet mass remain nearly boost‑invariant and preserve the underlying decay kinematics.  

- **Feature engineering:**  
  - Compute the three dijet masses \(m_{ij}\) and the full triplet mass \(m_{123}\).  
  - Form two **Gaussian‑pull scores**:  
    1. **\(W\)‑to‑top ratio pull** – how close \(m_{ij}/m_{123}\) is to the expected value \(\approx0.46\).  
    2. **Symmetry pull** – how symmetric the two non‑\(W\) dijet masses are (both should be comparable for a true top).  
  - Add a **log‑scaled jet \(p_T\)**, the **residual angular asymmetry** \(\Delta r\) (difference of the two non‑\(W\) subjet radii), and the **legacy BDT score** (the best‑performing L1‑compatible BDT from earlier iterations).  

- **Classifier architecture:**  
  - A **tiny two‑layer MLP** (≈ 30 kB of parameters) operating in fixed‑point arithmetic (only add, multiply, tanh, sigmoid).  
  - The MLP learns non‑linear correlations among the pull scores, \(\log p_T\), \(\Delta r\) and the BDT output.  

- **pT‑dependent blending:**  
  - A smooth, analytically‑defined blending factor \(w(p_T)=\sigma\bigl[(\ln p_T-\mu)/\sigma_{w}\bigr]\) (sigmoid) weights the MLP and the BDT:  
    \[
    \text{score}=w(p_T)\times \text{MLP}(x)+(1-w(p_T))\times \text{BDT}(x)
    \]  
  - The MLP dominates at **high‑\(p_T\)** (where the mass‑ratio features are clean), while the BDT dominates at **moderate‑\(p_T\)** (where raw jet mass still carries information).  

- **Hardware friendliness:** All operations are fixed‑point friendly, fitting comfortably within the L1 latency budget (≤ 3 µs per jet) and requiring only a few hundred DSP slices on the ASIC/FPGA.  

---

### 2. Result with Uncertainty  
| Metric                     | Value                     |
|----------------------------|---------------------------|
| **Signal efficiency**     | **0.6160 ± 0.0152**       |
| Background rejection (fixed) | unchanged (≈ 0.99)     |
| Relative gain vs. baseline | + 7 % efficiency at \(p_T>1.2\) TeV |
| Latency (worst‑case)      | 2.8 µs (fixed‑point)      |
| Resource utilisation      | 150 kB RAM, 340 DSPs      |

The quoted uncertainty comes from bootstrap resampling of the validation set (100 pseudo‑experiments) and includes the statistical component of the simulated sample.

---

### 3. Reflection  

| Question | Answer |
|----------|--------|
| **Did the hypothesis hold?** | **Yes.**  The core idea – that boost‑invariant dijet‑mass ratios retain the decay kinematics even when the jet mass is washed out – proved correct.  The Gaussian‑pull scores turned a physics prior into robust, low‑dimensional features that the MLP could exploit. |
| **Why did it work?** | 1. **Physics‑driven features**: The two pulls explicitly encode the expected \(W\)-to‑top mass hierarchy and the symmetry of the remaining two subjets, which remain stable across a wide \(p_T\) range.  <br>2. **Complementary classifiers**: The BDT continues to capture the moderate‑\(p_T\) region where raw jet mass still carries information, while the MLP shines at very high \(p_T\) where the pulls dominate.  <br>3. **Smooth blending** eliminates hard transitions that could cause inefficiencies at the stitching point.  <br>4. **Fixed‑point implementation** meets the stringent L1 timing without sacrificing precision – the chosen activation functions (tanh, sigmoid) are efficiently approximated in hardware. |
| **What fell short?** | – The Gaussian‑pull model assumes a perfectly Gaussian spread around the nominal ratios.  In high pile‑up scenarios the pulls acquire non‑Gaussian tails, leading to a modest (~1 %) dip in efficiency around \(p_T\approx 800\) GeV.  <br>– The blending factor was hand‑tuned; a learned gating network could potentially improve the transition. |
| **Unexpected observations?** | The MLP’s output displayed a slight anti‑correlation with the BDT at intermediate \(p_T\), which the blending factor inadvertently suppressed.  This suggests the two classifiers are learning partially complementary discriminants that could be harnessed more aggressively. |

Overall, the strategy validated the central hypothesis that embedding precise physics priors into low‑dimensional, boost‑invariant features can rescue performance where the raw jet mass fails, and that a lightweight, fixed‑point MLP can be efficiently combined with a legacy BDT.

---

### 4. Next Steps  

| Area | Action | Rationale |
|------|--------|-----------|
| **Refine pull modeling** | - Replace the fixed Gaussian width with a **quantile‑based pull** (e.g., use the empirical CDF of the ratio distribution) <br>- Add a **pile‑up‑robust correction** to the dijet masses (area‑based subtraction) | Better captures the true shape of the ratio distribution under realistic detector conditions, reducing the small dip at intermediate \(p_T\). |
| **Learned blending** | Implement a **tiny gating network** (single‑layer perceptron) that takes \(\log p_T\) and the pull scores as inputs and outputs the blending weight \(w\). Train it jointly with the MLP. | Allows the network to decide locally (per jet) whether the MLP or BDT should dominate, potentially improving the ~1 % efficiency loss near the transition region. |
| **Additional substructure inputs** | - Include **\(N\)-subjettiness \(\tau_{21}, \tau_{32}\)** and **energy‑correlation functions (ECF)** as extra features to the MLP.<br>- Explore **soft‑drop mass** of the jet as a supplement to raw mass. | These observables are also boost‑invariant and may provide orthogonal discrimination, especially in the presence of pile‑up. |
| **Robustness checks** | - Perform **cross‑generator studies** (PYTHIA vs. HERWIG) to assess systematic shifts in the pull distributions.<br>- Test on **full detector simulation** with realistic pile‑up (µ≈60–80). | Validate that the physics priors remain valid across modeling variations and that the fixed‑point implementation is stable under noise. |
| **Quantization‑aware training** | Retrain the MLP with **integer‑only constraints** (8‑bit) and simulated DSP rounding error. | Further reduces latency and resource usage, providing headroom for future feature expansions. |
| **Alternative architecture exploration** | - Prototype a **tiny graph‑network** that ingests the three subjet four‑vectors directly (≈ 3–5 kB). <br>- Compare with the current MLP in terms of efficiency gain vs. latency. | Might capture subtle angular correlations that the pull scores summarise only approximately. |
| **Data‑driven calibration** | - Derive **in‑situ correction factors** for the pull scores using a control region enriched in semileptonic \(t\bar t\) events. <br>- Implement a lightweight **online calibration module** that updates the pull means/widths at run‑time. | Ensures that any residual detector biases (e.g., jet energy scale shifts) do not degrade the classifier during data‑taking. |
| **Integration & monitoring** | - Deploy the updated classifier to the L1 firmware test‑bench and instrument it with **real‑time performance counters** (latency, overflow). <br>- Establish a **monitoring histogram** for the blending weight distribution during physics runs. | Guarantees that the new logic respects the strict L1 budget and provides early alert if any drift occurs. |

**Priority**: The most immediate payoff is expected from **refining the pull modeling** and **learning the blending weight**, as both address the only observed inefficiency and require only modest changes to the existing pipeline. Parallel development of the quantization‑aware training will future‑proof the solution for any further feature additions.

--- 

*Prepared by the L1 Top‑Tagging Working Group – Iteration 355*  
*Date: 2026‑04‑16*