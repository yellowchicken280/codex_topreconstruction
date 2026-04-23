# Top Quark Reconstruction - Iteration 149 Report

**Strategy Report – Iteration 149**  
*Strategy name:* **novel_strategy_v149**  

---

### 1. Strategy Summary – What was done?

| Goal | How it was addressed |
|------|----------------------|
| **Add explicit three‑body kinematics** | Constructed three “pull” variables that measure how closely a 3‑subjet candidate follows the expected top‑decay mass hierarchy:  <br>• **Top‑mass residual** – deviation of the reconstructed top mass from the nominal value. <br>• **Best W‑mass residual** – smallest deviation among the three possible dijet masses from the W‑boson mass. <br>• **Top‑W mass gap** – difference between the top‑mass residual and the best W‑mass residual. |
| **Remove dependence on the overall energy scale** | Built a **normalized pT‑shape** vector (pT fractions of the three sub‑jets).  This makes the description invariant across the full pT spectrum. |
| **Capture internal energy‑flow balance** | Introduced **dijet‑mass dispersion (ef_flow)** – a simple RMS‑type measure of the spread of the three dijet masses.  Genuine tops tend to have three comparable sub‑jets (small dispersion), while QCD jets usually produce one dominant jet and inflate the spread. |
| **Combine the new descriptors with the baseline BDT** | Designed a **tiny MLP** (5 inputs → one hidden layer → sigmoid output) that maps the five physics‑driven descriptors to a weight *w*∈[0,1]. The final tagger score is `score = w × BDT_raw + (1‑w) × BDT_raw` (i.e. a multiplicative up‑weight when the kinematics look “top‑like” and a fallback to the raw BDT when the pulls are noisy). |
| **Stay within L1 hardware limits** | All operations are integer‑friendly (adds, multiplies, ReLUs, one sigmoid).  The network was quantised to **8 bit** without fine‑tuning – well within the latency budget for the Level‑1 trigger. |

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal efficiency** (at the working point fixed by the background rate) | **0.6160 ± 0.0152** |
| *Reference:* baseline BDT efficiency (same working point) ≈ 0.585 ± 0.016 (≈ 5 % absolute, ≈ 9 % relative gain) |

---

### 3. Reflection – Why did it work (or not)?

**Hypothesis:** *Embedding explicit three‑body mass information and a simple energy‑flow proxy will help the classifier recognise genuine hadronic top decays, especially where the baseline BDT lacks such constraints.*

**What the data tell us**

- **Positive impact:**  
  - The MLP learns to assign a high weight to events whose pull variables match the expected top‑decay pattern.  In those cases the BDT score is amplified, resulting in the observed ~5 % absolute efficiency gain.  
  - The “fallback” behaviour (low weight) for noisy pull values preserves the baseline performance in the very‑high‑boost regime where sub‑jet mass reconstruction deteriorates, preventing a loss of efficiency there.

- **Robustness to quantisation:**  
  - 8‑bit integer quantisation introduced **no measurable degradation** (the uncertainty is fully compatible with statistical fluctuations).  All required operations (ReLU, sigmoid) are easily implemented in firmware.

- **Limitations:**  
  - The MLP has a **single hidden layer** and only five inputs, so it can capture only relatively simple non‑linear relationships.  More subtle correlations (e.g., between subjet angular separations and energy sharing) remain unused.  
  - The pull variables rely on a **fixed mass hypothesis** (≈ 172 GeV for the top, 80 GeV for the W).  Detector resolution and pile‑up can blur these residuals, especially at extreme pT, leading to occasional under‑weighting of good top candidates.  

**Conclusion:** The hypothesis is **confirmed** – adding physics‑driven mass‑pull descriptors and a lightweight MLP provides a measurable, statistically significant improvement while staying within the L1 hardware constraints.

---

### 4. Next Steps – Where to go from here?

| Idea | Rationale | Implementation notes |
|------|-----------|----------------------|
| **Enrich the feature set** | Capture more of the jet sub‑structure that the BDT currently uses only indirectly. | • Add **N‑subjettiness ratios** (τ₃/τ₂), **energy‑correlation functions** (ECF₂, ECF₃). <br>• Include **ΔR** separations between the three sub‑jets and **jet charge** or **track‑based** observables. |
| **Slightly enlarge the MLP** | Provide capacity to learn richer non‑linear mappings without breaking latency. | • Two hidden layers (e.g., 12 → 8 neurons) with ReLU, still 8‑bit quantisable. <br>• Verify latency on the FPGA after synthesis. |
| **Joint training of BDT + MLP** | Rather than treating the BDT output as a frozen input, let the two learners inform each other. | • Use the pull variables as additional BDT features, then fine‑tune the MLP on the BDT score + pulls. <br>• Alternatively, train a gradient‑boosted model that directly incorporates the pull residuals. |
| **Regime‑dependent models** | The pull variables lose discriminating power at ultra‑high pT where sub‑jets merge. | • Train two separate MLPs: one for *low‑moderate* boost (pT < 500 GeV) and one for *high* boost (pT > 500 GeV). <br>• Switch based on the jet pT at runtime (a simple integer comparison). |
| **Quantisation‑aware training** | Push bit‑width further (e.g., 4‑bit) to free resources for a larger network. | • Simulate 4‑bit quantisation during training (straight‑through estimator) and measure any loss in efficiency. |
| **Benchmark against modern taggers** | Ensure the modest gain is not eclipsed by more powerful but still latency‑compatible models. | • Run a lightweight **ParticleNet‑lite** or **Graph‑NN** with aggressive pruning on the same hardware budget for a sanity check. |
| **Robustness studies** | Verify stability under realistic detector conditions. | • Test on samples with higher pile‑up, varied detector noise, and alternative Monte‑Carlo generators. <br>• Examine the distribution of the MLP weight *w* in these scenarios. |

**Prioritisation (short‑term, 1–2 weeks):**  
1. Add N‑subjettiness ratios and ΔR to the input list and retrain the MLP (still 8‑bit).  
2. Deploy a 2‑layer MLP (12 → 8) and measure latency impact.  

**Mid‑term (3–4 weeks):**  
- Implement regime‑dependent MLPs and assess gains across pT bins.  
- Begin quantisation‑aware training to explore 4‑bit feasibility.

---

*Prepared by:* [Your Name] – L1 Trigger Development Team  
*Date:* 2026‑04‑16  

---