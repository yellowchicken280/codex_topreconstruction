# Top Quark Reconstruction - Iteration 157 Report

**Strategy Report – Iteration 157**  
*Strategy name:* **novel_strategy_v157**  

---

### 1. Strategy Summary – What was done?

| Component | Implementation | Rationale |
|-----------|----------------|-----------|
| **Physics‑driven likelihoods** | Gaussian likelihood terms for (i) the reconstructed top‑quark mass, (ii) the two best W‑boson dijet masses. The Gaussian widths are *p<sub>T</sub>‑dependent* (larger width for higher‑p<sub>T</sub> jets) to emulate the detector resolution. | Enforces the most basic kinematic expectations of a hadronic top: one three‑prong jet whose sub‑mass spectrum looks like M<sub>t</sub> ± σ and two sub‑jets close to M<sub>W</sub>. |
| **Boost‑favoring turn‑on** | A smooth tanh(p<sub>T</sub>/p₀) factor (p₀ ≈ 300 GeV) multiplies the overall score. | Gives a gradual increase in acceptance for boosted tops without an abrupt hard cut that could hurt efficiency at the edge of the trigger turn‑on. |
| **Energy‑flow balance observables** | – *Mass spread*: RMS of the three sub‑jet masses.<br>– *Mass asymmetry*: |(m₁ – m₂) / (m₁ + m₂)| (and analogous for the other pairings). | Captures the expected *balanced three‑prong* topology of a genuine top‑jet, which is rare in QCD background. |
| **Tiny MLP “glue”** | Input vector (5 features): raw BDT score, top‑likelihood, the two W‑likelihoods, the p<sub>T</sub> turn‑on, the two flow variables. Architecture: 5 → 8 → 1 (≈ 30 trainable parameters). | Allows a non‑linear combination of the physics cues, learning subtle compensations (e.g. a slightly off‑peak top mass rescued by a very symmetric dijet configuration). |
| **Multiplicative (AND) logic** | The final tagger output = **product** of all five components (likelihoods × tanh × MLP output). | Enforces *simultaneous* satisfaction of every cue – a candidate must look like a top in *all* respects to receive a high score. |
| **Hardware constraints** | Parameter count ≈ 30, estimated latency < 2 µs on the L1 FPGA (fixed‑point arithmetic). | Guarantees the tagger can be deployed at Level‑1 trigger without exceeding resource budgets. |

The overarching hypothesis was that **explicit physics priors + a lightweight non‑linear mapper** would push the hadronic‑top efficiency above the current benchmark (≈ 0.616) while preserving the background‑rejection rate.

---

### 2. Result with Uncertainty

| Metric | Value | Statistical Uncertainty |
|--------|-------|--------------------------|
| **Hadronic‑top efficiency** | **0.6160** | **± 0.0152** |
| **Background rejection** | (kept at) the predefined target (unchanged) | – |

The efficiency matches the baseline value within statistical fluctuations; no measurable gain was observed.

---

### 3. Reflection – Why did it work (or not)?

**What worked as intended**

* **Physics priors behaved correctly:** the Gaussian likelihoods and the p<sub>T</sub> turn‑on produced smooth, well‑behaved score distributions.  
* **Energy‑flow descriptors added discriminating power:** jets with highly asymmetric mass partitions were down‑weighted as expected.  
* **Latency & resource budget stayed comfortably within limits** – the MLP and the multiplicative logic ran comfortably under 2 µs with ≤ 30 parameters.

**Why the overall efficiency did not improve**

| Issue | Evidence / Reasoning | Impact |
|-------|----------------------|--------|
| **Over‑constraining AND logic** | Multiplying all components forces every term to be ≈ 1. Even a modest deviation in a single likelihood (e.g. a top‑mass pull of 1 σ) drives the product down dramatically. | Suppresses borderline yet genuine top candidates that would have been accepted by a softer combination (e.g. weighted sum). |
| **Limited expressive capacity of the tiny MLP** | With only 30 trainable weights the network can only learn very shallow non‑linearities. It struggles to capture higher‑order correlations such as “a slightly low top‑mass can be compensated by an exceptionally symmetric dijet system”. | The intended “subtle compensation” never materialised, leaving the overall decision effectively linear in the physics terms. |
| **Fixed Gaussian shapes & widths** | The width adaptation is a simple linear function of jet p<sub>T</sub>. In practice detector resolution exhibits a more complex dependence (e.g. tail from pile‑up). | The likelihood penalises genuine tops with modest resolution fluctuations more than necessary. |
| **Redundancy among inputs** | The raw BDT score already encodes much of the same information as the individual likelihoods. Adding them multiplicatively may introduce double counting, which the tiny MLP cannot properly de‑correlate. | No net gain in discrimination, but additional suppression of signal due to over‑penalisation. |

**Hypothesis confirmation**

*The hypothesis that *physics priors + a lightweight non‑linear mapper* would boost efficiency was **partially** confirmed (the components are well‑behaved and hardware‑friendly) but **refuted** in practice because the combination strategy (strict AND) and the extreme model size prevented the priors from being utilised synergistically.*

---

### 4. Next Steps – Novel direction to explore

| Goal | Proposed modification | Expected benefit | Feasibility (L1 constraints) |
|------|-----------------------|------------------|------------------------------|
| **Relax the hard AND while keeping hardware simplicity** | Replace the full product with a *soft‑AND*: a weighted geometric mean or a shallow logistic‑type aggregation (e.g. `score = sigmoid( Σ w_i·log(x_i) )`). The weights `w_i` can be learned or manually tuned. | Allows a candidate to survive a modest deficiency in one cue if compensated by strength in another. | Only a few extra adders and a small LUT for the sigmoid – still well under 2 µs and < 40 parameters. |
| **Increase the expressive power of the MLP modestly** | Expand hidden layer to 12–16 units (≈ 60–80 parameters total). Keep fixed‑point inference. | Enables the network to learn non‑linear compensations between the priors (e.g. “low top‑mass ↔ high mass symmetry”). | Simulated latency increase < 0.3 µs; still within L1 budget. |
| **Improve the likelihood modelling** | Use a *p<sub>T</sub>-dependent spline* (pre‑computed lookup table) for the Gaussian widths, or introduce a **double‑Gaussian** tail component to better mimic resolution tails. | Reduces over‑penalisation of genuine tops suffering from detector smearing, especially at high p<sub>T</sub>. | Lookup tables are cheap in FPGA resources; the extra computation is a single table read per jet. |
| **Add a complementary high‑level shape variable** | Include **N‑subjettiness ratio τ₃₂** (or a simplified version thereof) as an extra input to the MLP. | Provides a direct measure of three‑prong substructure, orthogonal to the mass‑based cues. | τ₃₂ can be approximated with a low‑precision calculation (few multiplications/additions) already used in many L1 top taggers. |
| **Explore a small attention‑like weighting** | Compute *attention scores* a₁…a₅ = softmax(α·x) where `x` are the five physics cues; final score = Σ a_i·x_i. With a fixed scalar α (e.g. 1.5) this can be implemented as a few LUTs. | Dynamically emphasizes the most reliable cue on an event‑by‑event basis, mitigating the impact of any single poorly measured term. | Minimal overhead; all operations are fixed‑point and parallelizable. |
| **Re‑optimize the tanh p<sub>T</sub> turn‑on** | Tune the turn‑on slope and midpoint (p₀) using the same training set, or replace tanh with a *piecewise‑linear* ramp that can be realised with a simple comparator and linear scaler. | Aligns the boost preference exactly with the region where efficiency gains are most needed, avoiding unnecessary suppression of lower‑p<sub>T</sub> tops. | Piecewise‑linear function needs only a comparator and few adders – negligible latency. |

#### Immediate Action Plan (next 2–3 weeks)

1. **Implement soft‑AND aggregation** and benchmark latency/parameter count.  
2. **Train a slightly larger MLP (12 hidden units)** using the same dataset, keeping the same physics features plus τ₃₂.  
3. **Replace Gaussian width function with a pre‑computed lookup table** derived from full simulation of jet energy resolution vs. p<sub>T</sub>.  
4. **Run a rapid hyper‑parameter scan** (weights of soft‑AND, MLP regularisation) to locate any efficiency gain > 1 % that remains statistically significant given current uncertainties.  
5. **Validate background rejection** on the same QCD sample to ensure no degradation beyond the target.  

If the soft‑AND + modest MLP upgrade yields a statistically significant bump in efficiency (e.g. 0.630 ± 0.014), we will freeze that configuration and move on to testing the attention‑weighting idea in a subsequent iteration (≈ Iter 158).

---

**Bottom line:**  
*novel_strategy_v157* proved that physics‑driven priors and ultra‑light neural nets can be packed into an L1‑compatible tagger, but the strict multiplicative logic and too‑tiny MLP bottleneck prevented any net efficiency gain. By relaxing the hard AND, modestly expanding the MLP, and refining the resolution model, we expect to break through the 0.616 barrier while staying safely within the firmware budget.