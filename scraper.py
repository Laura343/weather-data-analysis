import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service("/usr/bin/chromedriver")

def init_driver():
    return webdriver.Chrome(service=service, options=chrome_options)

def scrape_weekly_weather(driver, region_name, region_url):
    driver.get(region_url)

    weather_data = []

    # finding all rows in the weekly weather table
    rows = driver.find_elements(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/table/tbody/tr')
    for row_index in range(1, len(rows) + 1):
        date_xpath = f'/html/body/div/main/div/div[2]/div/div/div[1]/table/tbody/tr[{row_index}]/td[2]'
        precip_xpath = f'/html/body/div/main/div/div[2]/div/div/div[1]/table/tbody/tr[{row_index}]/td[3]'
        snow_xpath = f'/html/body/div/main/div/div[2]/div/div/div[1]/table/tbody/tr[{row_index}]/td[4]'
        forecast_xpath = f'/html/body/div/main/div/div[2]/div/div/div[1]/table/tbody/tr[{row_index}]/td[5]/p'
        hilo_xpath = f'/html/body/div/main/div/div[2]/div/div/div[1]/table/tbody/tr[{row_index}]/td[6]'

        # extracting text
        date_text = driver.find_element(By.XPATH, date_xpath).text
        precip_text = driver.find_element(By.XPATH, precip_xpath).text
        snow_text = driver.find_element(By.XPATH, snow_xpath).text
        forecast_text = driver.find_element(By.XPATH, forecast_xpath).get_attribute("innerText")
        hilo_text = driver.find_element(By.XPATH, hilo_xpath).text

        weather_data.append({
            "Date": date_text,
            "Precipitation": precip_text,
            "Snow": snow_text,
            "Forecast": forecast_text,
            "Hi/Lo": hilo_text
        })

    weather_df = pd.DataFrame(weather_data)
    return weather_df

def scrape_daily_info(driver, region_name, region_url):
    driver.get(region_url)
    
    # daily weather data
    weather_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]')
    humidity_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[1]/div[2]/div/ul/li[2]/strong')
    wind_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[1]/div[2]/div/ul/li[1]/strong')
    pressure_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[1]/div[2]/div/ul/li[3]/strong')
    uv_index_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[1]/div[2]/div/ul/li[4]/strong')
    cloud_cover_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[1]/div[2]/div/ul/li[5]/strong')
    ceiling_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[1]/div[2]/div/ul/li[6]/strong')
    dew_point_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[1]/div[2]/div/ul/li[7]/strong')
    visibility_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[1]/div[2]/div/ul/li[8]/strong')

    sunrise_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[2]/div[1]/ul/li[1]')
    sunset_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[2]/div[1]/ul/li[2]')
    day_duration_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[2]/div[1]/ul/li[3]')

    moonrise_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[1]')
    moonset_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[2]')
    moon_duration_element = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[3]')

    # extracting text
    daily_info = {
        "Region": region_name.split("(")[1].strip(")"),
        "City": region_name.split("(")[0].strip(),
        "Weather": weather_element.text,
        "Humidity": humidity_element.text,
        "Wind": wind_element.text,
        "Pressure": pressure_element.text,
        "UV Index": uv_index_element.text,
        "Cloud Cover": cloud_cover_element.text,
        "Ceiling": ceiling_element.text,
        "Dew Point": dew_point_element.text,
        "Visibility": visibility_element.text,
        "Sunrise": sunrise_element.text,
        "Sunset": sunset_element.text,
        "Day Duration": day_duration_element.text,
        "Moonrise": moonrise_element.text,
        "Moonset": moonset_element.text,
        "Moon Duration": moon_duration_element.text,
    }

    return daily_info

# for weekly
regions_and_cities = [
    ("Yerevan", "Yerevan"),
    ("Armavir", "Armavir"),
    ("Gegharkunik", "Gavar"),
    ("Kotayk", "Hrazdan"),
    ("Lori", "Vanadzor"),
    ("Shirak", "Gyumri"),
    ("Syunik", "Kapan"),
    ("Tavush", "Ijevan"),
    ("Vayotsdzor", "Yeghegnadzor"),
    ("Ararat", "Artashat"),
    ("Aragatsotn", "Ashtarak"),
]

# for daily
current_weather_urls = [
    ("Yerevan (Yerevan)", "https://exanak.am/en/current-weather-forecast/yerevan/yerevan"),
    ("Ashtarak (Aragatsotn)", "https://exanak.am/en/current-weather-forecast/aragatsotn/ashtarak"),
    ("Artashat (Ararat)", "https://exanak.am/en/current-weather-forecast/ararat/artashat"),
    ("Armavir (Armavir)", "https://exanak.am/en/current-weather-forecast/armavir/armavir"),
    ("Gavar (Gegharkunik)", "https://exanak.am/en/current-weather-forecast/gegharkunik/gavar"),
    ("Hrazdan (Kotayk)", "https://exanak.am/en/current-weather-forecast/kotayk/hrazdan"),
    ("Vanadzor (Lori)", "https://exanak.am/en/current-weather-forecast/lori/vanadzor"),
    ("Gyumri (Shirak)", "https://exanak.am/en/current-weather-forecast/shirak/gyumri"),
    ("Kapan (Syunik)", "https://exanak.am/en/current-weather-forecast/syunik/kapan"),
    ("Ijevan (Tavush)", "https://exanak.am/en/current-weather-forecast/tavush/ijevan"),
    ("Yeghegnadzor (Vayotsdzor)", "https://exanak.am/en/current-weather-forecast/vayotsdzor/yeghegnadzor"),
]

def run_scraper():
    driver = init_driver()
    output_dir = "outputs/raw"
    os.makedirs(output_dir, exist_ok=True)

    # scraping weekly weather data
    all_weather_data = []
    for region, city in regions_and_cities:
        region_name = f"{city.capitalize()} ({region})"
        region_url = f"https://exanak.am/en/7-days-weather-forecast/{region.lower()}/{city.lower()}"
        weekly_weather_data = scrape_weekly_weather(driver, region_name, region_url)
        if weekly_weather_data is not None:
            weekly_weather_data["Region"] = region
            weekly_weather_data["City"] = city
            all_weather_data.append(weekly_weather_data)

    if all_weather_data:
        combined_weather_data = pd.concat(all_weather_data, ignore_index=True)
        column_order = ["Region", "City"] + [col for col in combined_weather_data.columns if col not in ["Region", "City"]]
        combined_weather_data = combined_weather_data[column_order]
        combined_weather_data.to_csv(os.path.join(output_dir, "weekly-weather-data.csv"), index=False, quoting=1, sep=",")
        print(f"Saved weekly weather data to {os.path.join(output_dir, 'weekly-weather-data.csv')}")

    # scraping daily weather data
    all_daily_info = []
    for region_name, region_url in current_weather_urls:
        daily_info = scrape_daily_info(driver, region_name, region_url)
        all_daily_info.append(daily_info)

    daily_info_df = pd.DataFrame(all_daily_info)
    daily_info_df.to_csv(os.path.join(output_dir, "daily-weather-data.csv"), index=False)
    print(f"Saved daily weather data to {os.path.join(output_dir, 'daily-weather-data.csv')}")

    driver.quit()