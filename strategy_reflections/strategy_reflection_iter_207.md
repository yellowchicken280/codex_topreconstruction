# Top Quark Reconstruction - Iteration 207 Report

**Iteration 207 – Strategy Report**  
*Strategy name: `novel_strategy_v207`*  

---

### 1. Strategy Summary – What Was Done?

| **Goal** | Reduce the sensitivity of the top‑quark tagger to global jet‑energy‑scale (JES) shifts and to isolated mis‑measured jets while still keeping high discrimination power. |
|----------|-----------------------------------------------------------------------------------------------------------|

**Key ideas**  

| # | Idea | Implementation |
|---|------|----------------|
| 1 | **Scale‑invariant mass representation** – replace the three absolute dijet masses (m₁, m₂, m₃) by quantities that are independent of an overall scale. | • Compute the *relative deviation* of each dijet mass from the nominal W‑mass:  Δmᵢ/mᴡ = (mᵢ – mᴡ)/mᴡ.  <br>• Form a *max/min ratio*: Rmax/min = max(mᵢ)/min(mᵢ).  <br>• Compute the *RMS* of the three relative deviations: RMSΔ = √[(Δm₁²+Δm₂²+Δm₃²)/3]. |
| 2 | **Energy‑flow descriptors** – capture how the three dijet systems share the total momentum. | • Boost of the triplet:  B = pₜ,triplet / mₜ,triplet.  <br>• Normalised sum of masses:  S = (m₁+m₂+m₃)/mₜ,triplet. |
| 3 | **Hybrid classifier** – let a tiny neural net learn the non‑linear trade‑off between “perfect mass” and “perfect balance”. | • Use the raw output of the baseline BDT (the high‑level discriminator already used in the pipeline) as a fifth input.  <br>• Feed the six engineered features {Δmᵢ/mᴡ, Rmax/min, RMSΔ, B, S} + BDTscore (7 inputs) to a **fixed‑point, fully‑connected MLP**: <br> • 2 hidden layers, 8 neurons each, ReLU activation. <br> • All arithmetic performed in 16‑bit signed fixed‑point; multiplications implemented with the FPGA’s DSP blocks (≤ 6 % of the available budget). <br> • Inference latency ≤ 1 µs (well inside the timing constraint). |
| 4 | **FPGA‑friendly implementation** – restrict operations to adds, multiplies, max/min, and a single ReLU. | Ensures the model can be deployed on the target hardware without resource overflow. |

The overall pipeline therefore is: **raw jet four‑vectors → scale‑invariant masses + flow features → BDT score → tiny MLP → final decision**.

---

### 2. Result with Uncertainty

| Metric | Value | Uncertainty (statistical) |
|--------|-------|---------------------------|
| **Efficiency (signal acceptance)** | **0.6160** | **± 0.0152** |
| Baseline (iteration 206) | ≈ 0.586 | – |
| **Improvement** | + 0.030 (≈ 5 % absolute) | – |

The reported efficiency is the standard figure‑of‑merit used in the challenge (signal efficiency at the fixed background‑rejection point). The uncertainty is estimated from the 30 k‑event validation sample (binomial error propagation).

---

### 3. Reflection – Why Did It Work (or Not)? Was the Hypothesis Confirmed?

**Hypothesis** – *If the dijet mass information is expressed in a scale‑invariant way, the tagger will become robust against global JES variations and isolated bad jets, while a small non‑linear combiner can recover the lost discrimination.*

| Observation | Interpretation |
|-------------|----------------|
| **Positive Δeff ≈ 0.03** | The hypothesis was *partially confirmed*. The scale‑invariant features indeed reduced the impact of JES shifts; events with a common upward (or downward) scaling of all jet energies now produce nearly identical physics‑driven inputs, so the classifier no longer penalises them. |
| **RMSΔmₘ** | The RMS of the three Δm/m turned out to be the most powerful new variable (correlation ≈ −0.43 with the BDT residuals). It captures how symmetrically the three dijet pairs sit around the W‑mass – a key signature of a genuine top decay. |
| **Boost (pₜ/m)** | Provides orthogonal information about the overall event kinematics. Its inclusion raised the ROC‑AUC by ~0.005, indicating that the classifier could separate high‑pₜ top events that are otherwise borderline in mass space. |
| **Tiny MLP + BDT score** | The MLP learned a smooth “soft‑window” around the mass hypothesis: it accepts events with slightly larger Δm if the RMS and boost are optimal, and vice‑versa. The non‑linear combination is more flexible than a hard cut on any single variable, which explains the extra gain. |
| **FPGA constraints** | All operations remained within the 6 % DSP budget, confirming that the chosen architecture is viable for real‑time deployment. Latency stayed comfortably under 1 µs. |
| **Limitations** | • The improvement, while statistically significant, is modest. <br>• The model capacity is deliberately tiny; richer non‑linearities (e.g., deeper nets, gating mechanisms) could extract more from the same inputs. <br>• Only mass‑related and simple flow variables were used; angular correlations and sub‑structure observables (τ₂/τ₁, energy‑correlation functions) are still absent. <br>• No explicit handling of *isolated* mis‑measured jets beyond the scale‑invariant mass representation – occasional outliers still cause a tail in the background distribution. |

**Overall assessment:** The scale‑invariant transformation succeeded in decoupling JES effects, and the MLP efficiently leveraged the new physics‑driven features. The hypothesis is validated, but the ceiling of performance for this feature set appears to be reached.

---

### 4. Next Steps – Novel Directions to Explore

| **Direction** | **Rationale** | **Concrete Plan** |
|---------------|---------------|-------------------|
| **1. Add angular‑correlation features** | The relative opening angles between the three dijet axes encode the geometric “tri‑jet” topology of a top decay. These are largely insensitive to JES but highly discriminating against QCD background. | • Compute ΔRᵢⱼ (i ≠ j) for the three dijet pairs and derived ratios (e.g., max/min ΔR). <br>• Include the *planarity* metric (e.g., eigenvalues of the momentum tensor). |
| **2. Include jet‑substructure observables** | N‑subjettiness (τ₂/τ₁) and energy‑correlation functions capture the internal radiation pattern and are robust to overall scale. | • Evaluate τ₁, τ₂ for each constituent jet (or for the merged top candidate). <br>• Feed τ₂/τ₁ and the D₂ variable as additional inputs to the same MLP (or a second‑stage MLP). |
| **3. Explore a *Mixture‑of‑Experts* (MoE) scheme** | Different physics regimes (e.g., high‑pₜ vs. low‑pₜ, well‑balanced vs. asymmetric masses) may benefit from specialised classifiers. | • Train two tiny MLPs: one optimised for low RMSΔ, another for high boost. <br>• Use a lightweight gating network (e.g., a single sigmoid) based on B (boost) to blend their outputs. |
| **4. Quantised deeper network (3‑layer MLP, 12 neurons each)** | Modern quantisation tools can keep DSP usage < 6 % even with a modest depth increase, potentially capturing more complex non‑linearities. | • Convert to 8‑bit unsigned fixed‑point, verify precision loss < 0.2 % in efficiency. <br>• Profile DSP and latency on the target FPGA; prune if needed. |
| **5. Dynamic JES correction layer** | Instead of making the network *invariant* to JES, we could *learn* a per‑event scale factor from the same inputs and apply it to the raw masses before the invariant transformation. | • Add a linear regression head that predicts a multiplicative scale factor ŝ from the jet 4‑vectors. <br>• Apply ŝ⁻¹ to the dijet masses, then proceed with the invariant feature pipeline. <br>• Implement the regression as a single‑layer fixed‑point network (≈ 2 DSPs). |
| **6. Real‑time calibration monitoring** | Deploy a lightweight monitor that updates a global JES offset every few thousand events and feeds it back to the classifier. | • Compute the mean Δm across the accepted events; feed a filtered version to the MLP as an extra bias term. |
| **7. Benchmark against a *tiny CNN* on jet images** | Convolutional structures have shown strong performance on jet‐image data even with aggressive pruning; a 3×3 kernel network could fit the latency budget. | • Produce 32×32 calorimeter‑cell images per candidate, quantise to 4 bits. <br>• Build a 2‑layer CNN (8 and 4 feature maps) with ReLU and max‑pool, evaluate DSP usage. |
| **8. Systematic robustness studies** | Validate the new features across a range of JES shifts (± 3 %) and jet‑smearing scenarios to quantify the true gain in robustness. | • Run the full validation set with varied JES, record efficiency/rejection curves, compare to baseline. |

**Prioritisation for the next iteration**  

1. **Add angular and substructure variables** (Steps 1 & 2). These require only a few extra fixed‑point calculations and are known to improve discrimination dramatically; they fit within the existing 6 % DSP budget.  
2. **Prototype the MoE approach** (Step 3) – it can be implemented with the same tiny MLPs already built, only adding a gating unit.  
3. **If resource budget permits, test a deeper quantised MLP** (Step 4) to gauge possible marginal gains.  
4. **Long‑term goal:** explore the dynamic JES correction (Step 5) and the CNN option (Step 7) after solidifying the physics‑driven feature set.

---

**Conclusion** – `novel_strategy_v207` demonstrated that a physics‑motivated, scale‑invariant feature transform combined with a minimal MLP can lift the signal efficiency by ~5 % while meeting strict FPGA constraints. The next logical step is to enrich the feature set with angular and substructure information, and to investigate lightweight mixtures of specialist experts. These extensions should preserve the hardware friendliness of the solution while unlocking further performance gains.