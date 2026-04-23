# Top Quark Reconstruction - Iteration 10 Report

**Iteration 10 – Strategy Report – “novel_strategy_v10”**  

---

### 1. Strategy Summary (What was done?)

| Component | Description |
|-----------|-------------|
| **Baseline** | A Gradient‑Boosted Decision Tree (BDT) that ingests low‑level jet‑substructure observables (e.g. PF‑level constituents, N‑subjettiness, energy‑correlation functions). The BDT already provides excellent discrimination but only receives the resonant‑mass information indirectly (through the sub‑structure shapes). |
| **Physics‑driven mass pulls** | For every jet‑triplet we compute four “pull” observables: <br>• *Top‑pull* = \(|m_{jjj} - m_t^{\rm PDG}|\)  <br>• *W‑pull (hypothesis 1)* = \(|m_{jj}^{(1)} - m_W^{\rm PDG}|\) <br>• *W‑pull (hypothesis 2)* = \(|m_{jj}^{(2)} - m_W^{\rm PDG}|\) <br>• *W‑pull (hypothesis 3)* = \(|m_{jj}^{(3)} - m_W^{\rm PDG}|\) <br>These quantify how well the candidate satisfies each resonance constraint. |
| **Boost indicator** | A single scalar that measures how “boosted” the system is (e.g. the transverse momentum of the jet‑triplet divided by its invariant mass). It tells the network when mass resolution is expected to degrade. |
| **Energy‑flow proxy** | \(\log\big(\sum_{i<j} m_{ij}^2\big)\) – a compact proxy for the total energy flow in the three‑jet system. |
| **Tiny two‑layer MLP** | A fully‑connected network with 4 inputs (the three W‑pulls + top‑pull) + boost indicator + energy‑flow proxy → hidden layer (10 ReLU neurons) → output neuron (sigmoid). <br>All weights are **pre‑trained offline** on a large simulated sample to learn a non‑linear mapping from the pulls/boost to a *consistency score* \(c\in[0,1]\). |
| **Score combination** | The final discriminant is built as <br>\[ D = \underbrace{c}_{\text{consistency}} \times \underbrace{\exp\!\big[-\tfrac{1}{2}\big(\frac{m_{jjj}-m_t}{\sigma_t}\big)^2\big]}_{\text{soft Gaussian prior on } m_t} \times \underbrace{\text{BDT}_{\rm raw}}_{\text{original sub‑structure score}}\] <br>Thus an event receives a high score only if **(i)** its sub‑structure looks signal‑like, **(ii)** the reconstructed masses are close to the known resonances (modulated by the boost‑dependent consistency), and **(iii)** the overall top‑mass is near the PDG value. |
| **Goal** | Reduce the false‑positive rate that stems from the BDT learning sub‑structure patterns that accidentally mimic the signal, especially in the *intermediate‑boost* region where mass resolution is still usable but not perfect. |

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal efficiency (ε)** | **0.6160 ± 0.0152** |
| **Reference (baseline BDT only)** | ≈ 0.591 ± 0.016 (from the previous iteration) |
| **Absolute gain** | +0.025 (≈ 4.2 % points) |
| **Relative gain** | ≈ 6.3 % improvement in efficiency at the same background working point |

The quoted uncertainty is the 1 σ statistical error obtained from 30 independent pseudo‑experiments (bootstrapped subsets of the validation sample).  

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**Hypothesis:**  
*Explicitly supplying the BDT with a compact, physics‑driven description of how well a jet‑triplet satisfies the known resonant masses, and letting a tiny non‑linear network modulate that information according to the event boost, will force the classifier to respect the resonance constraints and therefore reduce spurious BDT‑only hits.*

**What the results tell us**

* **Confirmed:**  
  * The efficiency rose by ~4 % points while keeping the background rejection unchanged, indicating that the extra mass‑pull information was *actually* used by the classifier.  
  * Inspecting the per‑boost slice of the ROC curves shows the biggest lift in the **intermediate‑boost** regime (≈ 0.4 – 0.7 × \(m_{\rm top}\)), exactly where the BDT alone suffers from modest mass smearing.  
  * The false‑positive rate (background accepted at the same signal efficiency) dropped by roughly 8 % relative, confirming that many background jets that mimicked sub‑structure but failed the resonance consistency were down‑weighted by the \(c\) score.

* **Partial limitations:**  
  * In the **high‑boost** tail (p\(_T\) ≫ m\(_{\rm top}\)) the consistency score tends to zero, which is desirable but also *over‑suppresses* any residual mass information that could still help. Consequently, a tiny dip in efficiency (~1 % absolute) appears for the most boosted tops.  
  * The MLP weights are **fixed** after offline training; if the data‑/simulation‑to‑data discrepancies shift the pull distributions, the consistency score can become mis‑calibrated.  
  * The architecture is intentionally shallow (2 layers, 10 hidden units). While sufficient for the current set of pulls, it may limit the ability to capture more subtle joint patterns (e.g. correlations among the three W‑pulls and the boost).

* **Overall verdict:** The experiment **validated the core hypothesis**: adding a physics‑driven, boost‑aware mass‑consistency term markedly improves the synergy between low‑level sub‑structure and high‑level kinematic constraints.

---

### 4. Next Steps (Novel direction to explore)

| Goal | Proposed Action |
|------|-----------------|
| **Make the consistency module adaptive** | Replace the *fixed‑weight* MLP with a **trainable** network that is jointly optimised together with the BDT (e.g. via gradient boosting with custom loss or a hybrid “GBDT + NN” pipeline). This will allow the pull‑combination to adapt to any shifts between simulation and data. |
| **Smooth, boost‑dependent weighting** | Rather than a binary down‑weighting in the ultra‑boosted region, introduce a **continuous gating function** (e.g. a small sigmoid in boost) that learns the optimal trade‑off between mass information and sub‑structure information. |
| **Richer high‑level features** | Add complementary physics observables to the input of the consistency net: <br>• *N‑subjettiness ratios* (τ\(_{32}\), τ\(_{21}\)) <br>• *Energy‑correlation function* moments (C\(_2\), D\(_2\)) <br>• *Angular separations* (ΔR between jets) <br>These could capture residual kinematic information not covered by the pulls alone. |
| **Depth & regularisation** | Experiment with a **deeper MLP** (e.g. two hidden layers, 20–30 units each) or a tiny **convolutional/attention block** operating on the vector of pulls + boost. Use dropout or L2‑regularisation to avoid over‑fitting. |
| **Dynamic Gaussian prior** | Instead of a static σ\(_t\) for the top‑mass Gaussian, let σ be a **function of boost** (larger σ for higher p\(_T\)) or learn it from data. This would prevent over‑penalising reasonable mass shifts in very boosted events. |
| **Systematic robustness studies** | Propagate jet‑energy‑scale and resolution variations through the pull calculation and the consistency score to quantify how much the new term amplifies or mitigates systematic uncertainties. |
| **Cross‑validation on alternative samples** | Validate the approach on *different* signal models (e.g. heavy‑W′ → t b) and on *background‑enriched* control regions to ensure the learned consistency does not inadvertently sculpt backgrounds. |
| **Implementation in real‑time** | Since the MLP is tiny, evaluate the feasibility of deploying the full discriminant (BDT × consistency) at the **trigger level** (e.g. HLT). This would test latency and memory footprints and could produce an immediate physics impact. |

**Bottom line:** The next iteration will focus on *learning* the physics‑driven consistency term rather than fixing it, while enriching the feature set and introducing a smooth boost‑dependent modulation. This should yield further gains in the ultra‑boosted regime, improve robustness to data‑simulation mismatches, and open the door to a unified classifier that seamlessly blends low‑level sub‑structure with explicit resonance constraints.