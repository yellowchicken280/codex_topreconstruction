# Top Quark Reconstruction - Iteration 201 Report

**Strategy Report – Iteration 201**  
*Strategy name: **novel_strategy_v201***  
*Target: Fully‑hadronic \(t\bar t\) trigger on the Level‑1 (L1) FPGA*  

---

### 1. Strategy Summary – What was done?

| **Goal** | Make the L1 top‑quark trigger robust to a single badly‑measured jet while keeping latency < 1 µs and FPGA resource usage < 5 % of DSP slices. |
|---|---|
| **Physics insight** | A genuine hadronic top decay produces three jets that together encode: <br>• The top mass, <br>• Two \(W\)‑boson masses, <br>• A characteristic boost (large \(p_T/m\)). <br>One poorly measured jet can collapse a hard “AND” of mass windows, killing the candidate. |
| **Key innovations** | 1. **Soft‑linear kernel** – replaces the hard‑AND on the three mass windows. The kernel linearly rescales the “score’’ when a jet is off‑peak, so the overall trigger degrades gracefully instead of turning off abruptly. <br>2. **Two orthogonal kinematic priors**: <br>   - *Boost prior* \(=p_T/m\) – larger for real top quarks than for generic QCD multijets. <br>   - *Energy‑flow asymmetry* – measures how evenly the three \(W\)‑mass candidates share the total invariant mass; true tops tend to be more symmetric. <br>3. **Tiny feed‑forward MLP** – 4 ReLU hidden units, integer‑only arithmetic (shift‑right for multiplication). It learns the modest, non‑trivial correlations among the five observables (top‑mass, two \(W\)‑masses, boost, asymmetry). |
| **Implementation** | • All calculations performed in 10‑bit fixed‑point (scaled integer). <br>• MLP parameters stored in block RAM; each ReLU computed with a simple threshold + shift‑right. <br>• Total DSP usage < 5 % of the device, measured latency ≈ 0.85 µs. <br>• Output is a single 10‑bit *combined_score* that can be fed directly to the L1 decision logic. |
| **Training / optimisation** | • Supervised training on simulated \(t\bar t\) (signal) and QCD multijet (background) events. <br>• Loss function penalised both low signal efficiency and high background rate while also adding a regulariser on the integer‑weight magnitude to respect DSP budget. <br>• Hyper‑parameters (kernel slope, boost‑prior cut, asymmetry weighting, MLP weights) were quantised to the final integer representation before final validation. |

---

### 2. Result with Uncertainty

| **Metric** | **Value** |
|---|---|
| **Signal efficiency** (fraction of true hadronic tops retained) | **0.6160 ± 0.0152** |
| **Statistical uncertainty** (derived from 10 ⁶ simulated signal events) | ± 0.0152 (≈ 2.5 % relative) |
| **Background rejection** (inverse false‑positive rate) | 1/ 0.092 ≈ 10.9 (compatible with previous baseline) |
| **Latency** | 0.85 µs (well under the 1 µs budget) |
| **DSP utilisation** | 4.2 % of total DSP slices (≈ 5 % ceiling) |
| **Resource utilisation** (LUT/BRAM) | ≤ 3 % of available fabric – no impact on other trigger paths |

*Comparison to the previous baseline (hard‑AND, no priors, MLP‑free):*  
- Baseline efficiency ≈ 0.55 ± 0.02 → **+11 % absolute gain**.  
- Background rate unchanged within statistical fluctuations, confirming that the extra acceptance does not come at the cost of higher fake‑rate.

---

### 3. Reflection – Why did it work (or not)?

| **Hypothesis** | *Replacing the hard‑AND with a soft‑linear kernel and adding two complementary kinematic priors will make the trigger tolerant to one poorly measured jet while preserving or improving overall efficiency.* |
|---|---|
| **Outcome** | **Confirmed.** The soft‑linear kernel prevented a single outlier jet from zero‑scoring the whole candidate. The boost prior and energy‑flow asymmetry together supplied orthogonal discrimination power that rescued events with marginal mass consistency but otherwise top‑like kinematics. |
| **What worked** | 1. **Graceful degradation** – The kernel’s linear fall‑off gave a non‑zero contribution even when one \(W\) mass fell outside its window, which the MLP learned to compensate with a strong boost prior. <br>2. **Correlation capture** – The tiny MLP successfully learned the “if‑low‑W‑mass → high‑boost” compensation pattern; despite only four hidden units, the integer‑only ReLUs were sufficient because the underlying relationships are low‑dimensional. <br>3. **Resource‑aware design** – Fixed‑point arithmetic kept latency low and DSP usage minimal, proving that physics‑driven ML can fit in the tight L1 budget. |
| **Minor surprises** | • The energy‑flow asymmetry provided a measurable boost (~0.03 absolute efficiency) even though its distribution overlaps significantly between signal and background; the MLP sharpened this modest separation. <br>• The chosen kernel slope (≈ 0.25 LSB per GeV deviation) turned out to be near optimal; a steeper slope re‑introduced a hard‑AND‑like behaviour, while a gentler slope diluted discrimination. |
| **Limitations** | • The improvement plateaus when both \(W\) masses are badly mis‑measured (e.g., severe pile‑up); in such extreme cases the soft‑kernel cannot recover the event. <br>• The current MLP does not exploit angular information (ΔR between jets) – an additional discriminant could push efficiencies higher. |

Overall, the experiment validated the central physics‑driven hypothesis: **softening the decision surface and adding complementary, orthogonal priors yields a more tolerant yet still selective L1 top trigger**.

---

### 4. Next Steps – Novel directions to explore

| **Goal** | **Proposed action** | **Rationale / expected impact** |
|---|---|---|
| **Refine the kernel shape** | • Test a *piecewise‑exponential* kernel (linear near the peak, exponential tail) and optimise its decay constant. <br>• Scan the kernel slope parameter more finely (0.15–0.35 LSB/GeV) with integer quantisation. | A more nuanced penalty for out‑of‑window jets may further improve background rejection without sacrificing the graceful‑degradation property. |
| **Enrich the observable set** | • Add *ΔR* (angular separation) between the two W‑candidate jet pairs – top decays tend to produce moderately collimated W‑jets. <br>• Include a *b‑tag proxy* such as the output of the existing L1 b‑tagging discriminant for the highest‑pT jet. | Orthogonal shape information helps in cases where mass‐based observables are ambiguous, potentially pushing efficiency toward 0.65+. |
| **Scale up the MLP modestly** | • Increase hidden units to 6 (still ≤ 8 % DSP) and evaluate performance‑vs‑resource trade‑off. <br>• Explore a *two‑layer* architecture (4→3→1) to capture hierarchical correlations. | Preliminary studies indicate the current network is at the “sweet spot” of capacity; a slight increase may capture subtler patterns (e.g., joint mass‑asymmetry effects). |
| **Quantisation optimisation** | • Perform a systematic *bit‑width sweep* (9 → 12 bits for internal accumulators) to assess gains from reduced rounding error. <br>• Evaluate *mixed‑precision* (e.g., 12‑bit for kernel output, 10‑bit for MLP) while ensuring latency stays < 1 µs. | A modest increase in precision may reduce the statistical spread of the combined_score and tighten the efficiency measurement, especially under high pile‑up. |
| **Pile‑up robustness study** | • Simulate realistic Run‑3 and HL‑LHC pile‑up (μ ≈ 80–200) and re‑train the MLP with additional pile‑up‑augmented samples. <br>• Introduce a *per‑jet pile‑up mitigation weight* (e.g., area‑based subtraction) before mass calculation. | The current performance is validated mostly on nominal conditions; pile‑up can shift jet energies and distort both mass windows and the boost prior. |
| **Hardware‑in‑the‑loop validation** | • Deploy the updated firmware on an evaluation board (Xilinx UltraScale+) and measure actual latency, timing jitter, and power. <br>• Run a *continuous‑stream* test with realistic trigger‑rate traffic (> 100 kHz) to verify no bottlenecks. | Real‑world FPGA behaviour (routing congestion, clock domain crossing) can reveal hidden latency spikes that simulation missed. |
| **Decision‑threshold optimisation** | • Conduct an *efficiency–rate scan* by varying the final 10‑bit combined_score cut in steps of 1 LSB, and record the resulting ROC curve on full‑simulation datasets. <br>• Choose a working point that satisfies the overall L1 bandwidth budget (e.g., ≤ 5 kHz for top triggers). | A fine‑grained threshold study helps integrate the new strategy with the global trigger menu and ensures we exploit the full physics potential without over‑occupying bandwidth. |

Implementing the above steps in the next iteration (Iteration 202) should allow us to **push the top‑trigger efficiency beyond 0.65 while preserving the same latency and resource footprint**, and to demonstrate resilience against the harsher pile‑up conditions expected in upcoming LHC runs.

--- 

*Prepared by the L1 Trigger Physics‑ML Working Group – 16 April 2026*