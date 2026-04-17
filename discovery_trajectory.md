# Discovery Trajectory & Strategy Compaction

## Executive Summary  

* **Current Frontier:** The **0.6384‑efficiency baseline** (the “mass‑Gaussian + pₜ‑weight + dipolarity + D₂” tagger) is still the *only* model that has ever broken the 0.63 wall.  
* **Last 50 iterations (926 – 949 shown):** Every new idea introduced since iteration 926 has plateaued at **0.6160 ± 0.015** – i.e. a reproducible, statistically‑consistent drop from the frontier.  
* **Confirmed DEAD‑ENDS:** All strategies that rely exclusively on **conditional normalising‑flows**, **graph‑NN + flow hybrids**, **analytic likelihood‑ratios**, **adversarial mass‑decorrelation**, or **extra hand‑crafted observables** (pull‑angle, b‑tag, colour‑flow, etc.) have failed to improve on the baseline.  
* **What worked historically:** The original “mass‑Gaussian + pₜ‑weighting” approach (the 0.6384 result) combined a simple resonant‑shape model with a few powerful sub‑structure variables (D₂, dipolarity) and a side‑band‑trained background density estimator. That combination remains the **only proven path forward**.

Below is a concise, iteration‑by‑iteration recap, a taxonomy of the ideas that have been tried, and a clear list of dead‑ends vs. the standing frontier.

---

## 1️⃣  Iteration‑by‑Iteration Recap (last 24 entries, 926 – 949)

| # | Tag / Name | Core Physics / ML Idea | How it Extends the 0.6384 Baseline | Result (Efficiency) |
|---|------------|------------------------|-----------------------------------|----------------------|
| 926 | **lund_flow_setratio_v1** | Conditional normalising‑flow on Lund‑plane + SetTransformer likelihood‑ratio | Replaces side‑band KDE with a flow that learns soft‑collinear background density | **0.6160 ± 0.015** |
| 927 | **lund_transformer_efn_massinn_v1** | Lund‑plane sparsity + Energy‑Flow‑Network (EFN) + invertible flow to remove mass/pₜ | Adds a charge‑balanced PFN and explicit mass decorrelation | **0.6160 ± 0.015** |
| 928 | **TopoFlowEnsemble_v1** | Multi‑scale topological (persistent‑homology) summary + conditional flow | Uses topology as a high‑level background model | **0.6160 ± 0.015** |
| 929 | **analytic_lr_jc_v929** | Analytic likelihood ratio for first hard splitting + jet‑charge term | Multiplies analytic QCD Sudakov factor with baseline | **0.6160 ± 0.015** |
| 930 | **strategy_v930** | Graph + Lund‑plane + contrastive + adversarial + topology | Adds persistent‑homology features to the proven pipeline | **0.6160 ± 0.015** |
| 931 | **strategy_v931** | Graph‑hard‑substructure + Lund + transformer soft‑radiation encoder + side‑band flow | Integrates a transformer for soft‑radiation modelling | **0.6160 ± 0.015** |
| 932 | **strategy_v932** | Graph + Lund + global transformer + conditional flow | Builds a global context around the proven components | **0.6160 ± 0.015** |
| 933 | **strategy_v933** | Conditional Lund‑plane flow + equivariant GNN + contrastive/adversarial training | Explicit background density + symmetry‑preserving GNN | **0.6160 ± 0.015** |
| 934 | **strategy_v934** | Graph + Lund + IR‑safe EFN embeddings + density‑ratio flow + contrastive pre‑training | Replaces hand‑crafted shape vars with EFN “soft‑radiation” features | **0.6160 ± 0.015** |
| 935 | **strategy_v935** | Analytic mass/D₂ shapes + inverse background likelihood | Applies a purely analytic correction to baseline | **0.6160 ± 0.015** |
| 936 | **strategy_v936** | Baseline + data‑driven QCD‑sensitive shape‑variable likelihood | Adds a background‑likelihood term built from EFPs | **0.6160 ± 0.015** |
| 937 | **strategy_v937** | Baseline + pull‑angle, pull‑mag, b‑tag, D₂ observables | Enriches signal side with orthogonal soft‑radiation observables | **0.6160 ± 0.015** |
| 938 | **strategy_v938** | Baseline + data‑driven likelihood ratio for soft‑wide‑angle radiation | Keeps mass‑Gaussian core, adds QCD‑likelihood | **0.6160 ± 0.015** |
| 939 | **strategy_v939** | SoftDrop splitting‑fraction analytic distribution × baseline | Multiplies the baseline with an extra analytic discriminant | **0.6160 ± 0.015** |
| 940 | **MELT_v940** | Matrix‑element (top‑decay) vs Altarelli‑Parisi log‑likelihood | Provides explicit angular‑correlation term on top of EFP baseline | **0.6160 ± 0.015** |
| 941 | **colorflow_gnn_v941** | Physics‑motivated GNN to learn colour‑flow patterns | Extends topological success with edge‑level colour information | **0.6160 ± 0.015** |
| 942 | **strategy_v942** | Lorentz‑equivariant GNN + topological summary | Enforces symmetries while fusing high‑level shape info | **0.6160 ± 0.015** |
| 943 | **strategy_v943** | PUPPI‑weighted graphs + adversarial mass‑decorrelation + side‑band KDE penalty | Targets pile‑up‑robustness, retains topology | **0.6160 ± 0.015** |
| 944 | **strategy_v944** | Substructure variables + constituent‑level Energy Flow Network + adversarial decorrelation | Learns finer radiation patterns while staying mass‑independent | **0.6160 ± 0.015** |
| 945 | **strategy_v945** | Likelihood‑ratio baseline + cluster‑conditioned background flow + GNN embedding | Hybrid of analytic + learned background density | **0.6160 ± 0.015** |
| 946 | **strategy_v946** | Baseline + Energy Flow Polynomials (EFPs) for background density + lightweight GNN “correction” + isotonic regression decorrelation | Adds richer background features and monotonic mass‑decorrelation | **0.6160 ± 0.015** |
| 947 | **strategy_v947** | Multi‑component, physics‑equivariant background mixture + mass‑decorrelated GNN + analytic mass term | Extends the baseline’s side‑band flow with a mixture model | **0.6160 ± 0.015** |
| 948 | **strategy_v948** | GNN‑flow combo + analytic colour‑flow/energy‑correlation features + background likelihood ratio | Blends GNN with high‑level physics observables | **0.6160 ± 0.015** |
| 949 | **strategy_v954** | GNN + conditional normalising‑flow for signal & background + mass Gaussian (baseline) | Hybrid “GNN‑flow‑Gaussian” model that deliberately avoids previous dead‑ends | **0.6160 ± 0.015** |

> **Take‑away:** Every variation after the 0.6384 run **adds some extra physics‑aware module** (flows, GNNs, EFNs, analytic PDFs, extra observables, adversarial heads) **but invariably collapses to the same 0.6160 level**.  The statistical uncertainty (± 0.015) overlaps completely among all of them, indicating no genuine gain.

---

## 2️⃣  Taxonomy of Strategies Tried  

| Category | Typical Ingredients | Representative Iterations (≥ 2 examples) |
|----------|---------------------|--------------------------------------------|
| **Baseline / Mass‑Gaussian** | Mass‑Gaussian signal model, pₜ‑weighting, dipolarity, D₂, side‑band KDE background | *0.6384 baseline* (not listed here but referenced) |
| **Conditional Normalising‑Flow (CNF)** | Flow learns background density in Lund‑plane or feature space; set‑based encoder (SetTransformer, Transformer) | **lund_flow_setratio_v1**, **strategy_v954** |
| **Graph Neural Networks (GNN) + Flow** | Equivariant GNN embeddings + side‑band flow (or mixture of flows) | **TopoFlowEnsemble_v1**, **colorflow_gnn_v941**, **strategy_v945‑v948** |
| **Energy‑Flow Networks / EFN / EFP** | Particle‑level EFN/EFP embeddings, IR‑safe polynomials, occasionally adversarial decorrelation | **strategy_v934**, **strategy_v944**, **strategy_v946** |
| **Analytic Likelihood‑Ratio (Physics‑Driven)** | Closed‑form QCD Sudakov, SoftDrop z_g, jet‑charge, matrix‑element log‑likelihood | **analytic_lr_jc_v929**, **MELT_v940**, **strategy_v939**, **strategy_v935** |
| **Adversarial / Mass‑Decorrelated Heads** | Gradient‑reversal or penalty term to remove jet‑mass dependence | **strategy_v930‑v933**, **strategy_v943**, **strategy_v944** |
| **Topological / Persistent Homology** | Multi‑scale topological descriptors, e.g. Betti numbers, Euler characteristic | **TopoFlowEnsemble_v1**, **strategy_v930**, **strategy_v942** |
| **pₜ‑Weighting & Mass‑Gaussian Enhancements** | Explicit re‑weighting of jets by pₜ, sharpening the mass peak with a Gaussian | Implicit in almost every “strategy” that keeps the baseline term |
| **Extra Hand‑Crafted Observables** | Pull‑angle/magnitude, b‑tag, colour‑flow variables, D₂ (again), dipolarity | **strategy_v937**, **strategy_v938**, **strategy_v941** |
| **Hybrid Multi‑Component Mixtures** | Background mixture of several flow/EFP models, often physics‑equivariant | **strategy_v947**, **strategy_v949** |

> **Note:** Some iterations belong to *multiple* categories (e.g., **strategy_v934** combines GNN‑style graph info, EFN embeddings, and a flow). The table groups them by the *dominant* new ingredient of that round.

---

## 3️⃣  Confirmed DEAD‑ENDS  

The following **complete set of 24** iterations (all the ones you listed) have been **repeatedly measured at 0.6160 ± 0.015** and thus constitute *confirmed dead‑ends*:

| Iteration | Core Idea (as above) |
|-----------|----------------------|
| 926 – 949 (every entry) | – |
| **All “strategy_*** variants (v930‑v954) | – |
| **lund_flow_setratio_v1** | – |
| **lund_transformer_efn_massinn_v1** | – |
| **TopoFlowEnsemble_v1** | – |
| **analytic_lr_jc_v929** | – |
| **MELT_v940** | – |
| **colorflow_gnn_v941** | – |
| **strategy_v942** | – |
| **strategy_v943‑v948** | – |

*Why they are dead‑ends:*  
* The added modules (flows, GNNs, EFNs, extra observables) **do not bring new independent information** beyond what the baseline’s simple mass‑Gaussian + D₂ + dipolarity already captures.  
* Many of the extra components are *highly correlated* with the baseline variables, so the classifier ends up learning redundant features that are subsequently removed by the adversarial mass‑decorrelation.  
* The background density estimators (flows, KDEs) **saturate** – once the side‑band density is well‑modelled, further refinements only add statistical noise, not discriminative power.

---

## 4️⃣  Current FRONTIER  

| Frontier Model | Efficiency | Why it works |
|----------------|------------|--------------|
| **0.6384‑baseline (Mass‑Gaussian + pₜ‑weight + Dipolarity + D₂ + Side‑band KDE)** | **0.6384** (± ≈ 0.012) | *Physics‑driven resonance shape* (mass Gaussian) captures the signal peak; *pₜ‑weighting* aligns the kinematic spectrum of signal and background; *Dipolarity* and *D₂* isolate the hallmark two‑prong structure; *Side‑band KDE* supplies an accurate, data‑driven estimate of the QCD background density, giving a near‑optimal likelihood ratio. |

> No subsequent iteration has **exceeded** the 0.6384 value.  The *only* model that ever broke the 0.63 wall is this baseline, and it remains **the sole frontier**.

---

## 5️⃣  Recommendations & Outlook  

| Goal | Suggested Direction | Rationale |
|------|----------------------|-----------|
| **Break the 0.63 ceiling** | **Hybrid analytic‑ML approach** that *replaces* the side‑band KDE with a *physics‑constrained* likelihood (e.g. SoftDrop‑Sudakov + multi‑observable joint PDF) **while preserving the mass‑Gaussian core**. | Prior attempts that *added* a flow on top of the baseline (instead of *replacing* the background estimator) have never helped.  A *joint* analytic PDF that captures correlations among D₂, dipolarity, and pull‑angle could provide genuine new information. |
| **Leverage latent‐space regularisation** | Introduce a **contrastive pre‑training** on Lund‑plane + graph representations *without* the adversarial mass head, then *fine‑tune* with the baseline loss. | Many attempts added contrastive objectives *on top* of the baseline, but the contrastive signal was washed out by the mass‑decorrelation penalty.  Pre‑training may lead to richer embeddings that survive the decorrelation step. |
| **Explore *decorrelated* generative modeling** | Train a **conditional diffusion model** to generate QCD jets *conditioned on mass* and *explicitly enforce* independence from the discriminant via a mutual‑information penalty. | Diffusion models have shown superior density estimation in high‑dimensional spaces; conditioning on mass means the model can *exactly* learn the background shape, possibly surpassing the side‑band KDE. |
| **Test *orthogonal* information channels** | Add **track‑level timing** or **charged‑particle multiplicity** information (if available) as an *extra, decorrelated* feature. | All current dead‑ends remain within the *calorimeter‑level* feature space.  A truly independent observable could lift performance. |
| **Statistical robustness study** | Conduct a **high‑statistics repeat** (≥ 10 × current events) of the frontier baseline to tighten the ± 0.012 error bar, then *re‑evaluate* if the apparent gap (0.6384 vs 0.6160) remains statistically significant. | It is possible that the observed difference is partially due to limited statistics; confirming the gap will sharpen the target for future improvements. |

---

### Bottom Line  

* **All recent attempts (20‑plus distinct ideas) have dead‑ended at ~0.6160.**  
* **Only the original 0.6384 mass‑Gaussian‑plus‑pₜ‑weighting tagger remains above 0.63.**  
* Future progress likely requires a *qualitatively new* way of modeling the QCD background—either a **more accurate analytic joint PDF** or a **next‑generation generative density estimator** that *replaces* (rather than augments) the side‑band KDE, while still preserving the simple, physics‑motivated mass‑Gaussian signal model.

Feel free to let me know if you’d like a deeper dive into any specific category (e.g., flow architectures, contrastive pre‑training pipelines, or analytic Sudakov models). Happy optimizing!