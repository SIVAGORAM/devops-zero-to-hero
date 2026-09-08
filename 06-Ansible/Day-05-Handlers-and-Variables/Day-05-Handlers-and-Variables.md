# Ansible Day 5: Handlers and Variables

Welcome to Day 5! Today we master two incredibly powerful concepts in Ansible that separate junior engineers from seniors: **Handlers** (Task Dependencies) and **Variables** (Reusability).

---

## 🔗 1. Understanding Task Dependencies

To understand how Ansible handles tasks, let's briefly look at how Terraform handles dependencies:
1. **Default Dependencies:** If I want to create an EC2 and an S3 bucket, they have no relation. Terraform creates them both in parallel.
2. **Implicit Dependencies:** I want to create an EC2 machine and an Elastic IP. Terraform knows it *must* create the EC2 first before it can attach the IP. 
3. **Explicit Dependencies:** I want to force Terraform to create the EC2 first, and *then* the S3 bucket. We forcefully create this using `depends_on`.

**How does this relate to Ansible?**
In Ansible, the default behavior is to blindly run tasks one after another from top to bottom. But what if we have a strict requirement? What if we *only* want to run Task #2 if Task #1 actually made a change? 

### The Problem with Default Behavior
Look at this basic playbook:
```yaml
---
- name: Default playbook behavior
  hosts: all
  become: yes
  tasks:
    - name: install git
      apt: 
        name: git 
        state: present
        
    - name: install apache2
      apt: 
        name: apache2 
        state: present
        
    - name: start the service
      service: 
        name: apache2 
        state: started
```

```bash
sudo su
ansible-playbook handler.yml
```

If we run this, Ansible will blindly run the tasks one after another. It will always try to start the Apache service, even if nothing was actually installed or updated. This is inefficient. 

We want to tell Ansible: *"ONLY start/restart the service IF the Apache installation actually made a change to the server."*

---

## ⚡ 2. The Solution: Handlers (`notify`)

To create an explicit dependency between tasks in Ansible, we use **Handlers**. Handlers are exactly like regular tasks, but they **only run if they are notified**.

> [!IMPORTANT]
> **Interview Question: When do you use Handlers?**
> **Answer:** You use handlers when you want to restart a service (like Nginx or Apache) *only* if a configuration file was changed or a package was updated. A handler will only run ONCE at the very end of the playbook, no matter how many times it was notified.

### How to use a Handler
To use a handler, you need two things:
1. The `notify` keyword inside your main task.
2. A `handlers` section at the bottom of your playbook.

```yaml
# handler.yml
---
- name: Install a package and use handlers
  hosts: all
  become: yes
  tasks:
    - name: install git
      apt: 
        name: git 
        state: present
        
    - name: install apache2
      apt: 
        name: apache2 
        state: present
      notify: start the service     # <--- This MUST match the handler name exactly!

  handlers:
    - name: start the service
      service: 
        name: apache2 
        state: started
```
### Verifying the Handler
If you run this playbook, the handler will run. 
If you run the playbook a *second* time, the `apt` task will say "OK" (no changes made because of Idempotency). Because there were no changes, the `notify` trigger never fires, and the handler is completely skipped!

To force the handler to run again, you can manually uninstall Apache using an ad-hoc command:
```bash
ansible dev -b -m apt -a "name=apache2 state=absent"
```
Now, if you run the playbook, Ansible will install Apache (triggering a change), which notifies the handler to start the service!

---

## 🗃️ 3. Ansible Variables

**Variable Sections:** Store once, use wherever you want. There are two main types:
1. **Local Variables:** Only accessible inside the playbook where they are defined. Not accessible outside.
2. **Global Variables:** Accessible across multiple playbooks.

> [!NOTE]
> **What is a Local Variable?** Locals mean the values do not change. You define it once, use it wherever you want, and basically, it is static!

### The Golden Rule of Playbook Order
Before defining variables, you must always follow this strict ordering block inside your YAML file:
1. **Target Section** (`hosts`, `become`)
2. **Variable Section** (`vars`)
3. **Task Section** (`tasks`)
4. **Handler Section** (`handlers`)

### Defining Local Variables (`vars`)
You can define variables at the top of your playbook under the `vars` block, and inject them into your tasks using double curly braces `{{ }}`.

```yaml
# variable.yml
---
- name: Using Variables
  hosts: all
  become: yes
  vars:
    - package: apache2   # <--- We define the variable here
  tasks:
    - name: install git
      apt: 
        name: git 
        state: present
        
    - name: install {{package}}
      apt: 
        name: "{{package}}"  # <--- We inject it here
        state: present
      notify: start the service
      
  handlers:
    - name: start the service
      service: 
        name: "{{package}}" 
        state: started
```

### Advanced Execution: Verbose Mode
If you ever want to see extremely detailed output about what Ansible is doing under the hood (great for debugging variables), use the `-v` (verbose) flag:
```bash
ansible-playbook variable.yml -v
```

---

## 🔀 4. Overriding Variables at Runtime

You don't always want to hardcode variables inside your playbook. You might want to pass them directly from your terminal!

### The Base Playbook
```yaml
# name.yml
---
- name: Print my name
  hosts: dev
  become: yes
  vars:
    - my_name: ram
  tasks:
    - name: print my name 
      command: echo "My name is {{my_name}}"
```

### Overriding via Command Line (`--extra-vars`)
If you run `ansible-playbook name.yml`, it will print "ram". 
If you want to inject a different name without editing the file, use `--extra-vars`:
```bash
ansible-playbook name.yml --extra-vars "my_name=Dhoni" -v
```
*(Ansible will prioritize the terminal variable over the one hardcoded in the playbook!)*

---

## 📂 5. External Variable Files (`vars_files`)

If you want to override multiple values at once (or if you just have a massive list of variables), injecting them all through the terminal `--extra-vars` gets extremely messy. The best practice is to store them in a separate YAML file, and import them!

### Step 1: Create the Variables File
```yaml
# updated_vars.yml
---
my_name: Dhoni
```

### Step 2: Import it into the Playbook
Replace the `vars` keyword with `vars_files`:
```yaml
# name.yml
---
- name: Print my name
  hosts: dev
  become: yes
  vars_files:
    - updated_vars.yml   # <--- Tells Ansible to look in this external file!
  tasks:
    - name: print my name 
      command: echo "My name is {{my_name}}"
```
Run it:
```bash
ansible-playbook name.yml
```

---

## 🌍 6. Global Variables Overview

While Local variables are great, in the real world we use **Global Variables**. You define these once, and use them everywhere.
There are two main types you will learn about:
1. **`group_vars`:** Variables that apply to an entire group of servers (e.g., all machines in the `[dev]` group get `port=8080`).
2. **`host_vars`:** Variables that apply to *one specific machine* (e.g., only `NODE1` gets `database_password=secret`).
