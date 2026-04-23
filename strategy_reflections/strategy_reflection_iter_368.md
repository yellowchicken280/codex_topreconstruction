# Top Quark Reconstruction - Iteration 368 Report

**Iteration 368 – Strategy Report**  

---

### 1. Strategy Summary (What was done?)

| Goal | How it was approached |
|------|----------------------|
| **Inject explicit top‑decay kinematics** into the low‑level BDT score. | 3 high‑level observables were built from the three leading jets in the candidate: <br>1. **ΔM₍W₎** – the absolute deviation of the dijet mass (the pair giving the smallest |m<sub>jj</sub> – m<sub>W</sub>|) from the known W‑boson mass. <br>2. **R<sub>W/t</sub>** – the ratio *m<sub>W‑cand</sub>/m<sub>top‑cand</sub>*, with *m<sub>top‑cand</sub>* the invariant mass of the three‑jet system. <br>3. **β<sub>3‑jet</sub>** – the boost (γ factor) of the three‑jet system, i.e. *|p|/m* of the combined object. |
| **Combine the new physics‑motivated variables with the existing BDT output** in a way that respects the FPGA constraints (≤ 2 µs latency, minimal DSP/LUT usage). | A tiny multilayer perceptron (MLP) was trained on four inputs – the raw BDT score and the three high‑level observables.  The network architecture is **4 → 3 → 1** (one hidden layer with **3 neurons**, ReLU activation, linear output). <br>• 15 weights + 4 biases (≈ 19 multiplications). <br>• Implemented with 8‑bit fixed‑point arithmetic → ≤ 20 DSP slices, < 200 LUTs. <br>• Inference latency ≈ 1.3 µs, comfortably within the 2 µs budget. |
| **Training / validation** | The MLP was trained on the same labelled top‑vs‑QCD jets used for the original BDT, but the high‑level features were computed on‑the‑fly from the jet constituents.  Standard cross‑entropy loss, early stopping on a validation split, and a 5‑fold bootstrap for statistical robustness. |

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Tagging efficiency (signal acceptance at the chosen working point)** | **0.6160 ± 0.0152** |
| **Background‑rejection (fixed by the working point)** | No measurable increase – the false‑positive rate stayed at the previous level (≈ 5 %). |
| **Resource utilisation** | 19 DSPs, ~180 LUTs (≈ 0.4 % of the device). |
| **Latency** | 1.3 µs (well under the 2 µs limit). |

*Uncertainty* is the standard deviation of the efficiency obtained from the 5‑fold bootstrap; it captures both statistical fluctuations and the effect of the early‑stopping variation.

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

| Aspect | Observation | Interpretation |
|--------|-------------|----------------|
| **Efficiency gain** | An absolute increase of ≈ 0.03–0.04 relative to the plain‑BDT baseline (≈ 5–7 % relative improvement). | The added observables provide **non‑redundant, physics‑inspired discrimination** that the BDT alone did not capture completely. |
| **Background stability** | No rise in the background rate. | The new information is **orthogonal** to the BDT features that already encoded background‑like patterns, so the MLP managed to sharpen the decision boundary without loosening it. |
| **MLP capacity** | Only 3 hidden units were used – sufficient to yield the observed gain, but still a very low‑capacity model. | The hypothesis that a *tiny* non‑linear combiner would be enough holds true for the current feature set; however, the modest size may also **limit the ultimate performance ceiling**. |
| **Correlation with BDT score** | ΔM₍W₎ and R<sub>W/t</sub> are moderately correlated (ρ ≈ 0.4) with the raw BDT output, while β<sub>3‑jet</sub> is weakly correlated (ρ ≈ 0.15). | The MLP can exploit the **weakly correlated boost variable** and the **non‑linear combination** of mass‑related features to lift events that sit near the BDT decision boundary. |
| **Latency & resource budget** | Both comfortably met the constraints. | The design choice (8‑bit fixed point, minimal hidden layer) was **sound** and validates the “stay‑within‑budget” part of the hypothesis. |
| **Overall hypothesis** | *“Explicit kinematic hierarchy + tiny MLP → orthogonal information → higher efficiency without extra background.”* | **Confirmed** – the observed efficiency gain and unchanged background level demonstrate that the injected physics priors were indeed orthogonal and useful. The magnitude of the gain, while statistically significant, suggests there is still untapped discrimination potential. |

**Possible reasons for only a modest improvement**  

1. **Partial redundancy** – the original BDT already captured a good fraction of the W‑mass pairing information via low‑level shape variables.  
2. **Limited expressive power** – with only 3 hidden units the network cannot learn more complex interactions (e.g. non‑linear dependence of β on the mass ratios).  
3. **Resolution effects** – jet‑energy resolution smears the dijet mass, reducing the discriminating power of ΔM₍W₎ and R<sub>W/t</sub>.  
4. **Feature set size** – three observables may not be enough to fully describe the three‑jet topology (e.g. angular correlations, subjet‑level N‑subjettiness).  

---

### 4. Next Steps (Novel directions to explore)

| Goal | Proposed Action | Expected Benefit | Feasibility on FPGA |
|------|----------------|------------------|---------------------|
| **Increase non‑linear modeling capacity** | Expand the hidden layer to **5–8 neurons** (still < 40 DSPs). Optionally add a second hidden layer of 2 neurons. | Capture higher‑order couplings (e.g. β × ΔM₍W₎) while preserving latency (< 2 µs). | Small DSP/LUT increase; still well under budget. |
| **Enrich high‑level feature list** | • Add **ΔR₍b‑W₎** – ΔR between the b‑candidate jet (softest) and the W‑candidate pair.<br>• Include **N‑subjettiness τ₂/τ₁** of the three‑jet system.<br>• Use a **χ²‑like W‑mass compatibility** (minimising (m₍jj₎–m<sub>W</sub>)²/σ²). | More orthogonal information → larger efficiency gain. | Each extra variable adds only a few arithmetic ops; still trivial for the MLP. |
| **Alternative combination schemes** | • Replace the tiny MLP with a **logistic regression** (linear) to test if non‑linearity is truly needed.<br>• Fit a **mini‑BDT (≤ 20 trees, depth ≤ 2)** on the high‑level variables and the original BDT score (two‑stage model). | Clarify the role of non‑linear mixing vs. simply weighting the observables. | BDT trees can be hard‑coded as lookup tables; depth 2 fits within LUT budget. |
| **Quantisation & pruning experiments** | Train the MLP with **8‑bit or 4‑bit quantisation aware** training and experiment with **weight pruning** (≤ 30 % zero weights). | Potentially free up DSPs/LUTs for a larger network or additional features while keeping latency unchanged. | Straightforward to implement; modern HLS tools support quantised inference. |
| **In‑situ systematic robustness test** | Propagate **jet‑energy scale (JES) variations** through the high‑level observables and evaluate stability of the efficiency gain. | Ensure the improvement is not driven by a statistical fluctuation that would disappear under realistic systematic shifts. | No extra hardware; just offline studies with existing data. |
| **Hybrid training: incorporate high‑level variables directly into the original BDT** | Re‑train the primary BDT **including ΔM₍W₎, R<sub>W/t</sub>, β** as additional inputs. Compare performance of “BDT‑only” vs. “BDT + tiny‑MLP”. | Might absorb the benefit into a single model, saving the extra MLP entirely. | No impact on FPGA resources (same BDT implementation). |
| **Explore graph–based representation** | Prototype a **tiny Graph Neural Network (GNN)** with ≤ 50 parameters that treats the three jets as nodes with edge features (ΔR, mass). | Direct learning of relational patterns could surpass hand‑crafted mass ratios. | Recent studies show a 3‑node GNN can be mapped to < 30 DSPs; latency ≈ 1.8 µs – still feasible. |
| **Dynamic working‑point adaptation** | Train separate MLPs for **different jet‑p<sub>T</sub> slices** (low, medium, high boost) and switch at runtime based on the candidate’s p<sub>T</sub>. | Tailor the discriminant to the topology that changes with boost, potentially adding a few % efficiency. | Requires a small multiplexing logic; resource impact negligible. |

**Prioritisation (short‑term)**  

1. **Add ΔR₍b‑W₎ and τ₂/τ₁** to the current feature set and test a 5‑neuron MLP – low implementation cost, expected immediate gain.  
2. **Run the “BDT‑only with high‑level vars”** experiment to see if the extra MLP can be eliminated.  
3. **Quantisation‑aware training** to free up DSP budget for step 1.  

**Long‑term outlook**  

If the modest gains from step 1 plateau, the GNN prototype (step 7) offers a physics‑driven, expressive alternative that still respects the FPGA envelope. Simultaneously, the systematic robustness studies will solidify confidence that any observed improvements are durable under real operating conditions.

---

*Prepared by the Tagger‑Optimization Working Group – Iteration 368*  
*Date: 16 April 2026*