#!/usr/bin/env python3

# ==========================================
# Day 24 Practice: Requests & REST API
# Scenario: GitHub DevOps API Automation
# Features: Sessions, Retries, Pagination
# ==========================================

import requests
import time
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

class GitHubAPIClient:
    """A reusable, DevOps-grade REST API Client for GitHub."""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        
        # Create a persistent session for connection pooling
        self.session = requests.Session()
        
        # Safely load token from environment
        token = os.getenv("GITHUB_TOKEN")
        
        # Update session headers globally
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
            logging.info("GitHub Token found. Operating in Authenticated mode.")
        else:
            logging.warning("No GITHUB_TOKEN found. Operating in Unauthenticated mode (Strict Rate Limits applied).")
            
        self.session.headers.update(headers)

    def _make_request(self, endpoint: str, params: dict = None, retries: int = 3) -> dict:
        """Internal helper to make GET requests with robust retry and error handling."""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(retries):
            try:
                # Always use a timeout in production!
                response = self.session.get(url, params=params, timeout=10)
                
                # Check for 429 Rate Limits
                if response.status_code == 429:
                    logging.warning("Rate Limit Exceeded. Backing off...")
                    time.sleep(5)
                    continue
                    
                # Raise exception for 4xx and 5xx errors
                response.raise_for_status()
                
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logging.error("Attempt %s/%s failed: %s", attempt + 1, retries, e)
                if attempt < retries - 1:
                    logging.info("Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    logging.critical("API Request permanently failed for endpoint: %s", endpoint)
                    return None

    def get_repo_stats(self, owner: str, repo: str):
        """Fetches core statistics for a specific repository."""
        logging.info("Fetching repository stats for %s/%s...", owner, repo)
        data = self._make_request(f"/repos/{owner}/{repo}")
        
        if data:
            print("\n========================================")
            print(f" REPOSITORY: {data.get('full_name')}")
            print("========================================")
            print(f" Description : {data.get('description')}")
            print(f" Stars       : {data.get('stargazers_count')}")
            print(f" Forks       : {data.get('forks_count')}")
            print(f" Open Issues : {data.get('open_issues_count')}")
            print("========================================\n")

    def get_open_pull_requests(self, owner: str, repo: str, pages: int = 1):
        """Fetches open pull requests using Pagination logic."""
        logging.info("Fetching Open Pull Requests for %s/%s...", owner, repo)
        
        for page in range(1, pages + 1):
            logging.info("Requesting Page %s...", page)
            
            # Using query parameters for filtering and pagination
            params = {
                "state": "open",
                "per_page": 5, # Fetch 5 PRs per page
                "page": page
            }
            
            data = self._make_request(f"/repos/{owner}/{repo}/pulls", params=params)
            
            if not data:
                logging.info("No more pull requests found.")
                break
                
            for pr in data:
                print(f"  [PR #{pr.get('number')}] {pr.get('title')} (by {pr.get('user', {}).get('login')})")


def main():
    # Instantiate our DevOps API Client
    client = GitHubAPIClient()
    
    # 1. Fetch Repository Stats
    client.get_repo_stats("kubernetes", "kubernetes")
    
    # 2. Fetch Paginated Data (First 2 pages of PRs)
    client.get_open_pull_requests("kubernetes", "kubernetes", pages=2)

if __name__ == "__main__":
    main()
