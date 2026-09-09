# 🚀 Ansible Zero-to-Hero: Ultimate Speed Revision Guide

This is your master cheat sheet. If you have an interview in 1 hour or need to rapidly build an automation script, this document contains every core concept from Day 1 to Day 9. 

---

## 🏗️ 1. Introduction & Architecture (Days 1-2)

### Core Concepts
- **What is Ansible?** A Configuration Management tool used to automate infrastructure setup, application deployment, and task execution across thousands of servers simultaneously.
- **Push-Based:** You write code on a central machine, and Ansible "pushes" the changes to the slave machines. *(Puppet/Chef are Pull-based).*
- **Agentless:** You do NOT need to install any Ansible software on the slave nodes. Ansible communicates over standard protocols (SSH for Linux, WinRM for Windows).
- **Idempotency:** Ansible only makes changes if necessary. If you tell it to install Apache, and Apache is already installed, it does nothing.

### Architecture
1. **Controller Node:** The machine where Ansible is installed.
2. **Managed Nodes (Slaves):** The target machines you want to configure.
3. **Inventory:** A file (`/etc/ansible/hosts`) containing the IP addresses of your slaves.

---

## ⚙️ 2. Configuration & Authentication (Days 2-3)

Ansible needs to know *where* to connect and *how* to authenticate.

### SSH Key Authentication
Ansible uses SSH. Instead of typing passwords, we use SSH keys.
```bash
# On Controller: Generate Key
ssh-keygen

# Copy Key to Slave
ssh-copy-id username@<slave-ip>
```

### The Inventory File (`/etc/ansible/hosts`)
Where you list your target machines. You can group them logically!
```ini
[dev]
192.168.1.10
192.168.1.11

[test]
192.168.1.20
```

### The Configuration File (`/etc/ansible/ansible.cfg`)
This file dictates how Ansible behaves by default. Important settings include:
- `inventory = /etc/ansible/hosts` (Sets the default inventory path so you don't have to use `-i`).
- `host_key_checking = False` (Disables the strict SSH key checking prompt).

---

## ⚡ 3. Ad-Hoc Commands (Day 3)

For simple, one-time tasks, you don't need a playbook. You use Ad-Hoc commands.

**Syntax:** `ansible <target> -b -m <module> -a "<arguments>"`
- `-b`: Become (run as root / sudo)
- `-m`: Module name
- `-a`: Arguments

### The 34-Module Dictionary (`ansible-doc`)
If you forget how a module works or what arguments it takes, use the built-in dictionary:
- `ansible-doc -l` (Lists all available modules).
- `ansible-doc <module_name>` (Shows documentation and examples for a specific module).

### Crucial Modules & Differences:
- **Connectivity Test:** `ansible all -m ping`
- **`command` vs `shell`:** 
  - `command`: Runs raw Linux commands (`ansible dev -b -m command -a "uptime"`).
  - `shell`: Use this if your command has special characters like pipes (`|`, `>`, `<`) (`ansible dev -b -m shell -a "ls -l > out.txt"`).
- **`copy` vs `fetch`:**
  - `copy`: Pushes a file FROM the Controller TO the Slave. (`ansible dev -b -m copy -a "src=./file dest=/tmp/"`)
  - `fetch`: Pulls a file FROM the Slave TO the Controller. (`ansible dev -b -m fetch -a "src=/tmp/log dest=./"`)
- **Create User:** `ansible dev -b -m user -a "name=siva state=present"`
- **Install Package (Ubuntu):** `ansible dev -b -m apt -a "name=git state=present"`
- **Manage Service:** `ansible dev -b -m service -a "name=apache2 state=started"`

---

## 📜 4. Playbooks & Order of Operations (Day 4)

For complex, multi-step operations, we use Playbooks (YAML files). 

### The Golden Rule of Order
Every playbook must follow this strict block order:
1. **Target Section:** (`hosts`, `become`)
2. **Variable Section:** (`vars`)
3. **Task Section:** (`tasks`)
4. **Handler Section:** (`handlers`)

### Basic Playbook Example
```yaml
---
- hosts: dev
  become: yes
  tasks:
    - name: Update apt cache
      apt: update_cache=yes
      
    - name: Install Apache
      apt: name=apache2 state=present
```
**Execution:** `ansible-playbook setup.yml`
**Dry Run (Test without making changes):** `ansible-playbook setup.yml --check`

---

## 🗃️ 5. Variables & Handlers (Days 5-6)

### Variables
Store data once, use it everywhere via `{{ variable_name }}`.
1. **Local Variables:** Defined inside the playbook (`vars:`).
2. **External Variables:** Defined in a separate YAML file (`vars_files:`).
3. **Command Line:** Injected at runtime (`--extra-vars "my_name=Siva"`).
4. **Global Variables:** Automatically loaded based on inventory group or host.
   - `/etc/ansible/group_vars/<group_name>.yml`
   - `/etc/ansible/host_vars/<host_name>.yml` *(Overrides group_vars)*

### Handlers (The Dependency Mechanism)
In Terraform, we have Default, Implicit, and Explicit dependencies to control the order of creation. In Ansible, tasks run sequentially by default. If we want a task to run **ONLY IF** a previous task successfully executed and made a change, we use **Handlers**.
- Connect them using `notify: <name_of_handler>`. The string must exactly match!

```yaml
---
- hosts: dev
  become: yes
  tasks:
    - name: Change config
      copy: src=config dest=/etc/
      notify: restart apache  # <--- MUST EXACTLY MATCH HANDLER NAME

  handlers:
    - name: restart apache
      service: name=apache2 state=restarted
```

---

## ⏱️ 6. Advanced Execution Control (Day 6)

### Parallel Execution (`async` and `poll`)
Prevents Ansible from freezing your terminal during long tasks.
- `async: 30` (Run in background, timeout after 30s).
- `poll: 5` (Check status every 5s).

### Capturing Output (`register` and `debug`)
Store the output of a command into a variable to print or use later.
```yaml
    - name: Run command
      command: uptime
      register: my_output

    - name: Print output
      debug: var=my_output.stdout  # Use .stdout to skip JSON metadata
```

### Delegation & Limiting Execution
- **`run_once: true`**: Run the task exactly ONE time on ONE random machine.
- **`delegate_to: NODE2`**: Funnel the execution to a specific machine.
- *(Combo: Use both to run a task exactly once, exclusively on NODE2!)*

---

## 🔁 7. Loops and Conditionals (Day 7)

### Loops (`with_items`)
Stop repeating tasks! Use loops to iterate over lists or dictionaries.
```yaml
    - name: Create multiple users
      user: name="{{ item }}" state=present
      with_items:
        - siva
        - rama
```

### Conditionals (`when`) & Gathering Facts (`setup`)
Ansible runs the `setup` module implicitly to gather facts (like OS type) before tasks run. You use `when` to evaluate these facts.

**Interview Classic: Multi-OS installation:**
```yaml
    - name: Install on Ubuntu
      apt: name=apache2 state=present
      when: ansible_os_family == "Debian"

    - name: Install on RedHat
      yum: name=httpd state=present
      when: ansible_os_family == "RedHat"
```

---

## 🛑 8. Error Handling, Tags, and Vault (Day 8)

### Error Handling (`ignore_errors`)
By default, Ansible crashes on the first error. Use `ignore_errors: yes` at the task level to bypass errors and continue the playbook.

### Tags (`tags`)
Attach labels to tasks so you can run them selectively.
- Run only specific tags: `ansible-playbook file.yml --tags mytag`
- Run everything EXCEPT tags: `ansible-playbook file.yml --skip-tags mytag`

### Ansible Vault (Encryption)
Never store passwords in plain text. Use Vault to encrypt YAML variable files.
- **Create:** `ansible-vault create secret.yml`
- **View/Edit:** `ansible-vault view secret.yml` / `ansible-vault edit secret.yml`
- **Change Password:** `ansible-vault rekey secret.yml`
- **Encrypt/Decrypt:** `ansible-vault encrypt secret.yml` / `ansible-vault decrypt secret.yml`
- **Run Playbook:** `ansible-playbook master.yml --ask-vault-pass`

---

## 🧩 9. Ansible Roles & Best Practices (Day 9)

### Ansible Roles
Instead of massive, 1000-line playbooks, we break code into highly reusable **Roles** (identical to Terraform Modules). 
A Role is a directory structure containing specific `main.yml` files.

```text
roles/
└── dev/
    ├── tasks/main.yml
    ├── vars/main.yml
    └── handlers/main.yml
```

**Executing a Role:**
Create a master playbook outside the role folder:
```yaml
---
- hosts: dev
  become: yes
  roles:
    - dev
```

### Top 6 Industry Best Practices
1. **Version Control:** Store all playbooks and roles in Git.
2. **Environment Separation:** Use separate inventory files (e.g., `inventory_dev`, `inventory_prod`).
3. **Secret Management:** Always use Ansible Vault for sensitive data.
4. **Debugging:** Set verbose modes (`-v`, `-vv`) to troubleshoot.
5. **Modularity:** Never write monolithic playbooks; always use **Roles**.
6. **Standardization:** Maintain strict naming conventions and directory layouts.
