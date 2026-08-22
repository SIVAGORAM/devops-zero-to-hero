# Amazon EFS & FSx (File Storage) Interview Questions

Block storage (EBS) and Object storage (S3) aren't always enough. These questions test your knowledge of highly available, shared Network File Systems.

### 1. What is Amazon EFS?
**Answer:** Amazon Elastic File System (EFS) is a fully managed, scalable, and highly available NFS (Network File System) file system for use with AWS Cloud services and on-premises resources. It is built to scale on demand to petabytes without disrupting applications.

### 2. What is the difference between EBS, S3, and EFS?
**Answer:** 
* **EBS (Block):** A single hard drive that can only be attached to **one** EC2 instance at a time (mostly).
* **S3 (Object):** Accessed via HTTP API, not a traditional file system. Best for backups and static web hosting.
* **EFS (File):** A shared network drive. It can be mounted concurrently to **thousands** of EC2 instances, allowing them all to read and write to the exact same files simultaneously.

### 3. Does EFS span multiple Availability Zones?
**Answer:** Yes. Unlike EBS, which is strictly tied to a single Availability Zone, EFS is highly available and durably stores data redundantly across multiple Availability Zones in a region by default (unless using EFS One Zone).

### 4. How do EC2 instances access EFS?
**Answer:** EFS uses the standard **NFSv4.1** protocol. EC2 instances must be running a Linux OS (EFS does not natively support Windows) and use the standard Linux `mount` command to attach the file system.

### 5. What are the two Performance Modes in EFS?
**Answer:** 
* **General Purpose (Default):** Ideal for latency-sensitive use cases, like web serving environments and CMS (like WordPress).
* **Max I/O:** Scales to higher levels of aggregate throughput and IOPS, but with slightly higher latencies. Ideal for highly parallelized big data analytics or media processing.

### 6. What is Amazon FSx?
**Answer:** While EFS is an NFS system primarily for Linux, Amazon FSx provides fully managed third-party file systems with the native compatibility and feature sets of those systems.

### 7. What is Amazon FSx for Windows File Server?
**Answer:** It provides fully managed, highly reliable, and scalable file storage that is accessible over the industry-standard **SMB** protocol. It natively integrates with Microsoft Active Directory, making it the perfect solution for migrating legacy Windows corporate file shares to AWS.

### 8. What is Amazon FSx for Lustre?
**Answer:** Lustre is the world's most popular high-performance file system. FSx for Lustre is designed for applications that require extreme speeds (sub-millisecond latencies, millions of IOPS) such as High-Performance Computing (HPC), machine learning, and video rendering. It natively links to an S3 bucket to quickly load and save massive datasets.

### 9. Can AWS Lambda access Amazon EFS?
**Answer:** Yes. You can mount an EFS file system directly to a Lambda function. This is critical for Serverless applications that need to process large files (larger than Lambda's 10 GB ephemeral storage limit) or when multiple Lambda functions need to share state securely.

### 10. How do you secure data at rest and in transit for Amazon EFS?
**Answer:** You enable encryption at rest using AWS KMS when creating the file system. You enable encryption in transit by using the EFS Mount Helper utility, which automatically establishes an encrypted TLS tunnel between the EC2 instance and the EFS mount target.
