# Day 24: Advanced Ansible Mastery (Zero to Hero)

To truly go from "Zero to Hero" in Ansible, you must learn how to make your playbooks dynamic, secure, and intelligent. Today, we cover the final advanced concepts that every Senior DevOps Engineer uses daily.

---

## 1. Ansible Variables and Facts

Instead of hardcoding values into your playbooks (like usernames or file paths), you should use variables.

### Ansible Facts (System Data)
When Ansible connects to a server, the very first thing it does is run the `setup` module. This gathers "Facts" about the target server (e.g., its IP address, Operating System, CPU architecture).

You can see all the facts of a server using an ad-hoc command:
```bash
ansible -i inventory all -m setup
```

You can use these facts dynamically inside your playbooks:
```yaml
- name: Print the OS of the target server
  debug:
    msg: "This server is running {{ ansible_os_family }}"
```

---

## 2. Conditionals (`when` statements)

What if you have an inventory with both Ubuntu and RedHat servers? Ubuntu uses `apt` to install packages, while RedHat uses `yum`. If you run an `apt` command on RedHat, the playbook will fail!

We solve this using the `when` conditional statement.

```yaml
tasks:
  - name: Install Apache on Ubuntu/Debian
    apt:
      name: apache2
      state: present
    when: ansible_os_family == "Debian"

  - name: Install Apache on RedHat/CentOS
    yum:
      name: httpd
      state: present
    when: ansible_os_family == "RedHat"
```
*Now, the playbook is smart enough to check the OS Fact first, and only execute the correct task!*

---

## 3. Loops (`loop`)

If you want to install 5 different software packages (git, curl, wget, vim, unzip), you should not write the `apt` task 5 separate times. That violates the DRY (Don't Repeat Yourself) principle.

Use a loop to iterate through a list of items:

```yaml
tasks:
  - name: Install multiple packages
    apt:
      name: "{{ item }}"
      state: present
    loop:
      - git
      - curl
      - wget
      - vim
```
*Ansible will automatically loop through the list and install every package.*

---

## 4. Handlers (Smart Restarts)

Imagine you have a task that updates the `nginx.conf` file. If the file is updated, you must restart the Nginx service. But what if the file *hasn't* changed? Restarting the server for no reason causes unnecessary downtime.

**Handlers** are special tasks that *only run if notified* that a change actually happened.

```yaml
tasks:
  - name: Copy Nginx config file
    copy:
      src: ./nginx.conf
      dest: /etc/nginx/nginx.conf
    notify: Restart Nginx   # This triggers the handler ONLY if the file was modified!

handlers:
  - name: Restart Nginx
    service:
      name: nginx
      state: restarted
```

---

## 5. Ansible Vault (Security)

As a DevOps engineer, you will write playbooks that contain highly sensitive data (database passwords, API keys, AWS credentials). **Never commit plain-text passwords to GitHub!**

**Ansible Vault** allows you to encrypt your YAML files so hackers cannot read them.

### Encrypt a file:
```bash
ansible-vault encrypt secrets.yml
```
*(It will ask you to create a master password).*

### Edit an encrypted file:
```bash
ansible-vault edit secrets.yml
```

### Run a playbook that uses an encrypted file:
When you execute the playbook, you must tell Ansible to prompt you for the master password, otherwise, it can't read the secrets:
```bash
ansible-playbook -i inventory main.yml --ask-vault-pass
```

---

## Ansible Module Complete! 🎯
Congratulations! You now understand the full lifecycle of Ansible—from Ad-Hoc commands and basic playbooks, to Roles, Conditionals, and Vault encryption. You are officially ready to automate large-scale infrastructure!

---
**[Previous: Day 23 - Ansible Zero to Hero](./Day-23-Ansible-Zero-to-Hero.md)** | **[Next: Day 25 - Intro to Terraform](../07-Terraform/Day-25-Introduction-to-Terraform.md)**
