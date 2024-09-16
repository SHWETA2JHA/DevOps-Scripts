import boto3
import zipfile
import os
from datetime import datetime, timedelta
import shutil

def compress_directory(source_dir, output_filename):
    """Compress a directory into a ZIP file."""
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, source_dir))
    print(f"Directory {source_dir} compressed into {output_filename}")

def upload_to_s3(local_file, bucket_name, s3_key):
    """Upload a file to an S3 bucket."""
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(local_file, bucket_name, s3_key)
        print(f"Uploaded {local_file} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading {local_file}: {e}")

def delete_old_backups(bucket_name, prefix, days=30):
    """Delete old backups from S3."""
    s3_client = boto3.client('s3')
    cutoff_date = datetime.now() - timedelta(days=days)
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            last_modified = obj['LastModified']
            if last_modified < cutoff_date:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f"Deleted old backup {obj['Key']}")

if __name__ == "__main__":
    # Configuration
    SOURCE_DIR = '/path/to/source/directory'
    BACKUP_FILE = '/tmp/backup.zip'
    BUCKET_NAME = 'your-s3-bucket-name'
    S3_KEY = 'backups/backup-' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.zip'
    OLD_BACKUPS_PREFIX = 'backups/'

    # Compress directory
    compress_directory(SOURCE_DIR, BACKUP_FILE)

    # Upload to S3
    upload_to_s3(BACKUP_FILE, BUCKET_NAME, S3_KEY)

    # Optionally delete old backups
    delete_old_backups(BUCKET_NAME, OLD_BACKUPS_PREFIX, days=30)

    # Clean up local backup file
    os.remove(BACKUP_FILE)
    print(f"Local backup file {BACKUP_FILE} removed")
