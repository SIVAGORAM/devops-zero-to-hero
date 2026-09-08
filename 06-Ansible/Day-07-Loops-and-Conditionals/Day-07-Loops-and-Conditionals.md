# Ansible Day 7: Loops and Conditional Statements

Welcome to Day 7! Today we are learning how to write cleaner, more efficient playbooks by utilizing **Loops** (to avoid repeating ourselves) and **Conditional Statements** (to make our playbooks smart enough to adapt to different Operating Systems).

---

## 🔁 1. Ansible Loops (`with_items`)

### The Problem: Repeating Yourself
Imagine you are asked to create 5 new users on a server. If you don't know how to use loops, you would have to write the exact same task 5 times:

```yaml
---
- hosts: dev
  become: yes
  tasks:
    - name: create a user
      user: name=siva state=present
    - name: create a user
      user: name=ram state=present
    - name: create a user
      user: name=teja state=present
    - name: create a user
      user: name=example state=present
    - name: create a user
      user: name=etc state=present
```
This is terrible practice. If you needed to create 100 users, your playbook would be thousands of lines long!

### The Solution: Using Loops
In Ansible, we use the `with_items` keyword to define a list of items, and the `{{ item }}` placeholder to iterate through them. For each and every iteration, Ansible will run the task with the new item.

```yaml
# loop1.yml
---
- hosts: dev
  become: yes
  tasks:
    - name: create multiple users dynamically
      user: 
        name: "{{ item }}" 
        state: present
      with_items:
        - siva
        - jaya
        - ram
        - teja
        - sita
```

```bash
vi loop1.yml
ansible-playbook loop1.yml
```

### Advanced Loops (Dictionaries)
What if you need to pass multiple variables per loop? For example, different users might need to be assigned to different Linux groups. You can pass a dictionary of items!

*(Note: In your raw notes, the syntax was written as `name={{item}}`. I have corrected this to `name="{{ item.name }}"` and `groups="{{ item.groups }}"` because when passing a dictionary, you must explicitly call the keys, otherwise Ansible will crash!)*

```yaml
---
- hosts: dev
  become: yes
  tasks:
    - name: create users with specific groups
      user: 
        name: "{{ item.name }}" 
        groups: "{{ item.groups }}"
        state: present
      with_items:
        - { name: susitra, groups: root }
        - { name: Jeevan, groups: nogroup }
```

---

## 🧠 2. The `setup` Module (Gathering Facts)

Before we can use conditional statements, we must understand how Ansible knows things about our slave machines. 

Whenever you run a playbook (unless you explicitly set `gather_facts: no`), Ansible secretly runs a module called `setup` in the background before running your tasks. 
It collects all the details about the slave machine (OS, IP, CPU, RAM) and stores them in variables.

To see what this looks like manually via Ad-Hoc:
```bash
ansible dev -b -m setup
```
One of the most important variables it collects is `ansible_os_family`, which tells us if the machine is Debian (Ubuntu) or RedHat (CentOS/Amazon Linux).

---

## 🔀 3. Conditional Statements (`when`)

In normal programming languages, you use `if` / `else` to control the flow:
- `if (os == ubuntu)` -> install apache2 using apt
- `if (os == redhat)` -> install httpd using yum

In Ansible, the conditional statement keyword is **`when`**.

### 🌟 Classic Interview Question 🌟

> [!IMPORTANT]
> **Interview Question:** How do you write a single playbook to install a web server on a mixed environment of both Ubuntu and RedHat machines?
> 
> **Answer:** You use the `when` condition to check the `ansible_os_family` fact gathered by the `setup` module!

Here is the exact code you must memorize for interviews:

```bash
vi condition.yml 
```

```yaml
# condition.yml
---
- name: Install web servers across multiple OS families
  hosts: all
  become: yes
  tasks:
    - name: install git (Works on both if using apt/yum appropriately, but here we assume Debian)
      apt: 
        name: git 
        state: present
      when: ansible_os_family == "Debian"

    - name: install apache2 on Ubuntu/Debian machines
      apt: 
        name: apache2 
        state: present
      when: ansible_os_family == "Debian"

    - name: install httpd on RedHat/CentOS machines
      yum: 
        name: httpd 
        state: present
      when: ansible_os_family == "RedHat"
```
*(Note: I updated the third task to use `yum` since it targets RedHat. Using `apt` on RedHat will fail even if the condition is met!)*

```bash
ansible-playbook condition.yml
```
When you run this playbook, Ansible will evaluate the OS of every single slave machine. If a machine is Ubuntu, it will install `apache2` and simply skip the `httpd` task. If the machine is RedHat, it will skip `apache2` and install `httpd`!
