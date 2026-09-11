# Python Day 19: JSON & YAML in DevOps

Welcome to **Day 19**! If you work in DevOps, 90% of your career will be spent reading, writing, and parsing **JSON** (API Responses, AWS Infrastructure) and **YAML** (Kubernetes, Ansible, CI/CD pipelines).

Today we learn how Python acts as the ultimate bridge between these two formats.

---

## 1. JSON (JavaScript Object Notation)
JSON is the universal language of APIs. It is strict, uses curly braces `{}`, and maps directly to Python Dictionaries and Lists.

### The Big Four JSON Methods (Interview Question!)
You must know the difference between the `s` (string) and non-`s` (file) methods:

| Method | Purpose | Input / Output |
| :--- | :--- | :--- |
| `json.loads()` | **Load String** | Converts a JSON **String** into a Python Dict |
| `json.load()` | **Load File** | Reads a JSON **File** into a Python Dict |
| `json.dumps()` | **Dump String** | Converts a Python Dict into a JSON **String** |
| `json.dump()` | **Dump File** | Writes a Python Dict into a JSON **File** |

**Example: Reading an API Response String**
```python
import json

json_string = '{"server": "web01", "port": 8080}'
config = json.loads(json_string) # String -> Dictionary
print(config["server"]) # web01
```

---

## 2. YAML (YAML Ain't Markup Language)
YAML is the universal language of Configuration. It is human-readable, relies on indentation (spaces, not tabs!), and allows comments (`#`).
*(Requires running `pip install pyyaml`)*

### Safe Loading and Dumping
Always use `safe_load` and `safe_dump` to prevent security vulnerabilities when parsing external YAML files.

> [!CAUTION]
> **The `yaml.load()` Security Exploit**
> Never use the standard `yaml.load()` function. In Python, the standard YAML loader can actually execute arbitrary Python code if it encounters special tags. If a hacker submits a YAML file containing `!!python/object/apply:os.system ["rm -rf /"]`, the `yaml.load()` function will literally run that shell command and wipe your server! 
> 
> `yaml.safe_load()` is designed to ignore these tags, making it completely safe to parse YAML files from untrusted sources.

```python
import yaml

# Reading YAML (Always use safe_load!)
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Writing YAML
with open("output.yaml", "w") as file:
    yaml.safe_dump(config, file, default_flow_style=False)
```

---

## 3. Advanced DevOps: Configuration Validation
When a DevOps script reads a YAML or JSON file, it should **never** assume the file is correct. Senior engineers always validate the configuration before running automation.

```python
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Validation Phase
if "server" not in config:
    print("[FATAL] Missing 'server' block in config!")
    exit(1)
```

---

## 4. Advanced DevOps: Handling Parsing Errors
What happens if a developer forgets a comma in the `server.json` file? Your automation script will crash with a massive stack trace. Handle it gracefully using `try/except`.

```python
import json
import yaml

try:
    with open("server.json", "r") as file:
        data = json.load(file)
except json.JSONDecodeError as e:
    print(f"[FATAL] Invalid JSON format. Did you forget a comma? Error: {e}")
except FileNotFoundError:
    print("[FATAL] server.json does not exist!")
```

---

## 5. Advanced DevOps: Secrets Management
**Never hardcode passwords in JSON or YAML files.**
Instead, configuration files should define the structure, and Python should inject the secrets from Environment Variables.

**Bad YAML:**
```yaml
database:
  password: MySuperSecretPassword
```

**Good Python Injection:**
```python
import os
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Inject the secret from the CI/CD pipeline environment!
config["database"]["password"] = os.getenv("DB_PASSWORD")
```

---

## 🧑‍💻 Practice Exercises
We have created `server.json` and `day19_config_converter.py` in this folder. 
The script simulates a realistic DevOps pipeline: It reads the JSON file (handling errors), validates the required fields, injects an environment variable, and converts it into a beautifully formatted YAML file!
