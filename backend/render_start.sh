#!/usr/bin/env bash
# Render start script for PathPilot AI backend
set -e

# Run database migrations / table creation on startup (handled by FastAPI lifespan)
# Start uvicorn on the PORT assigned by Render (defaults to 10000)
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-10000}"
