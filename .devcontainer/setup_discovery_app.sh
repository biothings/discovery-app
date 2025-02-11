#!/bin/bash

set -e  # Exit on error
set -o pipefail  # Exit if any command in a pipeline fails

# Variables
INSTALL_DIR="/workspaces/discovery-app"
COMPOSE_DIR="$INSTALL_DIR/docker"
FILENAME="$INSTALL_DIR/.devcontainer/smartapi_20240725.json"
INDEX_NAME="smartapi_metakg_docs"

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

echo "🐍 Creating Python virtual environment..."
python3 -m venv $INSTALL_DIR/.venv

echo "🔎 Checking virtual environment..."
ls -l $INSTALL_DIR/.venv/bin/activate

echo "✅ Activating virtual environment..."
source $INSTALL_DIR/.venv/bin/activate
echo "🐍 Python Path: $(which python)"
# echo $PS1  # Check if PS1 is set
# export PS1="(.venv) $PS1"

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🔹 Starting Elasticsearch with Docker Compose..."

# Start Elasticsearch service
docker compose -f $COMPOSE_DIR/docker-compose.yml up -d es

echo "✅ Elasticsearch is now running!"

# Verify Elasticsearch is up
echo "🔎 Checking Elasticsearch status..."
sleep 50  # Give it time to start
curl -X GET "http://localhost:9200" || echo "⚠️ Elasticsearch is not responding!"
