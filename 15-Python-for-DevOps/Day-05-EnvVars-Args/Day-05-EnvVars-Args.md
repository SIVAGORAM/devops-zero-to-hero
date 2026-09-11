# Python Day 05: Environment Variables & Command Line Arguments

Welcome to **Day 05**! 
If you want to build Python automation scripts that run inside a Jenkins Pipeline or a Docker Container, you *must* master how to pass data into your scripts dynamically. Hardcoding values in your script is a massive anti-pattern in DevOps.

Today, we learn the two primary ways to pass data into a script: **Environment Variables** (for secrets and static config) and **Command Line Arguments** (for runtime inputs).

---

## 1. Environment Variables (`os` module)

An environment variable is a Key-Value pair provided to your Python script by the Operating System (Linux, Jenkins, Docker, etc.).

### Reading Environment Variables
To read them in Python, we use the built-in `os` module. There are two primary methods, and understanding the difference is a common interview question:

| Method | Behavior if variable is MISSING | Use Case |
| :--- | :--- | :--- |
| **`os.getenv("VAR")`** | Returns `None` (or a default value you provide). | Optional configuration (e.g., debug modes). |
| **`os.environ["VAR"]`** | Raises a fatal `KeyError` and crashes the script! | Required secrets (e.g., Database Passwords). |

**Example:**
```python
import os

# Example 1: Required variable (will crash if missing)
db_password = os.environ["DB_PASSWORD"]

# Example 2: Optional variable with a default fallback
environment = os.getenv("ENVIRONMENT", "dev")
```

---

## 2. Managing Secrets Locally (`.env` and `dotenv`)

In production (like Jenkins or AWS), the system injects environment variables for you. But when you are developing on your local laptop, it's annoying to constantly export variables in your terminal.

The solution is the **`.env` file** and the **`python-dotenv`** package.

### Step 1: Create a `.env` file
```text
APP_NAME=my_super_app
ENVIRONMENT=dev
DB_PASSWORD=super_secret_local_password
```

### Step 2: Load it in Python
```bash
pip install python-dotenv
```
```python
import os
from dotenv import load_dotenv

# This automatically loads all variables from the .env file into the OS environment!
load_dotenv() 

print(os.getenv("APP_NAME"))
```

> [!WARNING]
> **CRITICAL SECURITY RULE:** NEVER commit your `.env` file to Git! It contains raw passwords. You must add `.env` to your `.gitignore` file immediately. If you commit secrets, your infrastructure can be hacked in minutes.

---

## 3. Command Line Arguments

While Environment Variables are great for secrets, what if a user wants to quickly tell the script which server to deploy to? We use **Command Line Arguments**.

*(Example: `python deploy.py --environment prod --version 1.5.0`)*

### The Basic Way: `sys.argv`
`sys.argv` captures everything typed in the terminal as a List.
```python
import sys
# python deploy.py prod
print(sys.argv[1]) # prints "prod"
```
**Problem:** `sys.argv` gets extremely confusing if you have more than 2 arguments. You have to memorize the exact order.

### The Professional Way: `argparse`
`argparse` is the standard library used by DevOps engineers to build professional, documented Command Line Interfaces (CLIs).

```python
import argparse

parser = argparse.ArgumentParser(description="My Deployment Script")

# Define expected arguments
parser.add_argument("--environment", required=True, help="Target environment (dev/prod)")
parser.add_argument("--version", required=True, help="App version to deploy")

# DevOps Best Practice: Boolean Flags
# If the user passes --dry-run, this becomes True. Otherwise, it defaults to False.
parser.add_argument("--dry-run", action="store_true", help="Simulate deployment")

args = parser.parse_args()

print(f"Deploying v{args.version} to {args.environment}")
if args.dry_run:
    print("This is a DRY RUN. No changes will be made.")
```
**Benefit:** If a user types `python deploy.py --help`, Python automatically generates a beautiful help menu explaining how to use the script, including all optional flags!

---

## 4. The Golden Rule: Env Vars vs CLI Args

Knowing *when* to use which method is a classic Senior DevOps Engineer interview question.

| Feature | Environment Variables (`os.getenv`) | Command Line Arguments (`argparse`) |
| :--- | :--- | :--- |
| **Best For** | Secrets, Passwords, API Keys, Tokens. | File names, versions, targets, flags. |
| **Visibility** | Hidden from logs and users. | Highly visible in terminal history and CI/CD logs. |
| **Source** | Provided by Jenkins/Docker/K8s. | Typed by the user executing the script. |

---

## 5. The Complete DevOps Example

Here is how a real Jenkins CI/CD pipeline executes a Python deployment script. 

**1. Jenkins sets the secure environment variables in the background:**
```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="Secret..."
```

**2. Jenkins executes the script, passing the dynamic arguments for this specific build:**
```bash
python deploy.py --environment prod --version 2.0.0
```

**3. The Python script combines both seamlessly:**
```python
import os
import argparse

# 1. Parse Runtime Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--environment", required=True)
parser.add_argument("--version", required=True)
args = parser.parse_args()

# 2. Read Secure Environment Secrets
aws_key = os.environ["AWS_ACCESS_KEY_ID"]

print(f"Deploying {args.version} to {args.environment} using AWS Key: {aws_key[:4]}***")
```

---

## 🧑‍💻 Practice Exercises
We have created a highly realistic `deploy.py` script and a sample `.env.example` file in this folder. 

1. Review `.env.example` to see how we track configuration without exposing secrets.
2. Run `python deploy.py --help` in your terminal to see `argparse` in action!
3. Run `python deploy.py --environment dev --version 1.0.0` to execute the mock deployment.
