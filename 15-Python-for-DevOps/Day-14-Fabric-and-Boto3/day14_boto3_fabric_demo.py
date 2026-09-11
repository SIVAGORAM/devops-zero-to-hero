#!/usr/bin/env python3

"""
==========================================
Day 14 Project: Advanced DevOps Automation
Scenario: Dynamic AWS Deployment Script
==========================================
Note: This is an architectural template. 
To run it, you would need 'pip install fabric boto3' 
and valid AWS Credentials.
"""

try:
    import boto3
    from fabric import Connection
except ImportError:
    print("Dependencies missing! Run: pip install fabric boto3")

def get_ec2_instances():
    """
    Step 1: Use Boto3 to talk to AWS and find our servers.
    """
    print("[BOTO3] Contacting AWS API to find running EC2 instances...")
    
    # In a real script, this connects to AWS EC2
    # ec2 = boto3.client('ec2', region_name='us-east-1')
    
    # Mocking the AWS API Response
    running_ips = ["10.0.0.51", "10.0.0.52"]
    print(f"[BOTO3] Found {len(running_ips)} active instances: {running_ips}")
    return running_ips


def deploy_application(ip_address):
    """
    Step 2: Use Fabric to SSH into the specific IP and run commands.
    """
    print(f"\n[FABRIC] Initiating SSH connection to ubuntu@{ip_address}...")
    
    try:
        # 1. Establish connection (Requires SSH keys configured on your machine)
        # c = Connection(f"ubuntu@{ip_address}")
        
        print(f"[FABRIC] Connected! Executing deployment commands on {ip_address}:")
        
        # 2. Run remote Linux commands
        print(" -> c.run('mkdir -p /opt/myapp')")
        print(" -> c.run('git clone https://github.com/myrepo/app.git /opt/myapp')")
        print(" -> c.run('pip3 install -r /opt/myapp/requirements.txt')")
        print(" -> c.run('systemctl restart myapp.service')")
        
        print(f"[SUCCESS] Application deployed on {ip_address}!")
        
    except Exception as e:
        print(f"[ERROR] Failed to deploy to {ip_address}: {e}")


def main():
    print("=== STARTING CLOUD DEPLOYMENT PIPELINE ===\n")
    
    # 1. Get infrastructure state from Boto3
    target_servers = get_ec2_instances()
    
    # 2. Deploy to each server using Fabric
    for ip in target_servers:
        deploy_application(ip)
        
    print("\n=== PIPELINE COMPLETE ===")

if __name__ == "__main__":
    # We only run the pipeline if executed directly
    main()
