# Define the AWS provider configuration.
provider "aws" {
  region = "us-east-1"  # CHANGE THIS: Replace with your desired AWS region.
}

variable "cidr" {
  default = "10.0.0.0/16"
}

# 1. Creates an SSH Key Pair in AWS using your laptop's public key
resource "aws_key_pair" "example" {
  key_name   = "terraform-demo-abhi"  # CHANGE THIS: Replace with your desired unique key name
  public_key = file("~/.ssh/id_rsa.pub")  # CHANGE THIS: Replace with the actual path to your public key file (e.g. C:/Users/Name/.ssh/id_rsa.pub on Windows)
}

# 2. Creates the Virtual Private Cloud (VPC)
resource "aws_vpc" "myvpc" {
  cidr_block = var.cidr
}

# 3. Creates the Subnet inside the VPC
resource "aws_subnet" "sub1" {
  vpc_id                  = aws_vpc.myvpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true # Automatically assigns a public IP to our server
}

# 4. Creates an Internet Gateway so the VPC can talk to the internet
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.myvpc.id
}

# 5. Creates a Route Table directing internet traffic to the Gateway
resource "aws_route_table" "RT" {
  vpc_id = aws_vpc.myvpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

# 6. Associates the Route Table with our Subnet
resource "aws_route_table_association" "rta1" {
  subnet_id      = aws_subnet.sub1.id
  route_table_id = aws_route_table.RT.id
}

# 7. Creates a Security Group (Firewall) allowing Web (80) and SSH (22)
resource "aws_security_group" "webSg" {
  name   = "web"
  vpc_id = aws_vpc.myvpc.id

  ingress {
    description = "HTTP from VPC"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "SSH"
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

  tags = {
    Name = "Web-sg"
  }
}

# 8. Creates the EC2 Instance and runs the Provisioners
resource "aws_instance" "server" {
  ami                    = "ami-0261755bbcb8c4a84" # CHANGE THIS: Make sure this AMI is a valid Ubuntu AMI in your specific region
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.example.key_name
  vpc_security_group_ids = [aws_security_group.webSg.id]
  subnet_id              = aws_subnet.sub1.id

  # This block configures HOW Terraform logs into the server
  connection {
    type        = "ssh"
    user        = "ubuntu"  
    private_key = file("~/.ssh/id_rsa")  # CHANGE THIS: Replace with the actual path to your private key (e.g. C:/Users/Name/.ssh/id_rsa on Windows)
    host        = self.public_ip
  }

  # PROVISIONER 1 (FILE): Copies the python app from our laptop to the new AWS server
  provisioner "file" {
    source      = "app.py"  
    destination = "/home/ubuntu/app.py"  
  }

  # PROVISIONER 2 (REMOTE-EXEC): Runs these terminal commands inside the new AWS server
  provisioner "remote-exec" {
    inline = [
      "echo 'Hello from the remote instance'",
      "sudo apt update -y",  
      "sudo apt-get install -y python3-pip",  
      "cd /home/ubuntu",
      "sudo pip3 install flask",
      "sudo python3 app.py &", # The '&' ensures the app stays running in the background!
    ]
  }
}

# 9. A Null Resource to demonstrate the local-exec provisioner
resource "null_resource" "example" {
  # This trigger ensures the provisioner runs every single time Terraform is applied
  triggers = {
    always_run = "${timestamp()}"
  }

  # PROVISIONER 3 (LOCAL-EXEC): Runs this terminal command on YOUR laptop, not on AWS.
  provisioner "local-exec" {
    command = "echo 'The AWS Server has been successfully built! This is a local command.' > deployment_status.txt"
  }
}
