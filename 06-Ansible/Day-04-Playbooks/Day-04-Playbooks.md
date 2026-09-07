# Ansible Day 4: Playbooks Deep Dive

Welcome to Day 4! Ad-Hoc commands are great for quick, one-off fixes, but when we want to provision an entire infrastructure with multiple, complex, repeatable operations, we use **Ansible Playbooks**.

---

## 📖 1. What is a Playbook?

A Playbook is simply a YAML file where you declare the **Target Machines** you want to configure, and the **Tasks** (modules) you want to execute on them. 

### The Anatomy of a Playbook
Every YAML playbook begins with `---` (three hyphens) and is divided into two main sections:
1. **Target Section**: *Who are we connecting to, and how?*
2. **Tasks Section**: *What are we doing?*

### The Target Section Explained
```yaml
---
- hosts: dev               # The target group from your inventory file
  become: yes/no           # Run as sudo? (Default: no)
  connection: ssh/winrm    # How to connect? (Default: ssh)
  become_user: username    # Change the username at runtime
  gather_facts: yes/no     # Gather machine info before running?
```
*(In most real-world playbooks, you only need to specify `hosts` and `become`).*

---

## 🧪 2. The Golden Rule: The Dry Run (`--check`)

Before we run our first playbook, you must learn the most important command in Ansible:
```bash
ansible-playbook 1.yml --check
```
> [!IMPORTANT]
> The `--check` flag performs a **Dry Run**. It simulates the entire playbook execution end-to-end without actually making any changes to the slave machines! Always run this first to catch syntax errors or logic issues!

When you are confident, run the playbook for real:
```bash
ansible-playbook 1.yml
```

---

## 🛠️ 3. Practical Playbook Labs

Let's dive into 7 real-world playbook examples to master the syntax!

### Lab 1: Installing a Package (Git)
First, log in as root and navigate to the ubuntu home directory where we will store our playbooks:
```bash
sudo su
cd /home/ubuntu
vi 1.yml
```

If we were using an Ad-Hoc command, it would look like this: `ansible dev -b -m apt -a "name=git state=present"`.
Here is how we convert that into a Playbook:

```yaml
# 1.yml
---
- name: Install Packages
  hosts: dev
  tasks:
    - name: Install git
      apt: 
        name: git 
        state: present
```
*(Note: Be careful, it is `state=present`, not `status=present`!)*

To execute it:
```bash
ansible-playbook 1.yml --check
ansible-playbook 1.yml
```

### Lab 2: Creating a File
```bash
vi 2.yml
```

```yaml
# 2.yml
---
- name: Creation of the file 
  hosts: dev
  tasks:
    - name: Create a new text file
      file: 
        path: /home/ubuntu/xyz.txt 
        state: touch
```

To execute it:
```bash
ansible-playbook 2.yml --check
ansible-playbook 2.yml
```

### Lab 3: Copying Files (Master to Slave)
If we were using an Ad-Hoc command, it would look like this: `ansible dev -b -m copy -a "src=/home/ubuntu/456.txt dest=/home/ubuntu/"`.
Here is the Playbook version:

```bash
vi 3.yml
```

```yaml
# 3.yml
---
- name: Copy file to slave machines
  hosts: dev
  tasks:
    - name: Push text file to slaves
      copy: 
        src: /home/ubuntu/456.txt 
        dest: /home/ubuntu/
```

To execute it:
```bash
ansible-playbook 3.yml --check
ansible-playbook 3.yml
```

### Lab 4: Setting Strict File Permissions
```bash
vi 4.yml
```

```yaml
# 4.yml
---
- name: Set secure file permissions
  hosts: dev
  become: yes
  tasks:
    - name: Secure xyz.txt
      file: 
        path: /home/ubuntu/xyz.txt 
        owner: root 
        group: root 
        mode: '0644'
```

To execute it:
```bash
ansible-playbook 4.yml
```

### Lab 5: Targeting ALL Hosts
```bash
vi 5.yml
```

```yaml
# 5.yml
---
- name: Install Apache on all slave machines
  hosts: all
  become: yes
  tasks:
    - name: Install apache2
      apt: 
        name: apache2 
        state: present
```

To execute it:
```bash
ansible-playbook 5.yml --check
ansible-playbook 5.yml
```

### Lab 6: Updating All Packages on the Server
```bash
vi 6.yml
```

```yaml
# 6.yml
---
- name: Server Maintenance
  hosts: dev
  become: yes
  tasks:
    - name: Update all packages to the latest version
      apt: 
        name: "*" 
        state: latest
```

To execute it:
```bash
ansible-playbook 6.yml
```

### Lab 7: Multi-Task Playbooks
Playbooks are executed **sequentially** from top to bottom. At any given point in time, Ansible will perform only one task at a time; it will pick Task 1, connect to the slave machines to execute it, and only then proceed to Task 2. *(This is the default behavior, though it can be changed in advanced setups).*

```bash
vi 7.yml
```

```yaml
# 7.yml
---
- name: Provision Web Server
  hosts: dev
  become: yes
  tasks:
    - name: Install git
      apt: 
        name: git 
        state: present
        
    - name: Install apache2
      apt: 
        name: apache2 
        state: present
```

To execute it:
```bash
ansible-playbook 7.yml
```

---

## 🎯 4. Instructor Tasks (Homework Solutions)

Your instructor gave you two tasks to write on your own. Here are the perfect Zero-to-Hero solutions!

### Task 1: Write a playbook to download a file from the internet
*(Solution: We use the `get_url` module, which acts exactly like `wget` in Linux).*
```yaml
---
- name: Download external file
  hosts: dev
  become: yes
  tasks:
    - name: Download AWS CLI installer
      get_url:
        url: https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip
        dest: /home/ubuntu/awscli.zip
```

### Task 2: Write a playbook to execute a Linux command
*(Solution: We use the `shell` module, which gives us full Bash capabilities).*
```yaml
---
- name: Execute raw Linux commands
  hosts: dev
  become: yes
  tasks:
    - name: Check free memory on slaves
      shell: free -m
      register: memory_output    # Bonus: Saves the output to a variable!

    - name: Print the memory output to the screen
      debug:
        var: memory_output.stdout
```
