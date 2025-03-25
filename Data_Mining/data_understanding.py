# Data Understanding

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
The Function below should return the following attributes for the ith column:

Number of objects
The minimum value
The maximum value
The mean value
The standard deviation value
The Q1 value
The median value
The Q3 value
The IQR value
'''
def calculate(dataFile, col_num):
    """
    Input Parameters:
        dataFile: The dataset file.
        ithAttre: The ith attribute for which the various properties must be calculated.

    Default value of 0,infinity,-infinity are assigned to all the variables as required. 
    """
    # set defaults
    numObj, minValue, maxValue, mean, stdev, Q1, median, Q3, IQR = [0,"inf","-inf",0,0,0,0,0,0]
    # open csv as pandas dataframe
    df = pd.read_csv(dataFile)
    # make column a list and remove na
    col = df.iloc[:, col_num]
    col = col.dropna()
    # get length for number of objects
    numObj = len(col)
    # get min and max values
    minValue = min(col)
    maxValue = max(col)
    # create sum then get mean
    mean = col.mean()
    # get standard deviation
    stdev = np.std(col)
    # get Q1, median, and Q3
    Q1 = col.quantile(0.25)
    median = col.quantile(0.5)
    Q3 = col.quantile(0.75)
    # calculate IQR from Q1 and Q3
    IQR = Q3 - Q1
    return numObj, minValue, maxValue, mean, stdev, Q1, median, Q3, IQR

# Scatter plot of columns with attributes CO on x-axis and AFDP on y-axis
# Return the x values, y values, title, x-label and the y-label
def func():
    # Output: x, y, title, x-label, y-label
    title = 'CO vs. AFDP'
    x_label = 'CO'
    y_label = 'AFDP'
    df = pd.read_csv("./data/dataset.csv")
    x = df.loc["CO"]
    y = df.loc["AFDP"]
    
    return x, y, title, x_label, y_label