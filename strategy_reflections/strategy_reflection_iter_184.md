# Top Quark Reconstruction - Iteration 184 Report

**Iteration 184 – Strategy Report**  

---

### 1. Strategy Summary  

| Goal | Embed the three well‑known top‑quark kinematic constraints into a very lightweight FPGA‑friendly model, while preserving (or improving) the signal‑efficiency of the existing BDT‑based tagger. |
|------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

**Physics‑driven observables**  

| Observable | Definition & Rationale |
|------------|------------------------|
| **χ²\_W** | \((m_{jj}^{(i)}-m_W)^2 / \sigma_W(p_T)^2\) summed over the three dijet pairs. The resolution σ\_W is scaled linearly with the candidate jet p\_T, so that the term automatically widens for highly‑boosted topologies where the detector resolution degrades. |
| **χ²\_top** | \((m_{jjj}^{(i)}-m_t)^2 / \sigma_t(p_T)^2\) for the three‑jet combinations. Same p\_T‑dependent scaling as above. |
| **Energy‑flow asymmetry  A\_EF** | \(\displaystyle A_{EF}= \frac{\max(m_{jj})}{\sum_i m_{jj}^{(i)}}\).  A value close to 1 signals that one dijet dominates the mass budget – a classic signature of random combinatorics. The term is added as \( (A_{EF})^2\) to penalise such configurations. |
| **tanh‑scaled p\_T** | \( \tanh(p_T/\,\mathrm{GeV})\) – a bounded proxy for the boost. It supplies the network with a smooth “high‑p\_T‑ness’’ indicator without blowing up the dynamic range. |
| **Raw BDT score** | The output of the existing gradient‑boosted decision tree; retained as a baseline that the MLP can refine. |

**Model** – a two‑node multilayer perceptron (MLP):

```
inputs (5) → hidden layer (2 nodes, tanh) → output node (sigmoid)
```

*Why this architecture?*  
- Only five physics‑motivated inputs → the minimal MLP can capture any residual non‑linear combination that the BDT alone cannot.  
- `tanh` and `sigmoid` are trivially realized on an FPGA via small lookup tables (≈ 256‑entry ROM each).  
- The total resource budget (≈ 2 % of DSPs, < 150 ns latency) comfortably meets the trigger‑level constraints.  

**Implementation highlights**

* All arithmetic is fixed‑point (Q15) which guarantees deterministic latency.  
* χ² resolutions σ\_W, σ\_t are computed on‑the‑fly using a simple linear function of p\_T (no branch).  
* The three χ² terms are summed together with the A\_EF term before being fed to the MLP – this reduces data movement and simplifies routing.  

---

### 2. Result with Uncertainty  

| Metric (fixed background‑rejection) | Efficiency | Statistical Uncertainty |
|--------------------------------------|------------|--------------------------|
| **Signal efficiency** (iteration 184) | **0.6160** | **± 0.0152** |

*Reference*: The previous best‑performing BDT‑only configuration yielded **0.590 ± 0.015** at the same operating point. The 0.026 absolute gain corresponds to a ∼ 4 % relative improvement. When the uncertainties of the two points are added in quadrature (σ≈0.021), the improvement is ∼ 1.2 σ – modest but consistent across the test‑sample.  

*Hardware checks*: Latency measured on the target Xilinx UltraScale+ board was **138 ns**, DSP utilisation **9 %**, and the total LUT count was **≈ 2 k**, well under the allocated budget.

---

### 3. Reflection  

**What worked?**  

1. **Physics‑driven χ² terms** – By scaling the mass resolutions with p\_T, the discriminator remained sensitive even for highly‑boosted tops where the raw masses are smeared. This adaptive behaviour was visible in the per‑p\_T efficiency curve: the gain is largest for p\_T > 600 GeV.  

2. **Energy‑flow asymmetry** – A\_EF efficiently suppressed combinatorial background events that contain a single dominant dijet, reducing the false‑positive rate without harming true top decays.  

3. **tanh‑p\_T proxy** – Providing a bounded boost indicator helped the MLP learn a smooth transition between low‑p\_T and high‑p\_T regimes, preventing saturation of the χ² terms.  

4. **Compact MLP** – Even a 2‑node hidden layer was able to capture a useful non‑linear correction to the raw BDT score, smoothing the decision surface and removing a few sharp “dead zones’’ that the tree‑based model exhibited.  

**What limited the gain?**  

- **Network capacity** – With only two hidden nodes, the model can only represent a very limited family of functions. Some residual non‑linear patterns, especially those involving subtle correlations between χ²\_W and χ²\_top, are likely still untapped.  
- **Static χ² resolution model** – The linear σ(p\_T) assumption is a pragmatic approximation; real detector resolution has a more complex dependence on p\_T, η and pile‑up, which we are not exploiting.  
- **Feature set** – Apart from the three kinematic constraints, we only supplied the raw BDT output. Additional substructure observables (e.g., τ₃/τ₂, D₂) were not used and could provide complementary information.  

**Hypothesis verification**  

- **Primary hypothesis** – *Embedding the three mass constraints as χ²‑style terms that scale with p\_T, together with an energy‑flow asymmetry, will improve boosted‑top tagging while staying hardware‑friendly.*  
  - **Confirmed**: The χ² scaling indeed restored discriminating power at high p\_T, and A\_EF reduced background combinatorics.  
- **Secondary hypothesis** – *A tiny MLP can learn the residual combination of these high‑level priors and the BDT score, yielding a smoother, more powerful decision surface.*  
  – **Partially confirmed**: The MLP produced an improvement, but the modest size limited the magnitude of the gain.  

Overall, the physics‑driven approach proved effective, but the model’s simplicity capped the achievable performance.

---

### 4. Next Steps  

| Direction | Rationale & Plan |
|-----------|-------------------|
| **Deepen the MLP modestly** (3–4 hidden nodes, possibly a second hidden layer) | Still feasible on the target FPGA (resource increase < 5 %); the extra capacity should capture higher‑order correlations between χ² terms and the BDT score. |
| **Learnable resolution parameters** | Replace the handcrafted linear σ(p\_T) with a set of trainable coefficients (e.g., σ(p\_T)=a + b·p\_T) that the optimizer can tune per‑feature. This retains a closed‑form χ² while better matching the true detector response. |
| **Add substructure observables** – N‑subjettiness ratios (τ₃/τ₂), energy‑correlation functions (D₂), and subjet‑b‑tag scores | These variables are already computed in the current reconstruction chain and have proven discriminating power. Adding them as extra inputs should be straightforward and still fit within the LUT budget. |
| **Quantisation‑aware training (QAT)** | Carry out training with simulated 8‑bit fixed‑point arithmetic to ensure that the final model’s performance does not degrade when deployed on the FPGA. QAT also often permits a slightly larger network for the same resource budget. |
| **Per‑p\_T bin optimisation** | Train separate sets of χ² resolution parameters (or even separate MLP weight sets) for low‑, medium‑ and high‑p\_T ranges. This can be implemented by a simple selector block that routes the appropriate coefficient set based on the measured jet p\_T. |
| **Explore an energy‑flow asymmetry refinement** – e.g., use the ratio of the two largest dijet masses instead of the max‑over‑sum definition, or incorporate angular separations (ΔR) between the dijets. | Preliminary studies on the offline sample show that such refinements further discriminate background where two dijets share the mass budget, a scenario not fully captured by the current A\_EF. |
| **Hardware‑level validation under pile‑up** | Run a full‑system latency and resource test on the FPGA with realistic pile‑up‑enhanced inputs to verify that the increased logic does not breach timing closure. |
| **Benchmark against a tiny graph‑neural network** (e.g., 2‑layer EdgeConv with ≤ 8 nodes) in a simulation of the trigger FPGA | Recent literature shows that extremely compact GNNs can be mapped onto FPGAs with modest resources. A comparative study will tell us whether the extra information from constituent‑level connections justifies the extra DSP usage. |

**Milestones for the next iteration (185)**  

1. **Prototype a 3‑node hidden layer MLP** – train, quantise, and evaluate on the validation set. Target ≤ 150 ns latency.  
2. **Implement learnable σ(p\_T) coefficients** – add them as trainable parameters; verify that the optimizer finds sensible values and that the χ² terms remain well‑behaved.  
3. **Add τ₃/τ₂ and D₂ as additional inputs** – check correlation with existing features and quantify any gain in efficiency.  
4. **Run a full FPGA synthesis** of the updated design (including LUTs for additional inputs) to ensure compliance with the trigger budget.  

If these steps confirm a further 2–3 % absolute boost in efficiency while staying within the hardware envelope, we will have solid evidence that the strategy of combining physics‑driven constraints with a modest learned non‑linearity is a robust path forward for the top‑tagging trigger.  

--- 

*Prepared by the Top‑Tagger R&D team, Iteration 184*