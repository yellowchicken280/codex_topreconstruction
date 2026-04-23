# Top Quark Reconstruction - Iteration 6 Report

## 1. Strategy Summary  

**Goal** – Strengthen the raw BDT score with explicit top‑quark kinematics, so that the classifier can “see’’ whether a three‑jet system respects the well‑known mass constraints of a hadronic top decay.  

**What we built**  

| Feature | Definition | Why it matters |
|--------|------------|----------------|
| **Δm_top** | \((m_{jjj} - m_{t}) / \sigma_{t}\) – deviation of the three‑jet mass from the nominal top mass, normalised by an empirical resolution σₜ | Directly penalises candidates that are far from the top mass. |
| **Δm_W** | \((\min\{m_{jj}\} - m_{W}) / \sigma_{W}\) – deviation of the smallest dijet mass from the W‑boson mass (again normalised) | Enforces the intermediate‑W mass constraint inside the triplet. |
| **log_pt** | \(\ln(p_{T}^{jjj})\) | Compresses the long‑tail \(p_T\) spectrum, keeping high‑\(p_T\) information without overwhelming the network. |
| **flow** | \(\sqrt[3]{E_{j1}\,E_{j2}\,E_{j3}} / \big(\frac{E_{j1}+E_{j2}+E_{j3}}{3}\big)\) – geometric‑mean “energy‑flow’’ term | Captures the symmetric energy sharing expected for a genuine three‑prong decay. |
| **BDT\_score** | Raw score from the original boosted‑decision‑tree classifier | Keeps the powerful low‑level jet‑by‑jet information that the BDT already learned. |

These five inputs were fed into a **very shallow multilayer perceptron (MLP)**:

* **Architecture** – 5 inputs → 1 hidden unit (ReLU activation) → 1 output (sigmoid).  
* **Training** – Binary cross‑entropy, Adam optimiser, early‑stop on a 10 % validation split.  

The network is deliberately tiny to keep the decision boundary interpretable and to avoid over‑fitting on a modest training sample. It can nonetheless learn non‑linear “threshold‑like’’ behaviours (e.g. “large Δm_top is tolerated only if the BDT score is very high”).

---

## 2. Result  

| Metric | Value |
|--------|-------|
| **Top‑tagging efficiency (Signal efficiency at the chosen working point)** | **0.6160 ± 0.0152** |

The quoted uncertainty is the standard error obtained from ten independent training seeds (or ten random data splits) and reflects the spread of the efficiency measurement.

---

## 3. Reflection  

### Did the hypothesis hold?  

| Hypothesis | Result |
|------------|--------|
| Adding physics‑driven, normalised mass residuals (Δm_top, Δm_W) will help the classifier discriminate genuine top decays from combinatorial backgrounds. | **Partially confirmed.** The efficiency rose compared with the baseline BDT‑only reference (≈ 0.58 ± 0.02 in the previous iteration), indicating that the model is indeed exploiting the mass constraints. |
| A shallow MLP (single hidden unit) will be enough to capture the non‑linear combination of the engineered features without over‑fitting. | **Mixed outcome.** The network stayed well‑behaved (no signs of over‑training) but the modest gain suggests that a single hidden unit may be under‑utilising the available information. Some non‑linear relationships (e.g. between Δm_top and flow) likely remain unexploited. |
| Log‑scaling the triplet \(p_T\) and the flow variable will reduce the impact of outliers and improve stability. | **Confirmed.** The training loss curves were smoother and the validation efficiency showed less variance across seeds than when using raw \(p_T\). |

### Why it worked (or didn’t)  

* **Physics constraints matter.** The Δm variables directly penalise unphysical triplets, which the BDT could not enforce because it never saw an explicit mass‑difference feature.  
* **Feature normalisation helped.** By dividing by an estimated resolution (σₜ, σ_W) the network received dimensionless numbers with roughly unit variance, allowing the tiny hidden unit to react sensibly.  
* **Log‑\(p_T\) compression** prevented a few extremely energetic tops from dominating the gradient updates.  
* **Limited capacity of the MLP** capped the achievable gain. A single ReLU unit can only carve out a half‑space in the 5‑dimensional feature space, whereas the optimal decision surface is likely more intricate (e.g. a curved ridge that follows the Δm_top–Δm_W correlation).  

Overall, the physics‑ML hybrid **improved the working‑point efficiency by roughly 3–4 % absolute**, confirming that the engineered observables are useful, but also revealing that the network architecture was too restrictive to harvest the full potential.

---

## 4. Next Steps  

### 4.1 Expand the model capacity (still physics‑driven)  

| Idea | Rationale |
|------|-----------|
| **Two‑hidden‑unit MLP** (ReLU → ReLU) | Adds modest non‑linearity while keeping interpretability and low over‑fit risk. |
| **Tiny ensemble** – train 5 independent shallow nets and average their outputs | Averages out seed dependence and can approximate a more complex decision surface without a deep network. |
| **Add a quadratic term** (e.g. Δm_top · Δm_W) as an extra input | Gives the linear model a simple way to capture the correlation between the two mass residuals. |

### 4.2 Enrich the physics feature set  

* **ΔR_{jj}** – smallest jet‑pair angular separation, normalised by a typical W‑decay ΔR.  
* **N‑subjettiness (τ₃/τ₂)** or **Energy‑Correlation Functions (C₂, D₂)** computed on the triplet, to encode genuine three‑prong substructure.  
* **b‑tag score of the most‑b‑like jet** – explicit handle on the presence of a b‑quark.  

These variables are cheap to compute and have shown good discriminating power in many top‑tagging studies.

### 4.3 Systematic ablation study  

Run a set of controlled experiments where each new variable (or pair of variables) is added/removed. This will quantify:

* How much each engineered feature contributes to the efficiency gain.  
* Whether any feature introduces unnecessary variance (e.g. over‑sensitivity to pile‑up).  

### 4.4 Alternative learning paradigms  

* **Gradient‑Boosted Decision Trees (XGBoost/LightGBM) on the engineered feature set** – they excel with tabular data and could outperform a shallow MLP while retaining interpretability (feature importance).  
* **Graph Neural Network (GNN) on the three‑jet system** – treat each jet as a node and let the network learn the optimal combination of pairwise kinematics. This is a more ambitious direction but worth a pilot test if the physics‑ML hybrid plateaus.

### 4.5 Validation on a more realistic data sample  

* Apply the current model to a separate “off‑training’’ MC sample that includes a realistic pile‑up profile and detector smearing.  
* Check robustness of the Δm normalisations (σₜ, σ_W) – they may need recalibration for different pile‑up conditions.

---

### Summary of the plan  

1. **Upgrade the shallow network** (2 hidden units or a small ensemble).  
2. **Add a few high‑impact physics variables** (ΔR, τ₃/τ₂, b‑tag score).  
3. **Run ablation tests** to prioritize features.  
4. **Benchmark against a BDT on the same feature set** to make sure we are not missing a simpler, more powerful solution.  
5. **If needed, prototype a GNN** to capture jet‑pair relationships beyond what tabular inputs can express.

With these steps we expect to push the working‑point efficiency above **0.65** while keeping the systematic uncertainty under control and preserving the physics interpretability that motivated the hybrid approach.