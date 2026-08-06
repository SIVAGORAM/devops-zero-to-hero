# Project: Highly Available AWS Architecture using Terraform

This guide is a complete, step-by-step tutorial. By following this document, absolutely anyone—even a beginner—can understand, write, and execute this project from scratch to build a highly available AWS web architecture.

---

## 1. Project Overview (What are we building?)
We are going to write code that automatically builds an enterprise-grade web application in AWS. It includes:
- A custom **VPC (Virtual Private Cloud)** so our servers are isolated.
- **2 Subnets** across two different Availability Zones to ensure our app stays online even if a data center goes down.
- An **Internet Gateway and Route Tables** to allow the public to access our website.
- **Security Groups (Firewalls)** to allow HTTP (Port 80) and SSH (Port 22) traffic.
- **2 EC2 Web Servers** that automatically install an Apache web server on boot.
- An **Application Load Balancer (ALB)** to distribute user traffic evenly between our two servers.

---

## 2. Step-by-Step Implementation Guide

To reimplement this project yourself, create an empty folder on your computer and open it in VS Code. Create the following 5 files exactly as shown below.

### Step 1: `providers.tf`
This file tells Terraform to download the AWS plugin so it can talk to your cloud account.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.11.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
```

### Step 2: `variables.tf`
This file holds our network IP ranges so we don't have to hardcode them.

```hcl
variable "cidr" {
  default = "10.0.0.0/16"
}
```

### Step 3: The Bash Scripts (`userdata.sh` and `userdata1.sh`)
When our EC2 instances boot up, we want them to automatically install a web server and display a webpage. 
Create two files. 

**`userdata.sh` (For Server 1):**
```bash
#!/bin/bash
apt update
apt install -y apache2

INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
apt install -y awscli

cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html>
<head>
  <title>My Portfolio</title>
</head>
<body>
  <h1 style="color:blue;">Terraform Project Server 1</h1>
  <h2>Instance ID: <span style="color:green">$INSTANCE_ID</span></h2>
  <p>Welcome to Abhishek Veeramalla's Channel</p>
</body>
</html>
EOF

systemctl start apache2
systemctl enable apache2
```

**`userdata1.sh` (For Server 2):**
*(Copy the exact same code above, but change the `<h1>` tag to say **Server 2** and change the welcome message. This will prove our load balancer is working!)*

### Step 4: `main.tf` (The Core Infrastructure)
This is the master file that builds the network, servers, and load balancer.

```hcl
# 1. Create the VPC
resource "aws_vpc" "myvpc" {
  cidr_block = var.cidr
}

# 2. Create 2 Subnets in different zones
resource "aws_subnet" "sub1" {
  vpc_id                  = aws_vpc.myvpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "sub2" {
  vpc_id                  = aws_vpc.myvpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
}

# 3. Internet Gateway and Routing
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.myvpc.id
}

resource "aws_route_table" "RT" {
  vpc_id = aws_vpc.myvpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "rta1" {
  subnet_id      = aws_subnet.sub1.id
  route_table_id = aws_route_table.RT.id
}

resource "aws_route_table_association" "rta2" {
  subnet_id      = aws_subnet.sub2.id
  route_table_id = aws_route_table.RT.id
}

# 4. Security Group (Firewall)
resource "aws_security_group" "webSg" {
  name   = "web"
  vpc_id = aws_vpc.myvpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 5. Build the 2 EC2 Instances
resource "aws_instance" "webserver1" {
  ami                    = "ami-0261755bbcb8c4a84" # Ensure this Ubuntu AMI is valid for us-east-1
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.webSg.id]
  subnet_id              = aws_subnet.sub1.id
  user_data              = base64encode(file("userdata.sh"))
}

resource "aws_instance" "webserver2" {
  ami                    = "ami-0261755bbcb8c4a84"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.webSg.id]
  subnet_id              = aws_subnet.sub2.id
  user_data              = base64encode(file("userdata1.sh"))
}

# 6. Application Load Balancer
resource "aws_lb" "myalb" {
  name               = "myalb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.webSg.id]
  subnets            = [aws_subnet.sub1.id, aws_subnet.sub2.id]
}

resource "aws_lb_target_group" "tg" {
  name     = "myTG"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.myvpc.id
}

resource "aws_lb_target_group_attachment" "attach1" {
  target_group_arn = aws_lb_target_group.tg.arn
  target_id        = aws_instance.webserver1.id
  port             = 80
}

resource "aws_lb_target_group_attachment" "attach2" {
  target_group_arn = aws_lb_target_group.tg.arn
  target_id        = aws_instance.webserver2.id
  port             = 80
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_lb.myalb.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    target_group_arn = aws_lb_target_group.tg.arn
    type             = "forward"
  }
}

# 7. Output the Final URL
output "loadbalancerdns" {
  value = aws_lb.myalb.dns_name
}
```

---

## 3. How to Execute the Project

Once you have created all 5 files, open your terminal in that folder and follow these exact steps:

1. **Authenticate to AWS:**
   Make sure your AWS CLI is configured with your IAM credentials.
   ```bash
   aws configure
   ```

2. **Initialize Terraform:**
   This downloads the AWS plugins.
   ```bash
   terraform init
   ```

3. **Check the Plan:**
   This verifies the code and tells you what will be built.
   ```bash
   terraform plan
   ```

4. **Deploy the Infrastructure:**
   This executes the build in AWS. Type `yes` when prompted.
   ```bash
   terraform apply
   ```

---

## 4. How to Test Your Work!

Once the `terraform apply` finishes, look at your terminal. You will see an output variable named **`loadbalancerdns`** with a long URL (e.g., `myalb-123456789.us-east-1.elb.amazonaws.com`).

1. Copy that URL and paste it into Google Chrome.
2. You will see the website for **Server 1**.
3. **Hit Refresh** a few times.
4. Suddenly, the website will switch to **Server 2**. 

**Congratulations!** This proves your Application Load Balancer is successfully distributing traffic across both of your highly-available EC2 instances!

---

## 5. Teardown (Don't forget to delete!)
To ensure AWS does not charge you money, always delete your infrastructure when you are done practicing.
```bash
terraform destroy
```
*(Type `yes` when prompted, and Terraform will automatically delete the VPC, Load Balancer, and EC2 instances).*
