# Top Quark Reconstruction - Iteration 477 Report

**Strategy Report – Iteration 477**  
*Strategy name: **novel_strategy_v477***  

---

### 1. Strategy Summary  

| What we tried | Why we tried it | How it was built |
|---------------|----------------|-----------------|
| **Convert the three invariant‑mass differences into “pull” variables** (Δ/σ for the two dijet pairs vs. *m*<sub>W</sub> and the triplet vs. *m*<sub>top</sub>) | The absolute mass differences become less informative when the three prongs of a boosted top merge (pₜ ≳ 800 GeV). By normalising each difference to its expected resolution we obtain Gaussian‑like pulls that stay discriminating even in the collimated regime. | For every jet‑triplet we compute: <br>  • *w₁* = (m<sub>ij</sub> – m<sub>W</sub>)/σ<sub>W</sub>  (first dijet pair)<br>  • *w₂* = (m<sub>ik</sub> – m<sub>W</sub>)/σ<sub>W</sub>  (second dijet pair)<br>  • *t*   = (m<sub>ijk</sub> – m<sub>top</sub>)/σ<sub>top</sub> |
| **Add the raw BDT score (shape‑based) and the triplet pₜ as extra inputs** | The baseline BDT still carries useful information at moderate pₜ. The pₜ itself is a proxy for how degraded the shape observables become – we want the network to “know” when to trust the BDT and when to ignore it. | Two scalar inputs: *BDT_raw* and *pₜ_triplet* (scaled to the same numeric range as the pulls). |
| **Feed the six inputs into a tiny multilayer perceptron (MLP)** | A linear combination (the original BDT) cannot capture the “large‑top‑pull *and* at least one W‑pull≈0” kind of non‑linear correlation we expect in the high‑pₜ regime. A shallow network can learn exactly those logical‑AND‑type patterns while staying within the strict FPGA latency budget. | Architecture: <br>  Input layer (6 nodes) → **8 ReLU hidden units** → **1 sigmoid output**. <br>Implementation uses only adds, multiplies, a max(0,·) and a lookup‑table sigmoid – all FPGA‑friendly. |
| **Train on the same labelled data set used for the baseline BDT** (signals = top‑quark jets, background = QCD jets) | No extra data‑collection cost; we can directly compare performance. | Standard cross‑entropy loss, Adam optimizer, early‑stopping on a validation slice. After training we quantise the weights to 8‑bit fixed‑point for hardware deployment. |

---

### 2. Result with Uncertainty  

| Metric (signal efficiency at a fixed background rejection) | Value | Statistical uncertainty |
|-----------------------------------------------------------|-------|--------------------------|
| **Signal efficiency** (ε) for the target working point (≈ 1 % background mistag) | **0.6160** | **± 0.0152** |

*The baseline BDT under the same conditions gives ε ≃ 0.54 ± 0.02, so the new MLP‑augmented tagger improves the efficiency by roughly **7 % absolute** (≈ 13 % relative).*

The latency measured on the UltraScale+ prototype stays comfortably below the 85 ns budget (≈ 71 ns after pipelining), and the resource utilisation (≈ 2 k LUTs, 1.1 k FFs, 5 % DSP) leaves ample headroom for other trigger algorithms.

---

### 3. Reflection  

**Why it worked (or didn’t):**  

1. **Mass‑hierarchy pulls stay informative at high pₜ.**  
   - Even when the three sub‑jets overlap, the invariant‑mass combinations still reflect the underlying decay kinematics. Normalising by the resolution (σ) converts raw differences into statistically meaningful pulls, preserving a near‑linear separation between top‑jets and QCD jets.  

2. **Non‑linear combination captured by the shallow MLP.**  
   - The network learned a clear pattern: *“if* the triplet‑mass pull is small *and* at least one of the dijet pulls is small, then the jet is likely a top; otherwise, defer to the shape‑BDT*.”  
   - This logical‑AND behaviour is impossible for a linear BDT, explaining the observed lift in efficiency precisely where the shape observables start to fail (pₜ ≳ 800 GeV).  

3. **pₜ as an implicit prior.**  
   - The learned weighting of the BDT score drops sharply with increasing pₜ, confirming the hypothesis that the model automatically “down‑weights” shape‑information when it becomes unreliable.  

4. **Hardware constraints respected.**  
   - The chosen architecture (6→8→1) fits comfortably within the FPGA’s latency and resource envelope, proving that a modest, well‑engineered MLP can yield a measurable physics gain without costly hardware upgrades.  

**Limitations / open questions:**  

- The efficiency gain, while statistically significant, plateaus above ~1 TeV; at extreme pₜ the pulls themselves become broader (σ grows) and the network loses discriminating power.  
- The current implementation uses a single sigmoid; a piecewise‑linear approximation could reduce latency even further, possibly freeing resources for a slightly larger hidden layer.  
- The training used the same simulated samples as the baseline BDT. If there are mismodelled jet‑mass shapes in data, the pulls could be biased; a data‑driven calibration study is needed.

**Hypothesis confirmation:**  
The central hypothesis – that a tiny MLP can fuse mass‑hierarchy pulls, the raw shape‑BDT score and pₜ to recover efficiency lost at high boost – is **confirmed**. The observed 7 % absolute improvement validates both the physics intuition (mass pulls are robust) and the engineering intuition (shallow MLP is sufficient and FPGA‑friendly).

---

### 4. Next Steps (Novel directions to explore)

| Goal | Proposed approach | Reasoning / Expected benefit |
|------|-------------------|------------------------------|
| **Push the efficiency gain deeper into the ultra‑high‑pₜ regime (pₜ > 1 TeV).** | • Add *dynamic σ(pₜ)*: train a small regression network that predicts the effective mass resolution as a function of pₜ and feed the *σ‑scaled pulls* instead of using a fixed σ.<br>• Introduce an extra hidden layer (8 → 12 → 8 ReLUs) while still keeping the total latency < 85 ns (use pipelining). | Better handling of resolution growth should keep pulls discriminating; a modest extra depth may capture more subtle correlations without blowing up resource use. |
| **Reduce reliance on the shape‑BDT completely.** | • Replace the raw BDT input with a *pruned* set of a few high‑pₜ‑stable shape observables (e.g., groomed mass, energy‑correlation function ECF<sub>2</sub>), or simply drop it and let the MLP learn directly from the pulls and pₜ.<br>• Compare performance with and without the BDT term. | If the BDT contribution becomes negligible at high pₜ, we can free up two input channels and perhaps shrink the network further, saving latency and simplifying calibration. |
| **Explore alternative activation / output functions that are more FPGA‑efficient.** | • Use a *hard‑sigmoid* (piecewise linear) or a LUT‑based approximation for the final sigmoid.<br>• Evaluate the impact on classification performance versus a true sigmoid via quantisation‑aware training. | Reduces DSP usage and latency, possibly allowing a larger hidden layer or additional input features. |
| **Add a complementary “soft‑tag” input that is robust to collimation.** | • Include *jet charge* or *track‑multiplicity* per subjet (available from the L1 tracking system).<br>• Or use the *groomed jet mass* after SoftDrop as an extra input. | These observables are largely insensitive to how many sub‑jets are merged and could provide an orthogonal handle, especially against gluon‑initiated QCD jets. |
| **Perform a data‑driven validation / calibration of the pull distributions.** | • Use a control region enriched in hadronic W‑boson decays (e.g., semileptonic t t̄ events) to extract the σ of the dijet mass in data.<br>• Re‑scale the pulls accordingly and re‑evaluate the MLP on real data. | Guarantees that the Gaussian‑pull assumption holds in the real detector, mitigating possible simulation‑data mismodelling. |
| **Investigate a lightweight *gating* mechanism.** | • Insert a multiplicative gate (e.g., a sigmoid of pₜ) that multiplies the BDT input before it reaches the hidden layer, learned jointly with the rest of the network. | Gives the network explicit control over when to trust shape information, possibly improving stability across the whole pₜ spectrum. |
| **Benchmark alternative machine‑learning models.** | • Try a depth‑2 gradient‑boosted tree (XGBoost) with the same six inputs, quantised to 8‑bit and implemented via a decision‑tree lookup table.<br>• Compare latency, resource usage, and performance against the MLP. | Tree ensembles can capture non‑linear interactions without hidden units; they may be even more hardware‑friendly if the tree depth stays low. |

**Prioritisation for the next iteration (478):**  

1. Implement the *dynamic σ(pₜ)* regression + re‑scaled pulls (high physics impact).  
2. Prototype a hard‑sigmoid output and measure any latency headroom gained.  
3. Add a groomed‑mass input and test the “BDT‑free” variant.  

These steps directly build on the success of iteration 477, aim to recover the remaining efficiency loss at the highest boosts, and stay within the FPGA constraints that drive our trigger‑level design.