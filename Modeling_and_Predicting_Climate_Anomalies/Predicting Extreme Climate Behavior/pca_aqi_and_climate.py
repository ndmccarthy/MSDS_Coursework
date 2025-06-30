# unsupervised: wind speed and direction clustering with air quality (PCA and K-Means clustering)

# wind from east: 90 degrees
# wind from south: 180 degrees

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from preprocessing_climate_data_functions import *
import matplotlib.pyplot as plt
import numpy as np

# grab data
climate_df = prepare_climate_data()
aqi_df = clean_pm_data()

df = pd.merge(climate_df, aqi_df, on='date', how='inner')
df.drop(columns=['date'], inplace=True) # no longer need date and need to drop for scaling

# scale data
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# conduct PCA
pca = PCA(n_components=3)
df_pca = pca.fit_transform(df_scaled)

# identify which features affect components the most
loadings = pd.DataFrame(pca.components_.T,
                        index=df.columns,
                        columns=['PC1', 'PC2', 'PC3'])
print("PCA Loadings:\n", loadings)

abs_loadings = loadings.abs() # grabbing absolute values since strength can be measured in positive or negative directions

# Sort by PC1 to make the chart easier to read (optional)
abs_loadings = abs_loadings.sort_values(by='PC1', ascending=False)

# Explained variance
explained_var = pca.explained_variance_ratio_
cumulative_var = explained_var.cumsum()

# Scree plot
plt.figure(figsize=(8, 4))
plt.plot(range(1, len(explained_var) + 1), cumulative_var, marker='o')
plt.axhline(0.9, color='red', linestyle='--')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('PCA Scree Plot')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot absolute values of first 2 PCs
abs_loadings = loadings.iloc[:, :2].abs().sort_values(by='PC1', ascending=False)

plt.figure(figsize=(10, 6))
abs_loadings.plot(kind='barh')
plt.title('Absolute PCA Loadings (PC1 & PC2)')
plt.xlabel('Loading Magnitude')
plt.tight_layout()
plt.show()

# Scatter of observations
plt.figure(figsize=(8, 6))
plt.scatter(df_pca[:, 0], df_pca[:, 1], alpha=0.5)

# Arrows for original features
for i, feature in enumerate(df.columns):
    plt.arrow(0, 0, pca.components_[0, i]*4, pca.components_[1, i]*4,
              color='r', alpha=0.7)
    plt.text(pca.components_[0, i]*4.2, pca.components_[1, i]*4.2,
             feature, color='r', ha='center', va='center')
    
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA Biplot (AQI and Climate Features)')
plt.grid(True)
plt.tight_layout()
plt.show()