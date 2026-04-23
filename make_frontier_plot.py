import csv
import matplotlib.pyplot as plt
import numpy as np

rounds = []
effs = []
frontier_rounds = []
frontier_effs = []
current_max = 0

# 1. Read Data
with open('agent_trajectory.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            r = int(row['Round'])
            e = float(row['Metric'])
            rounds.append(r)
            effs.append(e)
            if e > current_max:
                current_max = e
                frontier_rounds.append(r)
                frontier_effs.append(e)
        except: continue

# 2. Plotting
plt.figure(figsize=(12, 6))

# The Cloud (All trials)
plt.scatter(rounds, effs, alpha=0.1, s=1, color='gray', label='All Trials (32k+)')

# The Staircase (Frontier)
# To make a proper staircase, we need to interpolate points
step_rounds = []
step_effs = []
for i in range(len(frontier_rounds)):
    step_rounds.append(frontier_rounds[i])
    step_effs.append(frontier_effs[i])
    if i < len(frontier_rounds)-1:
        step_rounds.append(frontier_rounds[i+1])
        step_effs.append(frontier_effs[i])

plt.plot(step_rounds, step_effs, color='royalblue', linewidth=3, label='Efficiency Frontier', zorder=5)
plt.scatter(frontier_rounds, frontier_effs, color='red', s=50, edgecolors='black', zorder=10, label='Breakthroughs')

# Annotations (Major Milestones)
plt.annotate('Phase I: Baseline', xy=(90000, 0.44), xytext=(80000, 0.35),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1))
plt.annotate('Phase IV: 0.6345 Milestone', xy=(frontier_rounds[-1], frontier_effs[-1]), xytext=(frontier_rounds[-1]-10000, 0.68),
             arrowprops=dict(facecolor='gold', shrink=0.05))

plt.title('Autonomous Strategy Discovery Trajectory', fontsize=16)
plt.xlabel('Round Number', fontsize=12)
plt.ylabel('Reconstruction Efficiency', fontsize=12)
plt.ylim(0, 0.75)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='lower right')

plt.tight_layout()
plt.savefig('efficiency_frontier.png', dpi=300)
print('Generated efficiency_frontier.png')
