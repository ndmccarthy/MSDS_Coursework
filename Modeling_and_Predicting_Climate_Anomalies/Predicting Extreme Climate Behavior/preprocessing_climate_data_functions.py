# functions for preprocessing climate data for multiple use

import pandas as pd
import requests
import time

def prepare_climate_data():
    # read in data
    print("Reading in climate data")
    df = pd.read_csv('HOU_1998-2025_Climate-Data.csv')

    # begin cleaning data
    print('Cleaning climate data')
    unwanted_cols = ['STATION', 'WT01', 'WT02', 'WT03','WT04',
                     'WT05','WT06', 'WT09', 'WT10', 'WT11', 'WT13',
                     'WT14', 'WT15', 'WT16', 'WT17', 'WT18', 'WT21']
    df.drop(columns=unwanted_cols, inplace=True) # remove unwanted columns

    # rename columns
    col_names = {'DATE': 'date',
                'AWND': 'avg_wind',
                'PRCP': 'precipitation',
                'TMAX': 'max_temp',
                'TMIN': 'min_temp',
                'WT07': 'dust',
                'WT08': 'haze',
                'WSF5': 'fastest_wind', # fastest 5-second wind speed
                'WDF5': 'fastest_wind_direction' # direction of fastest 5-second wind speed
                }
    df.rename(columns=col_names, inplace=True)
    
    # fill nulls in dust and haze columns with 0
    df[['dust', 'haze']] = df[['dust', 'haze']].fillna(0)

    # remove rows with nulls in any other column
    df.dropna(how='any', inplace = True)
    
    # make date column in date format
    df['date'] = pd.to_datetime(df['date'])

    # make dust and haze columns bools
    df['dust'] = df['dust'].astype(bool)
    df['haze'] = df['haze'].astype(bool)

    print('Climate data ready')

    return df

def grab_pm_data():
    url = 'https://aqs.epa.gov/data/api/dailyData/bySite?email=nicole.deere21@gmail.com&key=amberfrog15'
    param = '&param=88502' # grabbing PM2.5 in micrograms/cubic meter --> the more there is, the lower the air quality
    state = '&state=48' # 48 is code for Texas
    county = '&county=201' # 201 is code for Harris County
    site = '&site=1035' # Clinton monitor east of downtown (near Galena Park)
    
    # initialize with 2025 data
    print('Initializing PM2.5 dataframe')
    bdate = '&bdate=20250101'
    edate = '&edate=20250616'
    pm_url = url + param + bdate + edate + state + county + site
    pm_response = requests.get(pm_url)
    pm_data = pm_response.json()
    pm_df = pd.DataFrame(pm_data['Data'])

    for year in range(1998, 2025): # can only grab data for one year at a time
        print(f'Grabbing data from {year}')
        bdate = f'&bdate={year}0101'
        edate = f'&edate={year}1231'
        year_url = url + param + bdate + edate + state + county + site
        response = requests.get(year_url)
        data = response.json()
        print(data)
        if data['Header'][0]['status'] != 'No data matched your selection':
            year_df = pd.DataFrame(data['Data'])
            pm_df = pd.concat([pm_df, year_df])
        time.sleep(5)
    
    pm_df.to_csv('pm2.5_data.csv', index=False)

def clean_pm_data():
    print('Reading in PM2.5 data')
    df = pd.read_csv('pm2.5_data.csv')

    print('Cleaning PM2.5 data')
    unwanted_cols = ['date_of_last_change', 'cbsa', 'cbsa_code', 'city', 'county',
                     'state', 'site_address', 'local_site_name', 'method', 'method_code',
                     'first_max_hour', 'first_max_value', 'arithmetic_mean', 'validity_indicator', 'observation_percent',
                     'observation_count', 'event_type', 'units_of_measure', 'pollutant_standard', 'sample_duration',
                     'sample_duration_code', 'parameter', 'datum', 'longitude', 'latitude',
                     'poc', 'parameter_code', 'site_number', 'county_code', 'state_code']
    df.drop(columns=unwanted_cols, inplace=True)

    df.rename(columns={'date_local': 'date'},  inplace=True) # rename date column
    df.dropna(how='any', inplace=True) # drop rows with nulls
    df['date'] = pd.to_datetime(df['date']) # put date column in correct format

    return df