# Day-11: AWS CLI Deep Dive

## Introduction

So far, we have done everything using the AWS Management Console (UI). While the UI is great for learning and visual exploration, it is **not automation-friendly**.

In modern DevOps practices, infrastructure management needs to be automated, repeatable, and scalable. AWS provides an API (Application Programming Interface) that allows you to send requests programmatically using shell scripts, Python, or other programming languages.

To interact with the AWS API, we use tools like:
1.  **AWS CLI (Command Line Interface)**
2.  **Terraform** (Infrastructure as Code)
3.  **AWS CloudFormation** (Infrastructure as Code)
4.  **AWS CDK (Cloud Development Kit)**

The **AWS CLI** is a unified tool (built using Python) to manage your AWS services. With just one tool to download and configure, you can control multiple AWS services from the command line and automate them through scripts.

---

## AWS CLI vs. Infrastructure as Code (IaC)

*   **When to use AWS CLI:**
    *   Quick administrative tasks (e.g., creating a quick test bucket, listing instances).
    *   Simple scripting or cron jobs (e.g., taking daily snapshots).
    *   Troubleshooting and exploring APIs.
*   **When to use IaC (Terraform / CloudFormation):**
    *   Provisioning complete environments (VPC, Subnets, EC2, RDS together).
    *   Managing infrastructure state.
    *   Version-controlling your infrastructure.
    *   Complex, multi-resource deployments.

---

## 1. Installation

The AWS CLI is available for Windows, macOS, and Linux.

1.  Go to a search engine and search for "AWS CLI install".
2.  Navigate to the official AWS documentation: **[Installing or updating the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)**.
3.  Select your Operating System (Windows, Linux, or macOS).
4.  Copy the provided commands or download the installer and run it.

*Note: The AWS CLI requires Python to be installed on your machine.*

### Verify Installation
Once installed, open your terminal (Command Prompt, PowerShell, or Bash) and run:
```bash
aws --version
```
You should see output similar to `aws-cli/2.x.x Python/3.x.x Windows/10...`.

---

## 2. Configuration (`aws configure`)

To use the CLI, it needs to know *who* you are (Authentication) and *where* to create resources (Region). 

1.  Go to the **AWS Management Console**.
2.  Click on your username in the top right corner and go to **Security Credentials**.
3.  Scroll down to **Access keys** and click **Create access key**.
4.  Download or copy the **Access Key ID** and **Secret Access Key**. *(Keep these safe! Do not share them or commit them to GitHub).*

In your terminal, run:
```bash
aws configure
```

It will prompt you for four pieces of information:
*   **AWS Access Key ID:** (Paste your Key ID here)
*   **AWS Secret Access Key:** (Paste your Secret Key here)
*   **Default region name:** (e.g., `us-east-1`, `ap-south-1`)
*   **Default output format:** (Choose `json`, `text`, or `table`. `json` is standard)

This creates a hidden `.aws` folder in your home directory containing your credentials.

### Verify Configuration
To check if the AWS CLI is configured correctly, run a simple command to list your S3 buckets. If it is configured correctly, it will either list your buckets or return nothing without any errors.

```bash
aws s3 ls
```

*Example Output:*
```text
2026-08-17 12:31:52 app-1-payments-prod-siva.com
```

---

## 3. Basic Usage & Common Commands

The general syntax for the AWS CLI is:
`aws <command> <subcommand> [options and parameters]`

### A. S3 (Simple Storage Service) Commands

**1. List all S3 buckets:**
```bash
aws s3 ls
```

**2. Create a new S3 bucket:**
*(Bucket names must be globally unique!)*
```bash
aws s3 mb s3://my-unique-demo-bucket-name-12345
```

**3. Copy a file from your local machine to S3:**
```bash
aws s3 cp my-local-file.txt s3://my-unique-demo-bucket-name-12345/
```

**4. List contents of a bucket:**
```bash
aws s3 ls s3://my-unique-demo-bucket-name-12345
```

**5. Delete a bucket:**
*(The bucket must be empty first)*
```bash
aws s3 rb s3://my-unique-demo-bucket-name-12345 --force
```

### B. EC2 (Elastic Compute Cloud) Commands

**1. Describe (List) EC2 Instances:**
```bash
aws ec2 describe-instances
```
*(Tip: Use `--query` or output formatting if the JSON output is too large).*

**2. Create (Launch) an EC2 Instance:**
*(You will need an AMI ID, Instance Type, Key Name, and Subnet ID from your account)*
```bash
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --count 1 \
    --instance-type t2.micro \
    --key-name MyKeyPair \
    --subnet-id subnet-12345678 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyCliInstance}]'
```

**3. Start an Instance:**
```bash
aws ec2 start-instances --instance-ids i-1234567890abcdef0
```

**4. Stop an Instance:**
```bash
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
```

**5. Terminate an Instance:**
```bash
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

---

## 4. How to Read AWS CLI Documentation

The AWS CLI is massive. You cannot memorize every command. The most important skill is knowing how to find the right command.

### Method 1: Using the built-in help
You can append `help` to any AWS CLI command to see the manual directly in your terminal.
*   Get help for the main CLI: `aws help`
*   Get help for a specific service: `aws ec2 help`
*   Get help for a specific subcommand: `aws ec2 run-instances help`

### Method 2: Official Online Documentation
1.  Search Google for: `aws cli <service_name> <action>` (e.g., `aws cli s3 create bucket`).
2.  Click the official `docs.aws.amazon.com` link.
3.  **Read the Synopsis:** This shows the required and optional parameters.
4.  **Look for Examples:** Scroll down to the bottom of the documentation page. AWS almost always provides excellent, copy-pasteable examples for common use cases.
5.  **Understand the Output:** The documentation will explain what JSON output to expect when the command succeeds.

Mastering the documentation will make you an expert in the AWS CLI without needing to memorize everything!
