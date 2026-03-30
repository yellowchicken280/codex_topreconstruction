# topreco-agent

A thin wrapper that runs [codexlikeagent](https://github.com/yellowchicken280/codexlikeagent) against the top quark reconstruction pipeline ([topreconstruction](https://github.com/yellowchicken280/topreconstruction)). The agent handles running the pipeline, evaluating results, and optimizing parameters — without manual command-line steps.

Neither underlying project is modified. This repo just configures and directs the agent.

---

## What it does

- Runs all five triplet selection strategies on a dataset and produces a comparison report (purity, coverage, AUC)
- Sweeps the min_score threshold parameter for the best-performing strategy and finds the optimal cutoff
- (Planned) Reads the source code and proposes + implements new selection strategies

## How it works

codexlikeagent is a general-purpose LLM agent harness. It has tools for running shell commands, writing and executing scripts, and persisting memory across runs. This repo points it at the top quark reconstruction pipeline and gives it the domain knowledge it needs to operate it correctly.

The three pieces this repo adds:

- `config.yaml` — tells the agent which model to use, where to store sessions, timeout limits, etc.
- `run.sh` — sets up the right conda environment and launches the agent
- `prompts/` — the actual task instructions, one file per task
- A skill file in codexlikeagent (not in this repo) that gives the agent background knowledge on the pipeline: file paths, score scale quirks, environment setup, how to compute purity

## Usage

```bash
./run.sh prompts/01_orchestrate.txt              # benchmark all 5 strategies
./run.sh prompts/02_interpret_and_adapt.txt      # optimize the min_score threshold
./run.sh prompts/01_orchestrate.txt my-session   # named session (memory persists across runs)
```

## Requirements

- Access to the topreconstruction project and its `topml` conda environment
- codexlikeagent installed at `/global/u1/v/vinny/projects/codexlikeagent`
- A CBorg API key (LBL/NERSC OpenAI-compatible proxy):

```bash
export OPENAI_BASE_URL="https://api.cborg.lbl.gov"
export CBORG_API_KEY="your-key-here"
export OPENAI_API_KEY="$CBORG_API_KEY"
```

## Results so far

Threshold sweep on 10k ttbar events, greedy_disjoint strategy:

| min_score | Coverage | Purity | F1-proxy |
|---|---|---|---|
| 0.05 | 74.5% | 0.242 | 0.366 |
| 0.08 | 61.0% | 0.262 | 0.367 (recommended) |
| 0.10 | 52.5% | 0.277 | 0.363 (baseline) |
| 0.15 | 34.8% | 0.307 | 0.326 |
| 0.20 | 22.5% | 0.326 | 0.266 |
| 0.30 | 5.7%  | 0.411 | 0.100 |

Lowering the threshold from 0.10 to 0.08 picks up 8.5% more events with a small purity tradeoff, giving the best balance overall.
