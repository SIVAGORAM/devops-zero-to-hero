#!/usr/bin/env python3

# ==========================================
# Day 19 Practice: JSON & YAML Operations
# Scenario: DevOps Configuration Converter
# ==========================================
# Note: Requires `pip install pyyaml`

import os
import json

try:
    import yaml
except ImportError:
    print("[FATAL] PyYAML is not installed. Please run: pip install pyyaml")
    exit(1)

def main():
    json_filepath = "server.json"
    yaml_filepath = "server.yaml"
    
    print(f"--- 1. Loading JSON Configuration from {json_filepath} ---")
    try:
        with open(json_filepath, "r") as file:
            # json.load() (NOT loads!) because we are reading from a File
            config = json.load(file)
            print("[SUCCESS] JSON Loaded!")
            
    except FileNotFoundError:
        print(f"[FATAL] Could not find {json_filepath}.")
        return
    except json.JSONDecodeError as e:
        print(f"[FATAL] Invalid JSON formatting in {json_filepath}: {e}")
        return

    print("\n--- 2. Validating Configuration ---")
    # A DevOps engineer always validates config before using it
    if "database" not in config:
        print("[FATAL] Validation failed: Missing 'database' configuration.")
        return
    if "environment" not in config:
        print("[FATAL] Validation failed: Missing 'environment' configuration.")
        return
    print("[SUCCESS] Configuration is valid!")

    print("\n--- 3. Injecting Secrets securely ---")
    # We never store passwords in JSON/YAML. We inject them via Env Vars!
    # For this demo, we provide a default fallback.
    db_password = os.getenv("DB_PASSWORD", "SuperSecretInjectedPassword123!")
    config["database"]["password"] = db_password
    print("[SUCCESS] Environment variables injected into configuration.")

    print(f"\n--- 4. Converting and Saving as YAML to {yaml_filepath} ---")
    try:
        with open(yaml_filepath, "w") as file:
            # default_flow_style=False ensures it looks like standard human-readable YAML
            yaml.safe_dump(config, file, default_flow_style=False)
            print(f"[SUCCESS] YAML file generated successfully!")
    except Exception as e:
        print(f"[FATAL] Failed to write YAML: {e}")
        
    print("\n=== PIPELINE COMPLETE ===")

if __name__ == "__main__":
    main()
