# We call our reusable module and pass the variables into it.
module "ec2_instance" {
  source = "./modules/ec2_instance"
  ami    = var.ami
  
  # THE MAGIC LINE: 
  # lookup(map_name, key_to_find, default_value)
  # It looks at the current workspace (dev, stage, or prod), checks the map variable, 
  # and grabs the matching instance type! If it can't find a match, it defaults to t2.micro.
  instance_type = lookup(var.instance_type, terraform.workspace, "t2.micro")
}
