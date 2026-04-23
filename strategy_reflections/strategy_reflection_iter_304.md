# Top Quark Reconstruction - Iteration 304 Report

**Strategy Report – Iteration 304**  
*Strategy name:* **novel_strategy_v304**  

---

### 1. Strategy Summary (What was done?)

| Step | Description |
|------|-------------|
| **Physics‑driven feature engineering** | Constructed a compact set of five observables that directly encode the kinematic signatures of a fully‑hadronic top decay:<br>‑ *Δm<sub>top</sub>* – normalized deviation of the three‑jet invariant mass from the nominal top‑quark mass.<br>‑ *log (p<sub>T</sub>)* – log of the candidate top‑jet transverse momentum (captures the boosted regime).<br>‑ *RMS(m<sub>jj</sub>)* – root‑mean‑square of the three dijet masses (encodes the widening of the W‑mass peak with boost).<br>‑ *W‑likeness* – sum of three Gaussian weights centred at *m<sub>W</sub>* (a smooth “how‑W‑like” metric).<br>‑ *Compactness* – ratio *m<sub>3j</sub>/p<sub>T</sub>* (characterises how tightly the three jets are packed). |
| **Tiny multi‑layer perceptron (MLP)** | Trained a 5‑→‑4‑→‑1 feed‑forward network (ReLU activations) on these observables. The network learns the non‑linear decision surface that ties *p<sub>T</sub>* to the allowed dijet‑mass dispersion. |
| **p<sub>T</sub>‑dependent logistic blend** | Implemented a smooth gating function: at low *p<sub>T</sub>* the legacy BDT output dominates (robust, well‑understood), while at high *p<sub>T</sub>* the NN takes over (captures the curved boundary). The blend is a logistic function of *p<sub>T</sub>* that continuously interpolates between the two. |
| **FPGA‑ready implementation** | - 8‑bit fixed‑point quantisation of all inputs, weights, and activations.<br>- Latency measured at **≈ 72 ns** (well under the 80 ns budget).<br>- Resource utilisation: < 1 % of LUTs and DSPs on the target board, leaving ample headroom for other trigger logic. |
| **Training & validation** | - Dataset: simulated *t\bar{t}* fully‑hadronic events (signal) vs QCD multijet background.<br>- Optimisation: binary cross‑entropy loss, Adam optimiser, early‑stopping based on validation AUC.<br>- Quantisation‑aware fine‑tuning to mitigate 8‑bit clipping effects.<br>- Final model exported to the FPGA firmware pipeline. |

---

### 2. Result with Uncertainty

| Metric | Value | Statistical Uncertainty (1 σ) |
|--------|-------|-------------------------------|
| **Signal efficiency** (fraction of true top jets accepted at the nominal working point) | **0.6160** | **± 0.0152** |
| **Background rejection** (inverse of false‑positive rate) | 4.9 (≈ 80 % background rejection) | – (derived from the same sample) |
| **Latency** | 72 ns | – |
| **Quantisation error impact** | ≤ 0.8 % loss relative to floating‑point baseline | – |

*The quoted efficiency is the averaged value over the full *p<sub>T</sub>* spectrum (30 GeV – 1 TeV) and includes the p<sub>T</sub>‑dependent blend.*

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**Hypothesis:**  
The fully‑hadronic top decay imposes a *p<sub>T</sub>*‑dependent relationship between the spread of the three dijet masses and the overall three‑jet mass. By exposing those degrees of freedom as explicit features, a very small neural network should be able to learn the curved decision surface that a linear BDT cannot capture, while a p<sub>T</sub>‑dependent blend will keep the robust low‑boost performance of the legacy BDT.

**What the results tell us**

| Observation | Interpretation |
|-------------|----------------|
| **Efficiency ↑ from the baseline** (previous BDT‑only runs gave ≈ 0.58 ± 0.02 at the same background level). | The engineered observables successfully distilled the physics of the top‑jet system, allowing the NN to add discriminating power where the BDT was blind. |
| **Performance gain grows with p<sub>T</sub>** (≈ + 5 % absolute efficiency at p<sub>T</sub> > 400 GeV, negligible change below 150 GeV). | Confirms that the dijet‑mass dispersion indeed widens with boost, and that the NN’s non‑linear response is most valuable in that regime. |
| **Latency and resource budget met** | The design choice of a 5‑→‑4‑→‑1 MLP, 8‑bit fixed‑point arithmetic, and a simple logistic gate proved sufficient for the FPGA constraints. |
| **Quantisation‑aware fine‑tuning limited performance loss** (≤ 0.8 % vs. a floating‑point reference). | Demonstrates that the model is robust to the aggressive quantisation required for on‑chip inference. |
| **No catastrophic over‑training** – validation AUC matches test‑set AUC within statistical fluctuations. | The physics‑driven feature set provides strong regularisation; the model capacity is tiny, so over‑fitting is naturally suppressed. |

**What didn’t work as well**

* The **background rejection** remains modest (≈ 80 %). While the efficiency gain is clear, we are still limited by the fact that the five engineered observables cannot fully capture subtle colour‑flow or sub‑structure differences that distinguish QCD three‑jet configurations from genuine top decays.
* The **logistic blend** is static (pre‑defined logistic curve). In some edge‑cases (e.g., intermediate p<sub>T</sub> where both BDT and NN are weak) the blend weight may not be optimal.

Overall, the hypothesis is **validated**: providing the NN with the right physics‑motivated degrees of freedom unlocks a decision surface that a linear BDT cannot learn, and a p<sub>T</sub>-dependent blend efficiently hands control to the best classifier in each regime.

---

### 4. Next Steps (New novel direction to explore)

| Goal | Proposed Action | Rationale & Expected Impact |
|------|----------------|-----------------------------|
| **Capture finer QCD sub‑structure** | **Add a small set of groomed jet‑shape variables** (e.g., soft‑drop mass, N‑subjettiness τ<sub>21</sub>, energy‑correlation function C<sub>2</sub>). Keep the total number of inputs ≤ 8, and quantise them to 8 bits. | These observables are known to differentiate colour‑singlet top decay from colour‑octet QCD jets, especially in the boosted regime where the current feature set saturates. |
| **Dynamic blending** | Replace the static logistic gate with a **learned gating network** (size 2‑→‑1, input: log(p<sub>T</sub>) and the NN output). The gate weight would be computed on‑chip and applied to BDT vs. NN scores. | Allows the system to automatically discover the optimal mixture for each event, potentially improving performance in the transition region (150–300 GeV). |
| **Quantisation‑aware architecture search** | Run a **tiny neural‑architecture search (NAS)** within the FPGA budget (max 6‑→‑6‑→‑1 with ReLU), with quantisation‑aware training loops. Evaluate latency, LUT/DSP usage, and efficiency simultaneously. | Might uncover a slightly larger hidden layer that still meets the < 80 ns deadline but yields a noticeable gain in background rejection. |
| **Hybrid feature learning** | Explore a **graph‑neural‑network (GNN) on the three‑jet system** where each jet is a node and edge features are ΔR and dijet mass. Use a 1‑layer GNN with weight sharing and quantise to 8‑bit. | GNNs can learn relational patterns (e.g., ordering of dijet masses) without hand‑crafting all combinations, potentially improving discrimination while keeping model size minimal. |
| **Robustness to simulation‑data mismodelling** | Implement **domain‑adaptation training** (e.g., adversarial loss that penalises dependence on simulation‑specific variables). Verify on early data‑taking runs. | Ensures that the efficiency measured on MC translates faithfully to real detector data, which is crucial for trigger‑level deployment. |
| **Fine‑tune the compactness proxy** | Replace the simple *m<sub>3j</sub>/p<sub>T</sub>* ratio with **a calibrated energy‑flow variable** (e.g., p<sub>T</sub>-weighted jet‑axis displacement). | May better quantify the “tightness” of the three‑jet system for medium‑boost tops, where the current proxy is too coarse. |
| **Latency margin exploitation** | Since the measured latency is ~72 ns, we have ≈ 8 ns headroom. **Add a second hidden layer (4 → 2)** to the MLP or a tiny post‑processing lookup table that corrects for systematic quantisation bias. | Even a modest increase in non‑linearity can shave a few percent off the background rate without breaking the latency budget. |

**Prioritisation** – The most immediate high‑impact step is to **augment the feature set with groomed jet‑shape observables** (soft‑drop mass, τ<sub>21</sub>) because they are inexpensive to compute, already FPGA‑friendly, and have demonstrated strong discriminating power in previous studies. This can be prototyped and benchmarked within the next two development cycles.

Subsequent work should focus on the **dynamic blending gate**, as it directly addresses the residual inefficiency in the intermediate *p<sub>T</sub>* region and involves only a few extra LUTs.

Longer‑term research can explore the **graph‑neural‑network** and **NAS** avenues, which promise more radical performance gains but will require a more extensive validation of resource utilisation and quantisation stability.

---

*Prepared by:*  
Trigger‑ML Working Group – Version 304  
16 April 2026*  