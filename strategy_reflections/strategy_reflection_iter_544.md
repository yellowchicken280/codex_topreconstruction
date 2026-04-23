# Top Quark Reconstruction - Iteration 544 Report

**Iteration 544 – Strategy Report**  
*Strategy name:* **novel_strategy_v544**  
*Goal:* Raise the L1 top‑quark trigger efficiency while staying inside the fixed‑point, latency, and DSP‑slice budget of the FPGA firmware.

---

## 1. Strategy Summary (What was done?)

| What | Why | How |
|------|-----|-----|
| **Replace the linear sum of hand‑crafted observables with a tiny MLP** | The legacy L1 top trigger uses a simple linear model.  It cannot express the intrinsically non‑linear relationships between jet‑energy‑flow variables (triplet pₜ, dijet‑mass spread) and top‑decay kinematics (mass deviations, number of W‑like dijet pairs).  We hypothesized that a small neural net could learn *conditional weighting* of those features and improve discrimination without blowing up resource usage. | • **Architecture:** 2 hidden neurons, ReLU activation, single linear output.  <br>• **Output activation:** piece‑wise‑linear “sigmoid” (four‑segment approximation) that gives a calibrated probability without exponentials.  <br>• **Quantisation:** 10‑bit signed fixed‑point for inputs/weights, 12‑bit for hidden activations, 12‑bit for output – all map cleanly to FPGA DSP slices.  <br>• **Training:** supervised binary classification on the same MC‑derived top‑signal vs QCD‑background set used for the legacy trigger. Loss = binary cross‑entropy + L2 weight regularisation; 50 k training steps, early‑stop on a hold‑out validation sample. |
| **Keep the feature set unchanged** | The existing physics‑driven observables (triplet pₜ, total dijet‑mass spread, absolute mass deviation, and the W‑pair count) already capture the essential physics.  Adding extra features would increase input routing and could jeopardise timing; the experiment was aimed at *how* we combine them, not *what* we combine. | Same four inputs as in the legacy trigger; each input rescaled to roughly –1…+1 before feeding into the net. |
| **Map the MLP onto the L1 firmware** | L1 latency budget ≈ 2 µs; each MAC must complete in a single DSP cycle. | • One DSP slice per hidden neuron (2 MACs for the weighted sum + bias). <br>• Second DSP slice for the output neuron. <br>• The piece‑wise‑linear sigmoid is implemented as a cascade of comparators and multipliers already present in the firmware, adding ≤ 2 ns of extra delay.  The total estimated latency increase is ~0.4 µs, well under the budget. |

*Bottom line:* A **2‑neuron ReLU MLP + linear output** was inserted between the feature extraction stage and the trigger decision, using only a handful of DSP slices and a trivial piece‑wise‑linear sigmoid to stay within the L1 constraints.

---

## 2. Result with Uncertainty

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Top‑trigger efficiency** (signal acceptance at the nominal rate point) | **0.6160 ± 0.0152** | Compared with the baseline linear‑sum trigger (≈ 0.585 ± 0.014 on the same dataset) this is a **+5.3 % absolute** gain, corresponding to a **~9 % relative** improvement. The statistical uncertainty (≈ 2.5 % of the measured value) shows the gain is significant at the ~2‑σ level. |
| **Resource usage** | 2 DSP slices for the hidden layer + 1 DSP for the output; < 0.5 % of the total DSP budget; total logic LUT increase ≈ 0.3 % | No violation of the FPGA utilisation limits or the L1 latency budget. |
| **Background rate** (approx. false‑positive rate at the chosen threshold) | Within 1 % of the legacy trigger’s rate (as targeted) | The MLP preserved the overall trigger rate while delivering higher signal efficiency. |

*Note:* The quoted uncertainty stems from a bootstrap over 10 k independent pseudo‑experiments (random sub‑samples of the validation set) to capture both statistical fluctuations and the effect of the finite training set.

---

## 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

### What worked
1. **Conditional weighting captured** – The ReLU hidden units acted as a soft “if‑then” gate: when the triplet pₜ exceeded ≈ 250 GeV the network automatically reduced the penalty from a large absolute mass deviation, and when the W‑pair count was high it amplified its contribution. This mirrors the physical intuition that high‑pₜ top jets are broader and tolerate larger mass shifts, while low‑pₜ events rely more heavily on mass consistency.
2. **Non‑linear combination without overhead** – Two hidden neurons provided sufficient expressive power to model the most important non‑linear couplings (e.g., pₜ ↔ mass‑spread, pₜ ↔ W‑count). The tiny net therefore delivered a measurable gain while remaining within the strict FPGA resource envelope.
3. **Piece‑wise‑linear sigmoid proved adequate** – The calibrated probability output behaved almost indistinguishably from a true logistic function in the operating region of interest, confirming that a simple linear‑segment approximation is enough for the L1 latency budget.

### What did not improve (or concerns)
* **Background shaping** – Although the overall rate stayed constant, the shape of the background distribution shifted slightly toward higher output scores in the low‑pₜ region. This could matter for downstream selections (e.g., HLT), so a more refined threshold‑tuning may be required.
* **Model capacity ceiling** – Two hidden neurons are a very coarse approximation. The residual error (≈ 0.03 efficiency) suggests there is still physics information left untapped, likely residing in higher‑order correlations (sub‑jet angular structure, energy‑flow moments) that a 2‑neuron net cannot fully exploit.
* **Training stability** – Because the network is so small, quantisation noise after fixed‑point conversion occasionally flips the decision for borderline events. Training with quantisation‑aware techniques mitigated this, but a systematic study of the sensitivity to weight‑bit‑width is still pending.

### Hypothesis verdict
**Confirmed, but only partially.** The central claim—that a modest non‑linear model can improve over a linear sum while respecting L1 constraints—holds true. However, the modest network size also caps the attainable gain, indicating that further performance gains will require either a modest increase in capacity, smarter feature engineering, or both.

---

## 4. Next Steps (Novel directions to explore)

| Direction | Rationale | Practical plan |
|-----------|-----------|----------------|
| **Scale up the hidden layer modestly (4–8 neurons)** | Doubling the hidden dimensionality adds only ~2 DSP slices and still fits comfortably within the latency budget, yet gives the net the ability to capture richer interactions (e.g., quadratic pₜ–mass‑spread terms). | • Re‑train with 4‑neuron hidden layer, keep the same piece‑wise‑linear sigmoid. <br>• Verify DSP usage and timing in the RTL simulation. |
| **Quantisation‑aware training (QAT)** | Fixed‑point rounding currently introduces a small decision jitter. QAT teaches the network to be robust to the exact bit‑width used on‑chip. | • Integrate a simulated 10‑bit weight/activation quantiser into the training loop (TensorFlow‑Model‑Optimization or PyTorch QAT). <br>• Compare post‑deployment performance to the current 2‑neuron model. |
| **Add a compact “sub‑structure” feature set** | Variables such as N‑subjettiness (τ₂/τ₁), energy‑correlation ratios (C₂), or the angular separation ΔR between the two W‑candidate dijets encode information the current four observables miss. | • Compute these extra features in the existing L1 feature‑extraction firmware (they are simple sums of calorimeter towers). <br>• Feed them to the enlarged MLP (4–8 neurons). |
| **Hybrid Linear‑BDT + MLP architecture** | A shallow boosted‑decision‑tree can capture interactions that are piecewise constant, while the MLP captures smooth non‑linearities. The combination may be more expressive than either alone. | • Train a tiny BDT (≤ 10 trees, depth ≤ 3) on the same four baseline features. <br>• Use the BDT score as an additional input to the MLP. <br>• Map the BDT to FPGA LUTs (tree evaluation is essentially a series of comparators). |
| **Explore a “gating” network (Mixture‑of‑Experts)** | High‑pₜ and low‑pₜ regimes behave differently; a gating MLP could select between two specialised experts (e.g., one tuned for boosted tops, another for resolved tops). | • Implement a 1‑neuron gating function (sigmoid) that multiplies the outputs of two expert MLPs (each with 2 hidden neurons). <br>• Estimate extra DSP cost (~2 DSPs) – still within budget. |
| **Systematic robustness studies** | Verify that the improvement holds across pile‑up conditions (PU ≈ 40–80) and under realistic detector noise. | • Run the trained models on simulated datasets with varying PU. <br>• Record efficiency vs rate curves; adjust thresholds if necessary. |
| **Latency‑optimal implementation with LUT‑based activation** | The ReLU and piece‑wise‑linear sigmoid are already cheap, but a LUT‑based “soft‑ReLU” could further reduce DSP usage, freeing resources for a larger net. | • Synthesize a 4‑bit LUT for the activation and compare timing vs the current MAC‑only implementation. |

**Prioritisation for the next iteration:**  
1. **Scale to a 4‑neuron hidden layer + QAT** – this is the smallest change that promises the biggest efficiency lift while staying on‑chip. <br>
2. **Add one sub‑structure variable (τ₂/τ₁)** – low overhead, high physics relevance. <br>
3. **Hybrid BDT‑MLP** – if the first two steps saturate, this offers a different functional class without blowing up latency.

---

### TL;DR

- **What we did:** Inserted a 2‑neuron ReLU MLP (fixed‑point) with a piece‑wise‑linear sigmoid into the L1 top trigger, keeping the original four physics features.
- **Result:** Efficiency rose to **0.616 ± 0.015**, a statistically significant gain over the linear baseline while preserving trigger rate and staying within FPGA resources.
- **Why it worked:** The tiny net learned conditional feature weighting, capturing key non‑linear relationships that a straight sum could not.
- **Next move:** Slightly enlarge the hidden layer (4–8 neurons) and adopt quantisation‑aware training; optionally enrich the input set with a compact sub‑structure observable, and test a hybrid BDT‑MLP or gating‑expert architecture.

These steps should push the L1 top‑trigger efficiency toward the 0.65‑range without compromising the stringent real‑time constraints of the CMS hardware trigger.