# This block configures Terraform to use the S3 bucket and DynamoDB table as the backend.
terraform {
  backend "s3" {
    bucket         = "abhishek-s3-demo-xyz" # CHANGE THIS: Must exactly match the S3 bucket name created in main.tf
    key            = "abhi/terraform.tfstate" # The path inside the bucket where the state file will be saved
    region         = "us-east-1"            # CHANGE THIS: Must match the region where your bucket was created
    encrypt        = true                   # Keeps the state file encrypted in S3
    dynamodb_table = "terraform-lock"       # CHANGE THIS: Must exactly match the DynamoDB table name created in main.tf
  }
}
