# Ansible Day 6: Global Variables & Advanced Execution

Welcome to Day 6! Today we are tackling some of the most confusing concepts in Ansible: Global Variables, Parallel Execution (`async`), and Advanced Targeting (`run_once` vs `delegate_to`). 

I have broken down the theory and the practical labs so they are crystal clear and impossible to misunderstand!

---

## 🔄 0. Quick Recap (From Day 5)
Before we start, let's quickly recap what we learned yesterday:
- **Handlers:** What is the default behavior of Ansible? It runs one task at a time. By using `notify` and `handlers`, we create 1-to-1 dependencies. The key value must be exactly the same!
- **Variables:** There are Local variables (inside the playbook) and Global variables (outside).

---

## 🌍 1. Global Variables (`group_vars` and `host_vars`)

Yesterday we learned about Local Variables (defined inside a single playbook). But what if you have 10 playbooks that all need the exact same variable? You don't want to copy-paste it 10 times. You use **Global Variables**.

There are two types of Global Variables:
1. **`group_vars`:** Variables that apply to a specific *group* of machines (e.g., all machines in `[dev]`).
2. **`host_vars`:** Variables that apply to a specific *individual machine* (e.g., only `NODE1`).

### Lab 1: Setting up `group_vars`
Global variables are not stored inside your playbook. They are stored in dedicated folders inside `/etc/ansible`.

```bash
# 1. Go to the Ansible root directory
cd /etc/ansible
ls
mkdir group_vars
cd group_vars

# 2. Create a file with the EXACT name of your group!
vi dev.yml
```
Inside `dev.yml`, define your global variable:
```yaml
---
my_name: Kousik
```
Now, ANY playbook that targets `hosts: dev` will automatically inherit the `my_name` variable without you having to define it in the playbook!

### Lab 2: Setting up `host_vars`
If you want a variable to apply ONLY to `NODE1`, you use `host_vars`:

```bash
cd /etc/ansible
mkdir host_vars
cd host_vars

# Create a file with the EXACT name of your machine!
vi NODE1
```
Inside the `NODE1` file:
```yaml
---
my_name: Dhoni
```

### Lab 3: Testing the Global Variables
Let's write a playbook without any `vars` section and let Ansible magically find the global variables!
```bash
cd /home/ubuntu
vi variable.yml
```
```yaml
---
- name: Print my name
  hosts: dev
  become: yes
  tasks:
    - name: Print my name 
      command: echo "My name is {{my_name}}"
```

```bash
ansible-playbook variable.yml
# To see verbose details:
ansible-playbook variable.yml -v
```

If you run `ansible-playbook variable.yml`, `NODE1` will print "Dhoni" (because `host_vars` override `group_vars`), and `NODE2` will print "Kousik" (because it falls back to `group_vars`)!

---

## 🚀 2. Parallel Execution (`async` and `poll`)

By default, Ansible runs in **Sequential Order**. It picks Task 1, finishes it on all machines, and then moves to Task 2. 
If you have a task that takes 30 minutes to complete (like a massive database backup), Ansible will "freeze" your terminal for 30 minutes.

We can fix this by telling Ansible to run the task in the background (asynchronously) in parallel!

```yaml
# async.yml
---
- hosts: dev
  become: yes
  tasks:
    - name: Sleep for 30 seconds in the background
      command: sleep 30
      async: 30
```
```bash
ansible-playbook async.yml
```
Now it will run the same task at the same time in parallel on all machines!

### Using `poll` (Checking Status)
- **`poll: <seconds>`**: Tells Ansible, *"Go into the machine every X seconds and print what is happening inside."*

```yaml
# async.yml
---
- hosts: dev
  become: yes
  tasks:
    - name: Sleep for 30 seconds in the background
      command: sleep 30
      async: 30
      poll: 10
```
```bash
ansible-playbook async.yml
```
When you run this, Ansible will start the sleep command, but instead of completely freezing, it will check the machine every 10 seconds to see if it is done!

---

## 💾 3. The `register` and `debug` Modules

If you run a Linux command via Ansible (like `uptime`), Ansible will NOT print the output to the screen by default. It just tells you "SUCCESS".

If you actually want to see the output, you must capture it using `register`, and print it using `debug`.

```yaml
# out.yml
---
- hosts: dev
  become: yes
  tasks:
    - name: Run a raw command
      command: echo "Hi Hello"
      register: output              # Captures the raw output into a variable named "output"

    - name: Print the captured output to the screen
      debug: 
        var: output
```
```bash
ansible-playbook out.yml
```
`register` is the module used to capture the output, which you can use at a later point in time. 

However, I don't want to print *everything* (because `output` contains a massive block of metadata). I want to print a particular thing only! We use `varname.attribute` syntax:

```yaml
# out.yml
---
- hosts: dev
  become: yes
  tasks:
    - name: Run a raw command
      command: echo "Hi Hello"
      register: output              

    - name: Print the return code ONLY
      debug: 
        var: output.rc          # Only prints the Return Code (e.g., 0 for success)
```
```bash
ansible-playbook out.yml
```

---

## 🎯 4. Advanced Targeting (`run_once` vs `delegate_to`)

This is the most confusing part of Ansible. Let's make it incredibly simple.
Assume your `[dev]` group has **3 machines**.

### Scenario A: `run_once`
I want to run a task, but I ONLY want it to run **exactly one time**, on one single random machine. I don't care which machine it is. I just don't want it running 3 times.

```yaml
# runonce.yml
---
- hosts: dev
  become: yes
  tasks:
    - name: Print my name
      command: echo "Hi Hello"
      run_once: true   # <--- Runs 1 time on a random machine, and skips the other 2.
```
```bash
ansible-playbook runonce.yml
```

**What happens if we remove it?**
```yaml
# runonce.yml
---
- hosts: dev
  become: yes
  tasks:
    - name: Print my name
      command: echo "Hi Hello"
      # run_once: true   
```
```bash
ansible-playbook runonce.yml
```
Now it will run on ALL machines normally!

### Scenario B: `delegate_to`
I have 3 machines in my `[dev]` group. But for this specific task, I want to execute it specifically on `NODE2`. 

**The Catch:** Because your `hosts: dev` group has 3 machines, Ansible will trigger this task 3 times... but because you used `delegate_to: NODE2`, it will execute the task **3 times on NODE2**! All requests get funneled to that specific machine.

```yaml
# delegateto.yml
---
- hosts: dev
  become: yes
  tasks:
    - name: Print my name
      command: echo "Hi Hello"
      delegate_to: NODE2   # <--- Runs 3 times, all on NODE2.
```
```bash
ansible-playbook delegateto.yml
```

### Scenario C: The Perfect Combo (`run_once` + `delegate_to`)
If you want to run a task exactly **one time**, and you want it to happen specifically on **NODE2**:

```yaml
# runonce_delegateto.yml
---
- hosts: dev
  become: yes
  tasks:
    - name: Print my name
      command: echo "Hi Hello"
      run_once: true
      delegate_to: NODE2   # <--- Runs exactly 1 time, exclusively on NODE2.
```
```bash
ansible-playbook runonce_delegateto.yml
```
*Master this combo, and you will ace any advanced Ansible interview!*
