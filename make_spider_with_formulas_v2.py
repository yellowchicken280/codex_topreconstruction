import matplotlib.pyplot as plt
import numpy as np
import textwrap

# High-resolution settings
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

labels = ['Mass Precision', 'Internal Ratios', 'Angular Topology', 'Geometry (Eta)', 'Classifier Trust']
num_vars = len(labels)

# Rigorous Data Mapping
baseline = [1, 1, 1, 1, 9]
topology = [2, 9, 2, 2, 7]
kinematics = [9, 9, 3, 3, 6]
synergy = [9, 9, 5, 2, 4] 

phases = [baseline, topology, kinematics, synergy]
titles = ['Phase I: Baseline', 'Phase II: Topology', 'Phase III: Kinematics', 'Phase IV: Synergy']
formulas = [
    "combined_score = t.score",
    "combined_score = t.score * exp(-ratio_dev^2 / 0.02)\n(ratio_dev targeting 0.46)",
    "combined_score = t.score * ratio_factor * exp(-0.5 * ((mass-162)/sigma)^2)",
    "combined_score = t.score * top_prior * ratio_factor\n* (1.0 + 0.05 * tanh(1.5 - |eta|))"
]
colors = ['gray', '#1f77b4', '#2ca02c', '#ff7f0e']

# Increased height to 11 to give bottom-room
fig, axs = plt.subplots(1, 4, figsize=(24, 11), subplot_kw=dict(polar=True))

# 1. Plot the Spiders
for i, data in enumerate(phases):
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    data = data + [data[0]] 
    angles = angles + [angles[0]]
    
    axs[i].fill(angles, data, color=colors[i], alpha=0.3)
    axs[i].plot(angles, data, color=colors[i], linewidth=3)
    
    axs[i].set_ylim(0, 10)
    axs[i].set_rgrids([2, 4, 6, 8, 10], labels=['2','4','6','8','10'], 
                       angle=0, fontsize=7, color='gray', alpha=0.5)
    
    if i > 0: axs[i].set_yticklabels([]) 
    
    axs[i].set_xticks(angles[:-1])
    axs[i].set_xticklabels(labels, fontsize=9, fontweight='bold')
    axs[i].set_title(titles[i], size=18, color=colors[i], y=1.25, fontweight='black')

# 2. Add Lifted and Centered Formulas
# Lifted to y=0.28 to sit much higher above the bottom border
for i, formula in enumerate(formulas):
    x_center = 0.2 + i * 0.2
    plt.figtext(x_center, 0.28, textwrap.fill(formula, width=32), 
                ha='center', fontsize=12, family='monospace', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.8', fc='#FDFEFE', ec=colors[i], alpha=0.9, lw=2.0))

# Standard margin adjustment
plt.subplots_adjust(top=0.75, bottom=0.40, left=0.1, right=0.9)

# pad_inches=0.5 ensures the border is never cut off
plt.savefig('strategy_spider_with_formulas.png', bbox_inches='tight', pad_inches=0.5)
print('Generated SAFE-BORDER strategy_spider_with_formulas.png')
