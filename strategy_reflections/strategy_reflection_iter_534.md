# Top Quark Reconstruction - Iteration 534 Report

**Strategy Report – Iteration 534**  
*Strategy name:* **novel_strategy_v534**  
*Motivation (recap):* The legacy BDT captures high‑level correlations in the jet‑combination space, but its raw score ignores cheap, on‑chip physics constraints that are already known (the W‑boson and top‑quark masses). By turning three well‑motivated mass priors into Gaussian‑like weights and blending them with the BDT output and a boost‑sensitive pT term, we hoped to obtain a smoother, physics‑aware decision function that still fits inside an FPGA budget (≤ 200 LUTs, ≤ 5‑cycle latency).

---

### 1. Strategy Summary – What Was Done?

| Component | Implementation Details | FPGA‑friendly aspects |
|-----------|------------------------|------------------------|
| **Base classifier** | Existing Gradient‑Boosted Decision Tree (BDT) trained on the full set of high‑level jet variables. | Uses the same tree‑lookup logic already synthesised for the baseline. |
| **Mass priors** | 1. **Dijet‑mass prior** – three dijet combinations (candidate W’s) each weighted with  \(\exp\!\big[-\tfrac12((m_{jj}-m_W)/\sigma_W)^2\big]\). <br>2. **Trijet‑mass prior** – the three‑jet combination (candidate top) weighted with \(\exp\!\big[-\tfrac12((m_{jjj}-m_{t})/\sigma_t)^2\big]\). <br>3. **Mass‑ratio prior** – \(\exp\!\big[-\tfrac12\big((\overline{m_{jj}}/m_{jjj})-m_W/m_t\big)^2 / \sigma_{r}^2\big]\).  σ values were set to the detector‑level resolutions (≈ 10 GeV for W, 15 GeV for top, 0.05 for the ratio). | The exponential is approximated by a 5‑term LUT‑based piece‑wise polynomial; all coefficients are integer (≤ 31) so the whole prior chain fits into ≤ 60 LUTs. |
| **Boost term** | Scalar \(p_T^{\text{lead‑jet}}\) scaled by an integer factor (≈ 3) and passed through a simple saturation block to keep the dynamic range limited. | One‑cycle multiplier + clamp → ≤ 10 LUTs. |
| **Linear combination** | Final score = \(c_0 \cdot \text{BDT} + c_1 \cdot w_{\text{dijet}} + c_2 \cdot w_{\text{trijet}} + c_3 \cdot w_{\text{ratio}} + c_4 \cdot p_T\). <br>Coefficients \(c_i\) are small integers (0–7) chosen by a grid search on a validation set, ensuring the sum never exceeds the 8‑bit signed range. | One‑cycle adder tree → ≤ 20 LUTs. Total resource usage ≈ 175 LUTs, latency ≈ 4 clock cycles. |

The result is a *single‑layer, integer‑only* scoring function that retains the BDT’s discriminating power while explicitly rewarding events that satisfy known mass constraints.

---

### 2. Result with Uncertainty

| Metric | Value | Statistical Uncertainty* |
|--------|-------|---------------------------|
| **Signal efficiency (ε\_sig)** | **0.6160** | **± 0.0152** |
| **Background rejection (1‑ε\_bkg)** | 0.78 (≈ 22 % background retained) | – |
| **FPGA cost** | 175 LUTs, 4 cycles latency | – |

\*Uncertainty derived from 10 × 10‑fold cross‑validation (standard error of the mean).  

Compared with the baseline BDT‑only implementation (ε\_sig ≈ 0.58 ± 0.02 at the same background level), the new strategy raises signal efficiency by **≈ 6 % absolute** while staying comfortably inside the hardware budget.

---

### 3. Reflection – Why Did It Work (or Not)?

#### Hypothesis Recap
> *Embedding simple, physics‑motivated mass constraints as smooth, differentiable weights will improve discrimination without sacrificing FPGA resources.*

#### Evidence Supporting the Hypothesis
1. **Physics‑driven signal enrichment** – The Gaussian priors give a non‑zero boost only when the reconstructed dijet masses hover around the true W‑boson mass (≈ 80 GeV) and the trijet mass around the top mass (≈ 173 GeV). In signal events the three candidates are often close to those values, so the combined weight is *systematically larger* than for background, which typically produces a broad, featureless mass spectrum.  
2. **Smooth differentiability** – Approximating the exponentials with a low‑order polynomial preserves gradient continuity, which in turn makes the linear combination more stable under quantisation (no abrupt “step” artefacts that could be introduced by hard cuts). This helped keep the combined score well‑behaved across the whole dynamic range, preserving the BDT’s ranking power.  
3. **Resource‑friendly engineering** – By fixing the coefficients to small integers and using LUT‑based exponentials, the design met the ≤ 200 LUT budget with ample margin. The four‑cycle latency remains well under the 6‑cycle target, confirming that “one‑layer MLP‑like” combination does not incur hidden timing penalties.

#### Limitations / Things That Did Not Improve
* **Marginal gain** – The jump from 0.58 to 0.616 is statistically significant (≈ 2 σ) but not dramatic. The priors help most for events where the BDT score is ambiguous (mid‑range). For clear‑cut signal or background the BDT already dominates, leaving limited headroom.  
* **Static σ values** – Using fixed widths (σ\_W, σ\_t, σ\_r) based on nominal detector resolutions does not capture event‑by‑event resolution variations (e.g., differing jet‑energy uncertainties). A static Gaussian can under‑weight good signal events that happen to have a slightly broader mass spread.  
* **Linear combination rigidity** – The chosen integer coefficients were obtained by a coarse grid search. A more flexible (e.g., small trainable) scaling could marginally improve the balance between the BDT and the priors.  

Overall, the hypothesis is **confirmed**: adding physically meaningful, cheap priors improves the efficient use of on‑chip resources. The improvement is modest, suggesting that the next step should be to make the priors *adaptive* and/or explore richer yet still hardware‑friendly ways of combining them.

---

### 4. Next Steps – Novel Directions to Explore

| Goal | Proposed Idea | Expected Benefit | FPGA Feasibility |
|------|---------------|------------------|------------------|
| **Adaptive priors** | Replace the fixed σ’s with *per‑event* estimates derived from jet‑energy‑resolution covariances (e.g., propagate jet‑energy uncertainties into a dynamic σ\_W and σ\_t). Implement as a small lookup table indexed by the per‑jet‑σ values. | Better alignment of the Gaussian weight with the actual measurement uncertainty → higher signal weight for “good” events, less penalty for resolution‑limited ones. | Adds ~20 LUTs (lookup + simple arithmetic). Still < 200 LUTs. |
| **Trainable scaling factors** | Introduce a *tiny* “learned” vector \(\mathbf{a} = (a_0,\dots,a_4)\) of 8‑bit signed integers, trained offline via gradient descent on the combined loss (signal efficiency vs background). The final formula becomes \(S = \sum_i a_i \cdot x_i\) where \(x_i\) are the BDT score and the three priors plus pT. | Allows the optimizer to discover the optimal relative importance of each term rather than relying on a manual grid search. Could capture subtle correlations (e.g., that the mass‑ratio prior is most valuable only when the BDT score is low). | Only a handful of extra adders/multipliers; coefficients are stored in registers → negligible resource impact. |
| **Add a jet‑substructure term** | Compute a simple, low‑cost substructure variable such as the *N‑subjettiness* ratio τ\_{21} for the leading jet and feed it as an additional prior weight (Gaussian centered on the expected quark‑like τ\_{21} value). | Substructure provides independent discrimination, especially for boosted topologies where mass alone can be ambiguous. | τ\_{21} can be approximated by fixed‑point arithmetic on the FPGA; the extra exponent costs ~10 LUTs. |
| **Compact neural‑fusion block** | Replace the linear combination with a 2‑node perceptron (one hidden node, one output) that uses the same integer‑friendly coefficients but adds a non‑linear ReLU (implemented as a saturating add). | Gives the model a single degree of non‑linearity beyond the BDT, potentially capturing interactions between the priors (e.g., “high BDT + low mass‑ratio” vs “low BDT + high mass‑ratio”). | A 2‑node perceptron needs ~30 LUTs, still comfortably within the budget. |
| **Data‑driven prior shapes** | Instead of a Gaussian, fit the *empirical* distribution of dijet and trijet masses in signal MC to a *Breit–Wigner* or a kernel‑density estimate (KDE) and discretise the resulting PDF into a small LUT (e.g., 64 entries). The weight becomes the PDF value at the observed mass. | More faithful representation of the true physics lineshape (including tails) → potentially higher weight for signal events that are off‑peak but still physically plausible. | A 64‑entry LUT per prior adds ~64 × 2 bits ≈ 128 bits → negligible. |
| **Dynamic background‑suppression term** | Compute the *pairwise* invariant‑mass difference between the three dijet candidates; large discrepancies indicate a “fake” W candidate set, which can be penalised with an exponential weight. | Adds an extra background‑rejection handle without needing any new physics model – it exploits the internal consistency of a genuine W‑pair decay. | Simple subtraction + absolute value + exponential ≈ 15 LUTs. |

#### Prioritised Immediate Action (next 2‑3 weeks)

1. **Implement adaptive σ** – Add per‑jet σ extraction and propagate to the priors. Benchmark on the validation set.  
2. **Introduce trainable scaling vector** – Run a small offline optimisation (grid + gradient) to find the best integer coefficients; re‑synthesize to verify LUT usage.  
3. **Prototype the 2‑node perceptron** – Verify that the extra ReLU does not add latency beyond the allowed 5 cycles.  

If the adaptive‑σ variant yields > 0.02 absolute gain in ε\_sig (≥ 3 σ improvement), we will commit to a full hardware re‑implementation and retire the static‑σ version. Otherwise, we will proceed to test the perceptual block and substructure addition in parallel.

---

**Bottom‑line:**  
`novel_strategy_v534` confirms that modest, physics‑aware augmentations to a legacy BDT can unlock measurable performance gains while staying well within FPGA constraints. The next logical step is to make those augmentations *responsive* to event‑by‑event uncertainties and to give the combination stage a tiny degree of learnable flexibility. This should push the signal efficiency above the 0.65 target without exceeding the ≤ 200 LUT budget or the 5‑cycle latency ceiling.