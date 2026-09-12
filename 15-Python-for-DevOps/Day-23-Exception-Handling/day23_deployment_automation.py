#!/usr/bin/env python3

# ==========================================
# Day 23 Practice: Advanced Exception Handling
# Scenario: Server Deployment Automation
# Features: Custom Exceptions, Validation, Retry
# ==========================================

import logging
import subprocess
import time
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)

# ---------------------------------------------------------
# 1. CUSTOM EXCEPTIONS
# ---------------------------------------------------------
class DeploymentError(Exception):
    """Raised when a deployment step fails."""
    pass

class ConfigurationError(Exception):
    """Raised when configuration validation fails."""
    pass

# ---------------------------------------------------------
# 2. VALIDATION (FAIL FAST)
# ---------------------------------------------------------
def validate_environment(environment: str):
    """Fails immediately if the environment is invalid."""
    allowed = ["dev", "staging", "production"]
    if environment not in allowed:
        # Manually raise our custom error
        raise ConfigurationError(f"Environment '{environment}' is not allowed!")
    logging.info("Environment validation successful.")

def check_configuration():
    """Checks if the required config file exists."""
    config_file = Path("server.conf")
    if not config_file.exists():
        # Using a built-in Python exception
        raise FileNotFoundError(f"Missing required configuration file: {config_file.absolute()}")
    logging.info("Configuration file located.")

# ---------------------------------------------------------
# 3. OPERATION WITH RETRY LOGIC
# ---------------------------------------------------------
def restart_service_with_retry(service_name: str, max_retries: int = 3):
    """Attempts to restart a service using subprocess, with retry logic."""
    for attempt in range(max_retries):
        try:
            logging.info("Attempting to restart %s (Attempt %s/%s)...", service_name, attempt + 1, max_retries)
            # In a real scenario, this would be: ["sudo", "systemctl", "restart", service_name]
            # We use a dummy command here that will intentionally fail to demonstrate the retry logic!
            subprocess.run(["invalid_command_to_force_failure", service_name], check=True, capture_output=True)
            
            logging.info("%s restarted successfully!", service_name)
            return # Break out of function if successful
            
        except FileNotFoundError as e:
            # Command not found on the OS
            logging.error("The command does not exist on this OS: %s", e)
            raise DeploymentError(f"Cannot restart {service_name} due to missing OS command.") from e
            
        except subprocess.CalledProcessError as e:
            # Command executed but returned a non-zero exit code
            logging.warning("Failed to restart %s. Exit Code: %s", service_name, e.returncode)
            if attempt < max_retries - 1:
                logging.info("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                # Exception Chaining: Link our custom error to the original CalledProcessError
                raise DeploymentError(f"Failed to restart {service_name} after {max_retries} attempts.") from e

# ---------------------------------------------------------
# 4. MASTER DEPLOYMENT CONTROLLER (TRY/EXCEPT/ELSE/FINALLY)
# ---------------------------------------------------------
def deploy(environment: str):
    logging.info("--- DEPLOYMENT STARTED (%s) ---", environment.upper())
    
    try:
        # Step 1: Validate
        validate_environment(environment)
        
        # Step 2: Pre-flight checks
        # Let's create a dummy file so this passes, so we can see the retry logic fail later.
        Path("server.conf").touch()
        check_configuration()
        
        # Step 3: Execute dangerous operation
        restart_service_with_retry("nginx")
        
    except ConfigurationError as ce:
        logging.error("PRE-FLIGHT FAILURE: %s", ce)
        
    except FileNotFoundError as fnfe:
        logging.error("FILESYSTEM FAILURE: %s", fnfe)
        
    except DeploymentError as de:
        # We use logging.exception here to print the full Stack Trace so we can see the Exception Chain!
        logging.exception("FATAL PIPELINE CRASH: %s", de)
        
    else:
        # ONLY RUNS IF NO EXCEPTIONS WERE RAISED IN THE TRY BLOCK!
        logging.info("Deployment verified. Routing traffic to new instances!")
        
    finally:
        # RUNS 100% OF THE TIME! Clean up our temporary test file.
        logging.info("Initiating mandatory post-deployment cleanup...")
        tmp_config = Path("server.conf")
        if tmp_config.exists():
            tmp_config.unlink()
            logging.info("Cleaned up temporary configuration file.")
        logging.info("--- DEPLOYMENT PIPELINE TERMINATED ---\n")

def main():
    # 1. Test Fail Fast (Invalid Environment)
    deploy("local")
    
    # 2. Test Retry Logic & Exception Chaining (Valid Environment, but subprocess fails)
    deploy("production")

if __name__ == "__main__":
    main()
