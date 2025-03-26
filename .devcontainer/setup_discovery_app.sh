#!/bin/bash

set -e  # Exit on error
set -o pipefail  # Exit if any command in a pipeline fails

# Variables
INSTALL_DIR="/workspaces/discovery-app"
COMPOSE_DIR="$INSTALL_DIR/docker"

cd $INSTALL_DIR

sudo apt-get update && sudo apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    build-essential \
    vim \
    curl \
    git \
    python3-venv \
    python3-dev \
    libxmlsec1-dev \
    pkg-config 

echo "🐍 Creating Python virtual environment..."
python3 -m venv $INSTALL_DIR/.venv

echo "🔎 Checking virtual environment..."
ls -l $INSTALL_DIR/.venv/bin/activate

echo "✅ Activating virtual environment..."
source $INSTALL_DIR/.venv/bin/activate
echo "🐍 Python Path: $(which python)"

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🐳 Starting Elasticsearch with Docker Compose..."

# Start Elasticsearch service
docker compose -f $COMPOSE_DIR/docker-compose.yml up -d es

echo "✅ Elasticsearch is now running!"

# Verify Elasticsearch is up
echo "🔎 Checking Elasticsearch (ES) status..."
TIMEOUT=60   # Set timeout in seconds (e.g., 60 seconds)
START_TIME=$(date +%s)  # Record start time in seconds since epoch
ELAPSED_TIME=0
until curl -X GET "http://localhost:9200"; do
    CURRENT_TIME=$(date +%s)
    ELAPSED_TIME=$((CURRENT_TIME - START_TIME))
    # Check if elapsed time exceeds timeout
    if [ "$ELAPSED_TIME" -ge "$TIMEOUT" ]; then
        echo "⚠️ Failed to start ES within $TIMEOUT seconds. Check manually to make sure it's running properly."
        exit 1
    fi
    echo "ES is not running yet, retrying... (Elapsed: $ELAPSED_TIME seconds)"
    sleep 2  # Wait 2 seconds before retrying
done
echo "ES is started successfully after $ELAPSED_TIME seconds!"
