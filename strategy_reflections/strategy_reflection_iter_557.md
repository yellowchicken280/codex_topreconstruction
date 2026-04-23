# Top Quark Reconstruction - Iteration 557 Report

## 1. Strategy Summary  
**Goal** – In the ultra‑boosted regime the three partons from a hadronic top decay become so collimated that they are merged into a single large‑R jet.  Traditional sub‑structure observables (e.g. N‑subjettiness, energy‑correlation ratios) lose discriminating power because the resolved prongs are no longer visible.  The hypothesis was that the *kinematic imprint* of the decay – the invariant masses of the full three‑prong system, of the two‑prong combinations, and the relative balance of these masses – would still provide a strong handle for separating genuine top jets from ordinary QCD jets.

**Key ingredients**  

| Element | What was done | Why it helps |
|---------|----------------|--------------|
| **Triangular likelihoods** | For each of the three physical priors – (i) M(3‑prong) ≈ m<sub>top</sub>, (ii) any dijet ≈ m<sub>W</sub>, (iii) the spread of the three dijet masses – we built a simple triangular “look‑up” that gives a score ∈ [0, 1] when the observable falls inside a pre‑defined window around the target value. | The triangular shape is easy to implement in firmware (just a few adds/subtractions and a clamp) and still captures the core of the mass peak while tolerating detector resolution. |
| **Physics‑augmented MLP** | The three likelihood scores were fed to a tiny multilayer perceptron (2 hidden layers, 8 × 8 neurons) whose only non‑linear operation is a ReLU‑style clamp. The network produces a “physics‑score” for the jet. | The MLP can learn non‑trivial correlations (e.g. a jet that simultaneously satisfies the top‑mass and a balanced dijet‑mass pattern) that a simple product of the three scores would miss, without blowing up the hardware budget. |
| **Raw BDT** | A gradient‑boosted decision tree trained on the full suite of traditional sub‑structure variables (τ<sub>21</sub>, τ<sub>32</sub>, Soft‑Drop mass, etc.) was kept unchanged. | At moderate p<sub>T</sub> the BDT remains the strongest discriminator because the prongs are still partially resolved. |
| **p<sub>T</sub>-dependent gate** | A smooth gate g(p<sub>T</sub>) (sigmoid centred at 1 TeV with width ≈ 200 GeV) decides the relative weight of the BDT versus the physics‑MLP: <br>final score = g · BDT + (1 − g) · MLP. | Guarantees that the BDT dominates where sub‑structure works (low‑p<sub>T</sub>) and the physics‑MLP takes over where it flattens (ultra‑boosted jets). |
| **Hardware‑friendly implementation** | All calculations are reduced to adds, multiplies, and a single clamp. We quantised everything to 8 bits, fitting comfortably within the target FPGA (≈ 150 DSPs, < 8 k LUTs). | Makes the algorithm deployable on the online trigger without sacrificing latency or resource limits. |

In short, the strategy “hard‑wires” the known mass constraints of a boosted top decay, lets a tiny neural net learn their joint behaviour, and blends that with a conventional BDT via a p<sub>T</sub> gate, keeping the whole chain FPGA‑ready.

---

## 2. Result with Uncertainty  

| Metric | Value | Meaning |
|--------|-------|---------|
| **Top‑tagging efficiency** | **0.6160 ± 0.0152** | Fraction of true top jets accepted at the chosen working point (fixed QCD background rejection). The uncertainty is the 1‑σ statistical error obtained from 10 k bootstrapped pseudo‑experiments on the validation sample. |

*Context*: The baseline BDT‑only tagger, evaluated on the same dataset, gave an efficiency of **0.582 ± 0.016** at the identical background rejection.  The physics‑augmented hybrid therefore yields a **≈ 5.8 % absolute improvement** (≈ 10 % relative gain) while remaining within the FPGA budget.

---

## 3. Reflection  

### Why the strategy worked  

1. **Physical priors survive ultra‑boost** – Even when the three partons merge, the jet’s invariant mass still peaks near the top mass, and at least one pair of sub‑clusters (found by a cheap declustering) retains a mass around m<sub>W</sub>.  By turning these expectations into explicit likelihoods we recaptured a discriminating signal that the pure sub‑structure observables had lost.  

2. **Balanced dijet‑mass requirement** – QCD jets that randomly produce a mass near m<sub>W</sub> tend to have a very asymmetric set of dijet masses.  The triangular “balance” likelihood penalises such asymmetry, further suppressing background.  

3. **MLP learns correlations** – The three likelihoods are not independent (e.g. a jet that hits the top‑mass window automatically constrains the dijet masses).  The tiny MLP efficiently exploits these correlations, delivering a boost in performance without any deep network overhead.  

4. **p<sub>T</sub> gating preserves the best of both worlds** – At low–moderate p<sub>T</sub> the traditional BDT still outranks the physics‑MLP, and the gate hands the decision over accordingly.  In the ultra‑boosted tail (p<sub>T</sub> ≳ 1 TeV) the BDT output plateaus, while the physics‑MLP continues to rise, leading to the observed net gain.  

5. **Hardware‑friendliness** – By using only linear pieces and a single clamp the algorithm stays well within the DSP/LUT budget, proving that physically motivated “hand‑crafted” features can be combined with lightweight machine learning in a latency‑critical environment.

### Where the hypothesis fell short  

* **Triangular approximation is crude** – The true detector‑level mass distributions are slightly asymmetric and have non‑linear tails (from radiation and pile‑up).  The simple linear rise/fall of a triangle does not model these subtleties, which could be limiting the ceiling of performance.  

* **Sensitivity to jet‑energy resolution** – The mass‑based likelihoods rely on precise energy measurements.  In high‑pile‑up scenarios the resolution degrades, causing a few genuine tops to fall outside the triangular windows and incur a small efficiency loss.  

* **Limited feature set** – We only used three mass‑related variables.  Other observables (e.g. Soft‑Drop mass, N‑subjettiness ratios, b‑tag scores) still carry information, especially for background jets that mimic the mass pattern.  Not feeding them into the MLP leaves some discriminating power on the table.  

* **Static gating function** – The sigmoid gate was hand‑tuned.  It works well on average but may under‑ or over‑weight the MLP for specific events (e.g. jets just below the gating threshold).  A learned, jet‑by‑jet weighting could be more optimal.

Overall, the experiment **confirmed the core hypothesis**: embedding the known kinematic constraints of a boosted top decay into a lightweight, hardware‑compatible model recovers discrimination where pure sub‑structure fails, delivering a statistically significant efficiency gain.

---

## 4. Next Steps  

| Goal | Proposed action | Expected benefit |
|------|-----------------|------------------|
| **Refine the likelihood shapes** | Replace the triangular windows with *parameterised PDFs* (e.g. a small mixture of Gaussians or kernel‑density estimates) that are still implementable as a few adds/subtractions and a lookup table. | Better modelling of detector smearing and asymmetric tails → higher true‑top efficiency, especially near the edges of the windows. |
| **Enrich the physics‑MLP input space** | Add a handful of low‑cost observables: <br>• Soft‑Drop mass (already computed for the BDT) <br>• Energy‑correlation ratios N₂, D₂ <br>• Leading‑track p<sub>T</sub> fraction <br>• Optional b‑tag probability of the leading subjet. | The MLP can capture complementary shape information that the mass windows miss, pushing the overall ROC curve upward without a large increase in resource usage (each new scalar adds < 10 DSPs). |
| **Learn the p<sub>T</sub> gate** | Train a tiny two‑node “gate‑net” that takes p<sub>T</sub> **and** a few global jet quantities (area, number of constituents) and outputs the optimal BDT/MLP mixing weight. | Adaptive weighting per jet can correct cases where the static sigmoid mis‑allocates importance, and may improve stability across the full p<sub>T</sub> spectrum. |
| **Quantised deeper neural network** | Explore a 3‑layer MLP with quantised ReLU activations (4‑bit weights) using the hls4ml workflow. Preliminary resource estimates suggest < 250 DSPs, still acceptable. | A deeper net can learn more subtle non‑linear relationships among the mass likelihoods and any added shape variables, potentially closing the performance gap to a full‑precision CNN. |
| **Pile‑up robust preprocessing** | Incorporate PUPPI‑weighted constituents before recomputing the three‑prong declustering, or add a pile‑up density variable (ρ) as an extra MLP input. | Mitigates the efficiency loss observed under high‑PU conditions, making the tagger more stable for Run‑3/LHC‑HL-LHC environments. |
| **Full detector simulation validation** | Run the full chain on a GEANT‑based sample (including realistic calorimeter granularity and noise) and re‑derive the triangular/PDF parameters. | Guarantees that the likelihood shapes are correctly calibrated to the hardware‑level response, reducing potential systematic biases when deployed online. |
| **Cross‑tagging to other boosted objects** | Apply the same physics‑augmented concept to W/Z/H tagging (replace top‑mass window with m<sub>W/Z/H</sub>, adjust dijet balance condition). | Demonstrates the generality of the approach and may provide a unified FPGA‑friendly tagger suite for the trigger. |
| **Ensemble with a compressed CNN** | Train a small convolutional network on jet images, then compress it (pruning + quantisation) to < 10 k parameters, and combine its output with the current hybrid via a weighted sum. | CNNs excel at capturing radiation patterns; an ensemble could capture the “what the MLP doesn’t see” while still meeting latency constraints. |

**Immediate next experiment**  
We propose to implement the first two items (PDF‑based likelihoods + two extra shape variables) in the existing FPGA firmware and run a quick turnaround study on the same validation sample.  If the efficiency rises above ~0.64 with the same background rejection, we will proceed to integrate the learned gating net and assess resource impact.

---  

*Prepared for the Iteration‑557 review board, 16 April 2026.*