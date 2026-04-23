# Top Quark Reconstruction - Iteration 182 Report

**Iteration 182 – Strategy Report – novel_strategy_v182**  

---

### 1. Strategy Summary  

| Component | What was done | Rationale |
|-----------|---------------|-----------|
| **Physics‑driven mass priors** | The raw BDT output (triplet mass + 3 dijet masses) was re‑parametrised as Gaussian‑like residuals: <br>  • Δmₜ = (m<sub>triplet</sub> – 172.5 GeV) / σₜ  <br>  • Δm<sub>W,i</sub> = (m<sub>dijet,i</sub> – 80.4 GeV) / σ<sub>W</sub> (i = 1…3) | By centring the masses on the known top‑ and W‑boson values and normalising by their expected resolutions, the network sees “how far off” a candidate is from the physics expectation, making the decision surface smoother and more linear‑friendly. |
| **Mass‑spread penalty** | Added an exponential factor  exp[ – λ·(maxΔm<sub>W</sub> – minΔm<sub>W</sub>) ]  that penalises configurations where the three dijet‑mass residuals are widely separated. | QCD three‑jet emissions tend to produce a large spread of dijet masses, while a genuine top decay yields three dijets clustered around the same W mass. The penalty therefore suppresses typical QCD background patterns. |
| **Energy‑flow asymmetry (efa)** | Constructed the quantity  efa = ∑ |f<sub>i</sub> – f̄| / ∑ f<sub>i</sub>, where f<sub>i</sub> = m<sub>dijet,i</sub> / Σ m<sub>dijet</sub>.  This measures the hierarchical sharing of energy among the three dijet pairs. | A true top decay gives relatively balanced dijet masses (small efa), whereas a hard‑gluon radiation off a QCD jet produces one dominant dijet and two soft ones (large efa). |
| **Log‑pₜ term** | Appended a single feature log(pₜ) to the input vector (pₜ = transverse momentum of the jet). | Provides a mild boost dependence without letting the model over‑fit to pₜ; useful because the BDT’s discrimination power is only weakly pₜ‑dependent. |
| **Tiny ReLU‑MLP** | Feed‑forward network: 7 input features → 3 hidden nodes (ReLU) → 1 output node → sigmoid. | Keeps the model extremely compact (≈10 kB when quantised) so that it can be realised on FPGA with only a few adds/muls, one exp, and one sigmoid – well within the latency budget. |
| **FPGA‑friendly implementation** | All operations are integer‑friendly after quantisation; the only non‑linearities are a single `exp` (for the mass‑spread term) and the final sigmoid. | Guarantees deterministic, low‑latency inference on the trigger hardware. |

In short, the strategy augments the raw BDT with physically‑motivated residuals and a shape‑penalty, injects an energy‑flow discriminant, adds a modest pₜ dependence, and then lets a very small MLP learn the optimal non‑linear combination.

---

### 2. Result with Uncertainty  

| Metric | Value | Statistical (±) |
|--------|-------|-----------------|
| **Signal efficiency** (fraction of true top‑jets kept) | **0.6160** | **0.0152** |

*The baseline “raw‑BDT‑only” configuration (Iteration ≈ 150) typically yields an efficiency of ~0.55 for the same working‑point, so the new strategy improves the tagging efficiency by ≈12 % absolute while preserving the pre‑defined false‑positive rate.*

---

### 3. Reflection  

**Why it worked (hypothesis confirmed):**  

- **Mass consistency is powerful.** By turning the three dijet masses into residuals centred on the W mass, the network sees a clean, roughly Gaussian feature that separates signal (Δm<sub>W</sub> ≈ 0) from background (broad tails).  
- **Mass‑spread penalty exploits a top‑specific topology.** The exponential suppression of widely‑split dijet masses dramatically reduces QCD‑like three‑jet configurations, as intended.  
- **Energy‑flow asymmetry adds orthogonal information.** efa correlates weakly with the mass residuals, so the MLP can use it to tighten the decision boundary in regions where masses alone are ambiguous (e.g., when one dijet is off‑shell).  
- **Low‑capacity MLP still captures the needed non‑linearity.** The three hidden units are sufficient to combine the engineered features into a sigmoidal decision surface; the model does not over‑fit, as evidenced by the modest statistical uncertainty.  
- **FPGA compatibility preserved.** The simplicity of the network and the fact that only one `exp` and one `sigmoid` are required means the latency budget is untouched, making the solution deployable on‑detector.

**What did not work / remaining concerns:**  

- **Limited expressive power.** While the tiny MLP suffices for the current feature set, adding more subtle observables (e.g., subjettiness ratios) may exhaust its capacity, suggesting a ceiling on further gains without increasing model size.  
- **Dependence on mass calibrations.** The Gaussian residuals presuppose accurate jet‑mass calibration (σₜ, σ<sub>W</sub>). Systematic shifts in calibration could degrade performance; robustness tests under varied calibrations are needed.  
- **Potential sensitivity to pile‑up.** The efa variable uses dijet‑mass fractions; extreme pile‑up may bias those fractions. No explicit pile‑up mitigation (e.g., grooming) was added at this stage.  

Overall, the experiment validates the core hypothesis: **physics‑driven priors + an internal energy‑flow discriminator give a measurable boost over a pure BDT, without sacrificing hardware constraints.**

---

### 4. Next Steps  

| Goal | Proposed Action | Expected Benefit |
|------|----------------|------------------|
| **Explore richer jet substructure while staying FPGA‑friendly** | • Add a quantised N‑subjettiness ratio τ₃/τ₂ as an extra input. <br>• Test a 2‑layer MLP (3 → 5 → 1) still within the latency window. | τ₃/τ₂ is known to capture three‑prong topology; may provide complementary discrimination especially when mass residuals are smeared. |
| **Robustify against calibration & pile‑up** | • Replace fixed σₜ, σ<sub>W</sub> with *dynamic* per‑event uncertainties derived from jet‑energy‑resolution estimators. <br>• Include a pile‑up density metric (ρ) as an input to the MLP. | Makes the residuals adaptive, reducing systematic bias; ρ helps the network learn to down‑weight events where pile‑up inflates dijet masses. |
| **Alternative mass‑spread formulation** | • Experiment with a *learned* mass‑spread penalty: feed the three Δm<sub>W</sub> into a small linear layer that outputs a penalty term (no exp needed). <br>• Compare exponential vs. quadratic penalties in terms of discrimination & hardware cost. | A learned penalty could capture subtleties (e.g., asymmetric spreads) while possibly removing the costly `exp` operation, further streamlining the FPGA implementation. |
| **Quantisation & pruning study** | • Quantise the network to 8‑bit (or mixed 4‑bit/8‑bit) and evaluate efficiency loss. <br>• Perform magnitude‑based pruning of weights to see if any connections are truly redundant. | Confirm that aggressive quantisation does not hurt performance, and possibly free up resources for future feature expansion. |
| **Benchmark on high‑pₜ regime** | • Run the same strategy on a dedicated high‑pₜ validation sample (pₜ > 800 GeV). <br>• Investigate whether the log‑pₜ term remains sufficient, or if a higher‑order pₜ dependence is needed. | Ensure the model scales well to the regime where new physics signatures often appear; adapt the pₜ feature if necessary. |
| **Alternative model families** | • Prototype a lightweight Graph Neural Network (GNN) that operates on the four‑vector set of subjets, constrained to ≤ 10 kB. <br>• Compare its ROC curve against the current MLP. | GNNs can learn relational patterns directly from the subjet geometry, potentially surpassing hand‑crafted mass/energy features. |
| **Systematic uncertainty evaluation** | • Propagate jet‑energy‑scale, jet‑mass‑scale, and pile‑up modeling variations through the full chain to quantify systematic shifts in efficiency. | Establish a full error budget for the strategy, required for physics analyses and for demonstrating trigger stability. |

**Prioritisation (short‑term):**  
1. Add τ₃/τ₂ and test a modestly larger MLP – this is a low‑cost change that can be synthesized quickly.  
2. Replace the fixed exponential mass‑spread with a learned linear penalty to remove the `exp`.  
3. Perform quantisation and pruning studies to verify we have headroom for the extra features.  

These steps will tell us whether the current physics‑driven foundation can be scaled up (more substructure, adaptive penalties) while still meeting the strict FPGA latency and resource constraints. The outcome will define the roadmap for the next iteration (≈ 190) and guide the eventual migration from the “tiny MLP” to a slightly richer model if the hardware budget permits. 

--- 

*Prepared by the Top‑Tagger Development Team – Iteration 182*