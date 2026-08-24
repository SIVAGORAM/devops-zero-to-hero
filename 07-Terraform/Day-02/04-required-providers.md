# Provider Configuration (`required_providers`)

The `required_providers` block in Terraform is used to declare and specify the exact provider configurations required for your Terraform module. 

It acts as a safety mechanism, allowing you to explicitly specify the **provider name**, the **source registry**, and strict **version constraints**.

### Example Configuration

```hcl
terraform {
  required_providers {
    # AWS Provider Constraint
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"  # Allows any 3.x version, but NOT 4.x
    }
    
    # Azure Provider Constraint
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.0, < 3.0" # Strictly allows versions between 2.0 and 3.0
    }
  }
}
```

By defining this block, you ensure that anyone (or any CI/CD pipeline) running your Terraform code will use the correct version of the plugins, preventing unexpected breaking changes caused by provider updates.
