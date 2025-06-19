# 📊 Database Documentation - Web Games Collection

## Overview

The Web Games Collection uses SQLite databases to store user data, game scores, and security logs. Each game has its own dedicated database with similar schemas but game-specific optimizations.

---

## 🏍️ Bike Race Game Database

**Database Location**: `/home/sourav/bike-race-game/instance/bike_race.db`

### Database Schema

#### 1. **Users Table** (`user`)
```sql
CREATE TABLE user (
    id INTEGER NOT NULL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(120) NOT NULL,
    created_at DATETIME
);
```

**Purpose**: Stores user account information with secure password hashing.

**Current Data**:
- **Total Users**: 1
- **User ID 1**: sourav (xyz@email.com) - Joined: 2025-06-19 17:11:46

#### 2. **Scores Table** (`score`)
```sql
CREATE TABLE score (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    distance INTEGER NOT NULL,
    timestamp DATETIME,
    ip_address VARCHAR(45) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user (id)
);
```

**Purpose**: Records every race attempt with score, distance traveled, and security tracking.

**Current Data**:
- **Total Races**: 3
- **Highest Score**: 4,716 points (3,966m distance)
- **Average Score**: 1,953.0 points
- **Average Distance**: 1,703.3 meters

**Top Scores**:
| Score | Distance | Player | Date | IP |
|-------|----------|--------|------|-----|
| 4,716 | 3,966m | sourav | 2025-06-19 17:12 | 127.0.0.1 |
| 609 | 610m | sourav | 2025-06-19 17:12 | 127.0.0.1 |
| 534 | 534m | sourav | 2025-06-19 17:12 | 127.0.0.1 |

#### 3. **Login Logs Table** (`login_log`)
```sql
CREATE TABLE login_log (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    login_time DATETIME,
    ip_address VARCHAR(45) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user (id)
);
```

**Purpose**: Security tracking for user authentication attempts.

**Current Data**:
- **Recent Login**: sourav - 2025-06-19 17:11:55 from 127.0.0.1

---

## 🐍 Snake Game Database

**Database Location**: `/home/sourav/snake-game/instance/snake_game.db`

### Database Schema

#### 1. **Users Table** (`user`)
```sql
CREATE TABLE user (
    id INTEGER NOT NULL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(120) NOT NULL,
    created_at DATETIME
);
```

**Current Data**:
- **Total Users**: 1
- **User ID 1**: sourav (xyz@email.com) - Joined: 2025-06-19 15:52:20

#### 2. **Scores Table** (`score`)
```sql
CREATE TABLE score (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    timestamp DATETIME,
    ip_address VARCHAR(45) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user (id)
);
```

**Note**: Snake game doesn't track distance, only score points.

**Current Data**:
- **Total Games Played**: 44
- **Highest Score**: 90 points
- **Average Score**: 4.1 points
- **Success Rate**: ~18% (games with score > 0)

**Recent High Scores**:
| Score | Date | IP |
|-------|------|-----|
| 90 | 2025-06-19 17:45 | 127.0.0.1 |
| 40 | 2025-06-19 17:45 | 127.0.0.1 |
| 20 | 2025-06-19 15:53 | 172.20.32.1 |
| 10 | 2025-06-19 16:04 | 127.0.0.1 |

#### 3. **Login Logs Table** (`login_log`)
```sql
CREATE TABLE login_log (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    login_time DATETIME,
    ip_address VARCHAR(45) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user (id)
);
```

**Current Data**:
- **Total Login Sessions**: 5
- **Most Recent**: 2025-06-19 17:44:47 from 127.0.0.1
- **Network Access**: Multiple IPs (127.0.0.1, 172.20.32.1)

---

## 🌡️ Temperature Dashboard

**Data Storage**: In-memory (no persistent database)
**Data Source**: Static city temperature data in Python dictionary

```python
INDIA_CITIES = {
    'Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'temp': 32.5},
    'Delhi': {'lat': 28.7041, 'lon': 77.1025, 'temp': 35.2},
    # ... 25+ cities total
}
```

**Current Data**:
- **Cities Monitored**: 25
- **Temperature Range**: 26.9°C - 37.2°C
- **Average Temperature**: 32.4°C
- **Hottest City**: Jaipur (37.2°C)
- **Coolest City**: Mysore (26.9°C)

---

## 🔧 Database Management Tools

### View Database Contents

**Bike Race Game**:
```bash
cd bike-race-game
python3 view_database.py
```

**Snake Game**:
```bash
cd snake-game
python3 view_database.py
```

### Direct Database Access

**Using SQLite CLI**:
```bash
# Bike Race Database
sqlite3 bike-race-game/instance/bike_race.db

# Snake Game Database
sqlite3 snake-game/instance/snake_game.db
```

### Common SQL Queries

**Get Top Players**:
```sql
SELECT u.username, MAX(s.score) as best_score, COUNT(s.id) as games_played
FROM user u 
LEFT JOIN score s ON u.id = s.user_id 
GROUP BY u.id 
ORDER BY best_score DESC;
```

**Get Player Statistics**:
```sql
SELECT 
    u.username,
    COUNT(s.id) as total_games,
    MAX(s.score) as best_score,
    AVG(s.score) as avg_score,
    MAX(s.distance) as longest_distance  -- Bike Race only
FROM user u 
LEFT JOIN score s ON u.id = s.user_id 
WHERE u.username = 'sourav'
GROUP BY u.id;
```

**Security Analysis**:
```sql
SELECT 
    ip_address,
    COUNT(*) as login_attempts,
    MIN(login_time) as first_login,
    MAX(login_time) as last_login
FROM login_log 
GROUP BY ip_address 
ORDER BY login_attempts DESC;
```

---

## 📊 Data Analytics Insights

### Bike Race Game Analytics

**Performance Metrics**:
- **Score Efficiency**: 1.18 points per meter (4716 points / 3966m)
- **Consistency**: High variance in scores (534 to 4716)
- **Distance Achievement**: Maximum 3.97km in single race

**Player Behavior**:
- **Session Length**: 3 races in ~5 minutes
- **Improvement Rate**: 785% score increase (534 → 4716)
- **Access Pattern**: Local gameplay (127.0.0.1)

### Snake Game Analytics

**Gameplay Patterns**:
- **Attempt Rate**: 44 games played
- **Success Rate**: ~18% (8 games with score > 0)
- **Learning Curve**: Gradual improvement (max score: 90)
- **Session Behavior**: Multiple quick attempts

**Network Usage**:
- **Multi-device Access**: 2 different IP addresses
- **Peak Performance**: Best scores from local access (127.0.0.1)

---

## 🔒 Security Features

### Password Security
- **Hashing Algorithm**: PBKDF2 with SHA-256
- **Salt Rounds**: 600,000 iterations
- **Example Hash**: `pbkdf2:sha256:600000$7j5BEl2kE8cCCv94$a7edca...`

### Access Tracking
- **IP Address Logging**: Every login and game attempt
- **Timestamp Precision**: Microsecond accuracy
- **Session Monitoring**: Login time tracking

### Data Integrity
- **Foreign Key Constraints**: Referential integrity between users and scores
- **Unique Constraints**: Username and email uniqueness
- **Data Types**: Appropriate field types for data validation

---

## 🚀 Database Backup & Maintenance

### Backup Commands
```bash
# Backup Bike Race Database
cp bike-race-game/instance/bike_race.db bike_race_backup_$(date +%Y%m%d).db

# Backup Snake Game Database
cp snake-game/instance/snake_game.db snake_game_backup_$(date +%Y%m%d).db
```

### Database Optimization
```sql
-- Analyze database performance
ANALYZE;

-- Rebuild database (removes deleted space)
VACUUM;

-- Check database integrity
PRAGMA integrity_check;
```

### Monitoring Queries
```sql
-- Database size
SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size();

-- Table row counts
SELECT name, (SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=m.name) as row_count 
FROM sqlite_master m WHERE type='table';
```

---

## 📈 Future Database Enhancements

### Planned Features
1. **User Profiles**: Extended user information (avatar, preferences)
2. **Game Statistics**: Detailed analytics per user
3. **Achievements**: Badge and milestone tracking
4. **Social Features**: Friend connections and comparisons
5. **Tournament System**: Organized competitions with brackets

### Scalability Considerations
1. **Database Migration**: SQLite → PostgreSQL for production
2. **Indexing**: Performance optimization for large datasets
3. **Partitioning**: Time-based data separation
4. **Caching**: Redis integration for frequently accessed data
5. **Backup Strategy**: Automated daily backups with retention policy

---

**Database files are automatically created when games are first played and users register.**
