#!/bin/bash
# Script to start the FastAPI backend server

# Check if running in development or production
if [ "$1" = "prod" ]; then
    echo "Starting server in production mode..."
    cd backend
    USE_MOCK_AUDIO=false uvicorn main:app --host 0.0.0.0 --port 8000
else
    echo "Starting server in development mode with mock audio..."
    cd backend
    USE_MOCK_AUDIO=true uvicorn main:app --reload --host 0.0.0.0 --port 8000
fi