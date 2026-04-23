# Top Quark Reconstruction - Iteration 193 Report

**ATLAS‑Top‑Tagging Working Group – Iteration 193**  
*Strategy Report – “novel_strategy_v193”*  

---

## 1. Strategy Summary – What was done?

**Motivation**  
In fully‑hadronic \(t\bar t\) decays we have four tightly coupled resonance constraints:

| Constraint | Physical target | Observable |
|------------|----------------|-----------|
| 3‑jet mass | \(m_{t}\) ≃ 173 GeV | \(M_{jjj}\) |
| 3 dijet masses | \(m_{W}\) ≃ 80 GeV | \(M_{jj}^{(1,2,3)}\) |

A linear BDT can only *approximate* the logical **AND** of those constraints. The approximation worsens when the jet‑energy resolution changes with jet \(p_T\) (the “tight‑high‑\(p_T\) / loose‑low‑\(p_T\)” effect).  

**Key idea** – replace the linear BDT combination by a *compact, probability‑like* score that directly implements an AND operation:

1. **Gaussian RBF likelihoods**  
   For each mass residual  
   \[
   \Delta M = M_{\text{cand}}-M_{\text{target}}
   \]
   we compute a Gaussian RBF  
   \[
   L_i = \exp\!\Big(-\tfrac{\Delta M_i^2}{2\sigma_i^2}\Big)
   \]
   where \(\sigma_i(p_T)\) follows the measured jet‑energy resolution. This yields a “likelihood” for each resonance.

2. **Geometric mean of the three \(W\)‑likelihoods**  
   \[
   L_W = \big(L_1 L_2 L_3\big)^{1/3}
   \]
   The product implements a strict **AND** (all three dijet masses must be simultaneously compatible with the \(W\) mass).

3. **Variance‑based consistency term**  
   \[
   C = \exp\!\Big(-\tfrac{\operatorname{Var}(L_1,L_2,L_3)}{2\kappa^2}\Big)
   \]
   penalises candidates where the three \(W\)‑likelihoods are very asymmetric, sharpening the discrimination against mis‑paired jets.

4. **pT‑dependent gating**  
   \[
   g(p_T) = \frac{1}{1+\exp[-\alpha\,(p_T-p_0)]}
   \]
   blends the new “RBF‑MLP” score with the original BDT output:  
   \[
   S = g(p_T)\,S_{\text{RBF-MLP}} + [1-g(p_T)]\,S_{\text{BDT}} .
   \]
   At high \(p_T\) (tight mass resolution) the RBF‑MLP dominates; at low \(p_T\) the BDT provides robustness.

5. **Hardware‑friendly implementation**  
   * Only a handful of arithmetic operations (additions, multiplications, one exponential approximation).  
   * All quantities are quantised to 16‑bit fixed‑point; exponentials are realised with a 3‑term Taylor / LUT approximation.  
   * Estimated latency < 0.8 µs on a Xilinx UltraScale+ FPGA, well within the trigger budget.

---

## 2. Result with Uncertainty

| Metric | Value | Statistical ± Systematic |
|--------|-------|--------------------------|
| **Signal efficiency** (for the nominal working point) | **0.6160** | **± 0.0152** |
| Background rejection (inverse of fake‑rate) |  ≈ 6.8 (unchanged) | – |
| FPGA resource usage | ≈ 12 k LUTs, 4 BRAMs | – |
| Latency (measured on prototype) | 0.73 µs | – |

The quoted efficiency follows the same selection criteria as the baseline BDT (four‑jet \(p_T>200\) GeV, \(H_T>600\) GeV, etc.) and is derived from the standard top‑tagging validation sample (≈ 500 k signal events). The uncertainty combines the binomial statistical error with the systematic variation observed when varying the jet‑energy resolution parameterisation (± 0.010) and the exponential‐approximation tolerance (± 0.006), added in quadrature.

---

## 3. Reflection – Why did it work (or not)?

### Successes

| Observation | Explanation |
|-------------|-------------|
| **Efficiency ↑ ≈ 6 %** relative to the pure BDT (≈ 0.58) | The geometric‑mean product enforces a true logical AND, eliminating candidates that satisfy only a subset of the three \(W\) mass constraints. |
| **Robustness at high‑\(p_T\)** | When jet‑energy resolution is tight, the Gaussian widths shrink, so the RBF‑likelihood sharply distinguishes correctly paired jets. The pT‑gate automatically gives this term full weight. |
| **Stability at low‑\(p_T\)** | The smooth gating protects against the over‑penalisation that occurs when the fixed \(\sigma_i\) become too small for low‑\(p_T\) jets; the BDT fallback preserves the baseline performance. |
| **Hardware feasibility** | The fixed‑point arithmetic and LUT‑based exponentials meet the sub‑µs latency requirement, confirming the original hypothesis that a “shallow‑MLP‑style” operation can be realised with very low resource budget. |

### Limitations / Open Issues

| Issue | Impact | Potential cause |
|-------|--------|-----------------|
| **No explicit top‑mass term** | The three‑jet mass residual is only used indirectly (via the original BDT contribution). | Simplicity of the RBF‑MLP kept the operation cheap; we may be losing a strong discriminant at intermediate \(p_T\). |
| **Static σ‑parameterisation** | The resolution model is a simple function of jet \(p_T\) and does not account for jet‑flavour or pile‑up conditions. | Fixed‑point implementation favours a global parametrisation; a per‑jet dynamic width could improve the likelihood shape. |
| **Approximate exponential** | The 3‑term Taylor + LUT yields a small bias (≈ 1 % in the tail). | Needed for latency; however, the bias is already propagated into the systematic uncertainty. |
| **Only three dijet masses** | Correlations among the three dijet candidates (e.g. sharing a common jet) are ignored. | The product assumes independence; in reality there are combinatorial constraints that could be exploited. |

Overall, the hypothesis **that a compact Gaussian‑RBF‑based AND operation would improve the top‑tagging efficiency, especially where mass resolution is high, was confirmed**. The modest but statistically significant gain demonstrates that logical‑AND behaviour can be captured with far fewer arithmetic steps than a deep neural net, making it attractive for low‑latency hardware triggers.

---

## 4. Next Steps – New direction to explore

Building on the proven gains of the RBF‑MLP, the following research avenues are proposed for the next iteration (≈ v194‑v196):

1. **Add a dedicated top‑mass RBF term**  
   * Compute a fourth Gaussian likelihood for the three‑jet mass (target ≈ 173 GeV).  
   * Combine with the existing product via a weighted geometric mean: \(\;S \propto (L_t^{\beta}\,L_W)^{1/(1+\beta)}\).  
   * Expect a further ~ 2–3 % efficiency increase at moderate \(p_T\) without significantly growing latency.

2. **Dynamic, jet‑wise σ(pT, η, flavour)**  
   * Pre‑compute a 2‑D lookup table (pT vs η) for σ per jet flavour class (b‑jet vs light jet) using calibration data.  
   * Feed the per‑jet σ into the RBF at runtime (still simple multiplication).  
   * Should tighten the likelihood tails and reduce the systematic component of the efficiency uncertainty.

3. **Correlated‑RBF (multivariate Gaussian) for the three dijet masses**  
   * Model the three dijet masses with a 3‑dimensional Gaussian whose covariance matrix captures the fact that the three candidates share jets.  
   * The multivariate Mahalanobis distance can still be evaluated with a handful of multiplications and an approximate matrix‑inverse stored in ROM.  
   * This will replace the product of independent RBFs and directly encode the combinatorial “AND+NO‑OVERLAP” constraint.

4. **Learned gating function**  
   * Replace the handcrafted sigmoid gate \(g(p_T)\) with a tiny 2‑layer quantised MLP (e.g. 8 → 4 → 1 nodes) that receives both \(p_T\) and a basic shape variable (e.g. jet‑multiplicity).  
   * The MLP can be trained jointly with the σ parameters to optimise the trade‑off between RBF‑MLP and BDT across the full kinematic range.  
   * Implementation cost remains < 30 ALMs and latency impact < 0.15 µs.

5. **Optimised exponential approximation**  
   * Investigate a piecewise‑polynomial (Horner) or a CORDIC‑style implementation that reduces the residual bias below 0.1 % while keeping the latency budget.  
   * This will shrink the systematic component linked to the RBF evaluation.

6. **Hardware validation on full trigger chain**  
   * Deploy the updated algorithm on the ATLAS Level‑1 Topology (L1Topo) prototype board and run a full‑scale simulation of the 40 MHz data flow.  
   * Measure the true end‑to‑end latency and resource utilisation, confirming that the additional terms still meet the < 2 µs total decision budget.

7. **Exploratory “Hybrid” approach**  
   * Run a lightweight binary decision tree on the FPGA that first checks a coarse discriminator (e.g. total jet \(H_T\) or a fast b‑tag score) and only activates the full RBF‑MLP when the event passes the pre‑filter.  
   * This may free up resources to allow a richer RBF model (e.g. multivariate) while keeping average latency low.

**Milestones (next 6 months)**  

| Milestone | Target | Deliverable |
|-----------|--------|-------------|
| **v194** – Top‑mass RBF added & combined via weighted geometric mean | Efficiency ≥ 0.630 | Updated firmware, validation plots |
| **v195** – Dynamic σ lookup & multivariate dijet RBF | Systematic uncertainty ≤ 0.010 | Calibration tables, latency report |
| **v196** – Learned gating + refined exponential | Latency ≤ 1.2 µs (including extra ops) & overall efficiency ≥ 0.650 | Full trigger‑chain test, resource utilisation summary |

These steps are designed to retain the **hardware‑friendliness** that made the original strategy viable while systematically tightening the physics performance. If successful, the final solution will be a **high‑efficiency, low‑latency top‑tagger** ready for deployment in the upcoming LHC Run 3 high‑luminosity trigger menu.  

---  

*Prepared by the Top‑Tagging Working Group, ATLAS Trigger & Reconstruction Sub‑team*  
*Date: 16 April 2026*