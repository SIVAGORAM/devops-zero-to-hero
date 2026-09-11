#!/usr/bin/env python3

import time

# ==========================================
# Day 10 Practice: Loops and Control Statements
# ==========================================

print("--- Exercise 1: Standard Server Loop ---")
servers = ["web-01", "web-02", "db-01", "app-01"]

for server in servers:
    print(f"[Provisioning] Standing up {server}...")


print("\n--- Exercise 2: Searching with 'break' ---")
# We want to find the DB and stop looking to save time.
for server in servers:
    print(f"Scanning {server}...")
    if server == "db-01":
        print("--> TARGET FOUND: db-01. Halting scan.")
        break


print("\n--- Exercise 3: Skipping with 'continue' ---")
# We want to patch all servers EXCEPT the database.
for server in servers:
    if server == "db-01":
        print(f"--> SKIPPING: {server} (Database patching requires manual approval).")
        continue
    print(f"Applying OS patches to {server}...")


print("\n--- Exercise 4: While Loop (API Polling Simulation) ---")
# Simulating a health check that waits for a service to come online
max_attempts = 5
current_attempt = 1
service_is_ready = False

print("Waiting for API to become ready...")
while current_attempt <= max_attempts:
    print(f"Attempt {current_attempt}/{max_attempts}...")
    
    # Mocking a successful connection on the 3rd attempt
    if current_attempt == 3:
        service_is_ready = True
        print("Success! API is online.")
        break
        
    current_attempt += 1
    time.sleep(0.5) # Pauses the script for half a second

if not service_is_ready:
    print("FATAL: API failed to start after 5 attempts.")


print("\n--- Exercise 5: DevOps Log Analysis ---")
log_file = [
    "INFO: Server started securely.",
    "ERROR: Disk space critically low on web-02!",
    "INFO: Backup routine completed.",
    "DEBUG: User logged in.",
    "ERROR: Database connection timeout.",
    "INFO: Deployment successful."
]

error_count = 0

print("Scanning log file for errors...")
for line in log_file:
    # If the line does NOT contain "ERROR", skip it immediately
    if "ERROR" not in line:
        continue
    
    # We only reach this point if the line has an ERROR
    print(f"--> ALERT: {line}")
    error_count += 1

print(f"Log scan complete. Total errors found: {error_count}")
