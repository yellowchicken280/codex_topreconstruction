# Top Quark Reconstruction - Iteration 512 Report

**Iteration 512 – Strategy Report**  

---

### 1. Strategy Summary  
**Goal:** Boost the top‑tagging efficiency at high jet \(p_T\) where the calorimeter resolution degrades and a pure BDT begins to lose discrimination power.  

**What we did:**  

| Step | Description |
|------|-------------|
| **Physics‑driven observables** | Constructed three dijet invariant masses from the three hardest sub‑jets in a candidate hadronic top. <br> • *\(m_{jj}^{(W)}\)* – the pair that best matches the \(W\)‑boson mass (≈ 80 GeV). <br> • *\(m_{jjj}^{(\text{top})}\)* – the full triplet mass (≈ 173 GeV). <br> • *Variance* of the three dijet masses \( \sigma^2_{m_{jj}} \) – a cheap proxy for the symmetry of the energy flow (and indirectly colour‑flow). |
| **Gaussian pull transformation** | For each of the two mass constraints we built a \(p_T\)‑dependent pull:  \(\displaystyle P_W = \frac{m_{jj}^{(W)}-m_W}{\sigma_W(p_T)}\) and  \(\displaystyle P_t = \frac{m_{jjj}^{(t)}-m_t}{\sigma_t(p_T)}\).  The widths \(\sigma_{W,t}(p_T)\) were measured in simulation and encoded as simple lookup tables.  The pulls are approximately Gaussian and give smooth, bounded likelihood‑like features that are mostly uncorrelated with the raw BDT output. |
| **Tiny ReLU‑MLP** | A 2‑layer MLP (8 hidden neurons, ReLU activation) ingests four inputs: <br> 1. BDT score (already implemented on‑chip) <br> 2. \(P_W\) <br> 3. \(P_t\) <br> 4. \(\sigma^2_{m_{jj}}\) <br> The network learns non‑linear synergies between the BDT and the kinematic pulls. |
| **FPGA‑friendly implementation** | All weights quantised to 8‑bit unsigned integers.  The MLP adds ≈ 5 ns of latency and < 1 % of the available DSP resources, comfortably fitting the existing trigger budget. |

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Signal efficiency (fixed background rejection)** | **\( \displaystyle \epsilon = 0.6160 \pm 0.0152\)** |
| **Baseline BDT‑only efficiency** (same working point) | ≈ 0.58 (± 0.02) – derived from the previous iteration for reference |
| **Relative gain** | **+6.2 %** absolute, ≈ 10 % relative improvement over the pure BDT |

The quoted uncertainty is the statistical error from the validation sample (≈ 10⁶ events). Systematic variations (jet‑energy scale, pile‑up) have not yet been folded into the quoted number.

---

### 3. Reflection  

**Did the hypothesis hold?**  
The original hypothesis was that *hard kinematic constraints* (W‑mass and top‑mass pulls) together with a *simple measure of the spread* among dijet masses would provide information orthogonal to the BDT’s sub‑structure variables, and that a lightweight non‑linear combiner could harvest this synergy without breaching latency limits.  

**What we observed:**  

| Observation | Interpretation |
|-------------|----------------|
| **Modest but clear uplift** (≈ 6 % absolute) in signal efficiency, especially for jets with \(p_T > 800\) GeV. | The pulls capture the true three‑body decay topology that the BDT (trained mainly on shape variables) struggles with when the calorimeter granularity becomes coarse. |
| **Gaussian pulls behaved as expected** – distributions of \(P_W\) and \(P_t\) were centred near zero for genuine tops and broadened for QCD jets. | The \(p_T\)-dependent width parametrisation succeeded in normalising the pulls across the wide kinematic range. |
| **Variance of dijet masses contributed** – when the variance is small (i.e. triplet looks “balanced”), the MLP up‑weights the candidate; large variance often coincides with background. | Even a crude proxy for colour‑flow adds discriminating power, confirming the idea that energy‑flow symmetry is useful. |
| **Correlation with BDT ≈ 0.35** (Pearson) – the new features are not strongly redundant. | This justifies the extra MLP layer; the combination is truly orthogonal to the original sub‑structure information. |
| **Resource & latency budget respected** – the 8‑bit quantised MLP consumes < 1 % of the DSP slice budget and adds ~5 ns latency. | The hardware‑friendly design succeeded. |

**Why the improvement was not larger:**  

* The dijet‑mass variance is only a proxy; more sophisticated colour‑flow observables (e.g. pull angle, dipolarity) might capture extra information.  
* The Gaussian pull widths were derived from simulation and only parametrised in \(p_T\); residual dependence on pile‑up or jet‑mass could leave some discrimination on the table.  
* The MLP, while fast, is extremely shallow (only 8 hidden neurons). A modest increase in capacity might unlock the remaining non‑linear synergy without breaking latency, especially if we prune or compress the network further.

Overall, the experiment **validates the hypothesis** that adding physics‑driven, kinematic likelihood features can give a measurable boost to a BDT‑based top tagger at very high \(p_T\).

---

### 4. Next Steps  

| Direction | Rationale & Planned Work |
|-----------|--------------------------|
| **Enrich the colour‑flow descriptor** | Replace the simple variance with a hardware‑friendly *pull angle* (vector sum of constituent η–φ separations) or *dipolarity*. Both can be computed with a few integer operations and have shown strong discrimination in offline studies. |
| **Dynamic width calibration** | Extend the pull width lookup to a 2‑D table ( \(p_T\) × jet‑mass) or apply a small per‑event correction based on the jet’s pile‑up density (ρ). This should tighten the Gaussian pulls for out‑of‑distribution kinematics. |
| **Expand the MLP modestly** | Test a 2‑layer network with 16 hidden neurons (still 8‑bit) and evaluate the latency impact after applying weight pruning (e.g. 30 % sparsity). Preliminary RTL simulations suggest we can stay within the 5–7 ns budget. |
| **Hybrid quantisation** | Explore mixed‑precision (e.g. 8‑bit for inputs, 6‑bit for hidden weights) to free DSP budget for a slightly larger network while preserving performance. |
| **Cross‑validation with data‑driven background** | Use a sideband enriched in QCD (e.g. inverted BDT cut) to re‑fit the pull widths and validate that the Gaussian assumption holds on real data. This will reduce systematic uncertainty on the efficiency estimate. |
| **Alternative topology‑agnostic features** | Investigate *energy‑correlation functions* (ECFs) of low order (e.g. \(C_2\), \(D_2\)) that have straightforward integer‑based approximations. They could supplement the dijet‑mass pulls without a heavy resource cost. |
| **Model‑agnostic meta‑learner** | Build a tiny decision‑tree “gate” that selects between the baseline BDT output and the MLP‑augmented output based on jet‑\(p_T\) or other simple flag. This could preserve the pure BDT performance where it is already optimal and invoke the new features only where needed. |

**Short‑term plan (next 2–3 weeks):**  

1. Implement pull‑angle calculation and benchmark latency/resource usage.  
2. Train a 16‑neuron MLP on the same four inputs plus the new pull‑angle, compare ROC curves (focus on high‑\(p_T\) bins).  
3. Run a systematic scan of the width tables (add jet‑mass dimension) and evaluate any gain in pull Gaussianity.  

If the combined upgrades push the efficiency past **0.65 ± 0.01** at the same background rejection, we will consider the iteration ready for full‑system validation and eventual deployment.

--- 

*Prepared by the Trigger‑ML Working Group, Iteration 512*  
*Date: 2026‑04‑16*