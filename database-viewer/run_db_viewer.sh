#!/bin/bash
echo "📊 Starting Database Viewer Dashboard..."
echo "========================================"

cd /home/sourav/web-games-collection-clean/database-viewer

# Create virtual environment if it doesn't exist
if [ ! -d "db_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv db_env
fi

# Activate virtual environment
source db_env/bin/activate

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "📊 Database Viewer will be available at:"
echo "Local: http://127.0.0.1:5003"
echo "Network: http://172.20.38.126:5003"
echo ""
echo "🔗 API Endpoints:"
echo "All Data: http://127.0.0.1:5003/api/database-data"
echo "Bike Race: http://127.0.0.1:5003/api/bike-race"
echo "Snake Game: http://127.0.0.1:5003/api/snake-game"
echo "Temperature: http://127.0.0.1:5003/api/temperature"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"

# Start the Flask application
python app.py
