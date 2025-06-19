# 🎮 Web Games Collection

A comprehensive collection of web-based games with user authentication, database storage, and competitive leaderboards.

## 🏆 Games Included

### 🏍️ Bike Race Game
- **Port**: 5001
- **Features**: Top-down racing, obstacle avoidance, coin collection, speed control
- **Scoring**: Distance + speed bonuses + coin collection
- **Controls**: Arrow keys for steering, acceleration, and braking

### 🐍 Snake Game  
- **Port**: 5000
- **Features**: Classic snake gameplay with modern web interface
- **Scoring**: Food collection and survival time
- **Controls**: Arrow keys for movement

### 🌡️ Temperature Dashboard
- **Port**: 5002
- **Features**: Interactive temperature map of India, real-time data visualization
- **Data**: Live temperature readings from 25+ major Indian cities
- **Visualization**: Color-coded temperature map with city details

## 🚀 Quick Start

### Start All Games
```bash
./start_games.sh
```

### Individual Game Startup

**Bike Race Game:**
```bash
cd bike-race-game
python3 -m venv race_env
source race_env/bin/activate
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Werkzeug==2.3.7
python app.py
```

**Snake Game:**
```bash
cd snake-game
python3 -m venv game_env
source game_env/bin/activate
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Werkzeug==2.3.7
python app.py
```

**Temperature Dashboard:**
```bash
cd temperature-analysis
python3 -m venv temp_env
source temp_env/bin/activate
pip install Flask==2.3.3 matplotlib pandas numpy
python app.py
```

## 🌐 Access URLs

- **Bike Race Game**: http://localhost:5001
- **Snake Game**: http://localhost:5000
- **Temperature Dashboard**: http://localhost:5002

## 🔧 System Features

### User Authentication
- Secure user registration and login
- Password hashing with Werkzeug
- Session management
- IP address tracking for security

### Database Storage
- SQLite databases for each game
- User credentials and profiles
- Game scores and statistics
- Login logs with timestamps and IP addresses

### Leaderboards
- Top 10 players for each game
- Personal best scores
- Distance tracking (Bike Race)
- Real-time score updates

## 📊 Database Management

### View Game Statistics
```bash
# Bike Race Game stats
cd bike-race-game && python3 view_database.py

# Snake Game stats
cd snake-game && python3 view_database.py
```

## 🎯 Game Controls

### Bike Race Game
- **Left/Right Arrow**: Steer bike
- **Up Arrow**: Accelerate
- **Down Arrow**: Brake
- **Space**: Start/Restart

### Snake Game
- **Arrow Keys**: Move snake (auto-starts game)
- **Space**: Restart game

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5 Canvas, CSS3, JavaScript
- **Authentication**: Werkzeug password hashing
- **Deployment**: Flask development server

## 📁 Project Structure

```
web-games-collection/
├── bike-race-game/          # 🏍️ Bike racing game
├── snake-game/             # 🐍 Snake game
├── temperature-analysis/    # 🌡️ Interactive temperature dashboard
└── start_games.sh          # Quick start script
```

## 🚀 Deployment & Usage

1. Clone the repository
2. Run individual setup commands for each game
3. Use `./start_games.sh` to start all games
4. Access games via provided URLs
5. Register/login to play and compete

## 🎮 Game Features

### Bike Race Game
- **Graphics**: Gradient backgrounds, detailed sprites
- **Physics**: Realistic acceleration and friction
- **Obstacles**: Cars and rocks with collision detection
- **Collectibles**: Golden coins for bonus points
- **Progressive Difficulty**: Speed increases over time

### Snake Game
- **Classic Gameplay**: Traditional snake mechanics
- **Modern Interface**: Clean, responsive design
- **Smooth Controls**: Fixed arrow key responsiveness
- **Score System**: Points for food collection

## 🔒 Security Features

- Password hashing and salting
- Session-based authentication
- IP address logging
- SQL injection protection via ORM
- Input validation and sanitization

---

**Happy Gaming! 🎮**

**Repository**: https://github.com/SouravBarik00/race
