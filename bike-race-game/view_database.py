#!/usr/bin/env python3
"""
Database viewer for Bike Race Game
Shows all user data, scores, and login logs
"""

import sqlite3
from datetime import datetime
import os

def view_database():
    db_path = '/home/sourav/bike-race-game/instance/bike_race.db'
    
    if not os.path.exists(db_path):
        print("Database file not found. Run the game first to create it.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("🏍️ BIKE RACE GAME DATABASE VIEWER")
    print("=" * 70)
    
    # Show Users
    print("\n📋 RACERS:")
    print("-" * 50)
    cursor.execute("SELECT id, username, email, created_at FROM user ORDER BY created_at DESC")
    users = cursor.fetchall()
    
    if users:
        print(f"{'ID':<4} {'Username':<15} {'Email':<25} {'Joined':<20}")
        print("-" * 64)
        for user in users:
            created = datetime.fromisoformat(user[3]).strftime('%Y-%m-%d %H:%M')
            print(f"{user[0]:<4} {user[1]:<15} {user[2]:<25} {created:<20}")
    else:
        print("No racers found.")
    
    # Show Top Scores
    print("\n🏆 TOP RACE SCORES:")
    print("-" * 70)
    cursor.execute("""
        SELECT s.score, s.distance, u.username, s.timestamp, s.ip_address 
        FROM score s 
        JOIN user u ON s.user_id = u.id 
        ORDER BY s.score DESC 
        LIMIT 15
    """)
    scores = cursor.fetchall()
    
    if scores:
        print(f"{'Score':<8} {'Distance':<10} {'Racer':<15} {'Date':<17} {'IP':<15}")
        print("-" * 65)
        for score in scores:
            timestamp = datetime.fromisoformat(score[3]).strftime('%m-%d %H:%M')
            print(f"{score[0]:<8} {score[1]:<10} {score[2]:<15} {timestamp:<17} {score[4]:<15}")
    else:
        print("No race scores found.")
    
    # Show Login Logs
    print("\n🔐 RECENT LOGINS:")
    print("-" * 60)
    cursor.execute("""
        SELECT u.username, l.login_time, l.ip_address 
        FROM login_log l 
        JOIN user u ON l.user_id = u.id 
        ORDER BY l.login_time DESC 
        LIMIT 10
    """)
    logins = cursor.fetchall()
    
    if logins:
        print(f"{'Racer':<15} {'Login Time':<20} {'IP Address':<15}")
        print("-" * 50)
        for login in logins:
            login_time = datetime.fromisoformat(login[1]).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{login[0]:<15} {login_time:<20} {login[2]:<15}")
    else:
        print("No login logs found.")
    
    # Show Statistics
    print("\n📊 RACING STATISTICS:")
    print("-" * 40)
    
    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]
    print(f"Total Racers: {user_count}")
    
    cursor.execute("SELECT COUNT(*) FROM score")
    race_count = cursor.fetchone()[0]
    print(f"Total Races: {race_count}")
    
    cursor.execute("SELECT MAX(score) FROM score")
    max_score = cursor.fetchone()[0]
    if max_score:
        print(f"Highest Score: {max_score}")
        
        cursor.execute("""
            SELECT u.username, s.distance FROM score s 
            JOIN user u ON s.user_id = u.id 
            WHERE s.score = ? 
            LIMIT 1
        """, (max_score,))
        result = cursor.fetchone()
        if result:
            print(f"Top Racer: {result[0]} ({result[1]}m)")
    
    cursor.execute("SELECT MAX(distance) FROM score")
    max_distance = cursor.fetchone()[0]
    if max_distance:
        print(f"Longest Distance: {max_distance}m")
    
    cursor.execute("SELECT AVG(score) FROM score")
    avg_score = cursor.fetchone()[0]
    if avg_score:
        print(f"Average Score: {avg_score:.1f}")
    
    cursor.execute("SELECT AVG(distance) FROM score")
    avg_distance = cursor.fetchone()[0]
    if avg_distance:
        print(f"Average Distance: {avg_distance:.1f}m")
    
    conn.close()
    print("\n" + "=" * 70)

if __name__ == "__main__":
    view_database()
