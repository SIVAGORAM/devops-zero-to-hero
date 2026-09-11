# Python Day 15: GitHub to JIRA Integration (Project 4)

Welcome to **Day 15**! Today we tackle one of the most highly requested DevOps automations: **Connecting two different tools using REST APIs.**

We will build a workflow that automatically creates a JIRA ticket using Python! This simulates an environment where a developer leaving a comment on a GitHub Pull Request triggers a webhook that runs our Python code.

---

## 1. What is a RESTful API?
A RESTful API allows different applications to talk to each other over HTTP. 
Instead of a human clicking buttons on a website, a Python script sends HTTP requests to an API endpoint.

### Common HTTP Methods
| Method | Purpose | DevOps Use Case |
| :--- | :--- | :--- |
| **GET** | Retrieve data | "Give me a list of all active JIRA projects" |
| **POST** | Create data | "Create a new JIRA ticket" |
| **PUT/PATCH** | Update data | "Change the status of this ticket to 'Done'" |
| **DELETE** | Delete data | "Delete this testing ticket" |

---

## 2. The `requests` Library
Python's `requests` library is the industry standard for making HTTP requests.
*(You must install it via `pip install requests`)*

```python
import requests

url = "https://api.github.com/events"
response = requests.get(url)

print(response.status_code) # 200 = Success
```

### Important Response Properties
- `response.status_code`: Did it work? (200=OK, 401=Unauthorized, 404=Not Found, 500=Server Error)
- `response.text`: The raw text response from the server.
- `response.json()`: Automatically converts a JSON response into a Python Dictionary!

### Advanced DevOps: Handling Rate Limits (HTTP 429)
The most common error DevOps engineers face when automating JIRA or GitHub is **HTTP 429 (Too Many Requests)**. If your script runs too fast, the API will block you. Senior engineers handle this by implementing a "Retry with Backoff" strategy using the `time` module.

```python
import time
import requests

response = requests.get(url)
if response.status_code == 429:
    print("Rate limited! Sleeping for 10 seconds...")
    time.sleep(10)
    # Retry the request...
```

---

## 3. Webhooks & The DevOps Automation Flow
How does GitHub actually trigger a Python script? Using a **Webhook**.

A Webhook is an automated HTTP `POST` request sent from one app to another when an event happens.

### The Pipeline Architecture
1. **Developer:** Leaves a comment on a GitHub Pull Request.
2. **GitHub Webhook:** Sends an automated JSON payload to our Python API.
3. **Python:** Parses the JSON, extracts the comment text.
4. **Python (`requests`):** Sends a `POST` request to the JIRA API with the comment text.
5. **JIRA:** Creates the ticket!

### Advanced DevOps: Receiving Webhooks with Flask
The class notes explain that Python *receives* the Webhook, but how? A script that runs once and exits cannot receive a webhook. You must run a **Web Server**. DevOps engineers typically use the `Flask` micro-framework to build a server that constantly listens for GitHub's POST requests!

```python
# pip install flask
from flask import Flask, request

app = Flask(__name__)

# This URL listens specifically for GitHub Webhooks
@app.route('/github-webhook', methods=['POST'])
def handle_webhook():
    payload = request.json
    print(f"Received comment from GitHub: {payload['comment']['body']}")
    # -> Trigger the JIRA Ticket creation here! <-
    return "Success", 200

if __name__ == '__main__':
    app.run(port=5000)
```

---

## 4. API Authentication
APIs like JIRA require authentication, otherwise anyone could create tickets in your workspace! We use `HTTPBasicAuth` to send our credentials securely.

> [!CAUTION]
> **NEVER hardcode your API Token in your script!**
> If you commit an API token to GitHub, hackers will scrape it in seconds. In the real world, DevOps engineers load these from Environment Variables using `os.getenv("JIRA_API_TOKEN")`.

```python
import os
from requests.auth import HTTPBasicAuth

# Securely load the token from the environment
api_token = os.getenv("JIRA_API_TOKEN")
auth = HTTPBasicAuth("your-email@example.com", api_token)
```

---

## 5. Working with JSON Payloads
When making a `POST` request to create a ticket, you must send a **Payload** (a nested dictionary converted to JSON).

You must also send **Headers** to tell JIRA that you are speaking in JSON.
```python
headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}
```

---

## 🧑‍💻 Project 4: JIRA Automation Scripts
We have provided two template scripts in this folder:
1. `day15_list_jira_projects.py`: Demonstrates a `GET` request to retrieve data from JIRA.
2. `day15_create_jira_ticket.py`: Demonstrates a complex `POST` request with nested JSON payloads to create an issue.

To run these, you would need to replace the placeholder URLs and API tokens with a real JIRA Developer Account!
