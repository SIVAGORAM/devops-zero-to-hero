#!/usr/bin/env python3

# ==========================================
# Day 20 Practice: OS, Pathlib & Shutil
# Scenario: Deployment Directory Automation
# ==========================================

from pathlib import Path
import shutil

def check_disk_space():
    """Uses shutil to ensure the server has enough disk space for deployment."""
    usage = shutil.disk_usage(".")
    free_gb = usage.free / (1024 ** 3)
    
    print(f"[INFO] Free disk space: {free_gb:.2f} GB")
    if free_gb < 1.0:
        print("[WARNING] Disk space is critically low (< 1 GB)!")
    return free_gb

def create_directories(base_dir: Path):
    """Uses pathlib to generate a resilient directory structure."""
    directories = [
        base_dir / "config",
        base_dir / "logs",
        base_dir / "backup",
        base_dir / "release"
    ]

    for directory in directories:
        # parents=True acts like `mkdir -p`
        # exist_ok=True prevents crashes on re-deployments
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  -> Created/Verified: {directory}")

def create_config(base_dir: Path) -> Path:
    """Uses pathlib to write a configuration file."""
    config_file = base_dir / "config" / "server.conf"
    
    # write_text is a quick pathlib alternative to `with open("w")`
    config_file.write_text(
        "PORT=8080\n"
        "MAX_CONNECTIONS=600\n"
        "LOG_LEVEL=INFO\n"
    )
    return config_file

def create_release(base_dir: Path) -> Path:
    """Uses pathlib to create a release file."""
    release_file = base_dir / "release" / "application.txt"
    release_file.write_text("Application deployment v1.0.0 successful\n")
    return release_file

def backup_config(config_file: Path, base_dir: Path) -> Path:
    """Uses shutil to safely copy a configuration file."""
    backup_file = base_dir / "backup" / "server.conf"
    
    # copy2 preserves metadata (like creation date)
    shutil.copy2(config_file, backup_file)
    return backup_file

def show_files(base_dir: Path):
    """Uses pathlib.rglob to recursively list all files deployed."""
    print("\n[INFO] Deployment Files Structure:")
    # rglob("*") recursively finds everything (files and folders)
    for item in base_dir.rglob("*"):
        # We can format it to only show the path relative to the base_dir
        print(f"  - {item}")

def main():
    print("=== DEPLOYMENT PIPELINE INITIATED ===\n")
    
    # 1. Pre-flight Check
    check_disk_space()
    
    # Define our base deployment path
    base_dir = Path("devops-deployment")
    
    # 2. Execution
    print("\n[INFO] Provisioning directory structure...")
    create_directories(base_dir)

    print("\n[INFO] Generating configuration and release files...")
    config_file = create_config(base_dir)
    release_file = create_release(base_dir)

    print("\n[INFO] Backing up core configurations...")
    backup_file = backup_config(config_file, base_dir)

    print("\n=== DEPLOYMENT COMPLETED SECURELY ===")
    show_files(base_dir)

if __name__ == "__main__":
    main()
