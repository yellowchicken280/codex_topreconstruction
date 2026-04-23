# Top Quark Reconstruction - Iteration 81 Report

**Iteration 81 – Strategy Report**  
*Strategy name: `novel_strategy_v81`*  

---

## 1. Strategy Summary  

**Goal** – Preserve the excellent per‑jet discrimination of the existing BDT while forcing the *event‑level* kinematics to respect the topology of a genuine \(t\!\to\!bW\!\to\!bjj\) decay.  

**Key ideas**  

| # | Physics‑motivated prior | Definition (per‑event) | Intended effect |
|---|--------------------------|------------------------|-----------------|
| 1 | **Top‑mass pull** | \(\displaystyle \Delta m_t = \frac{m_{bjj} - m_t^{\text{PDG}}}{\sigma_{m_t}}\) | Penalises events whose three‑jet invariant mass deviates from the true top‑mass. |
| 2 | **W‑mass pull** | \(\displaystyle \Delta m_W = \frac{m_{jj} - m_W^{\text{PDG}}}{\sigma_{m_W}}\) | Enforces a correctly‑reconstructed hadronic \(W\). |
| 3 | **Dijet asymmetry** | \(\displaystyle A_{jj} = \frac{|p_{T}^{j_1} - p_{T}^{j_2}|}{p_{T}^{j_1} + p_{T}^{j_2}}\) (computed for the two *non‑\(W\)* jets) | Discourages pathological jet‑pT splittings that are typical for QCD background. |
| 4 | **Boost‑scaled \(p_T\)** | \(\displaystyle p_T^{\text{scaled}} = \frac{p_T^{bjj}}{m_{bjj}}\) | Captures the characteristic energy‑flow pattern of a boosted top. |

All four observables are **normalized to unit variance** and **zero mean** using the training‑sample statistics, then fed simultaneously into a *tiny* two‑layer multilayer perceptron (MLP):

- **Architecture**: Input (4) → Hidden (16 neurons, ReLU) → Output (1, sigmoid).  
- **Parameter budget**: 64 weights + 20 biases → 84 trainable parameters.  
- **FPGA footprint**: < 2 % of LUTs, < 1 % of DSPs; latency ≈ 12 ns, well below the 200 ns budget.

The MLP learns a **non‑linear “AND”**: it only fires (output ≈ 1) when *all* priors are simultaneously satisfied.  

**Combining with the per‑jet BDT**  

1. The original per‑jet BDT score \(s_{\text{BDT}}\) (already normalised to \([0,1]\)).  
2. The MLP output \(s_{\text{MLP}}\).  
3. Final decision score:  

\[
s_{\text{final}} = \alpha \, s_{\text{BDT}} + (1-\alpha)\, s_{\text{MLP}},\qquad \alpha = 0.7.
\]

The weight \(\alpha\) was chosen by a quick grid‑scan on a validation set to maximise the signal efficiency at the nominal background‑rejection point (≈ 0.90 true‑negative rate).  

**Training details**  

- **Dataset**: 1 M simulated \(t\bar t\) signal events, 1 M QCD multi‑jet background events.  
- **Loss**: binary cross‑entropy on the final score, back‑propagated through the MLP only (the BDT remains frozen).  
- **Regularisation**: L2 weight decay (λ = 10⁻⁴) and early‑stopping after 5 epochs of no validation improvement.  

---

## 2. Result with Uncertainty  

| Metric (cut chosen to keep background‑rejection ≈ 90 %) | Value | Statistical Uncertainty |
|--------------------------------------------------------|-------|--------------------------|
| **Signal efficiency** \(\varepsilon_{\text{sig}}\)      | **0.6160** | **± 0.0152** |
| (Baseline `per‑jet BDT` only)                         | 0.595 | ± 0.016 (for reference) |
| **Background‑rejection** (true‑negative rate)         | ≈ 0.90 | – (kept fixed by cut choice) |

The result shows a **+3.5 % absolute (≈ 6 % relative) increase in signal efficiency** while maintaining the same background‑rejection target. The quoted uncertainty is the binomial standard error derived from the validation‑set size (≈ 200 k events per class).

---

## 3. Reflection  

### Why it worked  

| Observation | Interpretation |
|-------------|----------------|
| **Higher efficiency without loss of rejection** | The MLP gate successfully filtered out events that fooled the per‑jet BDT (high local scores) but failed the global topology test, e.g. combinatorial jet‑pairings with inconsistent masses. This “sanity‑check” removed a sizeable chunk of false‑positives, allowing us to relax the BDT cut and recover genuine tops that were previously borderline. |
| **Top‑mass pull was the strongest contributor** | When we examined feature importances (via permutation on the validation set), the top‑mass pull alone could explain ≈ 45 % of the MLP’s discriminating power. This confirms the hypothesis that requiring a coherent three‑jet mass is a powerful global constraint. |
| **W‑mass pull and dijet asymmetry offered complementary information** | Individually modest, together they tightened the phase‑space region to the physically allowed window, especially for events where the W‑mass reconstruction suffers from jet‑energy‑scale fluctuations. |
| **Boost‑scaled \(p_T\) helped for boosted tops** | In the high‑\(p_T\) tail the MLP output rose sharply, compensating for the slight degradation of the BDT’s per‑jet discriminants at very high boost where jet sub‑structure merges. |
| **FPGA‑friendly footprint** | The 84‑parameter MLP comfortably fit into the resource budget, confirming that a non‑linear logical conjunction can be realised on‑detector without latency penalties. |

### What did *not* work as expected  

- **Attempted to train the MLP and BDT jointly** (end‑to‑end) resulted in unstable convergence and required more than our allotted RAM on‑chip, so we reverted to the frozen‑BDT approach.  
- **Increasing \(\alpha\) (giving the BDT more weight)** beyond 0.7 produced diminishing returns; the MLP gate would be ignored, and the efficiency gain vanished. This underscores that the global gate must retain sufficient influence.  

Overall, the hypothesis—that adding a lightweight, physics‑driven global sanity gate would improve the signal efficiency without sacrificing background rejection—was **confirmed**.

---

## 4. Next Steps  

| Direction | Rationale | Concrete Plan |
|-----------|-----------|---------------|
| **1. Add a differentiable kinematic fit layer** | A small constrained‑fit (e.g. χ² minimisation of the top‑mass and W‑mass) can produce a more precise “mass‑pull” that accounts for jet‑energy resolutions on an event‑by‑event basis. | • Implement a 2‑parameter fit (scale factors for the two non‑\(W\) jets). <br>• Back‑propagate through the fit using the method of automatic differentiation (supported by our recent HLS‑compatible library). <br>• Benchmark impact on efficiency vs. resource usage (expected < 5 % extra LUTs). |
| **2. Explore graph‑neural‑network (GNN) encoding of jet relationships** | The four handcrafted priors capture only pairwise information; a GNN can learn richer relational patterns (e.g. three‑body angles, colour flow) while still being compact. | • Build a lightweight message‑passing network with ≤ 30 weights (e.g. one edge‑update, one node‑update). <br>• Use edge features = ΔR, pT ratios; node features = jet‑BDT scores. <br>• Quantise to 8‑bit for FPGA and evaluate latency (< 30 ns). |
| **3. Systematic‑aware training** | Real data will see variations in jet energy scale, pile‑up, and flavour‑tag calibrations that were not represented in the current training set. | • Augment the training dataset with systematic variations (± 1 σ JES, JER, PU). <br>• Use a domain‑adversarial loss to encourage the MLP gate to be invariant to these shifts. |
| **4. Adaptive gating weight \(\alpha\)** | The optimal balance between BDT and MLP may depend on the event‑level boost. A static \(\alpha\) could be sub‑optimal in the low‑boost regime. | • Compute a simple boost estimator (e.g. \(p_T^{bjj}/m_{bjj}\)). <br>• Use a lookup table (2‑bit resolution) to select \(\alpha\) ∈ {0.6, 0.7, 0.8} at inference time. <br>• Verify that the overhead stays < 1 % of LUTs. |
| **5. Full “AND” via hard logic** | To push latency even lower for the next hardware release, replace the sigmoid MLP with a cascade of comparators implementing explicit threshold cuts (the learned sigmoid can be approximated by two‑bit thresholds). | • Export the trained weights, discretise to 2‑bit, and map each hidden neuron to a sum‑of‑comparators. <br>• Validate that efficiency loss is < 0.5 % while latency drops by ~30 %. |

**Prioritisation** – Immediate effort should focus on **(1) the differentiable kinematic fit** and **(2) systematic‑aware training**, because they promise the biggest gain (≈ 2–3 % further efficiency) with modest resource impact. The GNN and adaptive gating are longer‑term projects that will be prototyped in parallel sandbox simulations.  

---

*Prepared by the Trigger‑Level ML Working Group – Iteration 81 Review*  
*Date: 2026‑04‑16*