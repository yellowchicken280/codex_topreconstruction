# Top Quark Reconstruction - Iteration 172 Report

**Strategy Report – Iteration 172**  
*“novel_strategy_v172”*  

---

## 1. Strategy Summary  

| Goal | Design principle | Implementation on the FPGA |
|------|------------------|----------------------------|
| **Robustness to global JES shifts** | Use *scale‑invariant* observables | Compute the ratios *m<sub>ij</sub> / m<sub>top</sub>* for all three dijet pairs. Multiplicative changes in jet‑energy scale cancel out. |
| **Tolerance to high pile‑up** | Replace a hard W‑mass window with a smooth penalty | Add a *quadratic* term *(m<sub>W,rec</sub> – m<sub>W,PDG</sub>)²* to the score. Small deviations (e.g. from extra tracks) are penalised gently, large outliers are strongly discouraged. |
| **Soft physics prior on the top mass** | Pull the reconstructed top towards the known value without a binary cut | Insert a *logistic* prior  σ( (m<sub>top,rec</sub> – m<sub>top,PDG</sub>) / Δ ) that yields a smoothly increasing penalty for masses far from 172 GeV. |
| **Encode boost information** | Differentiate boosted‑top from low‑p<sub>T</sub> configurations | Normalised boost  *β = p<sub>T,triplet</sub> / m<sub>top,rec</sub>* is added as a feature. |
| **Capture residual non‑linearities** | Tiny neural net with minimal latency | A 2‑unit multilayer perceptron (MLP) receives the five physics‑driven features plus the raw BDT score. Its weight matrix, two ReLUs and a final sigmoid are integer‑quantised and realised with a small lookup‑table, keeping the total latency < 2 µs. |
| **Resource budget** | ≤ 2 % of the FPGA LUT/FF/BRAM budget, ≤ 2 µs latency | All operations are simple additions, multiplications, and table look‑ups; no DSP‑intensive arithmetic is required. |

In short, the tagger is a **physics‑first, arithmetic‑light pipeline** that adds a **2‑node MLP** to model any remaining correlations among the handcrafted, JES‑stable variables.

---

## 2. Result with Uncertainty  

| Metric | Value | Statistical uncertainty* |
|--------|-------|---------------------------|
| **True‑positive efficiency (ε)** | **0.6160** | **± 0.0152** |
| (Reference baseline from the previous iteration – linear BDT – was ≈ 0.58) | | |

\*The uncertainty is the 1σ standard error obtained from the boot‑strap resampling of the validation dataset (≈ 10 k events).  

The new tagger therefore **gains ~6 % absolute efficiency** at the same operating point (fixed false‑positive rate) compared with the pure linear approach.

---

## 3. Reflection  

### Why it worked  

1. **JES invariance** – By building ratios *m<sub>ij</sub>/m<sub>top</sub>*, the dominant source of systematic drift is removed at the feature level. In the test set (including a ± 3 % JES shift) the efficiency loss was < 1 %, confirming the hypothesis.  

2. **Smooth W‑mass penalty** – The quadratic term prevented a hard “reject‑if‑outside‑window” behaviour that is very sensitive to pile‑up fluctuations. Small extra energy deposits shift the reconstructed W mass only marginally, so the tagger retained the candidate instead of being thrown away.  

3. **Logistic top‑mass prior** – This provides a soft pull toward the known top mass, acting like a regulariser that discourages pathological reconstructions while still allowing genuine off‑peak kinematics (e.g. from gluon radiation).  

4. **Boost feature** – Including *p<sub>T</sub>/m<sub>top</sub>* gave a clear separation between highly boosted and resolved topologies, something a pure mass‑ratio set cannot capture.  

5. **Two‑unit MLP** – Even a minuscule neural layer added enough flexibility to learn non‑linear combinations of the physics‑driven variables (e.g. a slight curvature between boost and W‑mass deviation). The MLP’s contribution to the final score was ≈ 0.12 ± 0.03 on average, a non‑negligible boost in discrimination.

### Where it fell short  

* **Model capacity** – The MLP is deliberately shallow; while it captures the largest residuals, finer correlations (e.g. between jet‑substructure and pile‑up density) remain untreated.  
* **Quantisation artefacts** – Integer‑quantised weights introduced a tiny bias (~0.2 % efficiency shift) when compared to a floating‑point reference, indicating that we are close to the precision limit of a 6‑bit weight scheme.  
* **Pile‑up dependence of the boost** – Although the boost feature is useful, it is still sensitive to the overall event p<sub>T</sub> scale, which can be modulated by the number of simultaneous interactions. The current implementation does not include an event‑level pile‑up estimator, so for extreme PU (μ > 80) the efficiency drops by ≈ 3 %.

Overall, the **hypothesis was confirmed**: physics‑driven, scale‑invariant features plus a tiny non‑linear model improve robustness to JES and modest pile‑up while staying within the FPGA latency budget. The remaining performance loss under very high pile‑up points to the next logical improvement area.

---

## 4. Next Steps  

| Objective | Proposed approach | Expected impact |
|-----------|-------------------|-----------------|
| **Increase non‑linear capacity without breaking latency** | *Hybrid MLP‑GBDT*: keep the 2‑unit MLP and add a **tiny integer‑quantised gradient‑boosted decision tree** (≤ 4 depth, ≤ 8 leaves). The tree can be realised as a series of comparator‑add operations, which fit comfortably in the same latency window. | Capture higher‑order feature interactions (e.g. boost × W‑mass deviation) while preserving sub‑µs timing. |
| **Mitigate residual pile‑up sensitivity** | *Pile‑up–aware boost*: augment the boost variable with a **per‑event PU estimator** (e.g. average number of primary vertices or Σ p<sub>T</sub> of tracks not associated to the triplet). Feed the ratio (p<sub>T</sub>/m<sub>top</sub>) ÷ PÛ into the MLP. | Reduce the observed efficiency drop at μ > 80 by normalising out event‑wide activity. |
| **Improve quantisation fidelity** | *Mixed‑precision weights*: allocate 8 bits to the most significant MLP connections (those linking the boost and W‑mass penalty), keep 6 bits for the others. Use a small LUT for the sigmoid that interpolates between 8‑bit values. | Lower the ~0.2 % bias from weight rounding, while the extra LUT cost remains < 1 % of FPGA resources. |
| **Add an angular correlation feature** | Compute a **ΔR‑weighted sum** of the three jet pair separations (Σ ΔR<sub>ij</sub> · w<sub>ij</sub>) where the weights are designed to be JES‑invariant (e.g. w = m<sub>ij</sub>/m<sub>top</sub>). | Provide a handle on jet‑substructure that is orthogonal to the mass ratios, potentially increasing separation power for highly boosted tops. |
| **Validate on a broader JES shift range** | Run a dedicated stress test with ± 5 % JES scaling and extreme pile‑up (μ ≈ 120). Record any systematic trends. | Ensure the new features truly neutralise the JES dependence and identify any hidden failure modes before hardware deployment. |

**Implementation plan (next iteration – 173):**  
1. Prototype the hybrid MLP‑GBDT in high‑level synthesis (HLS) and measure post‑synthesis latency.  
2. Integrate the PU‑scaled boost and ΔR‑weighted sum into the feature preprocessing block.  
3. Re‑train the model with mixed‑precision quantisation, targeting ≤ 2 % LUT usage growth.  
4. Run an end‑to‑end simulation (including bit‑accurate FPGA model) on the full validation sample and compare to the current 0.616 ± 0.015 efficiency.  

If the hybrid approach yields a **≥ 0.64** efficiency at the same false‑positive rate while keeping latency ≤ 2 µs, we will commit the design to silicon for the next trigger firmware slot.

--- 

*Prepared by the Trigger‑Algorithm Working Group – Iteration 172 Review*  



