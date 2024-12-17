#!/bin/bash

set -e  # Exit on error
set -o pipefail  # Exit if any command in a pipeline fails

# Variables
REPO_URL="https://github.com/biothings/discovery-app.git"
INSTALL_DIR="$HOME/discovery-app"
PYTHON_VERSION="3.12"

echo "🔹 Updating system packages..."
sudo apt-get update && sudo apt-get install -y \
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
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.$PYTHON_VERSION 1
sudo update-alternatives --config python3

echo "✅ Python version set to: $(python3 --version)"

# Clone repository
if [ -d "$INSTALL_DIR" ]; then
    echo "📂 Discovery App already exists. Pulling latest changes..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "📥 Cloning Discovery App repository..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Create & activate virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

#