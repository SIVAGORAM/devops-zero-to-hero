#!/usr/bin/env python3

# ==========================================
# Day 25 Practice: API Auth & Webhooks
# Scenario: Event-Driven GitHub -> Jira Ticket
# Requirements: pip install flask requests python-dotenv
# ==========================================

import os
import logging
import requests
from flask import Flask, request, jsonify
# Note: You would normally run `from dotenv import load_dotenv; load_dotenv()` here
# to load secrets from a local .env file.

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

app = Flask(__name__)

# ==========================================
# 1. OUTBOUND AUTHENTICATION (Creating the Jira Ticket)
# ==========================================
def create_jira_ticket(action: str, repo: str, user: str):
    """Fires an authenticated API request to Jira to log the event."""
    
    jira_url = os.getenv("JIRA_URL", "https://example.atlassian.net")
    jira_user = os.getenv("JIRA_EMAIL", "devops@example.com")
    jira_token = os.getenv("JIRA_API_TOKEN", "mock_token")
    
    # In a real scenario, this payload exactly matches Jira's REST API Schema
    payload = {
        "fields": {
            "project": {"key": "DEVOPS"},
            "summary": f"GitHub Event: {action} on {repo}",
            "description": f"Triggered by user: {user}",
            "issuetype": {"name": "Task"}
        }
    }
    
    try:
        logging.info("Routing event to Jira API...")
        # Using HTTP Basic Auth for the Outbound API Call
        response = requests.post(
            f"{jira_url}/rest/api/3/issue",
            json=payload,
            auth=(jira_user, jira_token),
            timeout=10
        )
        
        # If this is a mock run, the request will fail (which is fine for this demo)
        if response.ok:
            logging.info("Successfully generated Jira Ticket!")
        else:
            logging.warning("Jira API returned: %s - %s", response.status_code, response.text)
            
    except requests.exceptions.RequestException as e:
        logging.error("Failed to reach Jira API: %s", e)


# ==========================================
# 2. INBOUND AUTHENTICATION (The Webhook Receiver)
# ==========================================
@app.route("/github-webhook", methods=["POST"])
def github_webhook():
    logging.info("--- INCOMING WEBHOOK DETECTED ---")
    
    # 1. Security Check: Validate the Webhook Secret
    expected_secret = os.getenv("WEBHOOK_SECRET", "my_super_secret")
    received_secret = request.headers.get("X-Webhook-Secret")
    
    if received_secret != expected_secret:
        logging.error("SECURITY ALERT: Invalid Webhook Secret provided!")
        # Return 401 Unauthorized
        return jsonify({"error": "Unauthorized"}), 401
        
    # 2. Extract Data
    data = request.get_json()
    action = data.get("action", "unknown")
    repo = data.get("repository", {}).get("name", "unknown")
    sender = data.get("sender", {}).get("login", "unknown")
    
    logging.info("Validated Webhook Event | Repo: %s | Action: %s | User: %s", repo, action, sender)
    
    # 3. Trigger Outbound Automation
    create_jira_ticket(action, repo, sender)
    
    # Return 200 OK so GitHub knows we successfully processed it
    return jsonify({"status": "Automation Triggered Successfully"}), 200


if __name__ == "__main__":
    logging.info("Starting Webhook Receiver on Port 5000...")
    logging.info("To test this, run the following curl command in another terminal:")
    logging.info("""
    curl -X POST http://localhost:5000/github-webhook \\
    -H "Content-Type: application/json" \\
    -H "X-Webhook-Secret: my_super_secret" \\
    -d '{"action":"opened","repository":{"name":"infrastructure-as-code"},"sender":{"login":"siva-devops"}}'
    """)
    app.run(host="0.0.0.0", port=5000)
