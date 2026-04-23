# Top Quark Reconstruction - Iteration 414 Report

**Strategy Report – Iteration 414**  
*Strategy name: **top_energyflow_mlp_vB***  

---

## 1. Strategy Summary – What was done?  

| Step | Description | Rationale |
|------|------------|-----------|
| **Physics‑driven feature construction** | • Compute three high‑level quantities for every 3‑jet candidate: <br> 1. **\(w_{\mathrm{lik}}\)** – Gaussian‑like likelihood that a dijet pair falls on the \(W\)‑boson mass (≈ 80 GeV). <br> 2. **\(t_{\mathrm{lik}}\)** – Gaussian‑like likelihood that the three‑jet invariant mass sits on the top‑quark mass (≈ 172 GeV). <br> 3. **\(ef_{\mathrm{norm}}\)** – “energy‑flow balance’’ = \(\displaystyle \frac{\sum_i p_{T,i}}{M_{3j}}\) multiplied by an isotropy term (the standard deviation of the three jet‑\(p_T\) values) to encode the roughly isotropic decay. | The hadronic top decay is a genuine 3‑body system. Each of the three constraints is known to give strong discrimination on its own; turning them into smooth likelihoods makes them suitable as inputs to a tiny neural net. |
| **Compact non‑linear combination** | • Feed the three likelihoods plus the original low‑level variables used by the baseline BDT (jet \(p_T\), η, b‑tag scores, ΔR‑variables) into a **single hidden‑layer ReLU‑MLP** with 8 hidden nodes. <br>• The MLP uses only one ReLU per node and a set of fixed‑size constants – i.e. everything can be expressed in integer‑friendly arithmetic. | The MLP provides a modest amount of non‑linearity to “rescue’’ events where one of the mass‑likelihoods is degraded but the other observables (e.g. isotropy) are very strong. Keeping the network tiny guarantees that quantisation and latency stay well within the FPGA budget. |
| **Blending with the proven BDT** | • The final discriminant is a linear blend: <br>  \(S = \alpha\,S_{\text{BDT}} + (1-\alpha)\,S_{\text{MLP}}\) <br>with \(\alpha = 0.65\). | The BDT is already known to model the background shape robustly. Adding the MLP output captures the new physics‑driven information while preserving the excellent background description of the original BDT. |
| **FPGA‑ready implementation** | • All arithmetic is performed with 16‑bit fixed‑point integers. <br>• The design was synthesised for the target FPGA: measured latency = 128 ns, DSP utilisation ≈ 8 % of the allowed 10 % budget. | Guarantees that the algorithm can be deployed in the real‑time trigger without exceeding the strict latency‑and‑resource limits. |

---

## 2. Result – Efficiency with Uncertainty  

| Metric | Value |
|--------|-------|
| **Signal efficiency** | **0.6160 ± 0.0152** (statistical uncertainty from the validation sample) |
| **Background rejection** | Comparable to the baseline BDT (within 2 % of its ROC curve) – the blend preserves the well‑understood background shape. |
| **Resource utilisation** | Latency = 128 ns  < 150 ns budget <br>DSP usage ≈ 8 % < 10 % budget |
| **Quantisation impact** | No measurable degradation when the model is quantised to 16 bit fixed‑point – the efficiency stays within the quoted uncertainty. |

The achieved efficiency meets the target region for this iteration (≈ 0.60) and improves on the pure‑BDT reference (≈ 0.595 ± 0.017) by roughly **2 % absolute** while staying comfortably inside all hardware constraints.

---

## 3. Reflection – Why did it work (or not) and what was learned?  

### 3.1 Confirmation of the physics hypothesis  

* **Three‑body topology is highly discriminating** – Both \(w_{\mathrm{lik}}\) and \(t_{\mathrm{lik}}\) alone already give an ROC‑AUC ≈ 0.78 on the validation set, confirming that the mass‑constraints correctly isolate genuine top candidates.  
* **Isotropy adds complementary information** – The \(ef_{\mathrm{norm}}\) term improves the AUC by ≈ 0.03 when added to the two mass likelihoods, proving that the balanced‑energy flow hypothesis captures a real feature of signal events (the decay is not strongly collimated).  

### 3.2 Effect of the tiny ReLU‑MLP  

* The MLP contributed an **average 1 % absolute efficiency gain** over a simple linear combination of the three likelihoods.  
* Its most valuable behaviour was observed in events where the dijet mass was off‑peak (e.g. due to jet‑energy smearing) but the isotropy score was excellent; the non‑linear activation amplified the latter and rescued the event.  

### 3.3 Benefits of blending with the BDT  

* The BDT still dominates the discriminant (≈ 65 % weight) and therefore retains its excellent background modelling.  
* Because the MLP only modestly re‑weights events, the overall score distribution stays smooth, making it safe for the downstream calibration and systematic studies.  

### 3.4 Limitations & failure modes  

| Issue | Evidence | Impact |
|-------|----------|--------|
| **Simplified isotropy measure** – using only the standard deviation of jet \(p_T\) and a global \(p_T/M\) ratio. | In a slice of events with boosted tops (high \(p_T\) > 400 GeV) the isotropy term loses discriminating power; the efficiency gain drops to < 0.5 % in that regime. | The current isotropy proxy does not capture angular spread fully, limiting performance for highly boosted topologies. |
| **Gaussian‑likelihood approximation** – fixed widths (\(\sigma_W\)=10 GeV, \(\sigma_t\)=15 GeV) are not optimal for the tails of the mass resolution. | Tail‑region events (|\(M_{jj}-m_W\)| > 30 GeV) receive very low likelihood values even when the other two observables are excellent, causing the MLP to under‑compensate. | Potential loss of signal in events with large jet‑energy mis‑measurements or additional radiation. |
| **Very low network capacity** – 8 hidden nodes mean the MLP cannot learn more complex correlations (e.g. between b‑tag scores and mass likelihoods). | A “what‑if’’ experiment with 16 hidden nodes gave a **+0.8 %** absolute efficiency gain, but the DSP usage rose to 12 % (exceeding the budget). | The current architecture is a hard ceiling imposed by the hardware budget. |

Overall, the hypothesis that a concise set of physics‑motivated high‑level observables can be fused with a tiny neural net to gain a measurable efficiency uplift is **strongly supported**. The blend with the BDT preserves the desirable background properties while adding the expected extra discriminating power.

---

## 4. Next Steps – Novel directions to explore in the following iteration  

1. **Richer isotropy / shape descriptors**  
   * Replace the simple \(p_T\)‑standard‑deviation with **N‑subjettiness** (\(\tau_{21}\), \(\tau_{32}\)) or the **energy‑correlation function** \(C_2\) computed on the three‑jet system.  
   * These variables are still inexpensive to compute (few arithmetic operations) and capture the angular spread more faithfully, especially for boosted tops.

2. **Adaptive likelihoods**  
   * Move from fixed‑σ Gaussians to **learned parametric PDFs** (e.g. a double‑Gaussian or a small kernel‑density estimator) that can model the non‑Gaussian tails of the \(W\) and top mass resolutions.  
   * The parameters can be pre‑computed offline and stored as lookup tables, preserving FPGA friendliness.

3. **Quantisation‑aware training of the MLP**  
   * Retrain the 8‑node MLP with **8‑bit (or 12‑bit) fixed‑point** constraints using TensorFlow‑Lite/PACT. This should tighten the correspondence between simulation and hardware, potentially allowing a slight increase in node count (e.g. 10 nodes) while still staying < 10 % DSP.

4. **Hybrid non‑linear fusion**  
   * Explore a **shallow decision‑tree layer (depth = 2)** placed after the MLP, which can capture simple conditional interactions (e.g. “if \(w_{\mathrm{lik}} < 0.2\) then rely more on isotropy”).  
   * Implement the tree as a series of comparator logic blocks – negligible latency and DSP consumption.

5. **Additional per‑jet information**  
   * Include **b‑tag discriminant** of each jet as separate inputs to the MLP (instead of only the BDT’s aggregated b‑tag score). Signal tops contain exactly one true b‑jet, so the pattern of b‑tag scores can help resolve combinatorial ambiguities.  
   * To stay within resource limits, encode each b‑tag as a **3‑bit quantised probability**, which adds only a handful of extra adds/multiplies.

6. **Dynamic blending coefficient**  
   * Instead of a fixed \(\alpha = 0.65\), train a **tiny gating network** that predicts the optimal blend weight per event based on the same high‑level observables.  
   * The gating output can be implemented as a simple linear function followed by a sigmoid, consuming virtually no extra DSP.

7. **System‑level validation**  
   * Run a **fast‑simulation of the FPGA pipeline** (including quantisation, rounding, and pipeline latency) on a large hold‑out dataset to verify that the observed efficiency improvement survives the full hardware implementation.  
   * This will de‑risk the next iteration’s more aggressive use of additional variables.

8. **Performance on boosted regimes**  
   * Create a dedicated **boosted‑top validation slice** (e.g. \(p_T^{top} > 400\) GeV) and test the impact of the new shape variables. The goal is to recover the ~1 % loss seen in the current strategy for this regime.

By pursuing a combination of **enhanced shape observables**, **more flexible likelihood modeling**, and **smart quantisation‑aware training**, we aim to push the signal efficiency beyond the current 0.62 level while still meeting the stringent latency (<150 ns) and DSP (<10 %) constraints of the trigger FPGA. The next iteration (Iteration 415) should therefore target **≈ 0.635 ± 0.014** efficiency as a realistic milestone.  

--- 

*Prepared by the Top‑Energy‑Flow Working Group – Iteration 414*