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

### Level 1: Simple Secret Validation
You can configure a Custom Header in your webhook provider.
```python
@app.route("/webhook", methods=["POST"])
def webhook():
    expected_secret = os.getenv("WEBHOOK_SECRET")
    received_secret = request.headers.get("X-Webhook-Secret")
    
    if received_secret != expected_secret:
        return {"error": "Unauthorized: Invalid Secret!"}, 401
```

### Level 2: Advanced DevOps (HMAC Signatures)
The simple secret check above is prone to timing attacks. The industry standard (used by GitHub Enterprise, Stripe, and Slack) is **HMAC Signatures**. 
The provider hashes the entire JSON payload using your secret key and sends the hash in a header (e.g., `X-Hub-Signature-256`). You must recalculate the hash locally and compare them securely!

```python
import hmac
import hashlib

@app.route("/github-webhook", methods=["POST"])
def secure_webhook():
    secret = os.getenv("GITHUB_WEBHOOK_SECRET").encode('utf-8')
    payload = request.get_data() # Get raw bytes, not parsed JSON
    
    # Calculate what the signature SHOULD be
    expected_hash = "sha256=" + hmac.new(secret, payload, hashlib.sha256).hexdigest()
    
    # Get what GitHub says the signature is
    received_hash = request.headers.get("X-Hub-Signature-256")
    
    # Compare them securely to prevent timing attacks!
    if not hmac.compare_digest(expected_hash, received_hash):
        return {"error": "Unauthorized: Signature Mismatch!"}, 401
```

---

## 5. Advanced DevOps: Testing Webhooks Locally (`ngrok`)
If your Flask server is running on `http://localhost:5000`, GitHub cannot reach it to send the webhook (because `localhost` is on your private Wi-Fi network).

DevOps engineers use a tool called **ngrok** to create a secure, temporary public URL that tunnels directly to their local machine.

```bash
# 1. Download and start ngrok in your terminal
ngrok http 5000

# 2. ngrok gives you a public URL:
# Forwarding  https://a1b2-c3d4.ngrok.app -> http://localhost:5000

# 3. Paste https://a1b2-c3d4.ngrok.app/github-webhook into GitHub's Webhook Settings!
```

---

## 6. Idempotency
If GitHub times out waiting for your Python script to reply, it might send the exact same Webhook again.
**Idempotency** means designing your script so that processing the identical webhook twice does not result in creating two duplicate Jira tickets!

---

## 🧑‍💻 Practice Exercises
We have created `day25_webhook_jira_integration.py` in this folder. 
It demonstrates the Holy Grail of DevOps Integration: **Event-Driven Architecture**. 
It spins up a secure Flask Webhook receiver. When it receives a simulated payload from GitHub, it validates the secret, and securely fires an authenticated API call to Jira to generate an Incident Ticket!
