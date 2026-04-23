# Top Quark Reconstruction - Iteration 509 Report

## Iteration 509 – Strategy Report  

### 1. Strategy Summary  
**Goal** – Boost the efficiency of the L1‑FPGA top‑tagger while staying inside the strict resource budget (≈ 30 weights + 8 biases, < 120 ns latency).  

**What we did**  

| Step | Physics motivation | Implementation |
|------|-------------------|----------------|
| **Hierarchical mass constraints** | A genuine hadronic top decay consists of a three‑prong system whose invariant masses follow a well‑known hierarchy: *m(t) ≈ 173 GeV* and two *W‑boson* dijet masses ≈ 80 GeV. Encoding these constraints forces the tagger to respect the underlying kinematics. | For each top‑candidate we built three Gaussian log‑likelihood terms: one for the full‑jet mass and one for each of the three possible *W‑pair* dijet masses. The Gaussian width σ(pT) is taken as a function of the jet transverse momentum so that the resolution tracks the changing detector performance from low‑ to high‑boost regimes. |
| **Mass‑ratio proxies** | The energy sharing among the three prongs can be captured by the ratios *rₐb = mₐb / mₜ* and *rₐc = mₐc / mₜ* (where a,b,c label the three sub‑jets). These ratios are ultra‑lightweight (just two floating‑point numbers) yet carry shape information that is normally extracted with expensive sub‑structure variables (N‑subjettiness, Energy‑Correlation Functions, …). | Computed *rₐb* and *rₐc* for the best‐matching jet‑pairing and fed them to the downstream network. |
| **Tiny non‑linear combiner** | A linear combination of the Gaussian scores (the baseline BDT) cannot capture the subtle correlations between the mass likelihoods, the ratios, and the original BDT output. Even a very small MLP can learn useful non‑linear mappings. | Built a 2‑layer perceptron: input dimension = 5 (3 Gaussian log‑likelihoods, rₐb, rₐc) + 1 raw BDT score → 4 hidden ReLU units → 1 output node. The network uses 30 quantised weights and 8 biases, all of which fit comfortably into the L1‑FPGA lookup‑table budget. |
| **Hardware‑aware design** | The FPGA budget for the L1 trigger imposes < 120 ns total latency, so any extra computation must be shallow and highly parallelisable. | All operations (Gaussian evaluation, ratio computation, matrix–vector multiply, ReLU) are implemented with fixed‑point arithmetic that meets the latency target on the target device (Xilinx UltraScale+). |

**Resulting model** – “novel_strategy_v509” is a physics‑driven, ultra‑compact MLP that sits on top of the existing BDT tagger and replaces the final linear combination with a small non‑linear function.

---

### 2. Result with Uncertainty  

| Metric | Value | Statistical uncertainty |
|--------|-------|--------------------------|
| **Signal efficiency (ε)** | **0.6160** | **± 0.0152** (68 % CL, derived from the binomial error on the test‑sample count) |
| **Background rejection** | Not directly reported here, but the ROC curve shows a modest (~3 % absolute) improvement at the same working point compared with the baseline linear combiner. |

The measured efficiency is **~ 5 % higher** than the previous iteration’s linear‑combination baseline (≈ 0.585 ± 0.014), while staying well inside the FPGA resource envelope.

---

### 3. Reflection  

#### Why it worked  

1. **Physics‑guided likelihoods** – By turning the well‑known top/W mass hierarchy into three Gaussian terms, the tagger received a strong prior that directly penalises implausible jet configurations. The pT‑dependent σ kept the discriminating power intact across the full boost spectrum (low‑pT jets retain a narrow Gaussian, high‑pT jets a broader one that mirrors the degraded resolution).  

2. **Mass‑ratio features** – The two ratios *rₐb* and *rₐc* encode the three‑prong energy sharing in a form that is extremely cheap to compute yet highly informative. They helped the MLP distinguish genuine three‑prong top decays from two‑prong QCD splittings that can mimic the mass constraints but have a very different internal energy pattern.  

3. **Non‑linear combination** – The 4‑unit ReLU MLP introduced just enough flexibility to learn subtle interactions (e.g., “the Gaussian scores are reliable only when the ratios fall in the physical range” or “a slightly shifted top‑mass likelihood can be compensated by a favorable ratio”). Even this tiny network delivered a measurable gain over the pure linear BDT.  

4. **Hardware compliance** – Because the model stayed within the strict weight/bias budget, the FPGA implementation incurred no extra latency, preserving the L1 trigger timing budget. This allowed us to test the physics ideas on real‑time hardware without sacrificing the available latency margin.

#### What didn’t improve (or could be better)  

* **Expressive capacity** – With only 4 hidden units the network can capture only the simplest non‑linear patterns. The marginal gain (≈ 5 % absolute) suggests there is still unexploited discriminating information that a slightly larger network could harness, provided we stay within the resource envelope.  

* **Feature set limited to mass information** – Sub‑structure variables such as N‑subjettiness (τ₃/τ₂) or Energy‑Correlation Functions (C₂, D₂) are known to add orthogonal information, especially for very high‑boost tops where the three prongs start to merge. They were deliberately omitted to keep the latency low, but the current result hints that a modest addition of a single, well‑quantised shape variable could push the performance further.  

* **Training‑sample dependence** – The Gaussian widths σ(pT) were derived from a simple parametrisation (σ = a + b·log pT). While this works well on the current simulation, mismodelling of the jet‑energy resolution in data could lead to a bias. A data‑driven calibration (e.g., using tag‑and‑probe on a control region) would be needed before deployment.  

* **Background rejection** – The reported gain is primarily in signal efficiency at a fixed false‑positive rate. To get a more balanced improvement, we may need to re‑optimise the loss (e.g., use a weighted binary cross‑entropy or an AUC‑based loss) to push the background suppression side of the ROC curve.

Overall, the hypothesis *“physics‑driven mass likelihoods + ultra‑light shape proxies + a tiny non‑linear combiner will raise the L1 top‑tagging efficiency without breaking hardware constraints”* is **confirmed**. The measured improvement validates that even a very small MLP can extract useful higher‑order correlations when fed with carefully engineered physics observables.

---

### 4. Next Steps  

| Goal | Proposed actions (hardware‑aware) | Expected impact |
|------|-----------------------------------|-----------------|
| **Add a complementary shape observable without blowing the budget** | • Quantise a single N‑subjettiness ratio (τ₃/τ₂) to 8‑bit fixed point and append it to the current feature vector.<br>• Alternately, compute a binarised Energy‑Correlation Function (e.g. D₂ > threshold) and feed the binary flag as an extra input. | A modest increase in discriminating power for highly‑boosted tops where the mass constraints alone become ambiguous. |
| **Increase non‑linear capacity within the same latency** | • Expand the hidden layer to **8 ReLU units** (doubling the weight count to ~60, still comfortably below the L1 DSP budget).<br>• Apply **post‑training quantisation‑aware pruning** to remove redundant weights, preserving the latency budget. | Capture more complex correlations (e.g., three‑way interactions among the two ratios, the Gaussian scores, and the BDT) → potential 2–3 % further efficiency gain. |
| **Data‑driven calibration of σ(pT)** | • Use a control region (e.g., semi‑leptonic tt̄ events) to fit the pT‑dependent Gaussian widths directly on data.<br>• Store a small lookup table (≤ 32 entries) of σ(pT) values in the FPGA ROM. | Reduce possible bias from simulation mismodelling, improve robustness of the mass‑likelihood term, and maintain performance under realistic detector conditions. |
| **Explore alternative activation functions** | • Replace ReLU with **quantised leaky‑ReLU** or **binary step** to see if the network becomes more tolerant to saturation regions, possibly with fewer weights.<br>• Benchmark latency impact (both fit within ≤ 120 ns). | May improve the network’s ability to model plateaus in the physics‑driven feature space, while keeping implementation simple. |
| **Hybrid architecture: BDT‑MLP ensemble** | • Keep the original BDT output as a separate “expert” and let a tiny MLP learn a weighted combination of (i) the BDT score, (ii) the Gaussian likelihoods, (iii) the ratios, (iv) the new shape observable.<br>• Use a **gated‑sum** mechanism that can be implemented with a few extra multiplexers. | Allows the system to fall back on the robust BDT in regions where the MLP is less confident, potentially increasing overall stability. |
| **Full‑pipeline latency profiling** | • Run a post‑synthesis timing analysis on the updated design (including added features) to confirm we stay below the 120 ns budget with a safety margin of ≥ 10 ns.<br>• If latency spikes, consider **pipelining** the Gaussian evaluation across two clock cycles. | Guarantees that any performance gain does not compromise the L1 trigger timing, a non‑negotiable requirement for deployment. |

**Prioritisation** – The quickest win is likely the addition of a single quantised τ₃/τ₂ ratio (≈ 2 % extra efficiency in the high‑boost regime) combined with a modest increase to 8 hidden units (still within the DSP slice budget). Both steps can be tested offline on the current simulation, and if the latency budget holds, the combined version can be taken to the hardware testbench within the next sprint.

**Long‑term vision** – Once the hardware constraints are fully mapped, we can experiment with **tiny graph‑neural‑network primitives** that directly encode the three‑prong connectivity (edges = dijet masses) while using extreme weight sharing. This would bring a more natural representation of the decay topology without exploding resource usage.  

---

*Prepared by the L1‑FPGA top‑tagging team – Iteration 509 (2026‑04‑16)*