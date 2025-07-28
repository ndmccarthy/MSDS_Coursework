import pandas as pd
import altair as alt

# load the data
running_df = pd.read_csv('running_data.csv')

# get correct data types
running_df['time'] = running_df['time'].astype('datetime64[ns]')
running_df['date'] = running_df['date'].astype('datetime64[ns]')
print(running_df.dtypes)

# create a scatter plot of pace and time
chart  = alt.Chart(running_df).mark_circle().encode(x = 'time', y = 'pace')
print(chart.to_html())