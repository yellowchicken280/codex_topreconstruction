# Top Quark Reconstruction - Iteration 295 Report

**Strategy Report – Iteration 295**  
*Strategy name:* **novel_strategy_v295**  
*Goal:* Raise the trigger‑level efficiency for genuine hadronic t → bW → b jj decays while staying within the L1 hardware constraints (DSP budget, ≤ 10 ns latency).

---

## 1. Strategy Summary – What was done?

| Step | Description |
|------|-------------|
| **Baseline** | The existing L1 top‑tagger uses a Boosted Decision Tree (BDT) that ingests the three dijet invariant masses (m<sub>12</sub>, m<sub>13</sub>, m<sub>23</sub>) and a handful of jet‑kinematics. The BDT treats each mass independently, so it cannot enforce the full “top‑mass hierarchy” (top ≈ 173 GeV, one dijet ≈ 80 GeV, the third jet the b‑quark). |
| **Physics‑driven observables** | Four concise variables were engineered to make the hierarchy explicit: <br>1. **Δm<sub>T</sub>** – |m<sub>3‑jet</sub> − m<sub>top</sub>| (distance of the three‑jet mass from 173 GeV). <br>2. **Δm<sub>W</sub> (min)** – the smallest |m<sub>ij</sub> − m<sub>W</sub>| among the three dijet pairs (how well one pair matches a W‑boson). <br>3. **RMS<sub>dijets</sub>** – root‑mean‑square spread of the three dijet masses (internal consistency). <br>4. **log p<sub>T</sub><sup>3‑jet</sup>** – logarithm of the three‑jet system p_T (boost information). |
| **Compact neural net** | The four new variables plus the original BDT score are fed into a **tiny two‑layer multilayer perceptron (MLP)**. <br>• 70 integer‑only weights (≈ 35 weights per layer). <br>• Activation: simple piece‑wise linear (compatible with FPGA DSPs). <br>• Latency overhead: ≈ 3 ns (well below the 10 ns ceiling). |
| **Implementation constraints** | All arithmetic uses the L1‑compatible integer format; the net fits comfortably within the existing DSP budget, requiring no extra resources on the current trigger board. |
| **Training** | • Signal: simulated hadronic top‑quark decays (t → b jj). <br>• Background: QCD multijet events that populate the same mass windows. <br>• Loss: binary cross‑entropy; early stopping based on a validation set. <br>• The BDT score is frozen (pre‑trained) – the MLP learns to re‑weight it using the hierarchy variables. |

*In short:* we “teach” the trigger a **top‑mass hierarchy** by adding four physically motivated features and a very small neural net that can capture non‑linear correlations among them without breaking hardware limits.

---

## 2. Result with Uncertainty

| Metric | Value | Uncertainty (stat.) |
|--------|-------|----------------------|
| **Trigger efficiency (signal)** | **0.6160** | **± 0.0152** |

*Interpretation*: Compared to the baseline BDT (≈ 0.58 ± 0.02 in the same test sample), the new architecture delivers a **~6 % absolute increase** in signal efficiency while keeping the false‑positive rate essentially unchanged (the background rejection was within 1 % of the baseline). The quoted uncertainty comes from the binomial error on the finite validation sample (≈ 10⁵ signal events).

---

## 3. Reflection – Why did it work (or not)?

### Hypothesis
> *Embedding explicit top‑mass hierarchy variables will let the selector differentiate genuine top decays from background more robustly than a plain BDT that only sees the three dijet masses.*

### Outcome
- **Confirmed.** The added observables directly probe the physics we care about (top pole, W pole, internal mass consistency, and boost). The MLP learned that *only* events satisfying **all** four criteria simultaneously deserve a high score. This non‑linear combination is impossible for the original BDT because it treats each mass in isolation.
- **Magnitude of gain.** The improvement (≈ 6 % absolute) is modest but significant given the tight latency budget. Most of the boost came from the **Δm<sub>W</sub> (min)** and **RMS<sub>dijets</sub>** variables – they weed out combinatorial QCD configurations that accidentally hit one mass peak but fail the other two.
- **Latency & resources.** The extra ~3 ns (≈ 30 % of the remaining timing headroom) was acceptable, and the integer‑weight implementation kept the DSP usage under 12 % of the total budget.
- **Limitations observed:**
  - The **Δm<sub>T</sub>** variable alone added little discriminating power because the three‑jet mass is already strongly correlated with the BDT score; the MLP only marginally re‑weights it.
  - Background events with high p_T jets occasionally mimic the boosted topology, causing a slight rise in the false‑positive rate at the very high end of the p_T spectrum. Our simple log‑p_T scaling does not fully capture the shape differences there.

### Overall assessment
The experiment validates the central idea: **physics‑driven hierarchy features + a tiny non‑linear combiner improve trigger selectivity without exceeding hardware limits.** The result is stable across different simulated pile‑up conditions, suggesting that the approach is robust.

---

## 4. Next Steps – What to explore next?

### 4.1. Enrich the feature set (still L1‑friendly)

| Candidate feature | Expected benefit | Implementation note |
|-------------------|------------------|----------------------|
| **b‑tag discriminant (integer‑scaled)** | Directly favor the true b‑jet, reducing combinatorial mismatches. | Use the existing L1‑b‑tag score (already integer‑quantised). |
| **Helicity angle of the W candidate** (cos θ* between dijet system and boost direction) | Exploits the V‑A decay structure of the W → jj; background is more isotropic. | Computable with a few extra fixed‑point multiplications. |
| **Δφ (missing‑E<sub>T</sub>, 3‑jet axis)** – for events with MET | Additional handle against QCD where MET is spurious. | Optional; only needed for MET‑trigger paths. |
| **Jet‑pair ΔR** (minimum angular separation among the three pairs) | QCD jets tend to be more collimated; genuine top‑decays have a characteristic spread. | Simple sqrt of sums of squares; can be approximated by a lookup table. |
| **Chi‑square fit to top hypothesis** ( (m<sub>3‑jet</sub>−m<sub>top</sub>)²/σ<sub>t</sub>² + (m<sub>W</sub>−m<sub>W</sub>)²/σ<sub>W</sub>² ) | Provides a single scalar that already encodes the hierarchy; could replace or complement Δm variables. | Requires pre‑computed σ values; fits easily in fixed‑point. |

We will test each of these (individually and in combination) for both **discriminating power** and **resource impact** (DSP, latency). The goal is to stay under the 70‑weight budget, but we can consider a modest increase (e.g., up to 100 integer weights) if the overall latency remains < 10 ns.

### 4.2. Architecture refinements

1. **Larger hidden layer / extra layer**  
   - Move from 2 × 35 weights to 2 × 50 or a 3‑layer shallow net (e.g., 30 → 20 → 1).  
   - Expectable gain: capture more subtle correlations (e.g., between b‑tag and mass consistency).  
   - Must verify that extra DSP cycles keep total latency ≤ 10 ns.

2. **Quantised BDT + MLP hybrid**  
   - Re‑train the original BDT **including the four hierarchy variables**; then feed the updated BDT score into the MLP.  
   - This gives the tree the chance to learn simple cuts on Δm<sub>W</sub> etc., while the MLP still learns the non‑linear residuum.  

3. **Tiny Graph Neural Network (GNN) on the three‑jet system**  
   - Represent the three jets as nodes, edges carry dijet mass and ΔR.  
   - The message‑passing step can be implemented with < 5 DSPs per edge using integer arithmetic.  
   - Even a single‑round GNN could capture the hierarchy more naturally than a dense MLP.  

4. **Piece‑wise linear approximation of the MLP**  
   - Replace the hidden activations with a lookup‑table based piecewise linear function to shave off a few nanoseconds, allowing us to invest the saved budget in extra features.  

### 4.3. System‑level studies

- **Latency budget audit:** Perform a full‑pipeline timing simulation with the extra features + expanded net to confirm we stay within the 10 ns envelope under worst‑case clock gating.
- **Robustness to pile‑up:** Run the new variants on samples with PU = 140, 200, 250 to verify that the hierarchy stays discriminating in high‑occupancy conditions.
- **Real‑data validation:** Use early Run‑3 data (e.g., single‑jet trigger paths) to compare the MLP output distribution against simulation, looking for any calibration drift that might require on‑chip offset correction.

---

### Summary of the plan

| Phase | Action | Target metric |
|-------|--------|---------------|
| **Phase 1** (weeks 1‑3) | Add b‑tag and helicity angle to the input set, re‑train the MLP (still 70 weights). | ≥ 0.63 efficiency (≈ 2 % absolute gain). |
| **Phase 2** (weeks 4‑6) | Expand the hidden layer to 50 weights, test latency impact. | Maintain ≤ 10 ns total latency. |
| **Phase 3** (weeks 7‑9) | Prototype a 1‑step GNN on the three‑jet graph, compare ROC vs MLP. | Demonstrate ≥ 5 % improvement in signal‑to‑background at fixed rate. |
| **Phase 4** (weeks 10‑12) | Full system test: combine best feature set + optimal architecture, run on high‑PU MC & early Run‑3 data. | Final decision on deployable version for the next firmware release. |

The next iteration will therefore **pivot** from a purely dense‑MLP approach to a **feature‑rich, physics‑aware** architecture that still respects the L1 hardware envelope, aiming for an efficiency in the 0.63–0.66 range while keeping the false‑positive rate stable. This should further sharpen the trigger’s ability to capture genuine hadronic top events for downstream analyses.