# 📊 Database Viewer Guide

## 🌐 **One-Click Database Access**

**URL**: http://localhost:5003 or http://your-ip:5003

The Database Viewer provides a comprehensive, real-time view of all database information across your Web Games Collection in a single, easy-to-use web interface.

---

## 🚀 **Quick Access**

### **Start Database Viewer Only**
```bash
cd database-viewer
./run_db_viewer.sh
```

### **Start All Applications (Including Database Viewer)**
```bash
./start_games.sh
```

---

## 📊 **Dashboard Features**

### **🏍️ Bike Race Game Data**
- **User Statistics**: Total racers, registration dates, email addresses
- **Performance Metrics**: Scores, distances, race completion times
- **Leaderboards**: Top 15 scores with player details
- **Security Logs**: Login times and IP address tracking

### **🐍 Snake Game Data**
- **Player Analytics**: User accounts and gameplay statistics
- **Score Tracking**: High scores, success rates, game attempts
- **Engagement Metrics**: Total games played, average scores
- **Access Monitoring**: Login patterns and session tracking

### **🌡️ Temperature Dashboard Data**
- **Geographic Coverage**: 25+ major Indian cities
- **Temperature Statistics**: Average, maximum, minimum readings
- **Regional Analysis**: Cities above/below temperature thresholds
- **City Details**: Coordinates and current temperature readings

---

## 🔗 **API Endpoints**

### **Complete Database Information**
```
GET /api/database-data
```
Returns all database information from all applications in JSON format.

### **Individual Application Data**
```
GET /api/bike-race      # Bike race game data only
GET /api/snake-game     # Snake game data only
GET /api/temperature    # Temperature dashboard data only
```

### **Example API Usage**
```bash
# Get all database data
curl http://localhost:5003/api/database-data

# Get only bike race data
curl http://localhost:5003/api/bike-race

# Get temperature data
curl http://localhost:5003/api/temperature
```

---

## 📈 **Real-time Analytics**

### **Live Statistics Displayed**
- **User Engagement**: Registration trends, login frequency
- **Game Performance**: Score distributions, improvement tracking
- **Security Monitoring**: IP access patterns, session management
- **System Health**: Database connectivity, data integrity

### **Auto-refresh Features**
- **30-second Updates**: Automatic data refresh for live monitoring
- **Manual Refresh**: On-demand data updates with refresh button
- **Real-time Counters**: Live user counts, game statistics

---

## 🎨 **User Interface Features**

### **Professional Dashboard**
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Styling**: Gradient backgrounds, smooth animations
- **Interactive Tables**: Sortable data with hover effects
- **Color-coded Data**: Temperature ranges, performance metrics

### **Navigation Controls**
- **Toggle Sections**: Show/hide specific application data
- **Export Functionality**: Download complete database as JSON
- **API Information**: Built-in API endpoint documentation

---

## 📊 **Current Database Statistics**

### **🏍️ Bike Race Game**
- **Total Racers**: 1 registered user
- **Total Races**: 3 completed games
- **Highest Score**: 4,716 points (3,966m distance)
- **Average Performance**: 1,953 points, 1,703m distance

### **🐍 Snake Game**
- **Total Players**: 1 registered user
- **Total Games**: 44 attempts
- **Highest Score**: 90 points
- **Success Rate**: ~18% (games with score > 0)

### **🌡️ Temperature Data**
- **Cities Monitored**: 25 major Indian cities
- **Temperature Range**: 26.9°C - 37.2°C
- **Average Temperature**: 32.4°C
- **Hottest City**: Jaipur (37.2°C)
- **Coolest City**: Mysore (26.9°C)

---

## 🔒 **Security & Privacy**

### **Data Protection**
- **Read-only Access**: Database viewer only displays data, no modifications
- **IP Tracking**: All access attempts logged for security
- **Session Management**: Secure data transmission
- **Error Handling**: Graceful handling of database connection issues

### **Access Control**
- **Network Security**: Configurable host access (localhost/network)
- **API Rate Limiting**: Built-in Flask security features
- **Data Validation**: Input sanitization and error checking

---

## 🛠️ **Technical Details**

### **Technology Stack**
- **Backend**: Flask 2.3.3 (Python web framework)
- **Database**: SQLite (direct database access)
- **Frontend**: HTML5, CSS3, JavaScript (responsive design)
- **API**: RESTful JSON endpoints

### **Database Connections**
- **Bike Race DB**: `/home/sourav/bike-race-game/instance/bike_race.db`
- **Snake Game DB**: `/home/sourav/snake-game/instance/snake_game.db`
- **Temperature Data**: In-memory Python dictionary

### **Performance Features**
- **Efficient Queries**: Optimized SQL for fast data retrieval
- **Caching**: Minimal database connections for better performance
- **Error Recovery**: Automatic retry on database connection issues

---

## 🚀 **Deployment Information**

### **Local Development**
```bash
cd database-viewer
python3 -m venv db_env
source db_env/bin/activate
pip install -r requirements.txt
python app.py
```

### **Production Deployment**
- **Port**: 5003 (configurable)
- **Host**: 0.0.0.0 (accessible from network)
- **Debug Mode**: Enabled for development
- **Auto-restart**: Built-in Flask reloader

### **Network Access**
- **Local**: http://127.0.0.1:5003
- **Network**: http://your-server-ip:5003
- **API Base**: http://your-server-ip:5003/api/

---

## 📱 **Mobile Compatibility**

### **Responsive Design**
- **Mobile-first**: Optimized for smartphone viewing
- **Touch-friendly**: Large buttons and touch targets
- **Adaptive Layout**: Adjusts to screen size automatically
- **Fast Loading**: Optimized for mobile networks

---

## 🔧 **Troubleshooting**

### **Common Issues**
1. **Database Not Found**: Ensure games have been played to create databases
2. **Connection Refused**: Check if port 5003 is available
3. **Empty Data**: Verify database files exist and have data
4. **API Errors**: Check Flask server logs for detailed error messages

### **Server Logs**
```bash
# View database viewer logs
tail -f database-viewer/db_viewer.log

# Check server status
ss -tlnp | grep 5003
```

---

## 🎯 **Use Cases**

### **For Developers**
- **API Integration**: Use REST endpoints for external applications
- **Data Analysis**: Export JSON data for further processing
- **Performance Monitoring**: Track user engagement and game metrics
- **Security Auditing**: Monitor access patterns and login attempts

### **For Administrators**
- **User Management**: View registered users and activity
- **System Health**: Monitor database connectivity and performance
- **Analytics Dashboard**: Real-time insights into application usage
- **Data Export**: Backup and analysis capabilities

### **For Users**
- **Leaderboards**: View top scores and player rankings
- **Personal Stats**: Track individual performance and progress
- **System Status**: Check application health and availability
- **Data Transparency**: Full visibility into stored information

---

**🌐 Access your database information instantly at: http://localhost:5003**

**📊 All your game data, user information, and analytics in one convenient dashboard!**
