# This is the reusable EC2 Blueprint
# NOTE: Industry standard dictates that provider blocks should NOT be in child modules!
# Providers should only be defined in the root module.

resource "aws_instance" "example" {
  ami           = var.ami
  instance_type = var.instance_type
}
