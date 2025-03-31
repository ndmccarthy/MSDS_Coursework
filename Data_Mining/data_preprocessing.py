import pandas as pd
import numpy as np


def rescale(value, series):
    # new min and max are 0 and 1
    new_val = (value - min(series))/(max(series) - min(series))
    return new_val

def standardize(value, series):
    new_val = (value - series.mean())/series.std()
    return new_val

def normalization (fname, attr, normType):
    '''
    Input Parameters:
        fname: Name of the csv file contiaining historical quotes (path)
        attr: The attribute to be normalized 
        normType: The type of normalization ('min_max' or 'z-score')
    Output:
        a dictionary where each key is the original column value and each value is the normalised column value. 
    '''
    # grab column out of file
    df = pd.read_csv(fname)
    col = df.iloc[:, attr]
    norm_col = col.copy()
    # calculate correct normalization for each row
    if normType == 'min_max':
        norm_col = norm_col.apply(lambda x: rescale(x, col))
    else:
        norm_col = norm_col.apply(lambda x: standardize(x, col))
    result = dict(zip(col, norm_col))
    return result

def correlation (fname1, attr1, fname2, attr2):
    '''
    Input Parameters:
        fname1: name of the first csv file
        attr1: The attribute to consider in the first csv file (fname1)
        fname2: name of the second csv file
        attr2: The attribute to consider in the second csv file (fname2)
        
    Output:
        correlation coefficient between attr1 in fname1 and attr2 in fname2
    '''
    # make files into data frames
    df1 = pd.read_csv(fname1)
    df2 = pd.read_csv(fname2)
    col1 = df1.iloc[attr1]
    col2 = df2.iloc[attr2]
    # get correlation coefficient
    correlation_matrix = np.corrcoef(col1, col2)
    correlation_coefficient = correlation_matrix[0, 1]
    return correlation_coefficient


############################################################################

import matplotlib
# Plot size to 14" x 7"
matplotlib.rc('figure', figsize = (14, 7))
# Font size to 14
matplotlib.rc('font', size = 14)
# Do not display top and right frame lines
matplotlib.rc('axes.spines', top = False, right = False)
# Remove grid lines
matplotlib.rc('axes', grid = False)
# Set backgound color to white
matplotlib.rc('axes', facecolor = 'white')

def temporal_graph():
    '''Input : x_data and y_data are the lists containing the data points for x and y axis
    xlabel and ylabel are the labels that should be given to the corresponding axes
    title contains the title of the graph
    
    Output : 
    Plot the temporal change of attributes High and Low values
    Return a temporal graph with attributes Date on x-axis and a tuple of High and Low on y-axis displayed
    
    x_data - a python list of Dates using "Date" attribute from the dataset
    y_data - a tuple of the High and Low values respectively. 'High' and 'Low' should be stored as python lists.
             Ex: y_data = (list(df['attr_1']), list(df['attr_2']))
    xlabel, ylabel - A string value representing the axes labels
    title - A string representing the title for the graph
    '''
    # set up data and labels
    df = pd.read_csv('./data/HistoricalQuotes.csv')
    dates = df["Date"]
    x_data = list(dates)
    highs = df["High"]
    lows = df["Low"]
    y_data = (list(highs), list(lows))
    xlabel = "Date"
    ylabel = "Highs and Lows"
    title = "Temporal Change of Highs and Lows for Historical Quotes"
    # create graph
    import matplotlib.pyplot as plt
    plt.plot(x_data, y_data[0], marker = '.', linestyle = '-', color = 'blue', label = 'High')
    plt.plot(x_data, y_data[1], marker = '.', linestyle = '-', color = 'green', label = 'Low')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()
    return x_data,y_data,xlabel,ylabel,title

def boxplot():
    '''Input : x_data and y_data are the lists containing the data points for x and y axis
    base_color and median_color can be used to set colors in the graph.
    xlabel and ylabel are the labels that should be given to the corresponding axes
    title contains the title of the graph.
    
    Output : A boxplot with Open and Close attributes on the x-axis displayed
    
    x_data - a tuple of Open and Close values respectively. Open and Close should be stored as a python list.
             Ex: x_data = (list(df['attr_1']), list(df['attr_2']))
    xlabel, ylabel - A string value representing the axes labels
    title - A string representing the title for the graph
    '''
    # set data and labels
    df = pd.read_csv('./data/HistoricalQuotes.csv')
    opens = df["Open"]
    closes = df["Close"]
    x_data = (list(opens), list(closes))
    xlabel = "Open and Close"
    ylabel = "Values"
    title = "Box Plot of Open and Close Values for Historical Quotes"
    # create plot
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.boxplot(x_data)
    ax.set_xticklabels(["Open", "Close"])
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.show()
    return x_data,xlabel,ylabel,title

def histogram():
    '''Input : data is the list containing the data points for histogram buckets
    xlabel and ylabel are the labels that should be given to the corresponding axes
    title contains the title of the graph
    
    Output : A histogram of the Volume attribute displayed
    
    data - A python list containing the data associated with the Volume attribute
    x_label, y_label - A string representing the axes labels 
    '''
    # get data and labels
    df = pd.read_csv('./data/HistoricalQuotes.csv')
    volumes = df["Volume"]
    data = list(volumes)
    x_label = "Volume"
    y_label = "Frequency"
    # create plot
    import matplotlib.pyplot as plt
    plt.hist(data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title("Frequency of Volumes for Historical Quotes")
    plt.show()
    return data, x_label, y_label

def amzn_new_plot():
    '''Define this function as you would seem fit to display the plot that interests you using
    the same dataset. Define your function parameters and display the resulting plots'''
    # making a scatter plot of Open versus Close
    # get data
    df = pd.read_csv('./data/HistoricalQuotes.csv')
    opens = list(df["Open"])
    closes = list(df["Close"])
    # make plot
    import matplotlib.pyplot as plt
    plt.scatter(opens, closes)
    plt.xlabel("Open")
    plt.ylabel("Close")
    plt.title("Scatter Plot of Open and Close for Historical Quotes")
    plt.show()
    return opens, closes