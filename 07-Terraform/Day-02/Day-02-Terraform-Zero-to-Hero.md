# Day 02: Terraform Zero to Hero (Hands-On: Provisioning Your First EC2 Instance)

Today we transition from theory to practice. We will install Terraform, configure our AWS credentials, and write our first script to deploy an EC2 instance completely through code.

---

## 1. The Scenario: Why Infrastructure as Code?

Imagine you are a DevOps engineer and you are asked to create an S3 bucket. Doing this manually via the AWS Console takes about 2 minutes. 
But what if the request changes, and you now need to create **100 S3 buckets** for different client environments? Doing this manually is prone to human error and takes hours.

With **Infrastructure as Code (IaC)**, you write a script once, and can programmatically create 100 S3 buckets in seconds via API calls. Note that IaC isn't restricted to one format; infrastructure templates can be written in JSON, YAML, or any compatible scripting language depending on the tool you choose.

While AWS provides **CloudFormation (CFT)**, Azure provides **Azure Resource Manager (ARM)**, and OpenStack uses **Heat Templates**, learning all these proprietary tools is nearly impossible. 
Instead, we use **Terraform**, developed by HashiCorp. It uses **HCL (HashiCorp Configuration Language)** to let you define infrastructure for *any* cloud provider.

---

## 2. Environment Setup

### Install Terraform
To install Terraform on your machine, always refer to the official [HashiCorp Installation Documentation](https://developer.hashicorp.com/terraform/install).
Select your operating system (Windows, Mac, Linux) and copy/paste the provided commands into your terminal.

### Configure AWS Credentials
Terraform needs permission to build things in your AWS account. As a security best practice, never use your root account!
1. Log into AWS and go to **IAM**.
2. Create a new IAM User with `AdministratorAccess` (or specific EC2 access).
3. Generate an **Access Key** and **Secret Access Key**.

Now, open your terminal and configure the AWS CLI so Terraform can use those credentials:
```bash
aws configure
```
- **AWS Access Key ID:** Paste your key
- **AWS Secret Access Key:** Paste your secret key
- **Default region name:** `us-east-1`
- **Default output format:** `json`

### VS Code Extensions
For the best experience, open VS Code, go to the Extensions marketplace, and install:
- **HashiCorp Terraform**
- **HashiCorp HCL**

*(This gives you syntax highlighting, error checking, and autocompletion!)*

---

## 3. Project: Creating an EC2 Instance with Terraform

Create a new directory for your project and open it in VS Code. Create a file named `main.tf`.

**`main.tf`:**
```hcl
provider "aws" {
    region = "us-east-1"    # Set your desired AWS region
}

resource "aws_instance" "example" {
    ami           = "ami-0c55b159cbfafe1f0"  # Note: AMI IDs change regularly. Check AWS for a current Ubuntu AMI!
    instance_type = "t2.micro"
    subnet_id     = "subnet-019ca91cdenfknfk" # Replace with your actual Subnet ID
    key_name      = "aws_login"              # Replace with your actual Key Pair name
}
```
*Tip: If you ever need to figure out how to write these scripts, just Google "Terraform AWS EC2" and the official documentation will give you exact examples.*

---

## 4. The Core Terraform Workflow

Once your script is written, you execute it using four core commands. Open your terminal in the directory where `main.tf` is located:

### 1. Initialize
```bash
terraform init
```
This is the first command you must run. It reads your script, sees that you are using AWS, and downloads the necessary AWS plugins/providers so Terraform can talk to the AWS API.

### 2. Dry Run
```bash
terraform plan
```
This acts as a "dry run." It checks your code and outputs a plan of exactly what it *will* do (e.g., "I will create 1 EC2 instance"). It does not actually build anything yet, giving you a chance to catch mistakes.

### 3. Deploy
```bash
terraform apply
```
This actually provisions the infrastructure. It will show you the plan again and ask for confirmation. Type `yes`.
*(If there are cloud-side errors—like an invalid Subnet ID—it will fail here. You must use your cloud knowledge to fix it).*

### 4. Teardown
```bash
terraform destroy
```
When you are done practicing, run this to completely delete all the infrastructure you just created so AWS stops charging you!

---

## 5. What is the State File? (`terraform.tfstate`)

After you run `terraform apply`, type `ls` in your terminal. You will notice a new file has appeared: `terraform.tfstate`.

```bash
cat terraform.tfstate
```
**This file is critically important.** It is essentially a database where Terraform records exactly what it just built. 
When you run `terraform destroy` or modify your script, Terraform looks at this `tfstate` file to compare what exists in the real world versus what is written in your code. 

---
**[Previous: Day 01 - Intro to Terraform](../Day-01/Day-01-Introduction-to-Terraform.md)** | **[Next: Day 03 - Terraform Providers & Variables](../Day-03/Day-03-Terraform-Providers-and-Variables.md)**
