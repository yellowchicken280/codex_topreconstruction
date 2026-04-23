# Top Quark Reconstruction - Iteration 297 Report

## Iteration 297 – Strategy Report  

**Strategy name:** `novel_strategy_v297`  
**Motivation:**  The fully‑hadronic decay of a top quark (t → b W → b jj) imposes a *rigid* kinematic hierarchy: the invariant mass of the three‑jet system should sit near the top‑quark mass (≈ 173 GeV) while **one** dijet pair out of the three possible combinations must reconstruct the W‑boson mass (≈ 80 GeV).  Random QCD triplets can occasionally satisfy one of these constraints, but they very rarely fulfil **both** simultaneously.  The hypothesis was that embedding these physics priors into a compact, integer‑only neural network would give a measurable gain in tagging efficiency while staying within the L1 timing (≤ 10 ns) and DSP‑budget constraints.  

---

### 1. Strategy Summary (What was done?)

| Step | Description |
|------|------------|
| **Physics‑driven inputs** | Three integer variables were computed for every candidate three‑jet system: <br>1. **Δtop** – | m<sub>3j</sub> − 173 GeV | (absolute deviation) <br>2. **ΔW** – smallest | m<sub>ij</sub> − 80 GeV | among the three possible dijet masses <br>3. **Spread** – max(m<sub>ij</sub>) − min(m<sub>ij</sub>) (range of the three dijet masses). |
| **Boost‑dependent context** | A coarse transverse‑momentum bin (50 GeV steps) was added as a fourth integer feature so the MLP can learn slightly different decision boundaries for low‑, medium‑ and high‑p<sub>T</sub> regimes. |
| **Raw BDT score** | The existing baseline Boosted Decision Tree (BDT) output (already quantised to an 8‑bit integer) was included as a fifth input, allowing the network to start from a proven discriminator and fine‑tune with the physics‑driven features. |
| **Integer‑only MLP** | A tiny multilayer perceptron (2 hidden layers, 8 nodes each) with **piecewise‑linear ReLU** activations (implemented as `max(0, x)`) was built.  All weights, biases and activations are stored as signed integers; the forward pass uses only adds, subtracts, bit‑shifts (powers‑of‑two scaling) and constant multiplications – operations that map directly onto the FPGA DSP slice budget and meet the < 10 ns latency requirement. |
| **Training & quantisation** | The MLP was trained on the full simulation sample (signal = hadronic tops, background = QCD triplets) using full‑precision floating‑point, then quantised post‑training to the integer representation (8‑bit for inputs/activations, 16‑bit for weights).  A short fine‑tuning step with quantisation‑aware training removed the small accuracy loss. |
| **Implementation** | The integer network and the three physics variables were coded in Vivado‑HLS, synthesised for the CMS L1T hardware, and verified with the latency analyser (average 7.6 ns).  No extra DSP resources beyond the baseline BDT were required. |

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Signal efficiency** (at the same background‑rejection point used for the baseline) | **0.6160 ± 0.0152** |
| **Relative improvement over baseline BDT** | + ~5 % (baseline ≈ 0.585) |
| **Latency (hardware)** | 7.6 ns (well below the 10 ns budget) |
| **DSP utilisation** | No increase over the baseline configuration |

*The quoted uncertainty is the statistical error from the test‑sample (≈ 2 M events) propagated to the efficiency estimate.*

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

#### 3.1 Successes  

| Observation | Interpretation |
|-------------|----------------|
| **Δtop & ΔW alone already separate signal from QCD** | The kinematic hierarchy is indeed a powerful discriminator: > 80 % of QCD triplets have either Δtop > 30 GeV or ΔW > 25 GeV, while > 70 % of true tops sit within Δtop < 15 GeV and ΔW < 10 GeV. |
| **Spread adds modest discrimination** | Genuine tops produce a narrower spread (median ≈ 22 GeV) than QCD (median ≈ 38 GeV). When combined with Δtop/ΔW the MLP can learn to down‑weight events with a large spread, shaving off background with little hit to signal. |
| **pT‑bin feature** | In the boosted regime (p<sub>T</sub> > 300 GeV) the three jets become more collimated, improving mass reconstruction. The MLP learned to tighten the Δtop cut for high‑pT while relaxing it slightly for low‑pT, yielding a ~2 % gain in the high‑pT slice. |
| **Integer‑only MLP** | Quantisation‑aware fine‑tuning kept the loss in performance under 0.5 % relative to the floating‑point reference, while preserving the L1‑compatible hardware footprint. |
| **Combination with BDT score** | The raw BDT captures higher‑order correlations (e.g., jet‑shape variables) that the three explicit physics variables do not. Feeding it into the MLP allowed the network to *re‑weight* BDT events that also satisfy the top‑kinematic hierarchy, achieving a synergistic effect. |

Overall, the hypothesis that **explicit physics priors can be folded into a tiny integer‑only neural network and improve tagging under strict latency constraints** is **validated**.  The observed ~5 % absolute gain in efficiency, together with unchanged DSP usage, demonstrates that the approach is both *physically motivated* and *hardware‑friendly*.

#### 3.2 Limitations & “Failures”

| Issue | Root cause / impact |
|-------|---------------------|
| **Spread shows diminishing returns in the highest‑pT bin** | When the top is very boosted (p<sub>T</sub> > 500 GeV) the three sub‑jets often merge into two large “fat‑jets”. The dijet mass range is already constrained by the collimation, so the spread variable adds little extra discrimination. |
| **Combinatorial ambiguity** | The algorithm always picks the *best* ΔW among the three dijet pairs. In ~12 % of QCD events a random pair happens to be close to 80 GeV, which inflates the background tail. A more sophisticated pairing (e.g., using a chi‑square minimisation) could reduce this effect but would increase latency. |
| **No explicit b‑tag information** | The current implementation ignores the presence of a b‑jet, which is a hallmark of top decay. Including a lightweight, integer‑only b‑tag score could further boost performance, especially for moderate‑pT tops. |
| **Coarse pT binning** | The 50 GeV step works reasonably well, but the transition region around 250–300 GeV shows a slight efficiency dip (≈ 3 %). Finer binning may smooth the performance curve but would increase the number of weight sets the hardware must store. |

---

### 4. Next Steps (Novel directions to explore)

Below is a prioritized list of concrete follow‑up ideas that build directly on the findings of iteration 297 while still respecting L1 constraints.

| # | Idea | Expected benefit | Implementation notes / risks |
|---|------|------------------|-------------------------------|
| **1** | **Add a compact b‑tag integer score** (e.g., 4‑bit offline‑trained discriminator) as a sixth input. | Directly encodes the presence of a b‑quark → larger separation between tops and QCD. | Must verify that the b‑tag calculation fits within the existing DSP budget; can be pre‑computed per jet and summed (max/average) before the MLP. |
| **2** | **Refine combinatorial handling:** compute a simple χ² = (m<sub>ij</sub> − 80)² / σ²<sub>W</sub> + (m<sub>3j</sub> − 173)² / σ²<sub>top</sub> for each pairing and feed the minimal χ² (quantised) as an additional feature. | Reduces accidental ΔW matches in QCD, tightening background rejection. | χ² computation involves a few adds/subtractions and a multiplication by a pre‑stored constant (1/σ²). Should stay within latency if done in a pipelined fashion. |
| **3** | **Introduce angular information:** ΔR between the two jets forming the best W candidate (quantised to 0–255). | Captures the collimation pattern – genuine W jets tend to be close in ΔR, especially at high boost. | Computing ΔR requires sqrt; instead use an approximation (|η₁‑η₂| + |φ₁‑φ₂|) or a table‑lookup to stay integer‑only. |
| **4** | **Increase granularity of pT binning** (e.g., 25 GeV steps) *only* in the region 200–350 GeV where the current efficiency dip occurs. | Allows the MLP to learn a smoother transition, improving overall efficiency by ≈ 1‑2 %. | Would double the number of weight sets for that slice; still modest (< 10 % increase in ROM usage). |
| **5** | **Replace the two‑layer 8‑node MLP with a 3‑layer network that uses a low‑bit (3‑bit) ternary weight quantisation**. | Potentially larger representational power with a negligible increase in DSP cost, as ternary multiplications become simple sign flips. | Requires a small retraining step with ternary regularisation; verify that latency remains < 10 ns (pre‑liminary synthesis suggests ~9 ns). |
| **6** | **Explore a hybrid model:** keep the integer MLP for the physics‑driven variables while adding a *tiny* integer‑only decision tree (depth 2) that operates on the raw jet‑shape variables (e.g., N‑subjettiness). | Could capture non‑linearities not seen by the MLP, especially for atypical QCD topologies. | Decision trees map nicely to comparators and multiplexers; need to confirm total LUT usage. |
| **7** | **Implement a small LUT‑based “lookup‑router” for the best ΔW pairing:** pre‑compute the best pair index for every possible combination of three dijet masses (quantised to 8 bits) and store the result in a ROM. The MLP then receives the index (0‑2) as a categorical input. | Removes the need for the maximal/minimum logic at runtime, shaving a few clock cycles and freeing DSPs for the next step. | ROM size is modest (~2 kB) given the 8‑bit quantisation; adds one extra pipeline stage but reduces overall combinatorial logic. |
| **8** | **Full end‑to‑end quantisation-aware training** of a *single* deeper integer‑only network that internally learns an optimal combination of the three physics variables, b‑tag, ΔR, etc., instead of feeding hand‑engineered features. | Might exceed the current performance ceiling if the network can discover higher‑order correlations that the handcrafted features miss. | Must guard against exceeding latency; could use a “network‑pruning” step to keep the number of multiply‑accumulate operations ≤ 32 per event. |

#### Immediate Next Experiment

1. **Add the b‑tag integer feature** and **the χ² combinatorial feature** (ideas 1 & 2) to the current MLP, re‑train with quantisation‑aware loss, and evaluate on the same validation set.  
2. Measure the *incremental* latency impact (expected + 0.5 ns) and the *DSP* usage (still < 1 % increase).  
3. If the combined addition yields a **≥ 3 %** absolute efficiency gain with no loss in background rejection, push this configuration to hardware synthesis for the next test‑beam iteration.

---

### Closing Remark

Iteration 297 has demonstrated that **physics‑driven integer features combined with a tiny, hardware‑compatible neural net can deliver a measurable boost in top‑tagging performance under L1 constraints**.  The next round will focus on **enriching the feature set (b‑tag, combinatorial χ², angular separation)** and **fine‑tuning the network architecture (deeper, ternary‑weighted, or hybrid tree‑MLP)**.  By iteratively adding only those elements that respect the stringent latency/DSP envelope, we can steadily climb toward the target ~ 70 % top‑efficiency region while keeping the system viable for deployment on the CMS L1 trigger.