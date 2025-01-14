import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

def generate_plots(read_path, output_dir):
    df_clean = pd.read_csv(read_path)
    
    # Plot 1: Temperature by City Across Regions
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 8))
    bar_plot = sns.barplot(
        x='Region', 
        y='Temperature', 
        hue='Region', 
        data=df_clean, 
        palette='coolwarm', 
        dodge=False, 
        legend=False
    )
    
    for index, row in df_clean.iterrows():
        plt.text(
            x=index, 
            y=row['Temperature'] + 0.1, 
            s=f"{row['Temperature']}℃", 
            color='black', 
            ha="center", 
            fontsize=12
        )
    
    plt.title('Temperature by City Across Regions', fontsize=18)
    plt.xlabel('Region', fontsize=14)
    plt.ylabel('Temperature (℃)', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    temp_by_region_path = os.path.join(output_dir, 'temperature_by_region.png')
    plt.savefig(temp_by_region_path)
    plt.close()
    
    # Plot 2: Grouped Bar Chart for Temperature, Humidity, and Wind Speed
    sns.set(style="whitegrid")
    df_melted = df_clean.melt(
        id_vars=['City'], 
        value_vars=['Temperature', 'Humidity', 'Wind Speed (km/h)'],
        var_name='Metric', 
        value_name='Value'
    )
    
    plt.figure(figsize=(14, 7))
    grouped_bar = sns.barplot(
        x='City', 
        y='Value', 
        hue='Metric', 
        data=df_melted, 
        palette='Set2'
    )
    
    plt.title('Temperature, Humidity, and Wind Speed Across Cities', fontsize=16)
    plt.xlabel('City', fontsize=14)
    plt.ylabel('Value', fontsize=14)
    plt.legend(title='Metric', fontsize=12, title_fontsize=12)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    
    grouped_bar_path = os.path.join(output_dir, 'grouped_bar_chart.png')
    plt.savefig(grouped_bar_path)
    plt.close()

    # Plot 3: Interactive Temperature Map

    fixed_marker_size = 10
    color_scale = px.colors.cyclical.IceFire  # alternatives: 'RdYlBu', 'Spectral', ...
    
    temp_min = df_clean['Temperature'].min()
    temp_max = df_clean['Temperature'].max()
    abs_max = max(abs(temp_min), abs(temp_max))
    color_range = [-abs_max, abs_max]
    
    fig = px.scatter_mapbox(
        df_clean,
        lat='Latitude',
        lon='Longitude',
        size=[fixed_marker_size] * len(df_clean),  # fixed size for all markers
        color='Temperature',
        hover_name='City',
        custom_data=['Temperature', 'Humidity', 'Wind Speed (km/h)', 'Pressure (mb)', 'Visibility (km)'],
        color_continuous_scale=color_scale,
        range_color=color_range,
        color_continuous_midpoint=0,
        opacity=0.9,
        size_max=12,
        mapbox_style="carto-positron",
        zoom=5,
        title='Temperature Distribution Across Cities in Armenia'
    )
    
    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>" +
            "Temperature: %{customdata[0]:.1f}℃<br>" +
            "Humidity: %{customdata[1]:.1f}%<br>" +
            "Wind Speed: %{customdata[2]:.1f} km/h<br>" +
            "Pressure: %{customdata[3]:.1f} mb<br>" +
            "Visibility: %{customdata[4]:.1f} km<br>" +
            "<extra></extra>"
        )
    )
    
    fig.update_layout(
        title_font_size=20,
        coloraxis_colorbar=dict(
            title="Temperature (℃)",
            tickprefix="",
            ticksuffix="℃",
            tickmode='linear',
            tick0=-abs_max,
            dtick=3,
            len=0.5,
            yanchor="middle",
            y=0.5
        )
    )
    
    interactive_map_path = os.path.join(output_dir, 'interactive_map.html')
    fig.write_html(interactive_map_path)

def run_daily_plotter():
    read_path = "outputs/processed/daily-weather-data-clean.csv"
    output_dir = "outputs/visualizations/daily"
    os.makedirs(output_dir, exist_ok=True)
    generate_plots(read_path, output_dir)