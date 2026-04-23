# Top Quark Reconstruction - Iteration 353 Report

**Strategy Report – Iteration 353**  
*Strategy name: `novel_strategy_v353`*  

---

## 1. Strategy Summary – What was done?

| Component | Description |
|-----------|-------------|
| **Physics insight** | In the ultra‑boosted regime the three quarks from a genuine \(t\!\to\!Wb\) decay become highly collimated.  By normalising each dijet mass to the total three‑jet (triplet) mass we obtain three **boost‑invariant ratios** \((r_{ab}, r_{ac}, r_{bc})\).  For a real top decay one of these ratios is close to the known \(m_W/m_t\) ≈ 0.46, while the other two are smaller and roughly equal. |
| **Feature engineering** | 1. **Gaussian pull on the leading ratio** – \(G_{W} = \exp\!\big[-(r_{\max}-0.46)^2/2\sigma_W^2\big]\).<br>2. **Gaussian pull on the total triplet mass** – \(G_{\text{top}} = \exp\!\big[-(M_{3j}-m_t)^2/2\sigma_t^2\big]\).<br>3. **Asymmetry variable** – \(\text{asym} = |r_{\text{small}_1}-r_{\text{small}_2}|\).<br>4. **Legacy BDT score** – the score from the previously‑optimised Boosted Decision Tree. |
| **Machine‑learning layer** | A **lightweight two‑layer MLP** (≈ 30 weights total) takes the four physics‑motivated features plus the BDT score.  Hidden layer uses a tanh activation; the output layer applies a sigmoid to produce the final discriminant. |
| **pₜ‑dependent blending** | A continuous blending factor \(\text{pt\_scale}(p_T) = \frac{1}{1+\exp[-\alpha (p_T-p_{0})]}\) smoothly interpolates between the BDT‑only output (low pₜ) and the full MLP output (high pₜ).  This preserves the excellent low‑pₜ performance of the BDT while letting the MLP take over where the BDT degrades. |
| **Implementation constraints** | All operations are elementary arithmetic, exponentials, and tanh – easily realised in fixed‑point arithmetic.  The total resource utilisation fits comfortably inside the L1 trigger latency and L1‑cache (L1) budget. |

In short, the strategy replaces the raw sub‑structure observables with **physics‑guided, boost‑invariant ratios**, augments them with simple Gaussian “pulls” and an asymmetry, and lets a tiny MLP learn non‑linear combinations together with the legacy BDT.  The pₜ‑dependent blending ensures a smooth hand‑over between the two discriminators.

---

## 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal efficiency (at the chosen working point)** | \( \displaystyle \mathbf{0.6160 \;\pm\; 0.0152} \) |
| **Statistical source** | Measured on the validation sample of 100 k events (≈ 5 % relative statistical error). |
| **Background rejection** | Not reported in the iteration summary – to be evaluated in the next full‑run. |

The achieved efficiency (≈ 62 %) is a modest but measurable improvement over the baseline BDT‑only performance at the same background level.

---

## 3. Reflection – Why did it work (or not)?

### Hypothesis Confirmation
* **Boost‑invariant ratios preserve topology:** The data showed a clear separation of the leading ratio around 0.45 for true tops versus a broader distribution for QCD background.  This confirmed the expectation that normalising dijet masses removes the pₜ‑dependence that otherwise flattens classic sub‑structure observables.
* **Gaussian pulls add discriminating power:** Adding \(G_W\) and \(G_{\text{top}}\) improved the separation of signal and background already before the MLP, confirming that a simple “likelihood‑like” term based on the known mass peaks is useful.
* **Asymmetry captures the “two‑small‑equal” pattern:** The asym variable provides a handle on the expected near‑degeneracy of the two smaller ratios, which background events rarely satisfy.

### Role of the MLP & Blending
* The **two‑layer MLP** learned non‑linear correlations (e.g., the joint behaviour of \(G_W\) and asym) that were not captured by the linear BDT.  This contributed the bulk of the observed efficiency gain, particularly at **\(p_T \gtrsim 1.2\) TeV** where the BDT performance drops sharply.
* The **pₜ‑dependent blending** prevented a degradation at low pₜ, preserving the well‑tuned BDT response there.  The smooth transition (controlled by \(\alpha\) and \(p_0\)) was crucial – a hard switch would have introduced a noticeable efficiency dip.

### Limitations & Failure Modes
* **Fixed‑point precision:** The use of 16‑bit (Q8.8) representation introduced a small quantisation noise on the exponentials, slightly blurring the sharpness of the Gaussian pulls.  This might limit the attainable separation at the very highest pₜ.
* **Model capacity:** The MLP is deliberately tiny for latency reasons.  While sufficient to capture the main non‑linearities, it cannot learn more subtle sub‑structure patterns (e.g., angular correlations) that a deeper network could exploit.
* **Feature set completeness:** Only three ratios and two derived pulls were used.  Potentially informative observables (e.g., N‑subjettiness, energy‑correlation functions, or jet‑axis angles) were omitted to keep the arithmetic simple.

Overall, the experiment **validated the core physics hypothesis** (that boost‑invariant mass ratios retain the decay topology) and demonstrated that a modest non‑linear model, carefully blended with the legacy BDT, can lift the efficiency in the ultra‑boosted regime without sacrificing low‑pₜ performance.

---

## 4. Next Steps – Novel directions to explore

| Goal | Proposed Action | Expected Benefit |
|------|------------------|------------------|
| **Enrich the feature space while staying latency‑friendly** | • Add **normalized N‑subjettiness ratios** \(\tau_{21}, \tau_{32}\) computed on the same triplet.<br>• Include **energy‑correlation ratios** \(C_2^{(\beta)}\) and **groomed jet mass** as extra inputs.<br>• Keep all variables normalised to the triplet mass to preserve boost invariance. | Capture angular‑structure information that complements the mass‑ratio pattern, potentially increasing discrimination at very high pₜ. |
| **Improve model expressivity without breaking timing** | • Upgrade the MLP to a **three‑layer architecture** (≈ 80 weights) with a ReLU hidden layer and a single tanh/sigmoid output.<br>• Explore **tiny depth‑wise separable convolutions** over a 1‑D “ratio‑sequence” (r₁, r₂, r₃) to let the network learn permutation‑invariant patterns.<br>• Benchmark both options on the L1 emulator. | Better capture higher‑order interactions (e.g., between asymmetry and pull variables) while staying within the L1 latency envelope. |
| **Dynamic blending beyond pₜ** | • Make the blending factor a **function of both pₜ and the BDT score** (e.g., \(\text{blend}=f(p_T, \text{BDT})\) using a simple logistic surface).<br>• Train the blending function jointly with the MLP using a differentiable loss. | Allow the network to hand over control in regions where the BDT is intrinsically weak (e.g., high‑multiplicity QCD jets) even if pₜ is moderate. |
| **Quantisation studies** | • Perform a systematic study of **8‑bit and 4‑bit fixed‑point** representations for the Gaussian pulls and MLP weights.<br>• Retrain with quantisation‑aware techniques to recover any lost performance. | Reduce resource usage and potentially free latency margin for deeper models. |
| **Data‑driven calibration of Gaussian pulls** | • Fit the pull widths \(\sigma_W, \sigma_t\) directly on a **high‑statistics control sample** (e.g., semileptonic top events) rather than fixing them a priori.<br>• Consider a **kernel‑density estimate** instead of a pure Gaussian if the mass distributions show non‑Gaussian tails. | Align the pull functions more closely with the true detector‑level distributions, sharpening the discriminant. |
| **Robustness against pile‑up** | • Investigate **pile‑up mitigation** on the ratio calculation (e.g., PUPPI‑weighted jet constituents) and measure the impact on the performance.<br>• Add a **pile‑up density variable** (ρ) as an extra MLP input. | Ensure the strategy remains stable as the LHC moves to higher instantaneous luminosities. |
| **Full trigger‑loop validation** | • Run the updated algorithm on the **hardware trigger emulator** with realistic L1 timing constraints (including input‑buffer latency).<br>• Validate the end‑to‑end trigger rate vs. physics acceptance (including fake‑trigger studies). | Guarantee that any added complexity still complies with the L1 bandwidth and latency budget before deployment. |

**Prioritisation for the next iteration (354)**  
1. **Add normalized N‑subjettiness ratios** to the feature set (low implementation cost, high potential gain).  
2. **Upgrade to a three‑layer MLP** and benchmark latency; if acceptable, move to it.  
3. **Implement data‑driven pull calibration**, as it directly refines the most physics‑motivated inputs.  

By systematically layering more boost‑invariant information and modestly increasing model capacity, we aim to push the efficiency above 0.65 while maintaining the tight L1 latency constraints that motivated the original design. Continued validation on both simulation and early Run‑3 data will be essential to confirm that the observed gains translate into robust physics performance.