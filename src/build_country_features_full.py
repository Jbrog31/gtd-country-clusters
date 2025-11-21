import pandas as pd
import numpy as np

df = pd.read_excel('data/raw/GlobalTerrorismDatabase.xlsx')

df = df[df['iyear'] >= 2000]

cols = [
    'country_txt', 'nkill', 'nwound',
    'attacktype1_txt', 'targtype1_txt', 'weaptype1_txt',
    'success', 'suicide', 'gname'
]

df = df[cols]

df['nkill'] = df['nkill'].fillna(0)
df['nwound'] = df['nwound'].fillna(0)
df['severity_index'] = np.log1p(df['nkill'] + df['nwound'])

df['attacktype1_txt'] = df['attacktype1_txt'].fillna('Unknown')
df['targtype1_txt'] = df['targtype1_txt'].fillna('Unknown')
df['weaptype1_txt'] = df['weaptype1_txt'].fillna('Unknown')
df['gname'] = df['gname'].fillna('Unknown')

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
attack_pct = attack_by_country.div(attack_by_country.sum(axis=1), axis=0).reset_index()

target_dummies = pd.get_dummies(df['targtype1_txt'], prefix='targettype')
target_by_country = df[['country_txt']].join(target_dummies).groupby('country_txt').sum()
target_pct = target_by_country.div(target_by_country.sum(axis=1), axis=0).reset_index()

weapon_dummies = pd.get_dummies(df['weaptype1_txt'], prefix='weaptype')
weapon_by_country = df[['country_txt']].join(weapon_dummies).groupby('country_txt').sum()
weapon_pct = weapon_by_country.div(weapon_by_country.sum(axis=1), axis=0).reset_index()

success_rate = df.groupby('country_txt')['success'].mean().reset_index(name='pct_successful')
suicide_rate = df.groupby('country_txt')['suicide'].mean().reset_index(name='pct_suicide')

groups = df[df['gname'] != 'Unknown'].groupby('country_txt')['gname'].nunique().reset_index(name='num_groups')

country = grouped_severity.merge(attack_pct, on='country_txt', how='left')
country = country.merge(target_pct, on='country_txt', how='left')
country = country.merge(weapon_pct, on='country_txt', how='left')
country = country.merge(success_rate, on='country_txt', how='left')
country = country.merge(suicide_rate, on='country_txt', how='left')
country = country.merge(groups, on='country_txt', how='left')

country.to_csv('data/processed/country_features_full.csv', index=False)
