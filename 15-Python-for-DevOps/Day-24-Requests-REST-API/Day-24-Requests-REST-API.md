# Python Day 24: Requests & REST API Advanced

Welcome to **Day 24**! 
A DevOps engineer rarely manages servers manually anymore. Instead, they write Python scripts that talk to the REST APIs of tools like AWS, GitHub, Jenkins, Jira, and Kubernetes.

The bridge between Python and these cloud systems is the `requests` library.

---

## 1. The Core HTTP Methods
When interacting with a REST API, you must tell it *what action* you want to perform:

| Method | Action | DevOps Example |
| :--- | :--- | :--- |
| `GET` | Retrieve data | Get a list of running Docker containers |
| `POST` | Create data | Trigger a new Jenkins build |
| `PUT` | Replace data | Update a Kubernetes deployment manifest |
| `PATCH` | Partially update | Change the status of a Jira ticket |
| `DELETE` | Delete data | Terminate an AWS EC2 instance |

---

## 2. Basic Requests: `params` vs `json`
When talking to an API, you pass data in two main ways.

### `params`: URL Query Parameters
Use this for `GET` requests to filter or paginate data (e.g. `?state=open&page=1`).
```python
import requests

response = requests.get(
    "https://api.github.com/repos/kubernetes/kubernetes/pulls",
    params={"state": "open", "per_page": 10}
)
```

### `json`: The Request Body
Use this for `POST` and `PUT` requests when sending data to the server.
```python
payload = {"summary": "Deployment failed", "issuetype": "Bug"}

# Requests automatically converts the dictionary to a JSON string and sets the headers!
response = requests.post("https://jira.example.com/api/issue", json=payload)
```

---

## 3. The DevOps Standard: Handling Failures
If you send an API request and the server crashes, your Python script should not blindly continue.

### Rule 1: Always use `timeout`
If a server hangs, your script will wait forever. ALWAYS pass a timeout.
```python
requests.get("https://api.example.com", timeout=10) # Fails if it takes > 10s
```

### Rule 2: Always use `raise_for_status()`
Instead of manually checking `if response.status_code == 200:`, just tell Python to crash if the API returns a `4xx` (Client Error) or `5xx` (Server Error).
```python
response = requests.get(url, timeout=10)
response.raise_for_status() # Automatically raises an exception on HTTP errors
data = response.json()      # Safely parse JSON knowing the request succeeded
```

### Rule 3: Catch `RequestException`
Wrap your calls in a try-except block to catch timeouts, DNS failures, or HTTP errors.
```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"API Call Failed: {e}")
```

---

## 4. Advanced DevOps: Sessions and Authentication
If you are making 50 requests to Jenkins, don't open 50 separate connections and pass the API token 50 times. Use a **Session** to pool connections and persist headers!

> [!CAUTION]
> **Never hardcode API Tokens!**
> Always read tokens from Environment Variables using `os.getenv()`.

```python
import requests
import os

# 1. Create a persistent session
session = requests.Session()

# 2. Attach our secret token and headers ONCE
api_token = os.getenv("GITHUB_TOKEN")
session.headers.update({
    "Authorization": f"Bearer {api_token}",
    "Accept": "application/json"
})

# 3. All subsequent requests automatically use those headers!
res1 = session.get("https://api.github.com/user")
res2 = session.get("https://api.github.com/user/repos")
```

---

## 5. Advanced DevOps: Pagination
APIs don't return 10,000 records at once. They return "pages" of data. You must loop through them!

```python
for page in range(1, 4): # Fetch pages 1, 2, and 3
    response = requests.get(url, params={"page": page, "limit": 100})
    data = response.json()
    
    if not data: 
        break # Exit loop if the page is empty!
        
    for item in data:
        print(item["name"])
```

---

## 6. Advanced DevOps: Internal Servers & SSL Certificates
DevOps engineers often talk to internal company servers (like an internal Jenkins or SonarQube instance) that use **Self-Signed SSL Certificates**. By default, `requests` will crash and throw an `SSLError` because it doesn't trust the certificate.

You can bypass this by passing `verify=False`.

> [!WARNING]
> Only do this for internal servers you completely trust! Never do this on the public internet.

```python
import requests
import urllib3

# Suppress the massive warning Python prints when you bypass SSL verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Pass verify=False to ignore the self-signed certificate error
response = requests.get("https://internal-jenkins.company.local", verify=False)
```

---

## 7. Advanced DevOps: Legacy Basic Authentication
While modern APIs use Bearer Tokens, many legacy systems (like older Jenkins servers or Router APIs) require HTTP Basic Authentication (Username + Password). You don't need to manually base64-encode this in the headers; `requests` has a built-in `auth` parameter!

```python
import requests
import os

username = "admin"
password = os.getenv("JENKINS_PASS")

# Requests automatically encodes this into an HTTP Basic Auth header
response = requests.get("https://jenkins.local/api", auth=(username, password), verify=False)
```

---

## 🧑‍💻 Practice Exercises
We have created `day24_github_api_automation.py` in this folder. 
It demonstrates a robust, Object-Oriented DevOps API Client! It uses `requests.Session`, injects Headers safely, implements Retries, handles Exceptions, and fetches Repository stats and paginated Pull Requests from GitHub!
