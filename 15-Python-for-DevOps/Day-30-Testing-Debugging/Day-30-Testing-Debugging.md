# Python Day 30: Testing & Debugging in Python

Welcome to **Day 30**, the grand finale! 
In DevOps, an untested automation script is a ticking time bomb. If you write a script to delete unused AWS EC2 instances, and a bug causes it to delete production instances, the consequences are catastrophic. Today, you learn how to make your code bulletproof using `pytest` and `mocking`.

---

## 1. Pytest Fundamentals
`pytest` is the industry standard testing framework for Python. 
Files should be named `test_*.py` and functions should be named `test_*`.

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Testing standard logic
def test_divide_success():
    assert divide(10, 2) == 5

# Testing exceptions
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

---

## 2. Advanced Testing: Fixtures & Parameterization
Instead of writing the same test 50 times, use **Parameterization**. 
Instead of redefining a mock server dictionary in every test, use **Fixtures**.

```python
import pytest

@pytest.fixture
def mock_server():
    return {"name": "web-01", "status": "running"}

def test_server_status(mock_server):
    assert mock_server["status"] == "running"

@pytest.mark.parametrize("a, b, expected", [(1, 2, 3), (10, -5, 5), (0, 0, 0)])
def test_addition(a, b, expected):
    assert a + b == expected
```

---

## 3. DevOps Mocking (`unittest.mock`)
You **never** want your unit tests to actually hit AWS or Kubernetes. They cost money, require credentials, and might accidentally destroy real infrastructure. You must **Mock** the external system.

```python
import requests
from unittest.mock import patch

def get_status(url):
    response = requests.get(url)
    if response.status_code == 200:
        return "UP"
    return "DOWN"

# We mock the 'requests.get' function inside the module we are testing
@patch("module_name.requests.get")
def test_get_status_success(mock_get):
    # We fake the API response so we don't actually hit the internet!
    mock_get.return_value.status_code = 200
    assert get_status("https://fake.url") == "UP"
```

---

## 4. Advanced DevOps: Mocking AWS with `moto`
While `unittest.mock` is great for simple APIs, mocking AWS `boto3` manually is a nightmare because AWS returns massive, complex JSON dictionaries.
Instead, DevOps engineers use **Moto** (`pip install moto`). Moto intercepts Boto3 calls and routes them to a fake, local AWS environment running in your RAM!

```python
import boto3
from moto import mock_aws

@mock_aws
def test_s3_bucket_creation():
    # 1. This connects to Moto's fake AWS, not the real internet!
    s3 = boto3.client("s3", region_name="us-east-1")
    
    # 2. We can create buckets and upload files instantly and for free
    s3.create_bucket(Bucket="my-test-bucket")
    
    # 3. Verify our code works
    response = s3.list_buckets()
    assert len(response["Buckets"]) == 1
    assert response["Buckets"][0]["Name"] == "my-test-bucket"
```

---

## 5. Advanced DevOps: Code Coverage (`pytest-cov`)
Writing tests is great, but how do you know if you tested *everything*? 
In a CI/CD pipeline, DevOps engineers use `pytest-cov` to measure **Code Coverage**. You can configure GitHub Actions to instantly fail a pull request if the test coverage drops below 80%!

**Installation:**
```bash
pip install pytest-cov
```

**CI/CD Execution Command:**
```bash
# This command runs tests, measures coverage in the 'monitor.py' file, 
# and returns an exit code of 1 (failing the pipeline) if coverage is under 80%
pytest --cov=monitor --cov-fail-under=80
```

---

## 6. Debugging (`pdb`)
When an automation script fails, don't just scatter `print()` statements everywhere. Use Python's built-in debugger (`pdb`).

```python
import pdb

x = 10
y = 0

# The script will pause here, allowing you to inspect variables in the terminal!
pdb.set_trace() 
result = x / y
```

*Commands: `n` (next), `c` (continue), `p x` (print variable x).*

---

## 🧑‍💻 Practice Exercises
We have created `monitor.py` and `test_monitor.py` in this folder. 
This is a complete, CI/CD-ready test suite. It uses `@patch` to mock `requests.get`, simulating what happens when an API is Healthy (200), Down (500), or completely Unreachable (`RequestException`) without ever needing the internet!
