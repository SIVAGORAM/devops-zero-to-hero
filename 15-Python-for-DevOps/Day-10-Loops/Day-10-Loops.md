# Python Day 10: Loops (for and while)

Welcome to **Day 10**! You've already seen a preview of `for` loops when we worked with lists, but today we dive deep into the absolute core of DevOps automation: **Repetition**.

In DevOps, if you find yourself doing the same task twice, you should script it. Loops allow us to execute the same block of code over multiple servers, files, or environments automatically.

---

## 1. The `for` Loop

A `for` loop is used to iterate over a sequence (like a List, Tuple, String, or Range). You use a `for` loop when you know **exactly how many items** you need to process.

### Syntax
```python
servers = ["web-01", "web-02", "db-01"]

for server in servers:
    print(f"Configuring {server}...")
```

### Using `range()`
If you just need to repeat a task a specific number of times, use `range()`.
```python
# This prints 0, 1, 2, 3, 4 (Stops BEFORE 5)
for attempt in range(5):
    print(f"Connection attempt {attempt}...")
```

### Real-World DevOps `for` Loop Use Cases:
1. **Deployments:** Looping through `environments = ["dev", "staging", "prod"]` to push configs.
2. **Backups:** Looping through a list of databases to run `pg_dump`.
3. **Log Rotation:** Looping through `/var/log` to archive old log files.
4. **Cloud Management:** Looping through a list of AWS EC2 Instance IDs to resize them.

---

## 2. The `while` Loop

A `while` loop executes a block of code **as long as a condition is True**. You use a `while` loop when you **don't know how many times** the loop needs to run.

### Syntax
```python
attempt = 0

while attempt < 3:
    print(f"Checking service status... (Attempt {attempt})")
    attempt += 1 # CRITICAL: You must update the condition!
```

> [!CAUTION]
> **Infinite Loops:** If you forget to increment the `attempt` variable, the condition `attempt < 3` will **never** become False. Your script will run forever and crash your CI/CD pipeline!

### Real-World DevOps `while` Loop Use Cases:
1. **Health Checks:** Polling an API endpoint every 5 seconds `while` the status is not "200 OK".
2. **Retry Logic:** Attempting to connect to a database `while` the connection fails (up to a max retry limit).

---

## 3. Loop Control Statements (`break` and `continue`)

Sometimes you need to manipulate how the loop behaves in the middle of its execution.

### `break` (Stop the Loop)
`break` completely exits the loop immediately.
**Use Case:** You are searching a list of 1000 servers for `db-01`. Once you find it, you `break` to stop searching and save CPU time.

```python
servers = ["web-01", "web-02", "db-01", "app-01"]

for server in servers:
    if server == "db-01":
        print("Database found! Stopping search.")
        break
    print(f"Scanning {server}...")
```

### `continue` (Skip the Iteration)
`continue` skips the rest of the current iteration and jumps straight to the next item in the list.
**Use Case:** You are upgrading all servers, but you want to *skip* the database server.

```python
servers = ["web-01", "web-02", "db-01", "app-01"]

for server in servers:
    if server == "db-01":
        print("Skipping database upgrade.")
        continue
    print(f"Upgrading {server}...")
```

### Advanced DevOps: Nested Loops
A "Nested Loop" is simply a loop inside of another loop. This is incredibly common in DevOps when you have a matrix of deployments.

**Use Case:** You need to deploy 3 different microservices across 3 different environments.

```python
environments = ["dev", "staging", "prod"]
apps = ["frontend", "backend", "auth-service"]

for env in environments:
    print(f"\n--- Deploying to {env.upper()} ---")
    for app in apps:
        print(f"Deploying {app} to {env} cluster...")
```

### The Python Loop Secret: `for...else`
Python has a unique feature where loops can have an `else` statement! The `else` block executes **only if the loop finishes completely without hitting a `break` statement.**

**Use Case:** You are scanning a list of servers to see if ANY of them are offline. If you find an offline server, you `break`. If the loop finishes and none were offline, the `else` block confirms everything is healthy!

```python
servers_status = ["online", "online", "online"]

for status in servers_status:
    if status == "offline":
        print("ALERT: Offline server detected!")
        break
else:
    # This ONLY runs if the loop never hits the 'break'
    print("SUCCESS: All servers are online and healthy.")
```

---

## 4. Master Example: Log File Analysis

One of the most common Python tasks for a DevOps engineer is parsing log files to find errors.

```python
log_file = [
    "INFO: Operation successful",
    "ERROR: File not found",
    "DEBUG: Connection established",
    "ERROR: Database connection failed",
]

for line in log_file:
    # Skip any line that doesn't have an error
    if "ERROR" not in line:
        continue
        
    print(f"Alert Triggered: {line}")
```

---

## 🧑‍💻 Practice Exercises
We have created a script called `day10_loops.py` in this folder. It combines all the `for` and `while` loop mechanics, alongside `break` and `continue` statements, into a full DevOps Log Analyzer and Server Manager! Run it locally to practice!
