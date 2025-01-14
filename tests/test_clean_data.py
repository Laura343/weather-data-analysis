import pytest
import os
import pandas as pd
from daily_processor import clean_daily_weather_data
from weekly_processor import clean_weekly_weather_data

# Fixture for daily weather data
@pytest.fixture
def raw_and_clean_daily_data_file(tmpdir):
    raw_data_file_path = tmpdir.join("raw_weather_data.csv")
    clean_data_file_path = tmpdir.join("cleaned_weather_data.csv")
    
    # Writing some mock raw weather data
    raw_data = """City,Weather,Humidity,Wind,Pressure,Ceiling,Dew Point,Visibility,Sunrise,Sunset,Day Duration,Moonrise,Moonset,Moon Duration
Yerevan,22C,65%,5 km/h,1020 mb,1500 m,15C,10 km,06:30,18:30,12:00,07:00,19:00,12:00
Ashtarak,18C,70%,10 km/h,1015 mb,1400 m,12C,8 km,06:45,18:15,11:30,06:50,18:05,11:15
"""
    
    with open(raw_data_file_path, "w") as f:
        f.write(raw_data)
    
    yield raw_data_file_path, clean_data_file_path


# Fixture for weekly weather data
@pytest.fixture
def raw_and_clean_weekly_data_file(tmpdir):
    raw_data_path = tmpdir.join("raw_weekly_weather.csv")
    clean_data_path = tmpdir.join("clean_weekly_weather.csv")
    
    raw_data_content = """City,Date,Hi/Lo,Precipitation,Snow
Yerevan,Mon 01.01,5/1,0.0,0
Ashtarak,Tue 02.01,6/2,0.1,0
Vanadzor,Wed 03.01,4/0,,0.5
Gyumri,Thu 04.01,-2/-6,0.0,1.0
Artashat,Fri 05.01,7/3,0.2,0.0
"""

    with open(raw_data_path, "w") as f:
        f.write(raw_data_content)
    
    yield raw_data_path, clean_data_path

# Testing daily weather data cleaning function
def test_clean_daily_weather_data(raw_and_clean_daily_data_file):

    raw_data_file_path, clean_data_file_path = raw_and_clean_daily_data_file
    
    # Call the cleaning function
    clean_daily_weather_data(raw_data_file_path, clean_data_file_path)
    
    # Check that the cleaned file exists
    assert os.path.exists(clean_data_file_path), "Cleaned file was not created"
    
    # Read the cleaned data into a DataFrame
    cleaned_df = pd.read_csv(clean_data_file_path)
    
    # Assert that the 'Scraped Date' column is in the cleaned data and not empty
    assert 'Scraped Date' in cleaned_df.columns, "'Scraped Date' column not found"
    assert cleaned_df['Scraped Date'].notnull().any(), "'Scraped Date' column is empty"
    
    # Validate transformations for the columns that should be numeric
    assert pd.api.types.is_float_dtype(cleaned_df['Temperature']), "Temperature column is not float"
    assert pd.api.types.is_float_dtype(cleaned_df['Humidity']), "Humidity column is not float"
    assert pd.api.types.is_float_dtype(cleaned_df['Wind Speed (km/h)']), "Wind Speed column is not float"
    assert pd.api.types.is_float_dtype(cleaned_df['Pressure (mb)']), "Pressure column is not float"
    assert pd.api.types.is_float_dtype(cleaned_df['Ceiling (m)']), "Ceiling column is not float"
    assert pd.api.types.is_float_dtype(cleaned_df['Visibility (km)']), "Visibility column is not float"
    
    # Validate that 'Moon Duration (min)' is a positive float and there are no negative values
    assert pd.api.types.is_float_dtype(cleaned_df['Moon Duration (min)']), "Moon Duration column is not float"
    assert (cleaned_df['Moon Duration (min)'] >= 0).all(), "Moon Duration contains negative values"
    
    # Check for 'Latitude' and 'Longitude' columns, and that they are not NaN
    assert 'Latitude' in cleaned_df.columns, "'Latitude' column not found"
    assert 'Longitude' in cleaned_df.columns, "'Longitude' column not found"
    assert cleaned_df['Latitude'].notnull().all(), "Latitude column contains NaN values"
    assert cleaned_df['Longitude'].notnull().all(), "Longitude column contains NaN values"


# Testing weekly weather data cleaning function
def test_clean_weekly_weather_data(raw_and_clean_weekly_data_file):
    raw_data_path, clean_data_path = raw_and_clean_weekly_data_file
    
    clean_weekly_weather_data(raw_data_path, clean_data_path)
    
    df_clean = pd.read_csv(clean_data_path)
    
    # Validate processed columns and data
    assert "Avg_Temp" in df_clean.columns
    assert "High_Temp" in df_clean.columns
    assert "Low_Temp" in df_clean.columns
    assert "Latitude" in df_clean.columns
    assert "Longitude" in df_clean.columns
    
    # Check processed data
    assert df_clean['High_Temp'].iloc[0] == 5.0
    assert df_clean['Low_Temp'].iloc[0] == 1.0
    assert df_clean['Avg_Temp'].iloc[0] == 3.0