#!/bin/bash

# Enable Python's unbuffered output
export PYTHONUNBUFFERED=1

# Set Python path
export PYTHONPATH="/opt/render/project/src:$PYTHONPATH"

# Log environment variables (without sensitive data)
echo "🔧 Environment Variables:"
echo "- MONGODB_URL: ${MONGODB_URL:0:20}..."
echo "- MONGODB_URI: ${MONGODB_URI:0:20}..."
echo "- DATABASE_NAME: $DATABASE_NAME"
echo "- ENVIRONMENT: $ENVIRONMENT"
echo "- PYTHONPATH: $PYTHONPATH"

# Install/update dependencies
echo "📦 Installing/updating dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Start the application with auto-reload in development
echo "🚀 Starting application..."
if [ "$ENVIRONMENT" = "development" ]; then
    echo "⚡ Running in development mode with auto-reload"
    exec uvicorn backend.main:app --host 0.0.0.0 --port $PORT --reload
else
    echo "🚀 Running in production mode"
    exec uvicorn backend.main:app --host 0.0.0.0 --port $PORT
fi
