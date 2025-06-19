from flask import Flask, render_template, jsonify
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)

def get_bike_race_data():
    """Get data from bike race database"""
    db_path = '/home/sourav/bike-race-game/instance/bike_race.db'
    
    if not os.path.exists(db_path):
        return None
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get users
    cursor.execute("SELECT id, username, email, created_at FROM user ORDER BY created_at DESC")
    users = cursor.fetchall()
    
    # Get top scores
    cursor.execute("""
        SELECT s.score, s.distance, u.username, s.timestamp, s.ip_address 
        FROM score s 
        JOIN user u ON s.user_id = u.id 
        ORDER BY s.score DESC 
        LIMIT 15
    """)
    scores = cursor.fetchall()
    
    # Get login logs
    cursor.execute("""
        SELECT u.username, l.login_time, l.ip_address 
        FROM login_log l 
        JOIN user u ON l.user_id = u.id 
        ORDER BY l.login_time DESC 
        LIMIT 10
    """)
    logins = cursor.fetchall()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM score")
    race_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT MAX(score), MAX(distance), AVG(score), AVG(distance) FROM score")
    stats = cursor.fetchone()
    
    conn.close()
    
    return {
        'users': users,
        'scores': scores,
        'logins': logins,
        'stats': {
            'user_count': user_count,
            'race_count': race_count,
            'max_score': stats[0] if stats[0] else 0,
            'max_distance': stats[1] if stats[1] else 0,
            'avg_score': round(stats[2], 1) if stats[2] else 0,
            'avg_distance': round(stats[3], 1) if stats[3] else 0
        }
    }

def get_snake_game_data():
    """Get data from snake game database"""
    db_path = '/home/sourav/snake-game/instance/snake_game.db'
    
    if not os.path.exists(db_path):
        return None
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get users
    cursor.execute("SELECT id, username, email, created_at FROM user ORDER BY created_at DESC")
    users = cursor.fetchall()
    
    # Get top scores
    cursor.execute("""
        SELECT s.score, u.username, s.timestamp, s.ip_address 
        FROM score s 
        JOIN user u ON s.user_id = u.id 
        ORDER BY s.score DESC 
        LIMIT 15
    """)
    scores = cursor.fetchall()
    
    # Get login logs
    cursor.execute("""
        SELECT u.username, l.login_time, l.ip_address 
        FROM login_log l 
        JOIN user u ON l.user_id = u.id 
        ORDER BY l.login_time DESC 
        LIMIT 10
    """)
    logins = cursor.fetchall()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM score")
    game_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT MAX(score), AVG(score) FROM score")
    stats = cursor.fetchone()
    
    # Get success rate (games with score > 0)
    cursor.execute("SELECT COUNT(*) FROM score WHERE score > 0")
    successful_games = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'users': users,
        'scores': scores,
        'logins': logins,
        'stats': {
            'user_count': user_count,
            'game_count': game_count,
            'max_score': stats[0] if stats[0] else 0,
            'avg_score': round(stats[1], 1) if stats[1] else 0,
            'successful_games': successful_games,
            'success_rate': round((successful_games / game_count * 100), 1) if game_count > 0 else 0
        }
    }

def get_temperature_data():
    """Get temperature dashboard data"""
    # Sample temperature data (same as in temperature dashboard)
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
    
    temps = [city_data['temp'] for city_data in INDIA_CITIES.values()]
    
    return {
        'cities': INDIA_CITIES,
        'stats': {
            'total_cities': len(INDIA_CITIES),
            'avg_temp': round(sum(temps) / len(temps), 1),
            'max_temp': max(temps),
            'min_temp': min(temps),
            'hottest_city': max(INDIA_CITIES.keys(), key=lambda x: INDIA_CITIES[x]['temp']),
            'coolest_city': min(INDIA_CITIES.keys(), key=lambda x: INDIA_CITIES[x]['temp']),
            'cities_above_35': len([t for t in temps if t > 35]),
            'cities_below_30': len([t for t in temps if t < 30])
        }
    }

@app.route('/')
def dashboard():
    """Main database dashboard"""
    return render_template('database_dashboard.html')

@app.route('/api/database-data')
def get_database_data():
    """API endpoint to get all database data"""
    try:
        bike_data = get_bike_race_data()
        snake_data = get_snake_game_data()
        temp_data = get_temperature_data()
        
        return jsonify({
            'success': True,
            'bike_race': bike_data,
            'snake_game': snake_data,
            'temperature': temp_data,
            'timestamp': datetime.now().isoformat(),
            'server_info': {
                'bike_race_db': '/home/sourav/bike-race-game/instance/bike_race.db',
                'snake_game_db': '/home/sourav/snake-game/instance/snake_game.db',
                'temperature_source': 'In-memory data'
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bike-race')
def get_bike_race_api():
    """API endpoint for bike race data only"""
    try:
        data = get_bike_race_data()
        return jsonify({
            'success': True,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/snake-game')
def get_snake_game_api():
    """API endpoint for snake game data only"""
    try:
        data = get_snake_game_data()
        return jsonify({
            'success': True,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/temperature')
def get_temperature_api():
    """API endpoint for temperature data only"""
    try:
        data = get_temperature_data()
        return jsonify({
            'success': True,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
