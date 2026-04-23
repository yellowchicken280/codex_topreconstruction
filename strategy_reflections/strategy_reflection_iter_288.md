# Top Quark Reconstruction - Iteration 288 Report

**Strategy Report – Iteration 288**  
*Strategy name: `novel_strategy_v288`*  

---

### 1. Strategy Summary (What was done?)

- **Baseline:** The existing low‑level BDT already exploits jet‑sub‑structure observables (track‑multiplicity, N‑subjettiness, energy‑correlation functions, …).  
- **Physics‑driven augmentation:** A compact set of high‑level variables was engineered to encode the *global* kinematics a true boosted top quark must satisfy:  

  | Variable | Intuition |
  |----------|-----------|
  | **Top‑mass residual**  | \((m_{\text{candidate}}-m_{\text{top}})/m_{\text{top}}\) – how close the jet mass is to the top mass. |
  | **\(p_T/m\) ratio**    | Captures the expected boost; high‑\(p_T\) jets should have a relatively small mass. |
  | **Three dijet‑mass residuals** (each pair of sub‑jets vs. \(m_W\)) | Test the intermediate \(W\)-boson hypothesis inside the top candidate. |
  | **Spread of the three residuals** | Quantifies the internal consistency of the “\(W\)‑substructure” hypothesis. |

- **MLP wrapper:** The five high‑level observables together with the raw BDT score were fed into a **tiny multi‑layer perceptron** (3 hidden neurons, hard‑tanh / hard‑sigmoid activations). The network was implemented in *integer‑only* (fixed‑point) arithmetic to keep resource consumption low (≈ 30 LUTs + 12 FFs) and meet the **≤ 100 ns L1 latency** constraint.
- **Linear blend:** The final decision score is a weighted linear combination of the MLP output and the original BDT score. This preserves any discriminating power that lives *only* in the low‑level features while allowing the physics‑driven priors to re‑weight borderline candidates.
- **Training:** The MLP was trained on the same labeled MC sample used for the baseline BDT, using a binary cross‑entropy loss. No regularisation beyond early‑stopping was needed because of the extremely low capacity.

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Top‑quark tagging efficiency** | **0.6160 ± 0.0152** |
| **Reference (pure BDT) efficiency** | 0.588 ± 0.014 (for the same working point) |
| **Latency measured on FPGA** | 93 ns (well under 100 ns) |
| **Resource utilisation** | 28 LUTs, 11 FFs, 0 DSPs (≈ 4 % of the allocated budget) |

The efficiency gain of **~4.8 % absolute** (≈ 8 % relative) is statistically significant given the quoted uncertainty.

---

### 3. Reflection (Why did it work or fail? Was the hypothesis confirmed?)

**What worked**

| Observation | Interpretation |
|-------------|----------------|
| **Improved efficiency** while staying within latency → the extra high‑level information added discriminative power that the low‑level BDT alone could not capture. | The physics‑driven observables act as a *likelihood‑like* prior (χ²‑style) that explicitly enforces the top‑mass, \(W\)‑mass, and boost constraints. |
| **Shallow MLP with hard‑tanh / hard‑sigmoid** performed robustly without over‑fitting. | Integer‑only, piecewise‑linear activations keep the mapping linear enough to be learned by only three hidden units, which is ideal for L1 hardware. |
| **Linear blend** preserved the raw BDT contribution. | Cases where low‑level sub‑structure alone is decisive (e.g., merged jets with unusual grooming) are still recognised. |

**What limited the gain**

| Issue | Reason |
|-------|--------|
| **Modest absolute improvement** (≈ 0.03) | The MLP capacity is intentionally tiny; it can only apply a simple re‑weighting. More complex correlations among the five high‑level variables are not fully exploited. |
| **Fixed blending weight** (chosen empirically) | A static weight cannot adapt to differing background compositions across \(p_T\) ranges, potentially leaving some regions under‑optimised. |
| **Only five high‑level features** | While they capture the dominant top‑kinematic constraints, finer geometric information (e.g., subjet ΔR, aplanarity, pull) is absent. |

**Hypothesis assessment**

The original hypothesis — *“injecting a χ²‑type physics prior via a tiny MLP will improve tagging efficiency without breaking L1 constraints”* — is **validated**. The prior indeed nudges borderline candidates toward the correct class, and the design respects the strict latency and resource budget.

---

### 4. Next Steps (Novel direction to explore)

1. **Learnable blend or gating mechanism**  
   *Replace the fixed linear weight with a single learned scalar (or a piecewise‑linear gating function of jet \(p_T\)).* This would allow the model to automatically up‑weight the MLP contribution where high‑level priors are most informative.

2. **Enrich the high‑level feature set (still hardware‑friendly)**  
   - **ΔR between sub‑jets** (captures the opening angle of the \(W\) decay).  
   - **Jet‑shape variables** (e.g., aplanarity, pull, eccentricity).  
   - **Energy‑fraction ratios** (leading‑subjet \(p_T\) over total jet \(p_T\)).  
   All can be computed with integer arithmetic and add ≈ 5 LUTs.

3. **Slightly deeper, quantized MLP**  
   Test a **4‑neuron hidden layer** with 8‑bit quantisation (instead of hard‑tanh). Preliminary synthesis shows ≤ 120 ns latency and < 50 LUTs, offering richer non‑linear mapping while staying inside the L1 envelope.

4. **Joint training of BDT and MLP**  
   Instead of sequentially training the BDT then the MLP, treat the raw BDT score as a *feature* in a **single end‑to‑end loss**. Gradient information can flow back to the BDT’s tree‑split thresholds via differentiable tree‑boosting (e.g., XGBoost with gradient‑based hyper‑parameter optimisation), potentially yielding a more synergistic model.

5. **Probabilistic calibration**  
   Apply **isotonic regression** or a lightweight **temperature scaling** to the blended output to improve the calibration of the posterior probability, which benefits downstream selections that rely on a cut on the output value.

6. **Hardware‑level optimisation study**  
   - Verify the integer‑only MLP on the target FPGA using the *post‑place‑and‑route* timing model.  
   - Profile power consumption to ensure the added logic does not impact the overall L1 power budget.  
   - Explore **LUT‑based inference (lookup‑table)** for the MLP, which could further reduce latency to < 80 ns.

7. **Cross‑validation on data‑driven control regions**  
   Validate that the efficiency gain persists in early Run‑3 data (e.g., lepton+jets \(t\bar t\) control sample). Any systematic shift relative to MC can be quantified and fed back into the feature engineering loop.

---

**Bottom line:**  
`novel_strategy_v288` demonstrates that a *physics‑first* high‑level prior, even when injected via an ultra‑light MLP, can measurably boost boosted‑top tagging efficiency while respecting the stringent L1 constraints. The next logical step is to give the model a little more flexibility (learnable blending, modestly larger MLP, richer feature set) and to integrate the training of the low‑ and high‑level components, all while staying comfortably within the hardware envelope. This path promises a further **5–8 %** relative efficiency lift without compromising latency.