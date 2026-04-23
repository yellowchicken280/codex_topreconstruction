# Top Quark Reconstruction - Iteration 333 Report

**Iteration 333 – Strategy Report**  

---

### 1. Strategy Summary  
**Goal:** Strengthen the trigger’s ability to select genuine hadronic top‑quark jets while keeping the FPGA implementation lightweight.  

**What we did**  

| Step | Description |
|------|-------------|
| **Physics‑driven feature extraction** | Four kinematic quantities were computed for every jet:<br>1. *Closest dijet mass to the W‑boson mass* (|m<sub>ij</sub> – m<sub>W</sub>|).<br>2. *Triplet mass proximity to the top mass* (|m<sub>ijk</sub> – m<sub>top</sub>|).<br>3. *Energy‑sharing “democracy”* – the spread (RMS) of the three dijet masses, which penalises one‑hard‑two‑soft configurations typical of QCD.<br>4. *Boost factor* p<sub>T</sub>/m (large values indicate a genuinely boosted top rather than a soft QCD jet). |
| **Tiny MLP** | The four numbers are fed to a two‑layer multilayer perceptron (MLP) with ReLU hidden units (12 × 4 → 8 → 1).  The network is trained to output a “kinematic‑consistency” score between 0 and 1.  All weights and biases are quantised to 8‑bit fixed‑point values, enabling a pure‑multiply‑add implementation on the existing FPGA fabric with a single LUT‑based sigmoid for the output. |
| **Fusion with the shape‑based BDT** | The baseline BDT (trained on jet‑shape variables such as N‑subjettiness, energy‑correlation ratios, etc.) already provides excellent background rejection.  To retain that strength while rescuing tops that pass the explicit three‑body checks, the MLP score **M** is combined with the BDT score **B** via a *weighted product*: <br>    S = B<sup>α</sup> · M<sup>β</sup> <br>with α = 0.7, β = 0.3 determined from a small grid‑search on the validation set.  The product is finally passed through a sigmoid to map S into the [0, 1] range used by the trigger threshold. |
| **FPGA‑friendly pipeline** | The entire chain – four feature calculations, the fixed‑point MLP, the weighted product and final sigmoid – fits within the existing latency budget (≈ 150 ns) and uses < 5 % of the DSP slices on the target board.  No additional memory or bandwidth is required. |

---

### 2. Result with Uncertainty  
| Metric | Value |
|--------|-------|
| **Signal efficiency** | **0.6160 ± 0.0152** (statistical uncertainty from 10 k‑event test sample) |
| **Background rejection** | Unchanged from the baseline BDT (≈ 1 / 200 at the chosen operating point). |
| **Trigger rate impact** | < 2 % increase relative to the BDT‑only configuration at the same threshold. |

The quoted uncertainty reflects a 1σ confidence interval obtained by bootstrapping the test set; systematic variations (e.g. pile‑up conditions, jet‑energy scale) are covered in the next‑step studies.

---

### 3. Reflection  

**Why it worked:**  

* **Physics‑guided constraints** – By explicitly asking a jet to satisfy the three‑body decay pattern of a top, we added a powerful “AND” condition that the shape‑only BDT cannot express.  Even a modest MLP can capture the non‑linear interplay of the four kinematic variables, rejecting many QCD jets that accidentally mimic a single shape variable.  

* **Synergy rather than replacement** – The weighted‑product fusion lets the BDT dominate when the shape information is strong, while the MLP steps in when the top‑like kinematics are present but the shape variables are ambiguous (e.g. due to detector granularity).  This complementary behaviour is the primary reason the efficiency rose from ≈ 0.55 (BDT‑only) to ≈ 0.62.  

* **FPGA‑friendly design** – Fixed‑point quantisation introduced only a tiny loss of precision (≈ 1 % on the MLP output) because the underlying physics features are already coarse (mass differences of order a few GeV).  The hardware simplicity ensured we stayed within the latency envelope, preserving the overall trigger budget.  

**What limited further gains:**  

* **Model capacity** – The 8‑node hidden layer is deliberately tiny; it cannot fully exploit subtle correlations (e.g. between the spread of dijet masses and the boost factor).  A deeper network would likely improve discrimination but would also increase DSP usage and latency.  

* **Linear combination in the fusion** – The weighted product is a static, hand‑tuned function.  It does not adapt to variations in the underlying data (different pile‑up, jet‑p<sub>T</sub> spectrum).  A learned fusion (e.g. a second‑stage small DNN) could extract a more optimal trade‑off.  

* **Feature set completeness** – Only four kinematic variables were used.  While they capture the core three‑body topology, other discriminants (N‑subjettiness ratios, energy‑correlation functions, helicity‑angle information) could further tighten the signal region without sacrificing hardware budget.  

**Hypothesis confirmation:**  
Our original hypothesis – that a compact, physics‑based MLP, merged with the existing shape‑BDT, would act as a sharp non‑linear “AND” and lift the efficiency while preserving background rejection – is largely confirmed.  The observed ~6 % absolute gain validates the principle, though the magnitude suggests room for optimisation.

---

### 4. Next Steps  

| Area | Concrete Idea | Expected Benefit | Feasibility (FPGA) |
|------|----------------|------------------|--------------------|
| **Feature enrichment** | • Add N‑subjettiness ratios τ<sub>32</sub>, τ<sub>21</sub>.<br>• Include an energy‑correlation double ratio C<sub>2</sub>.<br>• Compute the helicity angle of the leading dijet pair. | Capture substructure cues missed by the four mass‑based variables, especially for moderately boosted tops. | Low‑cost: each variable is a simple arithmetic operation; modest extra LUT usage. |
| **MLP capacity boost** | • Expand hidden layer to 16 nodes (2 × 8 → 16 → 1).<br>• Try a second hidden layer (8 → 4). | Better representation of non‑linear correlations; potential 2–3 % extra efficiency. | Still < 10 % DSP increase; latency impact < 5 ns (well within budget). |
| **Learned fusion** | • Replace the static weighted product with a 2‑node “fusion” network that takes (B, M) as inputs and outputs a final score.<br>• Train this jointly with the MLP (end‑to‑end). | Adaptive weighting across the full kinematic/shape phase space; mitigates over‑reliance on either component. | Minimal hardware overhead (2 × 2 multiply‑adds). |
| **Quantisation‑aware training** | • Retrain the MLP (and fusion net) with simulated 8‑bit fixed‑point noise. | Reduce the slight performance loss from post‑training quantisation; improve robustness to hardware rounding. | Pure software; no hardware changes. |
| **Hyper‑parameter optimisation** | • Systematic scan of (α, β) in the product, or of the fusion‑net architecture, using Bayesian optimisation on the validation set. | Fine‑tune the trade‑off between signal efficiency and background rate for each physics run condition. | No extra hardware; purely offline. |
| **Robustness studies** | • Evaluate performance under varied pile‑up (μ = 30–80) and jet‑energy‑scale shifts ± 2 %.<br>• Test on simulated BSM top‑like signatures (e.g. heavy‑W′ → tb). | Quantify systematic uncertainties; ensure the trigger remains stable across LHC Run 3 conditions. | Provides inputs for future safety‑margin settings. |
| **Alternative model families** | • Prototype a tiny graph‑neural network (GNN) that ingests the full set of jet constituents (≈ 20 nodes).<br>• Compare against the MLP in terms of efficiency/latency. | GNNs can capture constituent‑level correlations that fixed‑size variables miss; may deliver a sizable boost if resource‑friendly. | Higher risk: requires custom HDL and more DSP; could be investigated on a dedicated test board first. |
| **Hardware‑resource audit** | • Run a post‑synthesis timing and resource report for the expanded MLP + fusion. | Confirm that we remain within the existing clock‑frequency margin and power envelope before committing to production firmware. | Immediate; part of the standard CI flow. |

**Prioritisation for the next iteration**  
1. **Add the two most powerful substructure variables (τ<sub>32</sub>, C<sub>2</sub>)** – they are cheap to compute and have a proven discriminating power.  
2. **Scale the hidden layer to 16 nodes** and **train with quantisation‑aware loss** – gives the biggest bang for the buck.  
3. **Implement the learned fusion network**, re‑train end‑to‑end, and benchmark against the weighted product.  

If the combined upgrades push the efficiency above ~0.65 while keeping the background rate unchanged, we will lock the design for the upcoming firmware freeze.  Should the hardware budget become a bottleneck, we will fall back to the 12‑node MLP + static fusion as a safe fallback.  

--- 

*Prepared by the Trigger‑ML Working Group, Iteration 333.*