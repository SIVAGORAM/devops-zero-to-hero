#!/usr/bin/env python3

# ==========================================
# Day 22 Practice: Advanced Logging
# Scenario: DevOps Deployment Pipeline
# Features: Handlers, Rotation, Exceptions
# ==========================================

import logging
from logging.handlers import RotatingFileHandler
import time

# ---------------------------------------------------------
# 1. CONFIGURE ADVANCED LOGGING
# ---------------------------------------------------------
def setup_logger():
    """Configures a logger that outputs to both Console and a Rotating File."""
    
    # Create a custom logger tied to this specific module name
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG) # Catch everything

    # Define the log structure
    formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s - %(message)s")

    # Handler 1: Console Output (Terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # Only show INFO and above in terminal
    console_handler.setFormatter(formatter)

    # Handler 2: File Output with Rotation (Prevents disk exhaustion)
    # Max size ~10KB (very small for demo purposes), keep 3 backups
    file_handler = RotatingFileHandler(
        "deployment.log", 
        maxBytes=10000, 
        backupCount=3
    )
    file_handler.setLevel(logging.DEBUG) # Save EVERYTHING to the file
    file_handler.setFormatter(formatter)

    # Attach both handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Initialize our global logger
log = setup_logger()

# ---------------------------------------------------------
# 2. DEPLOYMENT AUTOMATION
# ---------------------------------------------------------
def deploy_application(app_name: str, environment: str):
    
    # We use %s to inject variables safely into log messages
    log.info("Initiating deployment pipeline | App: %s | Env: %s", app_name, environment)
    
    try:
        log.debug("Authenticating with AWS... (This won't show in terminal, only file!)")
        time.sleep(1)
        
        log.info("Stopping existing application instances...")
        time.sleep(1)
        
        log.info("Copying new application binaries...")
        time.sleep(1)
        
        # Simulating a sudden failure during deployment!
        log.warning("Detected low memory during copy operation. Proceeding anyway...")
        time.sleep(1)
        
        # Simulating a crash
        raise ConnectionError(f"Failed to connect to the database in {environment}")
        
        # This will never be reached
        log.info("Deployment completed successfully!")
        
    except Exception as e:
        # logging.exception automatically captures the Stack Trace!
        # This is CRITICAL for debugging production failures.
        log.exception("FATAL ERROR: Deployment pipeline collapsed!")


def main():
    deploy_application("Payment-API-v2", "Production")
    
    # To test Log Rotation, let's spam the log file
    log.info("Spamming logs to trigger file rotation...")
    for i in range(150):
        log.debug("Spam message number %s to fill up the log file...", i)
        
    log.info("Check your directory. You should see deployment.log, deployment.log.1, etc!")

if __name__ == "__main__":
    main()
