#!/bin/bash
echo "🌡️ Starting India Temperature Dashboard..."
echo "========================================"

cd /home/sourav/web-games-collection-clean/temperature-analysis

# Create virtual environment if it doesn't exist
if [ ! -d "temp_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv temp_env
fi

# Activate virtual environment
source temp_env/bin/activate

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "🌡️ Temperature Dashboard will be available at:"
echo "Local: http://127.0.0.1:5002"
echo "Network: http://172.20.38.126:5002"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"

# Start the Flask application
python app.py
