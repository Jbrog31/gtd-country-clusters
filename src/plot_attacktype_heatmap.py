import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('figures', exist_ok=True)

profiles = pd.read_csv('data/processed/cluster_profiles.csv')

attack_cols = [c for c in profiles.columns if c.startswith('attacktype_')]

data = profiles[['cluster'] + attack_cols].set_index('cluster')

row_labels = [f'Cluster {i}' for i in data.index.tolist()]
col_labels = data.columns.tolist()

plt.figure(figsize=(len(col_labels) * 0.6, 4))

im = plt.imshow(data.values, aspect='auto')
plt.colorbar(im)

plt.yticks(ticks=np.arange(len(row_labels)), labels=row_labels)
plt.xticks(ticks=np.arange(len(col_labels)), labels=col_labels, rotation=45, ha='right')

plt.title('Attack-Type Profile by Cluster')
plt.tight_layout()
plt.savefig('figures/attacktype_heatmap.png', dpi=300)
plt.close()
