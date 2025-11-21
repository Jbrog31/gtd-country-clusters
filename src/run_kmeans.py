import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv('data/processed/country_features_kmeans_scaled.csv')

feature_cols = [c for c in df.columns if c not in ['country_txt', 'attacks_total']]
X = df[feature_cols]

results = []

for k in range(3, 11):
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10)
    labels = kmeans.fit_predict(X)
    inertia = kmeans.inertia_
    silhouette = silhouette_score(X, labels)
    results.append((k, inertia, silhouette))

results_df = pd.DataFrame(results, columns=['k', 'inertia', 'silhouette'])
results_df.to_csv('data/processed/kmeans_diagnostics.csv', index=False)

final_k = results_df.sort_values('silhouette', ascending=False).iloc[0]['k']

kmeans_final = KMeans(n_clusters=int(final_k), random_state=0, n_init=10)
final_labels = kmeans_final.fit_predict(X)

out = df[['country_txt', 'attacks_total']].copy()
out['cluster'] = final_labels

out.to_csv('data/processed/country_clusters.csv', index=False)
