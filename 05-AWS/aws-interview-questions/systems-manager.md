# AWS Systems Manager Interview Questions

AWS Systems Manager (SSM) is the operational hub for AWS. These questions test your ability to manage fleets of instances at scale, execute remote commands securely, and store application secrets.

### 1. What is AWS Systems Manager?
**Answer:** AWS Systems Manager is an operational management service that provides a unified user interface so you can view operational data from multiple AWS services and automate operational tasks across your AWS resources and on-premises servers at massive scale.

### 2. What are some key components of AWS Systems Manager?
**Answer:** The suite includes:
* **Session Manager:** Secure shell access.
* **Run Command:** Remote script execution.
* **Parameter Store:** Configuration and secret management.
* **Patch Manager:** Automated OS patching.
* **Automation:** Complex operational workflow execution.
* **State Manager:** Configuration drift management.

### 3. What is the purpose of AWS Systems Manager Parameter Store?
**Answer:** Parameter Store is a secure, hierarchical storage service used for configuration data and secrets management. Instead of hardcoding API keys, database strings, or standard AMI IDs in your code, you store them as `String` or `SecureString` (encrypted via KMS) parameters. Applications dynamically fetch these values at runtime.

### 4. How can you use Run Command in AWS Systems Manager?
**Answer:** Run Command allows you to remotely and securely execute bash/PowerShell scripts on dozens or thousands of EC2 instances simultaneously without needing SSH access or bastion hosts. For example, you can use Run Command to instantly update a specific software package across an entire fleet of 500 servers.

### 5. What is State Manager in AWS Systems Manager?
**Answer:** State Manager is a configuration management service that ensures your EC2 instances (or on-premises servers) consistently remain in their intended state. You define a desired state (e.g., "The AWS CloudWatch Agent must be installed and running, and port 22 must be closed"). State Manager continuously monitors the fleet and automatically remediates any drift.

### 6. How does Automation work in AWS Systems Manager?
**Answer:** Automation uses JSON/YAML documents (Runbooks) to execute complex IT workflows. For example, you can build an Automation Runbook to safely patch an AMI: it launches an EC2 instance from an old AMI, installs OS updates, stops the instance, creates a new golden AMI, and deletes the temporary instance—all entirely automated.

### 7. What is Patch Manager in AWS Systems Manager?
**Answer:** Patch Manager automates the process of patching both Windows and Linux instances with the latest security updates. You define "Patch Baselines" (e.g., "Auto-approve critical security patches 7 days after release"). Patch Manager uses SSM Maintenance Windows to orchestrate the rolling installation of these patches across your fleet without causing widespread downtime.

### 8. How can you manage inventory using AWS Systems Manager?
**Answer:** Systems Manager Inventory collects deep metadata from your managed instances, such as installed software applications, OS versions, network configurations, and missing patches. You can use Amazon Athena to query this inventory data globally to prove compliance during software audits.

### 9. What is the difference between Systems Manager Parameter Store and AWS Secrets Manager?
**Answer:** 
* **Parameter Store:** Mostly free, handles standard configuration data and basic secrets (`SecureString`).
* **Secrets Manager:** More expensive, explicitly designed for secrets. Its major advantage is that it supports **Automatic Secret Rotation** via Lambda (e.g., it can automatically change your RDS database password every 30 days without human intervention).

### 10. How can you use AWS Systems Manager to automate instance configuration?
**Answer:** When launching EC2 instances via CloudFormation or Terraform, you can configure them to automatically attach to a Systems Manager **State Manager Association**. As soon as the instance boots, the SSM Agent pulls the configuration document and enforces the baseline (like joining an Active Directory domain or installing antivirus software).

### 11. What are AWS Systems Manager Documents?
**Answer:** SSM Documents are JSON or YAML files that define the actions that Systems Manager performs on your managed instances. There are different types: `Command` documents (for Run Command), `Automation` runbooks, and `Policy` documents (for State Manager).

### 12. How can you schedule automated tasks with AWS Systems Manager?
**Answer:** You use **SSM Maintenance Windows**. You define a schedule (e.g., "Every Saturday at 2 AM"), set a duration (e.g., "4 hours"), and assign tasks (like Patch Manager updates or Run Command scripts) to specific target groups of instances (using AWS Tags). This ensures disruptive maintenance only happens during approved hours.

### 13. What is the purpose of Distributor in AWS Systems Manager?
**Answer:** Distributor helps you package and publish your own software (or third-party agents like Datadog or CrowdStrike) to your AWS environment. State Manager then uses Distributor to ensure that this specific software package is installed and kept up-to-date across your entire fleet of instances.

### 14. How can you use AWS Systems Manager to manage compliance?
**Answer:** Systems Manager Compliance aggregates data from Patch Manager and State Manager. It provides a single dashboard to show exactly which instances are non-compliant (e.g., missing critical CVE patches, or missing mandatory antivirus software) allowing security teams to quickly identify and quarantine vulnerable servers.

### 15. What is the OpsCenter feature in AWS Systems Manager?
**Answer:** OpsCenter provides a central location where operations engineers can view, investigate, and resolve operational issues (OpsItems). For example, if a CloudWatch Alarm triggers for high disk space, it creates an OpsItem in OpsCenter, pulling in related runbooks, logs, and instance data so the engineer can resolve the issue immediately.

### 16. How can you integrate AWS Systems Manager with other AWS services?
**Answer:** SSM is highly integrated. It uses **IAM** for access control, sends all execution logs to **CloudWatch Logs** and **S3**, triggers alerts via **Amazon SNS**, and can trigger complex workflows using **EventBridge** and **AWS Lambda**.

### 17. Can AWS Systems Manager be used with on-premises resources?
**Answer:** Yes! This is a massive feature. You can install the **SSM Agent** on your physical on-premises servers (or VMs in Azure/GCP). You register them as "Managed Instances" in AWS. You can then use Run Command, Patch Manager, and Session Manager on your physical corporate servers using the exact same AWS console you use for EC2.

### 18. How does AWS Systems Manager help with troubleshooting?
**Answer:** It eliminates the need for jump-boxes and SSH keys. If an application crashes, an engineer can use **Session Manager** to get an instant, secure, browser-based terminal into the EC2 instance to investigate logs. All terminal commands typed by the engineer are fully audited and recorded in CloudWatch for security review.

### 19. What is the Session Manager feature in AWS Systems Manager?
**Answer:** Session Manager provides secure and auditable interactive shell (bash/PowerShell) access to EC2 instances and on-premises servers. It **does not require open inbound ports (like Port 22 for SSH)**, bastion hosts, or managing SSH keys, massively improving the security posture of your AWS environment.

### 20. How can you secure data stored in AWS Systems Manager Parameter Store?
**Answer:** You store sensitive data as a `SecureString`. Parameter Store automatically integrates with **AWS Key Management Service (KMS)** to encrypt the value at rest. Furthermore, you use strict IAM policies to ensure that only specific IAM Roles (e.g., a specific ECS Task) have the `ssm:GetParameter` and `kms:Decrypt` permissions required to read the secret.
