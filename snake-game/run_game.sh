#!/bin/bash
echo "🐍 Starting Snake Game Server..."
echo "================================"

cd /home/sourav/snake-game
source game_env/bin/activate

echo "Game will be available at: http://localhost:5000"
echo "Or from other devices at: http://192.168.1.9:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

python app.py
