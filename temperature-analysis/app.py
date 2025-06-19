from flask import Flask, render_template, jsonify
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime
import os

app = Flask(__name__)

# Sample temperature data for India (you can replace with real API data)
INDIA_CITIES = {
    'Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'temp': 32.5},
    'Delhi': {'lat': 28.7041, 'lon': 77.1025, 'temp': 35.2},
    'Bangalore': {'lat': 12.9716, 'lon': 77.5946, 'temp': 28.8},
    'Chennai': {'lat': 13.0827, 'lon': 80.2707, 'temp': 31.4},
    'Kolkata': {'lat': 22.5726, 'lon': 88.3639, 'temp': 33.1},
    'Hyderabad': {'lat': 17.3850, 'lon': 78.4867, 'temp': 30.7},
    'Pune': {'lat': 18.5204, 'lon': 73.8567, 'temp': 29.3},
    'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714, 'temp': 36.8},
    'Jaipur': {'lat': 26.9124, 'lon': 75.7873, 'temp': 37.2},
    'Lucknow': {'lat': 26.8467, 'lon': 80.9462, 'temp': 34.6},
    'Kanpur': {'lat': 26.4499, 'lon': 80.3319, 'temp': 35.1},
    'Nagpur': {'lat': 21.1458, 'lon': 79.0882, 'temp': 32.9},
    'Indore': {'lat': 22.7196, 'lon': 75.8577, 'temp': 31.8},
    'Bhopal': {'lat': 23.2599, 'lon': 77.4126, 'temp': 33.4},
    'Visakhapatnam': {'lat': 17.6868, 'lon': 83.2185, 'temp': 29.9},
    'Patna': {'lat': 25.5941, 'lon': 85.1376, 'temp': 36.3},
    'Vadodara': {'lat': 22.3072, 'lon': 73.1812, 'temp': 35.7},
    'Ghaziabad': {'lat': 28.6692, 'lon': 77.4538, 'temp': 34.8},
    'Ludhiana': {'lat': 30.9010, 'lon': 75.8573, 'temp': 33.2},
    'Coimbatore': {'lat': 11.0168, 'lon': 76.9558, 'temp': 27.6},
    'Kochi': {'lat': 9.9312, 'lon': 76.2673, 'temp': 30.1},
    'Thiruvananthapuram': {'lat': 8.5241, 'lon': 76.9366, 'temp': 29.4},
    'Chandigarh': {'lat': 30.7333, 'lon': 76.7794, 'temp': 32.8},
    'Mysore': {'lat': 12.2958, 'lon': 76.6394, 'temp': 26.9},
    'Dehradun': {'lat': 30.3165, 'lon': 78.0322, 'temp': 31.5}
}

def generate_temperature_map():
    """Generate temperature map visualization"""
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Extract data
    cities = list(INDIA_CITIES.keys())
    lats = [INDIA_CITIES[city]['lat'] for city in cities]
    lons = [INDIA_CITIES[city]['lon'] for city in cities]
    temps = [INDIA_CITIES[city]['temp'] for city in cities]
    
    # Create scatter plot with temperature-based colors
    scatter = ax.scatter(lons, lats, c=temps, s=100, cmap='RdYlBu_r', 
                        alpha=0.7, edgecolors='black', linewidth=1)
    
    # Add city labels
    for i, city in enumerate(cities):
        ax.annotate(f'{city}\n{temps[i]}°C', 
                   (lons[i], lats[i]), 
                   xytext=(5, 5), 
                   textcoords='offset points',
                   fontsize=8,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    # Customize the plot
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.set_title('India Temperature Map - Live Data\n' + 
                f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
                fontsize=14, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Temperature (°C)', fontsize=12)
    
    # Set map boundaries for India
    ax.set_xlim(68, 97)
    ax.set_ylim(6, 37)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Tight layout
    plt.tight_layout()
    
    # Convert plot to base64 string
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_base64

def generate_temperature_stats():
    """Generate temperature statistics"""
    temps = [city_data['temp'] for city_data in INDIA_CITIES.values()]
    
    stats = {
        'total_cities': len(INDIA_CITIES),
        'avg_temp': round(np.mean(temps), 1),
        'max_temp': max(temps),
        'min_temp': min(temps),
        'hottest_city': max(INDIA_CITIES.keys(), key=lambda x: INDIA_CITIES[x]['temp']),
        'coolest_city': min(INDIA_CITIES.keys(), key=lambda x: INDIA_CITIES[x]['temp']),
        'temp_range': round(max(temps) - min(temps), 1),
        'cities_above_35': len([t for t in temps if t > 35]),
        'cities_below_30': len([t for t in temps if t < 30])
    }
    
    return stats

@app.route('/')
def index():
    """Main temperature dashboard"""
    return render_template('temperature_dashboard.html')

@app.route('/api/temperature-map')
def get_temperature_map():
    """API endpoint to get temperature map"""
    try:
        map_image = generate_temperature_map()
        stats = generate_temperature_stats()
        
        return jsonify({
            'success': True,
            'map_image': map_image,
            'stats': stats,
            'cities': INDIA_CITIES,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/city-data')
def get_city_data():
    """API endpoint to get city temperature data"""
    return jsonify({
        'success': True,
        'cities': INDIA_CITIES,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats')
def get_stats():
    """API endpoint to get temperature statistics"""
    stats = generate_temperature_stats()
    return jsonify({
        'success': True,
        'stats': stats,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
