import pandas as pd
import numpy as np

df = pd.read_excel('data/raw/GlobalTerrorismDatabase.xlsx')

df = df[df['iyear'] >= 2000]

cols = [
    'country_txt', 'nkill', 'nwound',
    'attacktype1', 'attacktype1_txt',
    'targtype1', 'targtype1_txt',
    'weaptype1', 'weaptype1_txt',
    'success', 'suicide', 'gname'
]

df = df[cols]

df['nkill'] = df['nkill'].fillna(0)
df['nwound'] = df['nwound'].fillna(0)

df['severity_index'] = np.log1p(df['nkill'] + df['nwound'])

grouped = df.groupby('country_txt').agg(
    attacks_total=('country_txt', 'size'),
    avg_killed=('nkill', 'mean'),
    avg_wounded=('nwound', 'mean'),
    median_killed=('nkill', 'median'),
    max_killed=('nkill', 'max'),
    severity_index=('severity_index', 'mean')
).reset_index()

grouped.to_csv('data/processed/country_features_step1.csv', index=False)
