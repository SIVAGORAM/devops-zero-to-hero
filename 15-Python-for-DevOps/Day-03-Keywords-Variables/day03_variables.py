#!/usr/bin/env python3

# ==========================================
# Day 03 Practice: Variables and Scope
# ==========================================

print("--- 1. Basic Variables ---")
name = "Siva"
age = 23
role = "DevOps Engineer"

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Role: {role}")


print("\n--- 2. Configuration Variables ---")
environment = "dev"
server_name = "web-server"
port = 8080

print(f"Environment: {environment}")
print(f"Server: {server_name}")
print(f"Port: {port}")


print("\n--- 3. Environment Decision Logic ---")
environment = "prod"  # Reassigning the variable

if environment == "prod":
    print("WARNING: Executing Production Deployment!")
else:
    print("Executing Non-production Deployment.")


print("\n--- 4. Local vs Global Scope ---")
# Global Variable
app_status = "ONLINE"

def deploy():
    # Local Variable
    target_server = "db-server"
    
    # We can read the global variable 'app_status' here
    print(f"Deploying to {target_server} while status is {app_status}")

deploy()

# If we tried to print(target_server) here, it would crash!
# print(target_server)  # NameError: name 'target_server' is not defined


print("\n--- 5. Mini Deployment Engine ---")
# Practice Challenge: Define your own variables to control a deployment
target_env = "uat"
target_port = 8443
is_https = True

print(f"Preparing deployment to {target_env}...")
if target_env in ["uat", "prod"]:
    if not is_https:
        print("ERROR: HTTPS must be enabled for UAT and PROD environments!")
    else:
        print(f"Deployment authorized. Target port: {target_port}")
else:
    print(f"Deployment authorized for Dev environment.")
