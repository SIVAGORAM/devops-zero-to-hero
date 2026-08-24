# Multiple Region Implementation in Terraform

You can make use of the `alias` keyword to implement a multi-region infrastructure setup within the *same* provider. This allows you to deploy resources to `us-east-1` and `us-west-2` in the exact same Terraform project.

### Using the `alias` Keyword

First, define the provider multiple times, giving each an `alias` name:

```hcl
# Default provider (used if no alias is specified)
provider "aws" {
  region = "us-east-1"
}

# Aliased provider for the West region
provider "aws" {
  alias  = "us-west-2"
  region = "us-west-2"
}
```

When creating resources, use the `provider` meta-argument to specify which region that specific resource should be deployed to:

```hcl
# This will be deployed to us-east-1 (default)
resource "aws_instance" "example_east" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t2.micro"
}

# This will be deployed to us-west-2 (using the alias)
resource "aws_instance" "example_west" {
  provider      = aws.us-west-2
  
  ami           = "ami-0123456789abcdef0"
  instance_type = "t2.micro"
}
```
*(Note: In Terraform v0.15+, you reference aliased providers without quotes, e.g., `provider = aws.us-west-2` rather than `provider = "aws.us-west-2"`).*
