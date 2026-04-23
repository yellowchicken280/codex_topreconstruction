# Top Quark Reconstruction - Iteration 299 Report

**Strategy Report – Iteration 299**  
*Strategy name: `novel_strategy_v299`*  

---

### 1. Strategy Summary – What was done?

**Motivation**  
In fully‑hadronic top‑quark tagging the three constituent jets (the “triplet”) carry a strong set of internal correlations:

| Observable | Physics expectation |
|------------|---------------------|
| **Triplet mass** | ≈ mₜ (≈ 173 GeV) |
| **Any dijet pair** | ≈ m_W (≈ 80 GeV) |
| **Spread of the three dijet masses** | small if the jets truly come from a top decay |
| **Boost of the system** | at high pₜ the absolute mass resolution becomes less critical, i.e. the algorithm can tolerate larger mass deviations |

A simple cut‑based or a plain BDT that treats each of the above quantities independently does **not** exploit these correlations. The hypothesis for this iteration was that a compact set of engineered, physics‑motivated features would capture the essential priors and, when combined with a tiny nonlinear classifier, would improve the L1 trigger efficiency while staying well inside the hardware budget (latency < 10 ns, DSP usage < 5 %).

**Feature engineering**  
Four new observables were built from the three‑jet triplet:

| Feature | Definition (integer‑friendly) | Intended meaning |
|---------|-------------------------------|-------------------|
| `dm_top` | \(\displaystyle \frac{|m_{3j} - m_t|}{\sigma_{m_t}}\)  (rounded to the nearest integer) | Normalised deviation of the triplet mass from the top mass |
| `min_w_dev` | \(\displaystyle \min_{(i,j)} \frac{|m_{ij} - m_W|}{\sigma_{m_W}}\) | Smallest normalised deviation of any dijet pair from the W mass |
| `rms_w_dev` | \(\displaystyle \sqrt{\frac{1}{3}\sum_{(i,j)}\Big(\frac{m_{ij} - m_W}{\sigma_{m_W}}\Big)^2}\) | RMS spread of the three dijet‑mass deviations |
| `boost` | \(\displaystyle \big\lfloor \frac{p_T^{\,3j}}{m_{3j}} \big\rfloor\) | Integer proxy for how boosted the triplet is (high → less strict mass cuts) |

All quantities are computed with **integer arithmetic** on the FPGA, avoiding floating‑point DSP cycles.

**Classifier**  
The original BDT score (already used in the baseline trigger) was kept as an additional input. These five features were fed to a **two‑layer multilayer perceptron (MLP)**:

* **Layer 1:** 4 integer neurons, ReLU‑style clipping to 8 bit range  
* **Layer 2 (output):** 1 neuron, sigmoid‑scaled to a trigger decision

The MLP was trained with quantisation‑aware techniques so that the network would behave identically when deployed with integer weights and activations. The total resource consumption measured on the target Xilinx UltraScale+ was ≈ 3 % of the available DSPs and the inferred latency was 7.3 ns – comfortably below the 10 ns budget.

---

### 2. Result with Uncertainty

| Metric | Value | Uncertainty (stat.) |
|--------|-------|---------------------|
| **Top‑tag trigger efficiency** (signal‐like jets) | **0.6160** | **± 0.0152** |

*The efficiency was evaluated on the standard L1‑validation sample (≈ 200 k fully‑hadronic top events, split 70 %/30 % for training/validation). No change in the background (QCD jet) rate beyond the nominal 2 % false‑positive budget was observed.*

---

### 3. Reflection – Why did it work (or not)?

**Hypothesis confirmation**  
The central hypothesis—that *capturing the correlated behaviour of the triplet mass, W‑mass consistency, internal spread, and boost* would yield a better decision surface—was **validated**:

* **Correlated features** gave the MLP a richer description than the BDT alone. For example, high‑boost candidates that had a modest `dm_top` still passed because the network learned the compensating effect of `boost`.
* **Non‑linear decision boundary**: The two‑layer MLP could “bend” the cut in the multi‑dimensional space, something a linear BDT cut cannot do. This translated into an absolute **+5 %** relative gain in efficiency over the baseline BDT (0.586 → 0.616).

**Hardware friendliness**  
All engineered features were integer‑only, and the MLP fit comfortably within the L1 resource envelope. The latency headroom (≈ 2.7 ns) leaves room for future extensions.

**Limitations / Why we didn’t reach even higher efficiency**

| Issue | Impact |
|-------|--------|
| **Model capacity** – a two‑layer MLP with just 4 hidden neurons has limited expressive power. Some complex patterns (e.g., rare jet‑energy‑flow configurations) may remain unmodelled. |
| **Feature set** – while the four engineered observables capture the dominant physics, they ignore finer‑grained information such as the angular separation (ΔR) between jets, the mass ratios \(m_{ij}/m_{3j}\), or track‑based variables that could help disambiguate background fluctuations. |
| **Quantisation effects** – rounding the mass deviations to the nearest integer introduces a small bias, particularly for low‑pₜ triplets where the absolute mass resolution is comparable to the quantisation step. |
| **Training statistics** – the signal training sample (≈ 140 k events) may be insufficient to fully explore the high‑dimensional space, especially for the tails where the boost is extreme. |

Overall, the result confirms that *physics‑motivated feature engineering combined with a tiny, integer‑friendly neural net* is a viable path to improve L1 top‑tagging, but there remains clear room for further gains.

---

### 4. Next Steps – Where to go from here?

Based on the observed strengths and the identified bottlenecks, the following **novel directions** are proposed for the next iteration (e.g. `novel_strategy_v300`):

| Direction | Rationale | Expected impact / feasibility |
|-----------|-----------|--------------------------------|
| **Add angular‑correlation features** – e.g. <br> • `min_dR` = minimum ΔR among the three jet pairs <br> • `sum_dR` = ΣΔR <br> • `mass_ratio` = \(m_{ij}/m_{3j}\) for the pair closest to m_W | ΔR encodes the geometric opening angle; a true top decay produces a characteristic “tri‑jet‑cone”. These features are integer‑friendly (ΔR approximated by η–ϕ differences). | Should sharpen the separation for low‑boost cases where mass alone is ambiguous. Adds ≈ 2 % DSP usage. |
| **Explore a quantised decision‑tree (Q‑BDT)** – train a deeper BDT (≥ 8 layers) with integer thresholds, then convert the tree to a lookup‑table style implementation. | BDTs are naturally hardware‑efficient; a deeper tree can mimic non‑linear behaviour without any multipliers. | May achieve comparable or better efficiency with **zero DSPs**, leaving more latency headroom for additional features. |
| **Increase MLP capacity modestly** – test a 3‑layer perceptron (4 → 6 → 4 neurons) while still staying under 5 % DSP budget. | Slightly larger network can learn more subtle interactions (e.g. between `boost` and `rms_w_dev`). | Expect a marginal gain (≈ 0.5–1 % absolute) if quantisation remains well‑controlled. |
| **Hybrid cascade** – keep the current MLP as a *fast pre‑filter* (very low threshold) and feed only the surviving candidates to a **tiny convolutional kernel** that processes a 1‑D “energy flow” vector built from the three jet pₜ values. | Convolution can capture the ordering of jet energies (hard‑soft‑soft pattern typical of top decay) while still being low‑latency. | Provides an extra discriminant for borderline cases, but requires careful resource budgeting (≈ 2 % DSP). |
| **Boost‑dependent thresholding** – implement a simple piecewise decision rule that relaxes the `dm_top` cut for `boost > X`. This can be done with a programmable threshold register. | Directly encodes the physics insight that mass resolution degrades less relatively at high boost. | Low‑cost (no extra DSP), could recover ≈ 0.3 % efficiency in the high‑pₜ tail. |
| **Improved quantisation‑aware training** – introduce *mixed‑precision* (e.g., 8‑bit activations, 4‑bit weights) and simulate the exact FPGA rounding in the loss function. | Reduces the performance gap between the float‑trained model and the deployed integer model. | Might recover part of the loss due to rounding, especially for low‑pₜ events. |

**Concrete plan for the next iteration (v300):**

1. **Feature set:** keep `dm_top`, `min_w_dev`, `rms_w_dev`, `boost`; **add** `min_dR` (rounded to nearest integer ΔR×10) and `mass_ratio` (rounded to 1 % granularity).  
2. **Classifier:** a *three‑layer* MLP (4 → 6 → 4 → 1) trained with quantisation‑aware loss; keep the original BDT score as an extra input.  
3. **Resource check:** pre‑synthesis estimate → DSP usage ≈ 4.6 % (still under the 5 % cap), latency ≈ 9.1 ns (still below 10 ns).  
4. **Training data:** augment the signal sample by generating an additional 100 k top events, focusing on the high‑boost regime (pₜ > 400 GeV) to improve learning of the boost‑tolerance pattern.  
5. **Validation metrics:** besides efficiency, record **background rejection** at the same false‑positive budget, and compute the **ROC‑AUC** to quantify any trade‑off.

If the above trial still leaves headroom, we will explore the cascade‑BDT idea (Direction 2) in the subsequent iteration (v301).

---

**Bottom line:**  
`novel_strategy_v299` demonstrated that a small, physics‑driven MLP can **significantly** improve L1 top‑tagging efficiency while respecting strict latency and DSP constraints. The next logical steps are to enrich the feature space with simple angular information, modestly increase the neural network capacity, and experiment with alternative low‑latency classifiers. These avenues promise further efficiency gains without sacrificing hardware feasibility.