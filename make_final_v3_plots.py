import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def make_final_poster_plot(filename, round_range, title, sub_label):
    rounds = []
    effs = []
    insights = []
    
    with open('agent_trajectory.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                r = int(row['Round'])
                if r in round_range:
                    rounds.append(r)
                    effs.append(float(row['Metric']))
                    # First 40 chars of insight
                    ins = row['Insight'].split('.')[0][:45]
                    insights.append(ins)
            except: continue

    if not rounds: return

    plt.figure(figsize=(13, 7))
    plt.plot(rounds, effs, marker='o', markersize=10, linestyle='-', linewidth=3, color='#E64B35FF', label='Agent Evaluation')
    
    # Force Integer X-axis
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    
    # Staggered Annotations
    for i, (r, e, txt) in enumerate(zip(rounds, effs, insights)):
        # Calculate offset: Breakthroughs get labeled, middle ones get dots, plateau gets labeled
        is_breakthrough = (i == 0) or (i > 0 and e > max(effs[:i]))
        is_plateau = (i == len(effs)-1)
        
        if is_breakthrough or is_plateau or i % 3 == 0:
            offset = 0.015 if i % 2 == 0 else -0.035
            valign = 'bottom' if i % 2 == 0 else 'top'
            
            plt.annotate(f"R{r}:\n{txt}", 
                         xy=(r, e), 
                         xytext=(r, e + offset),
                         arrowprops=dict(arrowstyle='->', alpha=0.6, color='black'),
                         fontsize=10,
                         ha='center',
                         va=valign,
                         bbox=dict(boxstyle='round,pad=0.4', fc='white', ec='#E64B35FF', alpha=0.9))

    plt.title(f"{title}\n", fontsize=18, fontweight='bold')
    plt.suptitle(sub_label, fontsize=13, y=0.92, style='italic')
    plt.xlabel('Round Number (Iteration Time)', fontsize=14)
    plt.ylabel('Efficiency (%)', fontsize=14)
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Consistent scale to see the hill
    plt.ylim(min(effs)-0.08, max(effs)+0.08)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f'Generated {filename}')

# 1. Kinematics: The Mass Prior Hill-Climb
make_final_poster_plot('zoom_kinematics_v3.png', range(90000, 90012), 
                     'Discovery: Asymmetric Top-Quark Mass Priors',
                     'Initial discovery of non-Gaussian tails and mass-balance consistency.')

# 2. Topology: Breaking the Plateau
make_final_poster_plot('zoom_topology_v3.png', range(91195, 91206), 
                     'Innovation: Invariant W-Boson Mass Ratios',
                     'Agent autonomously shifted focus to dimensionless energy-sharing invariants.')

# 3. Synergy: Final High-Precision Tuning
make_final_poster_plot('zoom_synergy_v3.png', range(110000, 110012), 
                     'Optimization: Azimuthal & Geometric Symmetry',
                     'Final calibration of detector-region corrections to reach 0.6345 record.')
