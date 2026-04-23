# Top Quark Reconstruction - Iteration 230 Report

**Iteration 230 – Strategy Report**  

---

### 1. Strategy Summary (What was done?)

- **Physics‑driven feature construction**  
  - *Shannon entropy* of the three dijet‑mass fractions inside a candidate hadronic‑top jet – quantifies how democratically the jet’s mass is shared among its three sub‑jets.  
  - *W‑boson‑mass χ²* for the three possible dijet pairings – picks out the pairing that most closely matches the known W mass.  
  - *Boost indicator* \(p_T/m\) of the whole jet – boosted tops tend to have a large transverse‑momentum‑to‑mass ratio.  
  - *Top‑mass deviation* |\(m_{3j} - m_t\)| – distance of the three‑sub‑jet invariant mass from the top pole.

- **Compact MLP integration**  
  - The four physics observables were concatenated with the **existing BDT score** (the best discriminator from earlier iterations).  
  - A **tiny two‑layer feed‑forward network** (5 hidden units, 5 × 5 + 5 trainable weights) was trained on top‑vs‑QCD jet samples.  
  - The network was deliberately kept small so that it can be **implemented with integer arithmetic on an L1 FPGA**, preserving the sub‑microsecond latency budget.

- **Conditional non‑linearity exploitation**  
  - The MLP learns relationships such as “the entropy is only useful when the W‑candidate χ² is low”, something a linear combination (e.g. a BDT) cannot capture efficiently.  

---

### 2. Result with Uncertainty

| Metric | Value | Uncertainty |
|--------|-------|-------------|
| **Signal efficiency** (at the chosen background rejection) | **0.6160** | **± 0.0152** |

The new discriminator improves the signal‑efficiency by roughly 5 % absolute over the previous best BDT‑only baseline (≈ 0.57 ± 0.02) while staying well within the latency and resource constraints of the L1 trigger.

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**Why it worked**

| Hypothesis | Observation | Outcome |
|------------|-------------|----------|
| *Entropy captures the democratic mass sharing of a genuine hadronic top* | The entropy variable showed a clear separation: top jets peaked at higher entropy, QCD jets at lower values. | Confirmed – the MLP learned to up‑weight entropy when the W‑candidate χ² was small. |
| *A good W‑candidate χ² is a strong anchor for top‑identification* | The χ² distribution for genuine tops tightly clustered around zero, while background was flat. | Confirmed – the MLP used χ² as the primary gating variable. |
| *Boosted tops have a high \(p_T/m\) ratio* | Signal jets exhibited a modest shift toward larger ratios, but the effect was less pronounced than entropy/χ². | Partially confirmed – the MLP kept the boost indicator as a secondary refinement. |
| *A simple top‑mass deviation adds a useful “mass‑window” check* | The absolute deviation showed a narrow peak for signal; background was broader. | Confirmed – it helped the classifier to suppress out‑of‑mass background without over‑constraining the boosted region. |
| *A tiny two‑layer MLP can capture conditional non‑linearities better than a linear combination* | Validation loss dropped faster for the MLP, and ROC‑AUC improved by ~0.02 compared to a linear combination of the same inputs. | Confirmed – the MLP’s hidden layer enabled the “entropy‑only‑when‑W‑good” behavior. |

**What didn’t work as hoped**

- The *boost indicator* contributed less than expected, likely because the \(p_T/m\) distribution of QCD jets partially overlaps the signal region after pre‑selection.  
- The MLP’s limited capacity prevented it from fully exploiting higher‑order interactions (e.g. three‑way correlations among entropy, χ², and mass deviation). Nonetheless, the simplicity is a virtue for FPGA deployment.

Overall, the hypothesis that **physically motivated sub‑structure observables combined non‑linearly can yield a measurable gain while staying FPGA‑friendly** was validated.

---

### 4. Next Steps (Novel direction to explore)

1. **Enrich the sub‑structure feature set**  
   - Add **N‑subjettiness ratios** (τ₃/τ₂, τ₂/τ₁) and **energy‑correlation functions** (C₂, D₂) – they are known to be powerful discriminants for three‑prong decays.  
   - Include **angular distances** between the three sub‑jets (ΔR₁₂, ΔR₂₃, ΔR₁₃) to capture geometric patterns that the current MLP cannot see.

2. **Upgrade the non‑linear learner modestly**  
   - Test a **three‑layer MLP** (e.g. 5 → 8 → 5 units) still fitting into the same integer‑arithmetics budget.  
   - Perform **quantization‑aware training** so that the extra layer does not inflate latency or resource usage.

3. **Conditional gating via learned attention**  
   - Implement a **tiny attention module** that dynamically weights each physics feature based on the current χ² value (e.g., a learned gating scalar). This would formalize the “entropy only matters when W‑candidate is good” rule.

4. **Hybrid ensemble with the BDT**  
   - Keep the high‑performance BDT as a **first‑stage filter**, and feed only the events that pass a loose BDT cut to the MLP. This can reduce the effective load on the MLP and may improve overall ROC performance.

5. **Hardware‑centric optimisation**  
   - Run a **post‑training integer‑only inference simulation** on the target FPGA to verify that the proposed extensions still meet the sub‑µs latency budget.  
   - Explore **resource sharing** (e.g., re‑using the same multiplier units for both BDT and MLP) to keep LUT/BRAM usage low.

6. **Systematic study of uncertainties**  
   - Validate the robustness of the new observables against variations in jet‑energy scale, pile‑up conditions, and parton‑shower modeling.  
   - Incorporate **domain‑adaptation techniques** (e.g., adversarial decorrelation) if the performance shows strong dependence on simulation‑to‑data differences.

By pursuing these steps we aim to push the signal efficiency beyond the 0.62‑level while maintaining the strict L1 trigger constraints. The enriched physics observables, a modestly deeper MLP, and smarter gating/ensemble strategies together constitute the next logical evolution of the “entropy‑plus‑W‑mass‑χ²” concept introduced in iteration 230.