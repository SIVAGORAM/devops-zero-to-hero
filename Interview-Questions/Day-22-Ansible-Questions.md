# Day 22: Configuration Management & Ansible - Interview Questions

---

### Q1: What programming language is Ansible written in? What language do you use to write Ansible playbooks?
**Answer:**  
Ansible is written in **Python** under the hood. However, as a DevOps engineer, you do not write Python code to use it. You write Ansible configurations (Playbooks) using **YAML** (YAML Ain't Markup Language), which is extremely simple and human-readable.

### Q2: Does Ansible support both Windows and Linux?
**Answer:**  
Yes, Ansible supports both. For Linux servers, it connects natively using the **SSH protocol**. For Windows servers, it connects using the **WinRM protocol** (Windows Remote Management).

### Q3: Explain the difference between a Push model and a Pull model in configuration management.
**Answer:**  
In a **Pull model** (like Puppet or Chef), an agent is installed on the target servers. This agent constantly polls the central master server at regular intervals to "pull" down new configurations. 
In a **Push model** (like Ansible), there are no agents. The central control node actively initiates the connection and "pushes" the configurations or commands out to the target servers exactly when the engineer executes the playbook.

### Q4: Why did you choose Ansible over Puppet or Chef?
**Answer:**  
I prefer Ansible primarily because of its **Agentless architecture**. I do not have to waste time installing and maintaining agent software on 10,000 target servers; Ansible just uses native SSH. Secondly, it uses a **Push model**, which gives me immediate control over when changes happen. Finally, it uses **YAML** instead of a complex proprietary language (like Puppet's Ruby DSL), making it incredibly easy for the team to learn and read.

### Q5: Does Ansible support all cloud providers?
**Answer:**  
Yes! Ansible is cloud-agnostic. It has thousands of built-in modules that allow you to provision and configure resources across AWS, Azure, Google Cloud, VMware, and on-premise bare-metal servers.

---
**[Previous: Day 19 - AWS CLI Questions](./Day-19-AWS-CLI-Questions.md)**
