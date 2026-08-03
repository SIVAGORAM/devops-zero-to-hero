# Day 21: Top 15 AWS Services for DevOps Engineers

As a DevOps Engineer, you do not need to memorize all 200+ AWS services. Instead, you need to deeply understand the core services related to Compute, Networking, Storage, Security, Monitoring, and CI/CD. 

Here is the definitive list of what you must master:

---

## 1. Compute & Containers

*These services run your applications and code.*

- **EC2 (Elastic Compute Cloud):** Virtual machines in the cloud. The foundation of Infrastructure as a Service (IaaS). You manage the OS, updates, and scaling.
- **Lambda:** Serverless compute. You just upload your code (Python, Node.js, etc.) and AWS runs it without you ever managing a server. Perfect for event-driven automation scripts.
- **AWS EKS (Elastic Kubernetes Service):** AWS’s managed Kubernetes service. It is the industry standard for orchestrating and managing thousands of Docker containers.
- **AWS Fargate:** A serverless compute engine specifically for containers. If you use Fargate with EKS or ECS, you don't have to provision or manage the underlying EC2 instances—AWS handles the hardware scaling automatically.

### 💡 Interview Question: What is the difference between ECS and EKS?
- **ECS (Elastic Container Service):** AWS's proprietary container orchestration tool. It is simpler to set up, highly integrated with other AWS services, and has a lower learning curve.
- **EKS (Elastic Kubernetes Service):** Uses open-source Kubernetes. It is more complex and requires more management overhead, but it prevents vendor lock-in. If you build for EKS, you can easily migrate to Google Cloud (GKE) or Azure (AKS) later.

---

## 2. Networking

*These services manage how your servers communicate with each other and the internet.*

- **VPC (Virtual Private Cloud):** Your private, secure, and isolated network inside the AWS cloud. Everything you build lives inside a VPC.
  - **CIDR (Classless Inter-Domain Routing):** The IP address block assigned to your VPC (e.g., `10.0.0.0/16`), defining how many IP addresses your network has.
  - **Security Groups:** Instance-level firewalls. 
  - **Inbound / Outbound Rules:** You use these rules inside Security Groups to dictate exactly what traffic can enter (Inbound) or leave (Outbound) your servers.

---

## 3. Storage

*Where your data, OS, and backups live.*

- **EBS (Elastic Block Store):** Virtual hard drives attached directly to your EC2 instances. You install your Operating System and databases on EBS volumes.
- **S3 (Simple Storage Service):** Infinite, scalable object storage. You cannot run an OS on S3. It is used for storing backups, images, logs, CI/CD artifacts, and hosting static frontend websites.

---

## 4. Security & Auditing

*These services protect your infrastructure from hackers and internal mistakes.*

- **IAM (Identity and Access Management):** The absolute core of AWS security. It controls *who* can access *what*. You manage Users, Groups, Roles, and Policies here.
- **AWS KMS (Key Management Service):** Used to create and manage cryptographic keys. You use KMS to encrypt your EBS volumes, S3 buckets, and database passwords to protect them from theft.
- **CloudTrail:** The ultimate auditor. It records every single API call made in your AWS account. If a server is suddenly deleted, you check CloudTrail to see exactly which user deleted it and at what time.

---

## 5. Monitoring & Compliance

*These services keep your systems healthy and compliant.*

- **CloudWatch:** The monitoring service. It tracks performance metrics (CPU, Memory, Network) and collects application logs. You use it to trigger automated alarms (e.g., "Send an email if CPU > 80%").
- **AWS Config:** Continuously monitors and records your AWS resource configurations. It acts as a compliance checker (e.g., "Alert me if an S3 bucket is accidentally made public").
- **ELK Stack (Elasticsearch, Logstash, Kibana):** While not exclusively an AWS service (AWS offers it as managed *OpenSearch*), ELK is the industry standard open-source stack for centralizing, searching, and visualizing massive amounts of log data from your servers.

---

## 6. CI/CD & Developer Tools

*These services automate how your code gets from a developer's laptop to production.*

- **Cloud Build Services (AWS Code Suite):** AWS's alternative to tools like Jenkins or GitLab CI.
  - **AWS CodePipeline:** The orchestrator that manages the visual workflow from code commit to deployment.
  - **AWS CodeBuild:** The build server. It compiles source code, runs unit tests, and produces ready-to-deploy software packages.
  - **AWS CodeDeploy:** Automates the deployment of your application code to EC2 instances, Fargate, or Lambda.

---

## 7. Cost Management

*Because cloud bills can spiral out of control.*

- **Billing and Costing (AWS Cost Explorer):** As a DevOps engineer, you are often responsible for optimizing cloud architecture to save money. You must understand how to track spending, set budgets, and use cost anomaly detection.

---
**[Previous: Deploy App to AWS](./Day-20-Deploy-First-App-to-AWS.md)**
