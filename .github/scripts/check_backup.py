"""
This script checks if a backup file for the current date exists in a specified S3 bucket.
If the backup file does not exist, a notification is sent to a Slack channel.

Expected file format in the S3 bucket:
- The file should be in the folder 'db_backup/' with the following naming pattern:
  'dde_backup_YYYYMMDD.zip', where YYYYMMDD corresponds to the current date.

Required Environment Variables:
- AWS_ACCESS_KEY_ID: The AWS access key ID to read the AWS s3 bucket.
- AWS_SECRET_ACCESS_KEY: The AWS secret access key  to read the AWS s3 bucket.
- BACKUP_BUCKET_NAME: The name of the AWS S3 bucket where backups are stored.
- S3_FOLDER: The folder path within the S3 bucket where backups are stored (e.g., 'db_backup/').
- AWS_REGION: The AWS region where the S3 bucket is located.
- SLACK_CHANNEL: The Slack channel where notifications should be sent (e.g., '#observability-test').
- SLACK_WEBHOOK_URL: The Slack Webhook URL used to send the notification.

Functionality:
1. The script uses the AWS SDK (boto3) to check for the existence of the backup file in the specified S3 bucket.
2. If the file is found, it logs that no action is needed.
3. If the file is not found, it sends a notification to the configured Slack channel.

Dependencies:
- boto3: For interacting with AWS S3.
- requests: For sending HTTP POST requests to Slack.

"""

import boto3
import botocore
import os
import requests

from datetime import datetime


def send_slack_notification(message):

    print(f" └─ {message}")

    # Create the payload for Slack
    slack_data = {
        "channel": os.getenv("SLACK_CHANNEL"),
        "username": "DDE",
        "icon_emoji": ":thumbsdown:",
        "text": message,
    }

    try:
        print(" └─ Sending Slack notification.")
        response = requests.post(os.getenv("SLACK_WEBHOOK_URL"), json=slack_data, timeout=10)
        if response.status_code == 200:
            print(" └─ Slack notification sent successfully.")
        else:
            print(f" └─ Failed to send message to Slack: {response.status_code}, {response.text}")
    except requests.exceptions.Timeout as e:
        print(" └─ Request timed out to Slack WebHook URL.")
        raise e
    except requests.exceptions.RequestException as e:
        print(f" └─ Failed to send Slack notification. Error: {str(e)}")
        raise e


def check_backup_file():

    # Create the expected file name
    today_date = datetime.today().strftime("%Y%m%d")
    expected_file = f"{os.getenv('S3_FOLDER')}dde_backup_{today_date}.zip"

    # Create the S3 client
    s3_client = boto3.client("s3", region_name=os.getenv("AWS_REGION"))

    # Try to fetch the file metadata
    try:
        response = s3_client.head_object(Bucket=os.getenv("BACKUP_BUCKET_NAME"), Key=expected_file)
        print(f" └─ Backup file {expected_file} exists!")

        # Get the file size in bytes
        file_size = response['ContentLength']

        # Check if the file is larger than 1MB
        if file_size > 1048576:  # 1MB in bytes
            print(f" └─ Backup file is larger than 1MB! Size: {file_size} bytes.")
            print(" └─ Nothing to do!")
        else:
            message = f":alert: The backup file {expected_file} is smaller than 1MB!"
            send_slack_notification(message)

    except botocore.exceptions.ClientError as e:
        print(e)
        message = f":alert: The backup file {expected_file} was NOT created today!"
        send_slack_notification(message)


if __name__ == "__main__":
    check_backup_file()
