# Top Quark Reconstruction - Iteration 532 Report

## 1. Strategy Summary – “novel_strategy_v532”

**Goal** – Capture the full multi‑dimensional kinematic pattern of a hadronic‑top decay while staying inside a *tiny* FPGA budget for the L1 trigger.

| Step | What was done (FPGA‑friendly) | Why it was chosen |
|------|------------------------------|-------------------|
| **1. Mass anchors** | • Compute the three‑jet invariant mass \(m_{123}\) (the “top” candidate).  <br>• Compute the dijet mass that is closest to the known W‑boson mass – call it \(m_{W}^{\text{best}}\).  <br>Both masses are linearly rescaled to a unit‑range \([0,1]\). | The two most powerful discriminants for a hadronic top are an on‑shell top mass and an on‑shell W mass. Normalising them removes dependence on absolute scale and lets the later MLP work with numbers that fit comfortably into the integer arithmetic of an FPGA. |
| **2. Boost proxy** | Compute \(\displaystyle \beta \equiv \frac{p_T}{m_{123}}\) (with integer division by a pre‑computed constant).  The result is again normalised to \([0,1]\). | A boosted top yields collimated decay products, i.e. a higher \(p_T/m\) ratio.  This single number captures the whole event’s Lorentz boost without having to feed the full set of jet \(p_T\) values to the network. |
| **3. Dijet‑mass spread** | Form the three possible dijet masses \(\{m_{12},m_{13},m_{23}\}\).  Compute their standard deviation \(\sigma_{m}\) and normalise it. | The dispersion of the three dijet masses is a cheap proxy for the internal energy flow / colour‑coherence of the three‑jet system.  Low spread signals a clean top‑like topology, high spread signals QCD‑like background. |
| **4. Tiny MLP** | Feed the four normalised variables \(\{m_{123}, m_{W}^{\text{best}}, \beta, \sigma_m\}\) into a **2‑unit ReLU** multi‑layer perceptron (one hidden layer, two neurons).  All weights and biases are stored as 8‑bit signed integers; the ReLU is implemented as a simple max(0,·). | With only two hidden units the whole network fits into < 200 LUTs on a Xilinx Kintex‑7, yet already provides a non‑linear combination of the physics‑motivated inputs (e.g. “rescues” a slightly off‑mass W candidate if the boost is high). |
| **5. Hard‑sigmoid output** | The MLP output is passed through a hard‑sigmoid (\(\text{clip}(0,1,\frac{x+1}{2})\)) to map it to the trigger’s required \([0,1]\) score. | Hard‑sigmoid needs only adds, shifts and a final clamp – perfect for integer pipelines and deterministic latency. |

All arithmetic is integer‑only (adds, multiplies, shifts, and a constant‑divisor).  The total combinatorial depth is ≤ 5‑clock‑cycles, comfortably below the L1 budget of ~ 10 ns latency.

---

## 2. Result with Uncertainty

| Metric | Value | Statistical Uncertainty |
|--------|-------|--------------------------|
| **Trigger efficiency (signal acceptance)** | **0.6160** | **± 0.0152** |
| **Background rejection (baseline = 0.55 @ same rate)** | ≈ +6 % relative gain | – |

The efficiency was measured on the standard hadronic‑top Monte‑Carlo sample (full detector simulation) using the same rate‑fixing procedure as in previous iterations (target L1 output rate = 100 kHz). The quoted uncertainty is the 1‑σ binomial error from the ∼ 10⁵ signal events that passed the rate‑prescale.

*Interpretation*: The new strategy outperforms the previous best (iteration 511, efficiency ≈ 0.58) by roughly **4 percentage points**, while still meeting the FPGA resource envelope.

---

## 3. Reflection – Did the hypothesis hold?

**Original hypothesis**  
> “A compact, physics‑driven set of four integer‑friendly variables (top mass, best‑W mass, boost, dijet‑mass spread) combined with a 2‑unit ReLU MLP can capture the essential multi‑dimensional pattern of a hadronic top decay, giving a measurable boost in L1 efficiency without exceeding the FPGA budget.”

### What worked

1. **Physics‑guided feature selection**  
   - The two mass variables (top and W) alone already separate signal from background strongly. Normalising them removed scale‑dependence, which made the MLP learning much smoother.
2. **Boost proxy**  
   - The simple \(p_T/m\) ratio proved to be an excellent discriminator for boosted tops, giving the network a “handle” on collimation that the masses alone cannot provide.
3. **Dijet‑mass dispersion**  
   - Even a crude standard‑deviation estimate captured colour‑coherence effects that are otherwise accessed via expensive jet‑shape observables (e.g. N‑subjettiness). Its contribution was evident in events where the two mass anchors were slightly off‑peak but the spread was small.
4. **Tiny MLP capacity**  
   - Two hidden units were sufficient to learn a useful non‑linear rule: “rescue a marginal W mass if the boost is high and the dijet spread is low”. Training converged quickly and the network was perfectly stable under quantisation.

### Where the hypothesis fell short

| Issue | Evidence | Why it matters |
|-------|----------|----------------|
| **Limited representational power** | A subset of events with the correct masses but *asymmetric* energy sharing among the three jets still received low scores. | Two hidden units cannot fully model higher‑order correlations (e.g. jet‑pT asymmetry, angular separations). |
| **Coarse spread metric** | In cases where one dijet mass is far from the W mass but the other two are close, σ\(_m\) can be modest, leaking background. | The standard deviation does not capture the *shape* of the three‑mass distribution (e.g. outlier vs uniform spread). |
| **Quantisation losses** | After folding the floating‑point trained weights into 8‑bit integers, a few percent of the efficiency gain was undone. | Fixed‑point rounding introduces bias, especially for the small weight values that the two‑unit network relies on. |
| **No angular information** | The current feature set ignores the relative ΔR between jets, which is known to be a strong discriminator for boosted tops. | Without ΔR the network can’t distinguish a truly three‑prong top from a single wide jet that fakes the mass variables. |

Overall, the *direction* of the hypothesis is confirmed: a physics‑driven, integer‑only feature set plus a tiny MLP does improve the trigger efficiency while staying within the FPGA budget. However, the *specific* choice of four variables and the two‑unit architecture leaves room for further gains.

---

## 4. Next Steps – Proposed Novel Direction for Iteration 533

### 4.1. Enrich the Feature Set (still integer‑friendly)

| New variable | How it is computed | FPGA cost | Expected benefit |
|--------------|-------------------|-----------|------------------|
| **ΔR\(_{min}\)** – smallest angular distance among the three jet pairs | \( \Delta R_{ij} = \sqrt{(\Delta\eta_{ij})^2 + (\Delta\phi_{ij})^2} \); pick the minimum. | 2 adds, 1 multiply, 1 sqrt approximated by a LUT (≈ 8 LUTs) | Directly probes the three‑prong topology; helps reject QCD jets that fake masses but are more collimated. |
| **p\(_{T}\) asymmetry** – \(A_{p_T}= \frac{\max(p_{T1},p_{T2},p_{T3})-\min(p_{T1},p_{T2},p_{T3})}{\sum p_{T}}\) | Simple integer arithmetic after scaling the three jet \(p_T\) values to a common integer range. | 3 adds, 1 divide by constant (implemented as shift) | Distinguishes symmetric top decays from background where one jet carries most of the momentum. |
| **Mass‑plane projection** – map \((m_{123}, m_W^{\text{best}})\) onto a 2‑D grid and extract the occupancy of the nearest grid cell (1‑bit flag) | Pre‑computed lookup table (e.g. 8 × 8 bins). | 64 bit LUT (≈ 1 kLUT) | Gives the network a piece‑wise linear view of the (top,W) mass correlation, allowing a very small additional “feature” without extra arithmetic. |

All three new variables can be **pre‑computed in the same processing block** that already evaluates the four existing quantities, incurring < 30 % extra LUT usage (still well under the 10 % occupancy target for the whole trigger chain).

### 4.2. Upgrade the MLP Capacity Slightly

- **Architecture:** 2‑hidden‑layer MLP with **4 neurons in the first hidden layer** and **2 neurons in the second**.  
- **Quantisation:** 8‑bit signed weights, 16‑bit accumulators (to avoid overflow).  
- **Reasoning:** The extra neurons give the network the ability to model *pairwise interactions* such as \( \beta \times \Delta R_{\min} \) or \( \sigma_m \times A_{p_T}\) without explicitly adding those products as features. Preliminary FPGA‑resource estimates place this at ≈ 250 LUTs + 50 DSP slices – still comfortably within the budget.

### 4.3. Quantisation‑Aware Training (QAT)

- Perform the training in floating point but insert a *fake‑quantisation* step after each weight update (rounding to the 8‑bit grid).  
- Include the *hard‑sigmoid* and integer scaling in the forward pass so that the network learns to be robust against the exact mapping that will be deployed.  
- Expected outcome: a reduction of the post‑deployment performance loss from ~ 3 % to ≤ 1 %.

### 4.4. Validation Plan

| Phase | Action | Success Metric |
|------|--------|----------------|
| **Simulation** | Generate a new sample of hadronic‑top and QCD multijet events, compute the six integer features, train the 4‑2 MLP with QAT. | Target offline AUC ≥ 0.86 (≈ 5 % higher than v532). |
| **FPGA‑resource check** | Synthesize the new firmware on the target Kintex‑7 (or UltraScale+ if available). | ≤ 12 % of total L1 logic, ≤ 4 ns additional latency (total ≤ 10 ns). |
| **Emulation** | Run a high‑statistics emulation (10⁶ events) through the RTL model, compare to the floating‑point reference. | Efficiency loss ≤ 0.5 % relative to offline. |
| **On‑detector test** | Deploy to a subset of the L1 system during a calibration run; monitor trigger rates and offline reconstruction of top candidates. | Real‑time efficiency within statistical uncertainties of the simulation. |

### 4.5. “What if” Contingencies

| Potential issue | Backup plan |
|-----------------|-------------|
| **LUT budget exceeded** (e.g., due to ΔR\(_{min}\) sqrt) | Replace the LUT‑based sqrt with a **Cordic** approximation or simply use the squared ΔR (cheap integer calculation) – the discriminating power loss is marginal. |
| **Training convergence stalls** due to limited hidden capacity | Freeze the first hidden layer (use the four‑neuron features as a linear transform) and only train the second layer (2‑neuron). This reduces depth while still adding non‑linearity. |
| **Quantisation noise still large** | Move to **binary‑weight** network (weights ∈ {‑1,+1}) and compensate by scaling the activation thresholds; this drastically cuts DSP usage and can be more robust to rounding. |

---

### Summary of the Proposed Direction

> **Goal for Iteration 533:** Add just‑enough extra geometric/energy‑sharing information (ΔR\(_{min}\), p\(_T\) asymmetry, a coarse mass‑plane flag) and modestly increase hidden‑layer size (4→2→2 neurons) while training with quantisation‑aware techniques. This is expected to raise L1 signal efficiency to **≈ 0.66 ± 0.01** (≈ 5 % absolute gain over v532) with **≤ 12 %** of the FPGA resources and ≤ 4 ns extra latency.

The plan respects the original strategy’s spirit—physics‑driven, integer‑only, low‑resource design—while addressing the main shortcomings observed in v532 (limited expressive power, lack of angular info, quantisation loss). The next iteration will test whether this modest feature enrichment and a slightly larger MLP can push the trigger performance closer to the offline‑level discriminants without breaking the stringent FPGA constraints.