#!/usr/bin/env python3
"""
Database viewer for Snake Game
Shows all user data, scores, and login logs
"""

import sqlite3
from datetime import datetime
import os

def view_database():
    db_path = '/home/sourav/snake-game/instance/snake_game.db'
    
    if not os.path.exists(db_path):
        print("Database file not found. Run the game first to create it.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("🐍 SNAKE GAME DATABASE VIEWER")
    print("=" * 60)
    
    # Show Users
    print("\n📋 USERS:")
    print("-" * 40)
    cursor.execute("SELECT id, username, email, created_at FROM user ORDER BY created_at DESC")
    users = cursor.fetchall()
    
    if users:
        print(f"{'ID':<4} {'Username':<15} {'Email':<25} {'Created':<20}")
        print("-" * 64)
        for user in users:
            created = datetime.fromisoformat(user[3]).strftime('%Y-%m-%d %H:%M')
            print(f"{user[0]:<4} {user[1]:<15} {user[2]:<25} {created:<20}")
    else:
        print("No users found.")
    
    # Show Scores
    print("\n🏆 SCORES:")
    print("-" * 50)
    cursor.execute("""
        SELECT s.score, u.username, s.timestamp, s.ip_address 
        FROM score s 
        JOIN user u ON s.user_id = u.id 
        ORDER BY s.score DESC 
        LIMIT 10
    """)
    scores = cursor.fetchall()
    
    if scores:
        print(f"{'Score':<8} {'Username':<15} {'Date':<20} {'IP Address':<15}")
        print("-" * 58)
        for score in scores:
            timestamp = datetime.fromisoformat(score[2]).strftime('%Y-%m-%d %H:%M')
            print(f"{score[0]:<8} {score[1]:<15} {timestamp:<20} {score[3]:<15}")
    else:
        print("No scores found.")
    
    # Show Login Logs
    print("\n🔐 LOGIN LOGS:")
    print("-" * 50)
    cursor.execute("""
        SELECT u.username, l.login_time, l.ip_address 
        FROM login_log l 
        JOIN user u ON l.user_id = u.id 
        ORDER BY l.login_time DESC 
        LIMIT 10
    """)
    logins = cursor.fetchall()
    
    if logins:
        print(f"{'Username':<15} {'Login Time':<20} {'IP Address':<15}")
        print("-" * 50)
        for login in logins:
            login_time = datetime.fromisoformat(login[1]).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{login[0]:<15} {login_time:<20} {login[2]:<15}")
    else:
        print("No login logs found.")
    
    # Show Statistics
    print("\n📊 STATISTICS:")
    print("-" * 30)
    
    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]
    print(f"Total Users: {user_count}")
    
    cursor.execute("SELECT COUNT(*) FROM score")
    score_count = cursor.fetchone()[0]
    print(f"Total Games Played: {score_count}")
    
    cursor.execute("SELECT MAX(score) FROM score")
    max_score = cursor.fetchone()[0]
    if max_score:
        print(f"Highest Score: {max_score}")
        
        cursor.execute("""
            SELECT u.username FROM score s 
            JOIN user u ON s.user_id = u.id 
            WHERE s.score = ? 
            LIMIT 1
        """, (max_score,))
        top_player = cursor.fetchone()[0]
        print(f"Top Player: {top_player}")
    
    cursor.execute("SELECT AVG(score) FROM score")
    avg_score = cursor.fetchone()[0]
    if avg_score:
        print(f"Average Score: {avg_score:.1f}")
    
    conn.close()
    print("\n" + "=" * 60)

if __name__ == "__main__":
    view_database()
