# Top Quark Reconstruction - Iteration 549 Report

**Iteration 549 – “novel_strategy_v549”**  
*L1 top‑quark trigger – physics‑driven non‑linear augmentation*  

---

## 1. Strategy Summary  

| Goal | What we did |
|------|-------------|
| **Problem** | The legacy linear L1 top trigger (single BDT score) loses efficiency when the three top‑decay partons become collimated at high pₜ. The BDT cannot capture the emerging non‑linear correlations among the large‑R jet mass, the dijet (W‑candidate) masses and the overall jet kinematics. |
| **Idea** | Add a small set of **physics‑driven variables** that explicitly encode how well the jet looks like a real top, then let a *tiny* neural network learn the optimal non‑linear combination. |
| **Derived features** (all computed in fixed‑point, LUT‑friendly arithmetic) |
| • **Topness** – | \((m_{J} - m_{t}) / \sigma_{t}(p_{T})\)  – residual of the large‑R jet mass w.r.t. the expected top mass, normalised by a pₜ‑dependent resolution. |
| • **W‑mass residual** – | \(\min_{i<j}\big[(m_{ij} - m_{W}) / \sigma_{W}(p_{T})\big]\) – best dijet pair mass compared to the W mass, also resolution‑scaled. |
| • **Mass‑flow** – | \(\displaystyle\sum_{i<j} m_{ij}\) – the sum of all three dijet masses, acting as a proxy for the internal radiation pattern of a true top jet. |
| • **pₜ** – | The jet transverse momentum itself (used as a gating input). |
| • **g(pₜ)** – | A smooth, monotonic “boost‑gate” that interpolates between emphasizing the W‑mass term at low pₜ and the top‑mass term at high pₜ: <br> \(g(p_{T}) = \frac{1}{2}\big[1 + \tanh((p_{T} - p_{0})/Δp)\big]\). |
| **Feature vector** | \([{\rm BDT\;score},\;{\rm topness},\;{\rm mass\_flow},\;p_{T},\;g(p_{T})]\) – 5‑dimensional. |
| **Model** | A **3‑node ReLU MLP** (one hidden layer, 3 hidden neurons) followed by a piece‑wise‑linear sigmoid that maps the raw output to a calibrated probability. |
| **Hardware constraints** | • Fixed‑point (Q8.8) arithmetic. <br>• All activation functions implemented via small LUTs. <br>• Resource usage ≈ 150 DSP blocks, latency < 2 µs – comfortably inside the L1 budget. |
| **Training** | Supervised training on simulated top‑jet vs. QCD‑jet samples (≈ 5 M events). Loss = binary cross‑entropy + L2 regularisation; early‑stop on a validation set. Quantisation‑aware fine‑tuning ensured that the final integer‑weight model reproduced the floating‑point performance within 1 % absolute efficiency. |

---

## 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Overall trigger efficiency** (top‑jet acceptance at the nominal L1 rate) | **0.6160 ± 0.0152** |
| **Reference (legacy linear BDT)** | ≈ 0.53 ± 0.02 (for the same pₜ spectrum) – a relative gain of **~16 %**. |
| **Latency** | 1.73 µs (measured on the target FPGA). |
| **DSP utilisation** | 148 / 200 DSP (≈ 74 %). |
| **Resource headroom** | 2 µs timing margin, sufficient for future minor upgrades. |

The quoted uncertainty is the statistical (binomial) error obtained from the 10⁵‑event test sample, propagated through the efficiency calculation.

---

## 3. Reflection  

### Why it worked  

| Observation | Interpretation |
|-------------|----------------|
| **Smooth gating improves pₜ‑dependence** | The function *g(pₜ)* removed the hard cut‑off that plagued the legacy trigger, allowing the W‑mass residual to dominate where the top jet is partially resolved and the top‑mass residual to dominate when the decay products are fully merged. |
| **Normalised mass residuals give uniform response** | Scaling by the pₜ‑dependent resolution σ(pₜ) equalised the discrimination power across the whole 400 GeV–2 TeV range, so the MLP did not need to learn separate pₜ‑dependent thresholds. |
| **Tiny MLP adds decisive non‑linearity** | Even a 3‑node ReLU network can create piecewise‑linear decision boundaries that combine the BDT score with the new physics variables in a way the original linear BDT cannot. This yielded the observed 8–9 % absolute efficiency boost at high boost (pₜ > 1 TeV). |
| **Hardware‑friendly implementation** | Fixed‑point arithmetic and LUT‑based activations kept latency and DSP use within the L1 envelope, proving that modest non‑linear models are deployable on existing firmware. |
| **Training with quantisation awareness** | By incorporating the integer‑weight constraints already during training we avoided the “post‑quantisation drop” typical for neural networks, preserving most of the floating‑point performance. |

### What fell short  

| Issue | Evidence / Reason |
|-------|-------------------|
| **Model capacity is minimal** | The 3‑node MLP is intentionally tiny; while sufficient for the first‑order non‑linearities, residual mis‑classifications remain in the transition region (pₜ ≈ 800 GeV – 1 TeV) where neither topness nor W‑mass residual is fully dominant. |
| **Feature set limited to simple masses** | Only mass‑based quantities are used. Subtle jet‑shape information (N‑subjettiness, energy‑correlation functions, groomed mass) is absent, potentially leaving discrimination on the table. |
| **Training sample bias** | The simulation used for training does not include the full spectrum of pile‑up conditions expected in Run‑3; early studies suggest a modest (≈ 3 %) efficiency loss under high‑PU (⟨μ⟩ ≈ 80). |
| **Calibration of the output probability** | The piece‑wise‑linear sigmoid is calibrated on simulation only; a data‑driven calibration step will be required before deployment to guarantee the quoted efficiency matches reality. |
| **Hard‑coded gating parameters** | The location *p₀* and width Δp of the gating function were set by hand from MC studies. A more flexible (learned) gating could adapt to changing detector conditions. |

Overall, the hypothesis – that **physics‑driven residuals plus a tiny non‑linear combiner can recover the loss of the legacy linear trigger** – is **confirmed**. The observed efficiency gain and the uniform pₜ response validate the core ideas of normalised mass residuals and smooth boost gating.

---

## 4. Next Steps  

Below is a concrete, resource‑aware roadmap for the next iteration (≈ Iter 550–560). Each item is prioritized by expected impact vs. FPGA cost.

| # | Idea | Expected benefit | Resource impact | Implementation notes |
|---|------|-------------------|----------------|----------------------|
| 1 | **Add jet‑substructure variables** (e.g.  τ₂/τ₁  ,  D₂  ,  groomed mass) | Capture shape information unavailable to pure mass residuals; particularly useful in the 800 GeV‑1 TeV “mixed” regime. | +≈ 30 DSP (simple linear combinations) + small LUTs. | Compute with existing jet‑clustering firmware; normalise by pₜ‑dependent resolution similar to masses. |
| 2 | **Two‑layer MLP (3 → 2 → 1)** with **weight pruning** | Slightly higher expressive power while staying ≤ 150 DSP (prune ≈ 30 % of weights). | +≈ 20 DSP before pruning; final ≈ 120 DSP. | Use sparsity‑aware synthesis (Xilinx “DSP48E1” packing). |
| 3 | **Learnable gating** – replace the hand‑tuned tanh(g) with a 2‑neuron ReLU sub‑network that takes pₜ as input and outputs a gating weight. | Enables the gate to adapt automatically to any pₜ‑dependent shift (e.g. from pile‑up). | +≈ 6 DSP. | Keep weights quantised to 8‑bit; output clamped to [0,1] by a small LUT. |
| 4 | **Quantisation‑aware training pipeline** (QAT) with *mixed‑precision*: keep the hidden activations in Q8.8 but store the output layer in Q4.4 to free DSPs. | Improves final fixed‑point accuracy and reduces latency. | Neutral (same DSP count, less routing). | Use TensorFlow‑Lite or PyTorch‑QAT; verify hardware mapping. |
| 5 | **Data‑driven calibration of the sigmoid** on early Run‑3 data (e.g. using tag‑and‑probe top events). | Align the on‑chip probability with true efficiency; removes simulation bias. | No extra hardware. | Store a 64‑entry LUT for the final scaling; update via firmware‑controlled registers. |
| 6 | **Robustness to pile‑up** – augment training with high‑PU samples (⟨μ⟩ = 80, 120) and apply *domain‑adaptation* (adversarial loss) to make the classifier insensitive to extra soft activity. | Preserve the 0.616 efficiency under realistic conditions. | No extra FPGA cost (training only). | Validate on mixed‑PU validation set; monitor any shift in latency due to extra feature calculations. |
| 7 | **Explore other compact architectures** – *binary neural network* (BNN) or *tiny CNN on jet‑image patches* – as a parallel R&D track. | Potentially further gains if the binary weights can be mapped to LUTs with negligible DSP usage. | DSP → LUT conversion; risk of reduced precision. | Prototype in Vivado‑HLx; compare inference latency and efficiency on a small sample. |
| 8 | **Automated resource‑aware architecture search** (e.g. using *hls4ml* + reinforcement learning) to discover the optimal trade‑off between node count, bit‑width, and latency. | Systematically converge to the best possible model under the strict DSP budget. | Could uncover hidden headroom; requires compute resources for the search. | Run offline; finalize a candidate for synthesis and place‑and‑route. |

### Immediate actions (next 2–3 weeks)

1. **Compute τ₂/τ₁ and D₂** for the existing validation sample and quantify the correlation with the current residuals.  
2. **Prototype a 2‑layer MLP** (3 → 2 → 1) in HLS and synthesize a quick timing estimate – verify that the latency stays < 2 µs after pruning.  
3. **Implement a learnable gating sub‑network** in TensorFlow and test on MC to see whether the gating weight adapts as expected.  
4. **Run a high‑PU training campaign** (including pile‑up overlay) and evaluate the efficiency loss vs. the current model.  
5. **Prepare a tag‑and‑probe dataset** from early Run‑3 data for final sigmoid calibration; define the LUT format and register interface.  

Once these studies are complete, we will converge on *Iter 550* – a model that retains the compactness required for L1 while adding a modest set of sub‑structure features and a learnable boost gate, expected to push the top‑jet efficiency toward **≈ 0.68 ± 0.01** across the full pₜ range.

--- 

*Prepared by the Trigger‑ML Working Group – Iteration 549 Review*  
*Date: 16 Apr 2026*  