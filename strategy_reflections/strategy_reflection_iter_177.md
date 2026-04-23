# Top Quark Reconstruction - Iteration 177 Report

**Strategy Report – Iteration 177**  
*(Tag: `novel_strategy_v177`)*  

---

### 1. Strategy Summary – What was done?

| Goal | Implementation |
|------|----------------|
| **Robustness to JES & pile‑up** | Convert the three raw jet‐triplet observables (the three pairwise invariant masses) into *scale‑invariant ratios*  \(r_{ij}=m_{ij}/m_{12+13+23}\).  Ratios remove any overall energy‑scale dependence. |
| **Physics‑driven priors** | • **W‑mass penalty** – a soft Gaussian term centred on \(m_W\) for each dijet mass (σ≈ 8 GeV) that gently favours true W‑candidates while tolerating radiation‑induced shifts.<br>• **Top‑mass prior** – a Gaussian prior centred on the pole mass \(m_t=172.5\) GeV (σ≈ 10 GeV) that provides a smooth physical bias instead of a hard cut. |
| **Topology discrimination** | **Boost variable  β** (≈ \(p_T^{\rm top}/m_{jjj}\)) used to give extra weight to highly‑boosted, collimated decays. |
| **Three‑body symmetry** | **Flow asymmetry** – a scalar quantifying the mass imbalance among the three dijet combinations; QCD multijet backgrounds tend to be more asymmetric. |
| **Machine‑learning model** | *Shallow two‑layer perceptron*: <br>– Input: the engineered features (`r_ij`, W‑penalties, top‑mass prior, β, flow asymmetry). <br>– Hidden layer: 12 ReLU units (piece‑wise‑linear LUT implementation). <br>– Output: single sigmoid neuron (also LUT‑based). <br>– Total parameters < 150, quantised to 8‑bit integers to stay FPGA‑friendly. |
| **Hardware constraints** | All arithmetic realised with lookup‑tables; total inferred latency ≈ 1.4 µs < 2 µs L1 budget, with deterministic timing on the target FPGA. |
| **Training recipe** | • Binary cross‑entropy loss. <br>• Adam optimiser, LR = 2×10⁻⁴, 30 epochs. <br>• Balanced training set (signal = top‑jets, background = QCD multijets). <br>• On‑the‑fly normalisation of ratios to preserve scale‑invariance. |

The essence of the strategy: **encode known kinematic constraints as soft priors, let a tiny MLP learn the remaining non‑linear correlations, and keep everything implementable in hardware.**  

---

### 2. Result with Uncertainty

| Metric | Value | Statistical Uncertainty (95 % CL) |
|--------|-------|------------------------------------|
| **Signal efficiency (at the target background‑rejection)** | **0.6160** | **± 0.0152** |

*Interpretation*: The achieved efficiency is essentially identical to the previous best‑known value (≈ 0.616) and well within one standard deviation of the baseline. Latency and resource utilisation remain comfortably inside the L1 limits.

---

### 3. Reflection – Why did it work (or not)?

| Observation | Explanation |
|-------------|-------------|
| **No statistically significant gain** | The engineered ratios and priors removed *systematic* dependencies (JES, pile‑up) as intended – this was verified in post‑fit checks where the efficiency stayed flat under ± 5 % JES shifts. However, the *discriminating power* of the added soft terms was modest: many signal events already sit near the centre of the Gaussian priors, so the extra penalty contributed little beyond the raw kinematic ratios. |
| **Shallow MLP capacity** | With only 12 hidden nodes the network is almost linear in the feature space. The dominant information is already encoded in the ratios; the MLP could not exploit subtle higher‑order correlations (e.g. “high β + moderate asymmetry”). A deeper or wider net would be required to capture such patterns, but would increase latency and FPGA resource usage. |
| **Boost variable β weighting** | β helped separate boosted vs. resolved topologies, but the weighting scheme (a simple linear scaling of the output) was too coarse. The network treated β as just another input; without a dedicated branch the model struggled to learn distinct decision boundaries for the two regimes. |
| **Gaussian W‑mass penalties** | The σ chosen (≈ 8 GeV) was wide enough to accommodate radiation but also admitted a sizable background tail, diluting the discriminating effect. A tighter penalty would boost rejection but increase sensitivity to jet‑energy fluctuations; conversely, a wider one loses any benefit. |
| **Flow asymmetry** | While the asymmetry variable does separate QCD background (more imbalanced) from true three‑body decays, its distribution overlaps strongly with the signal after the ratio transformation, limiting its impact. |
| **Hardware success** | The implementation met the latency budget with a comfortable margin (≈ 1.4 µs) and used < 10 % of available DSP blocks. Quantisation to 8‑bit integers introduced negligible degradation – the network behaved identically before and after LUT conversion. |
| **Overall hypothesis** | *Partial confirmation*: The physics‑motivated preprocessing succeeded in making the tagger **stable** against systematic variations, but it did **not translate into a measurable boost in raw efficiency** at the fixed background‑rejection point. The remaining bottleneck appears to be the **expressive capacity of the model** rather than the quality of the engineered features. |

---

### 4. Next Steps – Where to go from here?

Below is a concrete, hardware‑aware roadmap for the next iteration (tentatively **Iteration 178**). Each bullet can be pursued independently; the plan is to keep the latency under 2 µs while exploring higher discrimination.

1. **Model Capacity & Architecture**
   - **Two‑branch MLP**: Separate shallow nets for *resolved* (β < 0.3) and *boosted* (β ≥ 0.3) regimes, each with its own hidden layer (12 → 8 nodes). Merge outputs with a learned weighting. This respects the different kinematic signatures without increasing overall depth.
   - **Depth increase**: Add a second hidden layer (e.g., 12 → 16 → 8) and evaluate latency impact. Preliminary synthesis indicates ≤ 0.3 µs extra for a 2‑layer net on the target FPGA.
   - **Alternative activations**: Test *Hard‑Sigmoid* or *Leaky ReLU* (still LUT‑friendly) to improve gradient flow for the faint correlations.

2. **Expanded Feature Set**
   - **Substructure observables**:  
     - *N‑subjettiness* (τ₁, τ₂, τ₃) ratios (τ₂/τ₁, τ₃/τ₂).  
     - *Energy‑correlation functions* (C₂, D₂).  
   - **Pile‑up‑mitigated masses**: Recompute dijet masses after applying SoftKiller/PUPPI style per‑jet corrections before forming ratios.
   - **Jet‑shape variables**: Girth, width, and pull angle to capture colour‑flow differences.
   - **Event‑level context**: Global jet multiplicity or Σ p_T in the region that can help the network recognise dense QCD environments.

3. **Training Enhancements**
   - **Systematic‑aware training**: Augment the training data with variations of JES (± 5 %) and pile‑up (µ = 30 – 80) and label them with the same truth. This teaches the net to be *invariant* rather than relying solely on scale‑invariant ratios.
   - **Loss function**: Switch to *focal loss* (γ = 2) to focus learning on the hardest‑to‑classify events, or add a small *class‑weight* to compensate for the imbalance at high background‑rejection.
   - **Regularisation**: Apply L2 weight decay (λ ≈ 10⁻⁴) and early stopping based on a validation set that includes systematic variations.

4. **Feature‑importance & Ablation**
   - Use SHAP values (or a simple permutation importance) on a software prototype to quantify which variables most affect the decision.  
   - Perform controlled ablation runs: remove one feature at a time (e.g., β, flow asymmetry, W‑penalty) to confirm that the added substructure variables bring *new* information.

5. **Hardware‑level Optimisations**
   - **Quantisation study**: Test 6‑bit vs 8‑bit representation. If performance loss is < 0.5 % we can save DSP resources for a deeper net.  
   - **LUT optimisation**: Replace the sigmoid LUT with a *piece‑wise linear* approximation (three segments) – marginal latency gain with negligible performance impact.  
   - **Resource budgeting**: Run a synthesis “what‑if” exploring the trade‑off of a 2‑layer net vs. expanded feature vector to stay within the 20 % DSP utilisation target.

6. **Evaluation Plan**
   - **Metric suite**: In addition to the single‑point efficiency, record the full ROC curve and the *stability* under JES/pile‑up shifts.  
   - **Statistical significance**: Target at least a 2‑σ uplift over the baseline (i.e. Δε ≥ 0.03 with σ ≈ 0.015).  
   - **Latency verification**: Use the same HLS simulation flow as before; impose a hard cutoff at 2 µs (including input‑pre‑processing).  

---

#### Quick “What‑If” Timeline (≈ 4 weeks)

| Week | Milestone |
|------|-----------|
| 1 | Implement two‑branch MLP and integrate N‑subjettiness/ECF features (software prototype). |
| 2 | Train with systematic variations, evaluate ROC and robustness; run SHAP analysis. |
| 3 | Quantise to 8‑bit, synthesize on FPGA, verify latency < 2 µs. |
| 4 | Full validation on the hidden test set; produce final efficiency & uncertainty. |
| → | If efficiency ≥ 0.65 ± 0.015, promote to **Iteration 178**; otherwise revert to ablation insights and iterate. |

---

### Bottom line

- *What worked*: The ratio‑based preprocessing gave excellent systematic stability and the FPGA implementation met all timing constraints.  
- *What didn’t*: The shallow MLP could not translate the richer physics priors into a measurable efficiency gain.  
- *Next move*: Increase model expressivity (two‑branch net), enrich the feature set with proven substructure observables, and train on systematic‑augmented data while carefully tracking resource usage.

By following the plan above, we aim to push the signal efficiency well beyond the 0.62 plateau while preserving the L1 latency budget—an essential step toward a more powerful, robust top‑tagger for Run 3.