# Day-25: AWS Real-Time Project with Terraform

Welcome to Day 25! Today, we are putting everything together to build a **Real-Time AWS Infrastructure Project** entirely via code using **Terraform**. 

By the end of this project, you will have written the Infrastructure as Code (IaC) to deploy a Virtual Private Cloud (VPC), Subnets, Security Groups, an S3 Bucket, multiple EC2 web servers, and an Application Load Balancer (ALB) to distribute traffic between them!

---

## 1. Prerequisites: IAM and AWS CLI Setup

Before Terraform can create resources in your AWS account, it needs permission to talk to the AWS API.

### Step 1: Create an IAM User
1. Go to the AWS Management Console $\rightarrow$ **IAM**.
2. Create a new user (e.g., `terraform-admin`).
3. Attach policies with proper authorization (e.g., `AdministratorAccess` for this learning lab).
4. Go to the user's **Security credentials** tab and create an **Access Key** and **Secret Access Key**. *Keep these safe!*

### Step 2: Configure the AWS CLI
Open your local terminal (Linux/Mac/Windows) and ensure the AWS CLI is installed.
Run the following command:
```bash
aws configure
```
It will prompt you for four pieces of information:
* **AWS Access Key ID:** Paste your Access Key.
* **AWS Secret Access Key:** Paste your Secret Key.
* **Default region name:** e.g., `us-east-1`
* **Default output format:** `json`

Now, your local machine (and Terraform) is securely authenticated with your AWS account!

---

## 2. Setting up the Project Workspace

Let's create an organized workspace for our project and open it in VS Code.

```bash
cd projects
mkdir terraformaws
mkdir terraformpro
cd terraformpro
code .  # This opens the folder in VS Code
```

> [!TIP]
> Install the **HashiCorp Terraform** extension in VS Code. It provides syntax highlighting, formatting, and auto-completion to make writing scripts much easier!

---

## 3. Understanding the Code (Line by Line)

We are going to create a modular Terraform structure. All of the code files can be found in the `day-25-terraform-project` folder in this repository. Let's break them down.

### A. The Provider (`provider.tf`)
Terraform needs to know *which* cloud provider it is talking to (AWS, Azure, GCP).
* **`required_providers`**: Tells Terraform to download the official HashiCorp AWS plugin (version 5.11.0).
* **`provider "aws"`**: Configures the region (`us-east-1`) where our resources will be built.

### B. The Variables (`variables.tf`)
Hardcoding values is a bad practice. We use variables to make our code reusable.
* We define a variable called `cidr` with a default value of `10.0.0.0/16`. We will call this variable in our main code using `var.cidr`.

### C. The Main Infrastructure (`main.tf`)
This is the heart of our project. Let's understand exactly what resources we are creating:

1. **VPC (`aws_vpc`)**: Creates our private network using the CIDR block from our variables.
2. **Subnets (`aws_subnet`)**: We create two public subnets (`sub1` and `sub2`) in two different Availability Zones (`us-east-1a` and `us-east-1b`) for high availability. We set `map_public_ip_on_launch = true` so our servers get public IPs.
3. **Internet Gateway (`aws_internet_gateway`)**: Attaches to the VPC to allow our network to connect to the outside internet.
4. **Route Table (`aws_route_table`)**: We create a route `0.0.0.0/0` pointing to the Internet Gateway, and then **associate** (`aws_route_table_association`) both subnets to it.
5. **Security Group (`aws_security_group`)**: Acts as a firewall. We open port `80` (HTTP for web traffic) and port `22` (SSH for terminal access) to the world `0.0.0.0/0`.
6. **S3 Bucket (`aws_s3_bucket`)**: Creates a simple storage bucket.
7. **EC2 Instances (`aws_instance`)**: We launch two `t2.micro` servers. Notice the `user_data` argument! It passes our `userdata.sh` scripts into the servers when they boot.
8. **Application Load Balancer (`aws_lb`)**: Creates the ALB to distribute traffic between our two servers. It requires a Target Group (`aws_lb_target_group`) which checks the health of the servers, and a Listener (`aws_lb_listener`) to forward port 80 traffic to the targets.

### D. The User Data Scripts (`userdata.sh` & `userdata1.sh`)
These are simple Bash scripts. When the EC2 instances launch, these scripts automatically run to:
1. Update packages and install `apache2` (a web server).
2. Fetch the unique Instance ID from AWS metadata.
3. Create a beautiful HTML file with custom CSS animations.
4. Start the Apache web server.

---

## 4. Terraform Execution Lifecycle

Now that our code is written, how do we actually deploy it? Open your VS Code terminal and run these commands in order. Let's understand what happens internally:

### 1. Initialize
```bash
terraform init
```
**What happens internally?** Terraform looks at your `provider.tf` and downloads the necessary AWS plugins/binaries into a hidden `.terraform` folder. It prepares your local directory for Terraform operations.

### 2. Validate
```bash
terraform validate
```
**What happens internally?** Terraform checks your code syntax. If you missed a bracket, misspelled a resource, or forgot a required argument, it will throw an error here so you can fix it before trying to deploy.

### 3. Plan (Dry Run)
```bash
terraform plan
```
**What happens internally?** This is a "dry run." Terraform compares your code to what currently exists in AWS (which is nothing right now). It prints out a detailed plan showing exactly what it *will* create (marked with a green `+`), modify (`~`), or destroy (`-`). **Always review the plan!**

### 4. Apply
```bash
terraform apply
```
**What happens internally?** Terraform reaches out to the AWS API using your IAM credentials and actually creates the resources in the exact order required (e.g., it knows it must create the VPC *before* the Subnets). Type `yes` to approve. 

At the end, Terraform prints the **Outputs**. You will see the `loadbalancerdns` printed on your screen. Copy that URL and paste it into your browser to see your highly available, load-balanced web application in action!

> [!CAUTION]
> **Cleanup:** When you are done testing, DO NOT manually delete resources in the AWS Console. Simply run `terraform destroy` in your terminal, type `yes`, and Terraform will cleanly delete everything it created, saving you from a massive AWS bill!
