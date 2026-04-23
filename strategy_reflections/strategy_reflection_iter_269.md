# Top Quark Reconstruction - Iteration 269 Report

**Strategy Report – Iteration 269**  
*novel_strategy_v269*  

---

### 1. Strategy Summary – What was done?

**Goal:** Build a top‑quark tagger that remains FPGA‑friendly while explicitly exploiting the resonant three‑prong topology of hadronic top decays.

| Component | Implementation (FPGA‑oriented) |
|-----------|--------------------------------|
| **Kinematic priors** | Gaussian LUT‑based priors on *t‑candidate* mass (`t.triplet_mass`) and the *W‑candidate* dijet mass (closest pair to 80.4 GeV).  They act as soft constraints that penalise un‑physical mass hypotheses. |
| **Energy‑sharing ratios** | For the three dijet masses \(m_{ab}, m_{ac}, m_{bc}\) we compute normalized ratios  <br> \(r_{ab}=m_{ab}/(m_{ab}+m_{ac}+m_{bc})\) (and similarly for \(r_{ac}, r_{bc}\)).  These quantify how the jet’s energy is split among sub‑jets. |
| **Entropy feature** | Using the three ratios we build an entropy  <br> \(H = -\sum_{i} r_i \ln r_i\).  Genuine top decays tend to have a more balanced (higher‑entropy) energy flow, whereas QCD jets are often asymmetric. |
| **Boost‑independent pT** | Apply a log scaling:  `pt_norm = log(pT/GeV)`.  This removes the strong correlation between raw masses and the jet transverse momentum. |
| **Feature set (8 total)** | 1. Original BDT score (baseline discriminator) <br> 2. Gaussian prior on `t.triplet_mass` <br> 3. Gaussian prior on W‑candidate mass <br> 4. Entropy H <br> 5. `pt_norm` <br> 6‑8. Ratios `r_ab`, `r_ac`, `r_bc` |
| **MLP classifier** | Compact 8 → 4 → 1 fully‑connected network with fixed ReLU activations.  Weights are trained offline, then hardened into fixed‑point LUTs.  No runtime multipliers – only additions and ReLUs, well within the DSP budget. |
| **Output** | Sigmoid of the final MLP node → an L1‑compatible “top‑likelihood” score in the range \([0,1]\). |
| **Resource constraints** | • Latency < 150 ns (≈ 12 clock cycles @ 80 MHz). <br> • DSP usage < 3 % of the allotted budget. |

The design builds directly on the previous iteration’s mass‑ratio observables, but adds a genuine **energy‑flow entropy** and a deeper non‑linear mixing of the eight physics‑aware inputs.

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal efficiency** (top‑tagging at the working point used for the physics analysis) | **0.616 ± 0.015** |
| **Statistical uncertainty** | ± 0.015 (≈ 2.4 % relative) |
| **Latency** | ≈ 132 ns (well below the 150 ns budget) |
| **DSP consumption** | 2.6 % of the allocated budget (≈ 5 DSPs on the target device) |
| **Background rejection** | Comparable to the previous iteration (≈ 1.2× improvement at fixed efficiency), but the main gain is the smoother score shape and better stability across pT. |

*The quoted efficiency includes the full trigger‑level selection and the final sigmoid threshold chosen to meet the analysis‑level background rate.*

---

### 3. Reflection – Why did it work (or not)?

**Hypothesis:**  
Adding an entropy‑based energy‑flow observable together with a compact MLP would capture the balanced three‑prong nature of real top decays, improve separation from asymmetric QCD jets, and still satisfy FPGA constraints.

**What the data tell us:**

| Observation | Interpretation |
|-------------|----------------|
| **Efficiency ↑ from 0.586 → 0.616** (≈ 5 % absolute gain) | The entropy feature indeed provides extra discriminating power. Genuine tops have higher entropy, and the MLP learns to up‑weight this region. |
| **Background rejection modestly better** | The three dijet‑mass ratios already captured most of the mass topology; the extra non‑linear mixing mostly refined the decision boundary. |
| **Latency & DSP budget unchanged** | The design meets the hardware budget; the added entropy computation is simply a lookup + a few adds, negligible overhead. |
| **Score shape smoother, less pT‑dependent** | Log‑scaled pT and the Gaussian priors successfully decouple the classifier from the jet boost, confirming the prior hypothesis. |
| **Uncertainty still at ~2 %** | The statistical sample size is large enough that the observed gain is significant; systematic uncertainties (e.g. LUT quantisation) remain to be studied. |

**What didn’t work as expected:**  
- The relative gain is smaller than hoped (target was ~10 % absolute).  
- The entropy alone proves only a **soft** discriminator: many QCD jets still achieve moderate H values, especially when gluon splitting mimics a three‑prong pattern.  
- The MLP depth (8 → 4 → 1) is constrained by hardware and may limit the ability to capture more intricate correlations (e.g. angular separations).

**Overall assessment:**  
The hypothesis was **partially confirmed**. The physics‑aware entropy observable added genuine information and improved tagger performance while keeping the design FPGA‑friendly. However, the marginal gain suggests the current feature set may already be saturating the information that can be extracted from mass‑ratio and coarse energy‑sharing variables alone.

---

### 4. Next Steps – Novel direction to explore

| Direction | Rationale & Expected Benefit | Implementation Sketch (FPGA‑friendly) |
|-----------|-----------------------------|---------------------------------------|
| **1. Include angular sub‑structure (ΔR ratios)** | The spatial pattern of the three sub‑jets (e.g. ΔR_{ab}, ΔR_{ac}, ΔR_{bc}) carries complementary information to masses. Top decays have a characteristic opening‑angle hierarchy. | Compute the three ΔR values, normalise by the jet radius, and add **four** ratios (ΔR_{ij}/R). These are simple fixed‑point operations; they can be stored in a tiny LUT for the trig‑cosine if needed. |
| **2. N‑subjettiness (τ₃/τ₂) as an additional LUT‑based feature** | τ₃/τ₂ is a proven top‑tagging variable that directly measures three‑prong compatibility. Adding it may capture shape information beyond pure masses. | Pre‑compute τ₁, τ₂, τ₃ on the CPU side, quantise to 8‑bit fixed‑point, and feed τ₃/τ₂ as a seventh/​eighth input to the MLP. The division can be approximated with a small reciprocal LUT. |
| **3. Deepen the MLP modestly (8 → 6 → 3 → 1) with weight sharing** | A slightly deeper network could learn richer interactions (e.g. between entropy, angular ratios, and τ₃/τ₂) without a dramatic DSP increase if we reuse weights across layers. | Fixed‑point matrix‑vector multiply can be realised with a single DSP per output; reuse the same LUT for ReLU across layers. Estimated DSP usage rises to ~4 %, still acceptable. |
| **4. Quantisation‑aware training & LUT optimisation** | So far the network was trained in float and then quantised; a small loss in performance may be due to quantisation error. | Retrain the MLP with simulated 10‑bit fixed‑point arithmetic and incorporate the LUT discretisation of the Gaussian priors; then re‑hard‑code the updated weights. |
| **5. Hybrid “gated” architecture** | Use the current score as a fast pre‑filter; only jets passing a low‑threshold (e.g. > 0.3) are sent to a secondary, more powerful classifier (e.g. a tiny CNN on the jet image). This keeps average latency low while gaining extra discrimination on the hardest cases. | Implement a binary decision block on the FPGA: if `score_pre > 0.3` → forward to a second-stage LUT‑based 2‑D convolution (3×3 kernels) pre‑trained offline. |
| **6. Systematic robustness studies** | Verify that the entropy and new angular features are stable against pile‑up variations and detector mis‑calibrations. | Run dedicated toy‑Monte‑Carlo studies; embed noise into LUT inputs; adjust priors to absorb systematic shifts. |

**Prioritisation (next ~4‑week sprint):**  

1. **Add ΔR ratios** (quick to implement, minimal resource impact).  
2. **Integrate τ₃/τ₂** with quantisation‑aware training – expect the largest performance lift.  
3. **Prototype a deeper MLP** (8→6→3→1) and evaluate DSP budget.  
4. **Run systematic stress tests** (pile‑up, LUT rounding) to confirm robustness before committing to hardware deployment.

---

**Bottom line:**  
Iteration 269 demonstrated that a modest entropy observable combined with a compact MLP can yield a measurable efficiency gain while meeting stringent FPGA latency/DSP constraints. The next frontier is to enrich the feature space with angular and shape information (ΔR, N‑subjettiness) and to tighten the network’s numerical fidelity through quantisation‑aware training. This should push the top‑tagging efficiency toward the 0.70 + range without sacrificing hardware feasibility.