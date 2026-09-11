#!/usr/bin/env python3

# ==========================================
# Day 17 Practice: Advanced Lists & Dicts
# Scenario: DevOps Server Inventory Manager
# ==========================================

def main():
    # Simulated API Response from AWS or Kubernetes
    servers = [
        {"name": "web01", "ip": "10.0.0.10", "status": "running", "env": "prod", "cpu": 85},
        {"name": "web02", "ip": "10.0.0.11", "status": "stopped", "env": "prod", "cpu": 0},
        {"name": "web03", "ip": "10.0.0.12", "status": "running", "env": "dev", "cpu": 40},
        {"name": "db01",  "ip": "10.0.0.20", "status": "running", "env": "prod", "cpu": 92}
    ]

    print("--- 1. All Server Names ---")
    # List comprehension extracting just the names
    names = [s["name"] for s in servers]
    print(names)


    print("\n--- 2. Running Production Servers ---")
    # List comprehension with multiple conditions
    running_prod = [
        s["name"] for s in servers 
        if s["env"] == "prod" and s["status"] == "running"
    ]
    print(running_prod)


    print("\n--- 3. High CPU Alerts (>80%) ---")
    high_cpu = [s["name"] for s in servers if s.get("cpu", 0) > 80]
    print(high_cpu)


    print("\n--- 4. Status Counting ---")
    # Using a dictionary to tally up statuses
    status_count = {}
    for server in servers:
        status = server["status"]
        # .get(status, 0) defaults to 0 if the key doesn't exist yet
        status_count[status] = status_count.get(status, 0) + 1
    print(status_count)


    print("\n--- 5. Build Fast Lookup Map ---")
    # Converting a List of Dictionaries into a Dictionary of Dictionaries
    server_map = {s["name"]: s for s in servers}
    
    # Now we can do O(1) instant lookups without looping!
    print("Looking up 'web02':")
    print(server_map.get("web02", "Server not found"))

if __name__ == "__main__":
    main()
