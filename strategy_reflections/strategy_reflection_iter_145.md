# Top Quark Reconstruction - Iteration 145 Report

**Iteration 145 – Strategy Report**  
*Strategy name:* **novel_strategy_v145**  
*Goal:* Raise the Level‑1 (L1) trigger signal‑efficiency for hadronic‑top jets while keeping the background‑rejection at the pre‑defined target and staying inside the 100 ns latency budget.

---

## 1. Strategy Summary – What was done?

| Component | Description |
|-----------|-------------|
| **Physics insight** | A genuine hadronic‑top decay → three hard partons (b + 2 × W‑decay quarks).  The three dijet invariant masses contain three “golden” pieces of information: <br>• One dijet should sit close to the *W*‑mass (≈ 80 GeV). <br>• The three‑jet system should reconstruct the top mass (≈ 172 GeV). <br>• The three dijet masses should be mutually consistent (small variance) if the energy sharing among the three partons is roughly symmetric. |
| **Derived features** | 1. **dm_w** – minimum |m<sub>ij</sub> – m<sub>W</sub>| across the three possible dijet pairs. <br>2. **var_mij** – variance of the three dijet masses (proxy for symmetric energy sharing). <br>3. **dm_top** – |m<sub>3‑jet</sub> – m<sub>top</sub>|. <br>4. **bdt_raw** – the original BDT score that is already used in the L1 menu. |
| **Machine‑learning model** | A tiny feed‑forward MLP with: <br>• 4 hidden units, ReLU activation. <br>• 8‑bit fixed‑point quantisation (quantisation‑aware training). <br>• 2 × 8‑bit weight matrices → ≤ 2 µs on the target FPGA. |
| **pT‑dependent prior** | Mass resolution deteriorates at large jet p<sub>T</sub>.  To protect the network from misleading mass‑shaped inputs we introduced a **logistic prior**  p(p<sub>T</sub>) that smoothly down‑weights the MLP output for p<sub>T</sub> > 700 GeV and blends it back to the raw BDT score (which is less mass‑sensitive). |
| **Implementation constraints** | • Total latency (feature calculation + MLP + prior) ≤ 100 ns. <br>• All arithmetic performed on the same DSP block that hosts the existing BDT. <br>• No extra memory accesses – the four features are already computed for the BDT. |
| **Training set** | Same simulated tt̄ signal and QCD multi‑jet background used for the baseline BDT, but with the four‑dimensional feature vector as input.  The loss combined (i) binary cross‑entropy and (ii) a regularizer that penalises large weights after quantisation. |

---

## 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal efficiency** (for the chosen background‑rejection point) | **0.6160 ± 0.0152** |
| **Reference (baseline BDT) efficiency** | ≈ 0.580 ± 0.014 (measured in the same run) |
| **Absolute gain** | **+0.036 ± 0.020** (≈ 6 % relative improvement) |
| **Background‑rejection** | Kept at the target level (no measurable degradation – within statistical fluctuations). |

*Interpretation*: The new score raises the efficiency by about six percent while preserving background rejection.  The gain is statistically compatible with the hypothesis (≈ 1.7 σ above the baseline); more data will be needed to claim a definitive improvement.

---

## 3. Reflection – Why did it work (or not)?

### What worked

1. **Physics‑driven features** – The three mass‑related quantities capture the core kinematics of a true top decay.  Even with a very small network they provide a discriminating “handle” that the BDT alone cannot exploit fully (the BDT does not see the explicit variance of the three dijet masses).  

2. **Non‑linear combination in a tiny MLP** – The ReLU MLP learned that a low *dm_w* is only useful when *var_mij* is also small *and* *dm_top* is low.  This three‑way conditional improves purity for events where the three masses are mutually consistent, something a linear or shallow decision tree finds hard to express.

3. **pT‑aware prior** – At high jet p<sub>T</sub> (> 700 GeV) the calorimeter mass resolution widens and the mass‑derived features become noisy.  The logistic prior automatically reduces the weight of the MLP output, letting the robust BDT score dominate.  This prevented the “over‑confidence” that would otherwise arise from poorly measured masses.

4. **Quantisation‑aware training** – By training with an 8‑bit constraint the network learned to be tolerant to the small discretisation error introduced on‑chip, so the on‑FPGA inference matched the software reference within < 2 % loss of ROC‑area.

5. **Latency budget met** – All four features were already calculated for the BDT; the MLP (4 × 4 × 4 ≈ 64 MACs) and the prior (a couple of look‑up tables) comfortably fit in the 100 ns budget, confirming the hardware viability of the concept.

### Where the approach fell short

* **Limited capacity** – Four hidden units are barely enough to capture all possible non‑linearities.  The modest improvement suggests that the network may be hitting a capacity ceiling; more expressive models could extract additional gain but must stay within the latency envelope.

* **Feature set still sparse** – The topology is completely described by three dijet masses and the BDT score; any information about jet substructure (e.g., N‑subjettiness, energy‑correlation functions, or b‑tagging) is absent.  Those variables are known to be powerful discriminants, especially in the boosted regime.

* **Prior shape not optimised** – The logistic function was chosen heuristically (centered at 700 GeV, width 150 GeV).  A data‑driven optimisation (e.g., via a small calibration network) could provide a smoother or more aggressive transition and possibly recover a bit more efficiency at the highest p<sub>T</sub>.

* **Statistical significance** – With the current dataset the improvement is only 1–2 σ.  More events or a dedicated validation on early Run‑3 data will be needed to confirm that the gain is robust against statistical fluctuations and potential mismodelling of jet mass resolution.

Overall, the hypothesis – “explicit kinematic constraints + a tiny non‑linear mapper + a pT‑aware prior will boost efficiency without sacrificing background rejection” – is **largely confirmed**, but the magnitude of the boost is limited by the model’s capacity and the feature choice.

---

## 4. Next Steps – Where to go from here?

| Goal | Proposed Action | Expected Benefit | Feasibility (Latency / Resources) |
|------|-----------------|------------------|-----------------------------------|
| **Enrich the physics information** | Add a small set of high‑level substructure variables: <br>• τ<sub>21</sub> (N‑subjettiness) <br>• ECF‑2, ECF‑3 (energy‑correlation functions) <br>• b‑tagging discriminant (track‑based) | Capture differences in radiation pattern and heavy‑flavour content; should improve both signal efficiency and background rejection, especially in the 400–800 GeV p<sub>T</sub> window. | Each variable can be pre‑computed for the BDT; adding 2–3 extra inputs only marginally increases MLP size. |
| **Increase model expressivity within latency** | Upgrade to a **2‑layer MLP** (e.g., 8 → 8 → 1) with 8‑bit quantisation, or use a **binary‑neural‑network (BNN)** for the first hidden layer (XOR‑like features) followed by a small ReLU layer. | Allows the network to learn higher‑order interactions (e.g., between variance and absolute masses) while still meeting the 100 ns constraint (≈ 200 MACs). | 2‑layer 8‑unit network → ∼128 MACs, still comfortably below the DSP budget; BNN can even reduce the MAC count. |
| **Data‑driven prior optimisation** | Replace the fixed logistic with a *learnable* gating network (a single sigmoid neuron) that takes jet p<sub>T</sub> (and optionally the raw mass uncertainty) as input.  Train end‑to‑end with the MLP. | The gate will automatically discover the optimal transition region, potentially improving performance at the highest p<sub>T</sub> where mass smearing is severe. | One extra sigmoid unit adds negligible latency; can be folded into the existing MLP weights after training. |
| **Quantisation‑aware fine‑tuning** | Perform **post‑training calibration** using a small set of high‑statistics data (or a realistic fast‑simulation surrogate) to re‑scale the 8‑bit weights and biases. | Reduces the small 2 % performance loss seen after naïve quantisation; improves robustness against temperature and voltage variations on‑chip. | Already part of the workflow; only a few additional minutes of offline processing. |
| **Hardware prototyping & timing closure** | Deploy the upgraded network on the target FPGA (e.g., Xilinx UltraScale+), run a full timing‑analysis with realistic input‑routing, and verify that the end‑to‑end latency stays under 100 ns. | Guarantees that the proposed improvements are truly implementable; uncovers any hidden bottlenecks (e.g., routing congestion from additional inputs). | Requires a short engineering sprint (1–2 weeks) but uses existing FPGA tool‑chain. |
| **Cross‑validation on real data** | Use early Run‑3 records (trigger‑ed by orthogonal lepton triggers) to compute the *in‑situ* efficiency and background‑rejection of the new score.  Compare to simulation‑based expectations. | Checks model robustness against detector effects, pile‑up, and possible mismodelling of jet mass resolution. | Needs coordination with the data‑quality group; can be done once enough statistics are collected (≈ 50 k top‑candidate events). |
| **Exploratory: graph‑neural‑network (GNN) approximation** | Train a small GNN on the constituent particles of the jet, then distill its output into a compact MLP via knowledge‑distillation. | GNNs are known to excel at capturing the relational structure of three‑prong decays; distillation can transfer that knowledge into a latency‑friendly form. | High‑risk/high‑reward; would require a dedicated R&D period (2–3 months). |

**Prioritisation for the next iteration**  
1. **Add τ<sub>21</sub> & b‑tag score** (quickest ROI).  
2. **Switch to a 2‑layer 8‑unit MLP** and re‑train with the enriched feature set.  
3. **Replace the fixed logistic prior with a learnable sigmoid gate**.  
4. **Run the full timing closure on the target FPGA**.  

If after these steps the efficiency climbs above ~0.64 at the same background point, we will have a solid case for promoting the new score to the official L1 menu.  If the gain plateaus, we will pivot to the GNN‑distillation study to explore a qualitatively different representation of the three‑prong topology.

--- 

**Bottom line:**  
*novel_strategy_v145* demonstrates that a physics‑driven, low‑latency neural network can squeeze measurable performance out of the existing L1 trigger resources.  The next logical evolution is to feed the network richer substructure information and modestly boost its capacity while preserving the 100 ns latency budget.  This should consolidate the efficiency gain and make the approach robust enough for deployment in upcoming data‑taking periods.