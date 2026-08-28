variable "ami" {
  description = "The AMI ID passed into the module"
  type        = string
}

# The Map Variable! This is the secret to Workspace magic.
variable "instance_type" {
  description = "A map defining the instance size for each environment"
  type        = map(string)
  default = {
    "dev"   = "t2.micro"  # Cheap servers for Developers
    "stage" = "t2.medium" # Medium servers for Testing
    "prod"  = "t2.xlarge" # Massive servers for Live Traffic
  }
}
