#!/bin/bash

set -e  # Exit on error
set -o pipefail  # Exit if any command in a pipeline fails

# Define the backup file path
# Update this with your file name >>>>>
BACKUP_FILE="dde_backup_20230815.json"  
# Activate the virtual environment (if not already active)
source /workspaces/discovery-app/.venv/bin/activate

# Ensure Python can find 'discovery'
export PYTHONPATH="/workspaces/discovery-app"

# Run the restore command
# Here we can replace with restore_from_s3(),
# to automatically pull from server and avoid file pass in 
python /workspaces/discovery-app/scripts/admin.py --filename="$BACKUP_FILE"

echo "✅ Restore completed from $BACKUP_FILE"
