variable "ami" {
  description = "The AMI ID for the instance"
  type        = string
}

variable "instance_type" {
  description = "The size of the instance (e.g. t2.micro, t2.medium)"
  type        = string
}
