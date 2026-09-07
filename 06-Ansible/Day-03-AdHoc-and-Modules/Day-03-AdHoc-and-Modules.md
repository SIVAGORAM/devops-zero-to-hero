# Ansible Day 3: Ad-Hoc Deep Dive & Custom Inventories

Welcome to Day 3! Today we dive deep into Ad-Hoc commands, learn how to build Custom Inventory files, and break down the absolute most critical modules you will use every single day as a DevOps Engineer.

---

## 🔁 1. The Core Philosophy: Idempotency

Before we run commands, you must understand the golden rule of Ansible: **Idempotency**.

> [!IMPORTANT]
> **Idempotency** means that running a task multiple times will have the *exact same effect* as running it once. If you tell Ansible to install Nginx, it installs it. If you run the exact same command 1,000 more times, Ansible will simply say "Already Installed" and do absolutely nothing. It is safe to run Ansible repeatedly!

---

## 🛠️ 2. Ad-Hoc Command Deep Dive

Ad-hoc commands are simple, non-repetitive commands meant for a single execution (like a quick server reboot or a one-time file copy).

### 1. Connection Testing (`ping`)
Remember, whenever you run an Ansible command, it checks the `ansible.cfg` file first! To do a quick connection test as a sudo user:
```bash
ansible dev -b -m ping
```

### 2. Packages (`apt` vs `yum` vs `package`)
If you are managing Ubuntu machines, you use the `apt` module:
```bash
ansible dev -b -m apt -a "name=git state=present"
```
If you are managing Red Hat, CentOS, or Amazon Linux machines, `apt` will fail! You must use `yum`:
```bash
ansible dev -b -m yum -a "name=git state=present"
```
**Pro Tip:** If your environment has a mix of Ubuntu AND Red Hat servers, use the generic `package` module. It automatically detects the OS and uses the correct package manager under the hood!
```bash
ansible dev -b -m package -a "name=git state=present"
```

### 3. Service Management (`service`)
Let's install Nginx, verify it manually on the slave, and then stop it using Ansible!
```bash
# 1. Install Nginx
ansible dev -b -m apt -a "name=nginx state=present"

# 2. Go to your slave node manually and verify it is running:
# nginx -v
# service nginx status

# 3. Stop the service using Ansible
ansible dev -b -m service -a "name=nginx state=stopped"
```

### 4. File Transfers (`copy` vs `fetch`)
**1. Master to Slave (`copy`):** I create `abc.txt` on my Master node and want to push it to all Slave nodes:
```bash
# Run on Master:
touch abc.txt
ansible dev -b -m copy -a "src=/etc/ansible/abc.txt dest=/home/ubuntu/"

# Run on Slave to verify:
# cd /home/ubuntu
# ls
```
**2. Slave to Master (`fetch`):** A log file `123.txt` is generated on a Slave node (Node-2), and I want to pull it back to the Master:
```bash
# Run on Slave:
touch 123.txt

# Run on Master:
ansible dev -b -m fetch -a "src=/home/ubuntu/123.txt dest=/etc/ansible/"
```

### 5. Command Execution (`command` vs `shell`)
These two modules look identical but have one massive difference.
```bash
ansible dev -b -m command -a "ls -l | wc -l"  # THIS WILL FAIL!
ansible dev -b -m shell -a "ls -l | wc -l"    # THIS WILL SUCCEED!
```
> [!CAUTION]
> **Interview Question:** What is the difference between `command` and `shell`?
> **Answer:** The `command` module runs raw executables and does NOT support Linux Bash features like pipes (`|`), redirects (`>`), or logical ANDs (`&&`). The `shell` module runs the command through `/bin/sh`, so pipes and redirects work perfectly.

### Managing Files and Directories (`file`)
```bash
# Create an empty file
ansible dev -b -m file -a "path=/home/ubuntu/devops.txt state=touch"

# Create an empty directory
ansible dev -b -m file -a "path=/home/ubuntu/aws state=directory"
```

---

## 🗂️ 3. Custom Inventory Files

You do not have to use the default `/etc/ansible/hosts` file. You can create your own custom inventory file in your local directory (the extension should be `.ini`).

```bash
cd /home/ubuntu
vi inventory.ini
```
Paste your custom host details inside:
`master ansible_host=172.31.3.222 ansible_user=ubuntu ansible_ssh_private_key_file=/etc/ansible/awslogin.pem`

If you try to run `ansible master -m ping`, it will fail because Ansible looks at `/etc/ansible/hosts` by default. You must explicitly pass your custom file using the `-i` flag:
```bash
ansible master -m ping -i inventory.ini
```

### Passing Custom Private Keys
If you don't want to hardcode the `.pem` file path inside the `inventory.ini`, you can pass it directly in the CLI using `--private-key`:
```bash
chmod 600 master.pem
ansible master -m ping -i inventory.ini --private-key master.pem
```

---

## 📚 4. Exploring the Documentation

Ansible has built-in offline documentation! You do not need to Google how a module works.
```bash
# List all thousands of modules installed on your machine
ansible-doc -l

# Read the manual/examples for a specific module
ansible-doc apt
```

---

## 👑 5. Zero-to-Hero: The Ultimate Modules Dictionary

As requested, here is a breakdown of the 34 critical modules you will use day-to-day. You must know what they do!

### ⚙️ System & Execution
1. **`command`**: Executes a command without shell processing (No pipes `|`).
2. **`shell`**: Executes a command through a shell (Pipes `|` work).
3. **`script`**: Copies a local bash script to the remote node and executes it.
4. **`setup`**: Gathers all "facts" (IPs, OS version, RAM) about the remote machine.
5. **`cron`**: Automates scheduling tasks (like taking backups at midnight).
6. **`debug`**: Prints text or variable values to your screen during execution.
7. **`register`**: Not a module, but a keyword used to save the output of a task into a variable.
8. **`wait_for`**: Pauses execution until a condition is met (e.g., wait for Port 80 to open).

### 📦 Package Management
9. **`apt`**: Installs packages on Ubuntu/Debian (`state=present`).
10. **`yum`**: Installs packages on RHEL/CentOS.
11. **`package`**: OS-agnostic package installer.
12. **`pip`**: Installs Python libraries (e.g., `pip3 install boto3`).
13. **`service`**: Starts, stops, or restarts background services (`name=nginx state=started`).

### 📁 Files & Storage
14. **`file`**: Creates files (`state=touch`) or folders (`state=directory`).
15. **`copy`**: Copies a file from the Master to the Slave.
16. **`fetch`**: Pulls a file from the Slave back to the Master.
17. **`lineinfile`**: Finds a specific line of text in a file and adds/modifies/removes it (Great for editing config files).
18. **`blockinfile`**: Similar to `lineinfile`, but inserts a massive block of multi-line text into a file.
19. **`replace`**: Finds a specific string using Regex and replaces it.
20. **`archive`**: Compresses files into a `.zip` or `.tar.gz`.
21. **`unarchive`**: Extracts compressed files.
22. **`mount`**: Mounts a new hard drive to the Linux file system.
23. **`stat`**: Gathers detailed information about a file or folder (e.g., does it exist? Is it a directory?).

### 🔒 Security & Users
24. **`user`**: Creates or deletes Linux users (`name=harshhaa state=present`).
25. **`acl`**: Manages Access Control Lists (advanced Linux file permissions).

### ☁️ Cloud & Web (AWS/Git)
26. **`aws_ec2`**: Dynamically manages EC2 instances.
27. **`aws_s3`**: Manages S3 buckets and objects.
28. **`get_url`**: Downloads a file directly from the internet (exactly like `wget` in Linux).
29. **`git`**: Clones a repository from GitHub to the node.

### 🧩 Playbook Organization
30. **`include_role`**: Dynamically loads an Ansible Role during a playbook.
31. **`include_tasks`**: Runs tasks from another YAML file to keep your code clean.
32. **`include_vars`**: Loads variables from external JSON or YAML files.
33. **`find`**: Searches for files based on specific criteria (like `find` in Linux).
34. **`ping`**: Tests SSH connectivity to the nodes.
