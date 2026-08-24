output "public_ip" {
  description = "Public IP Address of the EC2 instance"
  value       = module.ec2_instance.public-ip-address
}
