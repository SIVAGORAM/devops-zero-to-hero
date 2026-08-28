# Day 08: Most Asked Interview Scenarios (Importing & Drift Detection)

Welcome to Day 08! Today we are stepping away from standard deployments to focus exclusively on **Interview Preparation**. 

In almost every Terraform interview, the interviewer will test your real-world experience by asking you two specific "troubleshooting" scenarios:
1. How do you bring a manually created AWS resource into Terraform? (**Migration/Import**)
2. How do you detect if a developer manually changed a server in the AWS console? (**Drift Detection**)

Let's dive into both theoretically and practically from Zero to Hero!

---

## 🏗️ Scenario 1: Terraform Migration (The `import` command)

**The Interview Question:** 
*"A junior developer accidentally logged into the AWS Console and manually created an EC2 instance. We want to start managing that instance using Terraform without deleting it. How do we do that?"*

**The Answer:**
*"We use Terraform Import. We write an `import` block with the instance ID, run a command to generate the configuration, and bring it into our state file."*

### Hands-On: How to actually do it (Terraform 1.5+)

Look inside the `Scenario-1-Import` folder. Open `main.tf`.

**Step 1: Write the Import Block**
Instead of writing a massive `aws_instance` block from scratch, we just tell Terraform the ID of the manual server:
```hcl
import {
  id = "i-0534234i234i4234n" # The manual instance ID
  to = aws_instance.example  # What we want to name it in Terraform
}
```

**Step 2: Generate the Code (The Magic Trick)**
Run this command in your terminal:
```bash
terraform plan -generate-config-out=generated_resources.tf
```
*What happens?* Terraform reaches into AWS, looks at the manual server, and **automatically writes the HCL code for you** inside a new file called `generated_resources.tf`!

**Step 3: Clean up and Apply**
1. Open `generated_resources.tf`.
2. Copy the entire `resource "aws_instance" "example"` block that Terraform wrote.
3. Paste it into your `main.tf` file.
4. Delete `generated_resources.tf`.
5. Run `terraform apply`.

**Congratulations!** The manual EC2 instance is now officially managed by Terraform.

*(Note: In older versions of Terraform, we had to manually write all the code and then run the CLI command `terraform import aws_instance.example i-xxxxx`. If an interviewer asks, it is good to mention you know both the old CLI command and the modern `import` block method!)*

---

## 🚨 Scenario 2: Terraform Drift Detection

**The Interview Question:**
*"You deployed a database with 50GB of storage using Terraform. A week later, a sysadmin logs into the AWS console manually and increases it to 100GB. Your Terraform code still says 50GB. This is called 'Drift'. How do you detect and fix this?"*

**The Answer:**
*"There are two main approaches: Reactive Detection (Cron Jobs & Audits) and Proactive Prevention (Strict IAM Rules)."*

### Detailed Breakdown

#### 1. Reactive Detection (Finding the drift after it happens)
- **The `terraform plan` / `refresh` method:** 
  You can set up a CI/CD pipeline (like GitHub Actions) to run `terraform plan` on a schedule (a cron job) every night. When `terraform plan` runs, it silently runs a `refresh` in the background, comparing the real AWS world to your state file. If it detects a drift, the pipeline will flag an error and notify the team!
  👉 *(Check out `Scenario-2-Drift-Detection/github-actions-cron.yml` to see exactly what this code looks like in the real world!)*
  
- **The Audit Log / Webhook method (Advanced):**
  You can configure **AWS CloudTrail** (which records every single click in the AWS account). If CloudTrail detects that a user manually changed an EC2 instance, it triggers an **AWS EventBridge** rule, which triggers an **AWS Lambda** function, which instantly sends a **Slack Alert** to your DevOps team saying: *"Warning! User XYZ just manually edited a Terraform resource!"*

#### 2. Proactive Prevention (Stopping it before it happens)
- **Strict IAM Rules (The Best Solution):**
  The best way to fix drift is to never let it happen. You create strict AWS IAM Policies for your developers. You give them `Read-Only` access to the AWS Console, but give `AdministratorAccess` to your Terraform CI/CD pipeline role. This guarantees that **nobody** can manually click "Edit" in the AWS console. The only way to change infrastructure is by pushing code to GitHub!
  👉 *(Check out `Scenario-2-Drift-Detection/iam_prevention.tf` to see exactly how to write this policy!)*

---
### 🎓 Summary for Interviews
- If they ask about **bringing existing things into Terraform**: Mention `import` blocks and `-generate-config-out`.
- If they ask about **catching manual changes**: Mention Scheduled `terraform plan` cron jobs.
- If they ask about **preventing manual changes**: Mention Strict IAM `Read-Only` policies.
