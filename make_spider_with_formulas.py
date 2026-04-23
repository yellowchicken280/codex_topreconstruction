import matplotlib.pyplot as plt
import numpy as np
import textwrap

labels = ['Mass Precision', 'Internal Ratios', 'Angular Topology', 'Geometry (Eta)', 'Classifier Trust']
num_vars = len(labels)

# Corrected Stages matching the Efficiency Frontier Table
baseline = [1, 1, 1, 1, 9]
topology = [2, 9, 2, 2, 7]
kinematics = [9, 9, 3, 3, 6]
synergy = [9, 9, 8, 8, 4]

phases = [baseline, topology, kinematics, synergy]
titles = ['Phase I: Baseline', 'Phase II: Topology', 'Phase III: Kinematics', 'Phase IV: Synergy']
formulas = [
    "combined_score = t.score",
    "combined_score = t.score * exp(-ratio_dev^2 / 0.02)\n(ratio_dev targeting 0.46)",
    "combined_score = t.score * ratio_factor * exp(-0.5 * ((mass-162)/sigma)^2)",
    "combined_score = t.score * top_prior * ratio_factor\n* (1.0 + 0.05 * tanh(1.5 - |eta|))"
]
colors = ['gray', '#1f77b4', '#2ca02c', '#ff7f0e']

fig, axs = plt.subplots(1, 4, figsize=(22, 7), subplot_kw=dict(polar=True))

for i, data in enumerate(phases):
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    data = data + [data[0]] 
    angles = angles + [angles[0]]
    
    axs[i].fill(angles, data, color=colors[i], alpha=0.3)
    axs[i].plot(angles, data, color=colors[i], linewidth=2.5)
    axs[i].set_yticklabels([])
    axs[i].set_xticks(angles[:-1])
    axs[i].set_xticklabels(labels, fontsize=8, fontweight='bold')
    
    # Title
    axs[i].set_title(titles[i], size=16, color=colors[i], y=1.2, fontweight='black')
    
    # Formula Annotation below the polar plot
    # We use fig.text to place it accurately relative to each axis
    plt.figtext(0.125 + i*0.20, 0.05, textwrap.fill(formulas[i], width=30), 
                ha='center', fontsize=10, family='monospace',
                bbox=dict(boxstyle='round,pad=0.5', fc='white', ec=colors[i], alpha=0.1))

plt.subplots_adjust(top=0.8, bottom=0.25)
plt.savefig('strategy_spider_with_formulas.png', dpi=300)
print('Generated strategy_spider_with_formulas.png')
