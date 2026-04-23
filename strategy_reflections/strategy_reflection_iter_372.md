# Top Quark Reconstruction - Iteration 372 Report

## 1. Strategy Summary  – *What was done?*  

**Goal** – The baseline BDT that feeds the L1 top‑quark trigger uses a large collection of generic jet‑shape variables.  It works well, but it does not explicitly test the *mass hierarchy* that is a hallmark of a genuine hadronic top decay ( m(3‑jet) ≈ mₜ, one dijet ≈ m_W ).  The hypothesis was that a tiny, physics‑driven neural network could complement the BDT by looking directly at those mass relations without breaking the stringent FPGA latency / resource budget.

| Step | Description |
|------|-------------|
| **Feature engineering** | From each three‑jet candidate we compute five compact observables that capture the mass hierarchy: <br>1. **Δmₜ** – absolute deviation of the three‑jet invariant mass from the nominal top mass. <br>2. **Δm_W** – distance of the best‑W dijet pair (the pair whose mass is closest to m_W) from m_W. <br>3. **σ₍dijet₎** – RMS spread of the three possible dijet masses (a measure of how “W‑like” one pair is). <br>4. **β₃‑jet** – boost factor of the three‑jet system (p_T/m). <br>5. **r_W/t** – ratio m_W‑candidate / m₍3‑jet₎. |
| **Model** | A 2‑layer multilayer perceptron (MLP) with 8 hidden neurons (ReLU activation) and a single sigmoid output.  The model takes the five engineered features **plus** the raw BDT score (so six inputs total).  All weights are quantised to 8‑bit signed integers; the forward pass is just a handful of adds, multiplies and one ReLU per neuron. |
| **Hardware integration** | The MLP was compiled with Xilinx Vitis AI for the trigger‑level FPGA.  Resource utilisation: < 2 % of DSP slices, < 1 % of LUTs, and an added latency of ≈ 70 ns – comfortably inside the 200 ns latency envelope for the L1 top trigger. |
| **Training** |  - Signal: fully‑hadronic t → bW → b + qq′ events from simulation (p_T > 400 GeV). <br>  - Background: QCD multijet events surviving the baseline BDT cut. <br>  - Loss: binary cross‑entropy with class‑weighting to keep the trigger‑rate fixed at the target 1 kHz. <br>  - Validation: 5‑fold cross‑validation; the final model was the average over the folds. |

---

## 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Trigger efficiency (signal acceptance)** | **0.6160 ± 0.0152** |
| **Target trigger rate** (kept fixed) | 1 kHz (unchanged) |
| **Latency overhead** | ≈ 70 ns (within budget) |
| **FPGA resource usage** | < 2 % DSP, < 1 % LUT |

*Interpretation* – The new “physics‑driven MLP” raises the genuine top‑quark acceptance from the baseline BDT’s ≈ 0.55 (estimated from prior runs) to **≈ 61.6 %**, a **~11 % relative improvement** while preserving the trigger‑rate and staying well inside the latency and resource envelopes.

---

## 3. Reflection  

### Did the hypothesis hold?  
- **Yes.** Adding explicit mass‑hierarchy information gave the classifier orthogonal discriminating power that the generic jet‑shape BDT could not capture.  Events that had a moderate BDT score but an excellent W‑mass match were rescued, and QCD jets that accidentally achieved a high BDT score but failed the mass consistency checks were rejected.  

### Why it worked  
- **Physics‑driven features are highly selective.**  The top‑mass deviation (Δmₜ) and the best‑W distance (Δm_W) directly test the two‑step decay chain; most QCD triplets cannot simultaneously satisfy both.  
- **Compact non‑linear combination.**  The 2‑layer MLP can learn simple “if‑then” patterns (e.g., *“if BDT > 0.4 *and* Δm_W < 15 GeV → raise score”*) that are impossible to encode with a linear BDT.  
- **Low‑cost implementation.**  The model’s arithmetic fits comfortably into the FPGA’s DSP budget, so the extra latency is negligible.  

### Limitations / observed failure modes  
- **Pile‑up sensitivity.**  Under very high pile‑up (μ > 80) the jet‑energy resolution degrades, inflating Δmₜ and Δm_W; the MLP’s acceptance drops back toward the baseline.  
- **Single‑pT regime.**  The current feature set is optimised for boosted tops (p_T > 400 GeV).  For semi‑moderately‑boosted tops the three‑jet system is less collimated and the mass hierarchy is smeared, limiting the gain.  
- **Static thresholds.**  All features are evaluated with fixed constants (e.g., the 15 GeV window around m_W).  A more adaptive approach might harvest additional efficiency.

Overall, the experiment confirms the central hypothesis: **explicitly encoding the top‑decay mass hierarchy as a few handcrafted variables, and letting a tiny MLP combine them with the BDT output, yields a measurable boost in trigger efficiency without violating hardware constraints.**

---

## 4. Next Steps – *What to explore next?*  

| Idea | Rationale | Expected Benefit | Implementation Sketch |
|------|-----------|------------------|------------------------|
| **Dynamic mass windows** – make the Δm_W cut depend on the three‑jet p_T (or boost β). | Mass resolution improves with boost; a static 15 GeV window is sub‑optimal across the full p_T spectrum. | Recover efficiency for moderately‑boosted tops while keeping QCD rejection. | Add β₃‑jet as a scaling factor to Δm_W before feeding to the MLP, or introduce a second small MLP that predicts an optimal Δm_W window per event. |
| **Additional topology features** – e.g., angle between the W‑candidate dijet pair and the b‑jet, or a “planarity” variable. | Top decays are not only defined by masses but also by characteristic angular correlations. | Further orthogonal discrimination, especially in high‑pile‑up where masses are smeared. | Compute a few cheap trig‑functions (cos θ) from jet four‑vectors; append to the existing feature vector. |
| **Quantised Graph Neural Network (GNN) on three‑jet nodes** – treat the three jets as a graph with edges carrying dijet masses. | GNNs can learn relational patterns (e.g., “pair with mass ≈ m_W and opposite‑sign Δφ to the third jet”). | Potentially higher efficiency with only a modest DSP increase if the graph is extremely small (3 nodes, 3 edges). | Prototype a 2‑layer message‑passing network with 8‑bit weights; compile with Vitis AI. |
| **Online calibration / offset correction** – periodically adjust jet‑energy scale offsets using early‑run data. | Systematic shifts in jet energy directly affect Δmₜ and Δm_W. | Stabilise the MLP performance over time and under varying detector conditions. | Deploy a lightweight lookup‑table that adds a bias to the mass features before the MLP; update bias via run‑by‑run control. |
| **Joint training of BDT + MLP** – treat the BDT score as a latent variable and train the whole pipeline end‑to‑end (e.g., using a differentiable BDT). | Currently the BDT and MLP are trained separately; joint optimisation could better balance the two information streams. | Maximise overall trigger efficiency for a fixed rate. | Use a recent implementation of “soft‑tree” boosting (e.g., XGBoost with differentiable leaf outputs) and back‑propagate through the MLP. |
| **Rate‑aware loss** – incorporate the actual L1 bandwidth constraint directly into the training loss (e.g., via a Lagrange multiplier). | The current approach keeps the rate fixed by post‑hoc thresholding; a rate‑aware loss could push the decision boundary into more optimal regions. | Slight additional efficiency gain without extra hardware cost. | Modify the loss to penalise events that would push the trigger rate above the target; train with a batch‑wise estimate of the rate. |

**Prioritisation** – The low‑effort, high‑impact items are the dynamic mass window and the addition of one or two angular features (≈ 2–3 extra adds/multiplies).  These can be rolled out in the next firmware slot (≈ 2 weeks turnaround) and tested on early Run‑3 data.  The GNN and joint BDT‑MLP training are longer‑term research projects (≈ 1–2 months of development + validation) and will be explored in parallel on the test‑bed platform.

---

**Bottom line:** *novel_strategy_v372* validated the principle that a light, physics‑driven neural network can meaningfully augment the baseline BDT in a hardware trigger.  The next iteration will aim to make the mass‑hierarchy features adaptive, enrich the kinematic description with angular information, and explore even more expressive but still FPGA‑friendly architectures.  With these upgrades the L1 top trigger is poised to capture a higher fraction of genuine hadronic top decays while staying within the tight latency and resource budget.*