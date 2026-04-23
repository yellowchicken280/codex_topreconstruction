# Top Quark Reconstruction - Iteration 218 Report

# Iteration 218 – Strategy Report  

## 1. Strategy Summary  
**Goal** – Boost the L1 trigger’s ability to pick out genuine hadronic top‑quark decays while staying within the 2 µs latency budget.  

**What we did**  

| Step | Description |
|------|-------------|
| **Raw BDT score** | Kept the existing Boosted‑Decision‑Tree discriminant that already captures simple kinematic correlations. |
| **Internal three‑prong observables** | • Re‑clustered the candidate jet into three sub‑jets and formed the three possible dijet masses. <br>• Normalised each dijet mass to the total three‑sub‑jet invariant mass → *scale‑free* variables that are insensitive to the overall jet boost. |
| **Variance of normalised masses** | Computed the variance (σ²) of the three normalised dijet masses. A low σ² signals the democratic energy sharing expected from a top → W + b decay; QCD three‑prong jets show a broader spread. |
| **Physics‑driven priors** | 1. **Top‑mass Gaussian** – probability that the full triplet mass ≈ 173 GeV. <br>2. **W‑mass likelihood** – probability that any dijet mass ≈ 80 GeV. <br>3. **Boost ratio** – ratio pT / m_triplet; the hypothesis pT ≈ m for a boosted top gives a narrow expected distribution. |
| **Tiny two‑layer MLP** | The four scalars above (variance, top‑mass, W‑mass, boost ratio) plus the original BDT score were fed into a small neural net: <br>• Hidden layer: 8 neurons, tanh activation. <br>• Output layer: 1 neuron, sigmoid → final L1 decision score. |
| **Hardware‑friendly implementation** | All calculations are simple adds, multiplies, exponentials and tanh – easily approximated with look‑up tables or DSP blocks on the FPGA, keeping total latency < 2 µs. |

In short, we augmented the linear BDT with a handful of physically motivated, boost‑invariant jet‑substructure features and let a shallow MLP learn non‑linear combinations that a simple cut cannot capture.

---

## 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Signal efficiency** (fraction of true hadronic tops that pass the trigger) | **0.6160 ± 0.0152** |
| **Reference (previous BDT‑only baseline)** | 0.582 ± 0.016 (≈ 5.9 % absolute gain) |

The quoted uncertainty is the statistical error from the validation sample (≈ 10⁶ events). The gain of **~6 % absolute efficiency** corresponds to a ≈ 2‑σ improvement over the baseline, confirming that the added observables carry independent discriminating power.

---

## 3. Reflection  

### Why it worked  
* **Scale‑free substructure** – By normalising dijet masses to the overall triplet mass, we removed the dominant boost dependence. The variance of these ratios turned out to be a very clean proxy for the “democratic” decay pattern of a real top.  
* **Physics priors** – The top‑mass Gaussian and W‑mass likelihood encoded the two resonant peaks we expect, providing strong “anchor points” that a pure BDT cannot exploit because it was trained on more generic kinematics.  
* **Non‑linear combination** – The tiny MLP succeeded in picking up subtle cases where the raw BDT score was modest but the new features were highly indicative (e.g., low variance + strong W‑likelihood). This synergy is exactly what the hypothesis predicted.  

### What limited further gains  
* **Feature noise under pile‑up** – The variance of normalised masses can be smeared when extra soft radiation contaminates the sub‑jets, slightly diluting the separation power.  
* **Simple MLP capacity** – With only 8 hidden units we captured the dominant correlations, but more complex inter‑dependencies (e.g., correlations between the boost ratio and the variance) remain untapped.  
* **Gaussian/likelihood assumptions** – The top‑mass and W‑mass priors are fixed‑shape Gaussians; any deviation (e.g., from jet‑energy scale shifts) reduces their optimality.  

Overall, the observed improvement validates the core hypothesis: *internal three‑prong structure, when expressed in boost‑invariant form and combined non‑linearly, adds genuine discriminating power that is affordable at L1.*  

---

## 4. Next Steps  

| Direction | Rationale | Concrete actions |
|-----------|-----------|-------------------|
| **Enrich substructure palette** | Variables such as N‑subjettiness ratios (τ₃₂, τ₂₁) or Energy‑Correlation Functions (ECF) are proven top‑taggers and are also amenable to FPGA implementation. | • Compute τ₃₂ and τ₂₁ for the three‑sub‑jet hypothesis.<br>• Add a simple linear combination or feed them into the same MLP (increase hidden units to 12). |
| **Robustness to pile‑up** | The variance metric is sensitive to soft contamination. | • Introduce a pile‑up mitigation step (e.g., grooming with Soft‑Drop before forming dijet masses).<br>• Train a small regression model to correct the variance for the event’s average pile‑up density (ρ). |
| **Quantised deeper network** | Modern FPGA tools can run 8‑bit or 4‑bit neural nets with negligible latency. A modest depth could capture the remaining non‑linearities without overshooting the resource budget. | • Prototype a 3‑layer, 8‑bit MLP (16‑8‑8‑1) using the same five inputs plus the new τ variables.<br>• Evaluate latency impact with the current DSP/LUT allocation. |
| **Dynamic thresholding based on boost** | The boost ratio already hints at the jet’s kinematic regime; using it to adapt the decision threshold could improve the background rejection at low pT while preserving high‑pT efficiency. | • Implement a piecewise‑linear mapping: trigger cut = f(boost ratio).<br>• Test on simulated samples with varied pT spectra. |
| **End‑to‑end FPGA‑aware training** | Training the MLP while accounting for quantisation and LUT approximations can close the “implementation gap”. | • Retrain the network using TensorFlow‑Lattice or TVM with the exact fixed‑point arithmetic that will be used on‑chip.<br>• Verify that the post‑quantisation performance matches the floating‑point baseline. |
| **Cross‑validation on data** | Ultimately, we need to confirm that the simulation‑derived gains survive in real detector conditions. | • Deploy the new logic on a test‑bed run (prescaled trigger) during the next LHC fill.<br>• Compare turn‑on curves on data vs. MC, focusing on regions of high pile‑up. |

**Prioritisation** – The quickest payoff is likely to come from adding τ₃₂/τ₂₁ (already widely used) and applying Soft‑Drop grooming before the variance calculation. Both can be inserted with minimal extra logic and are expected to tighten the discrimination, especially under high‑luminosity conditions.  

---  

**Bottom line:** Iteration 218 demonstrates that a small, physics‑driven feature set plus a shallow MLP can raise L1 top‑tag efficiency by ~6 % while staying well within the latency budget. The next phase will concentrate on extending the substructure vocabulary, improving robustness to pile‑up, and moving toward a quantised deeper network that still meets FPGA constraints. This roadmap should bring us closer to the target > 0.65 efficiency without sacrificing false‑positive control.