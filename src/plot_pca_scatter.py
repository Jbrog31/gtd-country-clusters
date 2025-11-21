import os
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

os.makedirs('figures', exist_ok=True)

scaled = pd.read_csv('data/processed/country_features_kmeans_scaled.csv')
clusters = pd.read_csv('data/processed/country_clusters.csv')

df = scaled.merge(clusters, on=['country_txt', 'attacks_total'], how='inner')

feature_cols = [c for c in df.columns if c not in ['country_txt', 'attacks_total', 'cluster']]

X = df[feature_cols]

pca = PCA(n_components=2, random_state=0)
X_pca = pca.fit_transform(X)

plot_df = pd.DataFrame({
    'PC1': X_pca[:, 0],
    'PC2': X_pca[:, 1],
    'cluster': df['cluster'],
    'country_txt': df['country_txt'],
    'attacks_total': df['attacks_total']
})

plt.figure(figsize=(10, 8))

for cl in sorted(plot_df['cluster'].unique()):
    subset = plot_df[plot_df['cluster'] == cl]
    plt.scatter(subset['PC1'], subset['PC2'], label=f'Cluster {cl}', alpha=0.7)

plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA of Country Terrorism Profiles (Colored by Cluster)')
plt.legend()
plt.tight_layout()

plt.savefig('figures/pca_scatter.png', dpi=300)
plt.close()
