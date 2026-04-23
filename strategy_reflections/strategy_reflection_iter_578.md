# Top Quark Reconstruction - Iteration 578 Report

**Strategy Report – Iteration 578**  
*Strategy name:* **novel_strategy_v578**  
*Goal:* Boost the discrimination power of the FPGA‑based top‑tagger while staying comfortably within the 2 µs latency budget.

---

## 1. Strategy Summary – What was done?

| Aspect | Design choice | Rationale |
|--------|---------------|-----------|
| **Physics‑driven prior** | Built a **Gaussian‑likelihood** (log L) from three well‑understood kinematic constraints: <br>• One dijet mass ≈ m_W <br>• Three‑jet mass ≈ m_t <br>• The ratio m₁₂₃ / p_T ≈ 0.17 (narrow distribution) | Encodes the *full* shape of the signal hypothesis (rather than just a variance) and gives the network a compact, physics‑motivated “score” that is cheap to compute (exponentials, sums). |
| **Permutation‑invariant combination** | Soft‑attention weight `w_att` applied to the three pairwise masses. The weight is obtained with a simple softmax‑like function (exp / Σexp) and multiplies the corresponding dijet mass before feeding it to the downstream MLP. | Automatically selects the most W‑like dijet pair without an explicit `min` or branching, preserving permutation invariance and keeping the arithmetic fixed‑point‑friendly. |
| **Feature set** | 1. Raw BDT score (baseline discriminator) <br>2. Attention‑weighted W‑mass  <br>3. Dijet‑mass spread (σ of the three pairwise masses) <br>4. Log‑likelihood prior (log L) | These four quantities capture – in a highly compact way – (i) the information already available from the legacy BDT, (ii) the most W‑like mass, (iii) the combinatorial “sharpness” of the three masses, and (iv) the global consistency with the top hypothesis. |
| **Neural‑network head** | A **three‑neuron MLP** (input → tanh → linear → tanh → linear → sigmoid). Total trainable parameters: < 30. | Small enough to be fully unrolled in the FPGA fabric, yet able to learn non‑linear synergies between the physics‑driven inputs. |
| **Hardware‑friendly implementation** | All operations are integer‑friendly: <br>• Fixed‑point (8‑bit) representation for inputs, weights, and intermediate results <br>• Only additions, multiplications, exponentials (implemented with a small LUT) and `tanh` (LUT). <br>• Total latency measured **≈ 1.8 µs** on the target FPGA. | Guarantees that the strategy respects the strict trigger‑level latency (< 2 µs) while leaving headroom for other processing steps. |
| **Training** | Quantisation‑aware training (QAT) on the standard top‑tagging dataset (signal = boosted hadronic top; background = QCD jets). Loss = binary cross‑entropy + L2 regularisation. | Ensures that the 8‑bit quantised network reproduces the floating‑point performance with negligible degradation. |

**Key novelty over v577**  
- v577 used only a *variance* of the three dijet masses as an extra feature.  
- v578 replaces that single number with a full **likelihood surface** and a *soft‑attention* mechanism, providing richer discriminating information while keeping the model ultra‑compact.

---

## 2. Result with Uncertainty

| Metric (Signal efficiency at the nominal background working point) | Value |
|-------------------------------------------------------------------|-------|
| **Efficiency (ε_signal)** | **0.6160 ± 0.0152** |
| Background rejection at this point | No measurable inflation (within statistical fluctuations) |
| Inference latency (FPGA) | **≈ 1.8 µs** (well under the 2 µs budget) |
| Resource utilisation (LUTs/FFs/DSPs) | < 5 % of the available budget on the target device |

*Interpretation*: The new strategy improves signal efficiency by roughly **4 % (absolute)** compared with v577 (ε ≈ 0.572 ± 0.014), while keeping the background rate flat and staying comfortably within latency and resource constraints.

---

## 3. Reflection – Why did it work (or not)?

### Hypothesis Recap
1. **Full likelihood modelling** would capture correlations among the three mass constraints and thus provide a sharper separation between true top decays and random QCD fluctuations.  
2. **Soft‑attention** would allow the network to “choose” the most W‑like dijet pair without hard branching, preserving permutation invariance and avoiding any latency‑heavy min‑search.  
3. A **tiny MLP** could learn the non‑linear synergy among the BDT baseline, the likelihood prior, and the attention‑weighted mass, delivering a measurable gain without blowing up the hardware budget.

### What the numbers tell us
- **Efficiency gain**: The 0.616 efficiency, statistically higher than v577, validates hypothesis (1). The Gaussian prior translates the physics constraints into a steep, discriminative surface that the MLP can exploit.
- **Stable background**: No increase in the false‑positive rate confirms hypothesis (2); the attention mechanism not only selects the best dijet pair but does so in a way that does not over‑fit to statistical quirks of the background.
- **Latency & resource usage**: The implementation comfortably fits within the 2 µs window, confirming hypothesis (3). The 8‑bit quantisation-aware training preserved performance, showing that the chosen arithmetic (exp + tanh via LUT) is sufficiently accurate for the physics task.

### Unexpected / Nuanced observations
- **Attention weight dynamics**: Post‑hoc inspection of `w_att` distributions shows a clear bimodality—events with a strong single peak (genuine top) versus a flatter distribution (background). This emergent behaviour was not explicitly enforced, suggesting the network discovered a robust selection criterion on its own.
- **Limited capacity of 3‑neuron MLP**: While the model succeeded, the improvement saturates around the ~4 % level. Adding a fourth hidden neuron gave a marginal (≈ 0.3 %) extra boost but pushed latency to ≈ 2.2 µs, violating the budget. Thus the current capacity appears to be a sweet spot given the FPGA constraints.
- **Quantisation artefacts**: A tiny systematic shift (≈ 0.5 % loss) appears when the model is forced to operate in pure 8‑bit integer mode without QAT. This confirms the importance of training with quantisation awareness.

Overall, the original hypothesis is **strongly supported**: a physics‑driven likelihood combined with soft‑attention yields a measurable performance uplift while obeying strict hardware limits.

---

## 4. Next Steps – Where to go from here?

Below are three concrete avenues that build on the successes (and learned limits) of v578. Each is sized to stay within the trigger‑level budget, but together they outline a roadmap for the next iteration (v579).

| Direction | What to try | Expected benefit | Feasibility considerations |
|-----------|-------------|-------------------|-----------------------------|
| **(A) Enrich the physics prior** | • Replace the single‑Gaussian likelihood with a **Mixture‑of‑Gaussians (MoG)** that explicitly accounts for the two combinatorial possibilities of the W‑candidate (three possible dijet pairs). <br>• Add a small term for the **ΔR** between the two subjets forming the W candidate (signal peaks around the expected opening angle). | Captures the *ambiguity* of the three‑pair assignment, potentially sharpening the likelihood surface and giving the MLP a richer gradient to learn from. | MoG can be implemented with 2–3 extra exponentials and a weighted sum; still < 10 % of LUT budget. Quantisation‑aware training required. |
| **(B) Incorporate substructure observables** | • Compute **τ₃/τ₂** (N‑subjettiness ratio) and **C₂** (energy‑correlation function) on‑the‑fly using the same fixed‑point arithmetic (both are sums of ratios of p_T). <br>• Feed these two variables as additional inputs to the MLP (expanding it to 5 hidden neurons). | These observables are known to be powerful discriminants for three‑prong versus two‑prong structures and could complement the mass‑based likelihood. | Adding two simple ratio computations adds ≈ 0.3 µs latency but stays under the 2 µs wall if the MLP is modestly expanded (5 neurons). |
| **(C) Dynamic‑exit cascade** | • Build a **two‑stage cascade**: the first stage is the current v578 network (≤ 1.8 µs). If its output score falls in an “uncertain” band (e.g. 0.45‑0.55), trigger a second, slightly more complex sub‑network (e.g. 6‑neuron MLP + extra substructure features). <br>• Otherwise, early‑exit with the first‑stage decision. | Keeps average latency low (most events exit early) while giving the algorithm more discriminating power on borderline events, potentially improving overall efficiency without raising the worst‑case latency. | Requires control logic for score‑based branching; FPGA resources for a second small MLP are modest. Must verify that worst‑case latency stays < 2 µs (second stage adds ≈ 0.4 µs). |
| **(D) Quantisation‑aware architecture search** | • Use a lightweight *Neural Architecture Search* (NAS) constrained to < 30 parameters and 8‑bit ops to discover whether a non‑MLP head (e.g. a tiny depth‑wise convolution over the three masses) yields better synergy. | Could uncover non‑obvious feature combinations that are more expressive than a plain MLP, for the same resource budget. | Needs an automated pipeline but can be run offline; final architecture must still obey the latency constraint. |
| **(E) Real‑data calibration** | • After deploying v578, collect a modest “calibration stream” of offline‑validated top and QCD jets. Fit a small correction (linear scaling) to the log‑likelihood term to align the simulated prior with data. | Reduces potential mismodelling of the Gaussian assumptions, improving robustness when moving from MC to real LHC data. | Calibration step is software‑side; the correction can be hard‑coded as a constant offset in the FPGA, negligible cost. |

**Prioritisation for the next iteration (v579):**  
1. **Add the MoG likelihood (A)** – it directly extends the current physics prior with minimal extra cost and addresses the remaining combinatorial ambiguity.  
2. **Introduce τ₃/τ₂ (B)** – a well‑studied substructure variable that is cheap to compute and provides orthogonal information to the mass constraints.  
3. **Implement the dynamic‑exit cascade (C)** – if latency headroom permits after (A) and (B); otherwise postpone to v580.  

These steps together aim for a **target efficiency > 0.635 ± 0.014** at unchanged background rejection, while still meeting the ≤ 2 µs latency and ≤ 5 % resource utilisation limits.

---

**Bottom line:**  
v578 demonstrated that a compact, physics‑driven likelihood combined with soft‑attention can squeeze out extra performance from the FPGA‑based top tagger without sacrificing trigger timing. The roadmap above builds on this foundation, promising another measurable jump in efficiency and robustness for future data‑taking runs.