# LAB 1

import requests
import pandas as pd

url = "https://datausa.io/api/data?drilldowns=Nation&measures=Population"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    print("Failed to retrieve data.")

df = pd.json_normalize(data['data'])
print(df)


# LAB 2

import dataretrieval.nwis as nwis

# Define site number and date range
site_no = '07106500'
start_date = '2024-03-01'
end_date = '2024-03-31'
serv_type = 'dv'

# Retrieve the data.
data = nwis.get_record(sites= site_no, service= serv_type, start= start_date, end= end_date)

# The parameter code for streamflow is '00060' and for the daily value we will be using '00060_Mean' column.
# Find the mean of the streamflow data for March 2024 i.e. find the mean of the '00060_Mean' column

mean_streamflow = round(data['00060_Mean'].mean(), 0)
