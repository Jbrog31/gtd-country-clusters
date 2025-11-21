import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('data/processed/country_features_full.csv')

df = df[df['attacks_total'] >= 50].copy()

feature_cols = [c for c in df.columns if c not in ['country_txt', 'attacks_total']]

X = df[feature_cols]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols)
X_scaled_df.insert(0, 'country_txt', df['country_txt'].values)
X_scaled_df.insert(1, 'attacks_total', df['attacks_total'].values)

X_scaled_df.to_csv('data/processed/country_features_kmeans_scaled.csv', index=False)
