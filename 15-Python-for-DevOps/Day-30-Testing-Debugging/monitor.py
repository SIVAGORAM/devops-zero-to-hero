import requests

def check_server(url: str) -> str:
    """
    Business Logic: Checks if a server is online.
    Returns 'UP' if 200, 'DOWN' otherwise (including timeouts/connection errors).
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return "UP"
        return "DOWN"
    except requests.RequestException:
        # Handles DNS failures, connection refused, timeouts, etc.
        return "DOWN"
