# Python Day 17: Advanced Lists & Dictionaries

Welcome to **Day 17**! 

We previously covered the basics of Lists (Days 8/9) and Dictionaries (Day 12). Today, we level up. When you query the AWS API, Kubernetes API, or GitHub API, the response is almost always a **List of Dictionaries**. To manipulate that data, you need advanced techniques like slicing, comprehensions, and safe nested lookups.

---

## 1. Advanced List Operations

### Slicing & Negative Indexing
You can extract subsets of a list using `list[start:stop:step]`. Note that the `stop` index is excluded.
```python
servers = ["web01", "web02", "web03", "web04", "web05"]

print(servers[1:4]) # ['web02', 'web03', 'web04']
print(servers[:2])  # ['web01', 'web02']
print(servers[-1])  # 'web05' (The last element)
print(servers[::-1])# ['web05', 'web04', 'web03', 'web02', 'web01'] (Reverses the list)
```

### `append()` vs `extend()` (Interview Question!)
- `append()` adds exactly one object to the end of the list.
- `extend()` takes an iterable (like another list) and adds its elements individually.
```python
servers = ["web01", "web02"]
servers.append(["db01", "db02"]) 
# Result: ['web01', 'web02', ['db01', 'db02']] (Nested list!)

servers = ["web01", "web02"]
servers.extend(["db01", "db02"]) 
# Result: ['web01', 'web02', 'db01', 'db02'] (Flat list!)
```

### `sort()` vs `sorted()` (Interview Question!)
- `list.sort()` sorts the list *in-place*. It modifies the original list and returns `None`.
- `sorted(list)` creates and returns a *brand new* sorted list, leaving the original intact.

### List Comprehensions
The most "Pythonic" way to filter lists.
```python
servers = [
    {"name": "web01", "status": "running"},
    {"name": "web02", "status": "stopped"},
]

# Extract only the names of running servers
running = [server["name"] for server in servers if server["status"] == "running"]
print(running) # ['web01']
```

---

## 2. Advanced Dictionary Operations

### Safe Retrieval and `setdefault()`
Never access a nested dictionary directly like `server["aws"]["region"]`, as it will crash with a `KeyError` if the key doesn't exist.
```python
# Safe nested retrieval
region = server.get("aws", {}).get("region", "us-east-1")

# setdefault(): If 'status' exists, return it. If not, set it to 'unknown' and return 'unknown'.
status = server.setdefault("status", "unknown")
```

### Dictionary Comprehensions & Merging
```python
# Dictionary Comprehension
numbers = [1, 2, 3]
squares = {num: num**2 for num in numbers} # {1: 1, 2: 4, 3: 9}

# Merging with Unpacking (**)
default_config = {"port": 80}
prod_config = {"port": 443, "ssl": True}

final_config = {**default_config, **prod_config}
# {'port': 443, 'ssl': True}
```

---

## 3. The Ultimate DevOps Pattern: The List of Dictionaries
Almost all Cloud APIs return a List of Dictionaries. 
```python
servers = [
    {"name": "web01", "ip": "10.0.0.10"},
    {"name": "web02", "ip": "10.0.0.11"}
]
```

### Pattern 1: Converting to a Lookup Map
If you need to constantly search for a server by name, searching a List is slow. Convert it to a Dictionary!
```python
server_map = {server["name"]: server for server in servers}

# Now you have instant O(1) lookups!
print(server_map["web02"]["ip"]) # 10.0.0.11
```

### Pattern 2: Status Counting
```python
statuses = ["running", "stopped", "running", "running", "stopped"]
status_count = {}

for status in statuses:
    status_count[status] = status_count.get(status, 0) + 1

print(status_count) # {'running': 3, 'stopped': 2}
```

### Advanced DevOps: Custom Sorting with `lambda`
If you have a list of EC2 instance dictionaries, how do you sort them to find the one using the most CPU? You can't just run `servers.sort()` because Python doesn't know *which* dictionary key to sort by!

Senior engineers use **Lambda (Anonymous) Functions** to tell Python exactly how to sort the list of dictionaries.

```python
servers = [
    {"name": "web01", "cpu": 40},
    {"name": "web02", "cpu": 95},
    {"name": "web03", "cpu": 12}
]

# Sort the list based on the "cpu" key, in descending order!
servers.sort(key=lambda server: server.get("cpu", 0), reverse=True)

# The server with 95% CPU is now at the front of the list!
print(servers[0]["name"]) # web02
```

---

## 🧑‍💻 Practice Exercises
We have created `day17_practice.py` in this folder. It implements the "DevOps Server Inventory" master exercise, demonstrating how to filter, count, and remap a List of Dictionaries.
