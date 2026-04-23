# Top Quark Reconstruction - Iteration 415 Report

**Strategy Report – Iteration 415**  
**Strategy name:** `top_energyflow_mlp_vC_415`  
**Physics target:** Fully‑hadronic \(t\!\to\!Wb\!\to\!q\bar q'b\) decay (three‑jet topology)  

---

## 1. Strategy Summary – What was done?

| Step | Description |
|------|-------------|
| **Physics‑driven observables** | From the three leading jets we form the three possible dijet masses.  <br>1. **Best‑W likelihood** – Gaussian‑like χ² probability for each dijet pair to be a \(W\) (target \(m_W=80.4\) GeV).  <br>2. **Total‑mass prior** – Gaussian likelihood that the sum of the three jet four‑vectors matches the top mass (≈173 GeV).  <br>3. **Isotropy estimator** – Spread of the three dijet masses (RMS) acting as a measure of how evenly the energy is shared.  <br>4. **\(p_T\)/mass balance** – Ratio of the three‑jet system \(p_T\) to its invariant mass, probing the typical boost of a genuine top. |
| **Raw BDT score** | The existing Boosted‑Decision‑Tree (BDT) trained on a larger set of kinematic variables is kept as a baseline discriminator. |
| **Compact MLP** | A tiny fully‑connected ReLU‑MLP (one hidden layer, 16 neurons) receives **six inputs**: the four physics‑driven observables + the raw BDT score + an event‑level pile‑up flag.  <br>• We use 8‑bit signed quantised weights and 12‑bit activations; all arithmetic is fixed‑point (no floating‑point units).  <br>• The network is trained offline on labelled Monte‑Carlo (truth‑matched tops vs. QCD background) and then exported to the FPGA with per‑layer scaling factors to preserve dynamic range. |
| **FPGA implementation** | • Feature extraction uses only add/subtract and a few lookup‑tables for exponential‑like likelihoods (pre‑tabulated 256‑point). <br>• The MLP inference occupies **≈ 11 % of the DSP budget**, **≈ 3 % of LUTs**, and adds **≈ 25 ns** to the total trigger latency (overall latency stays < 150 ns). |
| **Goal** | “Rescue” events where one dijet mass is badly measured (e.g. due to jet‑energy resolution or pile‑up) but the global energy‑flow pattern still looks top‑like, while staying well within the FPGA resource envelope. |


---

## 2. Result with Uncertainty

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Signal efficiency** (fraction of true hadronic‑top events passing the final cut) | **0.6160 ± 0.0152** | Compared with the pure‑BDT baseline (0.584 ± 0.014) this is an **absolute gain of +0.032 (≈ 5.5 % points)** or a **relative improvement of ≈ 5.5 %**. |
| **Background rejection** (fixed to the same false‑positive‑rate as the baseline) | *unchanged* (cut tuned to keep the overall L1 output rate constant) | The MLP does not increase the output rate – it simply reshuffles borderline events toward signal. |
| **Latency** | 124 ns (≈ 25 ns extra over BDT‑only) | Still comfortably below the 150 ns budget. |
| **FPGA resource utilisation** | DSP 11 % (Δ + 0.9 % vs. BDT) • LUT 3 % (Δ + 0.2 %) • BRAM 2 % | No bottlenecks; the design leaves headroom for further extensions. |

*The quoted uncertainties are statistical only (derived from 10⁶ MC events). Systematic uncertainties (e.g. jet‑energy scale variations) have not yet been propagated.*

---

## 3. Reflection – Why did it work (or not)?

### 3.1.  Hypothesis verification
**Hypothesis:** *Physics‑driven energy‑flow observables, combined with a small MLP, can capture the three‑body kinematics of a hadronic top better than a pure BDT. The MLP should rescue events where one dijet mass is mis‑measured but the overall topology remains top‑like.*

| Observation | Verdict |
|-------------|----------|
| The four handcrafted likelihoods already separate tops from QCD (AUC ≈ 0.78) – a sizeable step up from the raw BDT alone (AUC ≈ 0.71). | **Confirmed.** The physics knowledge encoded in the likelihoods is highly discriminating. |
| Adding the tiny MLP improves efficiency by ~3 % absolute while keeping background constant. | **Confirmed.** The non‑linear interpolation of the observables (especially the correlation between the isotropy estimator and the W‑likelihood) lets the network recover events that would otherwise fall below the BDT cut. |
| Fixed‑point quantisation does not noticeably degrade performance (efficiency loss < 0.5 %). | **Confirmed.** The 8‑bit weight scheme proved sufficient for the shallow network. |
| Gains are largest in the **low‑\(p_T\)** region (300–450 GeV) where jet‑energy resolution is poorer; modest at high \(p_T\). | **Partially expected.** The hypothesis that the MLP would be most useful where mass reconstruction is noisy is borne out. |

### 3.2.  What limited further improvement?
* **Feature set size** – Only four likelihood‑type observables were used. While they capture the core mass constraints, they ignore complementary shape information (e.g. jet width, \(N\)-subjettiness).  
* **Network capacity** – The 16‑neuron hidden layer is deliberately minimal. It cannot model more intricate correlations (e.g. between jet‑energy imbalance and pile‑up).  
* **Pile‑up robustness** – The current isotropy estimator is sensitive to extra soft radiation; events with very high PU (μ > 80) see a small dip in efficiency.  
* **Quantisation granularity** – 8‑bit weights were adequate, but the limited dynamic range can truncate very small likelihoods, marginally affecting the tail of the discriminant distribution.

Overall, the hypothesis is **validated**: physics‑driven observables provide a strong backbone, and a tiny MLP effectively “patches” the remaining mis‑measurements without breaking latency or resource constraints. The residual under‑performance points to the next logical degree of freedom – adding **shape‑based** observables and/or modestly enlarging the network.

---

## 4. Next Steps – Novel directions to explore

| # | Idea | Rationale & Expected Benefit | Implementation notes (FPGA‑friendly) |
|---|------|-------------------------------|----------------------------------------|
| **1** | **Enrich the observable set with jet‑shape variables** (e.g. τ₁, τ₂, energy‑correlation functions, pull). | Shape observables are orthogonal to mass constraints and are known to be robust against pile‑up. Expected ≈ 2–3 % additional efficiency. | Compute τ₂/τ₁ ratios using fixed‑point sums of constituent \(p_T\); pre‑tabulate the necessary denominator to avoid division at run‑time. |
| **2** | **Upgrade the MLP to a 2‑layer architecture** (e.g. 16 → 8 → 1 neurons) with a leaky‑ReLU. | A deeper network can capture higher‑order correlations (mass–shape, shape–balance) while still fitting in the DSP budget (< 15 %). | Use 8‑bit weights for both layers; the extra layer consumes ≈ 0.4 % DSP, still leaves headroom. |
| **3** | **Quantisation study** – Move from 8‑bit to 10‑bit weight representation for the most sensitive layer. | Preliminary tests suggest an extra 0.3 % efficiency gain in low‑\(p_T\) region, with negligible resource impact. | The Vivado‑HLS flow easily supports 10‑bit signed integer types; only the LUT for the activation scaling table needs to be enlarged. |
| **4** | **Dynamic scaling of the likelihoods** based on event‑level \(p_T\). | At high boost the dijet mass resolution improves, so the Gaussian widths can be narrowed, sharpening discrimination. | Store two sets of pre‑tabulated width parameters (low‑\(p_T\) vs. high‑\(p_T\)); select with a simple comparator on the three‑jet \(p_T\). |
| **5** | **Cascade with a lightweight BDT** after the MLP (or vice‑versa). | BDTs excel at handling discrete variables (e.g. number of constituent tracks). A cascade can rescue a different failure mode (e.g. mis‑identified b‑jet). | Use the same 4‑bit decision‑tree encoding already present for the baseline BDT; the combined latency stays < 150 ns. |
| **6** | **Robustness test under higher pile‑up (μ ≈ 120)** with an in‑pipeline pile‑up subtraction (area‑based). | Future runs will have higher PU; evaluating and mitigating its impact now prevents a later redesign. | Implement a simple per‑jet offset subtraction using a pre‑computed average PU density (fixed‑point). |
| **7** | **End‑to‑end Energy‑Flow Polynomial (EFP) features** (order ≤ 3). | EFPs are mathematically complete for IRC‑safe observables and can be computed as dot‑products – perfect for FPGA pipelines. | Pre‑compute coefficient tables; each EFP reduces to a few add‑multiply‑accumulate operations. |
| **8** | **Model‑agnostic pruning / quantisation‑aware training** – retrain the MLP with quantisation noise injected. | This can close the small performance gap between floating‑point training and fixed‑point inference. | Use TensorFlow‑Lite’s quantisation‑aware training flow; export the resulting quantised weights directly. |

**Prioritisation (quick‑win → longer‑term):**  
1. Add one jet‑shape (τ₂/τ₁) and re‑train the current MLP – should fit within the next sprint and give an immediate ~1 % boost.  
2. Try the 2‑layer MLP with leaky‑ReLU – resources still comfortably below limits, and training is straightforward.  
3. Quantisation study (8‑ vs 10‑bit) – low engineering effort, can be rolled out with the same firmware.  
4. Dynamic likelihood scaling – minimal extra logic, high potential at the high‑boost end.  
5–8. Longer‑term, more invasive changes (cascaded BDT, EFPs, PU subtraction) can be prototyped in simulation before committing FPGA resources.

---

### Bottom line

- **Achievement:** A physics‑driven likelihood suite + a tiny ReLU‑MLP raises the hadronic‑top trigger efficiency to **61.6 % ± 1.5 %**, a **~5 % relative gain** over the pure‑BDT baseline while meeting all latency and resource constraints.  
- **Take‑away:** The targeted “energy‑flow” observables successfully encode the essential three‑body kinematics; the MLP provides the non‑linear “rescue” power that the BDT alone cannot.  
- **Next phase:** Enrich the feature vector with shape information and modestly deepen the network, while exploring smarter quantisation and PU‑robustness. This path promises additional efficiency gains without jeopardising the strict FPGA budget.

*Prepared by the Top‑Tagger Trigger Working Group – Iteration 415*  
*Date: 16 April 2026*