#!/usr/bin/env python3

import os
import argparse
from dotenv import load_dotenv

# ==========================================
# DevOps Deployment Script using Argparse & Dotenv
# ==========================================

# 1. Load local environment variables from a .env file (if it exists)
# In production (Jenkins/Docker), this fails silently and uses the real system env vars.
load_dotenv()

def main():
    # 2. Setup the Command Line Argument Parser
    parser = argparse.ArgumentParser(description="DevOps Application Deployment Script")
    
    parser.add_argument("--environment", 
                        choices=['dev', 'test', 'prod'], 
                        required=True, 
                        help="The target deployment environment.")
                        
    parser.add_argument("--version", 
                        required=True, 
                        help="The version tag of the application to deploy (e.g. 1.0.5).")
                        
    parser.add_argument("--dry-run", 
                        action='store_true', 
                        help="Simulate the deployment without making actual changes.")

    # Parse the arguments provided by the user
    args = parser.parse_args()

    print("--- Initialization ---")
    print(f"Target Environment: {args.environment.upper()}")
    print(f"Target Version: {args.version}")
    
    if args.dry_run:
        print("\n[!] DRY RUN MODE ACTIVATED - No changes will be made.")

    # 3. Read Secure Configuration from Environment Variables
    # We use os.getenv() for optional config, and os.environ[] for mandatory secrets.
    print("\n--- Validating Configuration ---")
    
    aws_region = os.getenv("AWS_REGION", "us-east-1") # Defaults to us-east-1 if missing
    print(f"AWS Region set to: {aws_region}")
    
    try:
        # We use os.environ to FORCE a crash if the secret is missing.
        # This prevents us from deploying with broken credentials!
        db_password = os.environ["DB_PASSWORD"]
        print("Database credentials found and loaded securely.")
    except KeyError:
        print("[ERROR] Fatal: DB_PASSWORD environment variable is missing!")
        print("Please export DB_PASSWORD or add it to your .env file.")
        exit(1)

    # 4. Execute Mock Deployment
    print("\n--- Executing Deployment ---")
    print(f"Deploying v{args.version} to {args.environment} infrastructure in {aws_region}...")
    
    if args.dry_run:
        print("[SUCCESS] Dry run complete. Deployment simulated perfectly.")
    else:
        print("[SUCCESS] Application deployed successfully!")

if __name__ == "__main__":
    main()
