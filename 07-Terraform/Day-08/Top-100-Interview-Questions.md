# 🚀 Top 100 Terraform Interview Questions & Answers (Zero to Hero)

Welcome to the ultimate Terraform Interview Cheat Sheet! This list is categorized from beginner concepts to advanced real-world scenarios. Master these, and you will confidently crack any DevOps Terraform interview.

---

## 🟢 Category 1: Terraform Fundamentals (1-20)

**1. What is Terraform?**
Terraform is an open-source Infrastructure as Code (IaC) tool created by HashiCorp. It allows you to define, provision, and manage infrastructure using a declarative language called HCL (HashiCorp Configuration Language).

**2. What is Infrastructure as Code (IaC)?**
IaC is the process of managing and provisioning computing infrastructure through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools.

**3. What is the difference between Declarative and Imperative IaC?**
- **Declarative (Terraform):** You specify *what* the final state should look like, and the tool figures out *how* to achieve it.
- **Imperative (Ansible/Chef):** You specify the exact step-by-step commands to achieve the final state.

**4. What are the main competitors to Terraform?**
AWS CloudFormation, Azure ARM Templates, Ansible, Pulumi, and Google Cloud Deployment Manager.

**5. Why choose Terraform over AWS CloudFormation?**
Terraform is **cloud-agnostic**. It can manage resources across AWS, Azure, GCP, and Kubernetes simultaneously using providers. CloudFormation is strictly locked to AWS.

**6. What is a Terraform Provider?**
A plugin that allows Terraform to interact with cloud platforms (like AWS, Azure), SaaS providers, and other APIs.

**7. Explain the core Terraform workflow commands.**
- `terraform init`: Initializes the directory, downloads provider plugins, and sets up the backend.
- `terraform plan`: Creates an execution plan, showing what actions Terraform *will* take.
- `terraform apply`: Executes the actions proposed in the plan to build the infrastructure.
- `terraform destroy`: Deletes all resources managed by the current Terraform configuration.

**8. What does `terraform validate` do?**
It checks whether the configuration is syntactically valid and internally consistent, without accessing any remote services.

**9. What does `terraform fmt` do?**
It automatically rewrites Terraform configuration files to a canonical format and style (fixes indentation).

**10. What is a `resource` in Terraform?**
A resource is the most important element in Terraform. It describes an infrastructure object, such as a virtual network, compute instance, or higher-level component.

**11. What is a `data source` in Terraform?**
Data sources allow Terraform to fetch and use data defined outside of Terraform (e.g., finding the latest AWS AMI ID or an existing VPC ID).

**12. What is the difference between a variable and an output?**
- **Input Variables:** Serve as parameters for a Terraform module, allowing users to customize behavior without editing the source.
- **Output Values:** Return values from a Terraform module, making information about your infrastructure available on the command line.

**13. What is a `.tfvars` file?**
A file used to systematically assign values to variables defined in your Terraform configuration, keeping your code clean and separating environment-specific data.

**14. What are `local` values in Terraform?**
Locals assign a name to an expression or value, allowing it to be reused multiple times within a module without repeating the expression (similar to temporary variables).

**15. Explain `count` vs `for_each`.**
Both create multiple instances of a resource.
- `count`: Uses a list/index. If you remove an item from the middle of a list, Terraform shifts all subsequent items, which can accidentally destroy/recreate resources.
- `for_each`: Uses a map/string set. It identifies instances by a unique string key, making it much safer for dynamic scaling.

**16. What is a `null_resource`?**
A resource that implements the standard resource lifecycle but takes no further action. It is commonly used to trigger `local-exec` or `remote-exec` provisioners.

**17. What is the `depends_on` meta-argument?**
Terraform automatically builds a dependency graph. If resource B implicitly uses resource A's ID, Terraform knows to build A first. `depends_on` is used to force a dependency when Terraform cannot infer it automatically.

**18. What is the `lifecycle` block?**
It allows you to customize the lifecycle of a resource. Common arguments include `create_before_destroy`, `prevent_destroy`, and `ignore_changes`.

**19. Explain `create_before_destroy`.**
By default, Terraform destroys an old resource before creating a replacement. If set to `true`, Terraform will create the new replacement first, and only destroy the old one once the new one is running (Zero downtime).

**20. Explain `ignore_changes`.**
Tells Terraform to ignore future changes to specific resource attributes made outside of Terraform (e.g., ignoring tags that are managed by a separate auto-tagging system).

---

## 🟡 Category 2: State Management (21-40)

**21. What is the `terraform.tfstate` file?**
The "heart" of Terraform. It is a JSON file where Terraform maps your code configurations to real-world resources. It allows Terraform to know what it has already created.

**22. Why is storing the state file locally a bad practice?**
- **Collaboration:** Teammates will have out-of-sync state files.
- **Security:** The state file stores secrets (like passwords and private keys) in plain text. Pushing it to Git exposes these secrets.

**23. What is a Remote Backend?**
A remote backend (like AWS S3, Terraform Cloud, or Azure Blob) stores the state file centrally, enabling team collaboration and allowing the file to be encrypted at rest.

**24. What is State Locking?**
When multiple team members run `terraform apply` simultaneously, state locking prevents concurrent runs from corrupting the state file.

**25. How do you implement State Locking in AWS?**
By using an AWS DynamoDB table with a partition key named `LockID` alongside an S3 remote backend.

**26. What happens if you delete your state file?**
Terraform loses its memory. The next time you run `terraform apply`, it will attempt to recreate all resources from scratch, causing duplicates or errors.

**27. What is `terraform state list`?**
Lists all resources currently tracked in the state file.

**28. What is `terraform state show`?**
Shows the detailed attributes of a single resource tracked in the state file.

**29. What is `terraform state rm`?**
Removes a resource from the state file *without* destroying the actual infrastructure in the cloud. Useful if you want to stop managing a resource with Terraform.

**30. What is `terraform state mv`?**
Moves an item in Terraform state. Useful for renaming a resource in your code without forcing Terraform to destroy and recreate it.

**31. What is Terraform Drift?**
When the real-world infrastructure (in AWS) diverges from the configuration defined in your code and state file (e.g., someone manually edited a security group).

**32. How does Terraform detect drift?**
When you run `terraform plan`, Terraform silently performs a "refresh", comparing the state file to the actual cloud resources.

**33. How do you prevent Terraform Drift?**
Implement strict IAM policies giving users "Read-Only" access to the cloud console, forcing all changes to go through the Terraform CI/CD pipeline.

**34. What command manually updates the state file to match the real world?**
`terraform refresh` (Note: In modern Terraform, this is safely integrated into `terraform plan`).

**35. What is the `terraform import` command used for?**
To bring existing infrastructure (created manually or by another tool) under Terraform's management by mapping it to an empty resource block in your code.

**36. Explain the modern `import {}` block (Terraform 1.5+).**
Instead of using the CLI, you define an `import { id = "...", to = ... }` block in your code and run `terraform plan -generate-config-out`. Terraform will auto-generate the HCL code for you!

**37. Does Terraform import generate the HCL code automatically?**
Before version 1.5, no. You had to write the HCL manually. In version 1.5+, yes, using the `-generate-config-out` flag.

**38. What is `terraform taint`?**
It marks a resource as degraded or damaged. The next time `terraform apply` is run, Terraform will destroy and recreate the tainted resource. (Note: Deprecated in favor of `terraform apply -replace`).

**39. How do you untaint a resource?**
`terraform untaint <resource_name>`

**40. What is a state file backup?**
Terraform creates a `.terraform.tfstate.backup` file locally before making changes to the state, allowing you to rollback if the state becomes corrupted.

---

## 🟠 Category 3: Modules & Workspaces (41-60)

**41. What is a Terraform Module?**
A module is a container for multiple resources that are used together. It acts as a reusable blueprint/template.

**42. What is the Root Module?**
The working directory where you run `terraform apply`. Every Terraform configuration has at least one root module.

**43. What is a Child Module?**
A module that is called by another module (usually the root module) using the `module {}` block.

**44. Where should provider blocks be defined?**
Providers should *only* be defined in the Root Module, never in Child Modules. This keeps child modules generic and reusable across different regions.

**45. How do you pass data into a module?**
Using input variables defined in the child module's `variables.tf`.

**46. How do you extract data out of a module?**
Using output values defined in the child module's `outputs.tf`.

**47. What is the Terraform Registry?**
A public repository hosting thousands of pre-built, community-verified Terraform modules (e.g., a pre-built VPC module).

**48. Can you source a module directly from GitHub?**
Yes! `source = "github.com/hashicorp/example"`

**49. What is a Terraform Workspace?**
Workspaces allow you to maintain multiple, isolated state files from the exact same directory of Terraform code.

**50. What is the primary use case for Workspaces?**
Managing multiple environments (e.g., `dev`, `stage`, `prod`) without duplicating your `.tf` files.

**51. How do you create a new workspace?**
`terraform workspace new <name>`

**52. How do you switch workspaces?**
`terraform workspace select <name>`

**53. Where are local workspace state files stored?**
In a hidden directory named `terraform.tfstate.d/<workspace_name>/`.

**54. How can your code dynamically react to the current workspace?**
By using the built-in `terraform.workspace` variable combined with a map variable and the `lookup()` function.

**55. Explain the `lookup()` function.**
`lookup(map, key, default)` retrieves the value of a single element from a map given its key. If the key does not exist, it returns the default value.

**56. What is the difference between Workspaces and Git Branches?**
Workspaces manage different *state files* for different environments using the same code. Git branches manage different versions of the *code itself*.

**57. Should I use Workspaces for a massive enterprise production environment?**
HashiCorp recommends using separate directories (with tools like Terragrunt) for completely isolated production environments to reduce the blast radius, using workspaces mostly for testing/dev.

**58. What is a `dynamic` block?**
It acts like a `for` loop inside a resource. It is used to dynamically generate nested configuration blocks (like multiple `ingress` rules in a Security Group) based on a variable.

**59. What is the `concat()` function?**
Combines two or more lists into a single list.

**60. What is the `merge()` function?**
Combines two or more maps into a single map.

---

## 🔵 Category 4: Provisioners & Advanced Execution (61-80)

**61. What is a Provisioner in Terraform?**
Provisioners execute scripts on a local or remote machine as part of resource creation or destruction (e.g., installing software on an EC2 instance).

**62. What are the three main types of provisioners?**
`local-exec`, `remote-exec`, and `file`.

**63. What does `local-exec` do?**
Runs terminal commands on the machine running Terraform (your laptop or CI/CD runner).

**64. What does `remote-exec` do?**
Connects to a newly created resource (via SSH or WinRM) and runs commands on that remote machine.

**65. What does the `file` provisioner do?**
Copies files or directories from your local machine to the newly created remote resource.

**66. Why does HashiCorp say Provisioners are a "Last Resort"?**
Provisioners break the declarative nature of Terraform. If a script fails halfway, Terraform can't fix it. It is better to use Configuration Management tools (Ansible) or Cloud-Init/User-Data.

**67. What is a creation-time provisioner?**
Runs only during resource creation. If it fails, Terraform marks the resource as tainted.

**68. What is a destroy-time provisioner?**
Runs *before* the resource is destroyed. Useful for cleanup tasks. Requires `when = destroy`.

**69. What does `on_failure = continue` do in a provisioner?**
If the provisioner script fails, Terraform will ignore the error and continue applying the rest of the infrastructure, rather than tainting the resource.

**70. How do you pass a bash script to an EC2 instance without a provisioner?**
Use the `user_data` argument in the `aws_instance` resource. AWS will automatically run the script when the server boots.

**71. What is the difference between `user_data` and `remote-exec`?**
`user_data` is executed by cloud provider (AWS) upon first boot. `remote-exec` is executed by Terraform establishing an SSH connection *after* the boot.

**72. Explain the `zipmap()` function.**
Constructs a map from a list of keys and a corresponding list of values.

**73. Explain the `coalesce()` function.**
Takes any number of arguments and returns the first one that isn't null or an empty string.

**74. What is a Conditional Expression in Terraform?**
A ternary operator: `condition ? true_val : false_val`. E.g., `var.env == "prod" ? "t2.large" : "t2.micro"`.

**75. What is the `random` provider?**
Generates random values (strings, passwords, integers) that can be used to ensure unique naming conventions or generate secure passwords.

**76. What is the `archive` provider?**
Used to zip files dynamically (e.g., zipping a Python script to deploy to an AWS Lambda function).

**77. How do you view the execution graph of Terraform?**
`terraform graph`. It outputs a DOT format representation of the dependency graph which can be converted to an image using Graphviz.

**78. What does `terraform console` do?**
Opens an interactive command-line console where you can test interpolations, variables, and functions safely without affecting infrastructure.

**79. How do you enable detailed debug logging in Terraform?**
Set the environment variable `export TF_LOG=TRACE` (or DEBUG, INFO, WARN, ERROR).

**80. Where does Terraform save the debug log if you want a file?**
Set the `TF_LOG_PATH` environment variable (e.g., `export TF_LOG_PATH=terraform.log`).

---

## 🟣 Category 5: Security, Vault & Architecture (81-100)

**81. What is HashiCorp Vault?**
A centralized identity-based secrets and encryption management system.

**82. How does Terraform integrate with Vault?**
Using the `vault` provider and the `vault_generic_secret` (or `vault_kv_secret_v2`) data source to fetch secrets dynamically during `apply`.

**83. Why use Vault instead of passing passwords via `terraform.tfvars`?**
`.tfvars` files sit on your hard drive and can be accidentally pushed to Git. Vault ensures the password is never stored locally; it is fetched in memory during execution.

**84. What is AppRole in Vault?**
A machine-to-machine authentication mechanism. Instead of Terraform logging in with a human username/password, it logs in using a Role ID and Secret ID.

**85. If you use Vault, is the secret hidden from the Terraform State file?**
**No!** Even if fetched from Vault, the secret will be written to the `terraform.tfstate` file in plain text. You *must* use a secure, encrypted remote backend (like S3 with KMS).

**86. What is Terraform Cloud?**
HashiCorp’s managed SaaS offering that acts as a remote backend, runs Terraform executions in the cloud, and securely stores variables.

**87. What is Sentinel?**
Policy-as-Code framework integrated with Terraform Enterprise/Cloud. It can enforce rules (e.g., "Nobody is allowed to create EC2 instances larger than t2.micro") *before* `terraform apply` runs.

**88. What is Terragrunt?**
A popular third-party wrapper for Terraform that provides extra tools for keeping your configurations DRY (Don't Repeat Yourself), managing remote state perfectly, and working with multiple AWS accounts.

**89. Explain a typical Terraform CI/CD workflow.**
1. Developer pushes code to GitHub.
2. Pipeline runs `terraform fmt` and `terraform validate`.
3. Pipeline runs `terraform plan` and outputs the result as a PR comment.
4. Senior Engineer reviews PR and Plan.
5. Code is merged to `main`.
6. Pipeline runs `terraform apply -auto-approve` to deploy.

**90. How do you pass secrets to a CI/CD pipeline running Terraform?**
Store them as GitHub Secrets (or GitLab CI Variables) and map them to environment variables like `TF_VAR_db_password` or `AWS_ACCESS_KEY_ID`.

**91. What happens if an API call to AWS fails in the middle of `terraform apply`?**
Terraform updates the state file with whatever it *successfully* created up to that point. The failed resource and anything depending on it will not be created.

**92. How do you handle multiple AWS accounts (e.g., Dev Account, Prod Account) in Terraform?**
Use multiple AWS provider blocks and assign them an `alias`. You can then specify `provider = aws.dev` or `provider = aws.prod` inside your resources.

**93. What is a Terraform Plugin?**
Terraform itself is just a core engine. Plugins (Providers and Provisioners) are separate binaries that Terraform downloads during `init` to actually talk to APIs.

**94. What folder does `terraform init` create?**
`.terraform/`. This hidden directory stores the downloaded provider plugins and backend configurations.

**95. How do you upgrade the version of a provider?**
Update the version constraint in your `required_providers` block, then run `terraform init -upgrade`.

**96. What is a Partial Backend Configuration?**
Instead of hardcoding backend details (like the S3 bucket name) in `backend.tf`, you omit them and pass them securely via the CLI during init: `terraform init -backend-config="bucket=my-bucket"`.

**97. How can you deploy infrastructure across multiple AWS Regions at once?**
Define two `provider "aws"` blocks. Give one an alias (e.g., `alias = "west"` with `region = "us-west-1"`). Pass the alias to the resources you want in that region.

**98. What is the `.terraform.lock.hcl` file?**
Introduced in Terraform 0.14, it locks the exact versions of the provider plugins you are using. This ensures that your CI/CD pipeline doesn't accidentally download a newer, breaking version of a provider.

**99. How do you destroy just ONE specific resource instead of everything?**
`terraform destroy -target=aws_instance.example`

**100. How do you apply changes to just ONE specific resource?**
`terraform apply -target=aws_instance.example` (Note: HashiCorp warns to use `-target` sparingly, mostly for troubleshooting, as it breaks the full dependency graph).
