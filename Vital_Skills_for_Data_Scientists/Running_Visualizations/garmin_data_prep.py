import pandas as pd

# file paths for the Garmin data
activities_path = "../../../../Personal/Running/Garmin_Data/DI_CONNECT/DI-Connect-Fitness/nicole.deere21@gmail.com_0_summarizedActivities.json"
load1_path = "../../../../Personal/Running/Garmin_Data/DI_CONNECT/DI-Connect-Metrics/MetricsAcuteTrainingLoad_20240928_20250106_113414287.json"
load2_path = "../../../../Personal/Running/Garmin_Data/DI_CONNECT/DI-Connect-Metrics/MetricsAcuteTrainingLoad_20250106_20250416_113414287.json"
load3_path = "../../../../Personal/Running/Garmin_Data/DI_CONNECT/DI-Connect-Metrics/MetricsAcuteTrainingLoad_20250416_20250725_113414287.json"

# Load and process the Garmin activities data into dataframes
# upload activities data
activities = pd.read_json(activities_path)
activities_df = pd.json_normalize(activities['summarizedActivitiesExport'][0])

# upload training load data into single dataframe
df1 = pd.read_json(load1_path)
df2 = pd.read_json(load2_path)
df3 = pd.read_json(load3_path)
load_df = pd.concat([df1, df2, df3], ignore_index= True)


# clean up activities data
# drop non-running activities and unnecessary columns
nonrun_activities = ['lap_swimming', 'strength_training', 'indoor_cycling', 'open_water_swimming', 'walking',
                     'treadmill_running', 'resort_skiing', 'incident_detected', 'yoga', 'e_bike_fitness',
                     'other']
outside_Houston = ['Galveston', 'Grayson County', 'Salem', 'College Station', 'Brenham',
                   'Cedar Park', 'Galveston County']
useless_activity_data = ['activityId', 'uuidMsb', 'uuidLsb', 'description', 'userProfileId',
                         'timeZoneId', 'workoutComplianceScore', 'workoutFeel', 'name', 'eventTypeId',
                         'rule', 'sportType', 'startTimeGmt', 'activityType', 'calories',
                         'bmrCalories', 'elapsedDuration', 'movingDuration', 'deviceId', 'manufacturer',
                         'trainingEffectLabel', 'aerobicTrainingEffectMessage', 'anaerobicTrainingEffectMessage',
                         'moderateIntensityMinutes', 'vigorousIntensityMinutes', 'autoCalcCalories', 'startLongitude',
                         'startLatitude', 'vO2MaxValue', 'avgDoubleCadence', 'maxDoubleCadence', 'endLongitude',
                         'endLatitude', 'waterEstimated', 'splitSummaries', 'splits', 'differenceBodyBattery',
                         'maxLatitude', 'maxLongitude', 'minLatitude', 'minLongitude', 'beginTimestamp',
                         'avgSpeed', 'maxSpeed', 'aerobicTrainingEffect', 'anaerobicTrainingEffect',
                         'avgPower', 'maxPower', 'steps', 'normPower', 'isRunPowerWindDataEnabled',
                         'powerTimeInZone_0', 'powerTimeInZone_1', 'powerTimeInZone_2', 'powerTimeInZone_3',
                         'powerTimeInZone_4', 'powerTimeInZone_5', 'runPowerWindDataEnabled',
                         'avgGradeAdjustedSpeed', 'workoutId', 'workoutRpe', 'avgVerticalSpeed', 'lapCount',
                         'avgVerticalOscillation', 'avgGroundContactTime', 'avgStrideLength', 'avgVerticalRatio',
                         'maxVerticalSpeed', 'avgFractionalCadence', 'maxFractionalCadence', 'locationName',
                         'maxElevation', 'avgRunCadence', 'maxRunCadence', 'hrTimeInZone_0', 'hrTimeInZone_1',
                         'hrTimeInZone_2', 'hrTimeInZone_3', 'hrTimeInZone_4', 'hrTimeInZone_5', 'hrTimeInZone_6',
                         'purposeful', 'favorite', 'pr', 'elevationCorrected', 'atpActivity', 'decoDive', 'parent',
                         'maxHr', 'minHr', 'activityTrainingLoad', 'minElevation']
# remove non-running activities
activities_df.drop(activities_df[activities_df['activityType'].isin(nonrun_activities)].index, inplace=True)
# remove activities outside of Houston
activities_df.drop(activities_df[activities_df['locationName'].isin(outside_Houston)].index, inplace=True)
# drop columns that have no data
activities_df.dropna(axis=1, how='all', inplace=True)
# drop unnecessary columns (see list above)
activities_df.drop(columns=useless_activity_data, inplace=True)
# convert time columns to readable formats
activities_df['startTimeLocal'] = pd.to_datetime(activities_df['startTimeLocal'], unit='ms')
activities_df['date'] = activities_df['startTimeLocal'].dt.date.astype('datetime64[ns]')
activities_df['time'] = activities_df['startTimeLocal'].dt.time
activities_df['duration'] = activities_df['duration'] / 60000 # convert from milliseconds to minutes
activities_df['distance'] = round(activities_df['distance'] / 160934, 2) # convert from centimeters to miles
feet_columns = ['elevationGain', 'elevationLoss']
activities_df[feet_columns] = round(activities_df[feet_columns] / 30.48, 0) # convert from centimeters to feet
# create pace column
activities_df['pace'] = activities_df['duration'] / activities_df['distance']

# clean up training load data
useless_load_data = ['userProfilePK', 'deviceId', 'timestamp', 'acwrStatus', 'acwrStatusFeedback', 'acwrPercent']
load_df.drop(columns=useless_load_data, inplace=True)
load_df['calendarDate'] = pd.to_datetime(load_df['calendarDate'], unit='ms')
load_df.drop_duplicates(subset='calendarDate', keep='first', inplace=True)

# merge activities and training load data
running_df = pd.merge(activities_df, load_df, left_on='date', right_on='calendarDate', how='left') # keep only info relevant to days with running in Houston tracked
running_df.drop(columns=['calendarDate', 'startTimeLocal'], inplace=True) # removes redundant date columns
running_df.dropna(axis=0, how='any', inplace=True)  # drop rows with NaN values in the merged data

# read in weather data
weather_df = pd.read_excel('Weather.xlsx')

# clean up weather data
weather_cols_to_drop = ['pressure_max', 'pressure_min', 'pressure_avg', 'precipitation_inches',
                        'temp_min', 'temp_max', 'wind_mph_max', 'wind_mph_min',
                        'dewpoint_max', 'dewpoint_min', 'humidity_max', 'humidity_min']
weather_df.drop(columns= weather_cols_to_drop, inplace=True)

# merge weather data with running data
running_df = pd.merge(running_df, weather_df, left_on='date', right_on='date', how='left')

# save the cleaned data to a CSV file
running_df.to_csv('running_data.csv', index=False)
