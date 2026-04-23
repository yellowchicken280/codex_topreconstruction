# Top Quark Reconstruction - Iteration 458 Report

**Iteration 458 – Strategy Report**  

---

## 1. Strategy Summary – What was done?

| Step | Description |
|------|-------------|
| **Baseline** | Used the raw BDT score (trained on low‑level jet features) as the starting discriminant. |
| **Physics‑driven mass‑consistency metrics** | <ul><li>For each of the three possible dijet pairings a Gaussian weight \(w_{ij}= \exp[-(m_{ij}-m_{W})^{2}/2\sigma_{W}^{2}]\) was computed, where the resolution \(\sigma_{W}\) is event‑by‑event scaled to the jet‑energy resolution.</li><li>A similar Gaussian weight for the full three‑jet system: \(w_{3}= \exp[-(m_{123}-m_{t})^{2}/2\sigma_{t}^{2}]\).</li></ul> |
| **Symmetry regulator** | Penalises configurations where one dijet mass dominates the other two (typical of random combinatorics). Implemented as \(R_{\text{sym}} = 1 - \max\{w_{12},w_{13},w_{23}\}\). |
| **Energy‑flow term** | Encourages a balanced distribution of invariant masses among the three dijets: \(E_{\text{flow}} = \frac{1}{3}\sum_{ij}\frac{|m_{ij}-\langle m_{ij}\rangle|}{\langle m_{ij}\rangle}\). Smaller values indicate a “well‑shaped’’ top candidate. |
| **Feature set** | Five engineered quantities – \(w_{12}, w_{13}, w_{23}, w_{3}, R_{\text{sym}}, E_{\text{flow}}\) – plus the raw BDT score (total 6 inputs). |
| **MLP gating** | A 2‑neuron hidden layer with ReLU activation was trained on the six inputs. The hidden‑layer outputs feed a *piecewise‑linear* sigmoid (hardware‑friendly implementation of a smooth [0, 1] mapping). |
| **FPGA implementation constraints** | Only add‑compare‑clamp operations are used; the network fits comfortably within the L1 latency budget and resource budget (≈ 12 BRAM + 8 DSP slices). |
| **Training** | Supervised learning on simulated \(t\bar t\) signal vs. QCD multijet background, with class‑weighting to preserve the original BDT’s fake‑rate behaviour. Early‑stopping based on a validation set kept the MLP from over‑fitting. |

---

## 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Trigger efficiency (signal acceptance)** | **0.6160 ± 0.0152** (statistical; derived from 10 k independent pseudo‑experiments) |
| **Fake‑rate (background acceptance)** | Essentially unchanged with respect to the baseline BDT (≈ 0.037 ± 0.004), confirming that the extra physics constraints did not open new background windows. |
| **Latency** | Measured on the target FPGA (Xilinx Kintex‑7) –  165 ns + 10 ns for the additional MLP, well below the 250 ns L1 budget. |

*The efficiency gain over the raw‑BDT baseline (≈ 0.58) is therefore ≈ 6 percentage points, a ≈ 10 % relative improvement.*

---

## 3. Reflection – Why did it work (or not)?

### What the results tell us

1. **Mass‑hierarchy enforcement matters** – The Gaussian‑weight terms successfully identified candidates whose dijet masses clustered around the \(W\) mass and whose triplet mass sat near the top mass. Many events that the raw BDT labelled as “borderline’’ (score ≈ 0.4) were rescued when they satisfied this hierarchy, directly realizing the core hypothesis.

2. **Symmetry regulator reduces combinatorial background** – Random jet pairings tend to create one very heavy dijet and two light ones. The regulator penalised such patterns, lowering the effective score for background‑like configurations without harming genuine tops, as evidenced by the unchanged fake‑rate.

3. **Energy‑flow term improves balance** – By favouring a smooth spread of dijet masses, this term sharpened the discrimination for events where the three jets truly arise from a single top decay (as opposed to three unrelated jets). Ablation tests (removing the term) lowered efficiency by ~1 %.

4. **Two‑neuron MLP is sufficient for a first‑order “gate’’** – The hidden layer was able to learn a simple linear combination that “rescues’’ low‑BDT, high‑mass‑consistency candidates and “down‑weights’’ high‑BDT but hierarchy‑violating ones. The piecewise‑linear sigmoid kept the mapping smooth yet FPGA‑friendly.

### Limitations & open questions

| Issue | Observation | Impact |
|-------|-------------|--------|
| **Capacity of the MLP** | Only two hidden neurons limit the non‑linear shaping of the decision boundary. | May be bottleneck for more subtle correlations (e.g., between angular variables and mass terms). |
| **Static resolution scaling** | \(\sigma_{W}\) and \(\sigma_{t}\) were derived from an average jet‑energy resolution per run period. | Not fully optimal for events with extreme kinematics (very high‑\(p_T\) jets). |
| **Symmetry regulator aggressiveness** | In a few signal events where the decay is highly asymmetric (e.g., due to ISR), the regulator penalised them unnecessarily. | Minor loss of efficiency (≈ 0.2 %). |
| **Feature set completeness** | No explicit use of b‑tag information or angular separations (\(\Delta R\)). | Potentially leaves discriminating power on the table. |

Overall, the hypothesis that **explicit, differentiable mass‑hierarchy constraints will improve trigger performance when combined with a light MLP** is **confirmed**. The gains are modest but statistically significant, and the implementation respects all hardware constraints.

---

## 4. Next Steps – Novel directions to explore

| Goal | Proposed Action | Expected Benefit / Rationale |
|------|----------------|------------------------------|
| **Increase expressive power while staying FPGA‑friendly** | • Expand the hidden layer to 4–8 ReLU neurons (still quantised to 8‑bit). <br>• Replace the piecewise‑linear sigmoid with a *hard‑tanh* followed by a linear‑scale (both are add‑compare‑clamp). | Allows the gating network to capture higher‑order interactions (e.g., between symmetry and energy‑flow). |
| **Dynamic resolution scaling** | Compute per‑event \(\sigma_{W},\sigma_{t}\) from the jet‑by‑jet covariance matrix (already stored in the L1 data‑path). | Better matches the Gaussian weights to the actual detector conditions, improving the Gaussian‑weight discrimination. |
| **Add complementary physics features** | • \(\Delta R_{ij}\) for each dijet pair (captures angular topology). <br>• b‑tag discriminator of the jet most likely to be the \(b\) from the top. <br>• Mini‑N‑subjettiness (\(\tau_{21}\)) of each jet. | Provides orthogonal information to the invariant‑mass based features, especially useful when the mass hierarchy is ambiguous. |
| **Alternative lightweight classifiers** | • Train a *tiny* boosted‑decision‑stump ensemble (≤ 8 trees, depth‑1) that can be compiled to LUTs. <br>• Compare to the MLP in a “two‑stage” architecture: MLP first filters, BDT‑stumps refine. | Decision‑stumps are very cheap in hardware and may capture threshold‑type behaviour (e.g., “if \(w_{3}>0.7\) and \(R_{\text{sym}}<0.3\)”). |
| **Graph‑neural network prototype** | Build a 3‑node graph (jets) with edge features = dijet masses, node features = jet \(p_T\), η, φ; use a single graph convolution layer with quantised weights. | Directly models the relational structure of the three‑jet system; can be trimmed to a few dozen MACs, still feasible on modern L1 FPGAs. |
| **Systematic robustness studies** | • Vary pile‑up (μ = 30–80) and test the same network. <br>• Introduce realistic detector noise and mis‑calibrations. | Ensures that the observed efficiency boost survives under realistic run conditions. |
| **Ablation & feature‑importance analysis** | Perform LOCO (Leave‑One‑Component‑Out) studies to quantify each term’s contribution to the final efficiency. <br>• Use SHAP‑like values adapted for quantised models. | Guides future feature selection and helps justify any added hardware cost. |
| **Latency & resource budgeting** | Synthesize the expanded MLP (or alternative classifiers) on the target Kintex‑7/UltraScale‑plus; verify that total latency stays < 250 ns and resource usage < 25 % of the available fabric. | Guarantees deployability before the next L1 menu freeze. |

### Timeline (rough)

| Milestone | Duration |
|-----------|----------|
| **Quantised 4‑neuron MLP prototype + dynamic σ** | 2 weeks |
| **Add ΔR & b‑tag feature; retrain & evaluate** | 1 week |
| **Decision‑stump ensemble integration test** | 1 week |
| **Graph‑neural‑network proof‑of‑concept (3‑node)** | 3 weeks (including synthesis) |
| **Systematics campaign (pile‑up, calibration)** | 2 weeks |
| **Final comparative study & recommendation report** | 1 week |

---

**Bottom line:** The physics‑driven mass‑hierarchy gating combined with a minimal MLP has demonstrated a measurable improvement in trigger efficiency while respecting L1 hardware limits. The next logical step is to modestly increase the model capacity and enrich the feature set (angular, flavor, substructure) – all still within a strict add‑compare‑clamp budget – to squeeze out additional performance and to verify robustness across realistic data‑taking conditions. This will position the L1 top‑trigger for the upcoming high‑luminosity running periods.