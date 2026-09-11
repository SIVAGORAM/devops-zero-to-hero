#!/usr/bin/env python3

"""
==========================================
Day 16 Project: Introduction to Flask
Script 1: Hello World Server
==========================================
Note: Run `pip install flask` before executing!
"""

from flask import Flask

# 1. Create the Flask Application Object
app = Flask(__name__)

# 2. Define the Route (The URL Endpoint)
@app.route('/')
def hello_world():
    """
    This function executes whenever someone visits http://localhost:5000/
    """
    print("Someone hit the root endpoint!")
    return 'Hello, World! The Flask server is running.'

# 3. Start the Application
if __name__ == '__main__':
    print("Starting Flask Development Server on port 5000...")
    # host="0.0.0.0" means it listens on all network interfaces
    app.run(host="0.0.0.0", port=5000)
