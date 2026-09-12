#!/usr/bin/env python3

# ==========================================
# Day 27 Practice: AWS EC2 + S3 Automation
# Scenario: Complete AWS Infrastructure CLI
# Features: EC2 Inventory, Safe State Management, S3 Backups
# ==========================================

import os
import sys
import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

logging.basicConfig(level=logging.INFO, format="%(message)s")

# Global AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

def get_client(service: str):
    """Safely retrieves a boto3 client."""
    try:
        return boto3.client(service, region_name=AWS_REGION)
    except NoCredentialsError:
        logging.error("FATAL: No AWS credentials found.")
        sys.exit(1)

# ==========================================
# 1. EC2 INVENTORY
# ==========================================
def inventory_instances():
    """Extracts exactly what we need from the massive EC2 dictionary."""
    ec2 = get_client("ec2")
    logging.info("\n--- AWS EC2 INVENTORY ---")
    
    try:
        # Use Paginator to handle hundreds of instances
        paginator = ec2.get_paginator("describe_instances")
        
        print(f"{'NAME':<20} | {'INSTANCE ID':<20} | {'STATE':<10} | {'PRIVATE IP':<15} | {'PUBLIC IP'}")
        print("-" * 90)
        
        for page in paginator.paginate():
            for reservation in page.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    
                    # 1. Safely get Name Tag
                    name = "Unnamed"
                    for tag in instance.get("Tags", []):
                        if tag["Key"] == "Name":
                            name = tag["Value"]
                            
                    # 2. Extract core fields
                    i_id = instance["InstanceId"]
                    state = instance["State"]["Name"]
                    
                    # 3. Safely get IPs (Stopped instances have no public IP)
                    private_ip = instance.get("PrivateIpAddress", "N/A")
                    public_ip = instance.get("PublicIpAddress", "N/A")
                    
                    print(f"{name:<20} | {i_id:<20} | {state:<10} | {private_ip:<15} | {public_ip}")
                    
        print("\n")
    except ClientError as e:
        logging.error("Failed to describe EC2 instances: %s", e)

# ==========================================
# 2. SAFE EC2 AUTOMATION
# ==========================================
def stop_development_instances():
    """Finds running Dev instances and safely stops them."""
    ec2 = get_client("ec2")
    logging.info("\n--- COST OPTIMIZATION: STOPPING DEV INSTANCES ---")
    
    # Server-side Filtering!
    filters = [
        {"Name": "tag:Environment", "Values": ["dev"]},
        {"Name": "instance-state-name", "Values": ["running"]}
    ]
    
    try:
        response = ec2.describe_instances(Filters=filters)
        targets = []
        
        for res in response["Reservations"]:
            for inst in res["Instances"]:
                targets.append(inst["InstanceId"])
                
        if not targets:
            logging.info("No running development instances found. All good!")
            return
            
        logging.info("Found %s running dev instances: %s", len(targets), targets)
        
        # Safe Automation: Ask for confirmation before destruction/modification!
        confirm = input("Are you sure you want to stop these instances? (y/n): ")
        if confirm.lower() == 'y':
            ec2.stop_instances(InstanceIds=targets)
            logging.info("Stop command issued successfully.")
        else:
            logging.info("Operation aborted by user.")
            
    except ClientError as e:
        logging.error("Failed to modify instances: %s", e)

# ==========================================
# 3. S3 LOG BACKUP AUTOMATION
# ==========================================
def backup_directory_to_s3(local_dir: str, bucket_name: str, s3_prefix: str):
    """Uploads an entire local directory of logs to an S3 bucket."""
    s3 = get_client("s3")
    logging.info(f"\n--- BACKING UP {local_dir} TO s3://{bucket_name}/{s3_prefix} ---")
    
    if not os.path.exists(local_dir):
        logging.error(f"Local directory '{local_dir}' does not exist.")
        return
        
    try:
        for file_name in os.listdir(local_dir):
            file_path = os.path.join(local_dir, file_name)
            
            # Skip subdirectories
            if os.path.isfile(file_path):
                s3_key = f"{s3_prefix}/{file_name}"
                logging.info("Uploading %s...", file_name)
                s3.upload_file(file_path, bucket_name, s3_key)
                
        logging.info("Backup completed successfully!")
    except ClientError as e:
        logging.error("S3 Upload Failed: %s", e)

# ==========================================
# CLI ROUTER
# ==========================================
def main():
    if len(sys.argv) < 2:
        print("Usage: python day27_aws_infrastructure_manager.py [command]")
        print("Commands:")
        print("  inventory    - Lists all EC2 instances in a table")
        print("  stop-dev     - Finds and stops all running Environment=dev instances")
        print("  backup       - Simulates backing up a local directory to S3")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    
    # 0. Validate Auth
    get_client("sts").get_caller_identity()
    
    if command == "inventory":
        inventory_instances()
        
    elif command == "stop-dev":
        stop_development_instances()
        
    elif command == "backup":
        # Create dummy log directory for testing
        os.makedirs("dummy_logs", exist_ok=True)
        with open("dummy_logs/app.log", "w") as f: f.write("INFO: App booted.")
        with open("dummy_logs/error.log", "w") as f: f.write("ERROR: DB disconnected.")
        
        # YOU MUST CHANGE THIS BUCKET NAME TO ONE THAT YOU OWN
        backup_directory_to_s3("dummy_logs", "my-devops-backup-bucket-123", "server-logs")
        
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
