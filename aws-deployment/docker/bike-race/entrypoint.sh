#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database connection..."
python -c "
import os
import time
import psycopg2
from urllib.parse import urlparse

# Get database URL from environment or secrets
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print('DATABASE_URL not found')
    exit(1)

# Parse database URL
parsed = urlparse(db_url)
host = parsed.hostname
port = parsed.port or 5432
database = parsed.path[1:]  # Remove leading slash
username = parsed.username
password = parsed.password

# Wait for database
max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        conn.close()
        print('Database connection successful')
        break
    except psycopg2.OperationalError as e:
        retry_count += 1
        print(f'Database connection attempt {retry_count}/{max_retries} failed: {e}')
        time.sleep(2)

if retry_count >= max_retries:
    print('Failed to connect to database after maximum retries')
    exit(1)
"

# Initialize database if needed
echo "Initializing database..."
python -c "
import os
from app import app, db

with app.app_context():
    db.create_all()
    print('Database tables created successfully')
"

echo "Starting Bike Race Game application..."
exec "$@"
