# Amazon EC2 (Elastic Compute Cloud) Interview Questions

Amazon EC2 is the foundational compute service in AWS. These questions test your knowledge of instance lifecycles, storage types (EBS vs Instance Store), and high availability.

### 1. What is Amazon EC2?
**Answer:** Amazon Elastic Compute Cloud (Amazon EC2) is a core web service that provides secure, resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers by allowing them to provision virtual servers (instances) in minutes rather than waiting weeks for physical hardware.

### 2. How does Amazon EC2 work?
**Answer:** Under the hood, AWS uses the Nitro System (a combination of custom hardware and a lightweight hypervisor) to slice massive physical servers into secure Virtual Machines. You launch these instances inside a Virtual Private Cloud (VPC), boot them using an Amazon Machine Image (AMI), and attach Elastic Block Store (EBS) volumes for persistent storage.

### 3. What are the different instance families in EC2?
**Answer:** EC2 instances are grouped into families optimized for specific use cases:
* **General Purpose (e.g., T3, M5):** Balanced CPU/Memory for web servers.
* **Compute Optimized (e.g., C5, C6g):** High CPU for batch processing or scientific modeling.
* **Memory Optimized (e.g., R5, X1):** Massive RAM for in-memory databases like Redis or SAP HANA.
* **Accelerated Computing (e.g., P3, G4):** GPUs for Machine Learning and 3D rendering.

### 4. Explain the differences between On-Demand, Reserved, and Spot instances.
**Answer:** 
* **On-Demand:** Pay by the second with no upfront commitment. Most expensive, but most flexible.
* **Reserved/Savings Plans:** You commit to 1 or 3 years of usage in exchange for massive discounts (up to 72%). Best for steady-state databases.
* **Spot Instances:** You bid on spare, unused AWS capacity at up to 90% off. However, AWS can reclaim the instance with only a 2-minute warning. Best for stateless, fault-tolerant workloads like CI/CD runners or batch processing.

### 5. How can you improve the availability of EC2 instances?
**Answer:** A single EC2 instance is a single point of failure. To achieve high availability, you must deploy multiple EC2 instances across at least two physically isolated **Availability Zones (AZs)** within a region, and place an Elastic Load Balancer (ELB) in front of them to distribute the traffic.

### 6. What is an Amazon Machine Image (AMI)?
**Answer:** An AMI is a read-only template used to boot an EC2 instance. It contains the operating system (e.g., Amazon Linux 2023, Ubuntu, Windows Server), the architecture type (x86 vs ARM), and any pre-installed application software or configuration settings needed to run your workload immediately upon boot.

### 7. How can you secure your EC2 instances?
**Answer:** 
1. Use **Security Groups** to tightly restrict inbound port access (e.g., only allow port 443 from the internet).
2. Use **IAM Roles** attached via Instance Profiles instead of hardcoding AWS access keys.
3. Keep instances in **Private Subnets** (no public IP) and access them securely using AWS Systems Manager (SSM) Session Manager instead of opening SSH (port 22).

### 8. Explain the difference between a Public IP and an Elastic IP in EC2.
**Answer:** A standard Public IP is ephemeral; if you Stop and Start your EC2 instance, the Public IP will change, breaking any DNS records pointing to it. An **Elastic IP (EIP)** is a static, dedicated IPv4 address that you own and attach to an instance. It remains the same even if the underlying instance is stopped, started, or completely replaced.

### 9. How can you scale your application using EC2?
**Answer:** 
* **Vertical Scaling:** Stopping the instance and changing the instance type (e.g., moving from a `t3.micro` to an `m5.large`). Causes downtime.
* **Horizontal Scaling:** Adding *more* instances to handle the load using an **Amazon EC2 Auto Scaling Group (ASG)**. This is the cloud-native approach and causes zero downtime.

### 10. What is Amazon EBS?
**Answer:** Amazon Elastic Block Store (EBS) is a highly available, persistent block storage service. Think of it as a cloud-based external hard drive. An EBS volume exists independently of the EC2 instance's lifecycle, meaning if the EC2 instance is terminated, the data on the EBS volume can be preserved and attached to a new instance.

### 11. How can you encrypt data on EBS volumes?
**Answer:** You can enable EBS encryption at creation time. AWS uses the **Key Management Service (KMS)** to encrypt the data at rest, data in transit between the EC2 instance and the EBS volume, and all snapshots created from the volume, ensuring strict compliance with security standards.

### 12. How can you back up your EC2 instances?
**Answer:** You create **EBS Snapshots**. A snapshot is an incremental backup of your EBS volume stored securely in Amazon S3. For automation, you should use **Amazon Data Lifecycle Manager (DLM)** or **AWS Backup** to automatically take daily snapshots and delete them after 30 days to save costs.

### 13. What is the difference between Instance Store and EBS-backed instances?
**Answer:** 
* **EBS-Backed:** Storage is persistent and decoupled via the network. If the instance stops, data is saved.
* **Instance Store:** Storage consists of physical NVMe SSDs directly attached to the physical host server. It offers extreme I/O performance (millions of IOPS), but it is **ephemeral**. If the instance stops or the underlying hardware fails, the data is permanently lost.

### 14. What are Instance Metadata and User Data in EC2?
**Answer:** 
* **User Data:** A bootstrap bash or PowerShell script you provide when launching an instance to automate software installations (e.g., `yum install httpd`) upon the very first boot.
* **Instance Metadata (IMDS):** An internal AWS API available at `169.254.169.254`. Applications running on the instance can query this IP to retrieve their own Instance ID, private IP, or temporary IAM credentials.

### 15. How can you launch instances in a Virtual Private Cloud (VPC)?
**Answer:** When launching an EC2 instance, you must explicitly specify the Target VPC and the specific Subnet (Public or Private) you want the instance to reside in. This places the instance into a logically isolated network environment, allowing you to control internet routing via Route Tables and NAT Gateways.

### 16. What is the purpose of an EC2 Security Group?
**Answer:** A Security Group acts as a stateful virtual firewall applied directly at the ENI (Elastic Network Interface) level of the EC2 instance. By default, it blocks all inbound traffic and allows all outbound traffic. You must explicitly write "Allow" rules for specific ports and source IPs (e.g., Allow TCP 80 from `0.0.0.0/0`).

### 17. How can you automate the deployment of EC2 instances?
**Answer:** In modern DevOps, you never launch EC2 instances manually via the console. Instead, you define the instance properties (AMI, Subnet, Security Group, User Data) in Infrastructure as Code (IaC) templates using **AWS CloudFormation** or **HashiCorp Terraform**, allowing you to deploy identically configured servers in seconds.

### 18. How can you achieve high availability for an application using EC2?
**Answer:** You create an **Auto Scaling Group (ASG)** that spans three Availability Zones. You set a minimum capacity of 3 instances. You then place an **Application Load Balancer (ALB)** in front of the ASG. The ALB routes user traffic to the healthy instances, and if one instance crashes, the ASG automatically provisions a replacement in a healthy AZ.

### 19. What is Amazon Machine Learning (Amazon ML) / SageMaker in relation to EC2?
**Answer:** While Amazon ML is deprecated in favor of **Amazon SageMaker**, modern ML workloads rely heavily on specialized EC2 instances. You use Accelerated Computing instances (like the `P4d` instances which feature multiple NVIDIA GPUs) to drastically reduce the time it takes to train massive Deep Learning models.

### 20. What is Amazon EC2 Instance Connect (or SSM Session Manager)?
**Answer:** EC2 Instance Connect and **AWS Systems Manager (SSM) Session Manager** provide secure shell access to your instances through the browser or AWS CLI without needing to manage public SSH keys (`.pem` files) or open inbound port 22 in your security groups. Access is securely audited and controlled strictly via AWS IAM policies.
