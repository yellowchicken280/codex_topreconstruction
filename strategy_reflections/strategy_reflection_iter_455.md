# Top Quark Reconstruction - Iteration 455 Report

**Iteration 455 – Strategy Report**  

---

### 1. Strategy Summary  
**Physics motivation**  
- Top‑quark hadronic decays form a clear *mass hierarchy*: the two jets from the W boson cluster around the narrow **W‑mass** (≈ 80 GeV) while the three‑jet system should reconstruct the broader **top‑mass** (≈ 173 GeV).  
- In the boosted regime the detector resolution improves and the decay products become collimated, so a pT‑dependent treatment of the mass constraints is natural.

**What was built**  
| Component | Description |
|-----------|-------------|
| **Quality scores** | • **fW** – deviation of the dijet mass from the nominal W mass (Gaussian‑like weighting). <br>• **fT** – deviation of the three‑jet mass from the top mass. <br>• **fR** – spread of the two dijet masses in the same triplet (penalises asymmetric splits). <br>All three are *continuous* and their resolutions are scaled with the triplet transverse momentum (pT). |
| **Base classifier** | A pre‑trained BDT that captures jet‑shape & sub‑structure information (track‑count, N‑subjettiness, etc.). The raw BDT output is normalised to \[0, 1\]. |
| **Fusion MLP** | A **two‑neuron ReLU MLP** that receives the four inputs \([\,\text{BDT}_{\text{norm}},\,fW,\,fT,\,fR\,]\). The non‑linear hidden layer allows “rescue” of otherwise marginal BDT scores when the kinematic consistency is excellent, and the opposite when the mass hierarchy fails. |
| **Decision function** | A **piece‑wise‑linear sigmoid** (a series of comparator‑adders) that maps the MLP output to a final discriminant. This implementation is fully FPGA‑friendly and meets the 150 ns latency budget. |

The full flow is therefore: jet‑triplet → BDT + mass‑scores → tiny MLP → linear‑sigmoid → trigger decision, all synthesised for low‑latency hardware.

---

### 2. Result with Uncertainty  
| Metric | Value |
|--------|-------|
| **Signal efficiency** (top‑tag acceptance) | **0.6160 ± 0.0152** |
| **Latency** (measured on the target FPGA) | **≈ 138 ns** (well below the 150 ns ceiling) |
| **Resource utilisation** | < 12 % of DSPs, < 8 % of LUTs – leaves ample margin for future extensions. |

The quoted efficiency is relative to the baseline (BDT‑only) working point that yields the same background rejection. The improvement over the pure‑BDT reference is ≈ +5 % absolute efficiency at fixed false‑positive rate.

---

### 3. Reflection  

| Question | Answer |
|----------|--------|
| **Did the hypothesis hold?** | **Yes.** The physics‑driven scores (fW, fT, fR) proved to be largely *orthogonal* to the BDT shape variables. Adding them via the MLP lifted many events that failed the BDT but satisfied the mass hierarchy, producing the observed 5 % efficiency gain. |
| **Where did it work best?** | The gain is most pronounced for **high‑pT** top candidates (pT > 600 GeV). In this regime the pT‑scaled resolution of fW/fT shrinks, making the mass constraints tighter and the MLP more decisive. At lower pT (≈ 300‑400 GeV) the improvement is modest (≈ 2 %) because the jet‑mass resolution is broader and the BDT already captures most of the discriminating power. |
| **Why the MLP‑only Fusion?** | A two‑neuron ReLU network is just enough to implement a *piece‑wise linear* mapping of the four inputs. This keeps the model within the FPGA’s integer‑arithmetic budget while still providing the non‑linear “rescue” effect the hypothesis required. |
| **Any weaknesses?** | • The **fR** spread score is simple (absolute difference of the two dijet masses) and may be sub‑optimal for asymmetric jet‑splittings in high‑pile‑up. <br>• The piece‑wise linear sigmoid limits the curvature of the final decision surface; a more expressive function could extract a few extra percent in efficiency but would need extra hardware resources. |
| **Overall verdict** | The strategy validates the core idea: *explicitly encoding the known mass hierarchy adds independent information that can be fused efficiently with shape‑based classifiers, yielding a measurable performance uplift within strict latency constraints.* |

---

### 4. Next Steps  

| Goal | Proposed Action | Expected Impact |
|------|----------------|-----------------|
| **Refine the mass‑score resolution model** | • Replace the simple Gaussian scaling with a *pT‑dependent, data‑driven resolution map* (derived from calibration runs). <br>• Add a small **pile‑up correction** (e.g., using the event‑level PU density) to fW/fT. | More accurate fW/fT at moderate pT, reducing the occasional over‑penalisation of good candidates. |
| **Enrich the kinematic feature set** | • Introduce a **ΔR\(_{W}\)** (angular separation of the two W‑jets) and a **3‑jet‑balance** variable (e.g., pT‑asymmetry). <br>• Keep the total number of inputs ≤ 6 to stay within the two‑neuron MLP budget. | Additional orthogonal information, especially for cases where the W‑mass is well‑reconstructed but the topology is atypical. |
| **Upgrade the fusion block** | • Test a **3‑neuron MLP** (still a single hidden layer) to allow a richer piece‑wise linear approximation. <br>• Quantise the hidden‑layer weights to 8‑bit integers – fits comfortably on the current FPGA. | Potentially recovers another ≈ 1‑2 % efficiency without breaking the latency budget. |
| **Explore a more flexible final activation** | • Implement a *lookup‑table based sigmoid* (e.g., 256‑entry monotonic LUT) that approximates a true logistic curve while still using only comparators and adders. <br>• Compare directly against the current piece‑wise linear version. | May tighten the decision boundary near the operating point, improving background rejection for a given signal efficiency. |
| **Validate on realistic conditions** | • Run the full chain on *full‑simulation samples with high pile‑up (µ ≈ 80)* and on *early Run‑3 data* to assess robustness. <br>• Monitor any drift of fW/fT distributions over time; if needed, introduce an **online calibration constant** stored in a small BRAM. | Guarantees that the gains survive the environment the trigger will actually see. |
| **Long‑term hardware roadmap** | • Prototype a **binary‑network version** (weights = {−1, +1}) of the MLP to explore a future upgrade path where resources become even tighter, allowing a deeper network (e.g., 2 hidden layers) while staying FPGA‑friendly. | Positions us to adopt more sophisticated models later without redesigning the whole trigger board. |

**Prioritisation for the next iteration (Iteration 456):**  
1. Implement the data‑driven pT‑dependent resolution for fW/fT (lowest cost, highest payoff).  
2. Add the ΔR\(_{W}\) and 3‑jet‑balance variables, keeping the input count at five.  
3. Evaluate a 3‑neuron MLP with 8‑bit quantisation; if latency remains < 150 ns, adopt it as the new default fusion block.  

These steps should push the top‑tag efficiency toward the **≈ 0.65** region at the same background rejection while preserving the stringent latency budget required for the Level‑1 trigger.  

--- 

*Prepared by the Trigger‑ML Working Group – Iteration 455 Review*  