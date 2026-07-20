# Day 6: Connecting to EC2, AWS CLI, & Infrastructure as Code (IaC)

In Day 5, we launched an EC2 instance. Today, we will learn how to connect to it securely, how to fix common connection errors, and how to manage AWS resources using the AWS CLI and Automation tools.

---

## 1. Connecting to an EC2 Instance

There are three common ways to connect to your EC2 virtual machine:

### Method 1: AWS Instance Connect (Browser)
You log into the AWS Console, select your instance, and click "Connect". AWS opens a terminal directly in your web browser.
- *Pros:* Very easy for beginners.
- *Cons:* Rarely used in real companies because it is not easily scriptable or automated.

### Method 2: Terminal SSH (Mac / Linux)
The industry standard. You open your terminal and connect using your Private Key (`.pem` file).
```bash
ssh -i ~/Downloads/my-key.pem ubuntu@54.210.xxx.xxx
```

**Crucial Error: "WARNING: UNPROTECTED PRIVATE KEY FILE!"**
If you try to run the SSH command and see this error, it means your `.pem` file is too exposed. SSH refuses to use an insecure key that other users on your laptop can read.
- **The Fix:** You must change the file permissions so that *only* you (the owner) can read the key.
```bash
chmod 600 ~/Downloads/my-key.pem
```
*(After running `chmod 600`, run the SSH command again and it will connect successfully).*

### Method 3: MobaXterm or PuTTY (Windows)
Since native Windows Command Prompt historically didn't handle SSH keys well, DevOps engineers on Windows use tools like **MobaXterm**.
- Open MobaXterm ➔ SSH Session ➔ Enter Public IP ➔ Username: `ubuntu` ➔ Advanced SSH Settings ➔ Upload Private Key ➔ Connect.

---

## 2. Deleting an EC2 Instance
When you are done practicing, you must delete your EC2 instance so AWS stops charging you.
- Go to EC2 Dashboard ➔ Select Instance ➔ Click **Instance State** ➔ Select **Terminate Instance**.
- *Note:* Terminating is permanent. The instance and its Root Volume are destroyed forever.

---

## 3. What is the AWS CLI?

The **AWS CLI (Command Line Interface)** is a tool you download to your laptop that allows you to manage your entire AWS account using terminal commands instead of clicking buttons in the web browser.

*Why do we need it?*
If your manager asks you to list all 500 S3 buckets in your account, clicking through the AWS website and counting them is impossible. With the CLI, you just type:
```bash
aws s3 ls
```

### Authenticating the AWS CLI (`aws configure`)
Before you can run commands, AWS needs to know who you are. You must create an **Access Key** and a **Secret Access Key** in the AWS Console (under IAM Security Credentials).

Run this command in your terminal:
```bash
aws configure
```
It will ask for 4 things:
1. **AWS Access Key ID:** (Paste your Access Key)
2. **AWS Secret Access Key:** (Paste your Secret Key)
3. **Default region name:** `us-east-1`
4. **Default output format:** `json`

**Where are these keys saved?**
When you run `aws configure`, AWS CLI creates two hidden files on your computer:
- `~/.aws/credentials` (Stores your Access Key and Secret Key)
- `~/.aws/config` (Stores your default Region and Output format)

**Managing Multiple AWS Accounts (Profiles):**
If you work at a company with multiple AWS accounts (e.g., a "Dev" account and a "Prod" account), you cannot just use `aws configure` because it overwrites your default keys. Instead, you use **Named Profiles**:
```bash
aws configure --profile prod-account
```
Then, to run a command against that specific account, you simply add the `--profile` flag:
```bash
aws s3 ls --profile prod-account
```

**⚠️ SECURITY WARNING:** Never share your Secret Access Key. Do not commit it to GitHub. If a hacker finds it, they can spin up thousands of servers in your account and cost you millions of dollars.

### The Golden Rule: IAM Roles vs Hardcoded Keys
If you want to run AWS CLI commands from your *local laptop*, you use `aws configure` and enter your Access Keys. 
However, if you want your **EC2 instance** to run AWS CLI commands (e.g., a backend script on the server that downloads files from S3), you should **NEVER** run `aws configure` on the server. If someone hacks the server, they steal your keys.
- **The Solution:** You create an **IAM Role** with S3 permissions and attach that role directly to the EC2 instance. The EC2 instance will magically have permission to use the AWS CLI without ever needing hardcoded Access Keys.

---

## 4. Introduction to Infrastructure as Code (IaC)

Using the AWS CLI is faster than the browser, but if you want to deploy complex architectures (like 5 servers, a database, and a load balancer), typing individual CLI commands is still too slow. 

Instead, DevOps engineers use **Infrastructure as Code (IaC)**.
IaC allows you to write a configuration file (in YAML or JSON) describing the infrastructure you want, and an automation tool builds it for you perfectly every time.

### Popular Automation Tools
1. **AWS CloudFormation:** AWS's native IaC tool. You write a YAML file, upload it to CloudFormation, and AWS creates the EC2 instances, S3 buckets, and VPCs automatically.
2. **Terraform:** The most popular open-source IaC tool in the world. Unlike CloudFormation (which only works on AWS), Terraform works on AWS, Azure, and Google Cloud.
3. **Boto3 (Python SDK):** A library that allows Python developers to write scripts that talk directly to the AWS API. You can write a Python script that says `ec2.create_instances(...)` to spin up servers programmatically.

---

## 🎯 Day 6 Summary
To be a DevOps engineer, you must move away from clicking buttons. You connect to servers via **SSH**, you manage your cloud resources using the **AWS CLI**, and you build massive architectures by writing **Infrastructure as Code** with tools like **Terraform** or **CloudFormation**.


---
**[⬅️ Previous: Day 5 - AWS EC2 Foundations](./Day-05-AWS-EC2-Basics.md)** | **[➡️ Next: Day 7 - Linux Basics](../02-Linux/Day-07-Linux-Basics.md)**
