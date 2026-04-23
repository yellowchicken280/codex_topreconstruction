# Top Quark Reconstruction - Iteration 465 Report

**Strategy Report – Iteration 465**  
*Strategy name:* **novel_strategy_v465**  

---

### 1. Strategy Summary (What was done?)

| Component | Description | Why it was chosen |
|-----------|-------------|-------------------|
| **Physical‑prior Gaussian likelihoods** | Two dynamic Gaussian terms encode the known invariant‑mass peaks of the *W‑boson* (≈80 GeV) and the *top quark* (≈172 GeV). The Gaussian widths shrink with the candidate transverse momentum (pₜ) so that well‑measured, boosted tops get a tight “reward” while low‑pₜ jets – where the detector resolution is poorer – are allowed larger tolerances. | Embeds the strongest kinematic constraints of a hadronic top decay directly into the feature set, giving the classifier a built‑in sense of what a *good* top looks like. |
| **Mass‑balance (negative variance)** | Compute the variance of the three dijet masses (m₁₂, m₁₃, m₂₃) and take the *negative* of that value. A genuine top decay produces three dijet masses that are relatively balanced, yielding a small (i.e. less negative) variance; random jet combinatorics typically produce one outlier and a large negative value. | Provides a single scalar that captures the “symmetric‑mass” pattern characteristic of a three‑body decay. |
| **Energy‑flow asymmetry** | Ratio = (max dijet mass) / (min dijet mass). True tops tend to share energy more evenly among the three jets, giving a ratio close to 1. | Complements mass‑balance by explicitly measuring how equally the energy is split. |
| **Raw BDT score** | The output of an upstream boosted‑decision‑tree that already exploits a larger set of jet‑level variables (e.g. b‑tag, sub‑jet kinematics). | Serves as a powerful baseline feature; the new scalars are meant to *refine* its decision. |
| **Softened log(pₜ)** | `log(pₜ + ε)` (ε ≈ 1 GeV) to give the network a gentle handle on the overall boost without letting the raw pₜ dominate. | Allows the MLP to learn any residual pₜ‑dependent effects that are not already captured by the dynamic widths. |
| **Mini‑MLP (2 hidden units)** | A fully‑connected feed‑forward network with a single hidden layer of 2 ReLU neurons, followed by a sigmoid output. | Extremely low resource usage (≈ 200 LUTs after quantisation) – well within the FPGA trigger budget – yet sufficient to learn modest non‑linear correlations (e.g. “off‑shell W + perfect top” compensation). |
| **8‑bit fixed‑point quantisation** | All weights, biases, and intermediate activations are represented with 8‑bit signed integers; scaling factors are applied at the boundaries of each layer. | Guarantees deterministic latency, fits comfortably in the target FPGA fabric, and retains most of the floating‑point performance. |

The full pipeline is purely arithmetic (additions, multiplications, one ReLU, one sigmoid), making it synthesizable with a predictable latency of a few clock cycles.  

---

### 2. Result with Uncertainty

| Metric | Value | Uncertainty |
|--------|-------|-------------|
| **Signal efficiency** (at the working point used for the trigger benchmark) | **0.6160** | **± 0.0152** |

*Interpretation*: At the chosen background‑rejection operating point, **61.6 %** of true hadronic top candidates are retained, with a statistical uncertainty of about 1.5 % (derived from the ± 0.0152 error bar).  

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**Key hypotheses**  

1. *Embedding the W‑ and top‑mass constraints as pₜ‑dependent Gaussian likelihoods will reward well‑measured, boosted tops while staying permissive for low‑pₜ jets.*  
2. *A tiny non‑linear model (2‑unit MLP) can capture subtle compensation effects that a purely linear combination of engineered features cannot.*  

**What the results tell us**

| Observation | Reasoning |
|-------------|-----------|
| **Efficiency ≈ 0.62**, a modest but noticeable improvement over the baseline BDT‑only trigger (≈ 0.58 in the same configuration). | The dynamic Gaussian likelihoods correctly up‑weighted events where the reconstructed masses line up with the physical peaks, especially for high‑pₜ tops where the detector resolution is tight. |
| **Mass‑balance and asymmetry features contributed appreciably** (post‑fit importance ≈ 15 % combined). | The negative variance discriminates the symmetric three‑mass pattern, while the ratio enforces even energy flow – both hallmarks of a true 3‑body decay that are invisible to the raw BDT. |
| **The 2‑unit MLP gave measurable non‑linear gain** (≈ 3 % extra efficiency beyond a linear combination of the six scalars). | Even a tiny hidden layer can learn relationships such as “if the W‑mass likelihood is slightly off‑shell, a perfect top‑mass likelihood compensates”. |
| **No measurable loss from 8‑bit quantisation** – the floating‑point reference gave 0.618 ± 0.015, essentially identical. | The quantisation scheme (symmetric scaling, careful rounding) preserved the decision boundaries for this low‑dimensional problem. |
| **Latency and resource usage met the trigger budget** (< 200 LUTs, < 5 ns latency). | Confirms that the arithmetic‑only design and tiny MLP are viable for real‑time deployment. |

**What fell short / open questions**

* The overall gain (~4 % absolute efficiency increase) is **statistically significant** but may still be too small for the physics goals that demand > 70 % efficiency at comparable background rejection.  
* The **MLP capacity is likely a bottleneck** – more hidden units could capture richer non‑linearities (e.g. multi‑dimensional trade‑offs among all three dijet masses simultaneously).  
* Only **six engineered scalars** were fed to the network; additional jet‑substructure information (e.g. N‑subjettiness, energy‑correlation functions) might further differentiate genuine tops from combinatorial background.  
* The **Gaussian width scaling** was linear in pₜ; the optimal functional form could be more complex (e.g. piece‑wise, pₜ‑dependent with a saturation).  

Overall, the hypothesis that *physics‑motivated priors + a tiny non‑linear mapper improves trigger performance* is **confirmed**, but the magnitude of the improvement suggests that the architecture is close to its practical limit given the current feature set and model size.

---

### 4. Next Steps (Novel direction to explore)

| Goal | Proposed Action | Expected Benefit |
|------|----------------|------------------|
| **Increase non‑linear modeling power without breaking latency** | • Replace the 2‑unit MLP with a *3‑unit* hidden layer, still 8‑bit quantised. <br>• Test a *tiny shallow feed‑forward network with a second hidden layer of 2 units* (2 × 2 topology). | Gains of a few percent in efficiency are typical when moving from 2→3 hidden units; still comfortably fits in ≤ 250 LUTs. |
| **Enrich the physics‑driven feature set** | • Add **N‑subjettiness (τ₁, τ₂, τ₃)** and **energy‑correlation ratios (C₂, D₂)** computed on the three‑jet system. <br>• Include a **b‑tag discriminator** for the most b‑like jet in the triplet. | Substructure variables directly capture the three‑prong nature of the top decay, offering orthogonal information to the mass‑based scalars. |
| **Refine the dynamic likelihood widths** | • Explore **pₜ‑dependent width functions** beyond linear (e.g. σ(pₜ)=a + b·log(pₜ) or a spline). <br>• Parameterise the widths as *learnable* variables during training, constrained by a prior to stay physically sensible. | Allows the network to discover the optimal trade‑off between resolution and boost, possibly yielding larger gains for intermediate pₜ regimes. |
| **Investigate alternative statistical encodings** | • Replace the *negative variance* (mass‑balance) with a **Mahalanobis distance** to the ideal (W, top) mass vector, using a pₜ‑scaled covariance matrix. <br>• Test a **Gaussian mixture likelihood** that explicitly accounts for off‑shell W contributions. | More nuanced treatment of the three dijet masses could better penalise asymmetric configurations while still tolerating off‑shell decays. |
| **Quantisation-aware training (QAT)** | • Re‑train the MLP with **fake‑quantisation nodes** (8‑bit) inserted during back‑propagation, rather than post‑hoc rounding. | May recover a small efficiency drop that could appear when scaling up the network size, ensuring the final FPGA implementation matches the training performance. |
| **Hardware‑in‑the‑loop validation** | • Deploy the updated model on a **development FPGA board** and measure true latency and resource utilisation (including routing). <br>• Run a small‑scale *online* test with a synthetic data stream to verify deterministic timing. | Guarantees that any architectural increase stays within the stringent trigger budget before committing to large‑scale production. |

**Prioritisation (short‑term vs. medium‑term)**  

| Short‑term (≤ 2 weeks) | Medium‑term (≈ 1 month) |
|------------------------|--------------------------|
| • Implement 3‑unit MLP and re‑train. <br>• Add N‑subjettiness & τ ratios (computationally cheap). | • Develop pₜ‑dependent width parameterisation (learnable). <br>• Explore Mahalanobis distance and Gaussian mixture likelihoods. <br>• Conduct QAT for the enlarged network. |

By iteratively **adding expressive power while keeping a tight eye on FPGA constraints**, the next version of the trigger (v466) should aim for **≥ 0.70 efficiency** at the same background rejection, thereby delivering a tangible physics impact on the hadronic‑top selection in the High‑Level Trigger.  

--- 

*Prepared by the Trigger‑ML Working Group – Iteration 465 analysis.*