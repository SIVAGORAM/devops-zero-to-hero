#!/usr/bin/env python3

import os

# ==========================================
# Day 11 Practice: Advanced Lists & Exceptions
# ==========================================

def list_files_in_folder(folder_path):
    """
    Attempts to list the files in a given folder.
    Returns a tuple: (files_list, error_message)
    """
    try:
        # Try to read the directory
        files = os.listdir(folder_path)
        return files, None
        
    except FileNotFoundError:
        return None, "Folder not found"
        
    except PermissionError:
        return None, "Permission denied (You might need sudo/Administrator privileges)"
        
    except Exception as e:
        # Catch-all for any other unexpected errors
        return None, f"An unexpected error occurred: {str(e)}"


def main():
    print("--- DevOps Folder Analyzer ---")
    print("Example input: /tmp /var/log /does/not/exist")
    
    # 1. Get string input and convert to a List using split()
    raw_input = input("\nEnter a list of folder paths separated by spaces: ")
    folder_paths = raw_input.split()
    
    # Check if the user actually entered anything
    if not folder_paths:
        print("No folders provided. Exiting.")
        return

    print("\n--- Scanning Directories ---")
    
    # 2. Iterate through the nested list
    for folder_path in folder_paths:
        
        # 3. Tuple Unpacking from our function
        files, error_message = list_files_in_folder(folder_path)
        
        # 4. Process the results
        if files is not None:
            print(f"\n[SUCCESS] Files in {folder_path}:")
            # Using list comprehension to skip hidden files (optional advanced logic)
            visible_files = [f for f in files if not f.startswith('.')]
            
            for file in visible_files:
                print(f"  ├── {file}")
        else:
            print(f"\n[ERROR] Failed to read {folder_path}:")
            print(f"  └── {error_message}")

# 5. The Execution Guard
if __name__ == "__main__":
    main()
