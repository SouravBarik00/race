from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bike-race-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bike_race.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scores = db.relationship('Score', backref='user', lazy=True)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=False)

class LoginLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=False)

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('game.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'})
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already exists'})
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            
            # Log the login
            login_log = LoginLog(
                user_id=user.id,
                ip_address=request.remote_addr
            )
            db.session.add(login_log)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/submit_score', methods=['POST'])
def submit_score():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.get_json()
    score_value = data.get('score')
    distance_value = data.get('distance')
    
    score = Score(
        user_id=session['user_id'],
        score=score_value,
        distance=distance_value,
        ip_address=request.remote_addr
    )
    db.session.add(score)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Score submitted'})

@app.route('/leaderboard')
def leaderboard():
    # Get top 10 scores
    top_scores = db.session.query(Score, User).join(User).order_by(Score.score.desc()).limit(10).all()
    
    # Get current user's best score
    user_best = None
    if 'user_id' in session:
        user_best = Score.query.filter_by(user_id=session['user_id']).order_by(Score.score.desc()).first()
    
    leaderboard_data = []
    for score, user in top_scores:
        leaderboard_data.append({
            'username': user.username,
            'score': score.score,
            'distance': score.distance,
            'timestamp': score.timestamp.strftime('%Y-%m-%d %H:%M')
        })
    
    return jsonify({
        'leaderboard': leaderboard_data,
        'user_best': user_best.score if user_best else 0,
        'user_best_distance': user_best.distance if user_best else 0,
        'current_user': session.get('username', '')
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
