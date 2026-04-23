import matplotlib.pyplot as plt
import numpy as np

labels = ['Mass Precision', 'Internal Ratios', 'Angular Topology', 'Geometry (Eta)', 'Classifier Trust']
num_vars = len(labels)

# Milestone Data (Scores 0 to 10 for feature importance/complexity)
# 1. Baseline
baseline = [1, 1, 1, 1, 9]
# 2. Asymmetric Mass
mass_phase = [8, 1, 1, 1, 6]
# 3. Ratio Gating
ratio_phase = [7, 8, 2, 2, 5]
# 4. Final Synergy (0.6345)
final_phase = [9, 9, 7, 6, 4]

phases = [baseline, mass_phase, ratio_phase, final_phase]
titles = ['Phase I: Baseline', 'Phase II: Kinematics', 'Phase III: Topology', 'Phase IV: Synergy']
colors = ['gray', 'royalblue', 'forestgreen', 'gold']

fig, axs = plt.subplots(1, 4, figsize=(20, 5), subplot_kw=dict(polar=True))

for i, data in enumerate(phases):
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    data = data + [data[0]] # Close the loop
    angles = angles + [angles[0]]
    
    axs[i].fill(angles, data, color=colors[i], alpha=0.3)
    axs[i].plot(angles, data, color=colors[i], linewidth=2)
    axs[i].set_yticklabels([])
    axs[i].set_xticks(angles[:-1])
    axs[i].set_xticklabels(labels, fontsize=8)
    axs[i].set_title(titles[i], size=14, color=colors[i], y=1.1)

plt.tight_layout()
plt.savefig('strategy_spider_evolution.png', dpi=300)
print('Generated strategy_spider_evolution.png')
