# Python Day 14: Remote Automation (Fabric & Boto3)

Welcome to **Day 14**! Today we bridge the gap between running Python locally and automating massive Cloud environments.

We will cover the two most important Python libraries in a DevOps engineer's toolkit:
1. **Fabric**: For Remote Server Execution (SSH)
2. **Boto3**: For Cloud API Automation (AWS)

---

## 1. Fabric (Remote Server Automation)
Normally, if you want to install software on 10 servers, you must SSH into each one manually. **Fabric** is a Python library that automates SSH connections and command execution!

### The Concept
Instead of: `ssh admin@10.0.0.5 -> run command`
We use Fabric to write a Python script that connects to 100 servers simultaneously and runs the command automatically.

### Basic Fabric Syntax
*(Requires running `pip install fabric`)*
```python
from fabric import Connection

# 1. Establish the SSH connection
c = Connection("admin@10.0.0.5")

# 2. Run standard commands
c.run("mkdir -p /home/admin/app")

# 3. Advanced DevOps: Running as Root (sudo)
# In the real world, restarting services requires root privileges!
c.sudo("systemctl restart nginx")
```

---

## 2. Boto3 (AWS Automation)
Fabric talks to *Operating Systems* (Linux). **Boto3** talks to the *AWS Cloud* (APIs).

If you want to create an EC2 instance, you don't SSH into anything. You use Boto3 to send an API request to AWS asking it to spin up a server.

### Basic Boto3 Syntax
*(Requires running `pip install boto3` and configuring `aws configure`)*
```python
import boto3

# Create a client to talk to the S3 storage service
s3 = boto3.client('s3')

# Create a client to talk to EC2 Virtual Servers
ec2 = boto3.client('ec2')
```

### Advanced DevOps: AWS Credential Security
**NEVER** hardcode your AWS Access Keys directly into your Python script! Boto3 is smart—if you don't provide keys, it will automatically look for them securely in your Environment Variables or in the `~/.aws/credentials` file created by the AWS CLI.

### Advanced DevOps: Boto3 Pagination
If you ask AWS to list your EC2 instances, it will only return a maximum of 1,000 instances to save bandwidth. If you have 2,000 servers, your script will miss half of them! Senior engineers use **Paginators** to loop through *all* pages of results safely.

```python
import boto3
client = boto3.client('s3')
paginator = client.get_paginator('list_objects_v2')

# This loops through ALL pages, even if there are millions of files!
for page in paginator.paginate(Bucket='my-massive-devops-bucket'):
    for obj in page['Contents']:
        print(obj['Key'])
```

---

## 3. Fabric vs Boto3 (Interview Question!)
You will absolutely be asked this in an interview. Know the difference:

| Library | Target | Action | Example Use Case |
| :--- | :--- | :--- | :--- |
| **Fabric** | Operating Systems (Linux) | Executes shell commands over SSH | "Install Nginx and restart the systemd service on `server-01`" |
| **Boto3** | AWS Cloud Infrastructure | Interacts with AWS APIs | "Provision 5 new EC2 instances and create an S3 bucket" |

---

## 4. The Ultimate DevOps Deployment Architecture
In real-world DevOps, Fabric and Boto3 work together.

Imagine you are pushing an application to production:
1. **Boto3** asks AWS for the IP addresses of all currently running EC2 instances.
2. The Python script loops through those IP addresses.
3. **Fabric** connects to each IP address.
4. **Fabric** runs `git pull` and `systemctl restart app`.

### The Flow
```text
Python Automation Script
       │
       ├─> [Boto3] -> "Hey AWS, give me the IPs of our Web Servers."
       │
       └─> [Fabric] -> "Connect to those IPs and install the app!"
```

---

## 🧑‍💻 Project 3: The Deployment Skeleton
We have created a conceptual deployment script in this folder: `day14_boto3_fabric_demo.py`. 

Because you would need active AWS credentials and SSH keys to run this, it serves as an architectural template. Read through the code to understand exactly how a Senior DevOps engineer combines Cloud APIs with Remote Command Execution!
