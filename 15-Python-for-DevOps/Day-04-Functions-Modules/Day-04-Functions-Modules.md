# Python Day 04: Functions, Modules, Packages, and Workspaces

Welcome to **Day 04**! Today is where you transition from writing simple scripts to engineering full-fledged Python architectures. 

As your DevOps scripts grow, putting everything into one massive file becomes impossible to manage. Today, we learn how to break our code into reusable **Functions**, organize those functions into **Modules** (files), and group those modules into **Packages** (directories). We will also learn how to isolate our dependencies using **Virtual Environments**.

---

## 1. Functions

A function is a reusable block of code that performs a specific task. Think of a function like a custom command you can call whenever you need it.

```python
# Defining a Function
def check_server(server_name):
    print(f"Checking health of {server_name}...")
    return "ONLINE"

# Calling a Function
status = check_server("web-server-01")
print(f"Status is: {status}")
```

### Why DevOps Engineers Use Functions:
- **Avoid Code Duplication:** Instead of writing the exact same 20 lines of AWS connection logic 5 times, write it once in a function and call it 5 times.
- **Easy Maintenance:** If the AWS connection logic needs to change, you only have to update the function, not the entire script.
- **Return Values:** Functions can pass data back to the main script using the `return` keyword.

---

## 2. Modules

A **Module** is simply a Python file (`.py`) containing reusable code (functions, variables, or classes). 

Instead of having your configuration variables and your deployment logic in the same file, you can separate them into different modules.

### Example: Configuration Module
Imagine a file named `config.py`:
```python
# config.py
server_name = "web-server"
port = 8080
environment = "production"
```

You can use this module in your `main.py` script by **importing** it:
```python
# main.py
import config

print(f"Deploying {config.server_name} on port {config.port} to {config.environment}")
```

### Ways to Import Modules
1. **Import entire module:** `import math` -> `math.sqrt(16)`
2. **Import specific function:** `from math import sqrt` -> `sqrt(16)`
3. **Import with Alias:** `import math as m` -> `m.sqrt(16)`

### DevOps Best Practice: The Execution Guard
When you `import` a module, Python executes *everything* in that file from top to bottom. If you have test code at the bottom of your module, it will accidentally run during the import!

To prevent this, DevOps engineers **always** use the Execution Guard (`if __name__ == "__main__":`):
```python
# aws.py
def deploy_to_aws():
    print("Deploying...")

# This block ONLY runs if you execute `python aws.py` directly.
# It will NOT run if another script does `import aws`.
if __name__ == "__main__":
    print("Testing the AWS module...")
    deploy_to_aws()
```

---

## 3. Packages

A **Package** is a directory that contains related Python modules. 

Traditionally, a Python package directory must contain a special (usually empty) file named `__init__.py`. This tells Python: *"Hey, treat this folder as a package!"*

### A Real-World DevOps Package Structure
```text
devops_project/
│
├── main.py
│
└── deployment/              <-- This is the Package
    ├── __init__.py          <-- Makes it a Package
    ├── aws.py               <-- Module
    └── docker.py            <-- Module
```

Inside `main.py`, you can import functions directly from the package:
```python
from deployment import aws
from deployment import docker

docker.build_image()
aws.deploy_to_aws()
```

### Quick Recap Table
> [!IMPORTANT]
> This is a highly common interview question! Memorize the differences:

| Concept | Description | Analogy |
| :--- | :--- | :--- |
| **Function** | Reusable block of code using `def` | Smallest unit (e.g., `square()`) |
| **Module** | A Python file (`.py`) containing code | Larger unit (e.g., `math.py`) |
| **Package** | A Directory containing related modules | Largest unit (e.g., `my_package/`) |

### DevOps Troubleshooting: `ModuleNotFoundError`
If you run your pipeline in Jenkins and get a `ModuleNotFoundError`, it is usually because Python doesn't know where your custom Package is located on the Jenkins server!

You can fix this by exporting the `PYTHONPATH` environment variable in your Linux terminal before running the script:
```bash
export PYTHONPATH=/path/to/your/devops_project
python main.py
```

---

## 4. Python Workspaces & Virtual Environments

A Python workspace is the environment where your code runs, including the Python interpreter and installed libraries.

### The Problem
If Project A requires `requests` version 2.x and Project B requires `requests` version 3.x, installing them globally on your Linux server will cause a **dependency conflict**.

### The Solution: Virtual Environments (`venv`)
A virtual environment creates an isolated Python environment just for your specific project.

**1. Create a Virtual Environment:**
```bash
# Linux/macOS
python3 -m venv myenv

# Windows
python -m venv myenv
```

**2. Activate the Virtual Environment:**
```bash
# Linux/macOS
source myenv/bin/activate

# Windows
myenv\Scripts\activate
```
*(You will see `(myenv)` appear in your terminal prompt when activated).*

**3. Install Dependencies Safely:**
```bash
pip install requests
```

**4. Deactivate when finished:**
```bash
deactivate
```

---

## 5. `requirements.txt` (CI/CD Best Practice)

As a DevOps engineer, you don't manually log into a Jenkins server and type `pip install boto3`. You automate it.

You track your project's dependencies in a `requirements.txt` file.

**Generate the file from your local environment:**
```bash
pip freeze > requirements.txt
```
*(Example content: `boto3==1.35.0`)*

**Install from the file in your Jenkins/CI Pipeline:**
```bash
pip install -r requirements.txt
```

---

## 🧑‍💻 Practice Exercises
We have created a sample **DevOps Automation Package** inside the `devops_automation` folder. 
1. Navigate into that folder.
2. Review the `deployment/` package structure.
3. Run `main.py` to see how Functions, Modules, and Packages work together!
