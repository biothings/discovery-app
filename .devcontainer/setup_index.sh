#!/bin/bash

set -e  # Exit on error
set -o pipefail  # Exit if any command in a pipeline fails

# Define the backup file path
BACKUP_FILE= #UPDATE WITH YOUR FILENAME HERE

# Activate the virtual environment (if not already active)
source /workspaces/discovery-app/.venv/bin/activate

# Ensure Python can find 'discovery'
export PYTHONPATH="/workspaces/discovery-app"

# Run the restore command (2 Options)

# Run the restore command for a local backup file (default)
python /workspaces/discovery-app/scripts/admin.py --filename="$BACKUP_FILE"

# Alternatively, uncomment the next line to restore directly from S3 (no filename required)
# python -c "from discovery.utils.backup import restore_from_s3; restore_from_s3()"

echo "✅ Restore completed from $BACKUP_FILE"
