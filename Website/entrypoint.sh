#!/bin/sh

set -e

wait_for_db() {
  echo "Waiting for postgres..."
  until pg_isready -h db -p 5432 -U postgres; do
    echo "Postgres is unavailable - sleeping"
    sleep 1
  done
  echo "Postgres is up - continuing..."
}

wait_for_db


# Check if migrations should be run
if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Running database migrations..."
  flask db upgrade
fi

echo "Starting the Flask application..."
exec gunicorn -b :5000 --access-logfile - --error-logfile - manage:app
