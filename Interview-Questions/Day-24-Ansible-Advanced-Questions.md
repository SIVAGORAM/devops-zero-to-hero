# Day 24: Advanced Ansible - Interview Questions

---

### Q1: How does Ansible know the Operating System of the target server without you telling it?
**Answer:**  
When a playbook runs, Ansible automatically executes the `setup` module as the very first step. This module gathers "Facts" (system data) about the target server, including its IP address, CPU, Memory, and Operating System (`ansible_os_family`). We can use these facts dynamically in our playbooks.

### Q2: How do you handle running a playbook against a mixed environment of Ubuntu and CentOS servers?
**Answer:**  
I would use the `when` conditional statement combined with Ansible Facts. I would write one task using the `apt` module with the condition `when: ansible_os_family == "Debian"`, and another task using the `yum` module with `when: ansible_os_family == "RedHat"`. This ensures the correct package manager is used for the correct server.

### Q3: What is the difference between a Task and a Handler in Ansible?
**Answer:**  
A **Task** runs every single time the playbook is executed (though it won't make changes if the state is already correct due to idempotency). 
A **Handler** is a special type of task that *only* runs if it is actively triggered by the `notify` keyword from another task. Handlers are typically used for restarting services only when a configuration file has actually been modified.

### Q4: How do you protect sensitive passwords in your Ansible code before pushing to GitHub?
**Answer:**  
I use **Ansible Vault**. It encrypts YAML files (or specific variables) using a password. When I run the playbook, I pass the `--ask-vault-pass` flag so Ansible can decrypt the file in memory during execution. This ensures no plain-text secrets are ever pushed to the version control system.

---
**[Previous: Day 22 - Ansible Questions](./Day-22-Ansible-Questions.md)** | **[Next: Top 18 Ansible Interview Questions](./Top-18-Ansible-Questions.md)**
