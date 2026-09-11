# Python Day 03: Keywords and Variables for DevOps

Welcome to **Day 03**! Today we cover the absolute building blocks of Python: **Keywords** and **Variables**.

In DevOps, we use variables all the time to handle configuration data (like storing a server's IP address, the deployment environment, or the port number). Understanding how these variables behave (their scope and lifetime) is crucial for writing reliable automation scripts.

---

## 1. Keywords in Python
Keywords are reserved words in Python that have predefined meanings and define the structure and logic of the language. 

> [!WARNING]
> **Important Rule:** You **cannot** use a keyword as a variable name or function name. Python keywords are case-sensitive.

### The Most Important Keywords for DevOps
Here is a categorized list of keywords you will use constantly in your automation scripts:

#### Logical & Conditional & Validation
| Keyword | Usage in DevOps | Example |
| :--- | :--- | :--- |
| **`if` / `elif` / `else`** | Used to run different logic depending on the environment (e.g., prod vs dev). | `if env == "prod":` |
| **`and` / `or` / `not`** | Combining conditions (e.g., check if a server is online AND has space). | `if online and has_space:` |
| **`in`** | Checking if a value exists in a List (e.g., checking if a server is in a target group). | `if server in target_group:` |
| **`assert`** | Validating state *before* doing something dangerous. If false, the script crashes immediately! | `assert env == "prod", "Wrong Env!"` |

#### Loops
| Keyword | Usage in DevOps | Example |
| :--- | :--- | :--- |
| **`for`** | Iterating over a list of servers or iterating through log files. | `for server in servers:` |
| **`while`** | Continuously polling an endpoint until a server comes back online. | `while not server_ready:` |

#### Error Handling & Functions
| Keyword | Usage in DevOps | Example |
| :--- | :--- | :--- |
| **`try` / `except` / `finally`**| Catching API connection timeouts gracefully so the script doesn't crash. | `try: connect()` |
| **`def` / `return`** | Defining a reusable block of logic (e.g., `def create_ec2_instance():`). | `def backup_db():` |
| **`import` / `from` / `as`** | Importing external SDKs like `boto3` for AWS or `os` for the filesystem. | `import os` |
| **`pass`** | Used as a placeholder when scaffolding out new automation scripts. | `def future_feature(): pass` |

#### Special Values & Identity
| Keyword | Usage in DevOps | Example |
| :--- | :--- | :--- |
| **`True` / `False`** | Toggling configuration flags (e.g., `https_enabled = True`). | `is_healthy = False` |
| **`None`** | Representing a missing or unassigned value (e.g., IP not yet assigned). | `public_ip = None` |
| **`is`** | Checking identity. Used frequently to check if a value is exactly `None`. | `if ip is None:` |

---

## 2. Variables in Python
A variable is simply a named storage location used to hold data. Because Python is dynamically typed, you don't need to declare what type of data it holds; Python figures it out automatically!

```python
server_name = "web-server"   # Automatically recognized as a String
port = 8080                  # Automatically recognized as an Integer
is_https_enabled = True      # Automatically recognized as a Boolean
```

### DevOps Best Practice: Type Hinting
While Python is dynamically typed, modern DevOps scripts heavily use **Type Hints**. This allows your IDE (like VS Code) to catch bugs *before* you run the script against your production servers!
```python
# Adding type hints makes your automation scripts infinitely safer
server_name: str = "web-server"
port: int = 8080
is_https_enabled: bool = True
```

### Variable Reassignment
Variables can be changed dynamically, which is perfect for updating configurations throughout a script:
```python
port = 80
print(f"HTTP Port: {port}")

port = 443
print(f"HTTPS Port: {port}")
```

---

## 3. Variable Scope and Lifetime
**Scope** determines where in your code a variable can be accessed. In Python, there are two main scopes you need to know: Local and Global.

### Local Scope (Function Level)
Variables defined *inside* a function exist only inside that function.
- **Lifetime:** They are created when the function is called, and destroyed immediately when the function finishes.
```python
def test_connection():
    environment = "dev"  # Local Variable
    print(environment)

test_connection()
# print(environment) --> This will throw an ERROR because 'environment' was destroyed!
```

### Global Scope (Module Level)
Variables defined *outside* of any function are Global. They can be read by any function in the script.
- **Lifetime:** They exist for the entire duration the Python script is running.
```python
environment = "production"  # Global Variable

def deploy():
    print(f"Deploying to {environment}") # Successfully reads the global variable

deploy()
```

> [!CAUTION]
> **The `global` Keyword:** If you want a function to *modify* a global variable, you must use the `global` keyword inside the function. However, in modern DevOps, this is considered a bad practice. It is better to pass variables explicitly as arguments to your functions!

---

## 4. Variable Naming Conventions
Writing clean, maintainable code is a massive part of being a Senior DevOps Engineer.

**Rules for Naming Variables:**
- Start with a letter or an underscore `_`.
- Do **not** start with a number.
- Do **not** use spaces.
- Do **not** use Python keywords (like `class` or `import`).

**DevOps Best Practice (`snake_case`):**
Python universally uses `snake_case` (lowercase words separated by underscores). 
- ❌ `serverName = "web"` (CamelCase - Avoid in Python)
- ❌ `a = "web"` (Not descriptive)
- ✅ `server_name = "web"` (Perfect)

### DevOps Constants (`UPPER_SNAKE_CASE`)
In DevOps, you often have configuration variables that should **never** change while the script is running (like a timeout limit or a base API URL). By convention, we write these in all uppercase to signal to other engineers: "Do not modify this!"
```python
# Standard variables can change
current_retries = 0 

# Constants NEVER change
MAX_RETRIES = 5
AWS_REGION = "us-east-1"
```

### Advanced: Passing Variables from the Command Line
Hardcoding variables like `environment = "dev"` is fine for practice, but in real DevOps pipelines (like Jenkins or GitHub Actions), you pass variables dynamically into your script when you run it!

You can capture these using Python's built-in `sys` module:
```python
import sys

# Example execution: python deploy.py prod
if len(sys.argv) > 1:
    environment = sys.argv[1] # Captures "prod" from the terminal
    print(f"Deploying to: {environment}")
```

---

## 5. Real-World DevOps Example
In automation scripts, we use variables to abstract our configuration. This way, if the port changes, we only update it in *one* place at the top of the file instead of hunting through 500 lines of code.

```python
# --- CONFIGURATION VARIABLES ---
environment = "prod"
server_name = "auth-server"
port = 443
https_enabled = True

# --- AUTOMATION LOGIC ---
print(f"Environment: {environment}")
print(f"Server: {server_name}")
print(f"Port: {port}")

if environment == "prod":
    print(f"Initiating Production Deployment to {server_name}:{port}...")
else:
    print(f"Initiating Test Deployment to {server_name}:{port}...")
```

---

## 6. Practice Exercises
Check out the `day03_variables.py` script included in this repository. It walks you through:
1. Basic Variable Assignment
2. Simulating Configuration changes
3. Checking Local vs Global Scope
4. Building a mini deployment decision engine based on the environment!
