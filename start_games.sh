#!/bin/bash
echo "🎮 Starting Web Games Collection Servers"
echo "========================================"

# Get the current directory
CURRENT_DIR=$(pwd)

# Start Bike Race Game
echo "🏍️ Starting Bike Race Game on port 5001..."
cd $CURRENT_DIR/bike-race-game
if [ ! -d "race_env" ]; then
    python3 -m venv race_env
    source race_env/bin/activate
    pip install -r requirements.txt
else
    source race_env/bin/activate
fi
nohup python app.py > race_server.log 2>&1 &
BIKE_PID=$!

sleep 2

# Start Snake Game  
echo "🐍 Starting Snake Game on port 5000..."
cd $CURRENT_DIR/snake-game
if [ ! -d "game_env" ]; then
    python3 -m venv game_env
    source game_env/bin/activate
    pip install -r requirements.txt
else
    source game_env/bin/activate
fi
nohup python app.py > snake_server.log 2>&1 &
SNAKE_PID=$!

sleep 2

# Start Temperature Dashboard
echo "🌡️ Starting Temperature Dashboard on port 5002..."
cd $CURRENT_DIR/temperature-analysis
if [ ! -d "temp_env" ]; then
    python3 -m venv temp_env
    source temp_env/bin/activate
    pip install -r requirements.txt
else
    source temp_env/bin/activate
fi
nohup python app.py > temp_server.log 2>&1 &
TEMP_PID=$!

sleep 2

# Start Database Viewer
echo "📊 Starting Database Viewer on port 5003..."
cd $CURRENT_DIR/database-viewer
if [ ! -d "db_env" ]; then
    python3 -m venv db_env
    source db_env/bin/activate
    pip install -r requirements.txt
else
    source db_env/bin/activate
fi
nohup python app.py > db_viewer.log 2>&1 &
DB_PID=$!

sleep 3

echo ""
echo "✅ All servers started successfully!"
echo "========================================"
echo "🏍️ Bike Race Game: http://127.0.0.1:5001"
echo "🐍 Snake Game: http://127.0.0.1:5000"
echo "🌡️ Temperature Dashboard: http://127.0.0.1:5002"
echo "📊 Database Viewer: http://127.0.0.1:5003"
echo ""
echo "🌐 Network Access (replace with your IP):"
echo "🏍️ Bike Race: http://172.20.38.126:5001"
echo "🐍 Snake Game: http://172.20.38.126:5000"
echo "🌡️ Temperature: http://172.20.38.126:5002"
echo "📊 Database Viewer: http://172.20.38.126:5003"
echo ""
echo "🔗 Database API Endpoints:"
echo "All Data: http://127.0.0.1:5003/api/database-data"
echo "Bike Race: http://127.0.0.1:5003/api/bike-race"
echo "Snake Game: http://127.0.0.1:5003/api/snake-game"
echo "Temperature: http://127.0.0.1:5003/api/temperature"
echo ""
echo "📊 Database Management:"
echo "cd bike-race-game && python3 view_database.py"
echo "cd snake-game && python3 view_database.py"
echo ""
echo "🛑 To stop all servers: pkill -f 'python app.py'"
echo "========================================"

# Check if servers are running
sleep 2
echo "Server Status:"
ss -tlnp | grep -E ":(5000|5001|5002|5003)" || echo "⚠️ Servers may still be starting..."
