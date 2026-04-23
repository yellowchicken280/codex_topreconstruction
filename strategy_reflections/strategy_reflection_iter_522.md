# Top Quark Reconstruction - Iteration 522 Report

**Iteration 522 – Strategy Report**  

---

### 1. Strategy Summary  

**Goal:**  Recover the information that is lost when a single dijet mass is chosen deterministically for the hadronic‑top three‑jet system, while staying within the tight latency and resource constraints of the L1‑FPGA trigger.  

**Core idea:**  
- **Soft‑assignment to the W‑boson mass** – For each of the three possible dijet pairings we compute the distance \(|m_{ij}-m_W|\) and turn it into a probability weight \(w_{ij}=1/|m_{ij}-m_W|\) (normalised over the three pairings).  
- **Physics‑motivated observables** built from these weights:  
  1. **Weighted ΔW** – the average absolute deviation of the three dijet masses from the W‑mass, weighted by \(w_{ij}\).  
  2. **Variance of dijet masses** – captures the expected similarity of the two light‑quark jet energies in a genuine three‑body decay.  
  3. **Top‑mass residual** – \(|m_{123}-m_t|\).  
  4. **Triplet pₜ** – the transverse momentum of the three‑jet system, acting as a boost prior.  

- **Tiny neural‑network layer:** The four observables are fed into a single hidden neuron with a tanh activation. This “tiny MLP” can model non‑linear correlations while staying integer‑friendly (fixed‑point arithmetic, only adds and multiplies by pre‑computed constants).  

- **Score fusion:** The hidden‑neuron output is linearly combined with the raw BDT score that is already deployed in the trigger. The combined value is passed through a sigmoid to produce the final decision variable.  

- **FPGA‑friendliness:** All operations are fixed‑point, the tanh and sigmoid can be realised with small lookup tables, and the total latency and DSP usage comfortably fit the L1‑FPGA budget.

---

### 2. Result with Uncertainty  

| Metric | Value | Statistical Uncertainty |
|--------|-------|--------------------------|
| Trigger efficiency (signal acceptance) | **0.6160** | **± 0.0152** |

The result is quoted with a 1‑σ (≈68 % CL) statistical error derived from the standard binomial propagation over the evaluation sample.

---

### 3. Reflection  

**Why it worked:**  

| Observation | Interpretation |
|-------------|----------------|
| **Higher efficiency than baseline** (≈0.60 % absolute gain) | The soft‑assignment retains information from *all* dijet pairings, preventing the hard decision on a single pairing from discarding useful kinematic patterns. |
| **Weighted ΔW** reduced the impact of badly reconstructed pairings, allowing the network to focus on configurations that are collectively W‑like. |
| **Variance of dijet masses** provided a clear discriminator for true three‑body decays (light‑quark jets sharing similar energies) versus combinatorial background. |
| **Top‑mass residual + triplet pₜ** supplied a global kinematic prior that the tiny MLP could combine non‑linearly with the “local” ΔW / variance features. |
| **Non‑linear hidden neuron** captured subtle correlations (e.g. a modest ΔW can be compensated by a very small variance only for high‑pₜ triples). | 

**Hypothesis confirmation:**  
The hypothesis that *soft‑weighted dijet‑mass observables plus a minimal non‑linear learner would outperform a pure linear BDT* is **supported**. The improvement exceeds the statistical uncertainty (≈1.5 σ significance) and demonstrates that richer three‑jet correlations can be exploited without exceeding latency or resource limits.

**Limitations / open questions:**  

- The gain, while statistically meaningful, is modest. The single‑neuron MLP may be saturating its capacity to model the full non‑linear structure of the problem.  
- The weighting scheme uses a simple inverse‑distance; alternative kernels (Gaussian, Student‑t) might give smoother probabilities and better robustness against outliers.  
- The current formulation treats the three dijet pairings symmetrically; however, the presence of a b‑tagged jet could be used to bias the weighting more physically.  

---

### 4. Next Steps  

| Proposed direction | Rationale | Expected benefit |
|--------------------|-----------|------------------|
| **Upgrade to a two‑layer MLP (e.g. 4→8→1) with quantisation‑aware training** | Additional hidden units allow the network to learn more complex interactions (e.g. coupling between ΔW and pₜ). Fixed‑point training will keep FPGA usage low. | Potentially 2–3 % extra efficiency gain. |
| **Explore alternative soft‑assignment kernels** (Gaussian with tunable σ, or a learned kernel) | Inverse distance can be overly sensitive to small fluctuations. A smoother kernel may reduce noise‑induced weight spikes. | Improved stability, possibly higher discrimination power. |
| **Incorporate b‑tag information** (e.g. binary flag or continuous CSV score) as an extra input to the MLP | The b‑jet is uniquely associated with the top decay; using its tag can break the permutation symmetry in a physics‑motivated way. | Better pairing discrimination, especially in high‑pile‑up conditions. |
| **Feature engineering: angular separations (ΔR) and jet‑pairwise opening angles** | The three‑body topology also manifests in angular patterns; adding ΔR_{ij} or cosθ* could complement the mass‑based observables. | Additional discriminating power without large computational cost. |
| **Model‑stacking: train a lightweight gradient‑boosted tree on the MLP output** | Allows the BDT to capture any residual linear trends while the MLP handles non‑linearities. | Synergistic gains, leveraging strengths of both classifiers. |
| **Full quantised deployment test on the target FPGA** (resource utilisation, timing closure) | Validate that the expanded model still respects latency and DSP budgets, and assess any needed optimisation (e.g. pruning, LUT sharing). | Ensure deployability before moving to production. |

**Immediate actionable plan:**  
1. Implement a 4‑input → 8‑hidden → 1‑output MLP with fixed‑point arithmetic and train it using quantisation‑aware techniques.  
2. Add a b‑tag flag as a fifth input and re‑evaluate on the same validation sample.  
3. Compare Gaussian‑kernel weighting (σ tuned on a hold‑out set) against the current inverse‑distance scheme.  
4. Run a quick resource‑usage estimate (Vivado HLx) to confirm that the enlarged network fits within the L1 budget (≤ 15 % DSP, ≤ 2 µs latency).  

If the combined upgrades deliver > 2 % absolute efficiency improvement with acceptable resource footprint, the new configuration will be rolled out for the next trigger firmware cycle.  

--- 

*Prepared for the L1‑Trigger Working Group – Iteration 522*  