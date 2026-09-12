# Python Day 23: Advanced Exception Handling

Welcome to **Day 23**! 
A junior programmer writes code that works when everything goes right. A Senior DevOps engineer writes code that **survives** when everything goes wrong.

In DevOps, networks timeout, APIs throttle you, servers crash, and permissions are denied. Advanced Exception Handling allows your automation to gracefully log the failure, retry if possible, or trigger an alert—all without the Python script exploding.

---

## 1. The Anatomy of Failure: `try/except/else/finally`
The core of DevOps error handling uses four distinct blocks.

```python
try:
    # 1. ATTEMPT: The dangerous code (e.g. connecting to a server)
    result = 100 / 2
    
except ZeroDivisionError as error:
    # 2. RECOVER: If it crashes, handle it gracefully
    print(f"Failed to calculate: {error}")
    
else:
    # 3. SUCCESS: Runs ONLY if the try block succeeded without crashing!
    print(f"Calculation succeeded! Result: {result}")
    
finally:
    # 4. CLEANUP: Runs 100% of the time, regardless of success or failure.
    print("Closing network connections and freeing memory.")
```

> [!TIP]
> **Why `finally`?**
> If your script opens a connection to AWS and crashes halfway through, that connection stays open. You put `aws_connection.close()` in the `finally` block to guarantee it cleans up resources no matter what happens!

---

## 2. Catch Specific Exceptions, NOT Everything
Never use a "Bare Except" (`except:`). It will catch everything, including KeyboardInterrupts (Ctrl+C), making your script impossible to stop!

**Bad:**
```python
try:
    subprocess.run(["systemctl", "restart", "nginx"], check=True)
except:
    print("Something failed.") # Was it a permissions issue? Command not found? You don't know!
```

**Good (Senior DevOps Style):**
```python
import subprocess
try:
    subprocess.run(["systemctl", "restart", "nginx"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Nginx failed to start! Exit code: {e.returncode}")
except FileNotFoundError:
    print("Systemctl command not found on this OS!")
```

---

## 3. Creating Custom DevOps Exceptions
Sometimes the built-in Python errors (`ValueError`, `TypeError`) don't describe what actually went wrong in your pipeline. You can create your own!

```python
# Create a Custom Exception
class DeploymentError(Exception):
    pass

class ConfigurationError(Exception):
    pass

# Using it in your code
env = "test"
if env not in ["dev", "prod"]:
    # Fail Fast! Stop the script intentionally.
    raise ConfigurationError(f"Invalid environment: {env}")
```

---

## 4. Exception Chaining (`from e`)
Often, a low-level error (like `FileNotFoundError`) causes a high-level failure (like `DeploymentError`). You can link them together to preserve the context!

```python
try:
    open("server.conf")
except FileNotFoundError as original_error:
    # This raises a high-level error, but keeps the original error attached!
    raise DeploymentError("Failed to deploy because config is missing!") from original_error
```

---

## 5. The Retry Pattern
In DevOps, if an API times out, you shouldn't crash the script immediately. You should wait 2 seconds and try again!

```python
import time
import requests

for attempt in range(3):
    try:
        response = requests.get("https://api.example.com", timeout=5)
        response.raise_for_status()
        print("API Call Successful!")
        break # Break the loop if successful!
        
    except requests.RequestException as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < 2:
            print("Retrying in 2 seconds...")
            time.sleep(2)
        else:
            print("All 3 attempts failed. Triggering PagerDuty alert!")
```

---

## 6. Advanced DevOps: Elegant Cleanup (`contextlib.suppress`)
In DevOps, you frequently need to clean up temporary files. If the file doesn't exist, it throws a `FileNotFoundError`. You *could* use a `try/except: pass` block, but the Senior DevOps approach is using `contextlib`.

```python
from pathlib import Path
import contextlib

# Elegant and readable: "Delete this file, and if it doesn't exist, just ignore the error silently."
with contextlib.suppress(FileNotFoundError):
    Path("/tmp/deployment_cache.json").unlink()
```

---

## 7. Advanced DevOps: Catching Unhandled Pipeline Crashes (`sys.excepthook`)
If a completely unexpected error occurs that you didn't wrap in a `try/except` block, the Python script will crash and print the traceback to the terminal. If this runs via a cronjob, that traceback is lost forever! 

You can override `sys.excepthook` to automatically intercept **all unhandled crashes** and route them to your DevOps Logger before the script dies!

```python
import sys
import logging

logging.basicConfig(filename="pipeline_crashes.log", level=logging.ERROR)

def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
    """Intercepts unhandled crashes and logs them."""
    # Do not intercept KeyboardInterrupt (Ctrl+C)
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
        
    logging.critical("UNHANDLED PIPELINE CRASH", exc_info=(exc_type, exc_value, exc_traceback))

# Override the default Python crash handler
sys.excepthook = log_uncaught_exceptions

# If this happens, it won't just print to terminal; it saves to pipeline_crashes.log!
result = 10 / 0 
```

---

## 🧑‍💻 Practice Exercises
We have created `day23_deployment_automation.py` in this folder. 
It demonstrates a professional DevOps Server Deployment pipeline. It utilizes **Custom Exceptions**, validates the environment (Fail Fast), wraps operations in a full `try/except/else/finally` block, and uses `logging.exception()` to track failures!
