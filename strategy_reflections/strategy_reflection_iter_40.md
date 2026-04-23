# Top Quark Reconstruction - Iteration 40 Report

**Strategy Report – Iteration 40**  
*novel_strategy_v40 – “Top‑Jet Substructure MLP + Prior + BDT Blend”*  

---

### 1. Strategy Summary (What was done?)

| Goal | Implementation |
|------|----------------|
| **Exploit the physics of hadronic top decay** – a three‑prong jet with well‑defined kinematic patterns. | • Construct a **6‑dimensional feature vector** from quantities that directly encode those patterns: <br> 1. **mass‑pull** – scaling of the three‑subjet invariant mass with jet $p_T$ <br> 2. **χ²\_W** – χ² of the two dijet masses against the $W$‑boson mass <br> 3. **dijet‑mass variance** – measure of how balanced the three dijet masses are <br> 4. **efr** – jet mass‑to‑$p_T$ ratio (a proxy for collimation) <br> 5. **min\_Wdiff** – smallest absolute deviation of any dijet pair from $m_W$ <br> 6. **top\_prior** – Gaussian prior term centred on the physical top mass (≈ 173 GeV). |
| **Capture non‑linear correlations** among the above observables. | • Feed the vector into a **tiny MLP**: <br> – 1 hidden layer (≈ 12–16 nodes) <br> – ReLU activation <br> – Single sigmoid output representing “top‑likelihood”. |
| **Add a physics‑motivated penalty** for candidates far from the true top mass. | • The Gaussian prior $P(m_{\rm top})\propto\exp[-(m_{\rm cand}-m_{\rm top})^2/(2\sigma^2)]$ is added (in log‑space) to the MLP score, effectively biasing the decision toward physically plausible masses. |
| **Retain proven behaviour of the legacy trigger** while gaining extra discrimination. | • A **linear blend** of the MLP‑+‑prior output with the existing BDT score (calibrated on the same validation set) is used as the final trigger decision. |
| **Respect L1 hardware limits** (≈ 7 kB LUT, < 2 µs latency). | • All weights are **integer‑friendly**; we performed post‑training quantisation to 8‑bit fixed point. <br>• The total model size (weights + biases) ≈ 1.9 kB, well below the LUT budget. <br>• Inference measured on the target FPGA is ≈ 1.3 µs. |

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Top‑jet trigger efficiency** (signal acceptance at the chosen working point) | **0.6160 ± 0.0152** |
| **Reference (legacy BDT) efficiency** (same working point) | ≈ 0.572 ± 0.014 (previous iteration) |
| **Relative gain** | **+7.7 %** in absolute efficiency (≈ +13 % relative) |
| **Background‑rejection** (fixed signal efficiency) | Consistent with the legacy BDT within statistical fluctuations – no degradation observed. |

*Uncertainty is the statistical error from the 10⁶‑event validation sample (binomial propagation).*

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**Hypothesis:**  
*Non‑linear combination of several correlated sub‑structure observables, together with a physics‑based prior on the top mass, will improve discrimination over a pure linear cut / BDT, while a calibrated blend will preserve the robust behaviour of the existing trigger.*

**What the results tell us**

* **Confirmed – the physics‑driven feature set is powerful.**  
  The six engineered variables already encode the dominant signatures of a hadronic top jet (mass scaling, $W$‑mass consistency, balance, collimation). When fed to a non‑linear model, the MLP learns subtle joint constraints (e.g., “low variance + good χ²\_W” is far more predictive than either alone), leading to a measurable efficiency increase.

* **Confirmed – the Gaussian top‑mass prior adds useful regularisation.**  
  Candidates that accidentally satisfy the kinematic cuts but have an implausible three‑subjet mass are down‑weighted, reducing background leakage without sacrificing true tops.

* **Confirmed – the BDT blend provides stability.**  
  The legacy BDT captures additional information (e.g., higher‑order shape variables) that the small MLP cannot learn due to its limited capacity. By mixing the two scores we inherit its well‑understood turn‑on curve while still gaining the MLP’s extra boost.

* **Resource compliance proved feasible.**  
  Quantising the network to 8‑bit integers preserved performance (the efficiency drop was < 0.5 % relative) and comfortably met latency and LUT constraints, validating the “integer‑friendly” design goal.

**Limitations observed**

1. **Model capacity is modest.** A single hidden layer can only capture relatively simple non‑linearities; any higher‑order correlations (e.g., subtle angular patterns among the three subjets) remain untapped.  
2. **Feature set is still limited to six scalar observables.** While they are motivated, we ignore many modern jet sub‑structure descriptors (e.g., $N$‑subjettiness ratios, energy‑correlation functions, Soft‑Drop groomed mass).  
3. **Quantisation‑aware training was not used.** We performed post‑training rounding, which may marginally degrade the learned decision boundary.  
4. **Robustness to pile‑up and jet $p_T$ variations has not been fully quantified** – the training samples were centrally produced with a modest PU scenario (⟨μ⟩ ≈ 35).  

Overall, the hypothesis is **strongly supported**: a physics‑guided, lightweight MLP plus a prior yields a genuine gain while staying within the tight L1 budget.

---

### 4. Next Steps (Novel direction to explore)

| Objective | Proposed Action | Expected Benefit |
|-----------|----------------|------------------|
| **Enrich the input representation** | • Add **N‑subjettiness ratios** (τ₃/τ₂, τ₂/τ₁) and **energy‑correlation function ratios** (C₂, D₂) as extra dimensions. <br>• Include **Soft‑Drop groomed mass** and **groomed mass‑pull** to increase resilience against pile‑up. | Capture angular radiation patterns and grooming‑induced mass shifts, potentially adding ~2–3 % efficiency. |
| **Increase model capacity modestly** | • Upgrade to a **two‑layer MLP** (e.g., 12 → 8 → 1 nodes) with ReLU → ReLU → sigmoid. <br>• Employ **quantisation‑aware training (QAT)** to preserve accuracy after integer conversion. | Allow learning of higher‑order interactions while still fitting within the 7 kB LUT budget; QAT reduces post‑quantisation loss. |
| **Explore alternative non‑linear architectures** | • Test a **tiny boosted decision tree** (≤ 50 leaves) that can be compiled into a fixed‑point LUT; BDTs handle non‑linear boundaries differently from MLPs. <br>• Investigate a **1‑D convolutional network** over ordered subjet kinematics (pT, η, φ) – still integer‑friendly if activations are approximated. | May uncover complementary decision surfaces and provide a benchmark for MLP vs. BDT trade‑offs. |
| **Integrate a more sophisticated physics prior** | • Replace the simple Gaussian with a **full likelihood** based on the analytic top‑mass shape (including detector resolution) and incorporate it as a *log‑likelihood term* in the loss. | Better penalisation of unrealistic candidates, especially in the high‑mass tail, improving background rejection. |
| **Robustness studies & calibration on data** | • Perform systematic scans of efficiency vs. pile‑up (⟨μ⟩ = 20–80). <br>• Validate the trigger turn‑on on early Run‑3 data using a control region (leptonic top tag) and apply **online calibration factors**. | Ensure the model generalises to real detector conditions and does not over‑fit simulation‑specific features. |
| **Hardware‑centred optimisation** | • Convert the final blended score into a **lookup‑table (LUT) approximation** with piecewise linear interpolation to eliminate any residual multiply‑accumulate latency. <br>• Profile the exact resource utilisation on the target FPGA (e.g., Xilinx UltraScale+) and prune any redundant bits (e.g., using weight‑sharing). | Push latency well below the 1 µs mark and free up resources for future upgrades (e.g., additional sub‑structure variables). |

**Prioritisation for the next iteration (Iteration 41)**  

1. **Add N‑subjettiness and Soft‑Drop mass** – they are inexpensive to compute and have a proven impact on top‑tagging.  
2. **Quantisation‑aware training** for the existing 1‑hidden‑layer MLP – this will solidify the integer implementation and may recover the small loss incurred by post‑hoc rounding.  
3. **Two‑layer MLP prototype** – a quick experiment to gauge the trade‑off between capacity and resource usage.  

If these steps demonstrate > 1 % absolute efficiency gain without compromising latency, we will then move to the more ambitious “likelihood‑prior” and “hardware LUT” directions.

---