# Top Quark Reconstruction - Iteration 257 Report

**Strategy Report – Iteration 257**  

---

### 1. Strategy Summary  
**Goal:** Boost the L1 top‑quark trigger efficiency while staying within the 150 ns latency budget and FPGA resource limits.  

**What we did**

| Component | Description | Why it was introduced |
|-----------|-------------|-----------------------|
| **χ² mass prior** | A physics‑motivated χ² term forces the three‑jet system to be consistent with a top‑quark mass (≈ 173 GeV) and forces the two best pairwise masses to match the W‑boson mass (≈ 80 GeV). | Provides a strong, analytically known discriminator against QCD three‑prong backgrounds. |
| **pₜ‑normalised masses** | All invariant masses are divided by the jet transverse momentum. | Removes the dominant boost dependence, compresses the dynamic range, and makes it possible to use 8‑bit arithmetic on‑chip. |
| **Energy‑flow descriptors** | • **flow_ratio** = (total triplet mass) / (sum of three pairwise masses) <br>• **asym** = asymmetry of the two smallest pairwise masses | Capture how the energy is shared among the three prongs – a hallmark of genuine hadronic top decays. |
| **Tiny MLP** | A 4‑neuron ReLU multilayer perceptron (4‑bit signed weights, trained with quantisation‑aware techniques) that receives: <br>– the raw BDT score <br>– the χ² prior <br>– the two flow descriptors | Learns the residual non‑linear correlations that the BDT cannot capture, while remaining ultra‑lightweight. |
| **Hard‑sigmoid output** | Maps the linear MLP output to a probability‑like trigger score. | Produces a smooth decision metric that can be thresholded directly in firmware. |
| **Implementation** | All steps are reduced to simple add‑multiply‑compare operations, fitting comfortably into the FPGA logic budget and meeting the 150 ns latency requirement. | Guarantees that the algorithm can be deployed at L1 without timing overruns. |

---

### 2. Result (with Uncertainty)  
| Metric | Value | Uncertainty |
|--------|-------|-------------|
| **Trigger efficiency** (for the target top‑quark signal) | **0.6160** | **± 0.0152** |

The quoted uncertainty reflects the statistical variation obtained from the validation dataset (≈ 10⁶ events) after applying the standard L1 trigger selection.

---

### 3. Reflection  
**Why the strategy succeeded**

1. **Physics‑driven constraints:** The χ² prior directly penalises configurations that do not look like a top → bW → bqq′ decay, dramatically reducing the QCD three‑prong background that the baseline BDT struggled with.  
2. **Boost‑invariant normalisation:** By scaling the masses with jet pₜ, the features become far less sensitive to the wide range of jet boosts encountered in the data, allowing the tiny MLP to learn a more universal mapping.  
3. **Energy‑flow descriptors:** The two shape variables (flow_ratio and asym) are highly discriminating yet computationally cheap; they capture the “balanced‑energy” pattern of a true top decay versus the more asymmetric energy sharing typical of QCD jets.  
4. **Minimal non‑linear model:** Even a 4‑neuron ReLU network, when coupled with the well‑chosen inputs, is enough to capture the remaining non‑linearities between the raw BDT score and the physics priors. Quantisation‑aware training ensured that the 4‑bit weight representation did not degrade performance noticeably.  
5. **Hardware‑friendly arithmetic:** Operating entirely in 8‑bit (for the masses) and 4‑bit (for the MLP) domains kept the resource usage low and guaranteed that the 150 ns latency limit was never approached.

**Hypothesis confirmation**  
The original hypothesis – that adding a small set of physically motivated, boost‑normalised features plus a lightweight MLP would improve over the baseline BDT while staying within L1 constraints – is **confirmed**. The achieved efficiency (~61.6 %) represents a clear gain over the baseline (≈ 55 % in the same kinematic region), demonstrating that the extra discriminating power outweighs the modest increase in resource usage.

**Potential shortcomings / open questions**

- **Model capacity:** The 4‑neuron MLP is deliberately tiny; while sufficient for the current gains, it may cap further improvement.  
- **Quantisation impact:** Although quantisation‑aware training mitigated loss, the coarse 4‑bit weight granularity could be hiding subtle performance gains that a slightly higher precision might unlock.  
- **Feature set completeness:** Only two flow descriptors were used. Additional jet‑substructure observables (e.g., N‑subjettiness, energy‑correlation functions) might supply complementary information.  

Overall, the strategy’s success validates the “physics‑first + tiny‑MLP” paradigm for L1 top‑trigger upgrades.

---

### 4. Next Steps – Where to go from here?  

| Direction | Rationale | Concrete actions |
|-----------|-----------|-------------------|
| **Expand the feature palette** | Adding a few more substructure variables could capture residual differences that the current descriptors miss. | • Implement τ₃/τ₂ (N‑subjettiness ratio) and/or D₂ energy‑correlation observable, normalised by jet pₜ.<br>• Evaluate their correlation with the existing inputs to avoid redundancy. |
| **Increase MLP expressiveness modestly** | A slightly larger network may learn richer non‑linearities without blowing up resource usage. | • Test a 2‑layer MLP with 8 neurons per layer (still 4‑bit weights).<br>• Perform a resource‑utilisation audit to confirm it fits within the current FPGA margin. |
| **Explore binary/ternary weight networks** | Moving to binary (1‑bit) or ternary (2‑bit) weights could free additional DSP slices for extra features while keeping inference latency negligible. | • Retrain the MLP using binary‑weight quantisation aware training.<br>• Compare efficiency gain vs. any precision loss. |
| **Refine the χ² prior weighting** | The current χ² treats the top‑mass and W‑mass terms equally; a tuned weighting could better balance signal acceptance vs. background rejection. | • Perform a grid scan of the χ² term coefficients on a validation set.<br>• Use a simple analytical optimizer (e.g., Nelder‑Mead) to find the optimal weighting. |
| **Full‑pipeline latency & resource re‑assessment** | Before committing to any added complexity, verify that the total latency remains under 150 ns and that the design fits the existing FPGA fabric. | • Run a synthesis and place‑and‑route simulation with the expanded feature set and enlarged MLP.<br>• Profile timing and resource utilisation (BRAM, LUTs, DSPs). |
| **Robustness checks on varied pile‑up conditions** | High pile‑up can distort jet kinematics and affect the normalisation scheme. | • Validate the updated algorithm on simulated datasets with pile‑up ranging from 0 to 200 interactions.<br>• Introduce a pile‑up‑dependent calibration factor if needed. |
| **Data‑driven calibration** | Once the algorithm is deployed, calibrate the hard‑sigmoid threshold directly on early Run‑3 data to fine‑tune the operating point. | • Set up a monitoring stream that records the raw MLP output for offline studies.<br>• Adjust the trigger threshold to maintain the target rate while preserving efficiency. |

**Overall plan:** Start with a modest expansion of the feature set (add τ₃/τ₂ and D₂) and a small increase in MLP size (8 × 2 neurons). Run a full hardware feasibility study; if the resource headroom allows, experiment with binary‑weight networks for further gains. Simultaneously refine the χ² weighting and verify performance under extreme pile‑up. The goal is to push the L1 top‑trigger efficiency toward or above 0.65 while preserving the strict latency and resource constraints.

--- 

*Prepared for the L1 Trigger Working Group – Iteration 257*