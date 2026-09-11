#!/usr/bin/env python3

# ==========================================
# Day 18 Practice: Advanced Functions
# Scenario: Automated Deployment Workflow
# Features: *args, **kwargs, Decorators, Type Hints
# ==========================================

import time
from functools import wraps

# ---------------------------------------------------------
# 1. DECORATORS
# ---------------------------------------------------------

def logger(func):
    """Decorator that logs the start and end of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n[INFO] Starting {func.__name__.upper()} operation...")
        result = func(*args, **kwargs)
        print(f"[INFO] {func.__name__.upper()} operation completed successfully.")
        return result
    return wrapper


def retry(func):
    """Decorator that automatically retries a function up to 3 times if it fails."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"[WARNING] Attempt {attempt} failed: {e}")
                if attempt == max_attempts:
                    print(f"[FATAL] Max retries reached. Aborting.")
                    raise
                print("[INFO] Retrying in 1 second...")
                time.sleep(1)
    return wrapper

# ---------------------------------------------------------
# 2. CORE FUNCTIONS
# ---------------------------------------------------------

# Applying both decorators! 
# It will Log the operation, and if it fails, it will Retry.
@logger
@retry
def deploy_application(application: str, environment: str, *servers, **config) -> bool:
    """
    Simulates deploying an application to multiple servers using advanced arguments.
    
    application: Positional string
    environment: Positional string
    *servers: Captures any number of server names as a Tuple
    **config: Captures any extra key=value arguments as a Dictionary
    """
    
    print(f"Deploying App: {application}")
    print(f"Target Environment: {environment}")
    
    # 1. Processing *args (Tuple)
    print("\nTarget Servers:")
    if not servers:
        print("  No servers provided!")
        raise ValueError("Deployment failed: No target servers.")
    
    for server in servers:
        print(f"  -> {server}")
        
    # 2. Processing **kwargs (Dictionary)
    print("\nDeployment Configuration:")
    for key, value in config.items():
        print(f"  {key.upper()}: {value}")
        
    return True

# ---------------------------------------------------------
# 3. EXECUTION
# ---------------------------------------------------------

def main():
    print("=== DEPLOYMENT PIPELINE INITIATED ===")
    
    # We pass the application and environment positionally.
    # We pass 3 servers, which get packed into *servers (Tuple).
    # We pass version and replicas as named parameters, which get packed into **config (Dict).
    
    deploy_application(
        "Payment-API",          # application
        "Production",           # environment
        "web-01",               # *servers
        "web-02",               # *servers
        "web-03",               # *servers
        version="v2.1.0",       # **config
        replicas=3              # **config
    )
    
    print("=== PIPELINE FINISHED ===")

if __name__ == "__main__":
    main()
