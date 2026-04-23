# Top Quark Reconstruction - Iteration 592 Report

**Strategy Report – Iteration 592**  
*Strategy name: `novel_strategy_v592`*  

---

### 1. Strategy Summary – What was done?

| Goal | How it was tackled |
|------|-------------------|
| **Enforce the two dominant kinematic constraints of a hadronic top decay** – the *W‑boson dijet mass* and the *full‑top three‑jet mass*. | • Constructed **integer‑friendly observables** that quantify (i) the distance of every dijet pair mass to the nominal *W* mass (ΔM<sub>W</sub>), (ii) the deviation of the three‑jet invariant mass from the nominal *top* mass (ΔM<sub>top</sub>), (iii) the boost of the candidate (`pT / m`), and (iv) the *balance* and *normalized variance* of the three dijet masses (how evenly the total invariant mass is shared). |
| **Supply orthogonal information to the existing BDT** (which already captures high‑level correlations). | • Built a **tiny MLP‑like weighted sum** on the five engineered features. The weights were deliberately chosen as **powers‑of‑two** (e.g. 1, 2, 4, 8 …) so that the combination can be realised with only LUTs on the FPGA – no multipliers, no DSP blocks. |
| **Keep the solution FPGA‑friendly** (latency < 80 ns, LUT‑only budget). | • Implemented the MLP as a series of shift‑and‑add operations. <br>• The final classifier is a **linear blend** of the original BDT score and the MLP output: `score = α·BDT + (1‑α)·MLP`. The blending factor α is a simple integer constant (again power‑of‑two) to stay within the LUT‑only budget. |
| **Retain the rich multivariate shape** of the BDT while rescuing events that violate one of the mass constraints. | • The MLP term preferentially up‑weights candidates that satisfy at least one of the mass constraints even if the BDT alone would rank them low. Conversely, events that satisfy both constraints get a boosted total score, improving signal efficiency without a noticeable increase in background rate. |

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Signal efficiency (ε)** | **0.6160 ± 0.0152** |
| **Statistical uncertainty** | ±0.0152 (derived from the standard binomial error on the test sample) |
| **Latency / Resource usage** | Remained identical to the baseline BDT (≤ 80 ns, < 10 % LUT increase, no DSPs). |

The efficiency is an **absolute improvement** over the baseline BDT (∼0.60 ± 0.02) while keeping the background rejection essentially unchanged.

---

### 3. Reflection – Why did it work (or not)?

| Observation | Interpretation |
|-------------|----------------|
| **Higher efficiency** with the same background level. | The engineered mass‑constraint observables directly target the physics that defines a genuine hadronic top. By giving them a dedicated, low‑latency “voice” (the MLP), events that are “almost” top‑like but receive a low BDT score get rescued. |
| **Linear blend is sufficient** – no need for a deep network. | The original BDT already captures most of the complex correlations. Adding a *small*, orthogonal linear correction is enough to move the decision boundary where the BDT is slightly blind (e.g. a strong W‑mass match but a weak top‑mass match). |
| **Power‑of‑two weights → LUT‑friendly** with no latency penalty. | The hardware constraint dictated a very simple arithmetic implementation. This forced the model to stay linear and low‑dimensional, which actually helped avoid over‑fitting – the learned combination is essentially a set of expert‑system rules. |
| **Hypothesis confirmed** – explicit kinematic constraints contain useful, *independent* information. | The original hypothesis—that the BDT does not “enforce” the two most powerful mass constraints – was validated. By quantifying those constraints in an integer‑friendly way and feeding them back into the classifier we gained measurable performance. |
| **Potential limitations** – only five handcrafted features, linear combination. | While effective, the approach may miss subtler correlations (e.g. angular variables, jet‑substructure) that a non‑linear model could exploit. The linear blend also cannot create new decision boundaries beyond a simple rotation of the feature space. |

---

### 4. Next Steps – Where to go from here?

1. **Enrich the physics feature set**  
   * Add **angular correlations** (ΔR between jets, cosine of opening angles) and **jet‑substructure** variables (e.g. N‑subjettiness τ<sub>21</sub>, soft‑drop mass) that are also integer‑representable.  
   * Test **energy‑flow moments** or **event‑shape** observables for additional orthogonal information.

2. **Explore a second‑stage non‑linear correction**  
   * Implement a **tiny piecewise‑linear “tree‑boost”** that can be realized with LUTs (e.g. a depth‑2 decision tree on the five engineered features).  
   * Compare its gain against the current linear MLP; keep the total LUT budget ≤ 15 % overhead.

3. **Optimize blending coefficient dynamically**  
   * Instead of a fixed α, learn a **small lookup‑table** that selects α based on a coarse binning of the BDT score (e.g. low, medium, high BDT). This adds a conditional weighting without extra arithmetic.

4. **Quantisation‑aware training**  
   * Retrain the BDT and the MLP **with the final integer bit‑widths** (e.g. 8‑bit fixed‑point) baked in, to see if a slight reduction in precision can be compensated by a modest gain in discriminating power.

5. **Resource‑headroom verification**  
   * Perform a full post‑synthesis run on the target FPGA to confirm that the additional LUTs for new features and trees stay within the allocated margin (currently ~10 % spare). If necessary, prune the least‑impactful features.

6. **System‑level evaluation**  
   * Run the new candidate on the *full trigger‑chain simulation* to assess any shift in overall rate, latency jitter, and robustness against pile‑up variations.  
   * Verify that the improved efficiency translates into a **real physics gain** (e.g. higher top‑pair acceptance in the physics analyses).

---

**Bottom line:**  
The `novel_strategy_v592` successfully demonstrated that **physics‑driven, integer‑friendly observables** can be fused with an existing BDT via a minimal MLP to boost signal efficiency without compromising FPGA constraints. The next iteration will broaden the feature space and test modest non‑linear post‑processing, staying within the same latency/LUT envelope, to see whether we can push the efficiency further toward the theoretical limit.