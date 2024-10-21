#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Function to wait for the database to be ready using pg_isready
wait_for_db() {
  echo "Waiting for postgres..."
  until pg_isready -h db -p 5432 -U postgres; do
    echo "Postgres is unavailable - sleeping"
    sleep 1
  done
  echo "Postgres is up - continuing..."
}

# Wait for the database
wait_for_db

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Start the Flask application
echo "Starting the Flask application..."
exec gunicorn -b :5000 --access-logfile - --error-logfile - manage:app
