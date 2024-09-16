# Complete the following steps before running the script: 
# 1. pip install -r requirements.txt
# 2. aws configure

import boto3
import paramiko
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def upload_to_s3(local_path, bucket_name, s3_path):
    """Uploads files to S3 bucket."""
    s3_client = boto3.client('s3')
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file = os.path.join(root, file)
            s3_key = os.path.join(s3_path, os.path.relpath(local_file, local_path))
            try:
                s3_client.upload_file(local_file, bucket_name, s3_key)
                print(f"Uploaded {local_file} to s3://{bucket_name}/{s3_key}")
            except FileNotFoundError:
                print(f"File {local_file} not found")
            except NoCredentialsError:
                print("Credentials not available")
            except PartialCredentialsError:
                print("Incomplete credentials provided")
            except Exception as e:
                print(f"Error uploading {local_file}: {e}")

def deploy_from_s3_to_ec2(bucket_name, s3_path, remote_path, server_ip, username, key_file):
    """Downloads files from S3 and deploys them to EC2."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_ip, username=username, key_filename=key_file)
    
    sftp = ssh.open_sftp()
    try:
        # Download files from S3 to EC2 instance
        s3 = boto3.client('s3')
        s3_objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_path)
        if 'Contents' in s3_objects:
            for obj in s3_objects['Contents']:
                s3_key = obj['Key']
                local_file = os.path.join('/tmp', os.path.basename(s3_key))
                remote_file = os.path.join(remote_path, os.path.basename(s3_key))
                
                # Download from S3 to local temp directory
                s3.download_file(bucket_name, s3_key, local_file)
                sftp.put(local_file, remote_file)
                print(f"Deployed {local_file} to {remote_file}")

        # Restart the server
        print("Restarting the server...")
        stdin, stdout, stderr = ssh.exec_command('sudo systemctl restart my-web-app.service')
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # Check deployment status
        print("Checking deployment status...")
        stdin, stdout, stderr = ssh.exec_command('systemctl status my-web-app.service')
        print(stdout.read().decode())
        print(stderr.read().decode())
    
    finally:
        sftp.close()
        ssh.close()

if __name__ == "__main__":
    # Configuration
    LOCAL_PATH = '/path/to/local/app'
    BUCKET_NAME = 'your-s3-bucket-name'
    S3_PATH = 'deployments/app'
    REMOTE_PATH = '/path/to/remote/app'
    SERVER_IP = '192.168.1.100'
    USERNAME = 'ec2-user'
    KEY_FILE = '/path/to/your/private-key.pem'
    
    # Upload to S3
    upload_to_s3(LOCAL_PATH, BUCKET_NAME, S3_PATH)
    
    # Deploy from S3 to EC2
    deploy_from_s3_to_ec2(BUCKET_NAME, S3_PATH, REMOTE_PATH, SERVER_IP, USERNAME, KEY_FILE)
