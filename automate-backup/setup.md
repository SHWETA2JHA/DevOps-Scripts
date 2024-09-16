# Automated Backup Script

This Python script automates the process of backing up a directory to an Amazon S3 bucket. It includes functionality for compressing a directory into a ZIP file, uploading it to S3, and optionally deleting old backups.

## Prerequisites

- Python 3.x
- `boto3` library
- AWS credentials configured

## Installation

Install the required library using pip:

```bash
pip install boto3
