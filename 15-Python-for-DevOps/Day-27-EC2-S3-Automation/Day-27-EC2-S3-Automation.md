# Python Day 27: AWS EC2 + S3 Automation

Welcome to **Day 27**! 
Yesterday we learned the fundamentals of Boto3. Today, we put it into action by building real-world automation scripts for Amazon EC2 and S3, the bread and butter of DevOps cloud management.

---

## 1. Advanced EC2 Inventory (Extracting Data)
When you call `ec2.describe_instances()`, AWS returns a massive nested JSON response. A DevOps engineer needs to parse this to extract exactly what they need.

```python
import boto3

ec2 = boto3.client("ec2")
response = ec2.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        # Extracting safe values using .get() for optional fields
        instance_id = instance["InstanceId"]
        state = instance["State"]["Name"]
        public_ip = instance.get("PublicIpAddress", "No Public IP")
        
        # Extracting the "Name" tag
        name = "Unnamed"
        for tag in instance.get("Tags", []):
            if tag["Key"] == "Name":
                name = tag["Value"]
                
        print(f"[{state}] {name} ({instance_id}) - IP: {public_ip}")
```

---

## 2. Server-Side Filtering (The Fast Way)
If you have 1,000 instances, downloading them all to Python just to find the 5 running `dev` instances is horribly inefficient. You should **Filter on the AWS side**.

```python
response = ec2.describe_instances(
    Filters=[
        {"Name": "instance-state-name", "Values": ["running"]},
        {"Name": "tag:Environment", "Values": ["dev"]}
    ]
)
```

---

## 3. Safe State Management
Junior engineers write `ec2.start_instances(InstanceIds=["i-123"])`. 
Senior DevOps engineers **check the state first** so they don't blindly throw errors.

```python
def safe_start(instance_id):
    # 1. Get current state
    response = ec2.describe_instances(InstanceIds=[instance_id])
    state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
    
    # 2. Safely react
    if state == "stopped":
        ec2.start_instances(InstanceIds=[instance_id])
        print(f"Booting {instance_id}...")
    elif state == "running":
        print(f"{instance_id} is already running. Ignoring.")
    else:
        print(f"Cannot start {instance_id}. It is currently in state: {state}")
```

---

## 4. Automating S3 Backups
A massive DevOps use-case is zipping application logs from a server and backing them up to an S3 bucket.

```python
import os
import boto3

s3 = boto3.client("s3")
log_dir = "/var/log/application"

# Loop through a directory and upload all files
for file_name in os.listdir(log_dir):
    file_path = os.path.join(log_dir, file_name)
    
    if os.path.isfile(file_path):
        s3_key = f"backups/2026-10-15/{file_name}"
        s3.upload_file(file_path, "my-devops-backup-bucket", s3_key)
        print(f"Backed up: {file_name}")
```

---

## 5. Advanced DevOps: S3 Data Retention Policies
If you run the backup script above every day, your AWS bill will eventually explode. A Senior DevOps engineer writes a cleanup script that inspects the `LastModified` metadata of S3 objects and deletes backups older than 30 days.

```python
import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')
bucket = "my-devops-backup-bucket"
retention_days = 30
cutoff_date = datetime.now(timezone.utc) - timedelta(days=retention_days)

response = s3.list_objects_v2(Bucket=bucket, Prefix="backups/")
for obj in response.get('Contents', []):
    if obj['LastModified'] < cutoff_date:
        s3.delete_object(Bucket=bucket, Key=obj['Key'])
        print(f"Deleted old backup: {obj['Key']}")
```

---

## 6. Advanced DevOps: EC2 Bootstrapping (`UserData`)
Instead of just starting an EC2 instance, you can pass a Bash script to it when it boots up. This is called **User Data**, and it allows the instance to automatically install Docker, pull your code, and start your app without you ever SSHing into it!

```python
import boto3

ec2 = boto3.client('ec2')

# A bash script to run on boot
init_script = """#!/bin/bash
yum update -y
yum install httpd -y
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello from Automated DevOps!</h1>" > /var/www/html/index.html
"""

# You pass this script when creating/running a NEW instance via run_instances
response = ec2.run_instances(
    ImageId='ami-0abcdef1234567890', # Amazon Linux 2 AMI
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    UserData=init_script # <--- The magic happens here!
)
print("Bootstrapping new Web Server!")
```

---

## 🧑‍💻 Practice Exercises
We have created `day27_aws_infrastructure_manager.py` in this folder. 
It is a massive operational CLI tool. It features three modes: 
1. **Inventory**: Prints a beautiful table of all EC2 instances and their IP addresses.
2. **Stop-Dev**: Uses server-side filters to find running development instances, prompts the user for confirmation, and stops them safely.
3. **Backup**: Takes a local directory and uploads all files inside it to an S3 bucket!
