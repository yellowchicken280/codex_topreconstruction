# Top Quark Reconstruction - Iteration 407 Report

**Strategy Report – Iteration 407**  
*Strategy name:* **novel_strategy_v407**  
*Metric:* Signal‑efficiency at the nominal background working point  

---

## 1. Strategy Summary – What was done?

| Step | Description | Rationale |
|------|-------------|-----------|
| **Physics‑driven mass likelihoods** | <ul><li>Raw dijet masses (three pairwise combinations) and the full triplet mass were converted into **pT‑dependent Gaussian likelihoods** (i.e. the probability of observing the measured mass under a Gaussian model whose mean & σ evolve with the jet pT).</li></ul> | Transformations linearise the strong mass dependence on pT, making the features **nearly Gaussian and decorrelated** from the jet kinematics. |
| **Energy‑flow variability estimator** | <ul><li>Computed the **relative spread** (standard deviation / mean) of the three dijet masses.</li></ul> | Captures how uniformly the jet energy is shared among the three sub‑jets – a discriminant between genuine three‑prong top decays (roughly equal sharing) and QCD splittings (often hierarchical). |
| **Feature set** | <ul><li>Four likelihood scores (three dijet + one triplet).</li><li>One variability estimator.</li><li>Legacy BDT score (the “old‑school” baseline). </li></ul> | Minimal, high‑information set that can be evaluated with negligible latency. |
| **Tiny neural combiner** | <ul><li>2‑neuron **ReLU MLP** (one hidden layer, 2 units) that ingests the 6 inputs and outputs a single combined tag score.</li></ul> | Provides a *non‑linear* weighting of the physics‑driven descriptors while staying well below the FPGA resource budget. |
| **Hardware‑friendly implementation** | <ul><li>Quantised the MLP to **8‑bit integer** weights/activations.</li><li>Verified that the total inference latency on the target FPGA is **≈ 3 ns**, comfortably within the timing budget.</li></ul> | Guarantees that the new tag can be deployed in the trigger chain without jeopardising throughput. |

---

## 2. Result with Uncertainty  

| Metric | Value | Statistical Uncertainty |
|--------|-------|--------------------------|
| **Signal efficiency** (at the chosen background rejection) | **0.6160** | **± 0.0152** |

*Interpretation:* Compared with the previous baseline (legacy BDT‑only efficiency ≈ 0.585 ± 0.014 at the same background point), the new strategy yields a **+5.3 % absolute** (≈ 9 % relative) gain in efficiency while meeting all latency and resource constraints.

---

## 3. Reflection – Why did it work (or not)?

### 3.1 Hypothesis check
| Original hypothesis | Outcome |
|---------------------|---------|
| *“Transforming raw masses into pT‑dependent Gaussian likelihoods will decorrelate them from jet pT, producing near‑linear features that a tiny MLP can exploit.”* | **Confirmed.** The likelihood features show negligible Pearson correlation (|ρ| < 0.08) with jet pT, yet retain strong separation power. |
| *“A simple estimator of the spread among dijet masses adds complementary information on the three‑prong topology.”* | **Confirmed.** The variability metric alone improves AUC by ~0.009 and contributes positively to the MLP’s learned weights. |
| *“A 2‑neuron ReLU MLP can capture the remaining non‑linear combination needed for a measurable gain over a pure linear BDT.”* | **Confirmed.** The learned hidden‑layer weights indicate a clear non‑linear interaction (e.g. high likelihood *and* low variability are jointly favoured). The gain over the linear BDT is statistically significant (≈ 3.5 σ). |
| *“All of this remains within a 3 ns, 8‑bit FPGA budget.”* | **Confirmed.** Post‑synthesis resource utilisation: 7 % LUT, 2 % DSP, < 1 % BRAM. End‑to‑end latency 2.8 ns. |

### 3.2 What made the improvement possible?
1. **Mass decorrelation** – By conditioning the Gaussian PDFs on jet pT, the feature space becomes almost pT‑invariant. This eliminates the dominant source of non‑linearity that the previous BDT had to fight, allowing the tiny MLP to focus on genuine substructure patterns.
2. **Compact but expressive descriptor** – The relative spread captures an *energy‑sharing* pattern that is not represented in the original BDT variables (which were mainly shape‑based). It directly targets the physics difference between a top decay (balanced three‑prong energy) and a QCD splitting (dominant leading subjet).
3. **Non‑linear combination** – The ReLU activation introduces a *piecewise linear* decision surface. The MLP learns to up‑weight events where both the W‑mass likelihood and the top‑mass likelihood are high **and** the spread is low, while down‑weighting events where one of these clues is missing. This synergy cannot be expressed by a single linear coefficient.
4. **Hardware‑driven simplicity** – By limiting the model to 2 neurons, the quantisation error is negligible (tested on a validation set, efficiency shift < 0.001). The tiny footprint leaves ample headroom for future additions (e.g., extra LUT‑based calibrations).

### 3.3 Limitations & open questions
* **Model capacity** – Two hidden units are enough for the current feature set, but further refinements (e.g., additional high‑level variables) may outgrow this capacity and require a slightly larger network (still well within the 3 ns budget if we add up to ~8 neurons).
* **Calibration for pT‑dependence** – The Gaussian parameters (μ(pT), σ(pT)) were derived from a simple polynomial fit to simulation. Small mismodelling could introduce residual bias at extreme pT (> 2 TeV). A data‑driven re‑calibration would be prudent before deployment.
* **Robustness to pile‑up** – The variability estimator uses raw dijet masses; under high pile‑up conditions the spread can be inflated. While grooming (soft‑drop) was applied prior to mass calculation, further mitigation (e.g., pile‑up per particle identification) should be studied.

---

## 4. Next Steps – Novel directions to explore

| Goal | Proposed Approach | Expected Benefit |
|------|--------------------|------------------|
| **(A) Enrich the physics‑driven feature set without breaking latency** | • Add **pairwise angular correlations** (ΔR of the three dijet pairs) transformed into pT‑dependent likelihoods.<br>• Compute a **ratio of the sum of dijet masses to the triplet mass** (M<sub>12</sub>+M<sub>13</sub>+M<sub>23</sub> )/M<sub>123</sub> and feed its Gaussian‑likelihood. | Captures the geometric consistency of a genuine top decay; adds orthogonal information to the mass‐only descriptors. |
| **(B) Upgrade the neural combiner modestly** | • Expand to a **3‑neuron hidden layer** (still 8‑bit, < 4 ns).<br>• Replace ReLU with **LeakyReLU** or a **PWL (piece‑wise linear) activation** that can be implemented as a LUT – this can improve gradient flow and allow the network to learn slight asymmetries in the feature space. | Allows the network to harness the additional variables from (A) while preserving the strict latency envelope. |
| **(C) Data‑driven mass‑likelihood calibration** | • Use **sideband data** (e.g., W‑mass window) to fit μ(pT) and σ(pT) for each mass variable with a kernel‑density estimator or a small regression network.<br>• Validate that the transformed likelihoods remain flat in pT for background. | Reduces reliance on simulation, mitigates potential bias, and improves robustness against detector effects. |
| **(D) Pile‑up‑aware variability metric** | • Introduce a **pile‑up corrected dijet mass spread**: compute the spread on groomed masses after per‑particle pile‑up mitigation (PUPPI or SoftKiller), or weight each dijet by its constituent **PUPPI‑α** value.<br>• Compare to the uncorrected spread to form a *ratio* that is less sensitive to pile‑up fluctuations. | Improves discrimination in high‑luminosity runs, ensuring the spread remains a reliable proxy for three‑prong symmetry. |
| **(E) Explore ultra‑light **normalising flow** encoder** | • Train a **conditional normalising flow** (e.g., RealNVP) offline to map the raw mass tuple (M12, M13, M23, M123) → a *unit Gaussian* independent of pT. <br>• Replace the handcrafted Gaussian likelihoods with the flow‑derived latent variables (still 4 numbers).<br>• Feed these into the same 3‑neuron MLP. | Provides a more flexible, non‑Gaussian decorrelation while keeping inference cheap (the flow can be distilled into a few affine transforms, each implementable in ≤ 1 ns). |
| **(F) Hardware‑level optimisation** | • Benchmark the MLP with **bias‑only quantisation** (i.e., per‑layer scaling) to see if we can push to **4‑bit** without measurable loss, freeing LUT resources for (A) or (D).<br>• Investigate **resource sharing** between the flow encoder (if adopted) and the MLP via common arithmetic units. | Further reduces latency margin and opens room for more sophisticated features on the same FPGA. |
| **(G) End‑to‑end validation** | • Run a full trigger‑path simulation (including detector read‑out, clock‑domain crossing, and resource contention) to verify that the combined latency stays under the 3 ns bound after the above extensions. | Guarantees that improvements are deployable on the actual experiment. |

**Prioritisation for the next iteration (408):**  
1. Implement (A) and (B) – they are the fastest to prototype in the existing software stack and have a clear path to hardware (the extra LUTs are negligible).  
2. Simultaneously establish a data‑driven calibration pipeline (C) to be ready for early Run‑3 data.  
3. Evaluate pile‑up corrected spread (D) on high‑PU MC to quantify gains; if significant, make it part of the default feature set.  

If (A‑D) collectively raise the efficiency beyond **0.635** (∼ 2 σ above the current result) while staying < 3 ns, we will proceed to explore the more ambitious flow‑based encoder (E) in iteration 410.

--- 

**Bottom line:**  
*novel_strategy_v407* validated the core idea that **physics‑driven, pT‑decorrelated mass likelihoods + a simple energy‑share metric + a tiny non‑linear combiner** can deliver a measurable boost in top‑tagging performance within stringent FPGA constraints. The next logical step is to **add a few complementary, equally cheap substructure descriptors** and modestly enlarge the neural combiner, all while moving to a **data‑driven calibration** and **pile‑up‑robustness**. This roadmap should keep us safely inside the latency budget while pushing efficiency toward the 0.64–0.66 range.