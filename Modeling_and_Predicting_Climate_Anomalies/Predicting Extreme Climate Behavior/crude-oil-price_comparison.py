# comparing prices of crude oil and air quality to determine relationship if any
# supervised: crude oil price comparison (linear regression)

from preprocessing_climate_data_functions import *
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# read in datasets
aqi_df = clean_pm_data()
oil_price_df = pd.read_csv('crude-oil-prices_1986-2025.csv')

# clean oil price data
oil_price_df.dropna(how='any', inplace=True) # remove columns with nulls
oil_price_df.rename(columns={'Crude Oil Price (Dollars per Barrel)': 'oil_price',
                             'Date': 'date'}, inplace=True) # rename columns
oil_price_df['date'] = pd.to_datetime(oil_price_df['date']) # get dates in right format

df = pd.merge(aqi_df, oil_price_df, on='date', how='inner') # merge dataframes where all values are present

# time to begin linear regression
X = df['oil_price'].to_numpy().reshape(-1, 1)
y = df['aqi'].to_numpy().reshape(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2021)

model = LinearRegression()
model.fit(X_train, y_train)
predicted_aqis = model.predict(X_test)

# other metrics for evaluation
mse = mean_squared_error(y_test, predicted_aqis)
r2 = r2_score(y_test, predicted_aqis)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# plot data and regression line
plot_points = df.sample(frac=0.1) # only plotting 10% of data for easier viewing
sns.scatterplot(data=plot_points, x='oil_price', y='aqi', color='blue', label='10 Percent of Actual Data')
plt.plot(X_test, predicted_aqis, color='red', label='Regression Line')
plt.xlabel('Crude Oil Price (Dollars per Barrel)')
plt.ylabel('Air Quality Index (AQI)')
plt.title('Linear Regression of Crude Oil Price and AQI')
plt.legend()
plt.show()