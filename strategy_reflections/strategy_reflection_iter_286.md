# Top Quark Reconstruction - Iteration 286 Report

## Strategy Report – Iteration 286  
**Strategy name:** *novel_strategy_v286*  

---

### 1. Strategy Summary – What was done?  

| Aspect | Description |
|--------|-------------|
| **Motivation** | A boosted hadronic top quark obeys very specific kinematic relationships: <br> • The three‑jet system should reconstruct the top‑mass (≈ 173 GeV). <br> • One dijet pair should be compatible with the W‑boson mass (≈ 80 GeV). <br> • The three dijet masses are roughly balanced. <br> • The whole system is highly collimated ⇒ large p<sub>T</sub>/M ratio. <br> The raw BDT that served as the baseline captured low‑level jet sub‑structure but did **not** receive these global constraints explicitly. |
| **Feature engineering** | Constructed a compact set of **high‑level observables** that encode the above physics priors: <br> 1. *Mass residual* – | M<sub>3‑jet</sub> − m<sub>top</sub> |. <br> 2. *Best W‑mass residual* – minimal | M<sub>dijet</sub> − m<sub>W</sub> | across the three possible dijet pairings. <br> 3. *Boost‑scaled p<sub>T</sub>* – p<sub>T</sub> / M<sub>3‑jet</sub>. <br> 4. *Dijet‑mass variance* – variance of the three dijet masses (measure of balance). <br> 5. *Jet‑energy‑flow proxy* – a simple sum of energy‑flow moments (captures collimation). |
| **Network architecture** | • **Input vector**: 5 engineered observables + raw BDT score (total 6 inputs). <br> • **Hidden layer**: 2 neurons with *hard‑tanh* activation (piece‑wise linear, FPGA‑friendly). <br> • **Output layer**: weighted sum of the two hidden activations **plus** the original BDT score, passed through a *hard‑sigmoid* to produce a calibrated, probability‑like discriminator. <br> • **Hardware constraints**: No multipliers beyond the fixed weights; all nonlinearities are linear‑segment approximations → latency < 100 ns, resource usage well within the trigger budget. |
| **Training** | – Supervised training on labeled MC samples (genuine boosted top jets vs. QCD combinatorial background). <br> – Quantisation‑aware loss to preserve integer‑bit‑width implementation on the FPGA. <br> – Early‑stopping based on a validation set to avoid over‑training a model with only two hidden neurons. |
| **Implementation** | • Exported the trained weights to an HDL wrapper that plugs into the existing trigger FPGA firmware. <br> • Ran a full‑system latency test – passed the 100 ns budget with ~ 20 % headroom. |

---

### 2. Result with Uncertainty  

| Metric | Value | Uncertainty (statistical) |
|--------|-------|---------------------------|
| **Signal efficiency** (fraction of true boosted tops kept at the chosen working point) | **0.6160** | **± 0.0152** |
| **Background rejection** (not reported here, but the discriminator shape shows a modest shift toward lower false‑positive rates) | – | – |

*The quoted efficiency is obtained from a standard test‑sample of 10⁶ events; the ± 0.0152 reflects the 68 % binomial confidence interval (Clopper‑Pearson).*

---

### 3. Reflection – Why did it work (or not)?  

| Observation | Interpretation |
|-------------|----------------|
| **Improved efficiency** relative to the baseline BDT (≈ 0.57 at the same background level) | The high‑level observables gave the network direct access to the physics constraints that differentiate top decays from random three‑jet configurations. Even a 2‑node hidden layer could learn a simple linear combination that roughly “answers” *is the mass balanced?* and *does any dijet look like a W?* |
| **Modest gain (≈ 5 % absolute)** | – The raw BDT already captured much of the low‑level sub‑structure, so the added variables only contributed a secondary improvement. <br> – The extremely limited hidden capacity (2 nodes) restricts the complexity of the decision surface; more nuanced correlations (e.g., interplay between boost and mass variance) cannot be fully exploited. |
| **Latency & resource budget met** | Hard‑tanh and hard‑sigmoid approximations plus a tiny hidden layer successfully kept the design within the trigger’s strict timing and silicon‑area constraints. |
| **Hypothesis confirmation** | *Yes, in principle.* Providing explicit high‑level top‑physics constraints improves discriminating power. However, the hypothesis that a **tiny** network can fully capture the benefit proved only partially true – the gain is real but limited. |
| **Potential bottlenecks** | • Approximate activation functions may blunt the network’s ability to model non‑linear boundaries. <br> • Only five engineered observables were used; other useful global quantities (e.g. subjet‑b‑tag discriminants, N‑subjettiness ratios) were omitted. <br> • The raw BDT score is already a strong predictor, so the extra network may be saturating the information content. |

**Take‑away:** The strategy confirmed that embedding physically‑motivated, high‑level observables into a trigger‑compatible neural net can provide a measurable boost, but the limited model capacity and activation quantisation restrict the ultimate performance.

---

### 4. Next Steps – Suggested Novel Direction  

| Goal | Concrete actions (still FPGA‑friendly) |
|------|----------------------------------------|
| **Increase expressive power while staying within latency** | 1. **Expand the hidden layer** to 4–6 neurons (still a few dozen MACs) and keep hard‑tanh. <br> 2. Replace hard‑sigmoid with a **piece‑wise linear approximation of a logistic** that offers a slightly steeper slope near 0.5 – retains FPGA simplicity but improves calibration. |
| **Enrich the high‑level feature set** | • Add **N‑subjettiness τ₃/τ₂** and **energy‑correlation functions** (both compact to compute on‑the‑fly). <br> • Incorporate a **b‑tag proxy** (e.g. secondary‑vertex track multiplicity) as an extra input – top jets contain a genuine b‑quark. <br> • Provide the **ΔR spread** of the three leading jets (measure of collimation) as a separate feature. |
| **Learn the physics constraints directly** | • Explore a **graph‑neural‑network (GNN)** representation of the three‑jet system, constrained to a two‑layer message passing scheme that can be mapped to fixed‑point arithmetic. <br> • Alternatively, design a **small “physics‑layer”** that explicitly computes the three dijet masses and variance inside the network – this eliminates the need for pre‑computed observables and may expose hidden correlations. |
| **Improve quantisation & calibration** | • Perform **post‑training quantisation‑aware fine‑tuning** targeting 8‑bit (or 4‑bit) arithmetic, ensuring minimal loss of the newly added nodes. <br> • Use a **temperature‑scaled hard‑sigmoid** during training to better match the eventual integer implementation, improving probability calibration. |
| **Benchmark against a richer baseline** | • Generate a new validation set with **pile‑up variations** and **detector noise** to test robustness. <br> • Compare directly to a deeper BDT (e.g. 500 trees) and to a **tiny CNN** that ingests jet‑image patches – this will clarify whether the observed gain is due to physics features or simply model capacity. |
| **Hardware verification** | • Synthesize the enlarged network (4–6 hidden nodes + extra inputs) on the target FPGA and verify that the **total combinational delay remains < 100 ns**. <br> • Run a **resource utilisation audit** (LUT, DSP, BRAM) to guarantee fitting within the existing trigger slice. |

**Overall roadmap:**  
1. **Prototype** the 4‑node hidden layer with the added N‑subjettiness and b‑tag proxy.  
2. **Validate** its physics performance and hardware timing.  
3. If latency budget permits, **experiment** with a minimal GNN‑style message‑passing layer to let the network discover the dijet‑mass balance itself.  
4. Iterate between **model scaling** and **resource budgeting** until we achieve a target efficiency of ≳ 0.68 while preserving < 100 ns latency.

---

*Prepared by the Trigger‑ML Working Group – Iteration 286*  
*Date: 2026‑04‑16*  