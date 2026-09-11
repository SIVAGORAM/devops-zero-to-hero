# Python Day 18: Advanced Functions

Welcome to **Day 18**! Today we transition from writing basic "scripts" to building professional DevOps "tools". 

We will cover advanced function architectures: handling unlimited arguments, tracking execution time, and writing functions that retry themselves when they fail!

---

## 1. Flexible Arguments (`*args` and `**kwargs`)
In DevOps, you rarely know exactly how many servers you are deploying to at any given time. Python handles this elegantly.

### `*args` (Variable Positional Arguments)
Captures an unlimited number of arguments into a **Tuple**.
```python
def restart_servers(*servers):
    # 'servers' is now a Tuple: ("web01", "web02", "web03")
    for server in servers:
        print(f"Restarting {server}")

restart_servers("web01", "web02", "web03")
```

### `**kwargs` (Variable Keyword Arguments)
Captures an unlimited number of key=value pairs into a **Dictionary**.
```python
def deploy_app(**config):
    # 'config' is now a Dictionary: {"env": "prod", "replicas": 3}
    print(f"Deploying to {config.get('env')}")

deploy_app(env="prod", replicas=3, version="v2")
```

---

## 2. Argument Unpacking
If you already have a List or Dictionary, you can "unpack" them directly into a function using `*` and `**`.

```python
servers_list = ["web01", "web02"]
config_dict = {"env": "prod", "version": "v2"}

def deploy(*args, **kwargs):
    print("Servers:", args)
    print("Config:", kwargs)

# The * unpacks the list, the ** unpacks the dictionary!
deploy(*servers_list, **config_dict)
```

---

## 3. Decorators
Decorators are the most powerful DevOps function concept. A decorator wraps another function to silently add behavior (like Logging, Timing, or Retries) without changing the original code!

You identify a decorator by the `@symbol` above a function.

### Example: The `@logger` Decorator
```python
from functools import wraps

# 1. Define the Decorator
def logger(func):
    @wraps(func) # Preserves the original function's name
    def wrapper(*args, **kwargs):
        print(f"[START] Executing {func.__name__}...")
        
        # Execute the original function!
        result = func(*args, **kwargs)
        
        print(f"[FINISH] {func.__name__} completed.")
        return result
    return wrapper

# 2. Use the Decorator
@logger
def restart_nginx():
    print("Systemctl restart nginx...")

restart_nginx()
# Output:
# [START] Executing restart_nginx...
# Systemctl restart nginx...
# [FINISH] restart_nginx completed.
```

---

## 4. Lambda Functions
Lambdas are small, anonymous, one-line functions. They are most commonly used in DevOps for custom sorting of complex data (like finding the server with the highest CPU).

```python
servers = [
    {"name": "web01", "cpu": 80},
    {"name": "web02", "cpu": 40}
]

# Sort the list of dictionaries based on the "cpu" key
servers.sort(key=lambda s: s["cpu"])
```

---

## 5. `map()` and `filter()`
In addition to Lambdas and List Comprehensions, DevOps engineers frequently use `map` and `filter` to process large amounts of data.

- `map(function, iterable)`: Applies a function to every item in a list.
- `filter(function, iterable)`: Returns only the items where the function returns `True`.

```python
servers = [{"name": "web01", "cpu": 80}, {"name": "web02", "cpu": 40}]

# Extract just the names (Transform)
names = list(map(lambda s: s["name"].upper(), servers)) # ['WEB01', 'WEB02']

# Filter for high CPU
high_cpu = list(filter(lambda s: s["cpu"] > 70, servers)) # [{'name': 'web01', 'cpu': 80}]
```

---

## 6. Scope (The LEGB Rule)
When you reference a variable, Python searches for it in this exact order:
1. **L**ocal: Inside the current function.
2. **E**nclosing: Inside any enclosing (nested) functions.
3. **G**lobal: At the top level of the script.
4. **B**uilt-in: Python's built-in names (like `print`, `len`).

> [!WARNING]
> While you *can* modify a Global variable inside a function using the `global` keyword, it is considered bad practice in DevOps automation. Always pass data in via arguments and pass data out via `return`.

---

## 7. Advanced DevOps: Type Hinting
In the real world, you are not the only one reading your code. Your IDE and your CI/CD pipelines are reading it too!

**Type Hinting** allows you to declare exactly what type of data a function expects and returns. While Python doesn't enforce it at runtime, tools like `mypy` can scan your code in a GitHub Actions pipeline and block deployments if you pass a String into a function that expects a Dictionary!

```python
# The ': str' tells us it expects a string.
# The '-> bool' tells us it returns a boolean.
def deploy(app_name: str, replicas: int) -> bool:
    print(f"Deploying {replicas} copies of {app_name}")
    return True
```

---

## 🧑‍💻 Practice Exercises
We have created `day18_decorators_and_args.py` in this folder. It combines all these concepts into a single, professional **Automated Deployment Workflow** that features custom Retry and Logging decorators, Type Hints, and `*args`/`**kwargs`!
