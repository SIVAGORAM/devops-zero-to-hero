#!/usr/bin/env python3

# ==========================================
# Day 13 Project: File Operations
# Scenario: Dynamic Server Config Updater
# ==========================================

def update_server_config(file_path, key, value):
    """
    Reads a configuration file, searches for a specific key, 
    updates its value, and overwrites the file.
    """
    
    print(f"Opening {file_path} to update '{key}' to '{value}'...")
    
    try:
        # Step 1: Read the existing content of the server configuration file
        with open(file_path, 'r') as file:
            # We use readlines() so we get a List of lines that we can iterate over
            lines = file.readlines()

        # Step 2: Open the file in 'w' (Write) mode. 
        # WARNING: This deletes the current file contents, so we must write everything back!
        with open(file_path, 'w') as file:
            for line in lines:
                
                # Check if the line starts with the specified configuration key
                if key in line:
                    # Overwrite the line with the new value
                    file.write(f"{key}={value}\n")
                    print(f" -> Successfully updated {key}!")
                else:
                    # Keep the existing line exactly as it was
                    file.write(line)
                    
        print("Configuration update complete.")
        
    except FileNotFoundError:
        print(f"FATAL ERROR: The configuration file {file_path} could not be found.")
    except Exception as e:
        print(f"FATAL ERROR: An unexpected error occurred: {e}")

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    # Path to our local server configuration file
    server_config_file = 'server.conf'

    # Simulated alert trigger: Traffic is spiking, we need to increase connections!
    key_to_update = 'MAX_CONNECTIONS'
    new_value = '1000'

    # Execute the automation script
    update_server_config(server_config_file, key_to_update, new_value)
