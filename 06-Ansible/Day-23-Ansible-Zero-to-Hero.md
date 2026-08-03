# Day 23: Ansible Zero to Hero

Welcome to the practical side of Ansible! Today, we will build a real-world Ansible environment in AWS, establish passwordless authentication, write ad-hoc commands, create our first playbook, and dive into Ansible Roles.

---

## 1. Environment Setup: Installing Ansible

Ansible requires a "Control Node" (your laptop or a dedicated server) to manage other "Target Nodes". We strongly recommend using a **Linux machine** as your Control Node.

### Step 1: Install Ansible on Ubuntu
```bash
sudo apt update
sudo apt install ansible -y
```

### Step 2: Verify Installation
Always refer to the official [Ansible Documentation](https://docs.ansible.com/) for troubleshooting.
```bash
ansible --version
```

---

## 2. Infrastructure Setup (AWS EC2)

To practice, we need two servers. Go to your AWS Console and create 2 EC2 Instances (Ubuntu, t2.micro):
1. **Ansible Server (Control Node):** Where you install Ansible and write your code.
2. **Target Server (Node 1):** The server we want to manage.

---

## 3. Passwordless Authentication (SSH Keys)

By default, if the Control Node tries to connect to the Target Server via SSH, it will ask for a password or require a `.pem` key file. In a large environment, this is unscalable. We need **Passwordless Authentication**.

### Step 1: Generate Keys on the Control Node
Log into your **Ansible Server** and generate an SSH key pair:
```bash
ssh-keygen
```
*(Press Enter three times to accept the default location and no passphrase).*

This creates two files in the `/home/ubuntu/.ssh/` directory:
- `id_rsa` (Your Private Key - **NEVER SHARE THIS**)
- `id_rsa.pub` (Your Public Key - Share this with the servers you want to access)

### Step 2: Copy the Public Key
View and copy your public key:
```bash
cat ~/.ssh/id_rsa.pub
```

### Step 3: Paste into the Target Server
Log into your **Target Server**, open the `authorized_keys` file, and paste the public key at the bottom:
```bash
vim ~/.ssh/authorized_keys
```
Save and exit.

### Step 4: Test the Connection
Go back to your **Ansible Server** and try to SSH into the Target Server using its Private IP address:
```bash
ssh <target-server-private-ip>
```
*Boom! You are logged in immediately without a password.*

---

## 4. The Ansible Inventory File

Ansible needs to know *which* servers it is managing. It stores this list of IP addresses in an **Inventory File**.

```bash
mkdir ansible-practice
cd ansible-practice
touch inventory
vim inventory
```

### Grouping Servers
Inside the `inventory` file, you can organize your servers into logical groups using brackets `[group_name]`. This allows you to target specific layers of your application.

```ini
[dbservers]
172.31.62.28

[webservers]
172.31.62.100
172.31.62.101
```

---

## 5. Ad-Hoc Commands vs Playbooks

### Ad-Hoc Commands
Ad-Hoc commands are fast, single-line commands used for quick tasks (like checking disk space or rebooting servers). They are executed directly in the terminal.

**Syntax:** `ansible -i <inventory_file> <target_group> -m <module> -a "<arguments>"`

**Examples:**
```bash
# Create a file on all servers
ansible -i inventory all -m "shell" -a "touch devopsclass"

# Check the number of CPU processors on all servers
ansible -i inventory all -m "shell" -a "nproc"

# Check disk space on webservers only
ansible -i inventory webservers -m "shell" -a "df -h"
```
*(If a command fails, Ansible will output the error in red).*

### Playbooks
Ad-Hoc commands are great for 1-off tasks, but they are not saved or reusable. **Playbooks** are YAML files where you define complex, multi-step configurations that can be saved in Git and executed repeatedly.

---

## 6. Writing Your First Playbook

Let's write a playbook to install and start Nginx on our target servers.

```bash
vim first-playbook.yml
```

**Content of `first-playbook.yml`:**
```yaml
---
- name: Install and start nginx
  hosts: all
  become: root      # This tells Ansible to run commands using 'sudo'

  tasks:
    - name: install nginx
      apt:
        name: nginx
        state: present
    
    - name: Start nginx
      service:
        name: nginx
        state: started
```

### Execute the Playbook
Run the playbook using the `ansible-playbook` command:
```bash
ansible-playbook -i inventory first-playbook.yml
```

**Debugging Tip:** If something goes wrong, add `-vvv` (verbose mode) to see exactly what Ansible is doing internally on the target server.
```bash
ansible-playbook -vvv -i inventory first-playbook.yml
```

---

## 7. Ansible Roles

When playbooks get massive (e.g., configuring an entire Kubernetes cluster), putting everything in one file becomes a nightmare. **Ansible Roles** solve this by breaking the playbook down into a standardized, efficient folder structure.

### Creating a Role
```bash
ansible-galaxy role init Kubernetes
```

This creates a folder named `Kubernetes` with a strict directory structure:
- **`tasks/`**: Contains the main list of actions to execute (replaces the `tasks:` section of a basic playbook).
- **`handlers/`**: Contains tasks that only run when triggered (e.g., "Restart Nginx if the config file changes").
- **`vars/`**: Stores variables (like port numbers or usernames).
- **`defaults/`**: Default variables (can be easily overridden).
- **`templates/`**: Dynamic configuration files (usually `.j2` Jinja2 files).
- **`meta/`**: Contains metadata like the author name, dependencies, and README.

By using Roles, your code becomes modular, reusable, and much easier to read!

*For advanced, real-world playbook examples, explore the official [Ansible Examples GitHub Repo](https://github.com/ansible/ansible-examples).*

---
**[Previous: Day 22 - Config Management](./Day-22-Configuration-Management-and-Ansible.md)** | **[Next: Day 24 - Advanced Ansible Mastery](./Day-24-Advanced-Ansible-Mastery.md)**
