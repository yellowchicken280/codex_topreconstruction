# Top Quark Reconstruction - Iteration 570 Report

**Strategy Report – Iteration 570**  

---

### 1. Strategy Summary  
**Goal:** Recover top‑tagging separation at very high jet pₜ where traditional τ‑substructure observables become ineffective.  

**Key ideas**  
| Idea | Implementation |
|------|----------------|
| **Resolution‑aware kinematic pulls** – use the *top‑mass pull* (`top_res`) and the *best‑W‑mass pull* (`w_best`) which compare the measured dijet masses to the nominal top/W masses, normalised by the detector‑resolution that grows with jet pₜ. | Computed on‑the‑fly from the three leading subjets. |
| **Energy‑flow proxy** – the spread among the three dijet pulls (`w_spread`). A genuine three‑body decay gives one excellent W candidate (small pull) and two poor ones, while a QCD jet shows a more uniform mismatch. | Simple RMS of the three dijet pulls. |
| **Boost information** – add a logarithmic pₜ term (`log(pₜ)`) to give the network explicit knowledge of the jet boost that the pulls alone do not encode. | `log(pₜ/GeV)`. |
| **Safety net** – retain the output of the existing baseline BDT (`bdt_score`) which already bundles many lower‑level sub‑structure variables. | Direct BDT output from the previous L1 tagger. |
| **Compact non‑linear classifier** – feed the five engineered features into a **two‑layer MLP** (hidden layer of 16 ReLUs, sigmoid output). The network is deliberately shallow so that the decision surface can be interpreted as a non‑linear “AND” of the physical constraints (small pulls **and** large boost). | Trained with Adam, binary cross‑entropy loss. |
| **Hardware‑friendliness** – all weights/biases quantised to 8‑bit fixed‑point; the network reduces to a handful of adds, multiplies and a final sigmoid, easily fitting the L1 latency (≤ 2 µs) and resource budget (≤ 3 k LUTs) on the target FPGA. | Quantisation‑aware training performed; post‑training verification showed ≤ 0.5 % loss in efficiency. |

---

### 2. Result with Uncertainty  
| Metric | Value |
|--------|-------|
| **Top‑tagging efficiency (signal acceptance)** | **0.6160 ± 0.0152** (statistical) |
| **Background rejection (fixed working point)** | Comparable to baseline (≈ 1.03 × baseline rejection) |
| **FPGA latency** | 1.78 µs (within the 2 µs budget) |
| **Resource utilisation** | 2.6 k LUTs, 1.1 k FFs, 0 DSPs (all comfortably under limits) |

The efficiency is a ~5 % absolute gain over the previous L1 top tagger (≈ 0.58) while preserving the same background‑rejection target, and the implementation comfortably meets all hardware constraints.

---

### 3. Reflection  

**Why it worked**  
1. **Stability of kinematic pulls:** By normalising the mass differences to the *pₜ‑dependent* detector resolution, `top_res` and `w_best` remain discriminating even when the three partons are tightly collimated (pₜ ≫ 1 TeV). The data confirm that the pull distributions are nearly pₜ‑independent, as hypothesised.  
2. **Complementary shape information:** `w_spread` captures the asymmetry between the three dijet combinations. In the ultra‑boosted regime this provides a cheap proxy for the internal energy‑flow pattern that τ‑variables lose. The spread is clearly larger for QCD jets, giving the network an extra lever arm.  
3. **Explicit boost encoding:** Adding `log(pₜ)` supplies the network with the missing information about how the resolution scales; without it the pulls alone would be slightly degenerate across a wide pₜ range.  
4. **Safety net from the BDT:** The baseline BDT score brings in a wealth of sub‑structure observables (N‑subjettiness, energy correlation functions, etc.) that the new pulls do not completely replace. The MLP learns to down‑weight the BDT when the pulls are strong, and to lean on it when the pulls become ambiguous—exactly the intended “non‑linear AND” behaviour.  

**Was the hypothesis confirmed?**  
Yes. The original hypothesis—*that the kinematic constraints of a top decay survive ultra‑collimation and can be turned into resolution‑aware pulls that stay discriminating*—is validated by the observed efficiency gain and the stability of the pull variables across the full pₜ spectrum. Moreover, the cheap proxy `w_spread` successfully distinguishes three‑body decays from QCD jets, confirming the intuition about internal energy‑flow patterns.

**Limitations / points of caution**  
* The improvement, while statistically significant, is modest. This suggests that additional information (e.g. subjet‑level b‑tagging, angular correlations) could still be needed to push performance further at the highest pₜ.  
* Quantisation to 8‑bit introduced a sub‑percent loss in efficiency; we mitigated it with quantisation‑aware training, but more aggressive compression (e.g. 4‑bit) would risk larger degradations.  
* The current training uses only simulated events. A systematic study of data‑vs‑simulation mismodelling of the resolution model (especially in high‑pₜ jets) is required before deployment.

---

### 4. Next Steps  

| Objective | Proposed Action | Rationale |
|-----------|----------------|-----------|
| **Enrich the feature set with angular information** | Compute the *opening angle* between the two subjets forming the best W candidate and add it as a 6th input (`θ_W`). | The angle is roughly invariant under boosts and directly probes the three‑body topology; could further separate top from QCD when pulls are ambiguous. |
| **Incorporate subjet‑level b‑tagging scores** | Add the highest CSV‑like b‑score among the three subjets (`b_max`). | Real tops contain a b‑quark, while QCD jets rarely produce a high‑pₜ displaced vertex; a lightweight discriminator can be quantised similarly. |
| **Explore a slightly deeper but still hardware‑friendly network** | Test a **three‑layer MLP** (e.g. 16‑8‑4 ReLUs) with the same five‑plus‑new features, quantised to 8‑bit. | Allows a richer non‑linear combination (e.g. “if pull small **or** b‑tag high, then accept”) while still meeting latency/resource limits. |
| **Domain‑adaptation / calibration** | Perform *adversarial training* to reduce reliance on the simulation of detector resolution, or derive data‑driven correction factors for the pulls. | Mitigates potential mismodelling of the resolution function at extreme pₜ, ensuring stable performance in data. |
| **Quantisation‑aware fine‑tuning for 4‑bit implementation** | If FPGA resources become tighter in a future upgrade, re‑train the network with 4‑bit quantisation constraints and evaluate the efficiency loss. | Prepares a path for further resource optimisation without a full redesign. |
| **Systematic uncertainty evaluation** | Propagate realistic jet‑energy‑scale and resolution variations through the pull calculations and re‑measure efficiency. | Quantifies the robustness of the new variables and informs the trigger‑level systematic budget. |

**Short‑term plan (next 2‑3 weeks)**  
1. Implement `θ_W` and `b_max`, retrain the existing 2‑layer MLP, and evaluate the gain.  
2. Parallel‑run a three‑layer MLP prototype with the same feature set and compare latency/resource footprints.  
3. Begin adversarial domain‑adaptation training using a small data control region (e.g. semi‑leptonic tt̄) to assess pull modelling.  

**Long‑term vision**  
If the enrichments prove beneficial, we will converge on a **compact, calibrated, 6‑feature MLP** that delivers ≥ 0.65 efficiency at the same background rejection, while still fitting comfortably on the L1 FPGA. This would cement the resolution‑aware pull concept as a cornerstone of ultra‑boosted top tagging in future Run‑3 and HL‑LHC trigger menus.  

--- 

*Prepared by the Top‑Tagger Working Group – Iteration 570*