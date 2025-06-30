from sklearn.ensemble import RandomForestRegressor
from preprocessing_climate_data_functions import *
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

# grab data
climate_df = prepare_climate_data()
aqi_df = clean_pm_data()

df = pd.merge(climate_df, aqi_df, on='date', how='inner')
df.drop(columns=['date'], inplace=True) # no longer need date and need to drop for scaling

# scale data
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# split data
X = df.drop(columns=['aqi'])
y = df['aqi']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2021)

model = RandomForestRegressor(n_estimators=100, random_state=2021)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# evaluate
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"R-squared: {r2:.3f}")
print(f"Mean Squared Error: {mse:.3f}")

# plot feature importance
importances = pd.Series(model.feature_importances_, index=X.columns)
importances_sorted = importances.sort_values(ascending=True)

plt.figure(figsize=(8, 6))
importances_sorted.plot(kind='barh', color='teal')
plt.title('Feature Importance (Random Forest)')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.show()

# plot regressions
plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred, color='salmon', edgecolor='k')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted')
plt.tight_layout()
plt.show()

# plot residuals
residuals = y_test - y_pred

plt.figure(figsize=(8, 5))
plt.scatter(y_pred, residuals, color='gray', alpha=0.6, edgecolor='k')
plt.axhline(0, color='red', linestyle='--', linewidth=1)
plt.xlabel('Predicted')
plt.ylabel('Residuals (Actual - Predicted)')
plt.title('Residuals Plot')
plt.tight_layout()
plt.show()