import re
import os
import pandas as pd
import numpy as np
from datetime import datetime

def clean_daily_weather_data(read_path, write_path):
    """
    Cleans the raw daily weather data and saves the cleaned data to a new CSV file.
    """

    # cities and their coordinates
    CITY_COORDINATES = {
        'Yerevan': {'Latitude': 40.1872, 'Longitude': 44.5152},
        'Ashtarak': {'Latitude': 40.2929, 'Longitude': 44.3505},
        'Artashat': {'Latitude': 39.9535, 'Longitude': 44.5520},
        'Armavir': {'Latitude': 40.1554, 'Longitude': 44.0387},
        'Gavar': {'Latitude': 40.3513, 'Longitude': 45.1273},
        'Hrazdan': {'Latitude': 40.5353, 'Longitude': 44.7693},
        'Vanadzor': {'Latitude': 40.8074, 'Longitude': 44.4970},
        'Gyumri': {'Latitude': 40.7929, 'Longitude': 43.8465},
        'Kapan': {'Latitude': 39.2077, 'Longitude': 46.4068},
        'Ijevan': {'Latitude': 40.8791, 'Longitude': 45.1471},
        'Yeghegnadzor': {'Latitude': 39.7633, 'Longitude': 45.3308}
    }
    
    df = pd.read_csv(read_path)
    
    # adding 'Scraped Date' with current timestamp
    df['Scraped Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # extracting and cleaning 'Temperature' from 'Weather' column
    df['Temperature'] = df['Weather'].astype(str).apply(
        lambda x: float(re.sub(r'[^\d\.-]', '', x)) if re.search(r'[-+]?\d*\.?\d+', x) else np.nan
    )
    
    # extracting and cleaning 'Humidity' as float
    df['Humidity'] = df['Humidity'].astype(str).apply(
        lambda x: float(re.sub(r'[^\d\.-]', '', x)) if re.search(r'[-+]?\d*\.?\d+', x) else np.nan
    )
    
    # extracting and cleaning 'Wind Speed (km/h)' from 'Wind' column
    df['Wind Speed (km/h)'] = df['Wind'].astype(str).apply(
        lambda x: float(re.sub(r'[^\d\.-]', '', x)) if re.search(r'[-+]?\d*\.?\d+', x) else np.nan
    )
    
    # extracting and cleaning 'Pressure (mb)' from 'Pressure' column
    df['Pressure (mb)'] = df['Pressure'].astype(str).apply(
        lambda x: float(re.sub(r'[^\d\.-]', '', x)) if re.search(r'[-+]?\d*\.?\d+', x) else np.nan
    )
    
    # extracting and cleaning 'Ceiling (m)' from 'Ceiling' column
    df['Ceiling (m)'] = df['Ceiling'].astype(str).apply(
        lambda x: float(re.sub(r'[^\d\.-]', '', x)) if re.search(r'[-+]?\d*\.?\d+', x) else np.nan
    )
    
    # extracting and cleaning 'Dew Point' from 'Dew Point' column
    df['Dew Point'] = df['Dew Point'].astype(str).apply(
        lambda x: float(re.sub(r'[^\d\.-]', '', x)) if re.search(r'[-+]?\d*\.?\d+', x) else np.nan
    )
    
    # extracting and cleaning 'Visibility (km)' from 'Visibility' column
    df['Visibility (km)'] = df['Visibility'].astype(str).apply(
        lambda x: float(re.sub(r'[^\d\.-]', '', x)) if re.search(r'[-+]?\d*\.?\d+', x) else np.nan
    )
    
    # extracting 'Sunrise' time in HH:MM format
    df['Sunrise'] = pd.to_datetime(
        df['Sunrise'].astype(str).str.extract(r'(\d{1,2}:\d{2})')[0],
        format='%H:%M',
        errors='coerce'
    ).dt.time
    
    # extracting 'Sunset' time in HH:MM format
    df['Sunset'] = pd.to_datetime(
        df['Sunset'].astype(str).str.extract(r'(\d{1,2}:\d{2})')[0],
        format='%H:%M',
        errors='coerce'
    ).dt.time
    
    # converting 'Day Duration' from 'HH:MM' to total minutes
    df[['Day_Hours', 'Day_Minutes']] = df['Day Duration'].astype(str).str.extract(r'(\d+):(\d+)')
    df['Day Duration (min)'] = df['Day_Hours'].astype(float) * 60 + df['Day_Minutes'].astype(float)
    df.drop(['Day_Hours', 'Day_Minutes'], axis=1, inplace=True)
    
    # extracting 'Moonrise' time in HH:MM format
    df['Moonrise'] = pd.to_datetime(
        df['Moonrise'].astype(str).str.extract(r'(\d{1,2}:\d{2})')[0],
        format='%H:%M',
        errors='coerce'
    ).dt.time
    
    # extracting 'Moonset' time in HH:MM format
    df['Moonset'] = pd.to_datetime(
        df['Moonset'].astype(str).str.extract(r'(\d{1,2}:\d{2})')[0],
        format='%H:%M',
        errors='coerce'
    ).dt.time
    
    # converting 'Moon Duration' from 'HH:MM' to total minutes
    df[['Moon_Hours', 'Moon_Minutes']] = df['Moon Duration'].astype(str).str.extract(r'(\d+):(\d+)')
    df['Moon Duration (min)'] = df['Moon_Hours'].astype(float) * 60 + df['Moon_Minutes'].astype(float)
    df.drop(['Moon_Hours', 'Moon_Minutes'], axis=1, inplace=True)
    
    # dropping original columns that are no longer needed
    columns_to_drop = [
        'Weather', 'Wind', 'Pressure', 'Cloud Cover', 'Sunrise', 'Sunset',
        'Day Duration', 'Moonrise', 'Moonset', 'Moon Duration'
    ]
    df_clean = df.drop(columns=columns_to_drop, errors='ignore')
    
    # handling missing values by filling with column mean for numeric columns
    numeric_cols = [
        'Temperature', 'Humidity', 'Wind Speed (km/h)', 'Pressure (mb)',
        'Ceiling (m)', 'Dew Point', 'Visibility (km)', 
        'Day Duration (min)', 'Moon Duration (min)'
    ]
    
    for col in numeric_cols:
        if col in df_clean.columns and df_clean[col].isnull().any():
            mean_value = df_clean[col].mean()
            df_clean[col].fillna(mean_value, inplace=True)
    
    # adding Latitude and Longitude based on City
    df_clean['Latitude'] = df_clean['City'].map(
        lambda x: CITY_COORDINATES.get(x, {}).get('Latitude', np.nan)
    )
    df_clean['Longitude'] = df_clean['City'].map(
        lambda x: CITY_COORDINATES.get(x, {}).get('Longitude', np.nan)
    )
    
    # handling negative 'Moon Duration (min)' by setting them to NaN and filling with mean
    if 'Moon Duration (min)' in df_clean.columns:
        negative_durations = df_clean['Moon Duration (min)'] < 0
        if negative_durations.any():
            print("Negative Moon Durations found. Setting them to NaN and filling with mean value.")
            df_clean.loc[negative_durations, 'Moon Duration (min)'] = np.nan
            mean_moon_duration = df_clean['Moon Duration (min)'].mean()
            df_clean['Moon Duration (min)'].fillna(mean_moon_duration, inplace=True)
    
    # saving the cleaned data to a new CSV file
    df_clean.to_csv(write_path, index=False)

def run_daily_processor():
    raw_csv_path = "outputs/raw/daily-weather-data.csv"
    output_dir = "outputs/processed"
    os.makedirs(output_dir, exist_ok=True)
    cleaned_csv_path = os.path.join(output_dir, "daily-weather-data-clean.csv")
    clean_daily_weather_data(raw_csv_path, cleaned_csv_path)