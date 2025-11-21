# Global Terrorism Database – Country Terrorism Profile Clustering Project

This small project applies unsupervised machine learning to the Global Terrorism Database (GTD) to identify distinct terrorism environment types across countries based on numerous characteristics. I find the data fascinating and wanted to see what I could do with it.

Goals:

- Cluster all countries with sufficient GTD activity into coherent terrorism-profile groups.
- Identify interpretable patterns in tactics, severity, and organizational diversity that distinguish these clusters.

The central question is whether quantitative behavioral features derived from GTD can reveal real-world patterns in how terrorism manifests across different states. This project demonstrates that country-level terrorism environments exhibit clear and consistent signatures that can be discovered without supervision.

## Countries Included

This project includes all countries in the GTD dataset with at least 50 recorded terrorist attacks from 2000–2021.

Countries with fewer than 50 incidents were excluded to avoid unstable or noisy profiles.

A full list of cluster assignments appears in:

```
data/processed/cluster_members.csv
```

## Project Structure

```
gtd-country-clusters/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── load_gtd.py
│   ├── build_country_features.py
│   ├── build_country_features_full.py
│   ├── prepare_kmeans_data.py
│   ├── run_kmeans.py
│   ├── interpret_clusters.py
│   ├── plot_pca_scatter.py
│   ├── plot_behavior_heatmap.py
│   └── plot_attacktype_heatmap.py
│
├── figures/
│
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Jbrog31/gtd-country-clusters.git
cd gtd-country-clusters
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Place the GTD Excel file here:

```
data/raw/GlobalTerrorismDatabase.xlsx
```

## Workflow

### 1. Load GTD data

```bash
python src/load_gtd.py
```

### 2. Build intermediate features

```bash
python src/build_country_features.py
```

### 3. Build full feature dataset

```bash
python src/build_country_features_full.py
```

### 4. Prepare k-means matrix

```bash
python src/prepare_kmeans_data.py
```

### 5. Run k-means clustering

```bash
python src/run_kmeans.py
```

### 6. Interpret clusters

```bash
python src/interpret_clusters.py
```

### 7. Generate visualizations

```bash
python src/plot_pca_scatter.py
python src/plot_behavior_heatmap.py
python src/plot_attacktype_heatmap.py
```

## Results Summary

The optimal number of clusters was k = 3.

### Cluster 0 — High-Intensity Insurgent Conflict States
- Highest severity
- High armed assault percentage
- Many active groups

### Cluster 2 — Bombing-Dominant, Moderate-Intensity States
- Very large number of attacks
- Bombings/IEDs dominate
- High organizational diversity

### Cluster 1 — Low-Intensity / Developed States
- Lowest severity
- Small-scale or isolated incidents

## Methodology

- Country-level GTD aggregation
- Feature engineering across severity, attack types, targets, weapons, and operational metrics
- Standardization (`StandardScaler`)
- K-means clustering (`scikit-learn`)
- PCA for visualization
- Heatmaps for behavioral signatures

## Future Additions

- Temporal clustering
- External covariates (GDP, regime type, conflict data)
- Streamlit dashboard
- Additional clustering algorithms

## Citation and License

START (National Consortium for the Study of Terrorism and Responses to Terrorism). (2022). Global Terrorism Database, 1970 - 2020 [data file]. https://www.start.umd.edu/data-tools/GTD Users must comply with GTD’s terms and conditions. All code in this repository is provided under the MIT License.
