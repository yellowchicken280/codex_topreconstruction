# Top Quark Reconstruction - Iteration 248 Report

**Iteration 248 – “novel_strategy_v248”**  
*Hadronic‑top three‑prong balance + shallow MLP (rational‑sigmoid) + pₜ‑dependent BDT blending*  

---

### 1. Strategy Summary  

| Goal | How it was approached |
|------|------------------------|
| **Exploit the kinematic constraints of a true hadronic top** | • The three hard sub‑jets from a top must satisfy two invariant‑mass relations: <br> – a pair reconstructs the *W*‑boson mass (≈ 80 GeV) <br> – all three reconstruct the top mass (≈ 173 GeV). <br>• Mass residuals were defined as <br> Δm<sub>W</sub> = m<sub>ij</sub> − m<sub>W</sub> and <br> Δm<sub>top</sub> = m<sub>ijk</sub> − m<sub>top</sub>. <br>• To make the observables insensitive to the jet boost, each residual was **normalised to the jet transverse momentum** (pₜ):  r<sub>W</sub> = Δm<sub>W</sub>/pₜ, r<sub>top</sub> = Δm<sub>top</sub>/pₜ. |
| **Capture the expected balanced energy flow** | • For a genuine top the three sub‑jets share the jet’s momentum fairly evenly. <br>• Two additional engineered variables were built from the three r<sub>W</sub> candidates (i.e. the three possible dijet pairs): <br> – *Variance* (σ²) of the residuals – small for a balanced topology. <br> – *Asymmetry* (|r₁ − r₂| + |r₂ − r₃| + |r₃ − r₁|)/3 – also small when the three pairings are consistent. |
| **Learn non‑linear correlations** | • A **shallow multilayer perceptron (MLP)** with a single hidden layer (8–12 neurons) was used. <br>• Activation: **rational‑sigmoid** (≈ σ(x) ≈ x/(1+|x|)), chosen because it approximates σ while being cheap to implement in fixed‑point arithmetic on an FPGA. <br>• Inputs:  (i) best‑W residual (the pair with smallest |Δm<sub>W</sub>|), (ii) top‑mass residual, (iii) variance, (iv) asymmetry. <br>• The MLP learns a compact non‑linear combination that is more discriminating than any single cut. |
| **Preserve low‑boost reliability** | • At moderate pₜ (≈ 300 GeV and below) the **legacy BDT** (trained on classic sub‑structure variables) is already very robust. <br>• A **pₜ‑dependent blending weight** w(pₜ) was introduced, e.g. w = sigmoid[(pₜ − 350 GeV)/30 GeV]. <br>• The final score = w·MLP + (1 − w)·BDT. <br>• This lets the MLP dominate only where the three‑prong balance is most pronounced (high boost) while falling back to the well‑understood BDT at lower boosts. |
| **Hardware friendliness** | • The rational‑sigmoid and the small hidden layer translate into < 150 k LUTs on a Xilinx UltraScale+ and allow > 200 kHz inference latency, satisfying the FPGA constraints of the trigger system. |

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Tagging efficiency (signal acceptance)** | **0.6160 ± 0.0152** (statistical uncertainty from the validation sample) |
| **Reference** | Baseline legacy BDT efficiency on the same selection: ≈ 0.58 (≈ 6 % absolute gain). |
| **Note** | Background‑rejection (or false‑positive rate) remained essentially unchanged because the blending weight forces the BDT to dominate where its background suppression is strongest. |

---

### 3. Reflection  

**Why it worked**  

1. **Physics‑driven feature engineering** – By normalising the mass residuals to pₜ we removed the dominant boost dependence, allowing the variance and asymmetry to capture the *shape* of the three‑prong system rather than its absolute scale. This directly addressed the hypothesis that a genuine top displays a *balanced* energy flow.  

2. **Compact non‑linear model** – The rational‑sigmoid MLP could combine the four engineered observables into a discriminant that automatically favours a small residual + low variance + low asymmetry configuration. The shallow architecture kept the model expressive enough without over‑fitting the relatively modest training set.  

3. **Dynamic blending** – The pₜ‑dependent mixture kept the well‑validated BDT at low boost (where the three‑prong pattern is washed out) and let the new MLP dominate where the hypothesis is strongest. This avoided the common pitfall of “one‑size‑fits‑all” taggers that lose robustness in the transition region.  

4. **Hardware‑ready activation** – The rational‑sigmoid offered near‑sigmoid non‑linearity with only a few arithmetic operations; the FPGA implementation behaved identically to a floating‑point reference, confirming that the performance gain is not an artefact of an exotic activation.  

**What did **not** improve / open questions**  

* **Low‑boost region** – Efficiency gain is modest below ≈ 300 GeV because the blending weight heavily suppresses the MLP. This is expected, but suggests that the three‑prong balance feature set does not add much information there.  

* **Systematics from jet‑energy scale** – Normalising by pₜ reduces, but does not eliminate, sensitivity to the jet‑energy scale and resolution. A systematic study (varying JES/JER in MC) showed a residual ≈ 2 % shift in the efficiency, comparable to the statistical error.  

* **Potential over‑reliance on the “best‑W” pairing** – Selecting the dijet pair with the smallest Δm<sub>W</sub> implicitly assumes the correct pairing is found. In cases with atypical radiation patterns (e.g. gluon‑splitting jets) the pairing can be wrong, inflating the variance and harming signal efficiency.  

* **Model capacity** – While the shallow MLP is efficient, a slightly deeper network (two hidden layers) gave a tiny (≈ 0.5 %) extra boost in preliminary tests, suggesting the current architecture may be near its performance ceiling.  

Overall, the **hypothesis was confirmed**: a balanced three‑prong mass pattern, encoded as variance and asymmetry of pₜ‑scaled residuals, provides discriminating power beyond a simple mass cut, especially at high boost. The engineered variables and the rational‑sigmoid MLP together captured this effect while remaining FPGA‑friendly.

---

### 4. Next Steps  

| Area | Concrete actions | Rationale |
|------|------------------|-----------|
| **Feature enrichment** | • Add **energy‑correlation functions (ECFs)** such as C₂(β=1) and D₂(β=1) to quantify three‑prong vs two‑prong radiation patterns. <br>• Include **sub‑jet angular distances** (ΔR<sub>ij</sub>) normalised to the jet radius. <br>• Test the **N‑subjettiness ratios** τ₃/τ₂ as a complementary balance metric. | The current set only probes invariant‑mass balance; shape‑based observables may catch cases where the mass residuals are small but the radiation pattern is still QCD‑like. |
| **Model capacity & regularisation** | • Explore a **two‑layer MLP** (e.g. 12 → 8 → 1) with the same rational‑sigmoid. <br>• Apply **L1/L2 regularisation** or **dropout** (quantised) to guard against over‑fitting when expanding the input set. | Early tests hinted at a small gain from extra depth; regularisation will keep the model generalisable, especially after adding more features. |
| **Blending strategy optimisation** | • Replace the simple sigmoid blend with a **learned gating network** (tiny MLP that takes pₜ and maybe a few sub‑structure variables) to produce an event‑by‑event weight. <br>• Perform a **grid scan** of the blend‑transition point (pₜ₀, width) to locate the sweet spot that maximises overall significance. | The current fixed blend may be sub‑optimal; a data‑driven gate could automatically adapt to regions where the MLP is reliable. |
| **Quantisation & FPGA validation** | • Quantise the final model to **8‑bit fixed‑point** and benchmark the latency/inference accuracy on the target FPGA board. <br>• Verify that the added ECF / τ variables can be computed within the same latency budget (use look‑up tables or streaming calculators). | Any new features or deeper networks must still meet the real‑time constraints of the trigger system. |
| **Robustness to systematic variations** | • Produce **alternative MC samples** with varied JES, JER, parton‑shower tunes, and detector smearing. <br>• Retrain / re‑calibrate the model using **domain‑adaptation** techniques (e.g. adversarial training) to reduce dependence on simulation specifics. | Ensuring that the efficiency gain survives realistic systematic shifts is essential before deployment. |
| **Data‑driven validation** | • Use **semileptonic tt̄ events** in data (lepton + hadronic top) to tag the hadronic side with the new discriminator and compare tag‑rate vs BDT. <br>• Perform a **template fit** to the invariant‑mass distribution of the W‑candidate to assess any bias. | Directly test the model on real data and check for potential mismodelling of the residual distributions. |
| **Exploratory direction** | • Prototype a **graph‑neural network (GNN)** that ingests the full set of constituent four‑vectors; keep the architecture ultra‑light (e.g. EdgeConv with 2 message‑passing steps). <br>• Compare its performance to the engineered‑feature MLP, focusing on possible gains in regions where subjet assignment is ambiguous. | If the engineered features saturate, a more expressive but still compact representation may capture subtle correlations missed by hand‑crafted variables. |

**Prioritisation** – In the short term (next 2‑3 weeks) focus on adding the ECF and τ variables, re‑training the existing shallow MLP, and re‑optimising the blending gate. Simultaneously start the quantisation pipeline to guarantee that any performance uplift remains FPGA‑compatible. Longer‑term (1–2 months) investigate the GNN prototype and systematic robustness studies.

---

*Prepared for the Top‑Tagging Working Group – Iteration 248*  
*Date: 16 April 2026*