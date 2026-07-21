# Day 6: AWS CLI & Infrastructure as Code - Interview Questions

These questions test your practical knowledge of the terminal, authentication, and the core philosophies of DevOps automation.

---

### Q1: What does the error "UNPROTECTED PRIVATE KEY FILE" mean when trying to SSH, and how do you fix it?
**Interview Answer:**  
"That error occurs when your SSH Private Key (`.pem` file) has file permissions that are too open, meaning other users on the system could potentially read it. SSH strictly enforces security and will refuse to use an exposed key. To fix it on a Linux or Mac system, you run the command `chmod 600` on the key file, which restricts read and write permissions strictly to the owner."

---

### Q2: What is the AWS CLI and why is it preferred over the AWS Management Console?
**Interview Answer:**  
"The AWS CLI is a command-line tool that lets you interact with AWS services via your terminal. It is highly preferred over the web console because it allows DevOps engineers to manage resources faster, automate repetitive tasks by writing shell scripts, and manage bulk operations (like querying hundreds of resources) that would be too slow to do manually in the browser."

---

### Q3: How do you authenticate the AWS CLI on your local machine?
**Interview Answer:**  
"To authenticate the CLI, I first generate an Access Key ID and a Secret Access Key from the IAM Security Credentials section in the AWS Console. Then, I run the command `aws configure` in my terminal and input the Access Key, Secret Key, my preferred default Region, and the default output format (usually JSON). This securely stores the credentials on my local machine to sign future API requests."

---

### Q4: Why must you keep your AWS Secret Access Key secure?
**Interview Answer:**  
"Your Secret Access Key provides programmatic access to your entire AWS account based on your IAM permissions. If it is leaked-for instance, accidentally pushed to a public GitHub repository-malicious actors can use it to launch thousands of crypto-mining EC2 instances, racking up massive bills in a matter of hours. If a key is ever exposed, it must be instantly deactivated and deleted in IAM."

---

### Q5: What is Infrastructure as Code (IaC)?
**Interview Answer:**  
"Infrastructure as Code is the practice of managing and provisioning computing infrastructure through machine-readable definition files, rather than through physical hardware configuration or interactive configuration tools. Instead of clicking through a cloud console, I write code (like Terraform or CloudFormation templates) that describes the desired state of my infrastructure. This ensures deployments are version-controlled, repeatable, and automated."

---

### Q6: What is the difference between AWS CloudFormation and Terraform?
**Interview Answer:**  
"Both are Infrastructure as Code tools, but CloudFormation is a proprietary service native to AWS and is written in YAML or JSON. Terraform is an open-source tool created by HashiCorp that uses HCL (HashiCorp Configuration Language). The major advantage of Terraform is that it is cloud-agnostic, meaning you can use the same workflow to manage resources across AWS, Azure, Google Cloud, and many other providers."

---

### Q7: What is Boto3?
**Interview Answer:**  
"Boto3 is the official AWS Software Development Kit (SDK) for Python. It allows Python developers to write scripts that interact directly with the AWS APIs to programmatically create, configure, and manage AWS services like EC2 and S3."

---

### Q8: When you run `aws configure`, where does the AWS CLI store your credentials locally?
**Interview Answer:**  
"When you authenticate using `aws configure`, the CLI creates a hidden `.aws` directory in your user's home folder. The Access Key and Secret Access Key are stored in plain text inside the `~/.aws/credentials` file, while the default region and output format are stored in the `~/.aws/config` file."

---

### Q9: How do you manage multiple AWS accounts using the AWS CLI on the same machine?
**Interview Answer:**  
"To manage multiple AWS accounts, you use Named Profiles. Instead of running the standard `aws configure` which overwrites the default profile, you run `aws configure --profile <profile-name>`. Then, whenever you execute a CLI command intended for that specific account, you append the `--profile <profile-name>` flag to the command. This ensures the CLI uses the correct set of credentials from the `~/.aws/credentials` file."

---

### Q10: If an application running on an EC2 instance needs to use the AWS CLI to access an S3 bucket, should you run `aws configure` on the server?
**Interview Answer:**  
"No, absolutely not. Hardcoding Access Keys on an EC2 instance is a massive security risk because if the server is compromised, the keys are compromised. Instead, you should create an IAM Role with the necessary S3 permissions and attach that role directly to the EC2 instance. The AWS CLI running on the instance will automatically inherit the temporary, secure credentials provided by the IAM Role without needing any hardcoded keys."


---
**[Next: Day 7 - Linux Questions](./Day-07-Linux-Questions.md)**
