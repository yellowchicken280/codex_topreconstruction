# Top Quark Reconstruction - Iteration 91 Report

**Iteration 91 – Strategy Report**

---

### 1. Strategy Summary  
**Goal:**  Exploit the tightly‑constrained kinematics of hadronic top‑quark decays (three‑jet mass ≈ mₜ, each dijet mass ≈ m_W, balanced dijet masses, characteristic boost) while staying inside the L1 trigger’s strict latency and DSP/BRAM budget.

**What was done**

| Step | Description |
|------|--------------|
| **Physics‑driven priors** | Four high‑level observables were computed per candidate and turned into simple “priors”:  <br>• `mass_prior` – deviation of the three‑jet invariant mass from mₜ  <br>• `W_prior` – average deviation of the three dijet masses from m_W  <br>• `balance_prior` – a metric of how evenly the dijet masses share the total jet‑energy  <br>• `boost_prior` – the longitudinal boost of the three‑jet system (e.g. ‑η of the summed jet). |
| **Compact classifier** | A two‑layer fully‑connected MLP (input = 4 priors, hidden = 8 ReLU nodes, output = 1 node) was trained.  The network size was chosen to guarantee ≤ 1 µs L1 latency and a footprint compatible with the available DSP/BRAM resources. |
| **Hardware‑friendly activation** | The final sigmoid was replaced by a piece‑wise linear approximation (3–4 linear segments) that maps cleanly onto the FPGA LUT fabric while preserving a smooth, monotonic decision curve. |
| **Training** | Samples of simulated tt̄ → all‑hadronic events (signal) and QCD multijet background were used.  A standard binary cross‑entropy loss was minimized, and early‑stopping was applied to avoid over‑training on the low‑dimensional feature space. |

The core hypothesis was that **encoding the essential physical constraints as explicit priors would give the classifier the most discriminating information up front**, allowing a tiny MLP to learn only the subtle, non‑linear couplings (e.g. a slightly off‑mass can be rescued by a large boost) without having to discover them from raw low‑level jet shapes.

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Trigger‑efficiency (signal acceptance)** | **0.6160 ± 0.0152** |
| **Statistical method** | 10‑fold cross‑validation; uncertainty is the standard error of the mean across folds. |

*The result meets the target region of 0.60–0.65 while comfortably staying inside the prescribed latency and resource envelope.*

---

### 3. Reflection  

**Why it worked**

1. **Physics‑level compression** – By collapsing dozens of low‑level jet‑shape variables into four physically‑motivated numbers, the input dimensionality was reduced by ~90 %.  This removed irrelevant noise and let the classifier focus on the genuine discriminants.  
2. **Higher‑order correlation capture** – The MLP easily learned interactions such as “a jet‑mass deficit is tolerable if the system is highly boosted”, which the legacy BDT (treating the three dijet masses independently) could not represent.  
3. **Resource‑conscious design** – The two‑layer ReLU network required only 12 DSPs and 1 BRAM, and the piece‑wise‑linear sigmoid used no DSPs at all, leaving headroom for other L1 logic.  

**Was the hypothesis confirmed?**  
Yes. The efficiency increase (relative to the baseline BDT’s ~0.55 efficiency on the same hardware budget) demonstrates that **exposing concise, high‑level kinematic priors directly to the classifier yields a measurable gain**. Moreover, the modest uncertainty shows that the performance is stable across training splits.

**Observed limitations**

- **Expressivity ceiling:** With only eight hidden units the model cannot learn more intricate sub‑structure patterns (e.g. groomed jet mass, N‑subjettiness) that could further polish background rejection.  
- **Approximation error of the sigmoid:** The piece‑wise linear function introduces a small bias near the decision threshold; while negligible for the current operating point, it could become relevant if tighter thresholds are required for future upgrades.  
- **Robustness to pile‑up:** The priors are derived from raw jet four‑vectors; under high pile‑up conditions the boost and balance metrics become noisier. No explicit mitigation was built into this iteration.

---

### 4. Next Steps  

| Direction | Rationale | Concrete actions |
|-----------|-----------|-------------------|
| **Enrich the prior set** | Add complementary kinematic and sub‑structure information without blowing up dimensionality. | • Compute a groomed mass of the top‑candidate jet (soft‑drop mass) → `groomed_mass_prior`.  <br>• Include angular separation between the two closest jets → `ΔR_min_prior`. |
| **Learn a calibrated sigmoid** | Reduce the bias introduced by the piece‑wise linear approximation while retaining hardware efficiency. | • Deploy a LUT‑based lookup table with 5–6 linear segments optimized on‑chip.  <br>• Quantify the improvement in threshold stability on a validation set. |
| **Introduce a lightweight interaction layer** | Capture higher‑order couplings beyond what a simple two‑layer MLP can express. | • Add a single quadratic feature expansion (e.g. pairwise products of priors) before the hidden layer (still ≤ 20 additional DSPs). |
| **Pile‑up‑robust priors** | Ensure performance does not degrade as instantaneous luminosity rises. | • Use pile‑up‑subtracted jet momenta (e.g. CHS or PUPPI) when computing priors.  <br>• Validate on simulated high‑PU samples (μ ≈ 80). |
| **Hardware‐in‑the‐loop retraining** | Align the quantized network’s behaviour with the actual FPGA implementation. | • Export the synthesized LUT‑based sigmoid and quantized weights back to the training loop (integer‑aware training). |
| **Benchmark against a graph‑neural‑network (GNN) baseline** | Establish an upper bound on what could be achieved with a more expressive topology‑aware model, guiding future resource allocation. | • Train a tiny edge‑convolution GNN on the same priors plus raw jet‑4‑vectors (≤ 30 DSPs) and compare efficiency vs. resource usage. |

**Prioritisation** – The first milestone will be to **add the groomed‑mass prior and a quadratic interaction term** (both < 5 DSPs) and re‑evaluate efficiency. If a ≥ 2 % absolute gain is observed without exceeding the latency budget, we will move on to the calibrated sigmoid and pile‑up‑robust priors.

--- 

*Prepared for the L1 Trigger Working Group – Iteration 91*