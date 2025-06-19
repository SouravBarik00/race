#!/bin/bash
echo "🎮 Starting Game Servers from /home/sourav"
echo "=========================================="

# Start Bike Race Game
echo "🏍️ Starting Bike Race Game on port 5001..."
cd /home/sourav/bike-race-game
source race_env/bin/activate
nohup python app.py > race_server.log 2>&1 &
BIKE_PID=$!

sleep 2

# Start Snake Game  
echo "🐍 Starting Snake Game on port 5000..."
cd /home/sourav/snake-game
source game_env/bin/activate
nohup python app.py > snake_server.log 2>&1 &
SNAKE_PID=$!

sleep 3

echo ""
echo "✅ Game servers started!"
echo "🏍️ Bike Race Game: http://127.0.0.1:5001 or http://172.20.38.126:5001"
echo "🐍 Snake Game: http://127.0.0.1:5000 or http://172.20.38.126:5000"
echo ""
echo "📊 To view databases:"
echo "cd /home/sourav/bike-race-game && python3 view_database.py"
echo "cd /home/sourav/snake-game && python3 view_database.py"
echo ""
echo "🛑 To stop servers: pkill -f 'python app.py'"
echo ""

# Check if servers are running
sleep 2
echo "Server Status:"
ss -tlnp | grep -E ":(5000|5001)" || echo "⚠️ Servers may still be starting..."
