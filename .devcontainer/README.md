# Discovery App Backend with Elasticsearch

## Overview  
This repository sets up a development environment for the Discovery Data App in a GitHub Codespace. The current configuration initializes the backend, setting up an Elasticsearch (ES) database and populating it with data in:  
- `smartapi_docs`  
- `smartapi_metakg_docs`  
- `smartapi_metakg_consolidated`  

The configuration includes:  
- **Docker Compose** for managing Elasticsearch.  
- **Devcontainer configuration** (`devcontainer.json`) for seamless development in a Codespace.  
- **VS Code extensions** for Python and Elasticsearch support.  

> 📖 **For more on GitHub Codespaces, see the [official documentation](https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces).**  

---

## Initial Setup Instructions  

### 1. Open in GitHub Codespaces  
1. Click the **"Code"** button in your GitHub repository.  
2. Select the **"Codespaces"** tab.  
3. Click **"Create codespace on main"** (or the appropriate branch).  
   - Running through **Visual Studio Code** is recommended.  

### 2. Container Configuration  
When the Codespace starts, `devcontainer.json` **automatically** configures the environment with:  
- **Base Image:** `ubuntu-24.04`  
- **Docker-in-Docker Support:** Runs Elasticsearch inside the container.  
- **Environment Variables:** Sets `ES_HOST=http://localhost:9200`.  
- **Port Forwarding:** Exposes ports `8000` and `9200`.  
- **Mounted Volume:** Persists Elasticsearch data via a local `data` folder.  
- **VS Code Extensions:** Installs support for Python and Elasticsearch.  

---

## Running the Application  

### 1. Set Up the Environment  
Once inside the Codespace, run:  
```bash
./setup_discovery_app.sh
```

This script will:

* Install system dependencies.
* Create and activate a Python virtual environment.
* Install project dependencies from requirements.txt.
* Start Elasticsearch using Docker Compose.


### 2. Start Elasticsearch
Elasticsearch is managed using `docker-compose.yml`:
```
docker compose up -d es
```  
### 3. Verify Elasticsearch
```
curl -X GET "http://localhost:9200"
```  
If it responds with cluster information, the setup was successful! ✅

## Restoring Data
After Elasticsearch is running, you can restore data from a local backup file.

### 1. Add the Backup File to Codespaces
Since we don’t want to commit large JSON files to the repository, you should manually upload the backup file to your Codespace environment.

1. Locally, place the backup JSON file (e.g., `dde_backup_20230815.json`) inside ~/workspaces/discovery-app/.
2. In the Codespace terminal, confirm the file exists:
```
ls -l ~/workspaces/discovery-app/dde_backup_20230815.json
```

### 2. Restore the Data  

Once the file is available in the workspace, run:
```
source /workspaces/discovery-app/.venv/bin/activate  
export PYTHONPATH="/workspaces/discovery-app"  
python /workspaces/discovery-app/scripts/admin.py --filename="dde_backup_20230815.json"
```
✅ If successful, you should see:
```
Restore completed from dde_backup_20230815.json
```

### Optional: Restore from S3 Instead of Local Files
To avoid manually handling backup files, you can modify the restore script to pull the backup directly from an S3 bucket.

## 1. Configure AWS Credentials in Codespaces
If you have an AWS S3 bucket storing the backup file, first configure your credentials:
```
aws configure
```
You’ll need to enter your:

* AWS Access Key
* AWS Secret Key
* Default region
### 2. Modify the Restore Script
Instead of using a local file, replace the filename with an S3 restore function inside `scripts/admin.py`:
```
from my_s3_utils import restore_from_s3

restore_from_s3(bucket_name="my-backup-bucket", object_key="backup/dde_backup.json")
```
This will automatically fetch and restore the latest backup from S3!