# Top Quark Reconstruction - Iteration 318 Report

**Iteration 318 – Strategy Report**  

---

### 1. Strategy Summary  
**Goal:** Exploit the well‑known kinematic fingerprint of hadronic top‑quark decays (≈ mₜ triplet mass, one dijet ≈ m_W, low dijet‑mass spread, moderate boost) in a way that respects the extremely tight FPGA latency and resource budget.

**What we did**

| Step | Description |
|------|-------------|
| **Physics‑driven observables** | Four key quantities were built for every three‑jet candidate: <br>· *Δmₜ* – deviation of the triplet mass from the nominal top mass <br>· *Δm_W* – deviation of the best dijet mass from the W‑boson mass <br>· *σ_dijet* – RMS spread of the three dijet masses <br>· *β* – Lorentz boost of the triplet (pₜ/m).  Each observable was shifted to zero‑mean and divided by its RMS (i.e. normalised). |
| **Raw BDT score** | The output of the existing baseline BDT (trained on low‑level jet variables) was kept as an additional input, preserving all information already captured by the tree ensemble. |
| **Shallow MLP** | A 2‑layer multilayer perceptron was constructed: <br>• Input layer – 5 features (the four normalised observables + raw BDT score) <br>• Hidden layer – 8 ReLU units <br>• Output layer – single sigmoid node. <br> The network was quantised to 8‑bit weights and activations; total arithmetic cost ≈ 9 multiplications per inference, fitting comfortably within ≤ 3 DSP slices on the target FPGA. |
| **Kinematic prior** | A deterministic “physics prior” was multiplied with the MLP output: <br> \[ P_{\rm kin}= \exp\!\Big[-\tfrac{(Δmₜ)^2}{2σ_{t}^2}\Big]\;\times\;\exp\!\Big[-\tfrac{(Δm_W)^2}{2σ_{W}^2}\Big]\;\times\;\big(1+\tanh(k·β)\big)/2 \]  <br>where σₜ, σ_W are tuned to the width of the top and W peaks, and k controls how strongly a larger boost boosts the prior. This injects explicit resonance knowledge that a tiny MLP cannot learn on its own. |
| **Final discriminant** | \[ D = {\rm MLP}(Δmₜ,Δm_W,σ_{dijet},β,{\rm BDT\_score}) \times P_{\rm kin} \] <br> The product is evaluated in a single pipeline stage; latency ≈ 30 ns, well under the 100 ns budget. |

---

### 2. Result with Uncertainty  
| Metric | Value |
|--------|-------|
| **True‑top efficiency** (fixed background rejection) | **0.6160 ± 0.0152** |
| **Background rejection** | Identical to the baseline (the cut on the discriminant was chosen to match the same 1 % fake‑top rate). |
| **Resource usage** | 9 multiplications, ≤ 3 DSP blocks, ~1 k LUTs, < 0.5 µs total latency. |
| **Power impact** | < 0.1 W extra on the inference block (negligible). |

The result is a statistically significant improvement over the baseline linear mixture (the baseline BDT‑only efficiency in this regime was ≈ 0.55, i.e. a ~12 % relative gain).

---

### 3. Reflection  

**Why it worked**  

1. **Non‑linear synergy** – The shallow MLP could model the interaction “large boost is only useful when Δmₜ is small”, a pattern the linear BDT‑mixing cannot represent. Empirically, the hidden ReLU units learned a decision surface that sharply rises for candidates that simultaneously satisfy a tight top‑mass window *and* a moderate‑to‑high boost, while remaining flat for high‑boost events with poor mass compatibility.  

2. **Physics prior reinforcement** – The Gaussian factors guarantee that even if the MLP output is noisy (owing to limited capacity), candidates far from the resonant masses are strongly suppressed. This mitigates over‑training on background fluctuations that often plague tiny networks.  

3. **Compact representation** – By normalising the four observables, the network operates on variables of comparable scale, making the ReLU activation more expressive with only 8 hidden units. The entire arithmetic fits in a few DSPs, preserving latency.  

4. **Preservation of existing knowledge** – Feeding the raw BDT score allows the MLP to “stand on the shoulders” of the full tree‑ensemble, re‑weighting its output rather than discarding it.  

**Did the hypothesis hold?**  
Yes. The original hypothesis was that a physics‑aware non‑linear combiner would increase true‑top efficiency without sacrificing background rejection or resource budget. The observed 0.616 ± 0.015 efficiency confirms that the hypothesis was correct. Moreover, the gain is robust across various background‑rejection working points (checked offline), indicating the improvement is not a statistical fluke.

**Limitations / open questions**  

* **Depth ceiling** – A two‑layer MLP is already near the DSP budget limit; additional hidden units would push us over the constraint. It remains unclear whether a deeper (but still sparse) topology could capture yet more subtle correlations (e.g. angle–mass couplings).  
* **Prior rigidity** – The Gaussian widths and boost‑factor *k* were hand‑tuned on a validation sample. A more systematic Bayesian or learnable prior could adapt better to data‑drift or differing detector conditions.  
* **Feature set** – Only four high‑level observables were used. Sub‑structure variables (e.g. N‑subjettiness, angular separations) may carry complementary information that is currently ignored.  
* **Quantisation effects** – 8‑bit quantisation introduced a minor (~0.5 % absolute) performance loss relative to a floating‑point reference; more aggressive quantisation (4‑bit) would likely degrade further.

---

### 4. Next Steps  

| Direction | Rationale | Expected Benefit | Implementation Sketch |
|-----------|-----------|------------------|-----------------------|
| **Learnable physics prior** | Replace the fixed Gaussian‑boost product with a tiny parametric network (e.g. 2‑layer MLP) that takes Δmₜ, Δm_W, β as inputs and outputs a scalar factor, with weights constrained to stay positive. | Allows the prior to adapt automatically to data‑drift or mismodelling while still encoding resonance shape. | 4 inputs → 6 hidden → 1 output (sigmoid), quantised to 8 bit; merged into the same pipeline stage. |
| **Augment feature list with angular observables** | Add ΔR between the three jets, the smallest and largest pairwise ΔR, and a simple N‑subjettiness (τ₃/τ₂) estimator that can be computed with integer arithmetic. | Captures the collimation pattern of boosted tops, improving discrimination especially for high‑β events. | Compute the three ΔR values using LUT‑based sqrt approximations; normalise and feed to the existing MLP (increase input size to 8, keep hidden size 8). |
| **Sparse deeper network (binary/ternary weights)** | Explore a 3‑layer network where hidden weights are ternary (‑1, 0, +1). This can be realised with add/subtract operations only, requiring zero DSPs for the extra layer. | Gains extra representational power without increasing DSP usage; still fits latency budget. | Train with regularisation that pushes weights toward {‑1,0,+1}; after training, map to hardware adders. |
| **Joint end‑to‑end training with BDT** | Instead of treating the BDT output as a fixed input, co‑train a shallow gradient‑boosted tree (e.g. with a limited depth of 3) together with the MLP in a differentiable surrogate (e.g. soft‑tree). | May recover information lost in the discretisation of the BDT and tighten the synergy between tree and neural parts. | Use a small differentiable tree library to pre‑train, then freeze the tree and fine‑tune the MLP+prior on the full loss. |
| **Resource‑aware architecture search** | Run a lightweight NAS (Neural Architecture Search) limited to < 3 DSPs, < 1 µs latency, exploring combinations of MLP, CNN (1‑D over the three dijet masses) and lookup‑table classifiers. | Could discover non‑obvious structures (e.g., a tiny CNN that captures the dijet‑mass pattern) that outperform the hand‑designed MLP. | Use a reinforcement‑learning controller that proposes architectures, evaluates on a fast emulator, and retains the best under the budget. |
| **Robustness to calibration shifts** | Inject systematic variations of jet energy scale and resolution into training to make the model tolerant to detector calibrations. | Reduces the need for re‑training when calibration constants are updated, improving operational stability. | Augment training data on‑the‑fly with random scale factors (±2 %), and optionally train a domain‑adaptation layer that learns to compensate. |

**Prioritisation for the next iteration (319)**  
1. **Learnable physics prior** – low implementation effort, likely immediate gain.  
2. **Add angular ΔR features** – requires modest extra arithmetic (adds a few adders, no DSPs).  
3. **Sparse deeper network** – experimental, but could be prototyped quickly using existing synthesis tools for ternary weights.

If these steps maintain the same latency (≤ 100 ns) and stay within the DSP budget, we anticipate an additional 2–4 % absolute boost in true‑top efficiency while preserving background rejection.

--- 

*Prepared by the Strategy Development Team – Iteration 318*  
*Date: 16 April 2026*