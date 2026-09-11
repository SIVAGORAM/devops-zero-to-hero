# Python Day 08 & 09: Lists, Tuples, and Iteration

Welcome to **Days 08 & 09**! We are combining these modules because they cover the absolute backbone of DevOps data management: **Collections**.

When you write a Python script for DevOps, you rarely operate on a single server. You are usually deploying to a *List* of 50 servers, or checking the status of a *List* of 10 Docker containers. Today, we learn how to store, manipulate, and iterate through multiple items efficiently.

---

## 1. Lists vs. Tuples

Python has two primary ways to store an ordered collection of items: **Lists** and **Tuples**.
Understanding the difference between them is one of the most common Python interview questions.

| Feature | List `[]` | Tuple `()` |
| :--- | :--- | :--- |
| **Syntax** | `servers = ["web-01", "web-02"]` | `steps = ("build", "test", "deploy")` |
| **Mutability** | **Mutable** (Can be changed) | **Immutable** (Cannot be changed) |
| **DevOps Use Case**| Dynamic data (e.g., active servers, running containers). You can add or remove items. | Fixed data (e.g., coordinates, deployment pipeline steps, configuration constants). |
| **Performance** | Slightly slower (requires memory reallocation). | Faster and more memory efficient. |

---

## 2. Accessing Elements (Indexing & Slicing)

Both Lists and Tuples are **zero-indexed**, meaning the first element is at index `0`.

```python
servers = ["web-01", "db-01", "app-01", "cache-01"]

# Indexing
print(servers[0])  # web-01
print(servers[-1]) # cache-01 (Negative indexing gets the last item!)

# Slicing (Extracting a subset)
# Syntax: list[start:end] (end is excluded)
print(servers[1:3]) # ['db-01', 'app-01']
```

---

## 3. List Manipulation Methods (The Master Cheat Sheet)

Because Lists are mutable, Python gives us a massive toolbox of methods to modify them. 

### Adding Elements
| Method | Description | Example |
| :--- | :--- | :--- |
| **`append(val)`** | Adds a single item to the very end. | `servers.append("web-03")` |
| **`insert(idx, val)`** | Inserts an item at a specific index. | `servers.insert(0, "load-balancer")` |
| **`extend(list)`** | Merges another list into the current one. | `servers.extend(["db-02", "db-03"])` |

> [!WARNING]
> **`append` vs `extend`**
> If you `append(["a", "b"])` to a list, it adds the *entire list* as a single element `['web', ['a', 'b']]`.
> If you `extend(["a", "b"])`, it flattens them `['web', 'a', 'b']`.

### Removing Elements
| Method | Description | Example |
| :--- | :--- | :--- |
| **`remove(val)`** | Removes the first occurrence of a specific **value**. | `servers.remove("web-01")` |
| **`pop(idx)`** | Removes and returns an item by its **index**. | `crashed = servers.pop(-1)` |
| **`clear()`** | Deletes everything in the list. | `servers.clear()` |

### Searching & Sorting
| Method | Description | Example |
| :--- | :--- | :--- |
| **`index(val)`** | Finds the index position of a value. | `idx = servers.index("db-01")` |
| **`count(val)`** | Counts how many times a value appears. | `servers.count("web-01")` |
| **`sort()`** | Sorts the list in ascending alphabetical/numerical order. | `servers.sort()` |
| **`reverse()`** | Reverses the current order of the list. | `servers.reverse()` |

---

## 4. Iterating Through Collections (`for` loops)

Having a list of 50 servers is useless unless you can do something to all of them. We use `for` loops to iterate over collections.

### The Standard DevOps Automation Loop
```python
deployment_targets = ["web-server-01", "web-server-02", "db-server-01"]

for server in deployment_targets:
    print(f"Connecting to {server}...")
    
    if server.startswith("web"):
        print(f" -> Deploying Nginx to {server}")
    elif server.startswith("db"):
        print(f" -> Deploying PostgreSQL to {server}")

print("All deployments completed!")
```
This is the core foundation of DevOps scripting: **List -> Loop -> SSH/API Call -> Automation.**

### Advanced DevOps: The `enumerate()` Function
If you are looping through a list but you *also* need to know the index number (e.g., to print a numbered list for a user menu), use the built-in `enumerate()` function!

```python
servers = ["web-01", "db-01", "app-01"]

for index, server in enumerate(servers):
    print(f"Server #{index + 1}: {server}")
```

### The DevOps Superpower: List Comprehensions
List Comprehensions are the ultimate "Pythonic" way to filter or modify a list in a single line of code. They replace massive, messy `for` loops.

**Scenario:** You have a mixed list of servers, and you only want to extract the "web" servers into a new list.

```python
all_servers = ["web-01", "db-01", "web-02", "cache-01"]

# ❌ The Junior Way (4 lines)
web_servers = []
for s in all_servers:
    if "web" in s:
        web_servers.append(s)

# ✅ The Senior DevOps Way (1 line - List Comprehension)
web_servers = [s for s in all_servers if "web" in s]
```

---

## 5. Tuple Packing and Unpacking
While you can't modify tuples, they have a superpower called **Unpacking**. This is highly useful when a function returns multiple values (like coordinates, or a status and a message).

```python
# Packing multiple values into a tuple
health_check_result = ("CRITICAL", "Disk space at 99%")

# Unpacking the tuple directly into variables!
status, message = health_check_result

print(f"Alert Status: {status}")
print(f"Details: {message}")
```

---

## 🧑‍💻 Practice Exercises
We have created a master script called `day08_09_lists.py` in this folder. It combines all the list manipulation techniques and iteration loops into a comprehensive DevOps Server Management script. Run it locally to see the operations in action!
