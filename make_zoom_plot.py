import csv
import matplotlib.pyplot as plt

rounds = []
effs = []

with open('agent_trajectory.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            r = int(row['Round'])
            if 100000 <= r <= 100015: # Specific optimization spur
                rounds.append(r)
                effs.append(float(row['Metric']))
        except: continue

plt.figure(figsize=(8, 5))
plt.plot(rounds, effs, marker='o', linestyle='-', color='darkorange', linewidth=2, label='Fine-Tuning Round')
plt.axhline(y=0.6151, color='red', linestyle='--', alpha=0.5, label='Local Champion Benchmark')

plt.title('Detail: Agent Parameter Fine-Tuning (Exploitation Phase)', fontsize=14)
plt.xlabel('Round Number', fontsize=12)
plt.ylabel('Efficiency (on Search Sample)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

plt.tight_layout()
plt.savefig('refinement_zoom.png', dpi=300)
print('Generated refinement_zoom.png')
