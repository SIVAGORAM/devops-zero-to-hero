# 🕵️ Terraform Scenario-Based Interview Questions (Zero to Hero)

While standard Q&A proves you know the definitions, **Scenario-Based Questions** prove you have actually used Terraform in production. Interviewers will give you a "disaster scenario" and ask how you would fix it.

Here are the top real-world scenarios you will face in a DevOps interview and exactly how to answer them!

---

### Scenario 1: The Corrupted State File
**The Interviewer asks:** *"A junior engineer accidentally deleted the `terraform.tfstate` file from the S3 bucket. What happens when you run `terraform apply` now, and how do you fix it without destroying the live infrastructure?"*

**The Answer:**
*"If the state file is deleted, Terraform loses its memory. Running `terraform apply` will attempt to recreate all the resources from scratch, which will cause errors or duplicates because the real infrastructure still exists in AWS.*
*To fix this, I would first check if S3 Versioning is enabled on the backend bucket (which is a best practice). If it is, I would simply restore the previous version of the state file. If versioning is disabled, I would have to use the `terraform import` command to manually bring every existing AWS resource back into a new state file."*

---

### Scenario 2: The Secret Leak
**The Interviewer asks:** *"You hardcoded a database password into `terraform.tfvars` and accidentally pushed it to a public GitHub repository. What are your immediate steps?"*

**The Answer:**
*"1. I would immediately go to the database (e.g., AWS RDS) and change the password so the leaked password is useless.*
*2. I would rotate any other keys exposed in that commit.*
*3. I would remove the `.tfvars` file from the Git history using a tool like BFG Repo-Cleaner or `git filter-branch`.*
*4. To prevent this from happening again, I would implement HashiCorp Vault or AWS Secrets Manager to fetch secrets dynamically, and ensure `*.tfvars` is permanently added to the `.gitignore` file."*

---

### Scenario 3: Zero-Downtime Deployment
**The Interviewer asks:** *"You have an EC2 instance running a live production website. You need to change the AMI (operating system) of the instance using Terraform. By default, Terraform will destroy the old server before creating the new one, causing 5 minutes of downtime. How do you achieve zero downtime?"*

**The Answer:**
*"I would use the `lifecycle` meta-argument inside the `aws_instance` resource block and set `create_before_destroy = true`. This forces Terraform to build the new EC2 instance first, wait for it to be ready, and only then destroy the old one, ensuring the website never goes offline."*

---

### Scenario 4: The CI/CD Pipeline Lock
**The Interviewer asks:** *"Your Jenkins pipeline ran `terraform apply`, but the pipeline crashed halfway through due to a network timeout. Now, whenever you try to run Terraform again, you get an error saying 'Error acquiring the state lock'. How do you fix this?"*

**The Answer:**
*"Because the pipeline crashed, Terraform never released the lock on the DynamoDB table. I would run `terraform force-unlock <LOCK_ID>`, using the Lock ID provided in the error message. However, before doing this, I must verify that no other team member is actively running an apply, otherwise forcing the unlock could corrupt the state file."*

---

### Scenario 5: Refactoring Code Without Destroying Infrastructure
**The Interviewer asks:** *"You have a massive `main.tf` file with 50 resources. You decide to clean up the code by moving the EC2 instances into a custom Module. If you just copy and paste the code into the module and run `terraform apply`, Terraform wants to destroy the old EC2 instances and create new ones. How do you refactor the code without destroying the live servers?"*

**The Answer:**
*"Terraform wants to destroy them because their logical address in the state file changed (e.g., from `aws_instance.web` to `module.ec2.aws_instance.web`). To fix this, I would use the `terraform state mv` command (or the `moved {}` block in modern Terraform) to manually update the state file to reflect the new address. This tells Terraform, 'Hey, the resource is the same, it just moved to a module folder.' "*

---

### Scenario 6: The Partial Failure
**The Interviewer asks:** *"Your Terraform code is supposed to create a VPC, a Subnet, and an EC2 instance. The VPC and Subnet create successfully, but the EC2 instance fails because you requested an instance type that isn't available in that region. What is the state of your infrastructure, and what happens when you run `terraform apply` again after fixing the typo?"*

**The Answer:**
*"Terraform is not fully atomic. The VPC and Subnet were created successfully and are recorded in the state file. The EC2 instance failed and is not in the state file. When I fix the typo and run `terraform apply` again, Terraform is smart enough to realize the VPC and Subnet already exist, so it will leave them alone and ONLY try to create the EC2 instance."*

---

### Scenario 7: Managing Multiple Environments
**The Interviewer asks:** *"We have Dev, Stage, and Prod environments. We want them to be identical, but Prod needs larger EC2 instances than Dev. How would you structure this in Terraform?"*

**The Answer:**
*"I would use a single generic Root Module. For the environments, I have two choices based on the company's scale:*
*1. **Workspaces (Small Scale):** Use `terraform workspace new dev/stage/prod` and use a `lookup()` map variable to dynamically assign instance sizes based on `terraform.workspace`.*
*2. **Terragrunt / Separate Directories (Enterprise Scale):** Create separate folders for Dev, Stage, and Prod. Each folder calls the same generic module but passes different variables via `terraform.tfvars`. This ensures complete isolation of state files and reduces the blast radius if something goes wrong."*

---

### Scenario 8: Provider Version Issues
**The Interviewer asks:** *"Your code works perfectly on your laptop. You push it to GitHub, and the CI/CD pipeline runs `terraform apply`, but it fails with an error saying a specific resource argument doesn't exist. You check, and the argument definitely exists in the AWS provider documentation. What went wrong?"*

**The Answer:**
*"This is a Provider Version mismatch. My laptop likely downloaded a newer version of the AWS provider plugin during `terraform init`, while the CI/CD pipeline downloaded an older version that doesn't support that new argument yet. To fix this, I would hardcode a specific version constraint in the `required_providers` block and commit the `.terraform.lock.hcl` file to Git to ensure all environments use the exact same provider version."*

---

### Scenario 9: The Manual Tagging Conflict
**The Interviewer asks:** *"Your company has a separate automated security script that scans AWS and adds a `Scanned=True` tag to all EC2 instances. Every time you run `terraform plan`, Terraform sees this tag, realizes it's not in the Terraform code, and wants to delete the tag. How do you stop Terraform from deleting the automated tags?"*

**The Answer:**
*"I would use the `lifecycle` block inside the `aws_instance` resource and add `ignore_changes = [tags["Scanned"]]`. This tells Terraform to ignore that specific tag during its drift detection, allowing the security script to do its job without Terraform interfering."*

---

### Scenario 10: The Untested Module Upgrade
**The Interviewer asks:** *"You are using a public Terraform module from the Registry for your EKS cluster. A new version of the module is released. You update the version number in your code and run `terraform apply` directly in production. What is wrong with this approach, and how should you do it?"*

**The Answer:**
*"Applying an unverified module version directly to production is highly dangerous because the module author might have introduced breaking changes that will destroy and recreate the EKS cluster!*
*The correct approach is:*
*1. Run it in a Sandbox or Dev environment first.*
*2. Always run `terraform plan` and carefully read the output to ensure no unexpected resources are marked for destruction (`- / +`).*
*3. Read the module's CHANGELOG on GitHub for any breaking changes before upgrading."*
