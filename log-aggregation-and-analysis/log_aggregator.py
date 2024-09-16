import boto3
import paramiko
import os
from collections import Counter
from io import StringIO

def download_logs_from_server(server_ip, username, key_file, remote_log_paths, local_log_dir):
    """Download logs from a remote server."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_ip, username=username, key_filename=key_file)
    
    sftp = ssh.open_sftp()
    try:
        for remote_log_path in remote_log_paths:
            local_log_path = os.path.join(local_log_dir, os.path.basename(remote_log_path))
            sftp.get(remote_log_path, local_log_path)
            print(f"Downloaded {remote_log_path} to {local_log_path}")
    
    finally:
        sftp.close()
        ssh.close()

def upload_logs_to_s3(local_log_dir, bucket_name, s3_path):
    """Upload logs to an S3 bucket."""
    s3_client = boto3.client('s3')
    for file_name in os.listdir(local_log_dir):
        local_file = os.path.join(local_log_dir, file_name)
        s3_key = os.path.join(s3_path, file_name)
        try:
            s3_client.upload_file(local_file, bucket_name, s3_key)
            print(f"Uploaded {local_file} to s3://{bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Error uploading {local_file}: {e}")

def analyze_logs(local_log_dir):
    """Perform basic analysis on log files."""
    error_counter = Counter()
    for file_name in os.listdir(local_log_dir):
        local_file = os.path.join(local_log_dir, file_name)
        with open(local_file, 'r') as file:
            for line in file:
                if "ERROR" in line:
                    error_counter[line.strip()] += 1

    print("Error Summary:")
    for error, count in error_counter.items():
        print(f"{error}: {count} occurrences")

if __name__ == "__main__":
    # Configuration
    SERVERS = [
        {'ip': '192.168.1.100', 'username': 'user1', 'key_file': '/path/to/key1.pem', 'logs': ['/var/log/app1.log']},
        {'ip': '192.168.1.101', 'username': 'user2', 'key_file': '/path/to/key2.pem', 'logs': ['/var/log/app2.log']}
    ]
    LOCAL_LOG_DIR = '/tmp/logs'
    BUCKET_NAME = 'your-s3-bucket-name'
    S3_PATH = 'logs/aggregated'

    # Ensure local directory exists
    if not os.path.exists(LOCAL_LOG_DIR):
        os.makedirs(LOCAL_LOG_DIR)

    # Download logs from each server
    for server in SERVERS:
        download_logs_from_server(
            server_ip=server['ip'],
            username=server['username'],
            key_file=server['key_file'],
            remote_log_paths=server['logs'],
            local_log_dir=LOCAL_LOG_DIR
        )

    # Upload logs to S3
    upload_logs_to_s3(LOCAL_LOG_DIR, BUCKET_NAME, S3_PATH)

    # Analyze logs
    analyze_logs(LOCAL_LOG_DIR)
