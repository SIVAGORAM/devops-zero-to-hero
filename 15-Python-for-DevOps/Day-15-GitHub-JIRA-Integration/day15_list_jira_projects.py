#!/usr/bin/env python3

"""
==========================================
Day 15 Project: GitHub-JIRA Integration
Script 1: GET Request (List Projects)
==========================================
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import os

def list_jira_projects():
    print("--- Fetching JIRA Projects ---")
    
    # Replace with your actual JIRA domain
    url = "https://your-domain.atlassian.net/rest/api/3/project"

    # Best Practice: Load from Environment Variable
    # For testing, you can temporarily hardcode this, but DO NOT commit it!
    api_token = os.getenv("JIRA_API_TOKEN", "your-temporary-token-here")
    email = "your-email@example.com"
    
    auth = HTTPBasicAuth(email, api_token)

    # Tell the API we expect JSON back
    headers = {
        "Accept": "application/json"
    }

    try:
        # Make the GET request
        response = requests.request("GET", url, headers=headers, auth=auth)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON string into a Python List of Dictionaries
            projects = json.loads(response.text)
            
            if projects:
                # Extract the name of the first project found
                first_project_name = projects[0]["name"]
                print(f"[SUCCESS] Found project: {first_project_name}")
            else:
                print("[INFO] No projects found in this JIRA workspace.")
        else:
            print(f"[ERROR] Failed to fetch data. HTTP Status: {response.status_code}")
            print(f"Details: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"[FATAL] Network error occurred: {e}")

if __name__ == "__main__":
    list_jira_projects()
