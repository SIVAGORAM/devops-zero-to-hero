# Python Day 12: Dictionaries and Sets (Project 1)

Welcome to **Day 12**! Today we tackle two massive data structures used heavily in DevOps: **Dictionaries** (for Configuration Management) and **Sets** (for Unique inventory). 

We will also build our very first API Integration project using the GitHub API!

---

## 1. Dictionaries (Key-Value Pairs)
A dictionary allows you to store data using meaningful **Keys** instead of numbers (indexes). In other languages, this is called a Hashmap or an Associative Array.

```python
# A simple server configuration
server = {
    "ip": "192.168.1.10",
    "port": 8080,
    "status": "active"
}
```

### Dictionary Operations
| Operation | Syntax | Description |
| :--- | :--- | :--- |
| **Access** | `server["ip"]` | Returns `"192.168.1.10"` |
| **Add / Modify** | `server["os"] = "linux"` | Adds a new key or overwrites an existing one |
| **Remove** | `del server["port"]` | Deletes the key-value pair |
| **Check** | `if "ip" in server:` | Returns `True` if the key exists |

### Iterating through Dictionaries (`.items()`)
To loop through a dictionary, you must use `.items()` to extract both the key and the value simultaneously. If you only need keys, use `.keys()`. If you only need values, use `.values()`.
```python
for key, value in server.items():
    print(f"{key}: {value}")
```

### Advanced DevOps: Merging Configurations
DevOps engineers constantly need to merge a "default" configuration with an "environment-specific" override. You can merge dictionaries using `.update()` or the Python 3.9+ Merge Operator (`|`).

```python
default_config = {"port": 8080, "log_level": "info", "env": "dev"}
prod_override = {"log_level": "error", "env": "prod"}

# Python 3.9+ Merge Operator (prod_override overwrites default_config)
final_config = default_config | prod_override
print(final_config) # {'port': 8080, 'log_level': 'error', 'env': 'prod'}
```

### Advanced DevOps: Dictionary Comprehensions
Just like Lists, you can filter a massive dictionary in a single line! This is extremely useful when an API returns 1,000 servers and you only want the "active" ones.

```python
servers = {"web-01": "active", "web-02": "inactive", "db-01": "active"}

# Keep only the active servers
active_servers = {name: status for name, status in servers.items() if status == "active"}
print(active_servers) # {'web-01': 'active', 'db-01': 'active'}
```

### Advanced DevOps: The `.get()` Method
If you try to access a key that doesn't exist (like `server["region"]`), Python will crash with a `KeyError`.
Senior DevOps engineers use `.get()` to safely retrieve values and provide a **default fallback**.

```python
# Returns "us-east-1" instead of crashing!
region = server.get("region", "us-east-1") 
```

---

## 2. Sets (Unique Elements)
A Set is a collection that does **not** allow duplicate values. It is also unordered, meaning you cannot use an index like `my_set[0]`.

```python
my_set = {1, 2, 3}
my_set.add(4)
my_set.remove(3)
```

### Lists vs Sets in DevOps
| Feature | List `[]` | Set `{}` | DevOps Example |
| :--- | :--- | :--- | :--- |
| **Duplicates** | Allowed | **Not Allowed** | Lists for history logs. Sets for finding unique Active IP addresses. |
| **Ordering** | Ordered | Unordered | Lists for CI/CD steps (Build -> Test). Sets when order doesn't matter. |
| **Speed** | Slower | **Extremely Fast** | Sets are incredibly fast for `if value in my_set:` checks. |

### Set Operations (Venn Diagrams)
Sets are mathematical. You can combine them!
- **Union (`union`)**: Combines all elements from both sets.
- **Intersection (`intersection`)**: Returns ONLY the elements that exist in *both* sets.
- **Difference (`difference`)**: Returns elements in Set A that are NOT in Set B.

---

## 3. Nested Dictionaries (Server Inventory)
In DevOps, you usually have multiple servers, each with their own configuration. This requires a Dictionary *inside* a Dictionary!

```python
server_config = {
    "web-01": {"ip": "10.0.0.1", "status": "active"},
    "db-01": {"ip": "10.0.0.2", "status": "inactive"}
}

# Accessing web-01's IP address:
print(server_config["web-01"]["ip"])
```

---

## 🧑‍💻 Project 1: GitHub API Integration
We are combining everything we've learned (Variables, API Requests, JSON, Loops, and Dictionaries) into a real-world project.

We will fetch all active Pull Requests from the Kubernetes GitHub repository, parse the JSON, and use a Dictionary to count exactly how many PRs each developer has submitted!

*(Note: You will need to install the `requests` library to run the API script! Run `pip install requests` in your terminal).*

### Practice Files
We have created two practice scripts in this folder:
1. `day12_server_config.py` - Managing nested dictionaries and using `.get()`.
2. `day12_github_prs.py` - The complete Kubernetes GitHub API integration project!
