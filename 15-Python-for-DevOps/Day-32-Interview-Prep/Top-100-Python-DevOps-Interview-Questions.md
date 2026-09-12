# Top 100 Python Interview Questions for DevOps Engineers 🚀

This guide contains the top 100 interview questions you will face as a DevOps Engineer. Every answer follows the **Golden Structure**: Definition, Example, and a real-world DevOps Use Case.

---

## 🟢 Category 1: Python Fundamentals (1-15)

### 1. Is Python interpreted or compiled?
- **Definition**: Python compiles source code to bytecode (`.pyc`) and then an interpreter (CPython) executes it line by line.
- **Example**: Running `python script.py`.
- **DevOps Use Case**: Because it is interpreted, you can quickly write and run deployment scripts on any Linux server without needing a build step (like Go or C++).

### 2. What is PEP 8?
- **Definition**: The official style guide for Python code.
- **Example**: Using 4 spaces for indentation and `snake_case` for variable names.
- **DevOps Use Case**: Ensures all automation scripts in a DevOps team's Git repository look uniform and are easy to maintain.

### 3. What is a Virtual Environment?
- **Definition**: An isolated environment that contains its own Python interpreter and installed libraries.
- **Example**: `python -m venv venv`
- **DevOps Use Case**: Prevents dependency conflicts. E.g., Script A needs `requests==2.0` and Script B needs `requests==3.0`.

### 4. What is `requirements.txt`?
- **Definition**: A file listing all third-party libraries and their versions required to run a Python project.
- **Example**: `pip freeze > requirements.txt`
- **DevOps Use Case**: Used in CI/CD pipelines and Dockerfiles to automatically install dependencies before running automation.

### 5. What are the mutable and immutable data types?
- **Definition**: Mutable objects can be changed after creation (List, Dict, Set). Immutable objects cannot (String, Tuple, Integer).
- **Example**: `my_tuple = (1,2)` -> `my_tuple[0] = 3` (Throws Error).
- **DevOps Use Case**: Use Tuples to store hardcoded API URLs that should never be altered during a deployment script's execution.

### 6. What is the difference between `==` and `is`?
- **Definition**: `==` compares the *value* of two objects. `is` compares the *memory address* (identity) of two objects.
- **Example**: `a = [1,2]; b = [1,2]; print(a == b) # True; print(a is b) # False`
- **DevOps Use Case**: Use `is None` when checking if an API returned an empty response, as it is faster and more precise than `== None`.

### 7. How do you handle Environment Variables in Python?
- **Definition**: Using the `os` module to read variables from the operating system.
- **Example**: `import os; token = os.getenv("API_TOKEN")`
- **DevOps Use Case**: Fetching secure AWS keys or API tokens injected by Jenkins/GitHub Actions without hardcoding them in the script.

### 8. What does the `pass` keyword do?
- **Definition**: A null operation; nothing happens when it executes. Used as a placeholder.
- **Example**: `if server == "dev": pass`
- **DevOps Use Case**: Stubbing out functions (e.g., `def backup_db(): pass`) while designing the architecture of a massive deployment script.

### 9. What is the difference between `break` and `continue`?
- **Definition**: `break` exits the entire loop. `continue` skips the rest of the current iteration and moves to the next one.
- **Example**: `for s in servers: if s == "offline": continue`
- **DevOps Use Case**: When looping through 100 servers to apply an update, if one server is unreachable, you `continue` to the next one rather than `break`ing and stopping the entire deployment.

### 10. How do you parse CLI arguments?
- **Definition**: Using the `argparse` or `sys.argv` modules to pass inputs to a script when running it.
- **Example**: `python deploy.py --env prod`
- **DevOps Use Case**: Allowing a single deployment script to dynamically target `dev`, `staging`, or `prod` based on the CLI flag passed by the CI/CD pipeline.

### 11. What is Exception Handling?
- **Definition**: Catching runtime errors so the script doesn't abruptly crash using `try`, `except`, `finally`.
- **Example**: `try: int("a") except ValueError: print("Error")`
- **DevOps Use Case**: Wrapping AWS or API calls in `try/except` blocks so that if a network timeout occurs, the script logs the error and retries instead of destroying the CI/CD pipeline.

### 12. What is the `finally` block?
- **Definition**: A block of code that executes regardless of whether an exception was raised or not.
- **Example**: `try: ... finally: file.close()`
- **DevOps Use Case**: Ensuring that a database connection or SSH session is always cleanly closed, even if the deployment command failed.

### 13. What is a lambda function?
- **Definition**: A small, anonymous, single-line function.
- **Example**: `square = lambda x: x * 2`
- **DevOps Use Case**: Used for quick, inline sorting of cloud resources. E.g., Sorting a list of AWS EC2 instances by their launch time.

### 14. What are `*args` and `**kwargs`?
- **Definition**: `*args` allows passing a variable number of positional arguments. `**kwargs` allows passing a variable number of keyword (dictionary) arguments.
- **Example**: `def deploy(**kwargs): print(kwargs.get("port"))`
- **DevOps Use Case**: Writing generic wrapper functions for AWS APIs where you don't know exactly how many configuration parameters the user will pass.

### 15. What is the difference between a Module and a Package?
- **Definition**: A module is a single `.py` file. A package is a directory containing multiple modules and an `__init__.py` file.
- **Example**: `import math` (module) vs `from devops import aws` (package).
- **DevOps Use Case**: Structuring large DevOps automation toolkits into logical packages (`aws`, `k8s`, `utils`) rather than writing a 2,000-line monolithic script.

---

## 🔵 Category 2: Data Structures (16-30)

### 16. What is a List?
- **Definition**: An ordered, mutable collection of items that allows duplicates.
- **Example**: `servers = ["web1", "web2"]`
- **DevOps Use Case**: Storing a dynamic queue of EC2 instance IDs that need to be terminated.

### 17. What is a Tuple?
- **Definition**: An ordered, immutable collection of items.
- **Example**: `ports = (80, 443)`
- **DevOps Use Case**: Storing fixed configuration values (like allowed security group ports) that should never be altered by the script.

### 18. What is a Set?
- **Definition**: An unordered collection of unique elements.
- **Example**: `ips = {"192.168.1.1", "10.0.0.1"}`
- **DevOps Use Case**: Removing duplicate IP addresses when parsing 50,000 lines of NGINX access logs.

### 19. What is a Dictionary?
- **Definition**: A mutable collection of key-value pairs.
- **Example**: `config = {"env": "prod", "timeout": 30}`
- **DevOps Use Case**: Parsing and modifying JSON payloads received from GitHub Webhooks or AWS APIs.

### 20. How do you safely access a Dictionary key?
- **Definition**: Using the `.get()` method instead of bracket notation to prevent `KeyError`s.
- **Example**: `config.get("port", 8080)`
- **DevOps Use Case**: Parsing complex Kubernetes JSON responses where a specific metadata field might be missing.

### 21. What is a List Comprehension?
- **Definition**: A concise way to create lists using a single line of code.
- **Example**: `prod_servers = [s for s in servers if "prod" in s]`
- **DevOps Use Case**: Quickly filtering a massive list of EC2 instances to find only the ones tagged with `environment: production`.

### 22. What is Dictionary Comprehension?
- **Definition**: Creating a dictionary in a single line using an iterable.
- **Example**: `squared = {x: x**2 for x in range(5)}`
- **DevOps Use Case**: Reformatting a raw AWS API response into a cleaner mapping of `InstanceID: IP_Address` for logging.

### 23. Difference between `append()` and `extend()`?
- **Definition**: `append()` adds a single object to the end. `extend()` merges another iterable into the list.
- **Example**: `list1.extend([3,4])`
- **DevOps Use Case**: Merging two lists of server IP addresses pulled from two different AWS regions into one master list.

### 24. Difference between `remove()`, `pop()`, and `del`?
- **Definition**: `remove()` deletes by value. `pop()` deletes by index and returns it. `del` deletes by index without returning.
- **Example**: `servers.pop(0)`
- **DevOps Use Case**: Using `pop()` to remove an IP address from a queue and process it simultaneously.

### 25. How do you iterate over a dictionary?
- **Definition**: Using `.items()` to get both keys and values.
- **Example**: `for k, v in config.items(): print(k, v)`
- **DevOps Use Case**: Looping through a deployment configuration dictionary to apply 10 different environment variables to a Docker container.

### 26. What does `zip()` do?
- **Definition**: Combines two or more iterables into tuples.
- **Example**: `for host, ip in zip(hosts, ips): print(host, ip)`
- **DevOps Use Case**: Merging a list of server hostnames and a list of their corresponding IP addresses to generate an `/etc/hosts` file.

### 27. What does `enumerate()` do?
- **Definition**: Adds a counter to an iterable.
- **Example**: `for idx, server in enumerate(servers): print(idx, server)`
- **DevOps Use Case**: Numbering the output of a script that lists unhealthy Kubernetes pods for the user to read clearly.

### 28. How do you merge two dictionaries?
- **Definition**: Using the `|` operator (Python 3.9+) or the `.update()` method.
- **Example**: `final_config = default_config | user_config`
- **DevOps Use Case**: Merging default infrastructure configurations with overrides provided by a specific developer.

### 29. What is slicing?
- **Definition**: Extracting a specific portion of a sequence (list, string, tuple).
- **Example**: `servers[0:5]`
- **DevOps Use Case**: Paginating output or batching a deployment so you only restart 5 servers at a time.

### 30. How do you reverse a list/string?
- **Definition**: Using the slice step `[::-1]` or `.reverse()`.
- **Example**: `word[::-1]`
- **DevOps Use Case**: Reversing the order of a log file so the newest lines are processed first.

---

## 🟡 Category 3: System & File Automation (31-45)

### 31. What is the `os` module?
- **Definition**: A module providing a portable way to use operating system dependent functionality.
- **Example**: `os.environ.get("PATH")`
- **DevOps Use Case**: Fetching environment variables, creating directories for backups, and reading file metadata.

### 32. What is the `subprocess` module?
- **Definition**: Used to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
- **Example**: `subprocess.run(["docker", "ps"])`
- **DevOps Use Case**: Executing bash commands (`kubectl`, `terraform`, `git`) directly from a Python script and capturing the stdout.

### 33. Why use `capture_output=True` in subprocess?
- **Definition**: It captures the stdout and stderr of the command so you can store it in a variable.
- **Example**: `res = subprocess.run(["ls"], capture_output=True)`
- **DevOps Use Case**: Running `kubectl get pods` and parsing the output in Python to see if any pods are crashing, rather than just printing it to the terminal.

### 34. What does `check=True` do in subprocess?
- **Definition**: It automatically raises a `CalledProcessError` if the executed command returns a non-zero exit status.
- **Example**: `subprocess.run(["false"], check=True)`
- **DevOps Use Case**: Ensuring your Python script instantly fails and alerts you if a bash command (like `git pull`) fails.

### 35. What is the `pathlib` module?
- **Definition**: An object-oriented way to interact with filesystem paths.
- **Example**: `Path("/etc/nginx/nginx.conf").exists()`
- **DevOps Use Case**: Safely joining directory paths (cross-platform) when writing automated backup scripts.

### 36. What is the `shutil` module?
- **Definition**: Offers high-level operations on files and collections of files, like copying and removal.
- **Example**: `shutil.copytree("src", "dest")`
- **DevOps Use Case**: Automating the backup of a massive configuration directory before running an update script.

### 37. What is the context manager (`with` statement)?
- **Definition**: Used to wrap the execution of a block of code, ensuring clean setup and teardown (like closing files).
- **Example**: `with open("config.txt", "r") as f: data = f.read()`
- **DevOps Use Case**: Reading large log files safely; ensures the file lock is released even if the script crashes midway.

### 38. How do you parse JSON in Python?
- **Definition**: Using the `json` module (`json.loads()` for strings, `json.load()` for files).
- **Example**: `data = json.loads('{"env": "prod"}')`
- **DevOps Use Case**: Decoding webhook payloads from GitHub or API responses from Datadog.

### 39. How do you write JSON to a file?
- **Definition**: Using `json.dump()`.
- **Example**: `with open("out.json", "w") as f: json.dump(data, f)`
- **DevOps Use Case**: Exporting a list of orphaned AWS resources into a JSON report for compliance auditing.

### 40. How do you parse YAML in Python?
- **Definition**: Using the `pyyaml` library and `yaml.safe_load()`.
- **Example**: `config = yaml.safe_load(file_stream)`
- **DevOps Use Case**: Reading Kubernetes manifests or Ansible playbooks directly into Python dictionaries for validation.

### 41. Why use `yaml.safe_load` over `yaml.load`?
- **Definition**: `safe_load` only resolves standard YAML tags and prevents arbitrary code execution.
- **Example**: `yaml.safe_load(user_input)`
- **DevOps Use Case**: A major security best practice to prevent attackers from injecting malicious Python code via a tampered config file.

### 42. What is the `logging` module?
- **Definition**: Defines functions and classes for implementing a flexible event logging system.
- **Example**: `logging.info("Deploying...")`
- **DevOps Use Case**: Replaces `print()` in production. Writes timestamped, severity-leveled (INFO/ERROR) logs to `/var/log/automation.log` so you can audit failures at 3 AM.

### 43. What are the 5 standard logging levels?
- **Definition**: DEBUG, INFO, WARNING, ERROR, CRITICAL.
- **Example**: `logging.error("DB Connection Failed")`
- **DevOps Use Case**: Filtering logs in Splunk/Datadog so alerts are only triggered on ERROR or CRITICAL events.

### 44. What is a Generator (`yield`)?
- **Definition**: A function that returns an iterator that produces a sequence of values lazily using `yield`.
- **Example**: `def gen(): yield 1`
- **DevOps Use Case**: Processing a 50GB NGINX access log line-by-line without loading the entire file into RAM and crashing the server.

### 45. How do you check if a file exists?
- **Definition**: Using `os.path.exists()` or `Path("file.txt").exists()`.
- **Example**: `if Path("config.yaml").exists(): ...`
- **DevOps Use Case**: Validating that a developer actually placed the `.env` file in the directory before starting the deployment script.

---

## 🟠 Category 4: APIs & Cloud Automation (46-70)

### 46. What is the `requests` library?
- **Definition**: The most popular standard library for making HTTP requests in Python.
- **Example**: `res = requests.get("https://api.github.com")`
- **DevOps Use Case**: Interacting with REST APIs (Jira, GitHub, PagerDuty) to automate ticket creation or alert management.

### 47. Why should you always use the `timeout` parameter in requests?
- **Definition**: It specifies how long to wait for the server to send data before giving up.
- **Example**: `requests.get(url, timeout=5)`
- **DevOps Use Case**: If the target server hangs indefinitely, your CI/CD pipeline will also hang forever. Timeouts ensure the pipeline fails quickly.

### 48. What does `response.raise_for_status()` do?
- **Definition**: Raises an `HTTPError` if the HTTP request returned an unsuccessful status code (4xx, 5xx).
- **Example**: `res.raise_for_status()`
- **DevOps Use Case**: Immediately throwing an exception and halting the automation if the Slack webhook rejects your message with a 403 Forbidden.

### 49. What is Boto3?
- **Definition**: The Amazon Web Services (AWS) SDK for Python.
- **Example**: `ec2 = boto3.client("ec2")`
- **DevOps Use Case**: Writing scripts to automatically snapshot databases, delete unused EBS volumes, or provision EC2 instances.

### 50. Boto3 `Client` vs `Resource`?
- **Definition**: `Client` is a low-level, dictionary-based API (maps 1:1 with AWS API). `Resource` is a high-level, object-oriented API.
- **Example**: `client.describe_instances()` vs `resource.Instance('i-123').stop()`
- **DevOps Use Case**: Using `Client` for massive data retrieval (listing all buckets) and `Resource` for simple targeted actions (stopping a specific instance).

### 51. How does Boto3 authenticate?
- **Definition**: It automatically searches for credentials in `.env`, `~/.aws/credentials`, or IAM Roles attached to the instance.
- **Example**: `boto3.client('s3')` (No keys passed).
- **DevOps Use Case**: You should never hardcode AWS keys in Python. Attach an IAM Role to the EC2/EKS pod running the script so Boto3 authenticates dynamically.

### 52. What is a Boto3 Paginator?
- **Definition**: A utility to iterate over AWS API responses that are too large to fit in a single response (AWS truncates at 1000 items).
- **Example**: `paginator = client.get_paginator('list_objects_v2')`
- **DevOps Use Case**: Ensuring your script doesn't miss files when deleting old backups from an S3 bucket containing 50,000 objects.

### 53. What is a Boto3 Waiter?
- **Definition**: A utility that blocks execution until a specific AWS resource state is reached.
- **Example**: `waiter.wait(InstanceIds=['i-123'])`
- **DevOps Use Case**: Scripting an EC2 launch, then using a waiter to pause the script until the instance is in the `running` state before attempting to SSH into it.

### 54. What is a Webhook?
- **Definition**: A user-defined HTTP callback triggered by an event.
- **Example**: GitHub sending a POST payload when a PR is merged.
- **DevOps Use Case**: Building a Python Flask API to receive webhooks from GitHub, triggering an automated Jenkins build automatically.

### 55. What is Flask?
- **Definition**: A lightweight WSGI web application framework in Python.
- **Example**: `@app.route("/") def home(): return "OK"`
- **DevOps Use Case**: Creating custom microservices or API gateways to expose internal bash scripts as REST APIs to developers.

### 56. What is basic Authentication?
- **Definition**: Sending a base64 encoded username/password in the HTTP header.
- **Example**: `requests.get(url, auth=('user', 'pass'))`
- **DevOps Use Case**: Authenticating against older enterprise tools (like basic Jira instances or internal Jenkins endpoints).

### 57. What is a Bearer Token?
- **Definition**: A security token sent in the `Authorization` header.
- **Example**: `headers={"Authorization": "Bearer abc123"}`
- **DevOps Use Case**: Authenticating securely with modern APIs like Kubernetes, GitHub, or Datadog.

### 58. How do you parse an API JSON response?
- **Definition**: Using the `.json()` method on the requests object.
- **Example**: `data = response.json()`
- **DevOps Use Case**: Extracting the exact `InstanceId` from a massive AWS REST API response to pass to the next function.

### 59. What does HTTP 403 mean?
- **Definition**: Forbidden. The server understood the request but refuses to authorize it.
- **Example**: Returning 403 when a user lacks IAM permissions.
- **DevOps Use Case**: Catching this in Python to alert the DevOps team that a Service Account token has expired.

### 60. What does HTTP 500 mean?
- **Definition**: Internal Server Error. The server crashed.
- **Example**: Python Flask app throwing an uncaught exception.
- **DevOps Use Case**: Using retry logic (Exponential Backoff) in your scripts, because 500s are often temporary backend hiccups.

### 61. How do you handle Pagination in REST APIs?
- **Definition**: Inspecting the response headers or payload for a `next_page` URL and making a `while` loop.
- **Example**: `while url: res = requests.get(url); url = res.json().get('next')`
- **DevOps Use Case**: Fetching 10,000 user records from an active directory API that only returns 100 users per request.

### 62. What is Idempotency in automation?
- **Definition**: An operation that produces the same safe result whether executed once or 100 times.
- **Example**: `Path("dir").mkdir(exist_ok=True)`
- **DevOps Use Case**: Crucial for deployment scripts. If a CI/CD pipeline fails midway and is restarted, it shouldn't crash because "Directory already exists".

### 63. How do you implement a Dry-Run?
- **Definition**: A script mode that prints what *would* happen, without actually executing the destructive actions.
- **Example**: `if dry_run: print("Would delete:", instance) else: delete()`
- **DevOps Use Case**: Allowing a junior engineer to run a cleanup script in `--dry-run` mode and get approval on the output before committing to it.

### 64. What is the Docker SDK for Python?
- **Definition**: A library (`import docker`) used to interact directly with the Docker Engine API.
- **Example**: `client = docker.from_env(); client.containers.list()`
- **DevOps Use Case**: Writing a "revive" script that monitors containers, dynamically fetches logs, and restarts any container in the `exited` state.

### 65. What is the Kubernetes Python Client?
- **Definition**: The official API client (`import kubernetes`) for Kubernetes.
- **Example**: `config.load_kube_config(); v1.list_namespaced_pod("default")`
- **DevOps Use Case**: Building custom auto-scalers that watch pod health and patch Deployment replica counts programmatically.

### 66. Difference between `load_kube_config` and `load_incluster_config`?
- **Definition**: `kube_config` loads local `~/.kube/config`. `incluster_config` loads the ServiceAccount token mounted inside a running K8s pod.
- **Example**: `try: load_kube_config() except: load_incluster_config()`
- **DevOps Use Case**: Writing a single script that works locally on your laptop for testing, but works seamlessly when deployed as a CronJob inside the cluster.

### 67. How do you stream logs in Python?
- **Definition**: Yielding data from an active connection rather than downloading it all at once.
- **Example**: `for line in container.logs(stream=True): print(line)`
- **DevOps Use Case**: Watching a newly deployed Kubernetes pod boot up in real-time within your CI/CD pipeline to ensure it doesn't crash on startup.

### 68. How do you execute commands inside a running container?
- **Definition**: Using the `docker exec` equivalent via APIs.
- **Example**: `container.exec_run("cat /etc/nginx/nginx.conf")`
- **DevOps Use Case**: A diagnostic script that verifies configuration files injected into a running production container without needing SSH access.

### 69. How do you perform a Rolling Restart via Python?
- **Definition**: You cannot directly "restart" a K8s deployment. You must patch its annotations with a new timestamp.
- **Example**: `apps_v1.patch_namespaced_deployment(..., body=patch_with_new_timestamp)`
- **DevOps Use Case**: Automating zero-downtime certificate rotations by forcing Kubernetes to cycle pods sequentially.

### 70. How do you handle K8s/Docker API errors?
- **Definition**: Catching `ApiException` or `docker.errors.APIError`.
- **Example**: `try: get_pod() except ApiException as e: print(e.status)`
- **DevOps Use Case**: Preventing your script from crashing with a stack trace if it attempts to scale a deployment that was already deleted (handling 404s gracefully).

---

## 🟣 Category 5: Testing, CI/CD, & Advanced Concepts (71-100)

### 71. What is Unit Testing?
- **Definition**: Testing an individual, isolated piece of code (like a single function).
- **Example**: `def test_add(): assert add(1, 1) == 2`
- **DevOps Use Case**: Ensuring the string-parsing function that extracts server IPs from a config file actually works before trusting it in production.

### 72. What is `pytest`?
- **Definition**: The most popular, robust testing framework in Python.
- **Example**: `pytest -v tests/`
- **DevOps Use Case**: Executed as the primary validation step in a Jenkins or GitHub Actions pipeline before a deployment is allowed to proceed.

### 73. What is Mocking?
- **Definition**: Replacing a real external dependency with a fake object that simulates its behavior.
- **Example**: `@patch("requests.get") def test_api(mock_get): ...`
- **DevOps Use Case**: You never want your unit tests to hit the real AWS API (costs money, risks destroying data). You mock it to return a fake JSON response.

### 74. What is the `moto` library?
- **Definition**: A specialized library that mocks AWS Boto3 completely by spinning up a fake AWS environment in RAM.
- **Example**: `@mock_aws def test_s3(): boto3.client('s3').create_bucket(...)`
- **DevOps Use Case**: The industry standard for safely testing complex AWS automation scripts offline in CI/CD pipelines.

### 75. What is a Pytest Fixture?
- **Definition**: A function that provides reusable baseline data or setup/teardown logic for tests.
- **Example**: `@pytest.fixture def dummy_server(): return {"ip": "1.1.1.1"}`
- **DevOps Use Case**: Injecting a fake Docker container object into 50 different tests without rewriting the mock initialization code.

### 76. What is Code Coverage?
- **Definition**: A metric indicating the percentage of your source code executed by your test suite.
- **Example**: `pytest --cov=src --cov-fail-under=80`
- **DevOps Use Case**: CI/CD pipelines use this command to instantly block and reject Developer Pull Requests if they didn't write enough tests.

### 77. What is `pdb`?
- **Definition**: The Python Debugger, an interactive source code debugger.
- **Example**: `import pdb; pdb.set_trace()`
- **DevOps Use Case**: Dropping into a live interactive shell to inspect exactly why a complex JSON payload from Kubernetes is causing a `KeyError`.

### 78. What is Python Packaging (`setup.py`)?
- **Definition**: A file used to configure how a Python project is built and installed.
- **Example**: `pip install -e .`
- **DevOps Use Case**: Packaging your automation script so the team can run `devops-tool deploy` natively in the terminal instead of `python main.py deploy`.

### 79. What is a Traceback?
- **Definition**: The stack trace printed when Python encounters an unhandled exception.
- **Example**: `Traceback (most recent call last): File "script.py", line 5...`
- **DevOps Use Case**: The primary artifact a DevOps engineer reads in CloudWatch or Datadog logs to pinpoint exactly which line of code crashed.

### 80. How do you implement Retries natively?
- **Definition**: Using loops and `time.sleep()`, or advanced libraries like `tenacity`.
- **Example**: `for _ in range(3): try: ping(); break except: sleep(5)`
- **DevOps Use Case**: Cloud environments are volatile. A momentary network blip shouldn't kill a 30-minute deployment pipeline. Retries save pipelines.

### 81. How do you hash a string/file in Python?
- **Definition**: Using the `hashlib` module.
- **Example**: `hashlib.md5(b"password").hexdigest()`
- **DevOps Use Case**: Calculating the MD5 checksum of a compiled binary or backup zip file before and after uploading it to S3 to verify file integrity.

### 82. What is Base64 encoding?
- **Definition**: Encoding binary data into ASCII strings using the `base64` module.
- **Example**: `base64.b64encode(b"secret")`
- **DevOps Use Case**: Kubernetes Secrets require all values to be Base64 encoded before being submitted to the API server via Python.

### 83. What is the `datetime` module?
- **Definition**: Classes for manipulating dates and times.
- **Example**: `datetime.now().strftime("%Y-%m-%d")`
- **DevOps Use Case**: Appending timestamps to backup files (e.g., `db_backup_2026-09-12.sql`) or measuring how long a deployment took.

### 84. What is a Decorator?
- **Definition**: A function that takes another function and extends its behavior without explicitly modifying it.
- **Example**: `@app.route("/")` in Flask.
- **DevOps Use Case**: Creating a custom `@retry` decorator that can be attached to any flaky AWS or HTTP function to automatically retry it 3 times.

### 85. What is the `__init__.py` file?
- **Definition**: A file that marks a directory as a Python package.
- **Example**: `devops/__init__.py`
- **DevOps Use Case**: Essential for organizing massive automation repositories so you can import modules cleanly across different folders.

### 86. What is the difference between `sys.exit(0)` and `sys.exit(1)`?
- **Definition**: `0` means the script completed successfully. `1` (or any non-zero) means it failed.
- **Example**: `if error: sys.exit(1)`
- **DevOps Use Case**: Jenkins and GitHub Actions strictly monitor the exit code. If your Python script prints "Error" but exits with `0`, the pipeline will falsely report Success!

### 87. How do you handle heavy parallel tasks in Python?
- **Definition**: Using `concurrent.futures` (ThreadPoolExecutor or ProcessPoolExecutor).
- **Example**: `with ThreadPoolExecutor(max_workers=5) as executor:`
- **DevOps Use Case**: SSHing into or fetching health checks from 500 EC2 instances simultaneously. Doing it synchronously would take hours; threading takes seconds.

### 88. What is the Global Interpreter Lock (GIL)?
- **Definition**: A mutex in CPython that prevents multiple native threads from executing Python bytecodes at once.
- **Example**: Limits CPU-bound threading efficiency.
- **DevOps Use Case**: Understand that for Network/I-O tasks (like making 100 API calls to AWS), Threading is great. For heavy CPU tasks, you must use Multiprocessing.

### 89. How do you find differences between two lists?
- **Definition**: Converting them to `sets` and using the `-` operator.
- **Example**: `missing = set(list_a) - set(list_b)`
- **DevOps Use Case**: Comparing a list of "Servers running in AWS" vs "Servers listed in our Database" to find unregistered/rogue infrastructure.

### 90. How do you read a large CSV file?
- **Definition**: Using the `csv` module or `pandas`.
- **Example**: `import csv; reader = csv.DictReader(file)`
- **DevOps Use Case**: Parsing legacy infrastructure reports or billing data provided by finance teams to automate cost-saving alerts.

### 91. What is the difference between `json.dump` and `json.dumps`?
- **Definition**: `dump` writes directly to a File object. `dumps` (dump string) returns the JSON as a string variable.
- **Example**: `json.dump(data, file_object)`
- **DevOps Use Case**: Use `dumps` to prepare a payload for an HTTP POST request, and `dump` to write a backup configuration to the filesystem.

### 92. Why use `python -m pip` instead of just `pip`?
- **Definition**: It executes `pip` using the exact Python interpreter you are currently invoking.
- **Example**: `python3.12 -m pip install boto3`
- **DevOps Use Case**: Linux servers often have multiple Python versions installed. Using `-m pip` guarantees you are installing the package for the correct version.

### 93. What is Duck Typing?
- **Definition**: "If it walks like a duck and quacks like a duck, it's a duck." Python cares about an object's *behavior* (methods), not its strict *type*.
- **Example**: Passing a File object or a Network Stream object to a function; as long as both have a `.read()` method, it works.
- **DevOps Use Case**: Writing highly flexible automation functions that can accept data streams from either a local file or a direct HTTP request indiscriminately.

### 94. How do you run Python inside a CI/CD pipeline efficiently?
- **Definition**: Caching dependencies to speed up the run.
- **Example**: Using `actions/setup-python` with `cache: 'pip'` in GitHub Actions.
- **DevOps Use Case**: Reducing pipeline execution time from 5 minutes to 30 seconds by not re-downloading `boto3` and `kubernetes` packages on every PR push.

### 95. What are f-strings?
- **Definition**: Formatted string literals (Python 3.6+) that evaluate expressions inside `{}`.
- **Example**: `f"Deploying to {env}"`
- **DevOps Use Case**: The cleanest, fastest way to inject variables into dynamic SQL queries, API endpoints, or shell commands inside a script.

### 96. What is a Memory Leak in Python?
- **Definition**: When objects are no longer needed but are still referenced, preventing the Garbage Collector from freeing RAM.
- **Example**: Appending massive log data to a global list inside a `while True` loop forever.
- **DevOps Use Case**: Long-running background DevOps agents (like custom autoscalers) will eventually crash the server if they accumulate memory leaks.

### 97. How do you validate an IP address in Python?
- **Definition**: Using the `ipaddress` module.
- **Example**: `ipaddress.ip_address("192.168.1.1")`
- **DevOps Use Case**: Writing an automation script that updates AWS Security Groups and securely validating user input to prevent bad formatting or injection attacks.

### 98. How do you secure Python source code?
- **Definition**: You cannot completely hide Python source code (it's interpreted). You secure the environment and the data it processes.
- **Example**: Utilizing IAM, TLS, `.env`, and restricted permissions.
- **DevOps Use Case**: Treating automation scripts as trusted actors. If a script has permissions to delete EC2 instances, you lock down access to the repository and the Jenkins runner executing it.

### 99. What is a "Wheel" (`.whl`) file?
- **Definition**: A built-package format for Python that speeds up installation compared to source distributions.
- **Example**: `pip install package.whl`
- **DevOps Use Case**: Pre-compiling your custom DevOps tools into wheels and hosting them in an internal JFrog/Nexus registry for secure, rapid enterprise deployment.

### 100. Why did you choose Python over Bash for DevOps?
- **Definition / Golden Answer**: 
> "Bash is excellent for simple, linear server configurations. However, I choose Python when the automation becomes complex. Python offers robust **Exception Handling** (so the script doesn't blindly continue after a failure), massive SDKs (like **Boto3** and **Kubernetes**), the ability to safely parse complex **JSON/YAML**, native **Testing frameworks (pytest)**, and modular **Object-Oriented** designs. Python transforms brittle scripts into resilient, testable, and maintainable software engineering solutions."

---

## 🏆 Bonus: Senior Architect Level Questions

If you are interviewing for a Senior or Lead DevOps role, expect questions that push beyond the standard libraries into architecture and scaling.

### 101. How do you scale Python automation? (Concurrency)
- **Definition**: Using `asyncio`, `threading`, or `multiprocessing` to run tasks simultaneously.
- **Example**: `with ThreadPoolExecutor(max_workers=50) as executor:`
- **DevOps Use Case**: Fetching health data from 10,000 servers. Doing it synchronously in a `for` loop would take hours. Using Threading (because network requests are I/O bound) completes it in seconds.

### 102. How does Python integrate with Terraform or Ansible?
- **Definition**: Interacting with Infrastructure-as-Code platforms programmatically.
- **Example**: Wrapping `terraform apply -auto-approve` using the `subprocess` module.
- **DevOps Use Case**: Ansible is entirely written in Python. A Senior DevOps engineer can write custom Ansible Modules in Python when a built-in module doesn't exist for a proprietary internal tool.

### 103. How do you prevent Injection Attacks in Python?
- **Definition**: Sanitizing inputs before passing them to external systems.
- **Example**: `subprocess.run(["ping", user_ip], shell=False)`
- **DevOps Use Case**: If you use `shell=True`, a malicious user could pass `8.8.8.8; rm -rf /` to your Slack Bot, causing command injection on your Jenkins runner. Always use `shell=False`.

### 104. How do you trigger CI/CD pipelines programmatically?
- **Definition**: Using specialized SDKs to interface with CI/CD platforms rather than just raw webhooks.
- **Example**: `import gitlab; gl = gitlab.Gitlab(url, private_token='secret')`
- **DevOps Use Case**: Using the `python-gitlab` or `jenkinsapi` libraries to build a massive Python orchestration script that triggers 50 distinct microservice deployment pipelines sequentially.

### 105. Why shouldn't you use `pickle` for sharing data?
- **Definition**: `pickle` serializes Python objects into a binary format, but it can execute arbitrary code upon un-pickling.
- **Example**: Attackers craft a malicious pickle payload that spawns a reverse shell.
- **DevOps Use Case**: If two automation servers need to share state or configuration data, **never** use `pickle`. Always serialize the data safely using **JSON** or **YAML**.
