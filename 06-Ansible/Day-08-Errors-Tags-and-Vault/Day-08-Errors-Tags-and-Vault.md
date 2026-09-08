# Ansible Day 8: Error Handling, Tags, and Vault

Welcome to Day 8! Today we are looking at three essential production skills:
1. **Error Handling:** Preventing a single failed task from crashing your entire playbook.
2. **Tags:** Executing only specific pieces of a playbook.
3. **Ansible Vault:** Encrypting passwords so they aren't stored in plain text.

*(Note: In your prompt you mentioned "tasks and filters", but your raw notes specifically covered "Tags and Vault". I have strictly followed your raw notes!)*

---

## 🛑 1. Error Handling (`ignore_errors`)

### The Default Behavior
If there is an error in an Ansible playbook while running a task, it immediately stops execution and comes out of it. It will completely skip any remaining tasks!

```bash
vi error.yml
```
```yaml
# error.yml
---
- hosts: dev
  tasks:
    - name: dummy cmd (This command does not exist!)
      command: nocmd
      
    - name: EOT
      command: echo EOT
```
If you run `ansible-playbook error.yml`, the execution stops at the first task, and the "EOT" task never runs.

### The Solution: Ignoring Errors
Sometimes we *expect* a task to fail, and we want Ansible to ignore the error and move on to the next task. We do this using `ignore_errors: yes`.

*(Note: I fixed the indentation from your raw notes. `ignore_errors` must align with the module name, not inside it!)*

```yaml
# error.yml
---
- hosts: dev
  tasks:
    - name: dummy cmd
      command: nocmd
      ignore_errors: yes    # <--- Ansible will flag the error but continue execution!
      
    - name: EOT
      command: echo EOT
```
Now if you run `ansible-playbook error.yml`, the first task fails, but the second task successfully prints "EOT".

---

## 🏷️ 2. Ansible Tags

If you have a massive playbook with 50 tasks, but you only want to execute Task 2, you don't want to run the whole file. You can attach **Tags** to specific tasks to run them selectively!

### Basic Playbook with Tags
```bash
vi tags.yml
```
```yaml
# tags.yml
---
- hosts: dev
  tasks:
    - name: Task-1
      command: echo "this is task-1"
      tags:
        - siva
        - dev

    - name: Task-2
      command: echo "this is task-2"
      tags:
        - rama

    - name: EOT
      command: echo EOT
```

### Executing Specific Tags (`--tags`)
*(Note: In your raw notes, this was written as `--tags -siva`. If you use the hyphen, Ansible might look for a tag literally named "-siva". The correct syntax is just the tag name: `--tags siva`!)*

If you only want to run the tasks tagged with "siva":
```bash
ansible-playbook tags.yml --tags siva
```
*Here, ONLY Task-1 will run. Task-2 and EOT are ignored!*

If you want to run everywhere you have the "dev" tag:
```bash
ansible-playbook tags.yml --tags dev
```

### Skipping Specific Tags (`--skip-tags`)
What if you want to run the whole playbook, but ignore a specific tag?
```bash
ansible-playbook tags.yml --skip-tags dev
```
*Now it will skip Task-1, but execute Task-2 and EOT!*

*(Note: If you run `ansible-playbook tags.yml` without any flags, it just runs all tasks normally, one by one).*

---

## 🔐 3. Ansible Vault (Encryption)

In production, you will have sensitive data like usernames and passwords. 

### The Problem: Plain Text Secrets
Imagine a playbook that loads a variable file containing a password.

*(Note: In your raw notes, you used the keyword `var_files:`. The correct Ansible keyword is `vars_files:`. I have corrected this below!)*

```yaml
# ansiblevault.yml
---
- hosts: dev
  become: yes
  vars_files:
    - /home/ubuntu/password.yml
  tasks: 
    - name: password example
      debug:
        msg: "This is username and password: {{username}} and {{password}}"
```

*(Note: In your raw notes, the variables were written as `- username:siva` which makes it a list. Variable files should be simple dictionaries. I have corrected this below!)*

```yaml
# password.yml
---
username: siva
password: 12345
```
If an unauthorized person looks at `password.yml`, they can see your password in plain text. We need to encrypt this file!

### Managing Encrypted Files with Vault

Ansible comes with `ansible-vault` installed by default to encrypt and decrypt YAML files. Delete the old `password.yml` and let's create a secure one.

**1. Create a brand new encrypted file:**
```bash
ansible-vault create password.yml
```
*(It will ask you to enter and confirm a password: `1234`. Now the data inside is completely encrypted!)*

**2. View the contents of an encrypted file:**
```bash
ansible-vault view password.yml
```
*(It will ask for your password. Only if you know it will it show you the contents!)*

**3. Edit the contents of an encrypted file:**
```bash
ansible-vault edit password.yml
```
*(You can add, remove, and save anything you want).*

**4. Reset/Change the Vault Password:**
```bash
ansible-vault rekey password.yml
```
*(It will ask for your old password, and then ask you to create a new one).*

```bash
cat password.yml
```
*(You will see that the file is still encrypted, but the locking key has changed!)*

**5. Decrypt the file completely (Remove Encryption):**
If you want to turn it back into a plain text file:
```bash
ansible-vault decrypt password.yml
```
If you run `cat password.yml` now, you can see the readable data.

**6. Encrypt an existing plain text file:**
If the file is already present in plain text and you want to lock it:
```bash
ansible-vault encrypt password.yml
```

### Executing a Playbook with Vault Files
If your playbook uses an encrypted `vars_files`, the playbook will crash because it doesn't know the password to unlock the file.

You must explicitly tell Ansible to ask you for the vault password when you run the playbook:
```bash
ansible-playbook ansiblevault.yml --ask-vault-pass
```
*It will ask for the password. Enter it, and it will execute the task successfully!*
