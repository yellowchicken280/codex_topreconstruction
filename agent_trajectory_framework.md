# Agent Trajectory Analysis Framework

This document outlines a literature-aligned approach to analyzing and visualizing agent behavior over iterative optimization rounds.

---

## 1. Trajectory Table

A structured table capturing each round of the agent’s behavior.

| Round | Action | Setup | Metric | ΔMetric | Insight |
|------|--------|-------|--------|--------|--------|
| 1 | Incremental Tuning | Param set A | 0.52 | +0.02 | Small gain from tuning |
| 2 | Component Innovation | New model | 0.60 | +0.08 | Major improvement from new method |
| ... | ... | ... | ... | ... | ... |

**Fields:**
- **Round**: Iteration number
- **Action**: Type of change (e.g., tuning, innovation, shift)
- **Setup**: Configuration used (parameters, model, strategy)
- **Metric**: Performance metric (e.g., efficiency)
- **ΔMetric**: Change from previous round
- **Insight**: Agent reasoning or interpretation

---

## 2. Time-Series Plot

Visualize performance over time.

- **X-axis**: Round (iteration number)
- **Y-axis**: Metric (e.g., efficiency)
- **Markers/Colors**: Represent action type
  - Example:
    - Blue = Incremental Tuning
    - Red = Component Innovation
    - Green = Component Shift
    - Gray = Diagnostic

**Purpose:**
- Identify trends
- Detect sudden improvements
- Observe convergence behavior

---

## 3. Optional Graph / Flow Representation

A structural view of the trajectory.

- **Nodes**: States
  - Each state includes:
    - Setup
    - Metric
- **Edges**: Actions taken by the agent

**Interpretation:**
- Shows how the agent navigates the search space
- Captures non-linear transitions (e.g., jumps, backtracking)

---

## 4. Summary Analysis

Key insights derived from the trajectory.

### 4.1 Major Improvements
- Identify rounds with large positive ΔMetric
- Analyze what actions triggered these jumps

### 4.2 Action Effectiveness
- Correlate action types with performance changes
  - Which actions consistently improve results?
  - Which actions have little or negative impact?

### 4.3 Plateau Detection
- Identify regions where metric stabilizes
- Determine if:
  - Further tuning is ineffective
  - A shift or innovation is needed

---

## Goal

The objective is to transform raw agent logs into a structured, interpretable representation that enables:

- Characterization of agent behavior
- Identification of optimization patterns
- Comparison across different runs or configurations
