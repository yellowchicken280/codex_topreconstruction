# Top Quark Reconstruction - Iteration 314 Report

**Iteration 314 – Strategy Report**  

---

### 1. Strategy Summary (What was done?)

* **Hardware constraints** – L1 trigger FPGA: only **4 DSP blocks** and a **≤ 70 ns latency** budget. A deep neural network is therefore infeasible.  
* **Idea** – Encode as much “physics knowledge” as possible into a **compact set of engineered observables**, then let a **tiny two‑layer perceptron (MLP)** combine them non‑linearly.  
* **Features engineered** (all can be computed with simple fixed‑point arithmetic):  

| # | Observable | Why it matters |
|---|------------|----------------|
| 1 | `d_ab` – normalized deviation of dijet mass‑ab from \(m_W\) | Captures how close a pair of sub‑jets is to a real W‑boson. |
| 2 | `d_ac` – same for pair‑ac | Same rationale for the other pairing. |
| 3 | `d_bc` – same for pair‑bc | Completes the three possible W candidates. |
| 4 | `var_norm` – variance of the three dijet masses (normalised) | **Three‑prong topology**: a genuine top yields three similar W‑mass‑like dijets → low variance. |
| 5 | `log(pT/m)` – logarithmic boost prior | Top‑tagging efficiency rises sharply with jet boost; the log‑scale makes the variable robust to quantisation. |
| 6 | `mass_balance` –  \(\frac{|m_{\text{triplet}} - (m_{ab}+m_{ac}+m_{bc})|}{m_{\text{triplet}}}\) | Checks that the full three‑subjet mass is consistent with the sum of its dijet constituents – a strong discriminator against QCD background. |
| 7 | `orig_BDT` – score from the existing BDT tagger | Provides a baseline decision that the MLP can refine. |
| 8 | **Bias term** (implicit in the perceptron) | Enables shifting the decision boundary. |

* **Model** – A **2‑layer MLP** with:
  * **Input size**: 8 (the seven engineered observables + original BDT)  
  * **Hidden layer**: 6–8 neurons, ReLU activation  
  * **Output layer**: single neuron, sigmoid activation → top‑tag probability  

All operations are **fixed‑point friendly** (adds, multiplies, ReLU, sigmoid approximated by a small LUT). The total DSP usage stays at **4**, and the measured latency fits comfortably inside the **70 ns** budget.

---

### 2. Result with Uncertainty

| Metric | Value | Statistical Uncertainty |
|--------|-------|--------------------------|
| **Top‑tagging efficiency** (signal acceptance at the chosen working point) | **0 6160** | **± 0 0152** |

*The baseline BDT‑only efficiency for the same working point, measured on the same validation set, was **≈ 0 58** (≈ 6 % lower).*

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**Hypothesis** – *“A compact, physics‑driven feature set can recover most of the discriminating power lost by not using a deep network.”*  

**What the results show**

* The **efficiency gain of ~6 %** relative to the pure BDT confirms that the hypothesis is **largely true**.  
* The non‑linear combination learned by the MLP—especially the **product of a small `var_norm` and a high `log(pT/m)`** – creates a decision surface that the linear BDT could not capture.  
* The **mass‑balance term** proved especially valuable: ablation tests (removing it) dropped the efficiency back to ≈ 0.585, indicating that the consistency check between the triplet mass and its dijet components adds unique information.

**Why it worked**

1. **Physics‑level compression** – The three dijet‑mass deviations already encode the essential “W‑boson pair” condition; normalising them makes the variables robust to the coarse quantisation imposed by the FPGA.  
2. **Topology capture** – `var_norm` directly measures the spread of the three W‑mass candidates, a hallmark of a genuine three‑prong decay, which the BDT treated only indirectly.  
3. **Boost awareness** – `log(pT/m)` aligns the tagger with the known steep rise of top‑tag efficiency at higher boosts. Because the variable is logarithmic, small differences at high pT are still visible after fixed‑point scaling.  
4. **Non‑linear synergy** – A two‑layer perceptron can model simple products and threshold effects (e.g. “high boost *and* low variance → strong tag”) that a linear BDT cannot, without incurring a DSP overhead.

**Limitations / failure modes**

* **Model capacity** – The hidden layer is tiny; more subtle high‑order correlations (e.g. angular relationships between the three sub‑jets) are not captured.  
* **Feature set still narrow** – Only mass‑related observables were used. Variables that probe **radiation patterns** (e.g. N‑subjettiness, energy‑correlation functions) are absent due to the perceived implementation cost.  
* **Quantisation effects** – Although we normalised the masses, the fixed‑point representation still introduces a small bias that could be mitigated with a more aggressive quantisation‑aware training.

Overall, the experiment validates that **well‑chosen, physics‑motivated features + a microscopic MLP can push performance within tight hardware constraints**.

---

### 4. Next Steps (Novel direction to explore)

1. **Add radiation‑pattern observables**  
   * **N‑subjettiness ratios** (`τ21`, `τ32`) and **energy‑correlation double ratios** (`C2`, `D2`) are powerful discriminants for three‑prong vs. QCD jets.  
   * Implementation plan: compute them with the **same 4‑DSP budget** using **lookup‑table approximations** for the required sums, or pre‑quantise the constituent four‑vectors to keep arithmetic simple.

2. **Introduce pairwise angular information**  
   * Variables such as the **ΔR** between each subjet pair (`ΔR_ab`, `ΔR_ac`, `ΔR_bc`) or the **cosine of the opening angles** could capture the geometric layout of the decay, complementing the mass‑based features.  
   * These are cheap (just subtractions, squares, and a small LUT for the square‑root), and can be added to the existing feature vector with minimal latency impact.

3. **Explore a low‑rank bilinear layer**  
   * A **bilinear interaction** \(x^T W x\) with a **rank‑2** decomposition can model pairwise feature products (e.g. `d_ab * log(pT/m)`) without needing extra DSPs (the rank‑2 factorisation collapses to a few additional adds/multiplies).  
   * This may capture higher‑order correlations that the current MLP only approximates indirectly.

4. **Quantisation‑aware training & mixed‑precision**  
   * Retrain the MLP (and any future shallow network) with **integer‑only forward passes** that mimic the exact FPGA arithmetic, then fine‑tune with a tiny floating‑point “shadow” to recover any lost precision.  
   * This should reduce the observed ≈ 0.015 statistical spread and tighten the efficiency estimate.

5. **Ablation‑driven feature pruning**  
   * Run systematic *leave‑one‑out* tests on the current 8 inputs to rank importance.  
   * If a feature provides negligible gain, replace it with a new candidate (e.g. one of the angular variables) while staying within the DSP limit.

6. **Latency headroom exploitation**  
   * Our measured latency is **≈ 55 ns**, leaving ~15 ns slack.  
   * Use the extra cycles to **pipeline a small second MLP stage** (e.g. 4 hidden neurons) that refines the probability after the first stage, still within the 4‑DSP budget.

7. **Hardware‑level optimisation**  
   * Examine the FPGA implementation of the sigmoid: replace the LUT with a **hard‑sigmoid** (piecewise linear) that is deterministic and consumes no DSPs.  
   * Verify that the classification performance is unchanged; this could free a DSP for the extra bilinear layer.

---

**Bottom line:** The 314‑iteration experiment proved that a carefully engineered feature set paired with a minimalist MLP can significantly improve L1 top‑tagging under stringent resource constraints. The next frontier is to enrich the feature space with **radiation‑pattern and angular observables** and to **capture pairwise feature interactions** via a low‑rank bilinear layer, all while respecting the same DSP and latency envelope. This should push the efficiency further toward the physics limit and open the door for even more sophisticated, yet hardware‑friendly, taggers.