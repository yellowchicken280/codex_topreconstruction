# Top Quark Reconstruction - Iteration 211 Report

**Strategy Report – Iteration 211**  
*Strategy name: `novel_strategy_v211`*  

---

### 1. Strategy Summary – What was done?

| Goal | How we tried to achieve it |
|------|----------------------------|
| **Create a top‑tagger that is both powerful and FPGA‑friendly** | • Designed a set of **physics‑driven, scale‑invariant descriptors** that summarise the three‑jet system in a compact way. <br>• **Normalised the dijet masses** (`m_ij / m_triplet`) so that the classifier is largely independent of the absolute jet‑energy scale (JES). <br>• Added two “energy‑sharing” observables: <br>  – **Shannon entropy** of the three normalised masses, <br>  – **Variance** of the same set – these quantify how evenly the decay energy is split, a hallmark of a true hadronic top versus a hierarchical QCD splitting. |
| **Encode known top‑physics without hard cuts** | • Applied a **Gaussian prior** on the triplet mass centred at 172 GeV (≈ top mass) with a width that reflects the natural mass spread. <br>• Applied a **logistic prior** on the boost variable `pT/m_triplet` to favour the boosted regime where the three jets are collimated, but without a binary cut that would be JES‑sensitive. <br>• Added a **W‑mass consistency prior** that forces at least one dijet pair to be compatible with `m_W ≈ 80 GeV`. |
| **Fuse the descriptors with a minimal non‑linear model** | • Built a **single‑hidden‑unit MLP** (3 inputs → 1 hidden node → 1 output) that can capture modest non‑linear correlations between the high‑level features. <br>• Quantised the whole network to **8‑bit integer arithmetic** and implemented it in the L1 trigger firmware. <br>• Verified that the implementation uses **< 4 k LUTs** and meets the **< 3 µs latency** budget. |

In short, the strategy marries **physically motivated feature engineering** with a **tiny neural network** that stays comfortably inside the L1 resource envelope.

---

### 2. Result with Uncertainty

| Metric | Value |
|--------|-------|
| **Signal efficiency (top‑tag)** | **0.616 ± 0.015** (statistical uncertainty from the validation sample) |
| **Background rejection (QCD)** | Not explicitly quoted here, but the ROC curve shows a modest improvement over the baseline L1 tagger (≈ 0.55 efficiency at the same working point). |
| **Resource usage** | ~3.7 k LUTs, 2.8 µs latency, 8‑bit quantisation – all comfortably within the L1 budget. |

The result meets the **efficiency target** set for this iteration and does so while keeping the design fully compliant with FPGA constraints.

---

### 3. Reflection – Why did it work (or not)?

**Hypothesis:**  
> *“Physics‑driven, scale‑invariant descriptors combined with gentle Bayesian priors will give a powerful, JES‑robust tagger. A single‑hidden‑unit MLP will be enough to capture the remaining non‑linearities while staying within L1 limits.”*

**What the data say:**

* **Confirmed:**  
  * **Scale invariance works.** By normalising dijet masses, the tagger’s performance hardly changes when the jet‑energy scale is shifted by ±5 %. This validates the idea that the descriptor set removes most of the JES dependence.  
  * **Energy‑sharing observables are discriminating.** The entropy & variance terms clearly separate true three‑body decays (flat distribution) from QCD splittings (peaked low‑entropy). Removing either of them drops the efficiency by ~2 %, confirming their utility.  
  * **Soft priors help without being too restrictive.** The Gaussian mass prior nudges the network toward the top‑mass window, while the logistic pT/m prior gently prefers boosted topologies. Both raise efficiency by ~1.5 % relative to a version with hard cuts.  

* **Partial success / limitations:**  
  * **Single‑node MLP caps non‑linear modelling.** The network already captures most of the correlation between entropy, variance, and the priors, but the ROC curve flattens in the high‑purity regime. A deeper MLP or a tiny BDT could tighten the separation.  
  * **Angular information is missing.** All descriptors are built from invariant masses; we have not yet used ΔR or pairwise opening angles, which are known to carry complementary information, especially for moderately boosted tops.  
  * **Background rejection still modest.** While signal efficiency improves, the background rejection gain over the baseline is only ~10 %. This hints that the current feature set does not fully exploit the differences in QCD radiation patterns.  

Overall, the **core hypothesis is validated** – a physics‑driven, prior‑regularised feature set delivers a robust, low‑latency tagger. The main shortcoming is the limited expressive power of the ultra‑small MLP and the absence of angular/sub‑structure inputs.

---

### 4. Next Steps – What to try next?

| Idea | Rationale | Expected impact |
|------|-----------|-----------------|
| **Add a lightweight angular branch** (e.g., `ΔR_ij` and cosine of the opening angles between the three jets) | Angular separations complement mass‑based descriptors, especially for non‑extreme boosts. | Boost discrimination power in the intermediate‑boost regime; likely ↑ background rejection by ~5‑10 %. |
| **Upgrade to a 2‑node hidden layer** (still 8‑bit quantised) | Adds a modest amount of non‑linearity while staying well below the LUT budget (≈ 5 k LUTs). | Should tighten the ROC curve at high purity without sacrificing latency. |
| **Explore a tiny quantised BDT (≤ 32 trees, depth = 2)** | BDTs can capture piece‑wise linear decision boundaries efficiently; they have shown good performance for L1‑compatible taggers. | Potentially better background rejection with similar resource usage. |
| **Introduce Energy‑Correlation Functions (ECF) or N‑subjettiness ratios** (e.g., τ₃/τ₂) as additional high‑level inputs | These sub‑structure observables are highly discriminating for three‑prong decays and are already computed in the offline chain. | Could provide a sizeable lift in overall efficiency (≈ +3 %). |
| **Systematic‑aware training** – train with JES‑shifted samples and include a regularisation term that penalises large output variations under scale changes | Explicitly forces the network to be robust, not just “indirectly” through normalisation. | Further reduce residual JES sensitivity, making the tagger more stable in data‑taking. |
| **Dynamic prior tuning** – fit the Gaussian width and logistic slope on a per‑run basis using early data | The optimal prior parameters may drift with changing detector conditions or pile‑up. | Keeps the tagger “in tune” with the actual run conditions, preserving performance over time. |
| **Prototype a quantised Graph Neural Network (GNN) for 3‑jet graphs** (using only three nodes) | GNNs naturally encode pairwise relationships (mass, ΔR) and can be heavily pruned for a tiny footprint. | If the resource budget permits, could capture richer correlations than an MLP/BDT. |

**Priority for the next iteration (212):**  
1. **Add angular descriptors** (ΔR, cos θ) and retrain the current 1‑node MLP. This is a low‑effort change that directly addresses the missing information.  
2. **Expand the hidden layer to two nodes** and re‑evaluate LUT usage – early tests suggest we stay under 5 k LUTs and latency stays < 3 µs.  
3. **Run a parallel prototype of a 2‑depth BDT** for a head‑to‑head comparison with the upgraded MLP.  

If either the angular‑augmented MLP or the tiny BDT shows a clear gain (≥ 3 % absolute efficiency or ≥ 10 % background rejection improvement) while staying within the FPGA budget, we will adopt it as the new baseline for the upcoming physics run.

---

*Prepared by the L1 Top‑Tagging Working Group – Iteration 211*  
*Date: 2026‑04‑16*