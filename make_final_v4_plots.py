import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def make_final_poster_plot(filename, round_range, title, sub_label, horizontal_jitter={}):
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
                    # Very short insights to prevent collision
                    ins = row['Insight'].split('.')[0][:35].strip()
                    insights.append(ins)
            except: continue

    if not rounds: return

    plt.figure(figsize=(13, 8))
    plt.plot(rounds, effs, marker='o', markersize=12, linestyle='-', linewidth=3, color='#E64B35FF', label='Agent Evaluation', zorder=1)
    
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    
    for i, (r, e, txt) in enumerate(zip(rounds, effs, insights)):
        # Apply manual horizontal jitter if specified for this round
        x_pos = r + horizontal_jitter.get(r, 0)
        
        # Stagger vertical offsets
        y_offset = 0.02 if i % 2 == 0 else -0.045
        valign = 'bottom' if i % 2 == 0 else 'top'
        
        plt.annotate(f"R{r}:\n{txt}", 
                     xy=(r, e), 
                     xytext=(x_pos, e + y_offset),
                     arrowprops=dict(arrowstyle='->', alpha=0.6, color='black', connectionstyle="arc3,rad=0.1"),
                     fontsize=10,
                     ha='center',
                     va=valign,
                     bbox=dict(boxstyle='round,pad=0.5', fc='white', ec='#E64B35FF', alpha=0.95),
                     zorder=10)

    # TITLES: Increased padding and separation
    plt.title(f"{title}", fontsize=20, fontweight='bold', pad=40)
    plt.suptitle(sub_label, fontsize=14, y=0.92, style='italic', color='#333333')
    
    plt.xlabel('Round Number (Iteration Time)', fontsize=14, labelpad=15)
    plt.ylabel('Efficiency (%)', fontsize=14, labelpad=15)
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.ylim(min(effs)-0.10, max(effs)+0.10)
    
    # Ensure titles don't overlap the top of the plot
    plt.subplots_adjust(top=0.82, bottom=0.15)
    
    plt.savefig(filename, dpi=300)
    print(f'Generated {filename}')

# 1. Kinematics: Added jitter to R90009 and R90011 to prevent overlap
make_final_poster_plot('zoom_kinematics_v4.png', range(90000, 90012), 
                     'Discovery: Asymmetric Top-Quark Mass Priors',
                     'Initial discovery of non-Gaussian tails and mass-balance consistency.',
                     horizontal_jitter={90009: -0.3, 90011: 0.3})

# 2. Topology
make_final_poster_plot('zoom_topology_v4.png', range(91195, 91206), 
                     'Innovation: Invariant W-Boson Mass Ratios',
                     'Agent autonomously shifted focus to dimensionless energy-sharing invariants.')

# 3. Synergy
make_final_poster_plot('zoom_synergy_v4.png', range(110000, 110012), 
                     'Optimization: Azimuthal & Geometric Symmetry',
                     'Final calibration of detector-region corrections to reach 0.6345 record.')
