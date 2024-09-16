# Deployment Script

This Python script automates the deployment of a web application using AWS S3 and an EC2 instance. It consists of two main parts:
1. **Uploading files to an S3 bucket**
2. **Deploying files from S3 to an EC2 instance**

## Prerequisites

- Python 3.x
- `boto3` and `paramiko` libraries
- AWS credentials configured
- Access to an EC2 instance and an S3 bucket

## Installation

Install the required libraries using pip:

```bash
pip install boto3 paramiko
