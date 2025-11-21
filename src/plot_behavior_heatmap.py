import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('figures', exist_ok=True)

profiles = pd.read_csv('data/processed/cluster_profiles.csv')

base_cols = [
    'avg_killed',
    'avg_wounded',
    'severity_index',
    'pct_successful',
    'pct_suicide',
    'num_groups'
]

behavior = profiles[['cluster'] + base_cols].copy()

attack_cols = {
    'attacktype_Armed Assault': ['attacktype_Armed Assault'],
    'attacktype_Bombing/Explosion': ['attacktype_Bombing/Explosion'],
    'attacktype_Assassination': ['attacktype_Assassination'],
    'attacktype_Hijacking': ['attacktype_Hijacking'],
    'attacktype_Hostage': [
        'attacktype_Hostage Taking (Kidnapping)',
        'attacktype_Hostage Taking (Barricade Incident)'
    ]
}

for new_col, source_cols in attack_cols.items():
    cols_present = [c for c in source_cols if c in profiles.columns]
    if not cols_present:
        continue
    if len(cols_present) == 1:
        behavior[new_col] = profiles[cols_present[0]]
    else:
        behavior[new_col] = profiles[cols_present].sum(axis=1)

behavior = behavior.set_index('cluster')

data = behavior.copy()
for c in data.columns:
    std = data[c].std()
    if std == 0:
        continue
    data[c] = (data[c] - data[c].mean()) / std

row_labels = [f'Cluster {i}' for i in data.index.tolist()]
col_labels = data.columns.tolist()

plt.figure(figsize=(len(col_labels) * 0.8, 4))

im = plt.imshow(data.values, aspect='auto')
plt.colorbar(im)

plt.yticks(ticks=np.arange(len(row_labels)), labels=row_labels)
plt.xticks(ticks=np.arange(len(col_labels)), labels=col_labels, rotation=45, ha='right')

plt.title('Behavioral Summary by Cluster (z-scored)')
plt.tight_layout()
plt.savefig('figures/behavior_heatmap.png', dpi=300)
plt.close()
