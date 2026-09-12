# Python Day 21: Subprocess & Linux Automation

Welcome to **Day 21**! This is where Python truly becomes a DevOps superpower. 

Instead of writing massive Bash scripts, we can use Python's `subprocess` module to execute Linux commands (`kubectl`, `docker`, `systemctl`, `df -h`), capture their output, and use Python's advanced logic (like `try/except` and JSON parsing) to automate system administration!

---

## 1. `os.system()` vs `subprocess`
In older scripts, you might see `os.system("ls")`. **Do not use this.**
`os.system` only runs the command; it cannot capture the output or handle errors cleanly. Modern DevOps uses `subprocess`.

---

## 2. The Golden Standard: `subprocess.run()`
This is the only function you need for 95% of your automation tasks. It tells Python to run a Linux command and wait for it to finish.

```python
import subprocess

# Basic Execution (Output prints directly to terminal)
subprocess.run(["df", "-h"])
```

### Passing Arguments
Always pass the command and its arguments as a **List of Strings**. Do not pass it as a single string!
- **Good:** `["ls", "-l", "/var/log"]`
- **Bad:** `"ls -l /var/log"`

---

## 3. Capturing Output and Errors
By default, `subprocess` prints directly to the terminal. To capture the output so Python can analyze it, use these critical flags:

- `capture_output=True`: Captures Standard Output (`stdout`) and Standard Error (`stderr`).
- `text=True`: Converts the output from raw Bytes (`b'...'`) into human-readable Strings.

```python
import subprocess

result = subprocess.run(["hostname"], capture_output=True, text=True)

print("The server's hostname is:", result.stdout.strip())
```

---

## 4. Handling Failures (Exit Codes)
In Linux, if a command succeeds, it returns an Exit Code of `0`. If it fails, it returns a non-zero number.

### Method A: Manual Checking
```python
result = subprocess.run(["ls", "/invalid/path"], capture_output=True, text=True)

if result.returncode != 0:
    print(f"Command Failed! Error: {result.stderr}")
```

### Method B: The DevOps Way (`check=True`)
Passing `check=True` tells Python to automatically raise a `CalledProcessError` if the Linux command fails. This is perfect for `try/except` blocks!

```python
import subprocess

try:
    # If nginx fails to restart, it immediately jumps to the except block
    subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
    print("Nginx restarted successfully.")
except subprocess.CalledProcessError as e:
    print(f"[FATAL] Failed to restart Nginx! Exit code: {e.returncode}")
```

---

## 5. Security Warning: `shell=True`
You will see examples online using `subprocess.run("ls -l", shell=True)`. 

> [!CAUTION]
> **Command Injection Vulnerability**
> Never use `shell=True` if you are passing user input or external data into the command. If a user inputs `"; rm -rf /"`, the shell will execute it and destroy the server. Always pass commands as a secure List: `["ls", "-l"]`.

---

## 6. Advanced DevOps: Piping Commands (`subprocess.PIPE`)
In Linux, you often pipe commands together: `ps aux | grep nginx`.
You *could* use `shell=True` to do this, but that's insecure. The senior DevOps approach is to use `subprocess.Popen` to securely pipe the `stdout` of one command directly into the `stdin` of the next!

```python
import subprocess

# 1. Start the first process, telling Python to hold its stdout in a PIPE
p1 = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)

# 2. Start the second process, reading its stdin directly from p1's stdout
p2 = subprocess.Popen(["grep", "nginx"], stdin=p1.stdout, capture_output=True, text=True)

# 3. Close the first process output (so it receives a SIGPIPE if p2 exits)
p1.stdout.close()

# 4. Read the final output from p2
result = p2.communicate()[0]
print(result)
```

---

## 7. Advanced DevOps: Silent Execution (`subprocess.DEVNULL`)
Sometimes you just want to know if a command succeeds (Exit Code 0) without capturing the output into memory, and without letting it spam the user's terminal screen. You can redirect output into the void using `subprocess.DEVNULL`.

```python
import subprocess

# Suppress ALL output. We only care if it succeeds or fails!
result = subprocess.run(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if result.returncode == 0:
    print("Internet is UP!")
```

---

## 8. Real-World DevOps Use Cases
You can use Python + Subprocess to orchestrate any CLI tool!

**Docker Automation:**
`subprocess.run(["docker", "ps"])`

**Kubernetes Automation:**
`subprocess.run(["kubectl", "get", "pods"])`

**Git Automation:**
`subprocess.run(["git", "pull"])`

---

## 🧑‍💻 Practice Exercises
We have created `day21_server_health.py` in this folder. 
This script simulates a complete **Linux Server Health Checker**. It executes `hostname`, `uptime`, `free`, and `df` using `subprocess.run()`, catches any timeouts or command failures, and outputs a beautifully formatted health report!
