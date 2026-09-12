import pytest
import requests
from unittest.mock import patch
from monitor import check_server

# ==========================================
# Day 30 Practice: Pytest & Mocking
# Run this file using: pytest -v test_monitor.py
# ==========================================

@patch("monitor.requests.get")
def test_server_up(mock_get):
    """Test the happy path where the server returns a 200 OK."""
    # 1. Arrange (Configure the mock)
    mock_get.return_value.status_code = 200
    
    # 2. Act
    result = check_server("https://example.com")
    
    # 3. Assert
    assert result == "UP"
    # Ensure our code actually called the mock with the right URL
    mock_get.assert_called_once_with("https://example.com", timeout=5)

@patch("monitor.requests.get")
def test_server_down_500(mock_get):
    """Test the scenario where the server returns a 500 Internal Server Error."""
    # 1. Arrange
    mock_get.return_value.status_code = 500
    
    # 2. Act
    result = check_server("https://example.com")
    
    # 3. Assert
    assert result == "DOWN"

@patch("monitor.requests.get")
def test_server_unreachable(mock_get):
    """Test the scenario where the server is completely offline (DNS/Connection Refused)."""
    # 1. Arrange (side_effect is used to raise Exceptions from mocks!)
    mock_get.side_effect = requests.RequestException("Connection refused")
    
    # 2. Act
    result = check_server("https://example.com")
    
    # 3. Assert
    assert result == "DOWN"
