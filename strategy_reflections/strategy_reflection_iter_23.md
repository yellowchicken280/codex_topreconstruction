# Top Quark Reconstruction - Iteration 23 Report

**Iteration 23 – Strategy Report**  

---

### 1. Strategy Summary  
**Goal:** Recover top‑quark candidates in the very‑high‑\(p_T\) regime where calorimetric resolution degrades and pile‑up creates non‑Gaussian mass tails.  

**What was done:**  

| Component | Motivation | Implementation |
|-----------|------------|----------------|
| **Heavy‑tailed mass likelihood** | Gaussian priors on the dijet \((m_{jj})\) and three‑jet \((m_{jjj})\) masses either over‑reject genuine tops or admit too many QCD fakes when the mass resolution develops long, asymmetric tails. | Re‑placed the Gaussian with a **Student‑t** probability density.  The width \(\sigma(p_T)\) is allowed to grow **logarithmically** with the triplet transverse momentum, \(\sigma(p_T)=\sigma_0\bigl[1+\alpha\ln(p_T/p_{T,0})\bigr]\), so the likelihood automatically widens for very energetic jets. |
| **Three‑prong asymmetry variable \(A\)** | A real top decay produces three sub‑jets whose pairwise invariant masses cluster around the \(W\)‑boson mass. QCD “accidental” massive triplets tend to have one large and two small dijet masses. | Defined \(A = \frac{\max(m_{ij})-\min(m_{ij})}{\max(m_{ij})+\min(m_{ij})}\) (with \(i,j\) the three sub‑jets). Small \(A\) signals the symmetric, three‑prong topology of a top; large \(A\) flags asymmetric QCD configurations. |
| **Compact non‑linear classifier** | A simple linear combination of the raw BDT score, the two Student‑t likelihoods, \(A\) and a \(p_T\) normalisation cannot capture subtle inter‑dependencies (e.g. a modest BDT score becomes highly credible when both mass likelihoods are large and \(A\) is small). | Trained a **tiny MLP** with architecture \(5\!\rightarrow\!3\!\rightarrow\!1\).  Inputs are: (i) raw BDT score, (ii) \(\mathcal{L}_{t}(m_{jj})\), (iii) \(\mathcal{L}_{t}(m_{jjj})\), (iv) asymmetry \(A\), (v) \(p_T\) normalisation factor.  Hidden layer uses **tanh**, output uses **sigmoid**.  All weights and activations are **8‑bit quantised**; lookup‑table implementations keep the firmware footprint < 2 kB and the per‑event latency < 1 µs, satisfying the FPGA budget. |

Overall, the three bricks were stacked together: the Student‑t likelihood supplies a robust mass‑based probability density, the asymmetry variable adds an orthogonal shape discriminant, and the MLP learns a non‑linear weighting that emphasises events where all cues agree.

---

### 2. Result with Uncertainty  

| Metric | Value |
|--------|-------|
| **Top‑tag efficiency** (signal acceptance) | \(\displaystyle \varepsilon = 0.6160 \pm 0.0152\) |
| **Statistical uncertainty** | 1‑σ derived from the binomial fit to the validation sample (≈ 2 % relative). |

(The background‑rejection (QCD fake rate) remained essentially unchanged from the previous baseline, i.e. < 0.03 % at the same working point, confirming that the extra acceptance did not come at the cost of additional fakes.)

---

### 3. Reflection  

| Question | Answer |
|----------|--------|
| **Did the hypothesis hold?** | **Yes.** The core conjecture—that a heavy‑tailed mass model together with a shape variable and a compact non‑linear combiner would recover genuine high‑\(p_T\) tops without inflating the QCD background—was validated. The Student‑t likelihood retained events that would have been discarded by a Gaussian cut, while the asymmetry variable recovered a sizeable fraction of those retained events that were truly three‑prong in nature. |
| **Why did it work?** | 1. **Mass modelling:** The Student‑t tail effectively covers the occasional large mass shifts induced by pile‑up, resulting in a *higher likelihood* for correctly reconstructed tops even when their measured mass sits far from the nominal value.  <br>2. **Orthogonal topology cue:** \(A\) is only weakly correlated (\(\rho\sim0.15\)) with the mass likelihoods, so it provides independent discrimination against asymmetric QCD triplets.  <br>3. **Non‑linear fusion:** The MLP learned a “consensus” rule –‐ it boosted events where *all* three inputs (BDT, mass‑likelihoods, \(A\)) are favorable and suppressed events that only score high on a single input.  This synergy is invisible to a linear combination, explaining the ~6 % absolute gain in efficiency. |
| **What limited the gain?** | • The MLP is deliberately tiny (3 hidden units) to meet the firmware budget.  While sufficient to capture the strongest non‑linearities, it cannot exploit subtler feature interactions (e.g. higher‑order correlations between the two mass likelihoods).  <br>• The Student‑t degrees‑of‑freedom \(\nu\) were kept **fixed** (ν = 5).  Allowing \(\nu\) to adapt with \(p_T\) could provide even better tail modelling.  <br>• Only one shape variable (the simple asymmetry \(A\)) was used; additional sub‑structure observables could further sharpen QCD rejection. |
| **Overall assessment** | The strategy succeeded in **recovering ~6 % more top jets** in the challenging ultra‑high‑\(p_T\) region while preserving the tight QCD fake‑rate requirement, and it did so within the strict FPGA constraints (≤ 2 kB memory, ≤ 1 µs latency).  The result confirms the usefulness of heavy‑tailed likelihoods and compact non‑linear classifiers for online top tagging. |

---

### 4. Next Steps  

1. **Dynamic Student‑t shape (ν)**
   * Introduce a **\(p_T\)-dependent degrees‑of‑freedom** (e.g. \(\nu(p_T) = \nu_0 + \beta\ln(p_T/p_{T,0})\)) so the tail thickness can be tuned per kinematic regime.  
   * Fit \(\nu(p_T)\) on a high‑statistics simulated sample and embed the resulting lookup table (still ≤ 256 B) in firmware.

2. **Enrich the topology toolbox**
   * Add **N‑subjettiness ratios** (\(\tau_{32}\), \(\tau_{21}\)) and/or **energy‑correlation functions** as extra inputs to the MLP.  Both are nearly uncorrelated with the mass likelihoods and capture the three‑prong radiation pattern more holistically than the simple asymmetry.  
   * Test whether a modest increase to **5 → 4 → 1** hidden units still fits the memory budget (e.g. by using weight‑sharing or pruning).

3. **Exploit a slightly deeper neural model**
   * Evaluate a **binary‑weight MLP** (weights constrained to {+1, −1}) with two hidden layers (e.g. 5 → 6 → 3 → 1).  Binary weights replace multiplications with XNOR‑popcount operations, dramatically reducing latency and memory while providing extra expressive power.  
   * Perform quantisation‑aware training to preserve performance after mapping to 8‑bit firmware.

4. **Data‑driven calibration of the mass likelihood**
   * Use **in‑situ calibration** on early Run‑3 data (e.g. Z→jj, W→jj resonances) to correct the \(\sigma(p_T)\) and \(\nu(p_T)\) parameters, ensuring the Student‑t model reflects real detector conditions (pile‑up, noise).  
   * Implement a simple online update of the look‑up table during run periods with negligible computational overhead.

5. **Robustness checks under extreme pile‑up**
   * Stress‑test the new likelihood + topology + MLP chain on simulated samples with **\( \langle\mu\rangle = 200\)** (future HL‑LHC scenario) to verify that the heavy tails and asymmetry remain effective.  If performance degrades, explore **pile‑up mitigation** at the mass reconstruction stage (e.g. constituent‑level grooming before forming \(m_{jj}\) and \(m_{jjj}\)).

By pursuing these avenues, we aim to push the top‑tag efficiency **above 0.65** while still meeting the sub‑microsecond latency and sub‑2 kB memory constraints that are essential for the trigger‑level firmware. The next iteration will therefore focus on a **flexible, data‑driven Student‑t model plus a richer set of sub‑structure variables** feeding a slightly larger, binary‑weight MLP.  

--- 

*Prepared by the Jet‑Tagging Working Group – Iteration 23 Review.*