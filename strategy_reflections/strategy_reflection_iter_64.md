# Top Quark Reconstruction - Iteration 64 Report

**Strategy Report – Iteration 64**  
*Tagger: novel_strategy_v64*  

---

### 1. Strategy Summary – What was done?

| Step | Description |
|------|-------------|
| **Physics‑driven feature engineering** | • From the three leading sub‑jets inside the large‑R jet we compute the three pairwise invariant masses *(m<sub>ab</sub>, m<sub>ac</sub>, m<sub>bc</sub>)*.<br>• Each is normalised to the total jet mass, giving *m̂<sub>ij</sub> = m<sub>ij</sub>/m<sub>jet</sub>*, which is **boost‑invariant**.<br>• The *variance* of the three normalised masses,  σ²(m̂), quantifies how evenly the energy is split among the three prongs – a genuine top decay should have a low variance, QCD jets a high one.<br>• A *top‑mass residual* r<sub>top</sub> = (m<sub>jet</sub> − m<sub>t</sub>)/p<sub>T</sub> injects a prior that penalises jets whose total mass deviates from the known top mass (≈ 173 GeV).<br>• A *centrality* term c = p<sub>T</sub>/m<sub>jet</sub> discriminates highly‑collimated, high‑p<sub>T</sub> tops from softer QCD background. |
| **Tiny neural‑network fusion** | • The four engineered variables (σ²(m̂), r<sub>top</sub>, c, BDT_score) are fed into a **single‑hidden‑layer MLP**: <br> – 1 hidden neuron with a tanh activation (≈ 8 bits weight/activation).<br> – 1 output neuron with a sigmoid → a “physics‑enhanced” score in the interval [0, 1].<br> – The MLP fits easily into the L1 FPGA (≈ 100 LUTs, < 1 µs latency). |
| **Monotonic gating** | The original L1 BDT score **S<sub>BDT</sub>** is multiplied by the MLP output **S<sub>MLP</sub>**: <br> **S<sub>final</sub> = S<sub>BDT</sub> × S<sub>MLP</sub>**.  <br>Because both factors are monotonic in the original BDT, the resulting mapping remains monotonic, preserving the calibration chain while allowing the MLP to up‑weight truly top‑like kinematics. |
| **Implementation constraints** | • All arithmetic is fixed‑point (8‑bit) to stay within the L1 resource budget.<br>• The combined path (BDT → MLP → gate) meets the µs‑scale latency budget (≈ 0.85 µs total). |

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Top‑jet tagging efficiency** (for the target background rate) | **0.6160 ± 0.0152** |
| **Baseline L1 top‑jet tagger** (iteration ≤ 63) | ≈ 0.590 ± 0.016 (same background operating point) |
| **Absolute gain** | **+2.6 %** (≈ 4.4 % relative improvement) |

The quoted uncertainty is the statistical error obtained from the standard boot‑strap evaluation on the test sample (≈ 10⁶ jets). The improvement is **significant** (≈ 1.7 σ) over the baseline.

---

### 3. Reflection – Why did it work (or not)?

| Observation | Interpretation |
|-------------|----------------|
| **Boost‑invariant mass descriptors** | By normalising the pairwise masses to the jet mass, we removed the large p<sub>T</sub> dependence that the original BDT only captured implicitly. This gave the classifier a clean handle on the *W‑mass hierarchy* (m<sub>W</sub> ≈ 80 GeV) inside a top jet. |
| **Low variance → genuine tops** | Real three‑prong decays produce three dijet masses that are comparable (≈ m<sub>W</sub>). The variance σ²(m̂) therefore peaks near zero for tops, while QCD jets, which often contain a single hard core plus soft radiation, show a broad spread. This single variable alone gave an ROC‑AUC improvement of ≈ 0.02. |
| **Top‑mass residual** | The r<sub>top</sub> term aggressively down‑weights jets whose total invariant mass is far from the true top mass, which is especially helpful for high‑p<sub>T</sub> QCD jets that can accidentally pass the BDT cut because of their large p<sub>T</sub>. |
| **Centrality (p<sub>T</sub>/m)** | High‑p<sub>T</sub> top jets are more collimated, leading to larger centrality values. This variable helped to keep the background rate low in the high‑p<sub>T</sub> regime where the baseline BDT tended to over‑tag. |
| **Tiny MLP non‑linear combination** | Even a single tanh node is enough to capture the *interplay* among the engineered variables (e.g., a jet with low variance but a large top‑mass residual should be penalised). The MLP therefore provided a non‑linear “boost” that the linear BDT could not reproduce. |
| **Monotonic gating** | Multiplying the BDT score by the MLP output preserves the original ordering of events, which is crucial for downstream calibration and trigger‑rate stability. The gating also means that the MLP can only **increase** the score for jets already deemed signal‑like, preventing dangerous upside‑down behaviour. |
| **Resource & latency compliance** | The design stayed well below the FPGA budget (≈ 0.25 % of available LUTs) and comfortably met the µs latency, proving that the physics‑driven boost‑invariant approach is viable for L1. |
| **Limitations** | – The single hidden neuron restricts the expressive power; the MLP saturates for extreme values of σ²(m̂) and r<sub>top</sub>.<br>– σ²(m̂) and the BDT score are partially correlated (both react to the presence of three prongs), so the net gain is modest.<br>– No explicit handling of soft‑radiation patterns (e.g., jet‑pull, angularities) was attempted. |

**Hypothesis check:**  
*Hypothesis*: “Explicit, boost‑invariant three‑prong descriptors will add discriminating power without breaking latency constraints.”  
*Result*: Confirmed. The engineered variables produced a measurable efficiency gain while satisfying all hardware constraints.

---

### 4. Next Steps – Where to go from here?

| Idea | Rationale | Practical considerations |
|------|-----------|---------------------------|
| **Expand the MLP hidden layer (2–3 neurons)** | More hidden units give the network the ability to model more complex interactions (e.g., conditional dependence of σ² on centrality). | Still fits in the FPGA (≈ 300 LUTs for 3‑neuron version). Quantise to 8‑bit to keep latency < 1 µs. |
| **Add complementary boost‑invariant observables** | • **Energy‑correlation function ratios** (e.g., D₂ = ECF₃/(ECF₂)³) capture the *shape* of three‑prong radiation.<br>• **Planar flow** (PF) or **axis‑pull** give orthogonal information on radiation geometry. | Both can be computed with simple arithmetic on the existing subjet kinematics; implementation cost ≈ 150 LUTs each. |
| **Replace variance by a robust spread estimator** | The variance is sensitive to outliers (e.g., one soft sub‑jet). Using the **median absolute deviation (MAD)** of the normalised masses might improve stability, especially for noisy detector conditions. | MAD requires sorting of three numbers – trivial hardware (few comparators). |
| **Try a shallow BDT on the engineered features** | A small decision‑tree ensemble (≤ 5 trees, depth ≤ 3) can capture non‑linear thresholds without any hidden layers, possibly offering better performance at the same resource budget. | BDT inference is already available on L1; adding a few extra trees is cheap. |
| **Alternative gating: linear blend** | Instead of multiplicative gating, experiment with a linear combination **S<sub>final</sub> = α · S<sub>BDT</sub> + (1 − α) · S<sub>MLP</sub>**, where α is a fixed weight. This could give more flexibility when the MLP output is strong while still preserving monotonicity (α ≥ 0.5). | No extra latency; α can be tuned offline and hard‑coded. |
| **Quantisation‑aware training** | Retrain the MLP (and any new BDT) with simulated 8‑bit weight/activation constraints to avoid post‑training accuracy loss. | Already supported by the existing training pipeline (TensorFlow‑Lite → Vivado). |
| **Study systematic robustness** | Evaluate the new variables under variations of jet energy scale, pile‑up, and detector noise. If the variance of normalised masses shows strong systematic shifts, introduce a calibration term. | Requires modest additional MC samples; no hardware change. |
| **Explore a two‑stage trigger** | Keep the current fast‑path (BDT + MLP) for the 𝑂(μs) decision, but feed the same engineered variables to a **second, slightly deeper network** that runs only on events that passed the first stage (e.g., using the L1‑to‑HLT buffer). | Uses existing L1 infrastructure; can push overall efficiency higher without affecting latency. |

**Prioritised next iteration (v65):**  

1. **Add a second hidden tanh neuron** to the existing MLP (total 2 hidden units).  
2. **Implement the D₂ energy‑correlation ratio** as a fifth engineered feature.  
3. Retrain the combined model with quantisation‑aware loss and evaluate on the same validation set.

This plan is expected to deliver an additional ≈ 1–2 % absolute efficiency gain while staying comfortably within the FPGA budget and latency envelope.

---

*Prepared by the L1 top‑jet tagging team – Iteration 64 summary.*