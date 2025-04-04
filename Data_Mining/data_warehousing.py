# Data Mining Pipeline Warehousing coding assignment
# uses embedded .csv in Jupyter notebook so not useful outside of that as is

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def aggregate_by_year():
    
    # Reading dataset
    df = pd.read_csv('./dataset/dataset.csv')
    cols_to_drop = ["month", "day", "country", "state", "city", "store", "category", "product"]
    df = df.drop(cols_to_drop, axis = 1)
    df = df.groupby(['year'])['sales'].sum()
    d = df.to_dict()
    return d
aggregate_by_year()

def plot_data_cube(): 
    '''
        Output: x, y, z
    '''
    # Reading dataset
    df = pd.read_csv('./dataset/dataset.csv')
    cols_to_drop = ["month", "day", "country", "state", "city", "store", "product"]
    df = df.drop(cols_to_drop, axis = 1)
    df = df.groupby(['year', 'category'])['sales'].sum().reset_index()
    x = list(df['year'])
    y = list(df['category'])
    z = list(df['sales'])
    return x,y,z
plot_data_cube()

x, y, z = plot_data_cube()
y_codes = (list(pd.Categorical(y).codes)) # To use scatter3D() function we need to convert to categorical codes
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(projection='3d')
ax.scatter(x,y_codes,z)

plt.xticks(np.arange(min(x), max(x)+1, 1))
plt.yticks(np.arange(min(y_codes), max(y_codes)+1, 1))
ax.set_yticklabels(y)

ax.set_xlabel('Year')
ax.set_ylabel('Category')
ax.set_zlabel('TotalSales')
ax.set_title('Datacube: Aggregate Sales across year and category')
plt.show() 