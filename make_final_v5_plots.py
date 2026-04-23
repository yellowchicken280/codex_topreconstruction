import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import textwrap

def make_v5_production_plot(filename, round_range, title, sub_label):
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
                    # Get full first two sentences and wrap them
                    full_text = row['Insight'].strip()
                    wrapped = textwrap.fill(full_text, width=22) 
                    insights.append(wrapped)
            except: continue

    if not rounds: return

    # Extra wide canvas for a poster
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111)
    
    ax.plot(rounds, effs, marker='o', markersize=14, linestyle='-', linewidth=4, 
            color='#E64B35FF', label='Agent Strategy Evaluation', zorder=1, alpha=0.8)
    
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    
    # 4-Tier Vertical Offsets to eliminate ANY overlap
    # [High-Above, Low-Below, Med-Above, Deep-Below]
    y_tiers = [0.04, -0.16, 0.10, -0.25]
    valigns = ['bottom', 'top', 'bottom', 'top']
    
    for i, (r, e, txt) in enumerate(zip(rounds, effs, insights)):
        tier = i % 4
        y_off = y_tiers[tier]
        va = valigns[tier]
        
        ax.annotate(f"ROUND {r}\n{txt}", 
                     xy=(r, e), 
                     xytext=(r, e + y_off),
                     arrowprops=dict(arrowstyle='->', alpha=0.4, color='black', connectionstyle="arc3,rad=0"),
                     fontsize=10,
                     ha='center',
                     va=va,
                     fontweight='medium',
                     linespacing=1.3,
                     bbox=dict(boxstyle='round4,pad=0.6', fc='#FDFEFE', ec='#E64B35FF', alpha=0.95, lw=1.5),
                     zorder=10)

    # Isolated Title Block
    plt.title(f"{title}", fontsize=24, fontweight='bold', pad=60)
    plt.suptitle(sub_label, fontsize=16, y=0.93, style='italic', color='#555555')
    
    ax.set_xlabel('Discovery Timeline (Round Number)', fontsize=16, labelpad=20)
    ax.set_ylabel('Selection Efficiency (%)', fontsize=16, labelpad=20)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Expand limits significantly for the 4-tier labels
    ax.set_ylim(min(effs)-0.30, max(effs)+0.20)
    
    plt.subplots_adjust(top=0.85, bottom=0.12)
    
    plt.savefig(filename, dpi=300)
    print(f'Generated {filename}')

# 1. Kinematics
make_v5_production_plot('zoom_kinematics_v5.png', range(90000, 90012), 
                     'Discovery: Asymmetric Top-Quark Mass Priors',
                     'Agent autonomously learned to model detector resolution tails using skewed Gaussian priors.')

# 2. Topology
make_v5_production_plot('zoom_topology_v5.png', range(91195, 91206), 
                     'Innovation: Invariant W-Boson Mass Ratios',
                     'Breakthrough in combinatorial background rejection via energy-sharing kinematic constraints.')

# 3. Synergy
make_v5_production_plot('zoom_synergy_v5.png', range(110000, 110012), 
                     'Optimization: Azimuthal & Geometric Symmetry',
                     'Final precision calibration of detector-region responses to reach the 0.6345 state-of-the-art.')
