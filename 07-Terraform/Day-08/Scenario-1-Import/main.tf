provider "aws" {
  region = "us-east-1"
}

# The modern way to import resources (Terraform 1.5+)
# 1. Provide the exact ID of the manually created resource
# 2. Tell Terraform what you want to call this resource in your code
import {
  id = "i-0534234i234i4234n" # CHANGE THIS to the actual Instance ID from your AWS Console
  to = aws_instance.example
}

# NOTE: Before running 'terraform apply', you must run this magic command:
# terraform plan -generate-config-out=generated_resources.tf
#
# This command will automatically look at AWS and write the HCL code for you!
