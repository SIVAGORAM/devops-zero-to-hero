#!/usr/bin/env python3

# ==========================================
# Day 28 Practice: Python Docker Automation
# Scenario: Zero-Downtime Deployment & Monitoring
# Requirements: pip install docker
# ==========================================

import sys
import logging
import time

try:
    import docker
    from docker.errors import NotFound, APIError
except ImportError:
    print("FATAL: The 'docker' python package is not installed. Run: pip install docker")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

# Global Configuration
IMAGE_NAME = "nginx:alpine"
CONTAINER_NAME = "devops-nginx-server"

def get_docker_client():
    """Safely connects to the local Docker Engine."""
    try:
        client = docker.from_env()
        # Ping the engine to ensure it's actually running
        client.ping()
        return client
    except Exception as e:
        logging.critical("Could not connect to Docker Engine. Is Docker Desktop/Daemon running? Error: %s", e)
        sys.exit(1)

# ==========================================
# 1. DEPLOYMENT AUTOMATION
# ==========================================
def deploy_container():
    """
    Simulates a CI/CD deployment step: 
    1. Pulls the latest image
    2. Safely stops and removes the old container
    3. Boots the new container
    4. Verifies the health status
    """
    client = get_docker_client()
    logging.info("--- STARTING DEPLOYMENT PIPELINE ---")
    
    try:
        # Step 1: Pull the image
        logging.info("Pulling latest image: %s...", IMAGE_NAME)
        client.images.pull(IMAGE_NAME)
        
        # Step 2: Cleanup Old Container
        try:
            old_container = client.containers.get(CONTAINER_NAME)
            logging.info("Found existing container '%s'. Initiating graceful shutdown...", CONTAINER_NAME)
            
            if old_container.status == "running":
                old_container.stop(timeout=10)
                logging.info("Container stopped.")
                
            old_container.remove()
            logging.info("Old container removed.")
            
        except NotFound:
            logging.info("No existing container found. Proceeding to fresh deployment.")
            
        # Step 3: Boot New Container
        logging.info("Booting new container from image %s...", IMAGE_NAME)
        
        # detach=True runs it in the background (like 'docker run -d')
        new_container = client.containers.run(
            IMAGE_NAME,
            name=CONTAINER_NAME,
            detach=True,
            ports={'80/tcp': 8080} # Expose port 80 to localhost:8080
        )
        
        # Step 4: Verification
        logging.info("Waiting 3 seconds for boot sequence...")
        time.sleep(3)
        
        # We must reload the container object to get the updated status from the Engine
        new_container.reload()
        
        if new_container.status == "running":
            logging.info("DEPLOYMENT SUCCESSFUL! Container ID: %s", new_container.short_id)
            logging.info("Test it by opening: http://localhost:8080")
        else:
            logging.error("DEPLOYMENT FAILED! Container is in state: %s", new_container.status)
            
    except APIError as e:
        logging.error("Docker API Error during deployment: %s", e)

# ==========================================
# 2. MONITORING AUTOMATION
# ==========================================
def monitor_and_revive():
    """Scans all containers. If our app crashed, it restarts it."""
    client = get_docker_client()
    logging.info("\n--- STARTING CONTAINER HEALTH SWEEP ---")
    
    # all=True ensures we see stopped/crashed containers
    containers = client.containers.list(all=True)
    
    found = False
    for container in containers:
        if container.name == CONTAINER_NAME:
            found = True
            if container.status == "exited":
                logging.warning("CRITICAL ALERT: %s has crashed (exited)! Attempting revival...", CONTAINER_NAME)
                try:
                    container.restart()
                    logging.info("Container successfully revived.")
                except APIError as e:
                    logging.error("Failed to restart container: %s", e)
            elif container.status == "running":
                logging.info("Health Check Passed: %s is running optimally.", CONTAINER_NAME)
            else:
                logging.warning("Unknown state for %s: %s", CONTAINER_NAME, container.status)
                
    if not found:
        logging.warning("Target container '%s' was not found on this host.", CONTAINER_NAME)

def main():
    if len(sys.argv) < 2:
        print("Usage: python day28_docker_automation.py [command]")
        print("Commands:")
        print("  deploy   - Pulls image, stops old container, boots new one")
        print("  monitor  - Scans for the container and restarts it if crashed")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    
    if command == "deploy":
        deploy_container()
    elif command == "monitor":
        monitor_and_revive()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
