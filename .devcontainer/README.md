# Discovery App Backend with Elasticsearch

## Overview
This folder is used to set up a development environment for the Data Discovery Engine (DDE) App in a GitHub Codespace. The current configuration initializes the backend, setting up an Elasticsearch (ES) database and populating it with data in three ES indices:
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
### Summary
This section covers the steps to set up the development environment in GitHub Codespaces, configure container settings, and ensure the necessary software and dependencies are ready for running the application. The Data Setup section, which follows, will guide you through the steps required to prepare the data for the application to use.
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


### 3. Set Up the Environment
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

Notes on Elasticsearch -

>Elasticsearch is managed using `docker-compose.yml` found under the `docker/` folder. When you run the `setup_discovery_app.sh` script, Elasticsearch will be automatically started.

If there is an issue starting ES, see if you can start it manually:

Elasticsearch is managed using `docker-compose.yml` found under the `docker/` folder:
```
docker compose -f docker/docker-compose.yml up -d es
```

If you're using **VS Code** or **GitHub Codespaces**, you can start Elasticsearch directly from the **Docker side panel**:

1. **Open the Docker Panel**: In VS Code or GitHub Codespaces, locate the **Docker** extension in the Activity Bar on the side panel (usually on the left side of the screen).
2. **Locate the `docker-compose.yml`**: Inside the Docker panel, you will see your project's containers and services listed. Find the `docker-compose.yml` under the **"Containers"** or **"Services"** section.
3. **Start Elasticsearch**: Right-click on the `es` service (it might be labeled as Elasticsearch or similar) and select **"Start"**.

*This method allows you to easily manage and start Elasticsearch with just a few clicks, without needing to use the terminal.*

### Verify Elasticsearch is running
After running the setup, you can verify that Elasticsearch is up and running.

#### Option 1: Using `curl`
Run the following command in your terminal to check if Elasticsearch is responding:
```
curl "http://localhost:9200"
```


#### Option 2: Viewing in the Browser
You can also view the Elasticsearch status directly in your web browser. Open your browser and navigate to: http://localhost:9200.

**If it responds with cluster information, the setup was successful!** ✅

## Restoring Data
> There are two options for data restoration. Backup data from a file, or backup the data from a server.

Once ES is setup correctly and **running**, you can add index data.

> Note: The data will persist through codespace sessions, therefore data restoration does not need to run each time you load a session.

### Option 1: Restore data from a file
1. Add the Backup File to Codespaces
Since we don’t want to commit large JSON files to the repository, you should manually upload the backup file to your Codespace environment.

1. Locally, place the backup JSON file (e.g., `dde_backup_20230815.json`) inside `~/workspaces/discovery-app/.devcontainer`.
2. In the Codespace terminal, you can confirm the file exists:
```
ls -l ~/workspaces/discovery-app/.devcontainer/dde_backup_20230815.json
```
3. Edit the `setup_index.sh` file and set the `BACKUP_FILE` key to your filename.
```
BACKUP_FILE = # your_filename_here
```
 4. Restore the Data
Once the file is available in the workspace and set in the bash script, run:
```
./setup_index.sh
```
✅ **If successful, in the terminal you should see:**
```
Restore completed from [your backup filename]
```

### Option 2: Restore from S3 Server
To avoid manually handling backup files, you can modify the restore script to pull the backup directly from an S3 bucket. This requires a working AWS credential with proper S3 read permission.

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

---

### **Viewing Running Ports and Application**

When the environment is set up, the application is ready to run.

With Elasticsearch running, navigate to the `/discovery-app` folder and start the application by running:
```bash
python index.py
```

#### **View the Application from the Ports Panel**

1. Open the **Ports** tab in the **Codespaces** UI.
2. Look for the row with **port 8000** (this is your application).
3. Click the **globe icon 🌐** next to port 8000 to open the application in your browser.

Alternatively, you can manually open:
```
https://<your-codespace-name>-8000.githubpreview.dev
```
*(Replace `<your-codespace-name>` with your actual Codespace name.)*


#### **Check Open Ports in Codespaces**
1. Click on the **Ports** tab in the **Codespaces** UI.
2. You’ll see a list of forwarded ports, including:
   - **8000** → Application API
   - **9200** → Elasticsearch

#### **Set Port Privacy Options**
- **Private:** Only you can access the port.
- **Public:** Anyone with the link can access it.
- **Organization:** Only users in your GitHub organization can access it.

To change privacy settings:
1. Click the **Port Settings** ⚙️ next to the port.
2. Select the desired **privacy option**.

#### **Access the Running Application**
- Open a browser and go to:
  ```
  https://<your-codespace-name>-8000.githubpreview.dev
  ```
  *(Replace `<your-codespace-name>` with the actual name of your Codespace, which is shown in the URL bar.)*



## **Wrapping Up**

Your development environment is now fully set up, and the application is running successfully. Here’s a quick recap:

✅ **Environment Setup:** GitHub Codespaces automatically configures your container.
✅ **Running the Application:** Start Elasticsearch, navigate to `/discovery-app`, and run `python index.py`.
✅ **Accessing the App:** Use the **Ports panel** and click the **globe icon 🌐** for port 8000.

### **Sharing with Live Share**

If you need to collaborate in real time, you can use **Visual Studio Code Live Share**:

1. Open **VS Code** in your Codespace.
2. Click the **Live Share** button in the status bar.
3. Copy the invite link and share it with your collaborators.
4. They can join your session to **edit, debug, and interact** with your environment.

### **Next Steps**
- Explore the API and test endpoints.
- Customize configurations as needed.
- Check logs and debugging tools if any issues arise.

If you have any questions or run into issues, refer to the documentation or reach out to the team. 🚀

**Happy coding! 🎉**

---
