import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def make_clean_zoom_plot(filename, round_list, title, category_name):
    rounds = []
    effs = []
    insights = []
    
    with open('agent_trajectory.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                r = int(row['Round'])
                if r in round_list:
                    rounds.append(r)
                    effs.append(float(row['Metric']))
                    # Clean up insight for labels
                    ins = row['Insight'].split('.')[0][:40] # First sentence only, short
                    insights.append(ins if ins else "Refining Parameters")
            except: continue

    if not rounds: return

    plt.figure(figsize=(12, 7))
    plt.plot(rounds, effs, marker='o', markersize=8, linestyle='-', linewidth=2.5, color='#1f77b4')
    
    # Force Integer X-axis
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    
    # Staggered Annotations to avoid overlap
    for i, (r, e, txt) in enumerate(zip(rounds, effs, insights)):
        # Alternate height: 1.05 above, 0.95 below
        offset = 0.015 if i % 2 == 0 else -0.025
        valign = 'bottom' if i % 2 == 0 else 'top'
        
        plt.annotate(f"Round {r}:\n{txt}", 
                     xy=(r, e), 
                     xytext=(r, e + offset),
                     arrowprops=dict(arrowstyle='->', alpha=0.5),
                     fontsize=9,
                     ha='center',
                     va=valign,
                     bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='gray', alpha=0.8))

    plt.title(f"{category_name}\n{title}", fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Round Number', fontsize=12)
    plt.ylabel('Reconstruction Efficiency', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.4)
    
    # Add a bit of space for labels
    plt.ylim(min(effs)-0.06, max(effs)+0.06)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f'Generated {filename}')

# 1. Kinematics: Mass Prior Tuning
make_clean_zoom_plot('zoom_kinematics_v2.png', range(90000, 90010), 
                     'Exploring Asymmetric Mass Constraints',
                     'Category: Kinematic Refinement')

# 2. Topology: Ratio Gating
make_clean_zoom_plot('zoom_topology_v2.png', range(91195, 110001), 
                     'Discovery of Energy-Flow Invariants',
                     'Category: Topological Innovation')

# 3. Synergy: Final Optimization
make_clean_zoom_plot('zoom_synergy_v2.png', range(110000, 110010), 
                     'Integrating Detector Geometry & Symmetry',
                     'Category: Cross-Component Synergy')
