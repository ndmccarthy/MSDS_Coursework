from data_understanding import calculate
from data_preprocessing import *

csv = "test_data.csv"
column = 2

numObj, minValue, maxValue, mean, stdev, Q1, median, Q3, IQR = calculate(csv, 2)
print(f"Mean: {mean}")
print(f"\nStDev: {stdev}")
print(f"\nMin: {minValue}")
print(f"\nMax: {maxValue}")

mm = normalization(csv, "Current_Age", 'min_max')
print(mm)
z = normalization(csv, "Current_Age", 'z-score')
print(z)