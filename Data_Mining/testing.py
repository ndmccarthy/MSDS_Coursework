from data_understanding import *

csv = "test_data.csv"
column = 2

# Testing the func() function
x, y, title, x_label, y_label = func()
plt.scatter(x, y)
plt.title(title)
plt.xlabel(x_label)
plt.ylabel(y_label)