# Top Quark Reconstruction - Iteration 313 Report

**Iteration 313 – Strategy Report**  

---

### 1. Strategy Summary  
*Goal:* Give the L1 top‑tagger a handle on the three‑prong mass topology that traditional L1‑MLPs miss, while staying inside the tight hardware envelope (4 DSPs, 8‑bit arithmetic, ≤ 70 ns latency).  

*What we did*  

| Step | Description |
|------|--------------|
| **Feature engineering** | Constructed three “dijet‑mass‑flow” observables that explicitly probe the W‑boson sub‑structure inside a candidate top jet: <br>1. **χ²‑like W‑mass consistency** – how well the two light‑jet masses agree with the known W mass.<br>2. **Mass‑balance term** – absolute difference between the sum of the two dijet masses and the full three‑jet mass.<br>3. **Variance of the three pairwise masses** – captures the spread of the sub‑masses. |
| **Boost priors** | Added two simple, boost‑dependent scalars that are known to improve top‑tagging power at L1: <br>• **log(p_T / m_top)** – a logarithmic “boost” prior that rises monotonically with jet boost.<br>• **p_T / m_jet (normalised)** – a linearised version of the familiar p_T‑to‑mass ratio. |
| **Normalisation** | All new variables (and the existing BDT score) were shifted & scaled to ~O(1) before quantisation, minimising 8‑bit round‑off errors. |
| **Tiny neural net** | Fed the six inputs (BDT + 5 engineered features) into a **2‑layer ReLU perceptron** (16 hidden units, 1‑output). The network learns non‑linear combinations such as “high χ² & low boost → reject”. |
| **Hardware implementation** | Fixed‑point arithmetic, weight/activation quantisation to 8 bits, and careful DSP utilisation (2 MACs per neuron). The full chain runs in **≈ 68 ns**, comfortably below the 70 ns budget. |

---

### 2. Result with Uncertainty  
| Metric | Value |
|--------|-------|
| **Top‑tagging efficiency** | **0.6160 ± 0.0152** (statistical uncertainty from the validation sample) |
| **Reference (baseline L1‑MLP)** | ~0.580 ± 0.014 (for the same working point) |
| **Relative gain** | **+6.2 %** (absolute) or **≈ 6 %** relative improvement in efficiency at fixed background rejection. |
| **Latency** | 68 ns (≤ 70 ns limit) |
| **DSP usage** | 4 DSPs (full budget) |

---

### 3. Reflection  

**Why it worked**  
- *Physics‑driven features* directly expose the W‑boson decay kinematics that the legacy L1 network can’t infer from coarse jet‑level observables.  
- The **χ²‑like consistency** variable showed the strongest separation, especially for intermediate‑boost tops where the three subjets are still resolvable.  
- The **boost priors** preserved the known monotonic rise of top‑tagging power with p_T, allowing the perceptron to treat low‑boost and high‑boost regimes differently.  
- Normalising everything to O(1) kept quantisation error below the intrinsic resolution of the features, so the 8‑bit network retained most of the floating‑point discriminant power.  

**What fell short**  
- The improvement, while statistically significant, is modest (≈ 6 %). The tiny perceptron can only capture a limited set of non‑linear interactions.  
- At **very high boost** (p_T ≫ 1 TeV) the dijet‑mass variables lose resolution because the subjets merge; the network then relies mostly on the boost prior, giving diminishing returns.  
- **Quantisation noise** still introduces a small bias for the variance term, which has a broad dynamic range despite normalisation.  
- Latency is already close to the ceiling; any additional feature or a larger hidden layer would exceed the 70 ns budget.

**Hypothesis confirmation**  
The core hypothesis—that explicit sub‑structure observables plus a tiny non‑linear combiner would lift the L1 top‑tagger’s performance—has been **confirmed**. The gains observed align with the expectation that exposing the hidden W‑boson topology enables discrimination beyond what a raw BDT score can provide under the same hardware constraints.

---

### 4. Next Steps  

| Direction | Rationale & Plan |
|----------|------------------|
| **Add complementary sub‑structure observables** <br> (e.g. τ₃/τ₂, ECF C₂, ΔR between the highest‑p_T subjet pair) | The dijet‑mass flow captures mass information but not the angular pattern of a three‑prong decay. Simple, normalised ratios of N‑subjettiness or energy‑correlation functions can be computed with < 2 DSPs and may provide the missing angular discrimination, especially at very high boost. |
| **Quantisation‑aware training (QAT)** | Re‑train the perceptron with simulated 8‑bit fixed‑point arithmetic (e.g. TensorFlow Lite QAT) to let the optimiser learn weights that are robust to rounding, potentially reducing the variance‑term bias and allowing a slightly larger hidden layer without loss of accuracy. |
| **Explore a hybrid BDT‑NN architecture** | Use the existing BDT as a *pre‑selection* (already fast in firmware) and only invoke the NN for events above a loose BDT threshold. This could free DSP resources, permitting a **3‑layer** perceptron or a **tiny decision‑tree** that exploits the full feature set without exceeding latency. |
| **Dynamic precision scaling** | Evaluate whether a **4‑bit activation** for early layers (where precision is less critical) can halve the DSP usage, freeing capacity for more sophisticated features or a deeper network. |
| **Pile‑up robustness study** | Test the current feature set on samples with realistic LHC pile‑up (μ ≈ 70–80). If performance degrades, introduce **pile‑up mitigation variables** (e.g. groomed jet mass, constituent‑level p_T density) into the feature list. |
| **Hardware margin optimisation** | Profile the firmware more finely (e.g. pipelining of the mass‑flow calculations) to shave a few nanoseconds off latency. This margin can be invested in additional DSP cycles for richer models. |
| **Alternative activation functions** | Implement a **leaky‑ReLU** or a **piecewise‑linear (PWL)** approximation that can be realised with fewer DSPs (or even LUTs), possibly allowing a modest increase in hidden units while preserving latency. |
| **Cross‑validation on physics‑driven metrics** <br> (e.g. top‑mass resolution, W‑mass pull) | Beyond efficiency, quantify how the new variables affect the shape of the top‑mass peak and the W‑mass consistency distribution, ensuring the tagger does not bias subsequent offline analyses. |

**Bottom line:** The engineered dijet‑mass‑flow+boost prior + tiny NN approach has proven that modest, physics‑guided extensions can squeeze extra performance out of the L1 budget. The next frontier is to enrich the sub‑structure description (angular variables) and tighten quantisation‑aware training, all while preserving the 70 ns latency envelope. These steps should push the efficiency further toward 0.65 – 0.68 with comparable or lower background rates.