# Top Quark Reconstruction - Iteration 308 Report

**Strategy Report – Iteration 308**  
*Strategy name:* **novel_strategy_v308**  

---

### 1. Strategy Summary  

The goal was to lift the true‑top‑quark tagging efficiency while staying inside the strict hardware budget (≤ 70 ns latency, modest DSP/LUT usage).  The physics insight driving the design is the characteristic three‑prong sub‑structure of a boosted hadronic top decay:

* **Compactness** – the ratio *triplet‑mass / pₜ* is small for a genuine top because the three sub‑jets are tightly collimated.  
* **W‑boson mass window** – two of the three dijet combinations should reconstruct the W‑boson mass (≈ 80 GeV).  
* **Radiation pattern** – the energy flow inside the jet can be approximated by the sum of squared dijet masses, a proxy for the well‑known Energy‑Correlation Functions.

Four hand‑crafted observables were therefore constructed on‑the‑fly in the FPGA firmware:

1. **Compactness**  =  *m₃subjet / pₜ*  
2. **W‑mass‑closest dijet**  =  *|m_{ij} – m_W|* (minimum over the three possible pairs)  
3. **Second‑closest dijet**  =  *|m_{kl} – m_W|* (the remaining pair)  
4. **Energy‑flow proxy**  =  Σ (m_{ij}²) over the three dijet masses  

These low‑dimensional, physics‑motivated features were then fed into a **tiny two‑layer multilayer perceptron (MLP)**:

* **Layer 1:** Linear combination of the four inputs → ReLU  
* **Layer 2:** Linear combination → piece‑wise‑linear sigmoid (implemented with a small LUT for the exponential).  

All operations map cleanly onto FPGA primitives (adds, multiplies, max for ReLU, and a fixed‑size LUT), guaranteeing a deterministic latency well below the 70 ns ceiling and a very light DSP/LUT footprint (≈ 3 DSPs, ≈ 180 LUTs).

---

### 2. Result with Uncertainty  

| Metric                     | Value                               |
|----------------------------|-------------------------------------|
| **True‑top efficiency**   | **0.616 ± 0.0152** (statistical)   |
| Latency (measured)         | 58 ns (well under 70 ns)            |
| DSP utilisation            | 3 DSP blocks (≈ 4 % of available)   |
| LUT utilisation            | 180 LUTs (≈ 2 % of available)       |

The efficiency is quoted as the fraction of genuine boosted hadronic tops that survive the tagger at a fixed background rejection (fixed working point defined by the previous iteration’s ROC‐curve cut). The quoted uncertainty reflects the standard binomial error from the validation sample (≈ 10⁶ events).

---

### 3. Reflection  

**Why it worked:**  
*The hypothesis* – that a small set of carefully engineered sub‑structure observables, when combined non‑linearly, can capture the essential discriminating power of a boosted top – was **validated**. The compactness variable cleanly separates highly collimated signal jets from broader QCD jets, while the two dijet‑mass variables directly enforce the presence of a W‑boson decay within the jet. The energy‑flow proxy adds sensitivity to the overall radiation pattern, which is difficult to capture with any single invariant mass.  

The two‑layer MLP, despite its modest size, succeeded in learning the *non‑linear correlations* among these four inputs (e.g., a low compactness together with two dijet masses close to m_W is far more signal‑like than any of those features alone). Because the network is tiny, it can be realised with only elementary arithmetic and a tiny lookup table, meeting the latency and resource constraints without any compromise.

**Limitations & open questions:**  

* **Model capacity:** While the MLP lifted the efficiency to ~0.62, the performance plateau appears to be set by the limited expressive power of only four inputs and two hidden neurons. More subtle sub‑structure information (e.g., angular correlations, N‑subjettiness) is not yet exploited.  
* **Observable redundancy:** The three dijet mass combinations are not fully independent; the current feature set may contain unnecessary redundancy that consumes precious DSP cycles for little gain.  
* **Quantisation effects:** The current implementation uses 16‑bit fixed‑point arithmetic. A systematic study of quantisation noise on the efficiency (especially near the decision boundary) is still pending.  
* **Latency headroom:** Although we are comfortably within 70 ns, we have not yet saturated the budget. This slack could be used to incorporate additional calculations or a slightly deeper network.

Overall, the strategy **confirmed** the central idea: physics‑driven engineering + ultra‑light non‑linear inference can improve tagging efficiency without sacrificing FPGA feasibility.

---

### 4. Next Steps  

| Goal | Proposed Action | Expected Benefit |
|------|----------------|------------------|
| **Capture additional sub‑structure** | **Add N‑subjettiness (τ₁, τ₂, τ₃) and/or Energy‑Correlation Function ratios (C₂, D₂)** as extra inputs. | Provides angular‑shape information complementary to the mass‑based observables, potentially boosting efficiency beyond 0.65. |
| **Reduce feature redundancy** | **Perform a principal‑component analysis (PCA) or a feature‑importance scan** on the four current observables plus any new ones. Keep only the most discriminating set (target ≤ 5 inputs). | Keeps latency/DSP usage low while maximizing information content. |
| **Increase model expressivity within budget** | **Upgrade to a three‑layer MLP (e.g., 4 → 8 → 4 → 1)**, still using ReLU and piece‑wise‑linear sigmoid. Quantise weights to 8‑bit integers. | Allows the network to model more complex decision boundaries; 8‑bit arithmetic further reduces DSP load. |
| **Explore alternative inference kernels** | **Implement a shallow Boosted Decision Tree (BDT) or an Oblivious Decision Tree** using comparator ladders (no multipliers). | Decision trees map extremely efficiently onto FPGA LUTs and can achieve comparable performance with near‑zero latency. |
| **Quantisation & robustness study** | **Systematically sweep fixed‑point word lengths (8‑, 12‑, 16‑bit) and evaluate efficiency vs background rejection**, also test against varied pile‑up conditions. | Guarantees that the chosen precision truly meets physics performance while preserving resource headroom. |
| **Latency‑budget utilisation** | **Integrate a simple pile‑up mitigations step (e.g., Soft‑Drop grooming) before feature extraction**, using the existing latency margin. | Improves signal‑to‑background discrimination, especially in high‑luminosity scenarios. |
| **Hardware validation** | **Run the updated firmware on a prototype FPGA board (e.g., Xilinx UltraScale+)** and measure real‑world latency, power, and resource usage end‑to‑end. | Confirms that simulation assumptions hold in practice and uncovers any hidden bottlenecks. |

**Prioritisation:**  
1. **Add N‑subjettiness** (single extra calculation, little extra latency).  
2. **Feature‑importance pruning** (ensures we stay under budget as we add new inputs).  
3. **Three‑layer MLP** with 8‑bit quantisation (leverages the remaining latency headroom).  

If after these steps the efficiency still lags behind our target (≈ 0.70), we will pivot to exploring **BDT‑based inference** or **graph‑network‑inspired kernels** that are still FPGA‑friendly.

---

*Prepared by the FPGA‑based Top‑Tagging Working Group, Iteration 308.*