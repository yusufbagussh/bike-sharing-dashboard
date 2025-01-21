import pandas as pd
import os
# Load the datasets
def load_datasets():
    day_data_path = os.path.join(os.getcwd(), 'data', 'day.csv')
    hour_data_path = os.path.join(os.getcwd(), 'data', 'hour.csv')

    # 1. Tahap Persiapan
    print("Preview of 'day.csv':")
    print(day_data.head())
    print("\nPreview of 'hour.csv':")
    print(hour_data.head())


    # 2. Tahap Gathering Data
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])
    hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
    merged_data = hour_data.merge(day_data[['dteday', 'season', 'holiday', 'workingday', 'weathersit']], 
                                on='dteday', how='left')
    print("\nMerged Dataset Preview:")
    print(merged_data.head())

    # 3. Tahap Assessing Data
    print("\nDay Data Info:")
    print(day_data.info())
    print("\nHour Data Info:")
    print(hour_data.info())
    print("\nMissing Values in Day Data:")
    print(day_data.isnull().sum())
    print("\nMissing Values in Hour Data:")
    print(hour_data.isnull().sum())
    print("\nDuplicate Rows in Day Data:", day_data.duplicated().sum())
    print("Duplicate Rows in Hour Data:", hour_data.duplicated().sum())
    print("\nSummary Statistics for 'cnt' (day.csv):")
    print(day_data['cnt'].describe())
    print("\nSummary Statistics for 'cnt' (hour.csv):")
    print(hour_data['cnt'].describe())

    # 4. Tahap Cleaning Data
    # Handling missing values (if any)
    hour_data.fillna(method='ffill', inplace=True)

    # Removing duplicate rows
    day_data = day_data.drop_duplicates()
    hour_data = hour_data.drop_duplicates()

    # Handling outliers in 'cnt' using IQR
    Q1 = day_data['cnt'].quantile(0.25)
    Q3 = day_data['cnt'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    day_data = day_data[(day_data['cnt'] >= lower_bound) & (day_data['cnt'] <= upper_bound)]

    # Normalize numerical columns (optional)
    numerical_cols = ['temp', 'atemp', 'hum', 'windspeed']
    day_data[numerical_cols] = day_data[numerical_cols].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    print("\nCleaned Day Data Preview:")
    print(day_data.head())
    
    # Preview data for season and weather
    print("Preview of Data for Season and Weather:")
    print(day_data[['season', 'weathersit', 'cnt']].head())

    # Statistik Deskriptif
    season_weather_stats = day_data.groupby(['season', 'weathersit'])['cnt'].describe()
    print("\nStatistics for Rentals by Season and Weather:")
    print(season_weather_stats)

    # Preview data for working day and holiday
    print("\nPreview of Data for Working Day and Holiday:")
    print(day_data[['workingday', 'holiday', 'cnt']].head())

    # Statistik Deskriptif
    working_holiday_stats = day_data.groupby(['workingday', 'holiday'])['cnt'].describe()
    print("\nStatistics for Rentals by Working Day and Holiday:")
    print(working_holiday_stats)
    return day_data
