# Day 5: AWS EC2 Foundations - Interview Questions

These questions test your practical knowledge of launching and securing cloud servers in AWS.

---

### Q1: What is an AMI (Amazon Machine Image)?
**Interview Answer:**  
"An AMI is a pre-configured template or blueprint used to launch an EC2 instance. It contains the Operating System (like Ubuntu or Amazon Linux), the boot instructions, and any pre-installed software required. You can use AWS-provided AMIs or create custom AMIs for your company so that every new server spins up with your specific software already installed."

---

### Q2: What is the difference between an AWS Region and an Availability Zone?
**Interview Answer:**  
"An AWS Region is a broad geographical location, like Mumbai or Virginia. An Availability Zone (AZ) is a specific, isolated physical data center *within* that Region. We deploy applications across multiple AZs within a Region so that if one physical data center loses power, the application stays online via the other AZs."

---

### Q3: What is an EC2 Instance Type?
**Interview Answer:**  
"An instance type determines the hardware capacity of the virtual machine, specifically the ratio of vCPUs to RAM, as well as storage and network performance. For example, a `t2.micro` is good for testing, while an `m5` or `c5` instance is optimized for heavy, production-level compute workloads."

---

### Q4: What is a Security Group in AWS?
**Interview Answer:**  
"A Security Group acts as a stateful, virtual firewall at the instance level. It controls inbound and outbound traffic by evaluating specific rules. For example, if I am launching a web server, I must configure the Security Group to allow inbound HTTP traffic on Port 80, and SSH traffic on Port 22 so I can manage the server remotely."

---

### Q5: How does AWS authenticate you when you SSH into an EC2 instance?
**Interview Answer:**  
"AWS highly discourages password authentication due to security risks. Instead, it uses an SSH Key Pair. During instance creation, AWS injects a Public Key into the server. I download the corresponding Private Key (`.pem` file) to my local machine. When I attempt to SSH into the server, the SSH client uses my private key to cryptographically prove my identity to the server."

---

### Q6: If an interviewer asks you to describe how to launch an EC2 instance, how do you respond?
**Interview Answer:**  
"To launch an EC2 instance, I first select the AWS Region and an Availability Zone. Next, I choose the appropriate AMI for my Operating System, followed by an Instance Type that matches my CPU and RAM requirements. Then, I assign or create a Key Pair for secure SSH access. Finally, I configure the Security Group to allow necessary inbound traffic—like SSH on Port 22—and launch the instance. Once it's running, I use the assigned Public IP and my private key to connect remotely."

---

### Q7: What happens to a default Public IP when you stop and start an EC2 instance, and how do you prevent it?
**Interview Answer:**  
"By default, an EC2 instance is assigned a dynamic Public IP. If you stop and start the instance, that Public IP is released back to the AWS pool and your instance receives a completely new one. To prevent this, you must allocate an Elastic IP (EIP)—which is a static, persistent IPv4 address—and associate it with your instance so the IP remains constant across reboots."

---

### Q8: What is EC2 User Data and what is it used for?
**Interview Answer:**  
"EC2 User Data is a feature that allows you to pass a script to an instance at launch. When the instance boots up for the very first time, it automatically executes this script as the root user. As a DevOps engineer, I use User Data to 'bootstrap' servers—for example, automatically installing web servers, downloading application code, and starting services without ever needing to manually SSH into the machine."

---

### Q9: What is an EBS Volume, and what happens to the Root Volume when an EC2 instance is terminated?
**Interview Answer:**  
"An EBS (Elastic Block Store) volume is the persistent virtual hard drive attached to an EC2 instance. The specific volume where the Operating System is installed is called the Root Volume. A critical thing to remember is that by default, when you terminate an EC2 instance, the Root Volume is automatically deleted along with it. To prevent data loss, you must either back it up using EBS Snapshots or explicitly disable the 'Delete on Termination' attribute before deleting the server."


---
**[⬅️ Previous: Day 4 - OS & Virtualization Questions](./Day-04-Virtualization-Questions.md)** | **[➡️ Next: Day 6 - AWS CLI Questions](./Day-06-AWS-CLI-Questions.md)**
