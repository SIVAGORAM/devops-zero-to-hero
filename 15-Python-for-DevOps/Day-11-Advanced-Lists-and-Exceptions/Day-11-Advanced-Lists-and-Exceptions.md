# Python Day 11: Advanced Lists & Exception Handling

Welcome to **Day 11**! Today, we combine everything we've learned about Lists and Loops to build our first **production-grade DevOps script**. 

We are introducing three highly critical concepts used in real-world automation:
1. Converting User Input into Lists (`split()`)
2. Interacting with the Operating System (`os` module)
3. Handling Errors Gracefully (`try / except`)

---

## 1. Advanced List Concepts Recap
Before jumping into error handling, let's review two advanced List features.

### List Comprehensions
List comprehensions allow you to create a new list from an existing list in a single line.
```python
files = ["app.log", "error.log", "server.txt", "access.log"]

# Get only the log files!
log_files = [file for file in files if file.endswith(".log")]
print(log_files) # ['app.log', 'error.log', 'access.log']
```

### Nested Lists
A list can contain other lists. This is useful for grouping resources.
```python
servers = [
    ["web-01", "web-02"], # Index 0
    ["db-01", "db-02"]    # Index 1
]
# Access the first database server:
print(servers[1][0]) # db-01
```

---

## 2. Converting Strings to Lists (`split()`)
When a user provides multiple items via the command line or `input()`, it is received as one giant string. We use `.split()` to chop it into a List!

```python
# User enters: /var/log /etc/nginx /opt/app
data = input("Enter folder paths: ")

# 'data' is currently a string: "/var/log /etc/nginx /opt/app"
folders = data.split()

# Now it is a List! ['/var/log', '/etc/nginx', '/opt/app']
```

---

## 3. The `os` Module
Python uses the built-in `os` module to interact with the underlying operating system (Linux/Windows/macOS).

To see what files exist inside a folder, DevOps engineers use `os.listdir()`.

```python
import os

files = os.listdir("/var/log")
print(files)
```

---

## 4. Exception Handling (`try` / `except`)
What happens if you run `os.listdir("/secret/folder")` and you don't have permissions? Or what if the folder doesn't exist?
**Python crashes.** 

In DevOps automation, a script crashing halfway through is a disaster. We use `try / except` blocks to catch the error and handle it gracefully without stopping the script!

```python
import os

folder_path = "/home/admin/secret"

try:
    # Python tries to run this...
    files = os.listdir(folder_path)
    print(files)
    
except FileNotFoundError:
    # If the folder doesn't exist, this runs instead of crashing!
    print(f"ERROR: The folder {folder_path} does not exist.")
    
except PermissionError:
    # If we don't have access, this runs!
    print(f"ERROR: Permission denied for {folder_path}.")
```

### Advanced DevOps: The `finally` Block
The `finally` block is executed **no matter what happens** (whether the script succeeded or crashed). In DevOps, this is critical for cleaning up resources, like closing an SSH connection or a Database connection.

```python
try:
    print("Opening database connection...")
    # do_database_stuff()
except Exception as e:
    print("Database error!")
finally:
    # This ALWAYS runs, preventing a dangling connection!
    print("Closing database connection safely.")
```

### Advanced DevOps: Failing Fast with `raise`
Sometimes, you *want* the script to crash if a critical requirement is missing. You can force an error using the `raise` keyword.

```python
aws_region = ""

if not aws_region:
    # This intentionally stops the script immediately!
    raise ValueError("FATAL ERROR: AWS Region is not set. Halting deployment.")
```

---

## 5. The Production DevOps Script Architecture
Real Python scripts aren't just lines of code running top-to-bottom. They use functions and an **Execution Guard**.

### The Execution Guard
```python
if __name__ == "__main__":
    main()
```
This tells Python: *"Only run the `main()` function if I am executing this script directly. Do NOT run it if someone is just importing this file."*

### Putting it all together
We have created `day11_folder_lister.py` in this directory. It is the culmination of Day 11:
1. It asks the user for multiple folder paths.
2. It uses `split()` to convert them to a list.
3. It uses a `for` loop to check each folder.
4. It uses `os.listdir()` to list the files.
5. It uses `try/except` to prevent crashes if a folder is missing or locked.

Run the script and try entering paths like `/tmp` or `C:\Windows`!
