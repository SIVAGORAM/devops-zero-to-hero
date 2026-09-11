#!/usr/bin/env python3

"""
==========================================
Day 16 Project: GitHub-JIRA Integration
Script 2: Flask Webhook Listener
==========================================
Note: Run `pip install flask requests` before executing!
"""

import os
import json
import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, request

# Initialize Flask Application
app = Flask(__name__)

# Define the Route that GitHub Webhooks will hit
# We strictly only allow POST requests
@app.route('/createJira', methods=['POST'])
def createJira():
    print("\n[WEBHOOK RECEIVED] Incoming request on /createJira!")
    
    # In a real environment, you would extract the GitHub comment text dynamically:
    # github_payload = request.json
    # comment_text = github_payload['comment']['body']
    
    # ----------------------------------------------------
    # PHASE 2: Send Request to JIRA
    # ----------------------------------------------------
    print("[JIRA] Formulating JIRA REST API Request...")
    
    # Replace with your actual JIRA domain
    url = "https://your-domain.atlassian.net/rest/api/3/issue"

    # Best Practice: Load from Environment Variable
    api_token = os.getenv("JIRA_API_TOKEN", "your-temporary-token-here")
    email = "your-email@example.com"
    
    auth = HTTPBasicAuth(email, api_token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Construct the JSON Payload for JIRA
    payload = json.dumps({
        "fields": {
            "project": {
                "key": "AB"
            },
            "summary": "Automated Ticket via Flask Webhook",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "This ticket was triggered by a GitHub Webhook hitting our Flask Server!"
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "id": "10006"
            }
        },
        "update": {}
    })

    try:
        # Make the POST request to JIRA
        print("[JIRA] Sending POST request...")
        response = requests.request("POST", url, data=payload, headers=headers, auth=auth)
        
        # Check if JIRA successfully created the ticket
        if response.status_code == 201:
            print("[SUCCESS] Ticket created successfully in JIRA!")
            
            # Format the JIRA response and return it to GitHub as the Webhook Response
            formatted_response = json.dumps(json.loads(response.text), sort_keys=True, indent=4)
            return formatted_response, 201
            
        else:
            print(f"[ERROR] JIRA returned Status {response.status_code}")
            return f"Failed to create ticket: {response.text}", 500
            
    except requests.exceptions.RequestException as e:
        print(f"[FATAL] Network error occurred: {e}")
        return "Internal Server Error", 500

# Start the Flask Webhook Server
if __name__ == '__main__':
    print("Starting Flask Webhook Server...")
    print("Listening for GitHub POST requests at: http://localhost:5000/createJira")
    app.run(host='0.0.0.0', port=5000)
