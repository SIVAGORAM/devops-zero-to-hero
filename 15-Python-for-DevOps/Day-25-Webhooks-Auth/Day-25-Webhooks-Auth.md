# Python Day 25: API Authentication & Webhooks

Welcome to **Day 25**! 
Yesterday we learned how Python can talk to external APIs. Today, we flip the architecture: **How do external tools talk to Python?**

The answer is **Webhooks**. When combined with **Secure API Authentication**, you can build a complete, bi-directional DevOps automation pipeline!

---

## 1. Authentication vs Authorization
Before we make APIs talk to each other, we must secure them.
- **Authentication**: *Who are you?* (e.g. Validating a username/password or API Token)
- **Authorization**: *What are you allowed to do?* (e.g. You are authenticated, but you only have `Read` access, not `Delete` access)

### The 3 Core Authentication Types in Requests
```python
import requests

# 1. Bearer Token (Modern Standard)
headers = {"Authorization": "Bearer my_secret_token"}
requests.get("https://api.example.com", headers=headers)

# 2. API Key (Usually passed in headers)
headers = {"X-API-Key": "my_secret_token"}
requests.get("https://api.example.com", headers=headers)

# 3. HTTP Basic Auth (Legacy Standard)
requests.get("https://api.example.com", auth=("username", "password"))
```

---

## 2. Managing Secrets Securely
> [!CAUTION]
> **Never hardcode secrets in Python scripts!**
> If you write `token = "ghp_12345"` in your code and push it to GitHub, bots will steal it within 5 seconds and spin up $10,000 of Bitcoin miners on your AWS account.

Always use Environment Variables or the `python-dotenv` package.
```python
# pip install python-dotenv
import os
from dotenv import load_dotenv

load_dotenv() # Automatically loads variables from a local `.env` file

api_token = os.getenv("API_TOKEN") # Safely retrieved!
```

---

## 3. What is a Webhook?
Instead of your Python script polling GitHub every 5 seconds asking *"Is there a new pull request?"*, GitHub can instantly send an HTTP `POST` request to your Python server the exact millisecond a pull request is created.

**Polling:** Python → GitHub
**Webhook:** GitHub → Python

### The Webhook Receiver (Flask)
We use the `Flask` micro-framework to listen for Webhooks.
```python
from flask import Flask, request

app = Flask(__name__)

# Listen for incoming POST requests from GitHub
@app.route("/github-webhook", methods=["POST"])
def webhook():
    # Parse the incoming JSON Payload
    data = request.get_json()
    print("Received Webhook Event:", data.get("action"))
    return {"status": "success"}, 200

if __name__ == "__main__":
    app.run(port=5000)
```

---

## 4. Webhook Security
If your Python server is exposed to the internet, **anyone** can send a fake HTTP POST request to `/github-webhook` and trigger your automation.

You must configure a **Webhook Secret** in GitHub, and your Python script must verify it.

```python
@app.route("/webhook", methods=["POST"])
def webhook():
    expected_secret = os.getenv("WEBHOOK_SECRET")
    received_secret = request.headers.get("X-Webhook-Secret")
    
    if received_secret != expected_secret:
        return {"error": "Unauthorized: Invalid Secret!"}, 401
```

---

## 5. Idempotency
If GitHub times out waiting for your Python script to reply, it might send the exact same Webhook again.
**Idempotency** means designing your script so that processing the identical webhook twice does not result in creating two duplicate Jira tickets!

---

## 🧑‍💻 Practice Exercises
We have created `day25_webhook_jira_integration.py` in this folder. 
It demonstrates the Holy Grail of DevOps Integration: **Event-Driven Architecture**. 
It spins up a secure Flask Webhook receiver. When it receives a simulated payload from GitHub, it validates the secret, and securely fires an authenticated API call to Jira to generate an Incident Ticket!
