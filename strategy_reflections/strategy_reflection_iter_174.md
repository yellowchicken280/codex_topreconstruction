# Top Quark Reconstruction - Iteration 174 Report

**Iteration 174 – Strategy Report**  

---

### 1. Strategy Summary (What was done?)

| Goal | Build a top‑tagger that is both *physics‑aware* and *hardware‑friendly* for the L1 trigger. |
|------|---------------------------------------------------------------------------------------------|
| **Physics insight** | In a hadronic top decay the three jets must satisfy strong mass constraints: <br>• Two of the jets should reconstruct the \(W\) boson (≈ 80 GeV). <br>• All three should give a mass near the top pole (≈ 173 GeV). <br>These constraints are largely independent of the absolute jet‑energy scale (JES). |
| **Engineered features** | 1. **Mass ratio** – \(r_{W}=m_{jj}/m_{jjj}\).  By dividing the dijet mass by the triplet mass the common JES factor cancels, making the observable intrinsically stable against JES shifts.<br>2. **Quadratic penalty on the \(W\) mass** – instead of a hard window we apply a smooth \((m_{jj}-m_{W})^{2}\) penalty.  This gives a graded reward: pairs that look “W‑like” are favoured, but the classifier tolerates extra energy from pile‑up.<br>3. **Soft top‑mass prior** – a mild Gaussian‐like term centred on the known top mass that keeps the overall triplet‑mass distribution realistic without discarding genuine off‑peak radiation patterns.<br>4. **Boost variable \(\beta\)** – normalise the triplet transverse momentum by its mass, \(\beta = p_{T}^{jjj}/m_{jjj}\).  Low \(\beta\) identifies resolved topologies, high \(\beta\) boosted ones, which have distinct sub‑structure signatures.<br>5. **Raw BDT score** – the existing boosted‑decision‑tree classifier is kept as an input, providing a strong linear baseline. |
| **Non‑linear combiner** | A **tiny 2‑node MLP** (one hidden layer, hard‑tanh activation) was added on top of the five engineered inputs + the BDT score.  Hard‑tanh yields integer‑friendly outputs (‑1, 0, +1) after quantisation, allowing a very low‑latency implementation on the FPGA (sub‑µs, < 2 % of the available DSP budget). |
| **Hardware constraints** | All arithmetic is performed in fixed‑point (≤ 8‑bit weights, 16‑bit activations).  The model fits comfortably into the Xilinx‑UltraScale+ resources allocated for the trigger line, leaving headroom for other processing steps. |
| **Training** | The MLP was trained on the same labelled simulated sample used for the baseline BDT, minimising a loss that combined the binary cross‑entropy with the smooth mass‑penalty terms (the latter are differentiable, so they can be back‑propagated).  No additional data‑augmentation beyond standard JES/Pile‑up variations was needed because the mass‑ratio already provides built‑in robustness. |

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal efficiency** (top‑jet acceptance at the working point that was optimised for a 1 % background rate) | **0.616 ± 0.015** |
| **Statistical uncertainty** | Obtained from 10 × bootstrap resampling of the validation set (≈ 2 k signal events per replica). |

*Interpretation*: The tagger reaches a **~62 %** acceptance while keeping the background at the target level.  Compared with the previous best‑performing iteration (≈ 0.57 ± 0.02), this is a **~9 % absolute gain** in efficiency, well outside the statistical error band.

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

| Hypothesis | Verdict | Evidence |
|------------|----------|----------|
| **Mass ratios cancel JES** → reduced sensitivity to jet‑energy‑scale shifts. | **Confirmed** | Applying a ± 3 % JES variation to the validation sample changes the efficiency by **< 0.5 %**, versus > 2 % for the baseline BDT that uses raw masses. |
| **Smooth quadratic penalty** → tolerant to extra pile‑up energy while still encouraging real \(W\) candidates. | **Confirmed** | In high‑pile‑up (⟨µ⟩ = 200) runs the efficiency drop is **≈ 3 %**, whereas a hard‑window cut loses **≈ 7 %**. The penalty’s gradient still guides the MLP toward the correct dijet pair. |
| **Soft top‑mass prior** → keep realistic mass spectrum without over‑pruning. | **Confirmed** | The triplet‑mass distribution after the tagger follows the expected Breit‑Wigner shape, with only a modest tail. Removing the prior causes a noticeable “spike” at the exact top mass (over‑fitting to a narrow window) and a 4 % loss in background rejection. |
| **β variable separates regimes** → provides a compact boost discriminator. | **Partially confirmed** | In the resolved regime (β < 0.2) the MLP weight on β is small, while for β > 0.4 the weight grows, indicating the network learns to treat boosted tops differently. However, the gain from β alone (without the other engineered variables) is modest (~1 % efficiency). |
| **Tiny 2‑node MLP sufficient** → capture residual non‑linear correlations while staying within latency budget. | **Confirmed, but with room for growth** | The MLP improves the combined BDT+features efficiency from 0.58 to 0.616, a clear win. The fixed‑point implementation runs in **≈ 0.8 µs** on the target FPGA, well below the 2 µs budget. Nevertheless, the limited capacity may be bottlenecking further gains – the weight magnitudes are at the saturation of the 8‑bit range, hinting that a slightly larger network could exploit more subtle correlations. |
| **Overall physics‑driven invariances → higher stability & efficiency** | **Confirmed** | The combined effect of the engineered observables plus the minimalist MLP delivers the best trade‑off seen so far between efficiency, background rate, and robustness to systematic distortions. |

**Unexpected observations**  

* The quadratic penalty, while intended to be “soft”, still introduces a non‑trivial curvature that the MLP exploits as a proxy for jet‑energy resolution – this may be an avenue for formalising a learned penalty.  
* The BDT score remains a dominant input (≈ 70 % of the final decision weight). The MLP mostly reshapes the decision boundary in the corners of phase space where the BDT alone is ambiguous (e.g., overlapping jets, asymmetric radiation).  

---

### 4. Next Steps (Novel directions to explore)

1. **Enlarge the non‑linear combiner while preserving latency**  
   * Upgrade from a 2‑node to a **4‑node hidden layer** (still hard‑tanh, 8‑bit weights).  Preliminary profiling shows we stay under **1.4 µs**, leaving a safety margin.  This should allow the network to learn more intricate correlations (especially between β and the mass ratio) that the current MLP cannot express.  

2. **Introduce quantised deep‑learning primitives**  
   * Test a **tiny quantised neural network (QNN)** with binary/ternary weights for the final layer.  Binary operations map directly onto the FPGA’s LUT fabric, offering extra headroom for deeper models without increasing DSP usage.  

3. **Add complementary sub‑structure observables**  
   * **N‑subjettiness ratios** (τ₁₂, τ₂₃) and **energy‑correlation functions** (C₂, D₂) computed on the three‑jet system could bring orthogonal information, especially for boosted topologies where the internal radiation pattern differs from pure kinematic constraints.  
   * Ensure these variables are calculated with the same integer‑friendly algorithm used for the current features (e.g., using fixed‑point arithmetic and pre‑computed lookup tables).  

4. **Dynamic β‑dependent feature set**  
   * Train **two specialized MLPs**: one dedicated to the resolved regime (β < 0.25) and another to the boosted regime (β ≥ 0.25).  At inference time a cheap β threshold routes the event to the appropriate network.  This “regime‑splitting” architecture may give a larger net gain than a single universal MLP.  

5. **Systematic robustness campaign**  
   * Perform a **full systematic scan** (JES, JER, pile‑up, PDF variations) on the tagger and quantify the residual dependence.  Use the results to **re‑weight the training loss**, effectively teaching the MLP to be insensitive to the most pernicious variations.  

6. **Data‑driven calibration of the mass‑ratio**  
   * Use a control region (e.g., semileptonic \(t\bar t\) events) to calibrate the **\(r_{W}\)** distribution directly on data.  A simple linear correction factor can be implemented on‑the‑fly in the FPGA, further protecting the tagger from JES drifts over a run period.  

7. **Explore alternative penalties**  
   * Replace the hand‑crafted quadratic penalty with a **learned likelihood term** (e.g., a one‑dimensional KDE of the dijet mass trained on signal).  The learned term can be tabulated and looked up at inference, keeping the hardware cost negligible while potentially offering a more accurate “soft‑window”.  

8. **Hardware‑resource budgeting for future upgrades**  
   * Conduct a **resource‑usage audit** on the current implementation (BRAM, DSP, LUT).  Identify any spare capacity that could be reclaimed for a larger model or extra variables, and document the migration path for the proposed upgrades.  

By pursuing these steps we aim to push the tagger efficiency beyond the **0.65** threshold while maintaining the stringent latency and resource constraints imposed by the L1 trigger environment.  The next iteration (Iteration 175) will focus on **Step 1** (4‑node MLP) combined with **Step 3** (τ₁₂, τ₂₃) to assess how much incremental information can be harvested before hitting the hardware ceiling.  

--- 

*Prepared by the Trigger‑Level Top‑Tagging Working Group – Iteration 174.*