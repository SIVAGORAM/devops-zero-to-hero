#!/usr/bin/env python3

# ==========================================
# Day 07 Practice: Conditional Handling
# ==========================================

print("--- Exercise 1: Number Check ---")
number = 10

if number > 0:
    print(f"{number} is Positive")
elif number < 0:
    print(f"{number} is Negative")
else:
    print("The number is Zero")


print("\n--- Exercise 2: Environment Router ---")
environment = "staging"
print(f"Target Environment: {environment}")

if environment == "production":
    print("Action: Applying strict production security group rules.")
elif environment == "staging":
    print("Action: Applying staging testing rules.")
elif environment == "development":
    print("Action: Allowing local developer access.")
else:
    print("Error: Unknown environment.")


print("\n--- Exercise 3: Server Health Check ---")
cpu_usage = 85
memory_usage = 60
print(f"CPU: {cpu_usage}% | RAM: {memory_usage}%")

if cpu_usage > 80 and memory_usage > 80:
    print("Status: CRITICAL - Both CPU and RAM are maxed out!")
elif cpu_usage > 80:
    print("Status: WARNING - High CPU Usage.")
elif memory_usage > 80:
    print("Status: WARNING - High Memory Usage.")
else:
    print("Status: OK - Server is healthy.")


print("\n--- Exercise 4: CI/CD Deployment Logic (Nested IFs) ---")
environment = "production"
build_status = "success"
print(f"Pipeline State -> Build: {build_status} | Env: {environment}")

if build_status == "success":
    if environment == "production":
        print("Decision: Deploying to Production 🚀")
    else:
        print("Decision: Deploying to Non-Production 🛠️")
else:
    print("Decision: Build failed. Halting deployment 🛑")


print("\n--- Exercise 5: Disk Monitoring Thresholds ---")
disk_usage = 92
print(f"Disk Usage: {disk_usage}%")

# Notice the order! We must check >= 90 FIRST. 
# If we checked >= 80 first, 92 would match that and stop checking!
if disk_usage >= 90:
    print("Alert: CRITICAL - Disk usage is dangerously high. Expanding volume.")
elif disk_usage >= 80:
    print("Alert: WARNING - Disk usage is getting high. Triggering cleanup.")
else:
    print("Alert: OK - Disk usage is normal.")
