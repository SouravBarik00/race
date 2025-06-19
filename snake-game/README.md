# 🐍 Snake Game with User Authentication

A web-based Snake game with user registration, login system, and competitive leaderboard.

## Features

- **User Authentication**: Register and login system
- **Database Storage**: User credentials, scores, and login logs with timestamps and IP addresses
- **Leaderboard**: Shows top 10 highest scores and current user's best score
- **Real-time Gameplay**: Classic Snake game with smooth controls
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (easily changeable to MySQL/PostgreSQL)
- **Frontend**: HTML5 Canvas, CSS3, JavaScript
- **Authentication**: Werkzeug password hashing

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and go to: `http://localhost:5000`

## Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- created_at (Timestamp)

### Scores Table
- id (Primary Key)
- user_id (Foreign Key)
- score
- timestamp
- ip_address

### Login Logs Table
- id (Primary Key)
- user_id (Foreign Key)
- login_time
- ip_address

## Game Controls

- **Arrow Keys**: Move the snake
- **Space**: Start/Restart game
- **Leaderboard Button**: View top scores

## Security Features

- Password hashing using Werkzeug
- Session management
- IP address logging
- SQL injection protection via SQLAlchemy ORM

## Customization

You can easily modify the game by:
- Changing game speed in `setTimeout(gameLoop, 150)`
- Adjusting canvas size and grid size
- Modifying scoring system
- Adding power-ups or obstacles
- Implementing different game modes

## Deployment

For production deployment:
1. Change the secret key in `app.py`
2. Use a production database (PostgreSQL/MySQL)
3. Set up proper environment variables
4. Use a WSGI server like Gunicorn
5. Configure reverse proxy with Nginx

## Alternative Game Ideas

The same framework can be used for other games:
- Tetris
- 2048
- Flappy Bird
- Memory Card Game
- Math Quiz Game
- Reaction Time Game
