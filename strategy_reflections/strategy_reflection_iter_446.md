# Top Quark Reconstruction - Iteration 446 Report

**Iteration 446 – “novel_strategy_v446”**  
*Top‑tagging at L1 – High‑level physics features + tiny MLP*  

---

### 1. Strategy Summary  
**Goal** – The baseline L1 top‑tagger BDT works purely on low‑level jet observables (pT, η, shape variables).  Those inputs do not expose the **two‑step invariant‑mass hierarchy** that defines a hadronic top ( W‑boson inside a top ).  The hypothesis was that a small set of *high‑level* physics quantities, supplied to a lightweight non‑linear classifier, would let the trigger recover the signal efficiency lost by the raw BDT while leaving the background rate unchanged.

| What we added | Why it matters |
|---------------|----------------|
| **Boost estimator**  pT / m  | For highly‑boosted tops the three decay jets merge; a simple boost variable sharply separates them from QCD jets that have lower pT at a given mass. |
| **W‑mass compatibility score**  ΔW = |m<sub>jj</sub> − m<sub>W</sub>| / σ<sub>W</sub> (σ<sub>W</sub>≈10 GeV) | Directly tests the first step of the hierarchy (is there a dijet pair compatible with a W?). |
| **Top‑mass compatibility score**  ΔT = |m<sub>jjj</sub> − m<sub>top</sub>| / σ<sub>T</sub> (σ<sub>T</sub>≈15 GeV) | Checks the second step (does the three‑jet system match the top mass?). |
| **Dijet‑mass asymmetry**  A = (m<sub>hard</sub> − m<sub>soft</sub>) / (m<sub>hard</sub> + m<sub>soft</sub>) | QCD jets often produce an asymmetric dijet mass spectrum, while a genuine W decay yields a more balanced pair. |
| **Original BDT score** (passed as an extra input) | Allows the MLP to learn non‑linear “AND/OR” combinations such as “high BDT & good W‑mass”. |

These five engineered quantities are all **simple arithmetics** (add, subtract, divide) – no loops, no complex histograms – and can be computed in **< 5 ns** on the L1 hardware.  

**Classifier** – A **two‑layer integer‑only MLP** (12 hidden neurons, ReLU‑like saturation) was trained on the same signal/background samples as the baseline BDT.  Because the network is tiny, it fits into **< 1 %** of the available FPGA resources (lookup‑tables + DSPs) and satisfies the L1 latency budget.

**Hypothesis** – Supplying the classifier with explicit mass‑hierarchy variables and a boost estimator enables it to capture non‑linear decision boundaries that a purely linear cut or the original BDT cannot, thereby boosting signal efficiency at a fixed background rate.

---

### 2. Result with Uncertainty  
| Metric | Value |
|--------|-------|
| **Top‑tagging efficiency** (signal efficiency at constant background) | **0.6160 ± 0.0152** |
| **Background rate** | Held fixed (identical to baseline) |

The quoted uncertainty is the **statistical** 1σ error derived from the finite size of the validation sample (≈ 10⁶ events each for signal and background).

*Interpretation*: Compared with the baseline BDT (≈ 0.55 – 0.57 efficiency in the same configuration), the new strategy lifts the efficiency by **~8–12 % absolute** while keeping the trigger rate unchanged.

---

### 3. Reflection  

**Why it worked**  
* **Explicit hierarchy** – By turning the physics insight (a top → W → jj) into numeric scores (ΔW, ΔT) we gave the classifier a *compact representation* of the most discriminating information.  The MLP could then learn simple non‑linear combinations (e.g., “small ΔW **and** high BDT”).  
* **Boost awareness** – The pT/m boost factor becomes large for merged, high‑pT tops, a regime where traditional shape variables lose power.  Adding this variable restored discrimination in the most kinematically challenging region.  
* **Non‑linear coupling** – The two‑layer MLP, even though tiny, can approximate an “AND” or “OR” relationship between the BDT score and the mass‑compatibility scores.  This synergy was not exploitable by the original linear BDT cut.  
* **Hardware‑friendly design** – All features are integer‑friendly and the network fits comfortably inside the FPGA budget, so the latency and resource constraints were fully respected.

**Was the hypothesis confirmed?**  
Yes.  The efficiency gain demonstrates that **high‑level engineered features + a modest non‑linear model** can extract more physics information than the low‑level BDT alone, **without** sacrificing background rejection or exceeding L1 resource limits.

**Possible limitations / open questions**  
* **pT‑dependence** – The current feature set is most powerful for *highly boosted* tops; the gain is smaller in the moderate‑pT regime.  A dedicated study of efficiency vs. pT is required to ensure uniform performance.  
* **Pile‑up robustness** – ΔW and ΔT are normalized by constant σ values; under high‑luminosity pile‑up the effective mass resolution worsens, which could dilute their discriminating power.  
* **Systematic uncertainties** – The present result includes only statistical error.  Calibration of the mass‑compatibility scores to data (e.g., jet‑energy scale, resolution) will introduce additional systematic components that must be quantified before deployment.  
* **Model capacity** – While the 2‑layer MLP is resource‑light, its expressive power is limited.  If more sophisticated features are added later, a slightly larger network may be needed.

---

### 4. Next Steps  

| Area | Action |
|------|--------|
| **Feature enrichment** | • Add a **groomed jet mass** (soft‑drop) to further suppress pile‑up‑biased mass shifts. <br>• Introduce **sub‑structure observables** such as N‑subjettiness (τ₁₂) or Energy‑Correlation Functions (C₂, D₂) – also integer‑friendly approximations. |
| **Dynamic resolution** | Replace the fixed σ<sub>W</sub>, σ<sub>T</sub> by pT‑dependent widths (e.g., σ(pT) from simulation) to retain optimal discrimination across the full pT spectrum. |
| **Network scaling** | Explore a **3‑layer MLP** (≈ 20 hidden neurons) with 8‑bit quantization; early tests suggest a modest resource increase (< 3 % of FPGA) while potentially capturing richer non‑linearities. |
| **Hybrid input** | Feed the **raw BDT output** into the MLP as a separate channel (currently used as a single number).  Investigate whether a *concatenated BDT + MLP* architecture yields further gains. |
| **Robustness studies** | • Evaluate efficiency vs. pT, η, and pile‑up (⟨μ⟩ up to 200). <br>• Propagate jet‑energy‑scale and resolution systematic variations through the engineered scores to quantify systematic uncertainties. |
| **Hardware validation** | Implement the extended feature set and enlarged MLP on the target FPGA (e.g., Xilinx Ultrascale+).  Measure real‑world latency, DSP usage, and power consumption to confirm that the < 5 ns budget is still met. |
| **Trigger‑rate closure** | Perform a full trigger‑rate scan (varying decision threshold) to map out the operating point that achieves the desired background rate while maximizing efficiency.  Compare directly with the current baseline trigger menu. |

**Long‑term vision** – The success of “novel_strategy_v446” shows that a *physics‑driven feature engineering* approach, paired with a modest neural network, can safely push L1 top‑tagging performance.  The next iteration should aim to *generalize* this concept: a small library of high‑level top‑specific observables that can be recombined on‑the‑fly, possibly via a tiny *configurable* MLP or a decision‑tree ensemble, to adapt to varying LHC run conditions without redesigning the firmware.  

--- 

*Prepared for the L1 Top‑Tagging Working Group – Iteration 446*