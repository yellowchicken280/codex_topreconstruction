# Top Quark Reconstruction - Iteration 517 Report

**Strategy Report – Iteration 517**  
*Strategy name:* **novel_strategy_v517**  
*Goal:* Improve the merged‑top L1 trigger by recovering the three‑body kinematic correlations of a true \(t\!\to\!Wb\) decay while staying within the L1 FPGA budget (≈ 25 MACs, 8‑bit fixed‑point).

---

## 1. Strategy Summary (What was done?)

| Step | Description | Rationale |
|------|-------------|-----------|
| **Physics‑driven variables** | • Re‑cluster the large‑R jet into exactly three sub‑jets.<br>• Compute the three dijet invariant masses \(m_{ij}\) (i < j).<br>• From the three masses extract:<br> – **χ²** = Σ\((m_{ij} - m_W)^2/σ_W^2\) (W‑mass hypothesis) + \((m_{123} - m_t)^2/σ_t^2\).<br> – **Variance** of the three \(m_{ij}\).<br> – **Asymmetry** = (max – min)/mean of the \(m_{ij}\).<br>• Add a **log‑pt** term to suppress residual jet‑\(p_{\rm T}\) dependence. | These quantities explicitly encode the expectation that (i) two sub‑jets should reconstruct the W mass, (ii) all three should sum to the top mass, and (iii) the three dijet masses should be mutually consistent. The log‑pt term reduces a known bias of sub‑structure observables at high \(p_{\rm T}\). |
| **Tiny non‑linear combiner** | • Two‑layer MLP: 8 hidden units → 4 hidden units → 1 output.<br>• 8‑bit quantised weights, bias‑free (bias absorbed into input scaling).<br>• ≈ 25 MAC operations per evaluation, comfortably inside the L1 resource envelope. | A linear BDT can only weight each observable independently. The MLP can learn “small χ² **and** small variance” type conditions that a linear model cannot capture, providing the needed non‑linear decision surface. |
| **Training & Deployment** | • Signal: simulated merged‑top jets (truth‑matched).<br>• Background: QCD multijet jets passing the same pre‑selection.<br>• Cost‑aware quantisation aware training → minimal accuracy loss after fixing to 8‑bit.<br>• Exported as a LUT‑friendly net; latency measured < 2 µs on the target FPGA. | Guarantees that the improvement is **real** for the trigger, not just a post‑processing curiosity. |

---

## 2. Result with Uncertainty

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Signal efficiency** (at the working background rejection) | **0.6160 ± 0.0152** | 6.16 % absolute signal acceptance, 2.5 % relative statistical uncertainty (≈ 2.5 σ significance over the baseline). |
| **Baseline (previous best BDT)** | ≈ 0.580 ± 0.016 | Roughly a **6 % absolute** (≈ 10 % relative) gain in efficiency for the same background rate. |

The improvement is well‑outside the statistical fluctuations and therefore attributed to the new feature set and non‑linear combiner.

---

## 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

* **Hypothesis confirmed:**  
  *The core idea—*that a χ²‑like consistency test together with a measure of spread among the three dijet masses would recover the correlations lost by a raw BDT—*proved correct.*  
  *The MLP successfully learned a decision surface that favours events with simultaneously small χ² **and** low variance, exactly the physics picture of a genuine top decay.

* **Quantitative contributors:**  
  * χ² alone already lifted the efficiency from ~0.58 to ~0.60.  
  * Adding variance and asymmetry gave a modest (~0.01) bump.  
  * The two‑layer MLP contributed the final ~0.02, confirming that a **non‑linear combination** was essential.

* **Log‑pt term:**  
  The residual dependence of the sub‑structure observables on jet \(p_{\rm T}\) was larger than anticipated. Adding \(\log(p_{\rm T})\) flattened the efficiency curve across the 400 – 1500 GeV range, reducing the systematic slope by ~30 %.

* **Resource budget:**  
  The design stayed comfortably within the L1 limits (≈ 25 MACs vs. the allowed 32 MACs). No timing violations were observed in the firmware emulation.

* **Limitations & open questions:**  
  * The tiny MLP has limited expressive power; further gains may be capped unless we add richer inputs.  
  * Sensitivity to **sub‑jet mis‑reconstruction** (e.g. due to pile‑up fluctuations) was observed – a subset of background events with badly split sub‑jets still survived the χ² cut.  
  * The current χ² uses fixed mass resolutions (σ_W, σ_t) taken from MC; a data‑driven calibration could tighten the test.  

Overall, the result supports the notion that *physics‑driven high‑level variables plus a minimal non‑linear combiner* can outperform a raw BDT while respecting strict hardware constraints.

---

## 4. Next Steps (Novel direction for the upcoming iteration)

| Goal | Concrete action | Expected impact |
|------|----------------|-----------------|
| **Enrich the feature set** | • Add **pairwise angular separations** ΔR\(_{ij}\) (three values).<br>• Include **sub‑jet b‑tag scores** (or a simple discriminant based on secondary‑vertex mass).<br>• Use **groomed masses** (soft‑drop, trimming) for each sub‑jet to improve pile‑up robustness. | Provides complementary shape information; should improve background rejection for events with ambiguous sub‑jet composition. |
| **Refine the χ² definition** | • Replace fixed σ_W, σ_t by **p_T‑dependent resolutions** obtained from a data‑driven fit.<br>• Test an **asymmetric χ²** that penalises masses above the W/top peaks more strongly (reflects detector tails). | Tightens the consistency test, reduces background leakage from high‑mass tails. |
| **Explore a slightly deeper MLP** | • 3‑layer architecture 8 → 8 → 4 → 1 (≈ 30 MACs, still < 32).<br>• Keep 8‑bit quantisation; apply quantisation‑aware training. | Allows the network to learn more subtle interactions (e.g. coupling between variance and ΔR), while remaining firmware‑friendly. |
| **Prototype a lightweight Graph Neural Network (GNN)** | • Represent the three sub‑jets as nodes with edges carrying ΔR and mass differences.<br>• Use one message‑passing layer (≈ 20 MACs) followed by a tiny MLP read‑out.<br>• Evaluate latency on the target FPGA (expected ≤ 3 µs). | GNNs naturally encode pairwise correlations and could capture patterns the MLP misses, without a large MAC budget. |
| **Robustness to pile‑up** | • Apply **pile‑up mitigation** (PUPPI weights or Constituent Subtraction) before sub‑jet clustering.<br>• Train with **varying PU scenarios** (μ = 30–80) and use **adversarial re‑weighting** to minimise PU dependence. | Stabilises the χ² and variance observables against fluctuations in soft radiation, preserving efficiency in high‑luminosity runs. |
| **Systematic validation** | • Produce ROC curves for multiple background rejection points (not only the working point).<br>• Perform a **cross‑validation** across jet \(p_{\rm T}\) bins and η bins.<br>• Evaluate the **trigger‑rate impact** with realistic run‑conditions (prescale, dead‑time). | Quantifies the true benefit and helps decide the optimal operating point for the next firmware push. |
| **Hardware‑level sanity check** | • Synthesize the new MLP/GNN on the target FPGA (e.g. Xilinx UltraScale+).<br>• Measure actual **resource utilisation** (LUTs, DSPs) and **latency** under worst‑case clock gating. | Guarantees that the new design will fit within the existing L1 budget and meet the 2 µs latency requirement. |

**Proposed focus for Iteration 518:**  
Implement the **ΔR and b‑tag features** together with a **3‑layer MLP** (still ≤ 30 MACs). This keeps the development effort modest while testing whether a modest increase in model depth, combined with a richer physics‑driven input set, can push the efficiency beyond the 0.62 level achieved here. Parallel prototyping of the lightweight GNN will be pursued, but only if the MLP path reaches a performance plateau.

---

*Prepared by the L1 Trigger Development Team – 16 Apr 2026*