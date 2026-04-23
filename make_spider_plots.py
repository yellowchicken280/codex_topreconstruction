import matplotlib.pyplot as plt
import numpy as np

labels = ['Mass Precision', 'Internal Ratios', 'Angular Topology', 'Geometry (Eta)', 'Classifier Trust']
num_vars = len(labels)

# Corrected Data Mapping (Rigorous Scale: 10=Hard Constraint, 2=Correction)
# Phase I: Baseline (Pure XGBoost)
baseline = [1, 1, 1, 1, 9]
# Phase II: Topology (0.46 Ratio Gating)
topology = [2, 9, 2, 2, 7]
# Phase III: Kinematics (Adding 162 GeV Mass Prior)
kinematics = [9, 9, 3, 3, 6]
# Phase IV: Synergy (Detector Geometry & Multi-variate Polish)
# NOTE: Geometry is a 2 (Correction), Angular is a 5 (Moderate)
synergy = [9, 9, 5, 2, 4]

phases = [baseline, topology, kinematics, synergy]
titles = ['Phase I: Baseline', 'Phase II: Topology', 'Phase III: Kinematics', 'Phase IV: Synergy']
colors = ['gray', '#1f77b4', '#2ca02c', '#ff7f0e']

fig, axs = plt.subplots(1, 4, figsize=(20, 5), subplot_kw=dict(polar=True))

for i, data in enumerate(phases):
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    data = data + [data[0]] 
    angles = angles + [angles[0]]
    
    axs[i].fill(angles, data, color=colors[i], alpha=0.3)
    axs[i].plot(angles, data, color=colors[i], linewidth=2.5)
    axs[i].set_yticklabels([])
    axs[i].set_xticks(angles[:-1])
    axs[i].set_xticklabels(labels, fontsize=9, fontweight='bold')
    axs[i].set_title(titles[i], size=16, color=colors[i], y=1.15, fontweight='black')

plt.tight_layout()
plt.savefig('strategy_spider_evolution.png', dpi=300)
print('Generated corrected strategy_spider_evolution.png')
