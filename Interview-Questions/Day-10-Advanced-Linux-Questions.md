# Day 10: Advanced Linux Administration - Interview Questions

These questions test your knowledge of system internals, service management, and advanced Linux administration which are critical for senior DevOps roles.

---

### Q1: You deployed an application, but it is failing to start on boot. How would you troubleshoot this using Systemd?
**Interview Answer:**  
"First, I would use `sudo systemctl status <app_name>` to see the current state of the service. If it shows as failed, I would use `journalctl -u <app_name> -e` to inspect the very end of the service logs to find the exact crash reason. Finally, I would ensure the service is actually configured to start on boot by running `sudo systemctl enable <app_name>`."

---

### Q2: An application throws a "Port 8080 already in use" error. How do you find out what is using that port?
**Interview Answer:**  
"I would use the command `sudo netstat -tulpn | grep 8080` or `sudo ss -tulpn | grep 8080`. This will list the listening network sockets on port 8080 and display the Process ID (PID) and the name of the program currently holding that port. Alternatively, `lsof -i :8080` can also provide this information."

---

### Q3: What is the difference between `/etc/passwd` and `/etc/shadow`?
**Interview Answer:**  
"`/etc/passwd` is a system file that stores essential user account information (like usernames, user IDs, home directories, and default shells). It is readable by all users. `/etc/shadow`, on the other hand, stores the actual encrypted passwords and password expiration data. It is heavily restricted and can only be read by the root user for security purposes."

---

### Q4: Explain the difference between Soft Links (Symlinks) and Hard Links in Linux.
**Interview Answer:**  
"A soft link (created with `ln -s`) is simply a shortcut that points to the original file path. If the original file is deleted, the soft link becomes broken or 'dangling'. A hard link (created with `ln`) creates a direct pointer to the underlying inode (the actual data on the disk). Even if the original file is deleted, the hard link still retains the data. Hard links cannot cross different file systems, whereas soft links can."

---

### Q5: You need to replace a database URL inside a configuration file automatically within a CI/CD pipeline. How do you do this without opening an editor?
**Interview Answer:**  
"I would use `sed` (Stream Editor). By running a command like `sed -i 's/OLD_URL/NEW_URL/g' config.yaml`, `sed` will search the file for 'OLD_URL', replace it with 'NEW_URL' globally across the file, and save the changes in-place (`-i`). This is standard practice in automated CI/CD pipelines."

---

### Q6: How do you set an environment variable so that it persists across reboots?
**Interview Answer:**  
"Running `export VAR="value"` only sets the variable for the current terminal session; it is lost when you log out. To make it persistent, I would append the export command to a shell configuration file like `~/.bashrc` or `~/.bash_profile` for a specific user, or `/etc/environment` if I want it applied globally to all users on the system."

---

### Q7: What are ACLs and when would you use them over standard `chmod` permissions?
**Interview Answer:**  
"Standard `chmod` permissions only allow you to set rules for the file's Owner, its Group, and Others. If I need to give read access to a very specific user (e.g., 'john') without making him the owner or modifying his groups, `chmod` is insufficient. Access Control Lists (ACLs) solve this. Using `setfacl -m u:john:r file.txt`, I can grant precise permissions to specific users or groups without altering the base permission structure."

---

### Q8: What is the purpose of the `/etc/fstab` file?
**Interview Answer:**  
"`/etc/fstab` (File System Table) is a critical configuration file used to define how disk partitions, block devices, or remote file systems should be mounted into the Linux filesystem. The system reads this file during boot. If you attach a new AWS EBS volume and mount it, you must add an entry into `/etc/fstab` to ensure the disk mounts automatically upon reboot."

---
**[⬅️ Previous: Day 8 & 9 - Shell Scripting Questions](./Day-08-Shell-Scripting-Questions.md)**
