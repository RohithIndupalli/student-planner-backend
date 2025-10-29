#!/bin/bash

# Enable Python's unbuffered output
PYTHONUNBUFFERED=1

# Set Python path
export PYTHONPATH="/opt/render/project/src:$PYTHONPATH"

# Log environment variables (without sensitive data)
echo "🔧 Environment Variables:"
echo "- MONGODB_URL: ${MONGODB_URL:0:20}..."
echo "- MONGODB_URI: ${MONGODB_URI:0:20}..."
echo "- DATABASE_NAME: $DATABASE_NAME"
echo "- ENVIRONMENT: $ENVIRONMENT"

# Start the application
echo "🚀 Starting application..."
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
