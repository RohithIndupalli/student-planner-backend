#!/bin/bash

# Exit on error
set -e

# Enable Python's unbuffered output
export PYTHONUNBUFFERED=1

# Set Python path
export PYTHONPATH="/opt/render/project/src:$PYTHONPATH"

# Log environment variables (without sensitive data)
echo "🔧 Environment Variables:"
echo "- MONGODB_URL: ${MONGODB_URL:0:20}..."
echo "- MONGODB_URI: ${MONGODB_URI:0:20}..."
echo "- DATABASE_NAME: $DATABASE_NAME"
echo "- ENVIRONMENT: ${ENVIRONMENT:-development}"
echo "- PYTHONPATH: $PYTHONPATH"

# Install/update dependencies
echo "📦 Installing/updating dependencies..."
python -m pip install --upgrade pip

# Install requirements with retry logic
MAX_RETRIES=3
RETRY_DELAY=5

for i in $(seq 1 $MAX_RETRIES); do
    echo "Attempt $i of $MAX_RETRIES: Installing requirements..."
    if pip install -r requirements.txt; then
        echo "✅ Dependencies installed successfully"
        break
    else
        if [ $i -eq $MAX_RETRIES ]; then
            echo "❌ Failed to install dependencies after $MAX_RETRIES attempts"
            exit 1
        fi
        echo "⚠️ Installation failed, retrying in $RETRY_DELAY seconds..."
        sleep $RETRY_DELAY
    fi
done

# Verify critical packages
echo "🔍 Verifying critical packages..."
python -c "
import pkg_resources
required = {'fastapi', 'uvicorn', 'pydantic', 'motor'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    print(f'❌ Missing packages: {missing}')
    exit(1)
print('✅ All required packages are installed')
"

# Start the application with auto-reload in development
echo "🚀 Starting application..."
if [ "$ENVIRONMENT" = "development" ]; then
    echo "⚡ Running in development mode with auto-reload"
    exec uvicorn backend.main:app --host 0.0.0.0 --port $PORT --reload
else
    echo "🚀 Running in production mode"
    exec uvicorn backend.main:app --host 0.0.0.0 --port $PORT
fi
