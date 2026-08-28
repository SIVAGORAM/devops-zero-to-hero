provider "aws" {
  region = "us-east-1"
}

# The Vault Provider tells Terraform how to connect to our HashiCorp Vault server
provider "vault" {
  address          = "http://<YOUR_EC2_IP>:8200" # CHANGE THIS: Replace <YOUR_EC2_IP> with the Public IP of your Vault EC2 instance
  skip_child_token = true

  # We use AppRole for machine-to-machine authentication (similar to an IAM Role)
  auth_login {
    path = "auth/approle/login"

    parameters = {
      role_id   = "<YOUR_ROLE_ID>"   # CHANGE THIS: Paste the Role ID you generated in the terminal
      secret_id = "<YOUR_SECRET_ID>" # CHANGE THIS: Paste the Secret ID you generated in the terminal
    }
  }
}

# This data block reaches out to Vault and securely fetches the secret we created!
data "vault_kv_secret_v2" "example" {
  mount = "kv"          # CHANGE THIS if your mount path is different (we used 'kv' in the lab)
  name  = "test_secret" # CHANGE THIS if you named your secret something else (we used 'test_secret')
}

# We create an AWS EC2 instance and securely inject the Vault secret as a tag!
resource "aws_instance" "my_instance" {
  ami           = "ami-053b0d53c279acc90" # CHANGE THIS: Ensure this is a valid AMI in your region
  instance_type = "t2.micro"

  tags = {
    Name = "test"
    # THE MAGIC: We are tagging the EC2 instance with the secret we fetched from Vault!
    # Vault Secret Key: "username" -> Value: "siva2003"
    Secret = data.vault_kv_secret_v2.example.data["username"] 
  }
}
