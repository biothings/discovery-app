#!/bin/bash

set -e  # Exit on error
set -o pipefail  # Exit if any command in a pipeline fails

# Variables
INSTALL_DIR="$HOME/discovery-app"
PYTHON_VERSION="3.12"

echo "🔹 Updating system packages..."
apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    build-essential \
    vim \
    curl \
    git \
    python3.$PYTHON_VERSION \
    python3.$PYTHON_VERSION-venv \
    python3.$PYTHON_VERSION-dev

echo "🔹 Setting Python $PYTHON_VERSION as default..."
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.$PYTHON_VERSION 1
update-alternatives --config python3

echo "✅ Python version set to: $(python3 --version)"

# Create & activate virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🔹 Starting Elasticsearch with Docker Compose..."

# Navigate to the directory containing docker-compose.yml
COMPOSE_DIR="$HOME/discovery-app/docker"
cd "$COMPOSE_DIR"

# Start Elasticsearch service
docker-compose up -d es

echo "✅ Elasticsearch is now running!"

# Verify Elasticsearch is up
echo "🔎 Checking Elasticsearch status..."
sleep 10  # Give it time to start
curl -X GET "http://localhost:9200" || echo "⚠️ Elasticsearch is not responding!"
