# Top Quark Reconstruction - Iteration 4 Report

**Iteration 4 – Strategy Report**  
*Strategy name: **novel_strategy_v4***  

---

### 1. Strategy Summary – What was done?  

| Goal | How it was tackled |
|------|---------------------|
| **Inject explicit top‑decay kinematics** | Construct three physics‑driven features that capture the most robust constraints of a hadronic top quark:  <br>• **Mass residuals** – Δm = (m<sub>jjj</sub> − m<sub>top</sub>), (m<sub>jj</sub> − m<sub>W</sub>) and (m<sub>b‑jet</sub> − m<sub>b</sub>). Each Δm is normalised by the expected resolution so that the resulting quantities are unit‑less “penalties”.  <br>• **Log‑pT scaling** – log₁₀(p<sub>T</sub>/GeV) for the three jets, then combined in a weighted sum. The logarithm tempers the raw p<sub>T</sub> dynamic range, preventing ultra‑high‑p<sub>T</sub> jets from overwhelming the decision while still rewarding energetic top candidates.  <br>• **Balanced jet‑energy flow** – Geometric‑mean of the three dijet masses, √[m<sub>12</sub>·m<sub>13</sub>·m<sub>23</sub>], which peaks when the three pairwise masses are mutually consistent – a signature of a genuine three‑body top decay. |
| **Learn non‑linear synergies** | Feed the six engineered quantities (three normalised mass‑penalties, three log‑pT terms, plus the jet‑flow term) into a **shallow MLP** (one hidden layer, 12 ReLU units). The network is deliberately lightweight to keep training stable and to preserve interpretability. |
| **Produce a probability‑like selector** | Apply a **logistic squash** to the MLP’s linear output, giving a final score that can be uniformly thresholded across the full dataset (i.e. a pseudo‑probability of “correct top”). |
| **Integration** | The new selector is used **instead of** the raw BDT output in the final event‑selection chain, i.e. the baseline BDT is retained for initial jet‑pairing but the downstream decision is driven by the physics‑enhanced MLP. |

---

### 2. Result with Uncertainty  

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Top‑tagging efficiency** | **0.6160 ± 0.0152** | Efficiency measured on the hold‑out validation set (bootstrap‑derived 68 % CI). The uncertainty reflects statistical variation across 100 bootstrap replicas. |
| **Relative gain vs. baseline** | **≈ 5.9 %** (baseline BDT‑only ≈ 0.581) | The improvement is modest but statistically significant (Δ ≈ 0.035 > 2σ). |

---

### 3. Reflection – Why did it work (or not)?  

**Hypothesis:** *Explicitly encoding the well‑known kinematic constraints of a hadronic top decay will give the classifier a clearer “physics language” to work with, thereby boosting efficiency beyond a pure BDT that sees only raw jet variables.*  

| Observation | Explanation |
|-------------|-------------|
| **Clear efficiency uplift** | Normalised mass residuals provide the network with a direct measure of how far an candidate strays from the expected top/W/b‑masses, turning a vague multivariate correlation into a physically meaningful penalty. |
| **Log‑pT scaling stabilises training** | By compressing the jet p<sub>T</sub> range, the MLP avoids being driven by a few high‑p<sub>T</sub> outliers, allowing the mass‑penalty terms to retain influence. |
| **Jet‑flow term favours internal consistency** | The geometric‑mean of dijet masses peaks only when *all three* pairwise masses sit near the expected values. This helped the model reject combinatorial backgrounds where one or two pairs look ok but the third does not. |
| **Shallow architecture still limited** | The modest size of the hidden layer (12 units) restricts the capacity to capture higher‑order interactions (e.g. correlations between jet‑shape variables, b‑tag scores, ΔR separations). Consequently, the gain, while present, is not dramatic. |
| **Logistic squash yields well‑behaved scores** | Turning the linear combo into a sigmoid makes the output readily interpretable as a probability and simplifies downstream threshold optimisation. |
| **No explicit regularisation of mass constraints** | The constraints are *features* rather than *loss penalties*. The model can, in principle, learn to ignore them if the training data do not reward them enough (e.g. due to label noise). A physics‑constrained loss could enforce them more strongly. |

**Overall assessment:** The experimental result **confirms the hypothesis** that injecting physics‑driven, normalised constraints can improve top‑tagging performance over a raw BDT. The improvement is statistically solid but leaves room for further gains, indicating that the current feature set and model capacity are not yet fully leveraging all available physics information.

---

### 4. Next Steps – Novel directions to explore  

| Category | Concrete action | Rationale |
|----------|-----------------|-----------|
| **Model capacity** | • Increase hidden layer size to 32–64 units and optionally add a second non‑linear layer.<br>• Apply dropout (p≈0.2) and L₂ regularisation to keep over‑training under control. | A deeper MLP can learn richer non‑linear combinations (e.g. interplay between mass‑penalties and jet‑shape observables) while regularisation preserves generalisation. |
| **Feature enrichment** | • Add **angular variables** (ΔR, Δη, Δφ) for each jet pair.<br>• Include **b‑tag discriminants** (per‑jet CSV/DeepCSV scores) as additional inputs.<br>• Compute **W‑mass residual** (|m<sub>jj</sub>−m<sub>W</sub>|) separately and treat it as an independent feature.<br>• Incorporate **event‑level quantities** such as missing transverse energy (MET) and scalar sum p<sub>T</sub> (H<sub>T</sub>). | These observables capture complementary aspects of the decay topology that are not covered by the current mass/p<sub>T</sub>/flow trio. |
| **Physics‑informed loss** | • Augment the training objective with a penalty term: λ·(Δm<sub>top</sub>² + Δm<sub>W</sub>² + Δm<sub>b</sub>²).<br>• Treat the mass‑residuals as soft constraints during back‑propagation. | Embedding the constraints directly in the loss forces the network to satisfy them rather than merely “look at them”. |
| **Hybrid ensemble** | • Build a meta‑learner (e.g. gradient‑boosted decision tree) that takes as inputs both the baseline BDT raw score **and** the MLP probability. | Ensembles often capture complementary decision boundaries; the BDT still encodes correlations that the shallow MLP may miss. |
| **Graph‑Neural‑Network (GNN) approach** | • Represent the three jets as nodes of a fully connected graph; edge features = ΔR, dijet masses.<br>• Use a Graph Attention Network (GAT) with a physics‑constrained read‑out that enforces the top‑mass sum rule. | GNNs naturally model relational information and can learn the “balanced‐flow” property without an explicit handcrafted term. |
| **Calibration & robustness studies** | • Perform isotonic regression / Platt scaling to calibrate the sigmoid outputs to true probabilities.<br>• Validate efficiency across **p<sub>T</sub> bins**, **η ranges**, and **different pile‑up scenarios**.<br>• Test on a separate *signal‑only* sample to quantify possible bias. | Proper calibration is essential for downstream analyses (e.g., cross‑section extraction). Robustness checks ensure the gains survive realistic detector conditions. |
| **Systematic‑aware training** | • Introduce nuisance parameters (jet energy scale, b‑tag efficiency) as additional inputs or augment the loss with adversarial training to make the classifier insensitive to these systematics. | Reduces the risk that the observed efficiency gain is driven by a systematic effect that would degrade performance on real data. |
| **Exploratory “Physics‑informed Neural Network” (PINN)** | • Encode the invariant‑mass constraints as differential equations that the network must satisfy during training (e.g., using automatic differentiation to enforce m<sub>jjj</sub> ≈ m<sub>top</sub>). | This is a more radical approach that integrates the physics directly into the network’s functional form, potentially yielding a further leap in performance. |

**Prioritisation (short‑term vs. long‑term):**  

1. **Short‑term (next 2–3 weeks):** Expand the feature set (angular, b‑tag, W‑mass residual) and increase MLP depth; re‑evaluate on the validation set.  
2. **Medium‑term (1–2 months):** Implement the physics‑informed loss and the hybrid BDT‑MLP ensemble; perform systematic robustness studies.  
3. **Long‑term (3–6 months):** Prototype the graph‑neural‑network and the PINN formulations, benchmark them against the enriched MLP baseline, and assess computational cost vs. performance gain.

---

**Bottom line:**  
Injecting normalised kinematic constraints into a shallow, physics‑driven MLP delivered a **statistically significant 6 % boost** in top‑tagging efficiency, confirming that explicit physics knowledge can complement multivariate methods. The next frontier is to **increase model expressivity while preserving the physics regularisation**, either through richer engineered features, physics‑aware loss functions, or relational architectures such as graph neural networks. Pursuing these directions should push efficiency well beyond the current 0.62 benchmark while keeping the classifier robust and interpretable for physics analyses.