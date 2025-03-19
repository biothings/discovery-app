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
Once inside the Codespace, open the terminal and go to `/workspaces/discovery-app/devcontainer`, and run our setup file:  
```bash
./setup_discovery_app.sh
```
alternatively,
```
bash setup_discovery_app.sh
```

This script will:

* Install system dependencies.
* Create and activate a Python virtual environment.
* Install project dependencies from `requirements.txt`.
* Start Elasticsearch using Docker Compose and/or Visual Studio.

--- 

Notes on ES:  
Elasticsearch is managed using `docker-compose.yml` found under the `docker/` folder. When you run the `setup_discovery_app.sh` script, Elasticsearch will be automatically started using the following command:

If there is an issue starting ES, see if you can start it manually:  

Elasticsearch is managed using `docker-compose.yml` found under the `docker/` folder:
```
docker compose up -d es
```  

If you're using **VS Code** or **GitHub Codespaces**, you can start Elasticsearch directly from the **Docker side panel**:

1. **Open the Docker Panel**: In VS Code or GitHub Codespaces, locate the **Docker** extension in the Activity Bar on the side panel (usually on the left side of the screen).
2. **Locate the `docker-compose.yml`**: Inside the Docker panel, you will see your project's containers and services listed. Find the `docker-compose.yml` under the **"Containers"** or **"Services"** section.
3. **Start Elasticsearch**: Right-click on the `es` service (it might be labeled as Elasticsearch or similar) and select **"Start"**.

This method allows you to easily manage and start Elasticsearch with just a few clicks, without needing to use the terminal.

---


### 3. Verify Elasticsearch
After running the setup, you can verify that Elasticsearch is up and running.

#### Option 1: Using `curl`
Run the following command in your terminal to check if Elasticsearch is responding:
```
curl -X GET "http://localhost:9200"
```  



#### Option 2: Viewing in the Browser
You can also view the Elasticsearch status directly in your web browser. Open your browser and navigate to:

If it responds with cluster information, the setup was successful! ✅

## Restoring Data
After Elasticsearch is running, you can restore data from a local backup file.

### 1. Add the Backup File to Codespaces
Since we don’t want to commit large JSON files to the repository, you should manually upload the backup file to your Codespace environment.

1. Locally, place the backup JSON file (e.g., `dde_backup_20230815.json`) inside `~/workspaces/discovery-app/.devcontainer`.
2. In the Codespace terminal, you can confirm the file exists:
```
ls -l ~/workspaces/discovery-app/.devcontainer/dde_backup_20230815.json
```  
3. Edit the `setup_index.sh` file and set the `BACKUP_FILE` key to your filename.

### 2. Restore the Data  

Once the file is available in the workspace and set in the bash script, run:
```
./setup_index.sh
```
✅ If successful, you should see:
```
Restore completed from [your backup filename]
```

### Optional: Restore from S3 Instead of Local Files
To avoid manually handling backup files, you can modify the restore script to pull the backup directly from an S3 bucket.

To do this use this edit the `setup_index.sh`:

1. Comment out the backup from file line:  
```
python /workspaces/discovery-app/scripts/admin.py --filename="$BACKUP_FILE"
```
goes to 
```
# python /workspaces/discovery-app/scripts/admin.py --filename="$BACKUP_FILE"
```
2. Uncomment the line for s3 upload:

```
# python -c "from discovery.utils.backup import restore_from_s3; restore_from_s3()
```
to this
```
python -c "from discovery.utils.backup import restore_from_s3; restore_from_s3()
```

Then run: ```/.setup_index.sh```
