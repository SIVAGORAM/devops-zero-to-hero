# Top 18 Ansible Interview Questions (Zero to Hero)

These 18 questions are the most frequently asked during DevOps interviews. The answers below are structured to show **real-world experience** and practical knowledge to impress the interviewer.

---

### 1. What is Configuration Management?
**Answer:**  
Configuration Management is the process of automating, managing, and standardizing the software, operating system, and hardware configurations across thousands of servers. Instead of manually logging into servers to install software or change settings, we write code (Infrastructure as Code) to define how a server should look, and the tool ensures the server matches that state.

### 2. Do you think Ansible is better than other configuration management tools (like Puppet or Chef)? If yes, why?
**Answer:**  
Yes, I strongly prefer Ansible for three main reasons:
1. **Agentless:** Unlike Puppet or Chef, I don't have to install and maintain background agent software on my target servers. Ansible connects natively via SSH.
2. **Push Model:** I have immediate control. When I run a playbook, changes happen instantly, rather than waiting 30 minutes for a node to "pull" updates.
3. **Simplicity:** Ansible uses human-readable YAML instead of a proprietary Ruby DSL, meaning my entire team (even junior developers) can read and write playbooks easily.

### 3. Can you write an Ansible playbook to install the `httpd` (Apache) service and get it running?
**Answer:**  
Yes, here is a simple and idempotent playbook:
```yaml
---
- name: Install and Start Apache
  hosts: webservers
  become: yes
  tasks:
    - name: Install httpd
      yum:
        name: httpd
        state: present
    
    - name: Start and enable httpd
      service:
        name: httpd
        state: started
        enabled: yes
```

### 4. How has Ansible helped your organization? (Real-time example)
**Answer:**  
In my previous project, our team had to apply critical monthly security patches to 500+ Linux servers. Doing this manually or via messy shell scripts used to take three engineers an entire weekend, causing significant downtime. 
I introduced Ansible and wrote a patching playbook using the `yum` module and `serial` execution (to patch them in batches of 50). We reduced our patching window from 48 hours to just 2 hours, completely automated, with zero human errors.

### 5. What is Ansible Dynamic Inventory?
**Answer:**  
In modern cloud environments like AWS, IP addresses of EC2 instances change constantly due to Auto Scaling. A static inventory file (typing IPs manually) becomes useless. 
**Dynamic Inventory** uses a plugin/script to query the AWS API in real-time to fetch the exact, current IP addresses of servers based on their tags (e.g., `tag:Role=Webserver`) just before the playbook runs.

### 6. What is Ansible Tower and have you used it? If yes, why?
**Answer:**  
Ansible Tower (now AWX/Automation Controller) is the enterprise Web GUI and REST API for Ansible. Yes, I have used it. We used it because running playbooks from a laptop terminal doesn't scale for a whole company. Tower gives us visual dashboards, scheduling for recurring jobs, centralized logging, and most importantly, Role-Based Access Control (RBAC).

### 7. How do you manage the RBAC of users for Ansible Tower?
**Answer:**  
In Ansible Tower, we manage RBAC by integrating Tower with our company's Active Directory (LDAP). We create "Teams" in Tower. For example, we grant the Junior Developers team "Execute-Only" access to a specific restart playbook. They can click a button to restart servers without ever seeing the SSH keys, Vault passwords, or being able to edit the underlying code.

### 8. What is the Ansible Galaxy command and why is it used?
**Answer:**  
Ansible Galaxy (`ansible-galaxy`) is the official hub for sharing Ansible Roles. We use it so we don't have to reinvent the wheel. If my manager asks me to deploy a complex MySQL cluster, instead of writing 1,000 lines of YAML from scratch, I can run `ansible-galaxy install geerlingguy.mysql` to download a highly-tested, community-approved Role and use it immediately.

### 9. Can you explain the structure of an Ansible Playbook using Roles?
**Answer:**  
A Role breaks a massive playbook into a strict folder structure for reusability:
- **`tasks/`**: The actual modules to run (e.g., install packages).
- **`handlers/`**: Tasks that only run when notified (e.g., restart service).
- **`vars/`**: Variables specific to the role.
- **`defaults/`**: Default variables (lowest priority, easy to override).
- **`templates/`**: Jinja2 (`.j2`) dynamic config files.
- **`meta/`**: Author details and role dependencies.

### 10. What are Handlers in Ansible and why are they used?
**Answer:**  
Handlers are special tasks that **only run if they are notified** that a change occurred. They are used for Idempotency. For example, you only want to restart the Nginx web server *if* the `nginx.conf` file was actually modified. If the file didn't change, the handler is skipped, preventing unnecessary downtime.

### 11. I would like to run a specific set of tasks only on Windows VMs and not Linux VMs. Is it possible?
**Answer:**  
Yes, absolutely. We use the `when` conditional statement combined with Ansible Facts. 
You simply add `when: ansible_os_family == "Windows"` to your task. Ansible will check the OS of the target server first; if it is Linux, it will gracefully skip the task.

### 12. Does Ansible support parallel execution of tasks?
**Answer:**  
Yes. By default, Ansible runs tasks in parallel across 5 servers at a time. This is controlled by the **`forks`** parameter in the `ansible.cfg` file. If I am deploying to 100 servers and my control node has a strong CPU/Network, I can increase `forks = 50` to execute on 50 servers simultaneously, drastically speeding up the deployment.

### 13. What is the protocol that Ansible uses to connect to Windows VMs?
**Answer:**  
For Linux, Ansible uses SSH. For Windows VMs, it uses **WinRM** (Windows Remote Management) over HTTP/HTTPS.

### 14. Can you place these variable types in their Order of Precedence (lowest to highest)?
*(Playbook group_vars, Role vars, Extra vars)*
**Answer:**  
1. Playbook `group_vars` (Lowest precedence)
2. Role `vars` (Higher)
3. Extra vars passed via CLI `-e` (Highest precedence - they override everything else).

### 15. How do you handle secrets in Ansible?
**Answer:**  
I handle secrets (like database passwords or AWS keys) using **Ansible Vault**. I use `ansible-vault encrypt secrets.yml` to AES-256 encrypt the file. When executing the playbook in a CI/CD pipeline (like Jenkins), I pass a Vault password file so Ansible can decrypt the secrets in memory securely without exposing them in plaintext on GitHub.

### 16. Can we use Ansible for IaC (Infrastructure as Code)? If yes, can you compare it with Terraform?
**Answer:**  
Yes, Ansible can provision infrastructure (VPCs, EC2s) using cloud modules. However, **Terraform is much better for provisioning** because it maintains a "State File". Terraform knows exactly what resources exist and can safely destroy or update them. Ansible does not have a state file; it is primarily a Configuration Management tool. 
*Best Practice:* Use Terraform to build the empty EC2 servers, and then hand them off to Ansible to install the software inside them.

### 17. Can you talk about an Ansible playbook you wrote and how it helped your company?
**Answer:**  
*(Real-world example)*: In my previous role, adding a new worker node to our Kubernetes cluster took a DevOps engineer about 2 hours of manual work (installing Docker, configuring iptables, installing Kubeadm/Kubelet, and joining the cluster). 
I wrote an Ansible Role that automated this entire pipeline. We hooked it up to Ansible Tower. After that, whenever we needed a new node to handle traffic spikes, a junior engineer could just click a button, and the node was fully configured and joined to the cluster in exactly 4 minutes.

### 18. What do you think Ansible can improve?
**Answer:**  
1. **Speed at massive scale:** Because Ansible uses SSH, running it against 50,000+ servers simultaneously can bottleneck the control node's network. Compiled agent-based tools (like Puppet) scale slightly better at massive numbers.
2. **Debugging:** Debugging deeply nested YAML loops or complex Jinja2 dictionary filters can sometimes produce obscure, hard-to-read error messages compared to standard programming languages like Python.

---
**[Previous: Day 24 - Advanced Ansible](./Day-24-Advanced-Ansible-Mastery.md)**
