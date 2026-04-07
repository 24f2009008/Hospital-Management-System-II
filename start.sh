#!/bin/bash
# Hospital Management System - Startup Script
# This script runs Redis, Celery worker, Celery beat, and Flask app

echo "=== Hospital Management System ==="

# Kill any existing celery processes to avoid lock conflicts
echo "Stopping any existing Celery processes..."
pkill -f "celery.*worker" 2>/dev/null
pkill -f "celery.*beat" 2>/dev/null
sleep 2

# Remove stale schedule file
rm -f celerybeat-schedule celerybeat-schedule.db /tmp/celerybeat-schedule /tmp/celerybeat-schedule.db

# Start Redis server (in background)
echo "Starting Redis..."
redis-server --daemonize yes 2>/dev/null || echo "Redis already running or not available"

# Wait for Redis to start
sleep 1

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start Celery worker
echo "Starting Celery worker (for processing tasks)..."
celery -A background_jobs worker --loglevel=info --detach --logfile celery_worker.log

# Start Celery beat (scheduler - runs daily/monthly jobs automatically)
echo "Starting Celery beat (scheduler for daily/monthly jobs)..."
celery -A background_jobs beat --loglevel=info --detach --logfile celery_beat.log

echo ""
echo "=== Scheduled Jobs ==="
echo "- Daily Reminders: Runs every 24 hours (sends appointment reminders)"
echo "- Monthly Report: Runs every 30 days (sends doctor activity reports)"
echo ""
echo "To manually trigger jobs:"
echo "  celery -A background_jobs call send_daily_reminders"
echo "  celery -A background_jobs call generate_monthly_reports"
echo ""

# Start Flask app
echo "Starting Flask app..."
python app.py