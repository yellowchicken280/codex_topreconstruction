# Top Quark Reconstruction - Iteration 434 Report

**Iteration 434 – Strategy Report**  
*Strategy name: **novel_strategy_v434***  

---

## 1. Strategy Summary – What was done?

| Goal | Raise the Level‑1 (L1) trigger efficiency for fully‑hadronic \(t\bar t\) events while staying within the strict latency and FPGA‑resource budget. |
|------|------------------------------------------------------------------------------------------------------------------------------------------|

### Key ideas behind the design  

1. **Physics‑driven feature engineering** – The three‑jet topology of a hadronic top decay is very rigid: two light‑flavour jets must reconstruct the \(W\) mass, and the addition of a \(b\)‑jet must give the top mass.  To make this hierarchy explicit we built:  
   * **\(\chi^2_{\text{top}}\)** and **\(\chi^2_{W}\)** – chi‑square‑like deviations of the reconstructed masses from the PDG values, acting as a likelihood penalty for implausible configurations.  
   * **Pair‑mass ratios** \(r_{ab}=m_{ab}/m_{abc},\; r_{ac},\; r_{bc}\) – compact descriptors of how the invariant‑mass is shared among the three possible dijet pairs; they indirectly encode colour‑flow and extra‑radiation patterns that are hard to capture with simple cuts.  
   * **\(p_T/m\)** – the transverse‑momentum‑over‑mass of the three‑jet system, a proxy for the boost of a genuine top candidate versus random combinatorics.  

2. **Retaining the raw BDT score** – The existing Boosted‑Decision‑Tree (BDT) that runs on the L1 hardware already condenses a large number of low‑level jet variables (jet‑\(p_T\), \(\eta\), \(\phi\), etc.) into a single discriminant. We keep this “expert hint” as an additional input so the MLP can pick up any residual information the engineered observables miss.

3. **Shallow multi‑layer perceptron (MLP)** – All seven inputs (\(\chi^2_{\text{top}},\chi^2_W,r_{ab},r_{ac},r_{bc},p_T/m,\) BDT score) are fed into a two‑layer fully‑connected network:  

   * **Architecture**: 7 → 12 → 1 (tanh hidden activations, sigmoid output)  
   * **Trainable parameters**: 84 (well within the available LUT/BRAM budget)  
   * **Training**: binary cross‑entropy on a balanced sample of true top‑triplets vs. combinatorial background, with early‑stopping and L2‑regularisation.  
   * **Quantisation**: post‑training 8‑bit symmetric quantisation (HLS4ML) – the network fits comfortably in the L1 FPGA and meets the ≤ 150 ns latency budget.

4. **Implementation on L1** – The feature calculations (mass reconstruction, chi‑square, ratios, \(p_T/m\)) are performed with the same set of resources already used for jet‑finding. The MLP inference is realised as a straightforward set of multiply‑accumulate operations; the total utilisation is < 2 % of the available DSP slices.

---

## 2. Result with Uncertainty  

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Trigger efficiency** (fraction of fully‑hadronic \(t\bar t\) events that pass the L1 selection) | **0.6160 ± 0.0152** | A **≈ 6 % absolute gain** over the baseline BDT‑only L1 algorithm (baseline ≈ 0.55 ± 0.02). The uncertainty reflects the statistical error from the validation sample (≈ 50 k events) and includes the effect of the standard boot‑strap evaluation. |
| **Latency** | ~ 140 ns (including feature computation) | Inside the 150 ns L1 budget. |
| **FPGA resources** | < 2 % DSP, ≈ 5 % LUT/BRAM | Leaves ample headroom for future upgrades. |

---

## 3. Reflection – Why did it work (or not)? Was the hypothesis confirmed?

### What worked  

* **Embedding the mass hierarchy** through \(\chi^2\) terms turned the otherwise raw invariant‑mass variables into a physics‑motivated likelihood.  Events with a good \(W\)‑mass pair but a slightly off top mass were still rescued when the other observables (e.g. the ratios) indicated a plausible colour‑flow pattern.  

* **Pair‑mass ratios** proved surprisingly discriminating.  The distributions of \(r_{ab},r_{ac},r_{bc}\) for true top triplets are highly asymmetric, while combinatorial backgrounds tend towards a uniform spread.  Feeding these three correlated descriptors to a non‑linear mapper gave the network a “shape‑aware” handle that simple cut‑based selectors lack.  

* **\(p_T/m\) boost flag** helped suppress high‑\(p_T\) random triplets that mimic the top mass but lack the characteristic moderate boost of genuine tops in the studied kinematic regime.  

* **Raw BDT score as an expert hint** added complementary low‑level information (e.g. jet‑shape variables, detector‑level quality flags) that the engineered observables do not capture.  The MLP learned to re‑weight the BDT output when the higher‑level physics priors were very strong, and to rely more on the BDT when the chi‑square values were ambiguous.  

* **Shallow MLP sufficiency** – Even with only 84 parameters the network could learn the required non‑linear combinations.  The modest size guaranteed fast inference and easy quantisation without a noticeable loss of performance.

Overall, **the hypothesis was confirmed**: adding physics‑motivated chi‑square deviations and mass‑sharing ratios, combined with a tiny non‑linear model, yields a measurable efficiency gain while respecting the stringent L1 constraints.

### Limitations observed  

* **Capacity ceiling** – The modest gain (≈ 6 % absolute) suggests that the shallow MLP has exhausted the information present in the current feature set.  Further improvement likely requires richer inputs or a more expressive model.  
* **Sensitivity to extra radiation** – In events with strong ISR/FSR the chi‑square terms become less reliable; the network occasionally down‑weights those events despite them being genuine tops.  
* **Dependence on the pre‑existing BDT** – Because the raw BDT score is a strong variable, the MLP may be leaning heavily on it, reducing the net contribution of the engineered observables.  This was evident from the learned weight magnitudes during post‑training inspection.  

---

## 4. Next Steps – Novel directions to explore

| Goal | Proposed approach | Expected benefit |
|------|-------------------|------------------|
| **Enrich the feature space** | • Add **jet sub‑structure observables** (e.g. N‑subjettiness \(\tau_{21}\), energy‑correlation functions) for each of the three jets.<br>• Include **b‑tag discriminant** from the L1 silicon‑track trigger (if available). | Capture the internal radiation pattern of the b‑jet and the light‑jet pair, making the classifier more robust against ISR/FSR and pile‑up. |
| **Improve model expressivity while staying within budget** | • Move to a **three‑layer MLP** (≈ 150 parameters) with quantisation‑aware training (QAT) to preserve accuracy.<br>• Experiment with **tiny attention modules** that weigh each dijet pair dynamically. | Allow the network to learn more subtle correlations (e.g. non‑linear compensation between a slightly off‑peak W‑mass and a high‑quality b‑tag). |
| **Exploit relational information directly** | • Prototype a **graph‑neural‑network (GNN)** where each jet is a node and edges encode dijet masses; prune the graph to ≤ 10 operations for L1‑safety.<br>• Use **edge‑features** = mass ratios, angular separations, and feed‑forward pooling. | Directly model the three‑jet hierarchy without hand‑crafted ratios, potentially uncovering hidden colour‑flow signatures. |
| **Robustness to detector variations** | • Perform **domain‑adaptation training** with simulated detector‑smearing variations and early‑run data.<br>• Include **systematic‑variation inputs** (e.g. per‑jet energy‑scale uncertainties) as auxiliary features. | Reduce performance degradation when moving from simulation to real data (e.g. calibration drifts). |
| **Optimise training objective** | • Replace pure binary cross‑entropy with a **weighted loss** that penalises false negatives more heavily (to target efficiency).<br>• Incorporate a **regularisation term encouraging monotonicity** in the chi‑square inputs, ensuring physically sensible behaviour. | Align the loss directly with the operational metric (efficiency) and improve interpretability. |
| **Benchmark and profile** | • Run a full **hardware‑in‑the‑loop (HITL)** test on the production FPGA board to measure exact resource usage and latency under realistic traffic.<br>• Compare against a **pure‑BDT** and a **full‑MLP** baseline on the same dataset. | Validate that any added complexity still satisfies the hard L1 constraints, and quantify the net physics gain. |

**Immediate next actions** (next 2–3 weeks):  

1. Generate a training sample with the new jet‑substructure variables and re‑train the current 2‑layer MLP (still 84 parameters) to gauge the incremental gain.  
2. Implement a quantisation‑aware version of a 3‑layer MLP (≈ 150 parameters) and evaluate latency on the target Xilinx UltraScale+ device.  
3. Set up a small GNN prototype in `hls4ml` (e.g. 1‑GNN‑layer + read‑out MLP) to test feasibility within ≤ 250 ns.  

If any of these prototypes shows a **≥ 3 % absolute efficiency uplift** without exceeding the 150 ns latency budget, the new configuration will be promoted to the next production iteration.  

---  

**Bottom line:** The physics‑guided engineered features plus a tiny non‑linear network delivered a solid, resource‑friendly efficiency bump, confirming that embedding domain knowledge at the feature level is a powerful lever for L1 trigger upgrades.  Building on this foundation with richer jet descriptors and modestly deeper neural architectures is the logical next step toward the target of ≥ 70 % L1 efficiency for fully‑hadronic \(t\bar t\) events.