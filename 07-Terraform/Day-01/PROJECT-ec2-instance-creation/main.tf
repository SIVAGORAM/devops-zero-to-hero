# Terraform Practical Exercises

# 1. Define the Provider (AWS)
provider "aws" {
  region = "us-east-1"
}

# 2. Start building resources below!

# Create an EC2 Instance
resource "aws_instance" "my_first_ec2" {
  ami           = "ami-0332d564d76dbd8d6" # Specify an appropriate AMI ID
  instance_type = "t3.micro"
  subnet_id     = "subnet-0711a9e8b97e6ca91"
  key_name      = "awslogin"
  tags = {
    Name = "Practical-EC2"
  }
}
