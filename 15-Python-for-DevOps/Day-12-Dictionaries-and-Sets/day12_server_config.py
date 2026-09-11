#!/usr/bin/env python3

# ==========================================
# Day 12 Practice: Dictionaries & Sets
# Scenario: Server Configuration Management
# ==========================================

print("--- 1. Nested Dictionary Setup ---")
server_config = {
    'server1': {'ip': '192.168.1.1', 'port': 8080, 'status': 'active'},
    'server2': {'ip': '192.168.1.2', 'port': 8000, 'status': 'inactive'},
    'server3': {'ip': '192.168.1.3', 'port': 9000, 'status': 'active'}
}

print(f"Total Servers Configured: {len(server_config)}")

print("\n--- 2. Dictionary Iteration ---")
for server_name, config in server_config.items():
    print(f"{server_name} is currently [{config['status'].upper()}] on IP {config['ip']}")


print("\n--- 3. Safe Retrieval using .get() ---")
def get_server_status(server_name):
    # If the server doesn't exist, it falls back to an empty dictionary {}
    # Then it tries to get 'status'. If that fails, it returns "Server not found"
    return server_config.get(server_name, {}).get('status', 'Server not found')

print("Checking 'server2':", get_server_status('server2'))
print("Checking 'server99':", get_server_status('server99')) # Won't crash!


print("\n--- 4. Sets in Action (Unique Inventory) ---")
# Imagine we pulled logs and found these servers making requests
active_logs = ["server1", "server2", "server1", "server3", "server1"]
print(f"Raw logs list (contains duplicates): {active_logs}")

# Convert the list to a Set to find exactly which unique servers were active
unique_servers = set(active_logs)
print(f"Unique servers (Duplicates removed): {unique_servers}")

print("\n--- 5. Set Operations ---")
frontend_servers = {"server1", "server2"}
backend_servers = {"server2", "server3"}

print(f"All infrastructure (Union): {frontend_servers.union(backend_servers)}")
print(f"Shared servers (Intersection): {frontend_servers.intersection(backend_servers)}")
print(f"Only Frontend (Difference): {frontend_servers.difference(backend_servers)}")
