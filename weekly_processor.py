import os
import pandas as pd
import numpy as np

def clean_weekly_weather_data(raw_csv, clean_csv):
    """
    Cleans the raw weekly weather data and saves the cleaned data to a new CSV file.
    """
    
    df = pd.read_csv(raw_csv)
    df[['High_Temp', 'Low_Temp']] = df['Hi/Lo'].str.replace('°','').str.split('/', expand=True).astype(float)
    df['Avg_Temp'] = (df['High_Temp'] + df['Low_Temp']) / 2  # calculating average temperature

    # converting 'Date' to Datetime Format (Assuming Year 2025)
    df['Date'] = pd.to_datetime(df['Date'] + '.2025', format='%a %d.%m.%Y')

    city_coords = {
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

    def get_coordinates(city):
        return pd.Series(city_coords.get(city, {'Latitude': np.nan, 'Longitude': np.nan}))
    
    # adding 'Latitude' and 'Longitude' columns
    df[['Latitude', 'Longitude']] = df['City'].apply(get_coordinates)

    # handling missing values
    numeric_cols = ['Precipitation', 'Snow', 'High_Temp', 'Low_Temp', 'Avg_Temp', 'Latitude', 'Longitude']
    
    for col in numeric_cols:
        if df[col].isnull().any():
            mean_value = df[col].mean()
            df[col].fillna(mean_value, inplace=True)

    # dropping unnecessary columns
    columns_to_drop = ['Hi/Lo']
    df_clean = df.drop(columns=columns_to_drop)
    
    df_clean.to_csv(clean_csv, index=False)

def run_weekly_processor():
    raw_csv = "outputs/raw/weekly-weather-data.csv"
    clean_csv = "outputs/processed/weekly-weather-data-clean.csv"
    os.makedirs("outputs/processed", exist_ok=True)
    clean_weekly_weather_data(raw_csv, clean_csv)
