#!/usr/bin/env python3

"""
==========================================
Day 15 Project: GitHub-JIRA Integration
Script 2: POST Request (Create Ticket)
==========================================
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import os

def create_jira_ticket(summary_text, description_text):
    print(f"--- Creating JIRA Ticket: {summary_text} ---")
    
    # Replace with your actual JIRA domain
    url = "https://your-domain.atlassian.net/rest/api/3/issue"

    # Best Practice: Load from Environment Variable
    api_token = os.getenv("JIRA_API_TOKEN", "your-temporary-token-here")
    email = "your-email@example.com"
    
    auth = HTTPBasicAuth(email, api_token)

    # Tell the API we are sending JSON, and we expect JSON back
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Construct the highly nested JSON Payload expected by JIRA's V3 API
    payload = json.dumps({
        "fields": {
            "project": {
                "key": "AB" # Replace with your actual JIRA Project Key
            },
            "summary": summary_text,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description_text
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "id": "10006" # Task issue type ID (May vary by workspace)
            }
        },
        "update": {}
    })

    try:
        # Make the POST request
        response = requests.request("POST", url, data=payload, headers=headers, auth=auth)
        
        # HTTP 201 means "Created successfully"
        if response.status_code == 201:
            print("[SUCCESS] Ticket created successfully!")
            
            # Format and print the JSON response beautifully
            response_dict = json.loads(response.text)
            formatted_json = json.dumps(response_dict, sort_keys=True, indent=4)
            print("Response Data:")
            print(formatted_json)
        else:
            print(f"[ERROR] Failed to create ticket. HTTP Status: {response.status_code}")
            print(f"Details: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"[FATAL] Network error occurred: {e}")

if __name__ == "__main__":
    # Simulated Webhook Trigger Data
    github_comment = "Bug: Server crashes on startup."
    ticket_title = "Automated Bug Report from GitHub"
    
    create_jira_ticket(ticket_title, github_comment)
