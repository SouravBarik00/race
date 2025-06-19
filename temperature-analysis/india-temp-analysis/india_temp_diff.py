#!/usr/bin/env python3
"""
India Temperature Difference Graph for June 2025
This script generates a visualization of temperature differences across India for June 2025.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random

# Set the style for our plots
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Create a date range for June 2025
start_date = datetime(2025, 6, 1)
end_date = datetime(2025, 6, 30)
date_range = pd.date_range(start=start_date, end=end_date)

# Major cities in India with their approximate coordinates
cities = {
    'New Delhi': {'lat': 28.6139, 'lon': 77.2090, 'base_temp': 38},
    'Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'base_temp': 32},
    'Chennai': {'lat': 13.0827, 'lon': 80.2707, 'base_temp': 36},
    'Kolkata': {'lat': 22.5726, 'lon': 88.3639, 'base_temp': 34},
    'Bangalore': {'lat': 12.9716, 'lon': 77.5946, 'base_temp': 29},
    'Hyderabad': {'lat': 17.3850, 'lon': 78.4867, 'base_temp': 35},
    'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714, 'base_temp': 37},
    'Pune': {'lat': 18.5204, 'lon': 73.8567, 'base_temp': 31},
    'Jaipur': {'lat': 26.9124, 'lon': 75.7873, 'base_temp': 39},
    'Srinagar': {'lat': 34.0837, 'lon': 74.7973, 'base_temp': 25},
    'Bhubaneswar': {'lat': 20.2961, 'lon': 85.8245, 'base_temp': 35},
}

# Generate temperature data for each city
data = []

# Simulate temperature patterns with some randomness
for city, info in cities.items():
    base_temp = info['base_temp']
    
    # Add some randomness to create variations
    for date in date_range:
        # Day of month effect (temperatures tend to increase through June)
        day_effect = (date.day - 1) * 0.2
        
        # Random daily fluctuation
        daily_random = random.uniform(-2, 2)
        
        # Calculate actual temperature
        actual_temp = base_temp + day_effect + daily_random
        
        # Calculate temperature difference from the city's average June temperature
        temp_diff = actual_temp - base_temp
        
        data.append({
            'City': city,
            'Date': date,
            'Temperature': round(actual_temp, 1),
            'Temp_Difference': round(temp_diff, 1)
        })

# Create DataFrame
df = pd.DataFrame(data)

# Calculate average temperature difference for each city across the month
avg_diff_by_city = df.groupby('City')['Temp_Difference'].mean().reset_index()
avg_diff_by_city['Temp_Difference'] = avg_diff_by_city['Temp_Difference'].round(1)

# Sort by temperature difference
avg_diff_by_city = avg_diff_by_city.sort_values('Temp_Difference', ascending=False)

# Create the plot
plt.figure(figsize=(14, 10))

# Create a bar plot for average temperature differences
ax = sns.barplot(
    x='City', 
    y='Temp_Difference', 
    data=avg_diff_by_city,
    palette='coolwarm'
)

# Add a horizontal line at y=0
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)

# Customize the plot
plt.title('Projected Temperature Differences from Average in Indian Cities - June 2025', fontsize=16)
plt.xlabel('City', fontsize=14)
plt.ylabel('Temperature Difference (°C)', fontsize=14)
plt.xticks(rotation=45, ha='right')

# Add value labels on top of bars
for i, v in enumerate(avg_diff_by_city['Temp_Difference']):
    ax.text(i, v + (0.1 if v >= 0 else -0.3), str(v), ha='center', fontsize=10)

# Add a note about the data
plt.figtext(0.5, 0.01, 
            'Note: Temperature differences are calculated from each city\'s historical June average.\n'
            'Data is simulated for June 2025 based on historical patterns with projected climate trends.',
            ha='center', fontsize=10, style='italic')

plt.tight_layout(rect=[0, 0.03, 1, 0.97])

# Save the figure
plt.savefig('india_temperature_diff_june_2025.png', dpi=300, bbox_inches='tight')

# Create a heatmap showing daily temperature differences
plt.figure(figsize=(16, 10))

# Pivot the data for the heatmap
heatmap_data = df.pivot_table(
    index='City', 
    columns=df['Date'].dt.day, 
    values='Temp_Difference'
)

# Create the heatmap
sns.heatmap(
    heatmap_data, 
    cmap='coolwarm', 
    center=0,
    annot=False, 
    fmt=".1f",
    linewidths=.5
)

plt.title('Daily Temperature Differences from Average in Indian Cities - June 2025', fontsize=16)
plt.xlabel('Day of June 2025', fontsize=14)
plt.ylabel('City', fontsize=14)
plt.tight_layout()

# Save the heatmap
plt.savefig('india_temperature_diff_heatmap_june_2025.png', dpi=300, bbox_inches='tight')

print("Analysis complete! Graphs have been saved.")
