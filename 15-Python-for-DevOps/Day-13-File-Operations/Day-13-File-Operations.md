# Python Day 13: File Operations & Configuration Automation

Welcome to **Day 13**! Today we tackle a fundamental DevOps superpower: **File Operations**.

In DevOps, "Configuration as Code" means you don't manually SSH into a server, open `vim`, and edit a file. Instead, you write a Python script that automatically opens a configuration file, finds the exact setting that needs changing, updates it, and saves it.

Today, we will build a script that automates exactly that!

---

## 1. Opening Files
Python uses the built-in `open()` function to interact with files on the operating system.

### File Modes
When you open a file, you must tell Python what you intend to do with it:
| Mode | Action | Description |
| :---: | :--- | :--- |
| **`r`** | Read | Reads a file. Fails if the file doesn't exist. |
| **`w`** | Write | Writes to a file. **CAUTION:** Overwrites the entire file! Creates it if it doesn't exist. |
| **`a`** | Append | Adds new content to the *end* of an existing file. |
| **`r+`** | Read/Write | Allows both reading and writing to the same file. |

---

## 2. Context Managers (`with open(...)`)
You could technically open a file like this:
```python
file = open("server.conf", "r")
content = file.read()
file.close() # If you forget this, the file stays locked in memory!
```

**DevOps Best Practice:** ALWAYS use the `with` statement (called a Context Manager). It automatically closes the file the exact moment the block of code finishes, even if the script crashes!

```python
with open("server.conf", "r") as file:
    content = file.read()
# The file is automatically safely closed here!
```

---

## 3. Reading and Writing

### `read()` vs `readlines()`
- `file.read()`: Returns the entire file as one giant string.
- `file.readlines()`: Returns a **List**, where every line in the file is a separate string. This is crucial for iterating over configuration files line-by-line!

### Writing
```python
with open("logs.txt", "a") as file:
    file.write("ERROR: Database connection failed.\n")
```

---

## 4. Advanced DevOps: Parsing JSON
In modern DevOps, you rarely parse raw text files. You parse **JSON** (API responses, Terraform state) and **YAML** (Kubernetes, Ansible). Python has a built-in `json` module specifically for reading and writing JSON files into Dictionaries!

### Reading JSON
```python
import json

with open("config.json", "r") as file:
    # Converts the JSON file directly into a Python Dictionary!
    config_dict = json.load(file)
    print(config_dict["server_ip"])
```

### Writing JSON
```python
import json

data = {"server_ip": "10.0.0.1", "status": "active"}

with open("config.json", "w") as file:
    # Converts the Python Dictionary back into a formatted JSON file!
    json.dump(data, file, indent=4)
```

---

## 5. Advanced DevOps: Cross-Platform Paths
If you hardcode a path like `C:\logs\server.log`, your script will crash when run on a Linux CI/CD server! Senior DevOps engineers use `os.path.join` to safely build file paths that work on any operating system.

```python
import os

# Safely joins paths using the correct slashes for the OS (Windows \ vs Linux /)
safe_path = os.path.join("var", "log", "server.log")
print(safe_path)
```

---

## 6. Introduction to Boto3
File operations allow you to manage configurations on *local* servers. But what about the Cloud?

**Boto3** is the official Python SDK for AWS. Just like `os` lets you interact with the operating system, `boto3` lets you interact with AWS services (EC2, S3, IAM) programmatically!

```python
import boto3

# We will dive deep into Boto3 in upcoming modules!
s3 = boto3.client('s3')
```

---

## 🧑‍💻 Project 2: Configuration Automation
We have created two files in this folder:
1. `server.conf`: A dummy configuration file that dictates network and security settings.
2. `update_server.py`: A Python script that automatically updates the `MAX_CONNECTIONS` setting inside `server.conf`!

This script simulates a real-world scenario where an external alert triggers a Python script to dynamically increase a server's connection limits!
