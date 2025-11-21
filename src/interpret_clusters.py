import pandas as pd

features = pd.read_csv('data/processed/country_features_full.csv')
clusters = pd.read_csv('data/processed/country_clusters.csv')

df = features.merge(clusters, on=['country_txt', 'attacks_total'], how='inner')

numeric_cols = df.select_dtypes(include='number').columns.tolist()
numeric_cols = [c for c in numeric_cols if c != 'cluster']

cluster_profiles = df.groupby('cluster')[numeric_cols].mean().reset_index()

sizes = df.groupby('cluster').size().reset_index(name='num_countries')

cluster_profiles = cluster_profiles.merge(sizes, on='cluster', how='left')

cluster_profiles.to_csv('data/processed/cluster_profiles.csv', index=False)

members = df[['country_txt', 'attacks_total', 'cluster']].copy()
members = members.sort_values(['cluster', 'attacks_total'], ascending=[True, False])

members.to_csv('data/processed/cluster_members.csv', index=False)
