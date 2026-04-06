#!/bin/bash
# Hospital Management System - Startup Script
# This script runs Redis, Celery worker, Celery beat, and Flask app

echo "=== Hospital Management System ==="

# Start Redis server (in background)
echo "Starting Redis..."
redis-server --daemonize yes 2>/dev/null || echo "Redis already running or not available"

# Wait for Redis to start
sleep 1

# Start Celery worker
echo "Starting Celery worker..."
source venv/bin/activate
celery -A background_jobs worker --loglevel=info --detach --logfile celery_worker.log

# Start Celery beat (scheduler)
echo "Starting Celery beat (scheduler)..."
celery -A background_jobs beat --loglevel=info --detach --logfile celery_beat.log

# Start Flask app
echo "Starting Flask app..."
python app.py
