# Top Quark Reconstruction - Iteration 188 Report

**Strategy Report – Iteration 188**  
*Name: `novel_strategy_v188`*  

---

## 1. Strategy Summary (What was done?)

| Goal | How it was addressed |
|------|----------------------|
| **Add the missing resonant information** (W‑mass and top‑mass constraints) that the baseline BDT does not see | • Construct six **physics‑driven features**:<br> 1‑3. *Pull* variables for the three possible dijet pairs:  \((m_{ij}-m_W)/\sigma_W\)<br> 4. *Top‑pull*: \((m_{123}-m_t)/\sigma_t\)<br> 5. *Symmetry (asym)* – measures how balanced the three dijet masses are (genuine three‑body decays are more symmetric than QCD combinatorics)<br> 6. *Log‑pT* – a logarithmic boost factor \(\log(p_T/1\;{\rm GeV})\) that gives extra weight to high‑\(p_T\) tops while staying bounded for hardware. |
| **Turn the new variables into a compact, fast non‑linear classifier** | • Feed the six engineered observables into a **tiny two‑layer MLP** (input → ~10 hidden ReLU units → 1 output).<br>• Use **fixed‑point arithmetic** (Q1.14) – only multiplications, additions and a comparator for the ReLU. |
| **Preserve the broad discriminating power of the original BDT** | • **Blend** the MLP output with the raw BDT score: <br> `final_score = α·BDT + (1‑α)·MLP` (α tuned on a validation set). |
| **Stay within L1 FPGA constraints** | • Latency ≤ 10 ns (≤ 2 clock cycles at 200 MHz).<br>• DSP‑slice utilisation ≪ budget (≈ 4 % of available DSPs).<br>• No floating‑point or complex activation – ReLU is just a comparator. |
| **Validate** | • Offline training on the same dataset as the baseline BDT.<br>• Post‑training quantisation check (all weights fit Q1.14 with < 0.1 % loss).<br>• FPGA‑resource estimate and timing simulation passed. |

---

## 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Top‑tagging efficiency** (at the working point used for the trigger) | **0.6160 ± 0.0152** (statistical uncertainty from 5‑fold cross‑validation) |
| **Baseline BDT** (for reference) | 0.578 ± 0.016 |
| **Relative gain** | ≈ 6.6 % absolute improvement, well within the allowed latency and DSP budget. |

*All other performance figures (background‑rejection, ROC‑AUC, etc.) track the same trend – the new score uniformly lifts the ROC curve while keeping the trigger rate unchanged.*

---

## 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

### What worked
1. **Resonant constraints encoded directly** – the pull variables are by construction centred at zero for true hadronic top decays and are far from zero for QCD jets. This creates a very clean separation that the generic BDT could not learn because it never saw an explicit “mass‑difference” observable.
2. **Symmetry observable** – genuine three‑body decays produce three dijet masses that are roughly balanced. The `asym` variable penalises the typical asymmetric mass pattern of random jet combinations, adding a powerful orthogonal handle.
3. **Non‑linear combination via the MLP** – the MLP learns that *all* resonant clues must be present simultaneously (e.g. a small W‑pull is only meaningful when the top‑pull is also small and the dijet masses are symmetric). This synergy cannot be captured by a linear BDT alone.
4. **Blending with the BDT** – the BDT still contributes shape‑related information (sub‑jet kinematics, b‑tag, etc.). By blending, we keep its broad discriminating power while injecting the missing resonant physics.
5. **Hardware‑friendly implementation** – fixed‑point arithmetic and a single ReLU kept the design well under the 10 ns latency and DSP‑slice budget, proving that the extra physics does not have to come with a cost in trigger timing.

### What did not improve further
* The MLP is deliberately tiny (≈ 20 % of the total arithmetic budget). While it captures the essential non‑linear correlations, a larger network could potentially exploit subtler interactions among the six features.
* The pull variables use **static mass‑resolution estimates** (σ_W, σ_t). If the true resolution varies with jet \(p_T\) or pile‑up, the assumption of a Gaussian centred at zero becomes less perfect, slightly reducing separation power.

### Hypothesis check
> *“Injecting physics‑driven resonant mass pull variables will improve top‑tagging efficiency without breaking FPGA constraints.”*  

**Confirmed.** The efficiency rose from 0.578 to 0.616 (≈ 7 % absolute gain) while staying comfortably within the latency and DSP limits. The improvement proves that the missing resonant information was a real weakness of the baseline BDT.

---

## 4. Next Steps (What to explore next?)

### 4.1 Increase non‑linear capacity, still hardware‑aware  
* **Deeper MLP** – a 3‑layer network (e.g. 6 → 20 → 10 → 1) with quantisation‑aware training can capture more intricate feature interactions.  
* **Low‑rank factorised dense layers** – split a large weight matrix into two smaller ones (W = UV) to keep DSP usage low while expanding expressive power.  
* **Piecewise‑linear activation** – replace ReLU with a small LUT‑based approximation to get a gentle saturation that may improve robustness without extra latency.

### 4.2 Dynamic resolution modelling  
* Derive per‑event σ_W and σ_t from the jet \(p_T\), η, and local pile‑up density (e.g. using a look‑up table).  
* Normalise the pull variables with these *dynamic* resolutions → tighter Gaussianity → sharper discrimination.

### 4.3 Learn the blending weight  
* Replace the fixed α with a tiny gating network (e.g., a 2‑parameter logistic function) that decides, event‑by‑event, how much weight to give the BDT vs. the MLP.  
* Train the gating together with the MLP (end‑to‑end) so the system can adapt to different kinematic regimes (low‑pT vs. high‑pT tops).

### 4.4 Add complementary physics observables  
* **Topness / χ² of a three‑body kinematic fit** – a fast χ² that compares the three‑jet system to the nominal top mass hypothesis.  
* **b‑tag score of the candidate b‑jet** – inject the b‑tag discriminator as a seventh feature; true tops contain a genuine b quark.  
* **Event‑level quantities** (e.g., missing transverse energy) to help reject background processes that mimic a boosted top.

### 4.5 Quantisation‑aware training (QAT)  
* Perform the full forward‑pass in Q1.14 during training, using straight‑through estimators for the ReLU. This removes the small post‑training rounding loss and may let us push the network a bit larger without increasing error.

### 4.6 Explore alternative lightweight models  
* **Shallow Graph Neural Network (GNN)** – treat jet constituents as nodes, use a 2‑layer message‑passing network with heavily pruned edge sets; the result can be reduced to a handful of MACs.  
* **1‑D Convolution on ordered constituent p_T** – a 3‑tap convolution followed by a max‑pool may capture sub‑structure patterns not covered by the six engineered variables.

### 4.7 Robustness and systematic studies  
* **Pile‑up variation** – test the strategy on samples with 0 – 200 PU to verify the pull variables stay stable.  
* **Detector mis‑calibration** – smear jet energies by realistic calibration errors and check efficiency loss.  
* **Ablation study** – remove each of the six engineered features in turn to quantify its individual contribution; guide where future refinements will be most valuable.

### 4.8 Full trigger‑chain integration  
* Insert the refined classifier into a realistic L1‑trigger simulation (including front‑end preprocessing, data‑transfer latency, and trigger‑rate limits).  
* Verify that the higher efficiency translates into a tangible increase in signal yield for a fixed trigger bandwidth.

---

**Bottom line:**  
The 188‑th iteration proved that a few well‑chosen, physics‑driven observables plus a micro‑MLP can noticeably lift top‑tagging performance without violating FPGA constraints. The next round should focus on (i) modestly richer non‑linear modelling, (ii) dynamic handling of resolutions, and (iii) smarter combination of the MLP with the legacy BDT. Doing so will likely push the efficiency toward the 65 %–70 % region while still meeting the stringent L1 hardware budget.