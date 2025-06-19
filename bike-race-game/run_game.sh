#!/bin/bash
echo "🏍️ Starting Bike Race Game Server..."
echo "===================================="

cd /home/sourav/bike-race-game
source race_env/bin/activate

echo "Game will be available at: http://localhost:5001"
echo "Or from other devices at: http://172.20.38.126:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo "===================================="

python app.py
