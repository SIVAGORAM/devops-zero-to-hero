#!/usr/bin/env python3

import requests

# ==========================================
# Day 12 Project: GitHub API Integration
# Note: You must run `pip install requests` to run this script!
# ==========================================

def get_kubernetes_pr_creators():
    print("Fetching active Pull Requests from the Kubernetes repository...\n")
    
    # URL to fetch pull requests from the GitHub API
    url = 'https://api.github.com/repos/kubernetes/kubernetes/pulls'
    
    try:
        # Make a GET request to fetch pull requests data
        # Note: Unauthenticated requests are heavily rate-limited by GitHub
        response = requests.get(url, timeout=10)
        
        # Only process if the response is HTTP 200 OK
        if response.status_code == 200:
            
            # Convert the JSON response into a Python List of Dictionaries
            pull_requests = response.json()
            
            # Create an empty dictionary to store PR creators and their counts
            pr_creators = {}
            
            # Iterate through each pull request
            for pull in pull_requests:
                # Extract the creator's username from the nested JSON
                creator = pull['user']['login']
                
                # If the creator is already in our dictionary, increment their count
                if creator in pr_creators:
                    pr_creators[creator] += 1
                # If this is their first PR, add them to the dictionary with a count of 1
                else:
                    pr_creators[creator] = 1
            
            # Display the resulting dictionary using .items()
            print("--- PR Creators and Counts ---")
            for creator, count in pr_creators.items():
                print(f"User: {creator} | PRs: {count}")
                
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"FATAL: Network error occurred while contacting GitHub API:\n{e}")

if __name__ == "__main__":
    get_kubernetes_pr_creators()
