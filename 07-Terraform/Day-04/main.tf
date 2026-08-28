provider "aws" {
  region = "us-east-1" # CHANGE THIS if you want a different region
}

resource "aws_instance" "abhishek" {
  instance_type = "t2.micro"
  ami           = "ami-053b0d53c279acc90" # CHANGE THIS: Ensure this AMI is valid in your region
  subnet_id     = "subnet-019ea91ed9b5252e7" # CHANGE THIS: Ensure this Subnet ID exists in your AWS account
}

# This bucket is created to store the Terraform State file centrally.
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "abhishek-s3-demo-xyz" # CHANGE THIS: S3 bucket names must be globally unique across all AWS accounts!
}

# This DynamoDB table is created to lock the state file and prevent concurrent modifications.
resource "aws_dynamodb_table" "terraform_lock" {
  name           = "terraform-lock"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
