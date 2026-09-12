# Python Day 26: Boto3 Fundamentals (AWS Automation)

Welcome to **Day 26**! 
Today, we bridge the gap between Python and Cloud Infrastructure. **Boto3** is the official AWS SDK for Python. It allows your Python scripts to control EC2, S3, IAM, VPCs, and every other AWS service via code.

---

## 1. Authentication (The Golden Rule)
Before Boto3 can talk to AWS, it must know *who* you are.

> [!CAUTION]
> **NEVER HARDCODE AWS CREDENTIALS IN YOUR PYTHON SCRIPT!**
> Do not put `aws_access_key_id="AKIA..."` in your code. If it leaks to GitHub, attackers will spin up thousands of servers in minutes.

**How Boto3 finds credentials:**
1. Environment Variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
2. Local AWS CLI Config (`~/.aws/credentials` created by `aws configure`)
3. IAM Roles attached to EC2 instances/Lambda functions (The DevOps Production Standard)

---

## 2. Client vs Resource
Boto3 has two ways to interact with AWS. You should know the difference for interviews.

- **Client (`boto3.client('ec2')`)**: A low-level interface. It closely maps 1-to-1 with the raw AWS REST API. It returns raw JSON dictionaries. (Used broadly across all AWS).
- **Resource (`boto3.resource('ec2')`)**: A higher-level, object-oriented abstraction. It returns Python objects (like an `Instance` object) rather than JSON dictionaries.

---

## 3. S3 Automation Basics

```python
import boto3

# 1. Create a client
s3 = boto3.client("s3")

# 2. Upload an artifact (e.g. from a Jenkins Build)
s3.upload_file("local_app.zip", "my-bucket", "releases/v1/app.zip")

# 3. Download a file
s3.download_file("my-bucket", "releases/v1/app.zip", "downloaded_app.zip")
```

---

## 4. EC2 Automation Basics

```python
import boto3

ec2 = boto3.client("ec2", region_name="us-east-1")

# List Instances (Returns a deeply nested dictionary)
response = ec2.describe_instances()
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        print(f"ID: {instance['InstanceId']} | State: {instance['State']['Name']}")

# State Management
ec2.stop_instances(InstanceIds=["i-1234567890abcdef0"])
ec2.start_instances(InstanceIds=["i-1234567890abcdef0"])
```

---

## 5. Advanced DevOps: Paginators
If you have 10,000 files in S3, AWS will not return them all at once. They return "pages". Instead of manually writing loops to check for `NextToken`, Boto3 provides **Paginators**.

```python
s3 = boto3.client("s3")
paginator = s3.get_paginator("list_objects_v2")

# Automatically handles fetching page after page
for page in paginator.paginate(Bucket="my-massive-bucket"):
    for obj in page.get("Contents", []):
        print(obj["Key"])
```

---

## 6. Advanced DevOps: Waiters
If you tell AWS to start an EC2 instance, the API immediately returns `Success`. However, the server takes 2 minutes to actually boot up.
Instead of using `time.sleep(120)`, Boto3 provides **Waiters** which intelligently poll the AWS API until the resource reaches the desired state!

```python
ec2 = boto3.client("ec2")
ec2.start_instances(InstanceIds=["i-12345"])

# Create a waiter
waiter = ec2.get_waiter("instance_running")

print("Waiting for instance to boot...")
waiter.wait(InstanceIds=["i-12345"]) # Script pauses here until fully running!
print("Instance is fully booted and ready!")
```

---

## 7. Advanced DevOps: Error Handling
Never use a bare `try/except`. Catch specific AWS `ClientError` or `NoCredentialsError`.

```python
from botocore.exceptions import ClientError, NoCredentialsError

try:
    s3 = boto3.client("s3")
    s3.list_buckets()
except NoCredentialsError:
    print("FATAL: No AWS Credentials found in environment or ~/.aws/credentials")
except ClientError as e:
    print(f"AWS API Error: {e}")
```

---

## 8. Advanced DevOps: Multi-Account Management (`boto3.Session`)
DevOps engineers never use just one AWS account. You usually have a `Dev`, `Staging`, and `Prod` account configured in your `~/.aws/credentials` file under different profiles (e.g., `[dev]`, `[prod]`).

To force a script to run against a specific account, you create a **Session** instead of using the default client.

```python
import boto3

# Connects to the AWS account configured under the [prod] profile in ~/.aws/credentials
prod_session = boto3.Session(profile_name="prod", region_name="us-east-1")

# Create the EC2 client using that specific session
prod_ec2 = prod_session.client("ec2")
prod_ec2.stop_instances(InstanceIds=["i-12345"])
```

---

## 9. Advanced DevOps: Secure S3 Sharing (`generate_presigned_url`)
If a developer asks you for a massive log file stored in S3, you **should not** make the S3 bucket public! 
Instead, Boto3 can generate a **Presigned URL**. This gives the developer a secure, temporary link that automatically expires after a set time (e.g., 1 hour).

```python
import boto3

s3 = boto3.client('s3')

# Generate a URL that allows downloading the object, expiring in 3600 seconds (1 hour)
url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={'Bucket': 'my-secure-bucket', 'Key': 'logs/crash-report.zip'},
    ExpiresIn=3600
)

print(f"Send this secure link to the developer: {url}")
```

---

## 🧑‍💻 Practice Exercises
We have created `day26_aws_boto3_automation.py` in this folder. 
It contains a complete, robust DevOps script that implements Boto3 Paginators, Waiters, and robust Error Handling to automate EC2 inventory management and S3 artifact uploading!
