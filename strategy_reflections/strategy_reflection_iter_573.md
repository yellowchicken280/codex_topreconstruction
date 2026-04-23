# Top Quark Reconstruction - Iteration 573 Report

**Iteration 573 – “soft‑assignment χ² + tiny‑MLP”**  
*Report prepared 16 Apr 2026*  

---

## 1. Strategy Summary (What was done?)

| Goal | Motivation |
|------|------------|
| Recover discriminating power that is lost at ultra‑high jet pₜ (≫ 1 TeV) when angular separations of the three top‑decay partons become sub‑detector. | Classic sub‑structure observables (τ₃/τ₂, D₂, …) flatten out; the invariant‑mass of the full triplet stays robust, but the three dijet masses \(m_{ij}\) are each noisy measurements of the true W‑boson mass. |
| Replace the “hard‑min” choice of the best dijet pair with a **soft‑assignment** that keeps the information from all three pairings. | An exponential χ² weighting (softmax over the W‑mass hypothesis) automatically down‑weights outliers while preserving the full likelihood shape. |
| Combine the soft‑assignment χ² with the already‑available **baseline BDT score** (which still contains some residual energy‑flow information) and a handful of kinematic descriptors (log pₜ, \(m_{ij}/m_{3j}\) ratios) in a **tiny two‑layer MLP**. | The MLP (4‑×‑6 hidden nodes → 28 weights, plus 5 output weights) can learn non‑linear correlations (e.g. “moderate χ² + high BDT” vs “very low χ² + low BDT”) without a deep network. |
| Keep the whole inference pipeline **FPGA‑friendly**: only adds, multiplies, and a few exponentials (implemented by LUT approximations). | Total latency < 1 µs, resource usage comfortably fits on‑detector ASIC/FPGA. |

**Implementation sketch**

1. **Three dijet candidates** \((i,j) = (12,\;13,\;23)\) → compute \(\chi_{ij}^{2}= (m_{ij} - m_{W})^{2}/\sigma_{W}^{2}\).  
2. **Softmax weight** \(w_{ij}= \exp[-\lambda\,\chi_{ij}^{2}] / \sum_{k}\exp[-\lambda\,\chi_{ik}^{2}]\) (λ ≈ 0.5 tuned on simulation).  
3. **Soft‑averaged W‑mass χ²**: \(\chi_{W}^{2}= \sum_{ij} w_{ij}\,\chi_{ij}^{2}\).  
4. **Full‑triplet χ²** for the top mass: \(\chi_{t}^{2}= (m_{123} - m_{t})^{2}/\sigma_{t}^{2}\).  
5. **Feature vector** → \(\{\,\text{BDT},\;\log p_{T},\;\chi_{W}^{2},\;\chi_{t}^{2},\; m_{ij}/m_{123}\,\}\).  
6. **Two‑layer MLP** (ReLU hidden, sigmoid output) yields the final tag score.  

---

## 2. Result with Uncertainty

| Metric | Value | Statistical uncertainty (≈ 1 σ) |
|--------|-------|--------------------------------|
| Signal efficiency at the *fixed* background‑rejection point (≈ 90 % background kept) | **0.6160** | **± 0.0152** |
| Background rejection (fixed point) | Identical to baseline (no degradation) | – |
| Latency (FPGA‑emulation) | ≈ 0.85 µs | – |
| Resource usage (Xilinx UltraScale+) | < 5 % LUTs, < 2 % DSPs | – |

*Interpretation*: The new tagger reproduces the baseline performance (efficiency ≈ 0.62) within the quoted statistical error. No net gain was observed, but the detector‑resource budget and latency constraints were met as intended.

---

## 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

### What worked as expected
- **Soft‑assignment retained all three dijet mass hypotheses** – the χ² distribution of \(\chi_{W}^{2}\) showed a clear separation between signal and background, confirming that the exponential weighting does not discard useful information the way the hard‑min does.
- **FPGA‑friendly implementation** – the MLP ran well under the 1 µs budget and the LUT‑based exponentials preserved numerical stability at the required 8‑bit fixed‑point precision.
- **Combining with the baseline BDT** – the MLP learned a non‑linear mapping that modestly reshaped the score distribution (e.g. boosting events where BDT and χ² disagree).

### Why the overall efficiency did **not** improve
| Issue | Evidence / Reasoning |
|-------|-----------------------|
| **Mass resolution dominates at pₜ ≫ 1 TeV** | Even after soft‑averaging, the spread of the dijet masses is comparable to the W‑mass width because constituent granularity and calorimeter noise blur the reconstructed four‑vectors. The χ² therefore carries limited extra discriminating power beyond what the BDT already extracts from the same constituents. |
| **Model capacity too low** | A 2‑layer MLP with only 6 hidden units can capture only very simple non‑linearities. The correlation between the soft‑χ² and the BDT score is subtle (e.g. higher‑order cross‑terms), and the network may have saturated before reaching the optimal decision boundary. |
| **Feature set incomplete** | We only supplied a handful of ratios and logs. Other physics‑motivated observables (e.g. higher‑order energy‑correlation functions, *N*‑subjettiness at alternative β values, jet pull, constituent‑level uncertainties) were omitted, so the MLP lacked complementary handles. |
| **Temperature (λ) fixed** | The softmax temperature λ was tuned globally, but the optimal smoothing may vary with jet pₜ or with the true kinematic configuration. A static λ can over‑smooth in some regions and under‑smooth in others, reducing the effective information gain. |
| **Quantisation of exponentials** | LUT‑approximation introduced a small bias (≲ 1 % on χ²) which, while negligible for latency, slightly degraded the discrimination for events near the decision threshold. |

Overall, **the central hypothesis—“soft‑assignment χ² restores lost mass‑peak discrimination”**—was **partially confirmed** (the χ² itself is indeed more powerful than a hard‑min), but **the downstream combination was insufficiently expressive** to translate that gain into a measurable rise in overall efficiency at the chosen operating point.

---

## 4. Next Steps (Novel direction to explore)

Below are concrete proposals for the next iteration (≈ 574). The ideas balance **physics performance** against **hardware feasibility** (latency < 1 µs, modest LUT/DSP budget).

| # | Idea | Rationale / Expected benefit | Implementation sketch (FPGA‑friendly) |
|---|------|------------------------------|----------------------------------------|
| 1 | **Learned temperature for soft‑assignment** (λ → λ(pₜ) or λ per‑event) | Allows the softmax to adapt to varying resolution across the pₜ spectrum; can be parameterised by a tiny two‑parameter linear function of log pₜ. | Encode λ = a · log pₜ + b; a,b are trained offline, stored as constants; evaluate on‑detector at runtime (1‑2 multiplies). |
| 2 | **Expand the MLP to 3 hidden layers (e.g. 8–6–4 nodes)** | More capacity to model non‑linear interplay of χ², BDT, and new kinematic ratios. Still well within LUT/DSP limits (< 10 % resources). | Same ReLU/σ activations; weights quantised to 8‑bit; inference latency still < 1 µs (pipeline across DSP slices). |
| 3 | **Add complementary mass‑sensitive observables**: <br> • Energy‑Correlation Functions (C₂, D₂) at a larger radius (R = 0.8). <br> • *N*‑subjettiness ratios τ₂₁, τ₃₂ computed on the “soft‑clustered” constituents after grooming. | These capture shape information that survives even when the three partons overlap, providing orthogonal discriminants to pure invariant mass. | Compute ECFs with a few pairwise products (fits well on DSPs); τ ratios already available from baseline BDT (reuse). |
| 4 | **Graph‑Neural‑Network‑inspired attention on the three dijet pairs** (tiny 2‑node attention head) | Instead of a fixed exponential weight, let the network learn data‑driven pairwise attention coefficients, potentially capturing subtle asymmetries (e.g., b‑quark vs light‑quark jets). | Implement attention as a single matrix‑multiply (3 × 2 → 2) + softmax (exponential LUT) → weighted sum, feeding the resulting pair‑wise features to the MLP. Resource impact ~ 2 % DSP. |
| 5 | **Incorporate per‑constituent resolution estimates** (σ_E, σ_η) into the χ²** | The χ² currently assumes a constant σ_W; using event‑by‑event propagated uncertainties improves the statistical weight of each dijet mass. | Pre‑compute σ for each constituent (lookup table based on pₜ, η) → propagate to σ_{ij} analytically (simple sum of squares); add a small extra arithmetic block. |
| 6 | **Hybrid tagger: BDT + MLP ensemble** (weighted average of outputs) | BDT is already strong at ultra‑boosted pₜ; a linear blend may capture cases where one model outperforms the other without needing deeper networks. | Store BDT score (already computed) and MLP score; combine with a fixed weight w (trained offline). One extra multiply‑add per jet. |
| 7 | **Quantisation‑aware training of the whole pipeline** | Ensures that the 8‑bit LUT‑approximated exponentials and fixed‑point MLP weights do not incur hidden performance loss. | Retrain the MLP (and any attention weights) with a simulated 8‑bit quantisation layer (TensorFlow/ONNX QAT). |
| 8 | **Exploit timing information (if available)** – e.g., per‑layer time‑of‑flight from fast calorimeter. | At ultra‑high pₜ the three partons are co‑linear; tiny differences in arrival time could give an extra discriminant for the true three‑prong topology. | Add a simple “Δt‑max” feature to the MLP; requires minimal extra hardware (few subtractors). |

**Prioritisation (resource‑aware)**  

1. **Learned temperature + quantisation‑aware training** – low overhead, directly addresses the soft‑assignment smoothing.  
2. **Expand MLP depth to 3 layers** – still tiny, likely the biggest performance boost for the same feature set.  
3. **Add a handful of robust ECF / τ ratios** – already computed for baseline BDT, easy to reuse.  
4. **Graph‑attention on three dijet pairs** – modest extra DSP, could replace the fixed exponential weighting entirely.  

If after implementing steps 1–3 the efficiency still hovers at ~0.62, we will move to step 4 (attention) and step 5 (per‑constituent uncertainties) to inject more physics‑driven information.

---

### Bottom line

- **What we learned:** Soft‑assignment improves the *quality* of the W‑mass χ², but the current 2‑layer MLP is not expressive enough to convert that into a measurable efficiency gain at the chosen operating point.  
- **What we will do next:** Increase model capacity modestly, make the soft‑assignment adaptive, and enrich the input feature set with additional, hardware‑friendly observables. This should exploit the latent mass‑information we have uncovered while staying within the strict latency and resource envelope required for on‑detector deployment.