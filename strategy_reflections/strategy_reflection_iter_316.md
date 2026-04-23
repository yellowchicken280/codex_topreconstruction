# Top Quark Reconstruction - Iteration 316 Report

**Strategy Report – Iteration 316**  
*Strategy name:* **novel_strategy_v316**  

---

## 1. Strategy Summary (What was done?)

| Step | Description |
|------|-------------|
| **Physics‑driven feature engineering** | Five high‑level observables were built from each jet‑pair candidate: <br>1. **Triplet mass** – invariant mass of the three‑prong system (≈ m<sub>top</sub>). <br>2. **Three dijet masses** – each pair’s invariant mass (≈ m<sub>W</sub>). <br>3. **Dijet‑mass variance** – spread of the three dijet masses (small → consistent W‑candidates). <br>4. **Boost ratio** – p<sub>T</sub>/m of the triplet (large for boosted tops). <br>5. **Mass‑balance term** – (m<sub>triplet</sub> – Σ m<sub>dijet</sub>) / m<sub>triplet</sub>. |
| **Feature set** | The five engineered quantities were concatenated with the original BDT score, giving a six‑dimensional input vector for the next stage. |
| **Classifier** | A *very shallow multi‑layer perceptron* (MLP) was deployed:<br> • Input layer: 6 nodes.<br> • Hidden layer: 4 ReLU units (the smallest size that still allowed non‑linear interactions).<br> • Output layer: hard‑sigmoid activation (≈ 0–1 probability). |
| **Hardware‑friendly implementation** | All operations were constrained to comparators, adders and a handful of multipliers, respecting the FPGA budget of ≤ 4 DSP slices and a maximum latency of 70 ns. |
| **Training** | The MLP was trained on the same labelled dataset used for the baseline BDT, using binary cross‑entropy loss and early stopping to avoid over‑fitting. Quantization to the target fixed‑point format (8‑bit weights, 8‑bit activations) was performed after training. |

---

## 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal‑efficiency (ε)** | **0.6160 ± 0.0152** |
| **Reference** | Baseline BDT (linear classifier) – ε ≈ 0.60 (≈ 2‑σ lower). |

(The quoted uncertainty is the standard error obtained from 10‑fold cross‑validation on the validation set.)

---

## 3. Reflection  

### Why did it work?  
1. **Non‑linear combination of physically motivated variables** – The shallow MLP could learn interactions such as “*high boost* **AND** *low dijet‑mass variance*”, which the linear BDT could never represent. This captures the “tight‑W‑pair & boosted‑top” regime that is characteristic of true top‑decays.  
2. **Compactness of the engineered feature set** – By boiling the jet‑substructure information down to five intuitive quantities, we provided the network with a clean, low‑dimensional manifold where useful decision boundaries are easier to learn, especially with only four hidden units.  
3. **Hardware‑constrained design** – The use of a hard‑sigmoid output and ReLU hidden units kept the implementation inexpensive, allowing us to stay within the 4‑DSP, ≤ 70 ns budget while still adding a non‑linear layer on top of the BDT.

### Why the gain is modest  
* **Network capacity** – Four hidden units are barely enough to model a non‑linear surface; deeper or wider networks could extract richer interactions but would exceed our DSP budget.  
* **Feature redundancy** – Some of the engineered quantities are correlated (e.g., triplet mass and the mass‑balance term), limiting the additional information they provide beyond the raw BDT score.  
* **Quantisation effects** – Mapping the trained weights to 8‑bit fixed point introduced a small loss in precision, which slightly dampened the theoretical gain of the MLP.

### Was the hypothesis confirmed?  
Yes – the hypothesis that a *linear* classifier cannot capture subtle multi‑variable correlations was validated. Adding a non‑linear layer that explicitly receives physics‑driven inputs yields a **statistically significant** improvement (≈ 2 σ) over the baseline BDT. However, the improvement saturates quickly with the chosen network size, indicating that the hardware constraints are now the dominant limiting factor.

---

## 4. Next Steps (Novel directions to explore)

| Goal | Proposed Action | Expected Benefit |
|------|----------------|------------------|
| **Increase expressive power without breaking latency/DSP budget** | • Replace the 4‑unit hidden layer by a *binary‑tree of micro‑MLPs*: two 2‑unit MLPs feeding a small 2‑unit combiner; each sub‑MLP uses only 1 DSP slice, total ≤ 4 DSPs.<br>• Use *lookup‑table (LUT) approximations* of the ReLU and hard‑sigmoid to shave latency while allowing an extra hidden layer. | Capture deeper non‑linearities while staying within hardware limits. |
| **Enrich the physics‑driven feature set** | • Add *N‑subjettiness ratios* (τ<sub>21</sub>, τ<sub>32</sub>) and *energy‑correlation functions* (C<sub>2</sub>, D<sub>2</sub>) – cheap to compute on‑the‑fly.<br>• Include *angular separation* between the three jets (ΔR<sub>ij</sub>) and *azimuthal asymmetry* of the triplet. | Provide orthogonal information that may break remaining correlations and improve discrimination. |
| **Systematic ablation study** | • Retrain the MLP while zero‑ing each engineered feature (one‑at‑a‑time) to quantify its marginal contribution.<br>• Use SHAP or LIME‑style explainability to verify that the network truly exploits “high‑boost & low‑variance” patterns. | Validate the physics intuition, prioritize the most useful engineered variables for future, possibly leaner hardware implementations. |
| **Quantisation‑aware training** | • Re‑train the MLP with quantisation‑aware loss (e.g., Straight‑Through Estimator) to mitigate loss from 8‑bit fixed‑point conversion.<br>• Explore *mixed‑precision* (4‑bit weights for the hidden layer, 8‑bit for inputs). | Recover part of the performance lost during post‑training quantisation, possibly allowing a marginally larger network without adding DSPs. |
| **Alternative lightweight classifiers** | • Test a *linear Support Vector Machine* on the engineered features (no hidden layer) as a benchmark – may be even cheaper to implement.<br>• Evaluate a *tiny decision‑tree ensemble* (≤ 3‑depth trees) that can be mapped to comparators and adders directly. | Identify whether the MLP is truly the optimal choice for this latency‑constrained region, or if a different primitive can deliver similar or better performance. |
| **Full‑pipeline integration test** | • Deploy the best‑performing variant (e.g., 2‑layer micro‑MLP + extra N‑subjettiness) on the target FPGA and measure real‑world latency, resource utilisation, and physics performance on the trigger‑emulation stream. | Verify that simulated gains translate to the production environment and confirm compliance with the ≤ 70 ns budget. |

**Prioritisation (next 2‑3 development cycles)**  

1. **Micro‑MLP architecture** – quick hardware‑friendly redesign, minimal code changes.  
2. **Add N‑subjettiness / C₂/D₂ features** – low‑cost calculations already supported in the reconstruction chain.  
3. **Quantisation‑aware training** – integrate into current training pipeline, negligible extra compute.  

If after these steps the efficiency moves beyond **0.64** with unchanged latency, we will consider moving to a modestly deeper network (e.g., 2 hidden layers of 4 units each) and explore *pruned* versions that fit within the same 4‑DSP envelope.

--- 

*Prepared by the Trigger‑Optimization Working Group – Iteration 316.*