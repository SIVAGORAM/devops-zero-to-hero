# Python Day 20: OS, Pathlib & Shutil

Welcome to **Day 20**! Today we tackle the holy trinity of DevOps filesystem automation. As a DevOps engineer, you will constantly write scripts to create deployment folders, copy configurations, archive old releases, and clean up logs.

Python provides three distinct modules for this, and you need to know exactly when to use which.

---

## 1. The Big Three: Which module do I use?

| Module | Primary Use Case in DevOps | Example Operations |
| :--- | :--- | :--- |
| `os` | **System State** | Environment variables (`os.getenv`), Current Working Directory (`os.getcwd`) |
| `pathlib` | **Modern Path Manipulation** | Creating paths (`Path()`), Recursively searching (`rglob`), Checking if a file exists (`.exists()`) |
| `shutil` | **High-Level File Ops** | Copying files (`copy2`), Moving files (`move`), Deleting entire folders (`rmtree`), Checking Disk Space (`disk_usage`) |

> [!TIP]
> **Modern DevOps Standard:**
> Always use `pathlib` instead of the old `os.path` for file routing. `pathlib` is object-oriented and automatically handles Windows vs Linux slashes (`\` vs `/`).

---

## 2. `os`: Environment Variables & Permissions
Never hardcode secrets or environment-specific data. Pull them from the OS.
```python
import os

# Safely read an environment variable, fallback to 'dev' if it doesn't exist
env = os.getenv("APP_ENV", "dev")

# Setting a variable (only affects the current Python run)
os.environ["AWS_REGION"] = "us-east-1"
```

### File Permissions (`os.chmod`)
In DevOps, you often deploy bash scripts that need to be executed. By default, newly created files do not have "execute" permissions on Linux.
```python
import os
import stat

# The equivalent of running `chmod +x deploy.sh` in the terminal
os.chmod("deploy.sh", os.stat("deploy.sh").st_mode | stat.S_IEXEC)
```

---

## 3. `pathlib`: The Modern Filesystem
`pathlib` replaces string-based path building (`"/var" + "/log"`) with elegant Path objects.

### Path Construction & Checking
```python
from pathlib import Path

# Combine paths using the forward slash `/` operator!
log_file = Path("/var/log") / "application.log"

if log_file.exists() and log_file.is_file():
    print(f"Found log file. Size: {log_file.stat().st_size} bytes")
```

### Directory Creation (The DevOps Way)
If an automation script tries to create a directory that already exists, it will crash. Use these flags to make it resilient:
```python
# parents=True: Creates intermediate folders like `mkdir -p`
# exist_ok=True: Doesn't crash if the folder already exists
Path("project/logs/archive").mkdir(parents=True, exist_ok=True)
```

### Searching Files (Globbing)
```python
# Find all .log files recursively in the current directory and below
for file in Path(".").rglob("*.log"):
    print(file.name)
```

### Symbolic Links (Symlinks)
In DevOps, it is common to deploy a new version of an app to a folder like `v2.0` and then update a `latest` shortcut to point to it. This shortcut is called a Symlink.
```python
from pathlib import Path

# Create a symlink named 'latest' that points to the 'v2.0' folder
Path("releases/latest").symlink_to(Path("releases/v2.0"))
```

---

## 4. `shutil`: Shell Utilities
When you need to act like bash (`cp`, `mv`, `rm -rf`), use `shutil`.

### Copying & Moving
```python
import shutil

# copy2 preserves file metadata (like timestamps)
shutil.copy2("server.conf", "backup/server.conf")

# Move a file
shutil.move("app.log", "archive/app.log")
```

### Deleting and Disk Space
> [!CAUTION]
> `shutil.rmtree()` is the Python equivalent of `rm -rf`. It will recursively delete a folder and everything inside it without asking for confirmation. Use with extreme caution in automation!

```python
# Delete an entire directory tree
shutil.rmtree("old_release")

# Check disk space
usage = shutil.disk_usage("/")
free_gb = usage.free / (1024 ** 3)
print(f"Free disk space: {free_gb:.2f} GB")
```

---

## 🧑‍💻 Practice Exercises
We have created `day20_deployment_automation.py` in this folder. 
It simulates a complete DevOps Deployment Lifecycle. It checks disk space using `shutil`, generates a nested directory structure using `pathlib`, writes configuration and release files, and backs up the configuration using `shutil.copy2`!
