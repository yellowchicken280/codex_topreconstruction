import csv
import matplotlib.pyplot as plt

def make_spur_plot(filename, round_range, title, annotations):
    rounds = []
    effs = []
    with open('agent_trajectory.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                r = int(row['Round'])
                if r in round_range:
                    rounds.append(r)
                    effs.append(float(row['Metric']))
            except: continue
    
    plt.figure(figsize=(10, 6))
    plt.plot(rounds, effs, marker='o', linestyle='-', color='darkcyan', label='Iteration')
    
    for r, text in annotations.items():
        if r in rounds:
            idx = rounds.index(r)
            plt.annotate(text, xy=(r, effs[idx]), xytext=(r, effs[idx]+0.01),
                         arrowprops=dict(facecolor='black', arrowstyle='->'),
                         fontsize=9, rotation=45)

    plt.title(title, fontsize=14)
    plt.xlabel('Round Number', fontsize=12)
    plt.ylabel('Efficiency', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.ylim(min(effs)-0.05, max(effs)+0.05)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f'Generated {filename}')

# 1. Spur: Kinematics (Early Mass Prior tuning)
make_spur_plot('zoom_kinematics.png', range(90000, 90010), 
               'Spur: Optimizing Asymmetric Mass Priors',
               {90003: 'Mass Balance Corrected', 90007: 'Symmetry Penalty Add'})

# 2. Spur: Topology (Ratio gating)
make_spur_plot('zoom_topology.png', range(91190, 110001), 
               'Spur: Fine-tuning Invariant Mass Ratios',
               {91198: 'Renormalization Scaling', 91200: 'Cross-Attention Shift'})

# 3. Spur: Synergy (Final Geometry)
make_spur_plot('zoom_synergy.png', range(110000, 110012), 
               'Spur: Final Geometric & Azimuthal Corrections',
               {110000: 'Azimuthal Symmetry Boost', 110004: 'Geometric Mean Ratio'})
