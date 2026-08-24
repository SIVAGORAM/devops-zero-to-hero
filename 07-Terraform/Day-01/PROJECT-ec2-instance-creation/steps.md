# AWS EC2 Instance Creation with Terraform

This guide walks you through the steps to provision an AWS EC2 instance using Terraform, as defined in our `main.tf` configuration file.

## 1. Overview of the Configuration

In this project, we have a Terraform configuration file named `main.tf`. Inside this file, we define the AWS provider and the specific EC2 instance resource we want to create. 

Based on our `main.tf`, the configuration looks like this:

```hcl
# 1. Define the Provider (AWS)
provider "aws" {
  region = "us-east-1"
}

# 2. Create an EC2 Instance
resource "aws_instance" "my_first_ec2" {
  ami           = "ami-0332d564d76dbd8d6" 
  instance_type = "t3.micro"
  subnet_id     = "subnet-0711a9e8b97e6ca91"
  key_name      = "awslogin"
  tags = {
    Name = "Practical-EC2"
  }
}
```

## 2. Initialize Terraform

In your terminal, navigate to the directory containing your `main.tf` file and run:

```bash
terraform init
```

This command initializes the Terraform working directory. It downloads the necessary AWS provider plugins required to interact with the AWS API.

## 3. Plan the Configuration

Before applying changes, it's a best practice to see what Terraform intends to do. Run:

```bash
terraform plan
```

Terraform will display an execution plan showing exactly what resources will be added, changed, or destroyed (in this case, creating one EC2 instance).

## 4. Apply the Configuration

Run the following command to actually create the AWS resources defined in your `main.tf`:

```bash
terraform apply
```

Review the plan that is printed to the screen, and type `yes` when prompted to apply it. Terraform will now provision your EC2 instance in AWS.

## 5. Verify Resources

After Terraform completes the provisioning process, you can verify the creation of your EC2 instance by logging into the **AWS Management Console** and navigating to the EC2 Dashboard, or by using the AWS CLI.

## 6. Destroy Resources

If you want to remove the resources created by Terraform to avoid unnecessary AWS charges, use the following command:

```bash
terraform destroy
```

Be cautious when using `terraform destroy` as it will completely delete the infrastructure specified in your Terraform configuration. Type `yes` when prompted to confirm the destruction.
