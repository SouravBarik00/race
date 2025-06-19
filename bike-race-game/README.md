# 🏍️ Bike Race Game

An exciting web-based bike racing game with user authentication and competitive leaderboard.

## Game Features

- **Top-down Racing**: Control your bike from a bird's eye view
- **Dynamic Obstacles**: Avoid cars and rocks on the road
- **Coin Collection**: Collect coins for bonus points
- **Speed Control**: Accelerate, brake, and steer your bike
- **Progressive Difficulty**: Game gets faster as you progress
- **Real-time Stats**: Track score, distance, and speed

## System Features

- **User Authentication**: Secure registration and login
- **Database Storage**: User data, scores, and login logs with IP tracking
- **Leaderboard**: Top 10 racers with scores and distances
- **Personal Stats**: Track your best performance
- **Responsive Design**: Works on desktop and mobile

## Game Controls

- **Left/Right Arrow Keys**: Steer the bike
- **Up Arrow**: Accelerate
- **Down Arrow**: Brake
- **Space**: Start/Restart game

## Scoring System

- **Distance Points**: 1 point per meter traveled
- **Speed Bonus**: Extra points for higher speeds
- **Coin Collection**: 50 points per coin
- **Survival Bonus**: Longer races = higher scores

## Installation

1. Create virtual environment:
```bash
python3 -m venv race_env
source race_env/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python app.py
```

4. Access at: http://localhost:5001

## Database Schema

### Users Table
- id, username, email, password_hash, created_at

### Scores Table
- id, user_id, score, distance, timestamp, ip_address

### Login Logs Table
- id, user_id, login_time, ip_address

## Game Mechanics

- **Collision Detection**: Precise collision with obstacles
- **Physics**: Realistic acceleration and friction
- **Procedural Generation**: Random obstacle and coin placement
- **Progressive Speed**: Game speed increases with player speed
- **Visual Effects**: Gradient backgrounds and detailed sprites

## Customization Options

- Adjust game speed and difficulty
- Add new obstacle types
- Implement power-ups
- Add different bike models
- Create multiple race tracks
- Add multiplayer functionality
