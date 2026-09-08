# Ansible Day 9: Roles and Best Practices

Welcome to Day 9! As your infrastructure grows, writing everything inside a single playbook becomes a messy, unmanageable nightmare. Today we solve this problem using **Ansible Roles**.

---

## 🧩 1. What are Ansible Roles?

To understand Roles, let's look back at Terraform. In Terraform, we use **Modules** to break our massive infrastructure into reusable, independent chunks (`main.tf`, `vpc`, `ec2`, `securitygroup`).

**In Ansible, Roles are exactly the same concept.** Instead of having one massive playbook file with 100 tasks, 50 variables, and 10 handlers, a Role splits them up into a clean folder structure.

### The Role Directory Structure
A role is simply a major folder (e.g., `dev`) that contains specific sub-folders. Every sub-folder must contain a file named `main.yml`.

```text
roles/
└── dev/
    ├── tasks/
    │   └── main.yml
    ├── vars/
    │   └── main.yml
    └── handlers/
        └── main.yml
```
*(Note: You can create your `roles` folder anywhere, but by default, Ansible will look in `/etc/ansible/roles` or the directory where your master playbook lives).*

---

## 🏗️ 2. Creating Your First Role (`dev`)

Let's manually build a role from scratch instead of putting everything into a single file!

### Step 1: Create the Folder Structure
```bash
cd /home/ubuntu
mkdir roles
cd roles

# Create the specific role folder
mkdir dev
cd dev

# Create the standard Ansible sub-folders inside the role
mkdir tasks vars handlers
ls

# View your beautiful new structure!
cd ..
tree
```

### Step 2: Write the Code in Separate Files
Now, instead of one massive file, we put specific code into its corresponding `main.yml` file!

**1. Define the Tasks:**
```bash
vi dev/tasks/main.yml
```
```yaml
# dev/tasks/main.yml
---
- name: print my name
  command: echo "My name is {{my_name}}"
  notify: successful execution

- name: EOT
  command: echo "Task EOT"
```
*(Note: I fixed the spelling of `succeeful` to `successful` from your raw notes so it matches the handler perfectly!)*

**2. Define the Variables:**
```bash
vi dev/vars/main.yml
```
```yaml
# dev/vars/main.yml
---
my_name: siva
```

**3. Define the Handlers:**
```bash
vi dev/handlers/main.yml
```
```yaml
# dev/handlers/main.yml
---
- name: successful execution
  command: echo "The handler ran successfully! Name is {{my_name}}"
```
*(Note: Your raw notes had `command: name is {{my_name}}`. This is not a valid Linux command and would crash the playbook! I added the `echo` command so it works perfectly).*

### Step 3: Create the Master Playbook
Now that your `dev` role is completely built, you need a way to execute it. We do this by creating a highly simplified `master.yml` file outside the role folder.

```bash
cd /home/ubuntu/roles
vi master.yml 
```
```yaml
# master.yml
---
- hosts: dev
  become: yes
  roles:
    - dev    # <--- This automatically loads tasks, vars, and handlers from the dev folder!
```

To run it and verify the directory:
```bash
ansible-playbook master.yml
ls
tree
```

---

## 🧪 3. Cloning and Modifying Roles (`test` role)

In your notes, your instructor asked: *"We copied the dev role to test. How do we change it and call it from the master file?"* 

Here is exactly how you do it!

### Step 1: Clone the Role
Instead of recreating the folder structure manually, we just copy the entire `dev` folder and name it `test`:
```bash
# We are inside the /home/ubuntu/roles directory
cp -R dev test
ls
```
*(Now you have two identical roles: `dev` and `test`!)*

### Step 2: Modify the `test` Role Content
Let's change the variables in the `test` role so it behaves differently than the `dev` role!

```bash
vi test/vars/main.yml
```
Change the variable inside:
```yaml
# test/vars/main.yml
---
my_name: Dhoni
```

### Step 3: Update `master.yml` to call both Roles!
Now we want to run our playbook so that the `dev` group uses the `dev` role, and the `test` group uses the `test` role!

```bash
vi master.yml
```
```yaml
# master.yml
---
# 1. Target the dev servers using the dev role
- hosts: dev
  become: yes
  roles:
    - dev

# 2. Target the test servers using the test role
- hosts: test
  become: yes
  roles:
    - test
```

When you run `ansible-playbook master.yml` now, Ansible will elegantly execute both roles on their respective environments without a single line of messy, hardcoded tasks in your master file!

---

## 🏆 4. Ansible Best Practices

To be a true DevOps Engineer, you must follow these industry-standard best practices:

1. **Version Control:** Always maintain version control (Git/GitHub) for your Ansible configuration files and playbooks.
2. **Environment Separation:** Maintain completely different inventory files for different environments (e.g., `inventory_dev.ini`, `inventory_test.ini`, `inventory_prod.ini`).
3. **Secret Management:** NEVER store passwords or sensitive data in plain text. Always encrypt them using **Ansible Vault**.
4. **Debugging:** Set the log level or use verbose mode (`-v`, `-vvv`) to debug issues effectively.
5. **Use Roles:** Never write massive, single-file playbooks. Always divide your code into modular, reusable **Roles**.
6. **Standardization:** Maintain a strict directory layout and consistent naming conventions for all your variables, tags, and files!
