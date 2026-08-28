# Day 06: Managing Environments with Terraform Workspaces

Welcome to Day 06! Today we tackle a massively important problem in real-world DevOps: **Managing Multiple Environments**. 
Every professional company has at least three environments:
- **Dev**: Where developers test broken code (`t2.micro` - cheap)
- **Stage**: Where QA tests finished code (`t2.medium` - slightly faster)
- **Prod**: Where actual customers use the app (`t2.xlarge` - massive and expensive)

How do we deploy to all three environments without rewriting our Terraform code three times? The answer is **Terraform Workspaces**.

---

## 🚫 The Bad Way (Why `terraform.tfvars` isn't enough)

Imagine you want to deploy a `dev` server and a `stage` server.
You might think: *"I'll just create a `stage.tfvars` file and run `terraform apply -var-file=stage.tfvars`!"*

**What happens if you do this?**
Terraform will look at your single `terraform.tfstate` file, see that a `dev` server already exists, and instead of creating a *second* server for staging, it will just **destroy** or **overwrite** your `dev` server to turn it into a `stage` server! 
This is because both environments are trying to share the exact same state file memory.

*(To reset your project and fix this, you must manually delete the old memory file by running `rm -rf terraform.tfstate` before starting the Workspace tutorial below).*

---

## ✅ The Professional Solution: Terraform Workspaces

Workspaces allow you to use the exact same code, but Terraform will automatically create a **completely separate, isolated state file** for each environment. It essentially places your code in a parallel universe.

### The Magic Commands
Open your terminal in the `Day-06` folder and try running these commands:

1. **Create the Workspaces:**
```bash
terraform workspace new dev
terraform workspace new stage
terraform workspace new prod
```
*If you run the `tree` command (or look in your file explorer), you will notice a new hidden folder called `.terraform.tfstate.d`. This is where Terraform is safely storing the separate state files!*

2. **Switching Environments:**
Want to deploy to Staging? Just switch your workspace!
```bash
terraform workspace select stage
```

3. **Check your Current Environment:**
Not sure where you are deploying? Run:
```bash
terraform workspace show
```

---

## 🧙‍♂️ The Code Magic: The `lookup()` function

Look at `Day-06/main.tf` and `Day-06/variables.tf`. How does the code know to build a `t2.xlarge` in Prod, but a `t2.micro` in Dev?

**1. The Map Variable:**
In `variables.tf`, we defined a "map" (a dictionary) that assigns an instance size to an environment name:
```hcl
variable "instance_type" {
  type = map(string)
  default = {
    "dev"   = "t2.micro"
    "stage" = "t2.medium"
    "prod"  = "t2.xlarge"
  }
}
```

**2. The Lookup Function:**
In `main.tf`, we use the `lookup()` function combined with `terraform.workspace` (a built-in variable that always knows what workspace you are currently in):
```hcl
instance_type = lookup(var.instance_type, terraform.workspace, "t2.micro")
```
**Translation:** *"Hey Terraform, check what workspace I am currently in. Look at the `var.instance_type` map. If I am in 'prod', pull the 'prod' value (`t2.xlarge`). If you can't find a match, just give me a `t2.micro`."*

---

## 🚀 Hands-On: Zero to Hero Deployment

Let's test this in the real world!

1. Initialize your directory:
```bash
terraform init
```

2. Switch to the `dev` environment:
```bash
terraform workspace select dev
```

3. Deploy the Dev server:
```bash
terraform apply -auto-approve
```
*(AWS is now building a cheap `t2.micro` server).*

4. Now, switch to the `stage` environment!
```bash
terraform workspace select stage
```

5. Deploy the Stage server:
```bash
terraform apply -auto-approve
```
*(Instead of updating the Dev server, AWS is now building a brand new, completely separate `t2.medium` server!)*

6. Clean up:
When you are done, make sure to destroy BOTH environments to avoid AWS charges:
```bash
terraform workspace select dev
terraform destroy -auto-approve

terraform workspace select stage
terraform destroy -auto-approve
```

---
### 🛠️ Industry Standard Note
*If you look at `Day-06/modules/ec2_instance/main.tf`, you'll notice I removed the `provider "aws"` block that was in the instructor's original notes. In the professional world, child modules must **never** contain provider blocks. Providers should strictly live in the root module (`Day-06/providers.tf`), which I created for you!*
