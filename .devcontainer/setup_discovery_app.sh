#!/bin/bash

set -e  # Exit on error
set -o pipefail  # Exit if any command in a pipeline fails

# Variables
INSTALL_DIR="/workspaces/discovery-app"
COMPOSE_DIR="$INSTALL_DIR/docker"
FILENAME="dde_backup_20230815.json"
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

# Create & activate virtual environment
echo "🐍 Creating Python virtual environment..."
echo $INSTALL_DIR/.venv
python3 -m venv $INSTALL_DIR/.venv
source $INSTALL_DIR/.venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🔹 Starting Elasticsearch with Docker Compose..."

# Start Elasticsearch service
docker compose -f $COMPOSE_DIR/docker-compose.yml up -d es

echo "✅ Elasticsearch is now running!"

# # Verify Elasticsearch is up
# echo "🔎 Checking Elasticsearch status..."
# sleep 50  # Give it time to start
# curl -X GET "http://localhost:9200" || echo "⚠️ Elasticsearch is not responding!"
# Verify Elasticsearch is up
echo "🔎 Checking Elasticsearch status..."
RETRIES=10  # Number of retries before failing
ES_READY=false

for i in $(seq 1 $RETRIES); do
    if curl -s "http://localhost:9200" | grep -q "cluster_name"; then
        echo "✅ Elasticsearch is ready!"
        ES_READY=true
        break
    else
        echo "⏳ Waiting for Elasticsearch to be ready... (attempt $i/$RETRIES)"
        sleep 10
    fi
done

if [ "$ES_READY" = false ]; then
    echo "❌ Elasticsearch did not start successfully. Exiting."
    exit 1
fi

# Check if the index exists
echo "🔍 Checking if index '$INDEX_NAME' exists..."
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:9200/$INDEX_NAME" | grep -q "200"; then
    echo "✅ Index '$INDEX_NAME' already exists. No restore needed."
else
    echo "⚠️ Index '$INDEX_NAME' not found. Running restore..."
    python3 -c "from discovery.utils.backup import restore_from_file; restore_from_file('$FILENAME')"
    echo "✅ Restore process completed!"
fi