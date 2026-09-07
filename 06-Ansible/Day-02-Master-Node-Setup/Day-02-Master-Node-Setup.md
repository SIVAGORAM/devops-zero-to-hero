# Ansible Day 2: Master-Node Setup & Ad-Hoc Commands

Welcome to Day 2! Today we are rolling up our sleeves to physically connect our Ansible Master (Controller) to our Slave Nodes, and we will execute our very first automation commands!

---

## 🏗️ 1. Architecture Setup (AWS Lab)

To see Ansible's power, we need multiple machines. Go to your AWS console and launch **3 Ubuntu EC2 Instances** simultaneously.

Rename them so you don't get confused:
1. `Ansible-Server` (This is our Master/Controller)
2. `Node-1` (Slave)
3. `Node-2` (Slave)

Connect to the `Ansible-Server` via MobaXterm. This is the only machine we will ever type commands into!

---

## ⚙️ 2. The Brain of Ansible: `/etc/ansible`

Inside your `Ansible-Server`, navigate to the absolute core directory of Ansible:
```bash
sudo su
cd /etc/ansible
ls
```
You will see two critically important files here:
1. **`ansible.cfg`**: The Configuration File.
2. **`hosts`**: The Inventory File.

### The Configuration File (`ansible.cfg`)
Whenever you type any Ansible command (like `ansible` or `ansible-playbook`), the system immediately checks `ansible.cfg` to see *how* it should behave before doing anything else. 
If your file is empty on the EC2 machine, you can copy the official default template from the **[`ansible.cfg`](file:///D:/Devops/Devops/06-Ansible/Day-02-Master-Node-Setup/ansible.cfg)** file in this folder. 

Paste the code into `vi ansible.cfg` on your master node, and **uncomment (remove the `#`) from these two specific lines**:
- `inventory = /etc/ansible/hosts` *(Tells Ansible where your list of IPs is located)*
- `remote_user = root` *(Tells Ansible which user to log in as by default)*

---

## 🗺️ 3. The Inventory File (`hosts`)

Ansible needs to know the IP addresses of `Node-1` and `Node-2`, and it needs the `.pem` key to SSH into them. We store all of this in the **Inventory File**.

### Step 1: Secure the `.pem` key on the Master
Ansible needs your AWS private key to log into the slave nodes.
```bash
# Create the key file on your master server
vi /etc/ansible/awslogin.pem
# Paste your AWS .pem key text here and save!

# IMPORTANT: You must restrict permissions on private keys!
chmod 600 /etc/ansible/awslogin.pem
```

### Step 2: Define your Groups in the `hosts` file
We have different environments in the real world (e.g., **Dev, Testing, RFS, Pre-Prod, Prod**). We create groups in our inventory file so we can run commands on specific environments without touching the others. Open `vi hosts` and paste this syntax:

```ini
# Syntax: <machine-name> ansible_host=<Private-IP> ansible_user=<user> ansible_ssh_private_key_file=<path>

[dev]
NODE1 ansible_host=172.31.2.215 ansible_user=ubuntu ansible_ssh_private_key_file=/etc/ansible/awslogin.pem
NODE2 ansible_host=172.31.1.255 ansible_user=ubuntu ansible_ssh_private_key_file=/etc/ansible/awslogin.pem

[local]
master ansible_host=172.31.3.222 ansible_user=ubuntu ansible_ssh_private_key_file=/etc/ansible/awslogin.pem
```
*(Always use Private IPs when machines are in the same AWS VPC!)*

### Step 3: Test the Connection!
Let's see if our Master can talk to the Slaves! You can target specific machines, groups, or everything at once:

```bash
# Ping the entire [dev] group
ansible dev -m ping

# Ping just one specific node
ansible NODE1 -m ping

# Ping the local master machine
ansible local -m ping

# Ping EVERY machine in the inventory file
ansible all -m ping
```
*If you see green "SUCCESS" text, your setup is perfect!*

---

## ⚡ 4. Executing Tasks: Ad-Hoc Commands

In Ansible, there are two ways to do things:
1. **Ad-Hoc Commands:** One-liners executed directly in the terminal. Used for quick, one-time, non-repetitive tasks.
2. **Playbooks:** YAML files for complex, repeatable automations.

Today, we focus on **Ad-Hoc Commands**.

### The Anatomy of an Ad-Hoc Command
`ansible <target-group> -m <module> -a "<arbitrary arguments>"`

### Becoming Sudo (`-b`)
If you try to install software, Ansible will fail with "Permission Denied" because you are the `ubuntu` user. You must add `-b` (Become) to elevate to sudo privileges!

### Practical Lab: Managing Packages and Services

**1. Install Git:**
```bash
ansible dev -b -m apt -a "name=git state=present"
```
*(The `apt` module manages packages. The `state` can be: `present` [install], `absent` [uninstall], or `latest` [update]).*

> [!NOTE]
> **How to check the state of the node:** Your notes mentioned checking the state in `ansible.cfg`. This is incorrect! To verify if Git or Apache was actually installed, you either look at the Ansible output color (Yellow = Changed, Green = Already Installed), or you can run a manual check like `service apache2 status`.

**2. Install Apache Web Server:**
```bash
ansible dev -b -m apt -a "name=apache2 state=present"
```

**3. Stop the Apache Service:**
```bash
ansible dev -b -m service -a "name=apache2 state=stopped"
```
*(The `service` module manages background processes. The `state` can be: `started`, `stopped`, or `restarted`).*

**4. Uninstall Apache:**
```bash
ansible dev -b -m apt -a "name=apache2 state=absent"
```

---

## 🧠 5. Zero-to-Hero Bonus: The Top 30 Day-to-Day Modules

Your instructor challenged you to list the 30-40 Ansible modules used daily in the real world. Instead of you hunting for them, here is your definitive cheat sheet for daily DevOps tasks!

**Package Management:**
1. `apt` (Manage packages on Ubuntu/Debian)
2. `yum` / `dnf` (Manage packages on RHEL/CentOS/Amazon Linux)
3. `pip` (Install Python packages)
4. `npm` (Install Node.js packages)
5. `gem` (Install Ruby gems)

**System & Files:**
6. `service` / `systemd` (Start/Stop background services)
7. `file` (Create/Delete directories, set permissions)
8. `copy` (Copy files from Master to Slaves)
9. `fetch` (Pull files from Slaves back to Master)
10. `template` (Copy a file, but replace variables inside it dynamically)
11. `lineinfile` (Ensure a specific line of text exists inside a file)
12. `archive` / `unarchive` (Zip or Unzip files)

**Users & Security:**
13. `user` (Create/Delete Linux users)
14. `group` (Create/Delete Linux groups)
15. `authorized_key` (Add SSH keys to users for passwordless login)
16. `ufw` / `firewalld` (Manage Linux firewalls)
17. `cron` (Schedule cron jobs)

**Commands & Execution:**
18. `ping` (Test connection to nodes)
19. `command` (Run a raw Linux command, does NOT support pipes `|` or `>`)
20. `shell` (Run a raw Linux command, fully supports bash features like `|` and `>`)
21. `script` (Run a local script on the remote node)
22. `raw` (Run a command over SSH without requiring Python on the target)

**Cloud (AWS):**
23. `amazon.aws.ec2_instance` (Create/Terminate EC2 instances)
24. `amazon.aws.s3_bucket` (Manage S3 buckets)
25. `amazon.aws.iam_user` (Manage AWS users)

**Version Control & DBs:**
26. `git` (Clone repositories automatically)
27. `mysql_db` (Create/Delete MySQL databases)
28. `postgresql_db` (Manage Postgres databases)

**Utilities:**
29. `debug` (Print variables or messages to the screen)
30. `setup` (Gathers the "facts" of the machine manually)
31. `wait_for` (Wait for a port to open before proceeding)
