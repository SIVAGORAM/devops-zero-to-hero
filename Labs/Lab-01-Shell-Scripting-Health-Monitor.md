# Lab 1: Automated System Health & Backup Monitor

## Objective
Write a production-grade Bash script that acts as an automated system monitor. The script will:
1. Check if the disk space usage is above a critical threshold (e.g., 80%).
2. Check if the available memory is getting too low.
3. Automatically back up an application directory if the system is healthy.
4. Output a summary report to a log file.

---

## The Script (`system_monitor.sh`)

Create a file named `system_monitor.sh` and make it executable:
```bash
touch system_monitor.sh
chmod +x system_monitor.sh
```

Paste the following code into the script:

```bash
#!/bin/bash

######################################### # Author      : Siva
# Date        : 21-01-2026
# Description : System Health Monitor & Auto-Backup
# Version     : v1.0
######################################### # Enable safe scripting
set -e
set -o pipefail

# Configuration Variables
APP_DIR="/tmp/my-app"
BACKUP_DIR="/tmp/backups"
LOG_FILE="/tmp/system_monitor.log"
DISK_THRESHOLD=80

echo "--- Starting System Monitor [$(date)] ---" | tee -a "$LOG_FILE"

# 1. Disk Space Check
# Extract the root (/) partition usage percentage using df, grep, and awk
DISK_USAGE=$(df -h / | grep -v Filesystem | awk '{print $5}' | sed 's/%//g')

if [ "$DISK_USAGE" -gt "$DISK_THRESHOLD" ]; then
    echo " WARNING: Disk usage is critically high at ${DISK_USAGE}%!" | tee -a "$LOG_FILE"
    echo "Aborting backup to save space." | tee -a "$LOG_FILE"
    exit 1
else
    echo " Disk usage is healthy at ${DISK_USAGE}%." | tee -a "$LOG_FILE"
fi

# 2. Memory Check
# Just outputting current RAM state
echo " Current Memory State:" | tee -a "$LOG_FILE"
free -h | tee -a "$LOG_FILE"

# 3. Auto Backup Execution
# Create dummy app dir for testing if it doesn't exist
mkdir -p "$APP_DIR"
touch "$APP_DIR/config.yml" "$APP_DIR/index.html"
mkdir -p "$BACKUP_DIR"

BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).tar.gz"

echo " Starting backup of $APP_DIR..." | tee -a "$LOG_FILE"
tar -czf "$BACKUP_DIR/$BACKUP_FILE" -C /tmp my-app

echo " Backup successfully created at $BACKUP_DIR/$BACKUP_FILE" | tee -a "$LOG_FILE"
echo "--- Monitor Run Complete ---" | tee -a "$LOG_FILE"
```

## How to test this lab:
1. Run `./system_monitor.sh`
2. You should see output printed to the terminal *and* saved to `/tmp/system_monitor.log`.
3. Verify the backup was created by running `ls -l /tmp/backups`
4. Try changing `DISK_THRESHOLD=1` temporarily in the script and run it again to see how the "WARNING" condition behaves and stops the script safely using `exit 1`.
