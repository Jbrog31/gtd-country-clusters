import pandas as pd
import numpy as np

df = pd.read_excel('data/raw/GlobalTerrorismDatabase.xlsx')

df = df[df['iyear'] >= 2000]

cols = [
    'country_txt', 'nkill', 'nwound',
    'attacktype1_txt'
]

df = df[cols]

df['nkill'] = df['nkill'].fillna(0)
df['nwound'] = df['nwound'].fillna(0)

df['severity_index'] = np.log1p(df['nkill'] + df['nwound'])

df['attacktype1_txt'] = df['attacktype1_txt'].fillna('Unknown')

grouped_severity = df.groupby('country_txt').agg(
    attacks_total=('country_txt', 'size'),
    avg_killed=('nkill', 'mean'),
    avg_wounded=('nwound', 'mean'),
    median_killed=('nkill', 'median'),
    max_killed=('nkill', 'max'),
    severity_index=('severity_index', 'mean')
).reset_index()

attack_dummies = pd.get_dummies(df['attacktype1_txt'], prefix='attacktype')

attack_by_country = df[['country_txt']].join(attack_dummies).groupby('country_txt').sum()

attack_by_country_pct = attack_by_country.div(attack_by_country.sum(axis=1), axis=0)

attack_by_country_pct = attack_by_country_pct.reset_index()

country_features = grouped_severity.merge(attack_by_country_pct, on='country_txt', how='left')

country_features.to_csv('data/processed/country_features_step2.csv', index=False)
