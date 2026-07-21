# Assignment: Advanced Linux Administration

This assignment tests your ability to practically apply the concepts learned in the Linux and Shell Scripting modules (Days 7 to 10). It simulates a real-world scenario where you are given a fresh server and need to configure it for a production application.

## Scenario
You are a newly hired DevOps Engineer. Your team lead has given you access to a fresh Ubuntu Linux server. You need to secure it, configure a service, set up a backup job, and manipulate some text files.

---

## Task 1: User & Security Management
1. Create a new user named `deployer`.
2. Grant the `deployer` user `sudo` privileges.
3. Generate an SSH keypair for the `deployer` user without a passphrase.
4. Using ACLs, give the `deployer` user explicit read and write (`rw`) permissions to the `/var/log/syslog` file without changing the file's current owner or group.

## Task 2: Service Management & Systemd
1. Install the `nginx` web server using your package manager.
2. Start the `nginx` service and ensure it is configured to start automatically on system boot.
3. Check the status of `nginx` to confirm it is running.
4. Simulate a crash by forcefully killing the `nginx` process using `kill -9 <PID>`.
5. Use `journalctl` to view the last 20 log entries of the `nginx` service to observe the crash logs.

## Task 3: Text Manipulation (`sed` & `awk`)
1. Create a dummy configuration file named `database.yml` with the following content:
   ```yaml
   db_host: localhost
   db_port: 5432
   db_user: admin
   db_pass: secret123
   ```
2. Using the `sed` command, modify the file in-place to change `localhost` to `production-db.aws.com`.
3. Using the `awk` command, print *only* the value of the port (e.g., extract `5432` from the second line).

## Task 4: Advanced `find` and Archiving (`tar`)
1. Create a directory named `/tmp/old_logs` and generate 5 empty `.log` files inside it.
2. Write a single `find` command that finds all `.log` files in `/tmp/old_logs` and deletes them directly (Hint: use the `-exec rm {} \;` flag).
3. Archive the entire `/etc/nginx` configuration directory into a compressed file named `nginx_backup.tar.gz` and place it in the `/tmp` directory.

## Task 5: Cronjobs & Automation
1. Write a bash script named `disk_alert.sh` that checks if the root `/` partition is over 90% full. If it is, echo a warning message. (You can reuse parts of the Health Monitor lab).
2. Schedule this script in `crontab` to run automatically every hour, on the hour (e.g., 1:00, 2:00, 3:00).

---

### Verification
Once you complete these tasks, you have proven that you possess the practical, hands-on Linux skills required for an Associate-level DevOps Engineer role. You are ready for the Cloud!
