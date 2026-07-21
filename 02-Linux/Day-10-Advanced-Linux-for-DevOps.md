# Day 10: Advanced Linux for DevOps (Zero to Hero Capstone)

To truly wrap up the Linux module and move on to Cloud and Containers, you need to master the advanced Linux concepts that DevOps engineers use daily. These include service management, networking, SSH security, user management, and archiving.

---

## 1. Systemd and Service Management (`systemctl`)

In the modern Linux ecosystem, background services (like Nginx, Docker, Jenkins) are managed by a system and service manager called **Systemd**. As a DevOps engineer, you will constantly start, stop, and debug these services.

The primary command used to interact with Systemd is `systemctl`.

### Essential `systemctl` Commands:
- `sudo systemctl status nginx`: Checks if the Nginx service is running, crashed, or stopped.
- `sudo systemctl start nginx`: Starts the service.
- `sudo systemctl stop nginx`: Stops the service.
- `sudo systemctl restart nginx`: Stops and starts the service (used after changing configuration files).
- `sudo systemctl enable docker`: **Crucial:** Configures the service to start automatically when the server boots up.
- `sudo systemctl disable docker`: Prevents the service from starting on boot.

### Viewing Logs with `journalctl`
If `systemctl status` shows a service failed, the detailed logs are stored in the system journal.
- `journalctl -u nginx`: Views all logs for the Nginx unit (`-u`).
- `journalctl -u nginx -f`: Follows the logs live (like `tail -f`).

---

## 2. Linux Networking Commands

When microservices can't talk to the database, you need to debug the network.

### Checking Connectivity
- `ping google.com`: Tests if your server can reach the internet (sends ICMP echo requests).
- `curl -v http://localhost:8080`: Tests if a web server is responding on a specific port.

### Checking Open Ports and Connections
- `netstat -tulpn` or `ss -tulpn`: Displays all listening ports and the Process IDs (PIDs) bound to them. Very useful if an app fails to start because "Port 8080 is already in use."
- `lsof -i :8080`: Lists open files and processes using port 8080.

### DNS Resolution
- `nslookup google.com` or `dig google.com`: Checks if DNS is correctly resolving domain names to IP addresses.

---

## 3. SSH Security & Secure Copy (`scp`)

SSH (Secure Shell) is how we connect to servers remotely and securely.

### Generating SSH Keys
Instead of passwords, servers use cryptographic keys for secure authentication.
```bash
ssh-keygen -t rsa -b 4096
```
This generates a public key (`~/.ssh/id_rsa.pub`) and a private key (`~/.ssh/id_rsa`). You put the **public** key on the server (`~/.ssh/authorized_keys`) and keep the **private** key on your laptop.

### Copying Files Securely (`scp`)
If you need to move a configuration file from your laptop to an EC2 instance:
```bash
scp -i my-key.pem ./app-config.yaml ubuntu@192.168.1.10:/home/ubuntu/
```

---

## 4. User and Group Management

Servers often have multiple users (e.g., developers, service accounts). You need to manage who can access what.

### Managing Users
- `sudo useradd siva`: Creates a new user named siva.
- `sudo passwd siva`: Sets or changes the password for the user.
- `sudo usermod -aG sudo siva`: Adds (`-a`) the user to the `sudo` Group (`-G`), granting them admin privileges.
- `sudo userdel siva`: Deletes the user.

*(Note: User information is stored in `/etc/passwd` and passwords are encrypted in `/etc/shadow`).*

### Managing Groups
- `sudo groupadd developers`: Creates a group.
- `sudo chown :developers /var/www`: Changes the group ownership of a folder.

---

## 5. Advanced Permissions (ACL & SUID)

Standard `chmod` limits you to Owner, Group, and Others. What if you want to give a *specific* user read access without changing the owner?

### Access Control Lists (ACLs)
- `setfacl -m u:siva:rx file.txt`: Modifies (`-m`) the ACL to give user (`u`) siva read and execute (`rx`) permissions on the file.
- `getfacl file.txt`: Views the detailed ACLs on a file.

### Special Permissions (SUID)
If you set the SUID bit on an executable file, it runs with the permissions of the file's owner, not the person running it. (e.g., the `passwd` command has SUID set so regular users can modify the highly protected `/etc/shadow` file to change their own password).

---

## 6. Archiving and Compression (`tar`)

In DevOps, we constantly package application code into single files to deploy them, or compress massive log files to save space.

### Using `tar` (Tape Archive)
- `tar -cvf archive.tar /var/log/`: **Creates** (`-c`) a tarball archive (verbosely `-v`) into a file (`-f`).
- `tar -xvf archive.tar`: **Extracts** (`-x`) the archive.
- `tar -czvf archive.tar.gz /var/log/`: Creates and **compresses** it using gzip (`-z`), significantly reducing the file size.

---

## 7. Storage and Disk Management

When a database server runs out of space, you attach a new EBS volume in AWS. But you must mount it in Linux.

- `lsblk`: Lists all block devices (hard drives and partitions) attached to the system.
- `df -h`: Shows mounted filesystems and their free space.
- `mount /dev/nvme1n1 /data`: Mounts a newly formatted disk partition to the `/data` folder.
- `/etc/fstab`: A configuration file that tells Linux to automatically mount the disk every time the server reboots.

---

## 8. Text Manipulation & Environment Variables

There are two massive concepts used extensively in CI/CD pipelines: `sed` and Environment Variables.

### `sed` (Stream Editor)
If you need to change a database URL in a config file dynamically in an automated pipeline, you cannot open `vi`. You use `sed`.
- `sed -i 's/old-db-url/new-db-url/g' config.yaml`: Searches for `old-db-url`, replaces it with `new-db-url` globally (`g`), and saves the change directly in the file (`-i`).

### Environment Variables
Variables that define the environment your application runs in (e.g., API keys, Java home paths).
- `env` or `printenv`: Lists all active environment variables.
- `export API_KEY="12345"`: Sets a variable for the current terminal session.
- **Persistence:** To make a variable survive a reboot, you must add the `export` command to `~/.bashrc` (for a specific user) or `/etc/environment` (for all users).

---

## 9. Soft Links vs Hard Links

- **Soft Link (Symlink):** Like a Windows shortcut. If the original file is deleted, the link breaks.
  `ln -s /path/to/original /path/to/link`
- **Hard Link:** A direct mirror of the underlying data. If the original file is deleted, the hard link still works.
  `ln /path/to/original /path/to/link`

---

## 🎯 Final Linux Module Summary
You have now completed the entire Linux curriculum. From the core basics (`cd`, `ls`, `chmod`), to Shell Scripting automation (`awk`, `grep`, loops), right through to advanced system administration (`systemctl`, `netstat`, `tar`, SSH keys). 

You possess all the fundamental OS knowledge required to begin orchestrating infrastructure in the Cloud!

---
**[➡️ Next: Day 11 - Networking Foundations](../03-Networking/Day-11-Networking-Foundations.md)**

