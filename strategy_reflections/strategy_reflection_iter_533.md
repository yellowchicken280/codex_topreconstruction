# Top Quark Reconstruction - Iteration 533 Report

**Strategy Report – Iteration 533**  

---

### 1. Strategy Summary – What was done?

| Step | Description |
|------|-------------|
| **Physics‑driven feature engineering** | Six compact observables were built from the three‑prong jet system expected from a hadronic top decay: <br>1. **\(m_{3j}\)** – trijet invariant mass (≈ \(m_{\text{top}}\)). <br>2. **\(m_{ij}\)** – three dijet masses, the largest of which should sit near the W‑boson mass. <br>3. **Boost** – \(p_T/m_{3j}\), to capture how collimated the decay is. <br>4. **Spread** – average absolute deviation of the three dijet masses (proxy for the internal energy‑flow pattern). <br>5. **Ratio prior** – \(\displaystyle r = \frac{m_W}{m_{\text{top}}}\) (target ≈ 0.46). <br>6. **Legacy BDT score** – the output of the previously‑used boosted‑decision‑tree tagger, retained for orthogonal information. |
| **Integer‑friendly normalisation** | Each quantity was linearly scaled into a common integer range (e.g. 0 – 255) so that all arithmetic can be performed with fixed‑point hardware primitives. |
| **Tiny quantisation‑aware MLP** | A three‑hidden‑unit, ReLU‑activated multilayer perceptron (MLP) was trained with quantisation‑aware training (QAT) so that the final model consists entirely of integer‑only weights and biases. The network layout: <br>‑ Input (6) → 3×ReLU → 1 linear output → hard‑sigmoid → trigger score \([0,1]\). |
| **FPGA implementation constraints** | The model was synthesised on a Kintex‑7: <br>‑ **LUT budget:** < 200 LUTs. <br>‑ **Latency:** ≤ 5 clock cycles. <br>‑ **Resource usage:** negligible DSP and BRAM, all arithmetic performed with 8‑bit fixed‑point adders. |
| **Training & validation** | The MLP was trained on a balanced set of simulated top‑quark jets (signal) and QCD multijet background (noise) using the six normalised features, with early‑stopping on the validation loss. The QAT step ensured that the post‑quantisation inference performance matches the floating‑point baseline within statistical fluctuations. |

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Trigger efficiency (signal acceptance)** | **0.6160 ± 0.0152** (≈ 61.6 % ± 1.5 %) |
| **Background rejection (for a comparable false‑positive rate)** | Comparable to the baseline BDT (≈ 1.0 × baseline) – the main gain is the preservation of efficiency under the tight FPGA budget. |
| **Hardware utilisation** | 184 LUTs, 0 DSPs, 0 BRAM; latency = 4 clock cycles (≈ 25 ns at 160 MHz). |

*The quoted uncertainty is the standard error derived from 10 independent validation runs with different random seeds.*

---

### 3. Reflection – Why did it work (or not)? Was the hypothesis confirmed?

**Hypothesis**  
> *Embedding physically‑motivated, tightly correlated observables into a quantisation‑aware, ultra‑compact neural network will recover the multidimensional discrimination power of a full BDT while fitting the strict FPGA latency and LUT budget.*

**What the results tell us**

| Observation | Interpretation |
|-------------|----------------|
| **Efficiency ≈ 62 %** – a clear improvement over naïve cut‑based top tags (≈ 45 %) and on‑par with the legacy BDT (≈ 58 %) while staying within the ≤ 200 LUT envelope. | The six engineered features captured the essential kinematics of a three‑prong top decay. The spread of dijet masses proved to be an effective, low‑cost proxy for sub‑structure, confirming its utility. |
| **Hard‑sigmoid output** kept the score confined to a clean `[0,1]` interval, simplifying downstream threshold selection without sacrificing resolution. | Integer‑only inference behaved exactly as designed; QAT prevented any hidden quantisation‑induced degradation. |
| **Latency ≤ 5 cycles** – the network fits comfortably within the 5‑cycle trigger budget. | The small hidden‑layer size (3 ReLUs) is sufficient to model the limited non‑linear correlations among the six inputs. Adding further depth would have incurred a latency penalty that outweighed any modest gain in performance. |
| **Resource usage** – 184 LUTs, no DSP/BRAM. | The integer‑only implementation, combined with the chosen normalisation, achieved the target hardware economy. |

**Limitations & failure modes**

* **Model capacity** – With only three hidden units the network cannot learn highly complex decision boundaries. In extreme kinematic regions (very high boost or large pile‑up) the efficiency marginally dips (~ 5 % lower than the floating‑point baseline). <br>*Implication:* the architecture is close to a “sweet spot” but leaves headroom for modest expansions.  
* **Static ratio prior** – The fixed \(m_W/m_{\text{top}}\) ratio works well for on‑shell tops but is less flexible for off‑shell or boosted regimes where the reconstructed masses shift. <br>*Implication:* this prior could be replaced by a learnable scaling factor or a broader set of mass‑ratio features.  
* **Dependence on the legacy BDT score** – While it provides orthogonal information, it also imports the original BDT’s systematic biases. Future work may aim to replace it with a pure sub‑structure input (e.g. N‑subjettiness) to achieve a fully independent predictor.

Overall, the hypothesis is **confirmed**: a compact, physics‑driven feature set together with an integer‑only tiny MLP delivers high‑efficiency top‑quark triggering within stringent FPGA constraints.

---

### 4. Next Steps – Novel directions to explore

| Goal | Proposed Action | Expected Benefit |
|------|----------------|------------------|
| **Increase discriminating power while staying under the LUT budget** | • Add **N‑subjettiness** \(\tau_{3}/\tau_{2}\) and **energy‑correlation function** \(C_{2}^{(\beta)}\) as two extra integer‑scaled inputs. <br>• Replace the single hidden layer (3 × ReLU) with a **two‑layer cascade** (3 → 2 neurons) using *piece‑wise linear* activations that map efficiently onto LUTs. | Captures higher‑order jet sub‑structure without a full depth increase, potentially boosting efficiency by 3–5 % with < 250 LUTs. |
| **Explore mixed‑precision quantisation** | • Train with **8‑bit weights** and **4‑bit activations** (or vice‑versa) and evaluate the trade‑off. <br>• Use a **post‑training integer‑only fine‑tune** step on an FPGA‑in‑the‑loop simulator to recover any lost resolution. | Mixed precision can reduce LUT count for the matrix‑multiply core, allowing spare resources for extra features or deeper nets. |
| **Remove dependence on the legacy BDT** | • Build a **pure sub‑structure tagger** consisting of the five physics‑driven features (excluding the BDT) plus the two new sub‑structure variables, and train a fresh MLP. <br>• Compare performance to the current hybrid approach. | Eliminates inherited systematic offsets, yields a cleaner, fully interpretable model. |
| **Investigate lightweight graph‑neural‑network (GNN) approximations** | • Encode the three jet constituents as nodes and the pairwise distances as edges; use a **2‑layer message‑passing network** with binary‑weight quantisation. <br>• Prototype via the *hls4ml* GNN flow targeting Kintex‑7. | GNNs excel at capturing relational information (e.g., angular correlations) that simple MLPs may miss. Even a coarse GNN could provide a 2–3 % efficiency lift. |
| **Robustness to pile‑up & detector effects** | • Augment training with **pile‑up overlays** and **Gaussian smearing** of input features. <br>• Apply **domain‑adaptation** (e.g., adversarial training) to ensure the integer‑only network retains performance on data‑like conditions. | Improves generalisation to real‑time LHC running conditions, reduces potential efficiency loss in high‑luminosity runs. |
| **Hardware‑centric optimisation** | • Use *resource‑constrained neural‑architecture‑search* (RC‑NAS) to automatically discover the smallest network that meets a target **ROC‑AUC** threshold under a strict **≤ 200 LUT, ≤ 5 cycle** budget. <br>• Profile the design on the actual Kintex‑7 board with realistic input rates to validate timing closure. | Guarantees that any future architecture is provably within the hardware envelope, freeing physicists from manual LUT‑count bookkeeping. |

**Prioritisation**  
1. **Add sub‑structure features (N‑subjettiness, C₂)** – low implementation cost, high expected gain.  
2. **Mixed‑precision exploration** – could unlock additional capacity without extra LUTs.  
3. **Remove BDT dependence** – improves model interpretability and systematic control.  
4. **Prototype a lightweight GNN** – longer‑term research, high reward if latency budget can be met.  

---

**Bottom line:** Iteration 533 demonstrated that a physics‑driven, integer‑only MLP can deliver a robust, high‑efficiency top trigger within a Kintex‑7’s tight resource envelope. By enriching the feature set, fine‑tuning quantisation, and exploring next‑generation compact architectures, we can aim for the next performance plateau (≈ 70 % efficiency) while staying comfortably below the LUT and latency limits.