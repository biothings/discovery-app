# Discovery App Backend with Elasticsearch

## Overview
This repository sets up a development environment for the Discovery App backend using Elasticsearch in a GitHub Codespace. The configuration includes:
- **Docker Compose** for managing Elasticsearch.
- **Devcontainer configuration** for seamless development in a Codespace.
- **VS Code extensions** for Python and Elasticsearch support.

## Setup Instructions

### 1. Open in Codespaces
1. Click the **"Code"** button in your GitHub repository.
2. Select the **"Codespaces"** tab.
3. Click **"Create codespace on main"** (or the appropriate branch).

### 2. Container Configuration
Your environment is pre-configured using `devcontainer.json`, which includes:
- **Base Image:** `ubuntu-24.04`
- **Docker-in-Docker Support:** Allows running Elasticsearch inside the container.
- **Environment Variables:** `ES_HOST` set to `http://localhost:9200`.
- **Port Forwarding:** Ports `8000` and `9200` exposed.
- **Mounted Volume:** Local `data` folder is mounted to persist Elasticsearch data.
- **VS Code Extensions:** Installed automatically for Python and Elasticsearch.

### 3. Running Elasticsearch
Elasticsearch is managed using `docker-compose.yml`:
# Start Elasticsearch
docker-compose up -d
