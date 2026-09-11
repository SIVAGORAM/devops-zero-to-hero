#!/usr/bin/env python3

# ==========================================
# Day 08 & 09 Practice: Lists, Tuples, and Iteration
# ==========================================

print("--- 1. List Creation & Indexing ---")
servers = ["web-01", "web-02", "db-01", "app-01"]
print("Initial Servers:", servers)
print(f"First Server: {servers[0]}")
print(f"Last Server: {servers[-1]}")
print(f"Total Servers: {len(servers)}")

print("\n--- 2. Adding Elements ---")
servers.append("cache-01")  # Add to end
print("After append('cache-01'):", servers)

servers.insert(0, "load-balancer")  # Add to beginning
print("After insert(0, 'load-balancer'):", servers)

new_nodes = ["worker-01", "worker-02"]
servers.extend(new_nodes)  # Merge lists
print("After extend(new_nodes):", servers)

print("\n--- 3. Removing Elements ---")
servers.remove("web-02")  # Remove by value
print("After remove('web-02'):", servers)

crashed_node = servers.pop(-1)  # Remove by index (last item)
print(f"Node '{crashed_node}' was popped from the cluster.")
print("Current Servers:", servers)

print("\n--- 4. Searching & Sorting ---")
db_index = servers.index("db-01")
print(f"'db-01' is located at index: {db_index}")

servers.sort()
print("Alphabetically Sorted Servers:", servers)

print("\n--- 5. Tuple Packing & Unpacking ---")
# Tuples are immutable, great for fixed configuration
db_config = ("postgresql", 5432, "admin")
engine, port, user = db_config  # Unpacking!
print(f"DB Engine: {engine} | Port: {port} | User: {user}")

print("\n--- 6. DevOps Automation: The For Loop ---")
# This is how you automate tasks across multiple servers!
for server in servers:
    if server.startswith("web"):
        print(f"[Deploy] Updating Nginx configuration on {server}...")
    elif server.startswith("db"):
        print(f"[Backup] Running pg_dump on {server}...")
    else:
        print(f"[Skip] No specific actions defined for {server}.")

print("\n--- Automation Pipeline Complete ---")
