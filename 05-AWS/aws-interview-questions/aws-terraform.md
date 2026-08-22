# Terraform (IaC) Interview Questions

Terraform is the industry standard for Infrastructure as Code (IaC). These questions test your ability to safely and predictably manage cloud infrastructure at scale.

### 1. What is Terraform?
**Answer:** Terraform is an open-source Infrastructure as Code (IaC) tool created by HashiCorp. It allows DevOps engineers to define, provision, and manage infrastructure resources across various cloud providers using a human-readable, declarative configuration language (HCL).

### 2. How does Terraform work with AWS?
**Answer:** Terraform acts as a client. It reads your `.tf` configuration files, compares them to the current state of the infrastructure, and makes authenticated API calls to AWS on your behalf to create, modify, or destroy resources so that the cloud matches your code.

### 3. What is an AWS Provider in Terraform?
**Answer:** Providers are plugins that Terraform uses to translate your HCL code into API calls for a specific service. The AWS Provider contains all the logic required to authenticate and interact securely with AWS APIs. You define it using the `provider "aws" {}` block.

### 4. How do you define resources in Terraform?
**Answer:** Resources are the fundamental building blocks of Terraform. They are defined using HashiCorp Configuration Language (HCL). You use the `resource` block, followed by the resource type (e.g., `"aws_instance"`) and a local logical name, enclosing the configuration arguments in curly braces.

### 5. What is a Terraform state file (`terraform.tfstate`)?
**Answer:** The state file is the "brain" of Terraform. It is a JSON file that maps your Terraform code to the real-world resources deployed in AWS. Terraform uses this file to determine what currently exists, what needs to be updated, and what needs to be destroyed.

### 6. How can you initialize a Terraform project?
**Answer:** You run the `terraform init` command in your project directory. This is the first command you must run; it initializes the backend, downloads the required provider plugins (like the AWS provider), and prepares the working directory.

### 7. How do you plan infrastructure changes in Terraform?
**Answer:** You run the `terraform plan` command. This performs a "dry run" by comparing your code against the state file. It outputs a detailed execution plan showing exactly what resources will be created (`+`), modified (`~`), or destroyed (`-`) without actually making any changes to AWS.

### 8. What is the `terraform apply` command used for?
**Answer:** The `terraform apply` command actually executes the changes shown in the plan. It reaches out to the AWS API and provisions, updates, or deletes the real-world infrastructure to match your code. It will prompt for a `yes` confirmation before executing.

### 9. What is the purpose of Terraform variables?
**Answer:** Variables (`variables.tf`) allow you to parameterize your Terraform configurations. Instead of hardcoding values (like an AMI ID or instance type), you use variables (`var.instance_type`), making your code dynamic, reusable, and easily deployable across different environments (Dev, QA, Prod).

### 10. How do you manage secrets and sensitive information in Terraform?
**Answer:** Never hardcode passwords or secrets in plain text! You should use environment variables (e.g., `TF_VAR_db_password`), retrieve them dynamically at runtime using AWS Secrets Manager or AWS Systems Manager Parameter Store data sources, and mark the variables as `sensitive = true` so Terraform redacts them from terminal output.

### 11. What is remote state in Terraform?
**Answer:** By default, Terraform stores the state file locally on your hard drive, which breaks team collaboration. "Remote State" means storing the `terraform.tfstate` file in a centralized, secure location like an Amazon S3 bucket. This enables team collaboration and allows you to use DynamoDB for "State Locking" to prevent two engineers from applying changes simultaneously.

### 12. How can you manage multiple environments (Dev, Prod) with Terraform?
**Answer:** There are two main approaches: 
1. **Workspaces:** Using `terraform workspace` allows you to use the exact same code directory but maintain separate state files for each environment.
2. **Directory Layout:** Creating physically separate folders (e.g., `/dev`, `/prod`) that call reusable Terraform Modules. This is generally preferred for production isolation.

### 13. How do you handle dependencies between resources in Terraform?
**Answer:** Terraform automatically handles **Implicit Dependencies**. If an EC2 instance references a VPC ID (`vpc_id = aws_vpc.my_vpc.id`), Terraform knows it must create the VPC *before* the EC2 instance. For complex scenarios where Terraform cannot infer the dependency, you use the `depends_on` meta-argument to enforce explicit ordering.

### 14. What is Terraform's "apply" process?
**Answer:** The apply process follows three steps: 
1. **Refresh:** Checks the real-world status of resources in AWS.
2. **Plan:** Compares the desired state (your code) against the current state and generates an execution graph.
3. **Apply:** Makes the necessary AWS API calls in the correct dependency order to achieve the desired state.

### 15. How can you manage versioning of Terraform configurations?
**Answer:** Your `.tf` files should be treated like application source code and stored in a Version Control System (like Git/GitHub). You should enforce peer reviews via Pull Requests before any `terraform apply` is executed via a CI/CD pipeline (a practice known as GitOps).

### 16. What is the difference between Terraform and CloudFormation?
**Answer:** AWS CloudFormation is a proprietary IaC tool that only manages AWS resources. Terraform is an open-source, multi-cloud tool that can manage AWS, Azure, GCP, and third-party tools (like GitHub, Datadog, or Kubernetes) using a unified HCL language.

### 17. What is a Terraform Module?
**Answer:** A module is a reusable, self-contained package of Terraform configurations. Just like functions in programming, modules allow you to abstract complex infrastructure (like an entire VPC setup) into a single block that can be called repeatedly with different variables, enforcing DRY (Don't Repeat Yourself) principles.

### 18. How can you destroy infrastructure created by Terraform?
**Answer:** You run the `terraform destroy` command. This reads your state file and safely deletes all resources managed by that specific configuration in the reverse order of their creation.

### 19. How does Terraform manage updates to existing resources?
**Answer:** Terraform is declarative. If you change a parameter (like adding a tag), Terraform will use the AWS API to modify the existing resource *in-place*. However, if you change a fundamental property (like changing an EC2 instance's AMI), Terraform will destroy the old instance and recreate a new one, as AWS does not allow in-place AMI changes.

### 20. Can Terraform be used for managing third-party resources?
**Answer:** Yes! Terraform has thousands of providers in the Terraform Registry. You can write one Terraform script that provisions AWS infrastructure, configures a Snowflake database, sets up Datadog monitoring alerts, and creates GitHub repositories all at the same time.
