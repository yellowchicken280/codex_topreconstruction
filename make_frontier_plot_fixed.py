import csv
import matplotlib.pyplot as plt

data = []
# 1. Read and Sort Data
with open('agent_trajectory.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            data.append({'Round': int(row['Round']), 'Metric': float(row['Metric']), 'Setup': row['Setup']})
        except: continue

# Sort by Round to ensure chronological order
data.sort(key=lambda x: x['Round'])

# 2. Sequential Mapping
trial_indices = range(len(data))
effs = [d['Metric'] for d in data]

frontier_idx = []
frontier_effs = []
frontier_labels = []
current_max = 0

for i, d in enumerate(data):
    if d['Metric'] > current_max:
        current_max = d['Metric']
        frontier_idx.append(i)
        frontier_effs.append(d['Metric'])
        frontier_labels.append(d['Setup'][:20]) # Short slug for label

# 3. Plotting
plt.figure(figsize=(14, 7))
plt.scatter(trial_indices, effs, alpha=0.05, s=2, color='gray', label='Individual Trials')

# Staircase construction
step_x = []
step_y = []
for i in range(len(frontier_idx)):
    step_x.append(frontier_idx[i])
    step_y.append(frontier_effs[i])
    if i < len(frontier_idx)-1:
        step_x.append(frontier_idx[i+1])
        step_y.append(frontier_effs[i])

plt.plot(step_x, step_y, color='firebrick', linewidth=3, label='Efficiency Frontier', zorder=5)

# High-impact Annotations
for i in [0, len(frontier_idx)//2, len(frontier_idx)-1]:
    plt.annotate(frontier_labels[i], 
                 xy=(frontier_idx[i], frontier_effs[i]),
                 xytext=(frontier_idx[i], frontier_effs[i]+0.05),
                 arrowprops=dict(facecolor='black', arrowstyle='->'),
                 fontsize=10, fontweight='bold')

plt.title('Autonomous Discovery Frontier (32,000+ Evaluations)', fontsize=18)
plt.xlabel('Trial Number (Sequential)', fontsize=14)
plt.ylabel('Reconstruction Efficiency', fontsize=14)
plt.ylim(0, 0.75)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend(loc='lower right')

plt.tight_layout()
plt.savefig('efficiency_frontier_fixed.png', dpi=300)
print('Generated efficiency_frontier_fixed.png')
