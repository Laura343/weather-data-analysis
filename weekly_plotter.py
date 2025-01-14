import os
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def visualize_weekly_weather_by_city(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Plot 1: Interactive Map: Average Temperature Distribution by City
    fig_map = px.scatter_mapbox(
        df.sort_values('Date'),
        lat='Latitude',
        lon='Longitude',
        color='Avg_Temp',
        size=[5] * len(df),
        hover_name='City',
        hover_data=['Avg_Temp', 'Precipitation', 'Snow', 'Forecast'],
        color_continuous_scale=px.colors.diverging.RdYlBu,
        range_color=[df['Avg_Temp'].min(), df['Avg_Temp'].max()],
        mapbox_style='carto-positron',
        zoom=5,
        animation_frame=df['Date'].dt.strftime('%a %d.%m'),
        title='Weekly Average Temperature Distribution Across Cities in Armenia'
    )
    fig_map.write_html(os.path.join(output_dir, 'interactive_temperature_map.html'))

    # Plot 2: Temperature Trends for Yerevan
    plt.figure(figsize=(10, 6))
    city_data = df[df['City'] == 'Yerevan']
    plt.plot(city_data['Date'], city_data['High_Temp'], label='High Temp (°C)', color='red', marker='o')
    plt.plot(city_data['Date'], city_data['Low_Temp'], label='Low Temp (°C)', color='blue', marker='o')
    plt.title("Temperature Trends for Yerevan")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    temp_trends_path = os.path.join(output_dir, 'temperature_trends_yerevan.png')
    plt.savefig(temp_trends_path)
    plt.close()

    # Plot 3: Temperature Trends Over the Week (Line Chart by City)
    df_melted = df.melt(
        id_vars=['City', 'Date'],
        value_vars=['High_Temp', 'Low_Temp', 'Avg_Temp'],
        var_name='Temperature_Type',
        value_name='Temperature'
    )
    fig_line = px.line(
        df_melted,
        x='Date',
        y='Temperature',
        color='Temperature_Type',
        facet_col='City',
        facet_col_wrap=4,
        title='Temperature Trends Over the Week for Each City in Armenia',
        labels={
            'Date': 'Date',
            'Temperature': 'Temperature (℃)',
            'Temperature_Type': 'Temperature Type'
        },
        markers=True
    )
    fig_line.write_html(os.path.join(output_dir, 'temperature_trends_all_cities.html'))
    
    # Plot 4: Precipitation and Snow by City (Bar Chart)
    df_agg = df.groupby('City').agg({'Precipitation': 'sum', 'Snow': 'sum'}).reset_index()
    df_melted_bar = df_agg.melt(
        id_vars='City',
        value_vars=['Precipitation', 'Snow'],
        var_name='Precipitation_Type',
        value_name='Amount'
    )
    fig_bar = px.bar(
        df_melted_bar,
        x='City',
        y='Amount',
        color='Precipitation_Type',
        barmode='group',
        title='Total Precipitation and Snow per City Over the Week',
        labels={'Amount': 'Amount (mm for Precipitation, cm for Snow)'}
    )
    fig_bar.write_html(os.path.join(output_dir, 'precipitation_snow_by_city.html'))
   
    # Plot 5: Precipitation Proportion by City (Pie Chart)
    precip_data = df.groupby('City')['Precipitation'].sum().reset_index()
    fig_pie = px.pie(
        precip_data,
        names='City',
        values='Precipitation',
        title='Proportion of Total Precipitation by City',
        labels={'Precipitation': 'Total Precipitation (mm)'},
        color='City',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.write_html(os.path.join(output_dir, 'precipitation_proportion_pie_chart.html'))

def run_weekly_plotter():
    """
    Loads the cleaned weekly weather data from outputs/processed
    and generates visualizations saved in outputs/visualizations/weekly.
    """
    # Input cleaned weekly data
    cleaned_csv = "outputs/processed/weekly-weather-data-clean.csv"
    # Output directory for weekly visualizations
    output_dir = "outputs/visualizations/weekly"

    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load the DataFrame, parse 'Date' as datetime
    df = pd.read_csv(cleaned_csv, parse_dates=['Date'])

    # Call the weekly visualization function
    visualize_weekly_weather_by_city(df, output_dir)
