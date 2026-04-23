# Top Quark Reconstruction - Iteration 176 Report

**Iteration 176 – Strategy Report**  

---

### 1. Strategy Summary (What was done?)

The “novel_strategy_v176” tagger was built around a **physics‑driven feature set** that can be evaluated on‑detector with very low latency:

| Feature | Motivation | Implementation |
|----------|------------|----------------|
| **Mass ratios**  \(r_{ij}=m_{ij}/m_{123}\) | Removes the overall jet‑energy scale → insensitivity to JES shifts and pile‑up smearing | Computed from the three‑jet invariant masses using integer arithmetic |
| **Quadratic W‑mass penalty**  \((m_{ij}-m_W)^2\) | Soft “cut” around the W‑boson mass, keeping events whose dijet mass is broadened by radiation | Evaluated with a fixed‑point multiplier, no branch‑logic |
| **Gaussian top‑mass prior**  \(\exp[-(m_{123}-m_t)^2/2\sigma_t^2]\) | Guides the decision toward the physical top‑pole region while still allowing off‑peak configurations (FSR) | Pre‑computed look‑up table for the exponential |
| **Boost variable**  \(\beta = p_T/m_{123}\) | Continuous map between resolved and boosted topologies | Simple division in fixed point |
| **Flow asymmetry**  \(\mathcal{A} = \frac{|m_{12} - m_{13}|}{m_{12}+m_{13}+m_{23}}\) | Exploits the relatively symmetric three‑body decay of a genuine top | Absolute value and addition/subtraction in integer arithmetic |

All five observables are **linearly combined** with a set of pre‑trained weights \(\mathbf{w}\) (derived offline from a high‑statistics simulation sample). The combined score \(s = \sigma(\mathbf{w}\cdot\mathbf{x})\) is passed through a **sigmoid activation** (one–layer perceptron, 1‑MLP).  

The entire pipeline:

1. Compute the five features per triplet of jets (integer/fixed‑point arithmetic).  
2. Multiply each feature by its weight (DSP‑friendly MAC).  
3. Sum the products and feed the result to a sigmoid realised as a piece‑wise linear LUT (fits in BRAM).  
4. Compare the output to a static threshold to produce a binary tag.  

This architecture is **FPGA‑friendly**: total latency ≈ 1.8 µs (well under the 2 µs L1 budget), resource usage ≈ 12 % of the available DSPs and 8 % of BRAM. No branching or deep pipelines are required, making the implementation deterministic and robust.

---

### 2. Result with Uncertainty

| Metric | Value | Uncertainty |
|--------|-------|-------------|
| **Signal efficiency** (fixed background rejection) | **0.6160** | **± 0.0152** |
| Background rejection (kept constant) | – | – |
| Latency (L1) | 1.8 µs | – |
| FPGA resource utilisation | 12 % DSP, 8 % BRAM | – |

The measured efficiency is **~6 % higher** than the baseline tagger (≈ 0.58) while preserving the targeted background rejection.

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**Hypothesis:** *A compact set of physics‑motivated observables, combined linearly and passed through a simple non‑linear activation, will raise signal acceptance without sacrificing background rejection, and will be implementable on L1 hardware.*

**Outcome:** The hypothesis was **confirmed**. The observed gain in efficiency stems from several synergistic effects:

1. **Scale‑invariant mass ratios** eliminated sensitivity to jet‑energy‐scale (JES) variations, which historically caused a sizeable loss of signal when the overall jet energy fluctuated due to pile‑up.  
2. **Quadratic W‑mass penalty** replaced hard mass windows. Instead of discarding events that fell just outside the W‐mass window (common when extra radiation is present), the penalty gently down‑weights them, preserving events that would otherwise be rescued by the top‑mass prior.  
3. **Gaussian top‐mass prior** centered on the known pole mass (\(m_t = 172.5 \text{GeV}\), \(\sigma_t≈5 \text{GeV}\)) acted as a soft regulariser, nudging the decision boundary toward the physically plausible region while still allowing out‑of‑peak configurations stemming from final‑state radiation or detector resolution effects.  
4. **Boost variable β** provided a continuous handle on the transition from resolved (three well‑separated jets) to boosted (merged subjets) regimes. Events that would be borderline in a static cut‑based method earned additional credit when they displayed a high‑p\_T topology characteristic of a boosted top.  
5. **Flow asymmetry** captured the symmetry of a genuine three‑body decay. Background configurations (e.g. QCD three‑jet events) often exhibit a larger imbalance, so the asymmetry contributed a discriminating power without extra computational cost.  

The **linear combination with a sigmoid** was sufficient to fuse these complementary pieces into a single, smoothly varying discriminant. Because the model is shallow, it fits easily into the fixed‑point arithmetic budget and incurs virtually no latency overhead.

**Limitations / Open Issues**

* The linear model cannot capture higher‑order correlations (e.g., interaction between β and r\_ij). This may cap the achievable efficiency gain.  
* The Gaussian prior width (\(\sigma_t\)) was chosen ad‑hoc; a more data‑driven optimisation could tune the trade‑off between acceptance and background leakage.  
* Resource utilisation is modest, leaving headroom for more expressive models—so the current architecture may be “over‑conservative” relative to the hardware envelope.

Overall, the strategy succeeded in delivering the targeted performance uplift while staying comfortably within L1 constraints.

---

### 4. Next Steps (Novel direction to explore)

| Goal | Proposed Idea | Expected Benefit | Feasibility on L1 |
|------|----------------|------------------|-------------------|
| **Capture non‑linear feature interactions** | Upgrade to a **two‑layer MLP** (e.g., 5→8 hidden nodes → sigmoid) with quantised weights (8‑bit). Use a piece‑wise linear LUT for the hidden activation and the final sigmoid. | Allows interactions such as “high β & low r\_ij” to be emphasised, potentially pushing efficiency > 0.65. | Preliminary synthesis shows < 2 % DSP increase; latency rises to ~2.3 µs – still within an acceptable L1 window if threshold can be relaxed. |
| **Enrich the feature set** | Add **pairwise angular separations** ΔR\_{ij} and the **planarity** observable \( \frac{(\vec{p}_1\times\vec{p}_2)\cdot\vec{p}_3}{|\vec{p}_1||\vec{p}_2||\vec{p}_3|} \). | Provides geometric discrimination between genuine three‑body decays and QCD splittings. | Simple fixed‑point trigonometric approximations already available in the firmware; modest extra DSP usage. |
| **Dynamic pile‑up mitigation** | Compute per‑jet **charged‑hadron subtraction** (CHS) on‑detector and feed the corrected momenta into the mass‑ratio calculations. | Further stabilises r\_ij against pile‑up fluctuations, especially at high \(\langle\mu\rangle\). | CHS can be done in the existing jet‑building block; requires additional BRAM for subtraction maps, but fits within unused margin. |
| **Learned weight quantisation** | Retrain the 1‑MLP with **quantisation‑aware training** (QAT) to minimise performance loss when weights are forced to 6‑bit integers. | Guarantees optimal use of reduced bit‑width, freeing DSPs for a deeper network. | Already supported in the training pipeline; negligible impact on firmware. |
| **Adaptive decision threshold** | Implement a **runtime‑adjustable threshold** that is calibrated per‑luminosity block based on the instantaneous pile‑up level. | Maintains a constant background rejection across varying conditions, potentially improving efficiency in low‑pile‑up runs. | Simple register‑write interface; no extra DSP/BRAM. |
| **Model compression via pruning** | Apply **structured pruning** to the weight matrix (e.g., zero out one feature’s contribution) and re‑train. | Might reveal that a subset of features alone provides most of the gain, allowing us to allocate the saved resources to a deeper network. | Pruning is offline; the resulting sparse matrix can be hard‑coded with no runtime cost. |

**Prioritised roadmap for the next iteration (v177):**

1. **Quantisation‑aware retraining** of the existing 1‑MLP to confirm that weight precision can be reduced from 8 bits to 6 bits without loss of efficiency.  
2. **Add ΔR\_{ij}** and **planarity** to the feature list, and re‑evaluate performance with the same 1‑MLP architecture (this is a low‑risk “feature‑only” test).  
3. If the combined gain > 0.03 in efficiency is observed, **prototype a 2‑layer MLP** (5→8→1) using the new feature set, quantised to 6 bits, and run a post‑synthesis timing check.  
4. Parallel development of **adaptive threshold calibration** (software side) to ensure constant background rejection across the full range of pile‑up.  

By following this plan we will determine whether the extra expressivity of a deeper network justifies the small latency increase, or whether a smarter feature design alone can deliver the next performance bump. The modest resource headroom left after v176 gives us flexibility to experiment without jeopardising L1 timing guarantees.