# Python Day 16: Building Webhooks with Flask (Project 4 - Part 2)

Welcome to **Day 16**! In the previous module, we learned how to make our Python script *send* requests to JIRA. Today, we learn how to make our Python script *receive* requests from GitHub!

To do this, we must upgrade our simple Python scripts into a **Python Web Application** using **Flask**.

---

## 1. Introduction to Flask
Flask is a lightweight Python web framework. It allows you to build APIs and Web Servers with just a few lines of code.

*(You must install it via `pip install flask`)*

### The Basic Flask App (`hello_world.py`)
```python
from flask import Flask

# Initialize the Flask Web Application
app = Flask(__name__)

# Define the Route (URL)
@app.route('/')
def hello_world():
    return 'Hello, DevOps!'

if __name__ == '__main__':
    # Start the server!
    app.run(host="0.0.0.0", port=5000)
```
When you run this script, your Python code stays running forever! If you open your browser to `http://localhost:5000/`, it will trigger the `hello_world()` function and return "Hello, DevOps!".

---

## 2. Important Flask Concepts

| Concept | Explanation |
| :--- | :--- |
| **`@app.route('/createJira')`** | Defines the API Endpoint URL. If someone goes to `/createJira`, this function runs. |
| **`methods=['POST']`** | Tells Flask to only accept `POST` requests on this route. If someone tries a `GET` request (like opening it in a web browser), Flask blocks it. |
| **`host='0.0.0.0'`** | Tells Flask to listen on ALL network interfaces, allowing external services (like GitHub) to reach your server. |
| **`port=5000`** | The default network port Flask uses. |

---

## 3. The Master DevOps Flow
This is the most critical architecture to understand for DevOps interviews. You must understand the difference between the API *you build* and the API *you consume*.

### The Full Pipeline
```text
                 GITHUB (The Source)
                    |
             Comment Created
                    |
                    ↓
             GitHub Webhook (Sends HTTP POST)
                    |
                    ↓
        ┌────────────────────────┐
        │ FLASK API (Your Code)  │
        │   @app.route('/jira')  │  <-- You built this API!
        │   Receives Webhook     │
        └────────────────────────┘
                    |
                    ↓
             Python Logic (Extracts Comment)
                    |
                    ↓
         JIRA REST API (External) <-- You are consuming this API!
                    |
               (HTTP POST)
                    |
                    ↓
               JIRA TICKET
```

**Flask is our API layer.** It receives the webhook.
**JIRA REST API is the external API.** We send a request to it using the `requests` module.

---

## 4. Advanced DevOps: Webhook Security (HMAC)
> [!CAUTION]
> If your Flask server listens on `0.0.0.0`, **anyone on the internet** can send a POST request to `/createJira` and spam your workspace with fake tickets!

How does your server know the request *actually* came from GitHub and not a hacker?
**HMAC Signatures**.

When you configure a Webhook in GitHub, you provide a **Secret Token**. 
1. GitHub hashes the JSON payload using your Secret Token and sends the hash in the `X-Hub-Signature-256` header.
2. Your Flask server receives the JSON, hashes it with your local copy of the Secret Token, and compares the two hashes.
3. If they match, the request is authentic! If they don't, Flask drops the request with an HTTP 401 Unauthorized.

```python
import hmac
import hashlib

# Example of how DevOps engineers verify Github Webhooks
def verify_signature(payload_body, secret_token, signature_header):
    mac = hmac.new(secret_token.encode(), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)
```

---

## 🧑‍💻 Project 4 (Part 2): The Webhook Listener
We have provided two template scripts in this folder:
1. `day16_hello_flask.py`: The basic Hello World server to test that Flask is working.
2. `day16_github_jira_webhook.py`: The ultimate DevOps script! It runs a Flask server that listens on `/createJira` for incoming POST requests. Once triggered, it automatically fires a new POST request to JIRA to create a ticket!
