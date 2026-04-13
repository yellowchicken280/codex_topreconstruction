# topreco-agent

A thin wrapper that runs [codexlikeagent](https://github.com/yellowchicken280/codexlikeagent) against the top quark reconstruction pipeline. This project uses AI agents to autonomously optimize physics selection strategies for hadronic top-quark reconstruction.

---

## The Optimization Journey (Progression)

### Phase 1: The Baseline (~43%)
Starting with a pure BDT-score-based "Greedy Disjoint" selection, the efficiency was roughly **43.4%**. At this stage, the agent was simply learning how to interact with the pipeline.

### Phase 2: The "Denominator Trap" & The 59% Plateau
The agent began injecting physics knowledge (Gaussian mass priors). However, we hit a major roadblock:
*   **The Mistake:** A previous iteration reported a "hallucinated" 63% efficiency. When the agent "fixed" its math, it concluded that 63% was mathematically impossible and that **59.75%** was the absolute ceiling for this model.
*   **The Correction:** By cross-referencing with the Professor's original write-up and manual verification, we realized the denominator bug was in our *evaluation script*, not the professor's results. We locked the denominator to exactly **1026 truth triplets** (for the 2k set) to ensure rigorous, honest reporting.
*   **Parameter Discovery:** We found that for our specific model checkpoint, raw BDT scores ($\gamma=1.0$) and a tight W-window ($\sigma_W=15$) actually outperformed the professor's suggested parameters.

### Phase 3: Breaking 60% (The Greedy Trap)
We identified that the "Greedy" algorithm was a bottleneck. If a high-score fake triplet overlaps with two slightly lower-score truth triplets, the Greedy algorithm picks the fake and loses both truths.
*   **The Solution:** We implemented the **Exact Global Optimizer** (`iteration15_exact`). This uses a recursive search to find the combination of triplets that maximizes the *total* event score while maintaining jet-disjointness.
*   **Result:** Successfully broke the barrier, reaching **60.04%** efficiency on the standard benchmark.

### Phase 4: Scaling the Data (Ongoing)
We've identified that the final gap to the professor's 63% is likely the **BDT Model quality**. 
*   **The Realization:** Our current model was trained on only 2,000 events, while the professor used 10,000. 
*   **Action:** We are currently running a **50,000 event pipeline** to generate a 10k-training/35k-test split to provide the agent with a "State-of-the-Art" model foundation.

---

## Benchmark Comparison (Current Model)

| Strategy | Efficiency | Truth Triplets Found | Notes |
| :--- | :--- | :--- | :--- |
| **greedy_disjoint** | 43.37% | 445 / 1026 | Baseline |
| **mass_gaussian_wmass** | 57.80% | 593 / 1026 | Professor's Param Sweep |
| **iteration13 (Greedy)** | 59.75% | 613 / 1026 | Agent-tuned Plateau |
| **iteration15 (Exact)** | **60.04%** | **616 / 1026** | **Current Record** |

---

## Technical Features
- **Recursive Subset Optimization:** Solves the Maximum Weight Independent Set problem for triplet selection.
- **Physics Priors:** Multiplicative Gaussian penalties for Top and W mass consistency.
- **Automated Harness:** Prevents agent hallucinations by locking evaluation metrics and denominators.

## Usage
```bash
./run.sh prompts/04_reproduce_and_optimize.txt   # Run the latest optimization harness
```
