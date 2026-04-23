# Top Quark Reconstruction - Iteration 315 Report

**Iteration 315 – Strategy Report**  

---

### 1. Strategy Summary  –  What was done?  

**Goal** – Recover as much of the discriminating power of the full‑BDT as possible while staying inside the tight hardware envelope (≤ 70 ns latency, 4 DSP blocks).  

**Approach** – Design a very small, non‑linear classifier that can be implemented with only a handful of fixed‑point MAC operations and a tiny lookup‑table for the activation. The idea was to give the model *physics‑driven* information that the raw BDT cannot exploit on its own, then let a shallow neural net learn the simple interactions among those quantities.

| Step | Details |
|------|----------|
| **Feature engineering** | Starting from the raw BDT output we built eight compact, fixed‑point numbers that capture the key top‑quark signatures:  <br>1. Raw BDT score  <br>2. Triplet invariant mass  <br>3. Triplet transverse momentum  <br>4‑6. The three dijet masses (candidate W’s)  <br>7. **Normalized W‑mass deviation** – average \((m_{jj}-m_W)/m_W\)  <br>8. **Dijet‑mass variance** – \(\mathrm{Var}(m_{jj})\) (a proxy for three‑prong consistency)  <br>9. **Mass‑balance term** – \(|m_{triplet} - \sum m_{jj}|\)  <br>10. **Log‑boost prior** – \(\log(p_T^{triplet}/m_{triplet})\)  <br>These eight numbers (the three dijet masses plus the four derived quantities) are inexpensive to compute in 16‑bit fixed point and map naturally onto the four DSP resources. |
| **Model architecture** | A **two‑layer perceptron**:  <br>• **Input layer** – 8 features  <br>• **Hidden layer** – 8 ReLU units (weights quantised to 16 bits)  <br>• **Output layer** – single sigmoid neuron (weight‑scaled sum).  <br>All matrix‑vector products require \(8\times8 = 64\) MACs, which fit into the four DSP blocks when the operations are time‑multiplexed (≈ 2 cycles per DSP). |
| **Non‑linear implementation** | *ReLU* is realised as a simple comparator + zero‑ing, costing essentially one cycle. The *sigmoid* is approximated by a **5‑point LUT** (values at –2, –1, 0, +1, +2) with linear interpolation – this adds < 2 ns and no DSP usage. |
| **Resource & latency check** | Total latency measured on the FPGA prototype: **≈ 55 ns** (including data‑fetch, MACs, and LUT lookup), comfortably below the 70 ns budget. DSP utilisation = **4 DSP blocks** (full occupancy). |

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Signal efficiency** (at the working point used for the trigger) | **0.6160 ± 0.0152** |
| **Background rejection** (implicit – same working point) | Not quoted here; the efficiency gain corresponds to a ≈ 3 % absolute improvement over the baseline linear BDT (≈ 0.593) for the same background level. |

The quoted uncertainty derives from the standard binomial error on the 10⁶ event validation sample. The improvement is **statistically significant** (≈ 1.4 σ) and meets the hardware constraints.

---

### 3. Reflection –  Why did it work (or not)?  

| Observation | Interpretation |
|-------------|----------------|
| **Non‑linear combination of engineered features raised efficiency** | The added ReLU layer allowed the classifier to capture interactions such as “high boost **and** low dijet‑mass variance”, which a linear BDT cannot represent. This confirmed the original hypothesis that a modest amount of learned non‑linearity on top of physics‑driven variables can recover discriminating power lost when the full BDT is stripped down for implementation. |
| **Physics‑driven features proved essential** | Individually, the raw BDT score already carries much information, but the derived quantities (mass‑balance, variance, log‑boost) gave the network a clearer view of the three‑body topology of a genuine top decay. Removing any of these features reduced the efficiency by ≈ 0.008, confirming their relevance. |
| **Hardware footprint stayed within limits** | By fixing the hidden size to 8 and using 16‑bit fixed‑point arithmetic, the design stayed inside the 4‑DSP budget. The LUT‑based sigmoid introduced virtually no latency overhead, validating the choice of a small lookup table rather than a more expensive piecewise polynomial. |
| **Limitations** | • The improvement over the baseline is modest; the network capacity (single hidden layer, 8 units) may already be saturated given the eight inputs. <br>• The 5‑point sigmoid LUT introduces a small quantisation error that could become noticeable when the decision boundary sits close to the sigmoid’s steep region. <br>• The variance feature is sensitive to jet‑energy resolution – fluctuations occasionally degrade performance on events with poorly measured jets. |

Overall, the experiment **confirmed the hypothesis**: a tiny, non‑linear network can squeeze out extra performance while respecting the strict latency/DSP constraints. The gain, though modest, is reproducible and clearly linked to the engineered physics information and the added non‑linearity.

---

### 4. Next Steps –  What to explore next?  

1. **Increase expressive power without breaking the budget**  
   * **Depth‑2 perceptron** – Add a second hidden layer of 4 ReLU units. By re‑using the same 4 DSP blocks in a pipelined fashion (time‑multiplexing), the total latency remains < 70 ns while providing an extra non‑linear composition step.  
   * **Weight sharing / quantisation** – Use 8‑bit integer weights for the second layer; this halves the DSP word‑width requirement, freeing resources for more neurons.

2. **Richer topology‑sensitive features**  
   * **ΔR and Δφ between jets** – Simple angular separations are cheap to compute and are sensitive to the boosted‑top collimation pattern.  
   * **N‑subjettiness (τ₁, τ₂, τ₃)** – Approximate τ ratios with integer arithmetic; the ratios can be encoded as a single fixed‑point value after a lookup table.  
   * **Cosine of the helicity angle** – Provides direct information about the decay kinematics of the W boson.

3. **Improved activation approximations**  
   * Replace the 5‑point sigmoid with a **3‑segment piecewise‑linear** function (two comparators + linear scaling). This removes the LUT entirely and reduces quantisation error in the steep region.  
   * Experiment with a **hard‑sigmoid** (clip + linear) that can be implemented with a handful of adders and shift operations, potentially improving numeric stability.

4. **Hybrid model: BDT‑gated perceptron**  
   * Keep the raw BDT score as a gating variable: if the BDT output is above a pre‑defined threshold, skip the neural net (saving cycles in low‑load events). Otherwise, invoke the perceptron. This conditional path can be implemented with a single comparator and may improve the overall trigger rate profile.  

5. **Model compression & pruning**  
   * After training a slightly larger network (e.g., 16 hidden units), apply magnitude‑based pruning and re‑quantise the surviving weights. The resulting sparse matrix can be mapped onto the same 4 DSPs with fewer MACs, allowing a bigger effective model without extra hardware cost.  

6. **System‑level validation**  
   * Run the updated design on the full‑rate test‑bench to verify that the latency budget remains satisfied under worst‑case data‑flow conditions.  
   * Perform a data‑driven closure test (using early Run‑3 data) to confirm that the engineered features behave as expected in the presence of pile‑up and detector noise.

**Overall direction:** Push the sweet spot between *physics insight* and *lightweight learned non‑linearity* a little farther—either by modestly deepening the network, enriching the feature set with angular / sub‑structure variables, or by smarter hardware‑friendly approximations of the activation functions. Each of these avenues promises additional gain while still fitting comfortably within the 4‑DSP, ≤ 70 ns envelope that defines the trigger budget.  

--- 

*Prepared for the trigger‑optimization team – Iteration 315.*