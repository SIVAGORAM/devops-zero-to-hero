# Multiple Providers

You can use multiple different providers in one single Terraform project. This is highly useful for multi-cloud deployments or integrating different services (e.g., AWS and Azure) simultaneously.

### Step-by-Step Example

**1. Create a `providers.tf` file** in the root directory of your Terraform project.

**2. Define the AWS and Azure providers** inside `providers.tf`:
```hcl
provider "aws" {
  region = "us-east-1"
}

provider "azurerm" {
  # Azure requires explicit authentication details if not using CLI login
  subscription_id = "your-azure-subscription-id"
  client_id       = "your-azure-client-id"
  client_secret   = "your-azure-client-secret"
  tenant_id       = "your-azure-tenant-id"
  
  features {} # Required block for the azurerm provider
}
```

**3. Use both providers in your configuration files.** You can now create resources in both AWS and Azure side-by-side:

```hcl
# This resource will be created in AWS
resource "aws_instance" "example" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t2.micro"
}

# This resource will be created in Azure
resource "azurerm_virtual_machine" "example" {
  name     = "example-vm"
  location = "eastus"
  size     = "Standard_A1"
  # Note: Additional required arguments like resource_group_name are omitted for brevity
}
```
