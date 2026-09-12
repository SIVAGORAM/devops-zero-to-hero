#!/usr/bin/env python3

# ==========================================
# Day 26 Practice: Boto3 AWS Automation
# Scenario: Cost Optimization & Artifact Deployment
# Features: Paginators, Waiters, ClientError Handling
# ==========================================

import os
import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

# Ensure a region is set, defaulting to ap-south-1 if missing
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")


def get_aws_client(service: str):
    """Safely instantiates a Boto3 client, checking for credentials."""
    try:
        # Boto3 automatically looks for env vars or ~/.aws/credentials
        client = boto3.client(service, region_name=AWS_REGION)
        # Force a simple call to validate credentials immediately
        if service == "sts":
            client.get_caller_identity()
        return client
    except NoCredentialsError:
        logging.critical("AWS Credentials not found! Please run 'aws configure' or set AWS_ACCESS_KEY_ID.")
        exit(1)
    except ClientError as e:
        logging.critical("AWS Error during client creation: %s", e)
        exit(1)


# ==========================================
# 1. EC2 COST OPTIMIZATION (Using Paginators & Waiters)
# ==========================================
def stop_development_instances():
    """
    Finds all EC2 instances tagged with Environment=dev that are currently running,
    stops them to save money, and uses a Waiter to ensure they stopped.
    """
    logging.info("--- Starting EC2 Cost Optimization Sweep ---")
    ec2 = get_aws_client("ec2")
    
    # We use a Paginator just in case we have thousands of instances
    paginator = ec2.get_paginator("describe_instances")
    
    # We filter purely via the AWS API rather than downloading all data to Python
    # This is much faster and more efficient!
    filters = [
        {"Name": "tag:Environment", "Values": ["dev"]},
        {"Name": "instance-state-name", "Values": ["running"]}
    ]
    
    instances_to_stop = []
    
    try:
        for page in paginator.paginate(Filters=filters):
            for reservation in page.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances_to_stop.append(instance["InstanceId"])
                    
        if not instances_to_stop:
            logging.info("No running 'dev' instances found. Cost optimization complete.")
            return

        logging.info("Found %s running 'dev' instances. Initiating shutdown...", len(instances_to_stop))
        
        # Issue the stop command
        ec2.stop_instances(InstanceIds=instances_to_stop)
        
        # Use a Waiter to pause the script until the AWS API confirms they are stopped
        logging.info("Waiting for instances to fully stop (this may take a minute)...")
        waiter = ec2.get_waiter("instance_stopped")
        waiter.wait(InstanceIds=instances_to_stop)
        
        logging.info("Successfully stopped instances: %s", instances_to_stop)

    except ClientError as e:
        logging.error("Failed to process EC2 instances: %s", e)


# ==========================================
# 2. S3 ARTIFACT DEPLOYMENT
# ==========================================
def upload_jenkins_artifact(local_file_path: str, bucket_name: str, s3_key: str):
    """Simulates a Jenkins pipeline uploading a build artifact to S3."""
    logging.info("--- Starting S3 Artifact Upload ---")
    s3 = get_aws_client("s3")
    
    if not os.path.exists(local_file_path):
        logging.error("Local file '%s' does not exist. Cannot upload.", local_file_path)
        return
        
    try:
        logging.info("Uploading %s to s3://%s/%s...", local_file_path, bucket_name, s3_key)
        s3.upload_file(local_file_path, bucket_name, s3_key)
        logging.info("Artifact upload successful!")
        
    except ClientError as e:
        # ClientError usually contains an AccessDenied (403) or NoSuchBucket (404)
        logging.error("AWS S3 Upload Failed: %s", e)


def main():
    # 0. Validate Authentication Identity first
    sts = get_aws_client("sts")
    identity = sts.get_caller_identity()
    logging.info("Authenticated as AWS IAM ARN: %s", identity['Arn'])

    # 1. Stop all dev instances (Cost saving cronjob script)
    stop_development_instances()
    
    # 2. Create a dummy artifact and upload it (CI/CD simulation)
    dummy_file = "dummy_build_artifact.zip"
    with open(dummy_file, "w") as f:
        f.write("Simulated compiled binaries.")
        
    # NOTE: You must change "my-devops-bucket-12345" to a bucket that actually exists in your account!
    upload_jenkins_artifact(dummy_file, "my-devops-bucket-12345", "releases/v1/dummy_build_artifact.zip")
    
    # Cleanup dummy file
    if os.path.exists(dummy_file):
        os.remove(dummy_file)

if __name__ == "__main__":
    main()
