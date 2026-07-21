# Day 5: AWS EC2 Foundations & VM Automation

Welcome to Day 5! In the last class, we learned what a Virtual Machine is. Today, we learn how to actually create them in the cloud (AWS) and how DevOps engineers automate this process.

---

## 1. Manual vs Automated VM Creation

**Manual Creation (For Beginners):**
You log into the AWS Management Console (the website), click "Launch Instance", fill out the forms, and click Create. 
- *Problem:* If your manager asks for 100 Virtual Machines, you cannot click "Launch" 100 times. It's too slow and error-prone.

**Automated Creation (For DevOps Engineers):**
DevOps is all about efficiency through automation. Instead of clicking buttons, we write code (scripts) to interact with the **AWS API**. 
- Your Script âž” AWS API âž” AWS Creates 100 VMs instantly.

### Popular Automation Tools
DevOps engineers use various tools to talk to the AWS API:
- **AWS CLI:** Running commands directly from the terminal (e.g., `aws ec2 run-instances`).
- **AWS SDK (Boto3):** Writing Python scripts to manage AWS resources.
- **Terraform:** The industry-standard tool for Infrastructure as Code (IaC). It works across AWS, Azure, and Google Cloud.
- **AWS CloudFormation / AWS CDK:** AWS-native tools for writing infrastructure as code.

---

## 2. What Happens When You Request a VM?

When you or your script requests a VM, AWS performs three security checks before building it:
1. **Authentication:** *Who are you?* (Checks if you are logged in with valid credentials).
2. **Authorization:** *Are you allowed to do this?* (Checks IAM permissions to see if you are allowed to create EC2 instances).
3. **Validation:** *Is your request valid?* (Checks if the region, OS, and instance type you requested actually exist).

If all checks pass, AWS provisions the VM.

---

## 3. Core AWS EC2 Concepts

If you are creating an EC2 instance (Virtual Machine) in AWS, you must define 6 core components:

### 1. AMI (Amazon Machine Image)
An AMI is the blueprint for your server. It tells AWS which Operating System (Ubuntu, Windows, Amazon Linux) and what pre-installed software you want on your VM.
- *Analogy:* Like choosing the architectural blueprint before building a house.

### 2. EC2 Instance Type
This defines the physical hardware power of your VM (vCPUs and RAM).
- **t2.micro:** 1 vCPU, 1GB RAM (Free-tier, for learning).
- **m5.large:** High CPU and RAM (For enterprise production).

### 3. AWS Region
The geographical location of the massive AWS data center where your server will live.
- Examples: `ap-south-1` (Mumbai), `us-east-1` (Virginia). 
- *Rule:* Always choose a region closest to your customers to reduce network latency.

### 4. Availability Zone (AZ)
An isolated data center *within* a Region. 
- The Mumbai Region has multiple AZs (e.g., `ap-south-1a`, `ap-south-1b`). If one data center catches fire, the others in the same region stay online, ensuring high availability.

### 5. Security Group
A virtual firewall attached to your EC2 instance. It controls exactly who can enter and exit your server using network rules.
- To connect to your Linux server remotely, you **must** allow **SSH on Port 22** in your Security Group. If you don't, you will be blocked.

### 6. Key Pair (Public & Private Key)
Instead of passwords, AWS uses SSH Key Pairs to log in securely.
- **Public Key:** AWS puts this lock on your EC2 instance.
- **Private Key (`.pem` file):** You download this file to your laptop. It acts as the physical key. Never share this with anyone!

### 7. Public IP vs Elastic IP (Crucial Gotcha)
By default, the Public IP assigned to your EC2 instance is **Dynamic**. If you stop and restart your server, AWS will take back the IP and give you a *completely new* Public IP address. 
- To prevent this, you must allocate an **Elastic IP (EIP)**. An Elastic IP is a **Static** IPv4 address that never changes, ensuring your server's address remains constant even if it is stopped and restarted.

### 8. EC2 User Data (Bootstrapping)
**User Data** is a feature that allows you to pass a shell script to your EC2 instance when you launch it. As soon as the virtual machine boots up for the very first time, it automatically runs this script.
- *Why is this useful?* Instead of SSHing into the server to manually install software (like Nginx, Docker, or Java), you can put the installation commands in the User Data. The server will configure itself automatically upon boot. This process is known as **bootstrapping**.

### 9. EBS Volumes (Elastic Block Store)
When you buy a laptop, it comes with an internal hard drive. When you launch an EC2 instance, AWS attaches a virtual hard drive called an **EBS Volume** (Elastic Block Store).
- The drive that contains the Operating System is called the **Root Volume**.
- **Crucial Gotcha:** By default, when you terminate (delete) an EC2 instance, its Root Volume is completely destroyed. Always back up important data or change the default setting to retain the volume!

---

## 4. How to Connect to Your EC2 Instance (Windows)

Once you launch your Ubuntu EC2 instance in AWS, you need to log into it from your Windows laptop using SSH.

1. **Get the IP:** Go to the AWS Console and copy your EC2 instance's **Public IPv4 Address**.
2. **Download MobaXterm:** Since the default Windows command prompt isn't always great for SSH, download and install *MobaXterm Home Edition*.
3. **Start SSH Session:** Open MobaXterm âž” Session âž” SSH.
4. **Enter Details:**
   - **Remote Host:** Paste the Public IP (e.g., `54.xxx.xxx.xxx`).
   - **Username:** Type `ubuntu`.
5. **Use the Private Key:** Click Advanced SSH Settings âž” Check "Use private key" âž” Upload the `.pem` file you downloaded when creating the instance.
6. **Connect:** Click OK. You are now inside your remote AWS server!

---

## 🎯 Day 5 Summary
You have now bridged the gap between basic virtualization and actual Cloud Computing. 
Workflow: **AWS Console âž” Choose Region & AZ âž” Choose AMI (Ubuntu) âž” Choose Instance Type (t2.micro) âž” Create Key Pair âž” Configure Security Group (Open Port 22) âž” Launch EC2 âž” Connect via SSH (MobaXterm).**

---
**[➡️ Next: Day 6 - AWS CLI & IaC](./Day-06-AWS-CLI-and-IaC.md)**

