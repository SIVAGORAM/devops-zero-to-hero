#!/usr/bin/env python3

# ==========================================
# Day 21 Practice: Subprocess Automation
# Scenario: Linux Server Health Checker
# ==========================================

import subprocess

def run_linux_command(command_list: list) -> str:
    """
    Executes a Linux command securely using subprocess.
    Captures the output, decodes it to a string, and handles timeouts/failures.
    """
    try:
        # capture_output: Grabs stdout and stderr
        # text=True: Returns strings instead of raw bytes
        # check=True: Raises an exception if exit code != 0
        # timeout=10: Prevents the script from hanging forever
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        return result.stdout.strip()
        
    except subprocess.CalledProcessError as e:
        return f"[ERROR] Command failed with exit code {e.returncode}:\n{e.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return f"[ERROR] Command timed out after 10 seconds."
    except FileNotFoundError:
        return f"[ERROR] Command '{command_list[0]}' not found on this system."

def main():
    print("========================================")
    print("       LINUX SERVER HEALTH REPORT       ")
    print("========================================\n")

    # Define the Linux commands we want to execute as Lists of Strings
    commands = {
        "Hostname": ["hostname"],
        "Uptime": ["uptime", "-p"],
        "Memory (RAM)": ["free", "-h"],
        "Disk Usage": ["df", "-h", "/"],
        # Example of a command that will likely fail if Nginx isn't installed
        "Nginx Status": ["systemctl", "is-active", "nginx"] 
    }

    # Iterate through our dictionary and execute each Linux command
    for component, cmd in commands.items():
        print(f"--- {component.upper()} ---")
        output = run_linux_command(cmd)
        print(f"{output}\n")

    print("========================================")
    print("       SERVER CHECK COMPLETED           ")
    print("========================================")

if __name__ == "__main__":
    main()
