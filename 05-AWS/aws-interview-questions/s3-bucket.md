# Amazon S3 (Simple Storage Service) Interview Questions

Amazon S3 is the foundational storage service in AWS. These questions test your knowledge of storage tiers, data lifecycle management, security (encryption/policies), and performance optimization.

### 1. What is Amazon S3?
**Answer:** Amazon Simple Storage Service (Amazon S3) is a highly scalable, highly durable (11 9's) object storage service. It is designed to store and retrieve any amount of unstructured data (like images, backups, videos, or raw data lake files) from anywhere on the web using a simple REST API.

### 2. What are the key features of Amazon S3?
**Answer:** Key features include virtually infinite scalability, 99.999999999% durability, strong consistency for read-after-write operations, fine-grained access control (Bucket Policies/IAM), data encryption at rest and in transit, and intelligent storage tiering for cost optimization.

### 3. What is an S3 Bucket?
**Answer:** An S3 Bucket is a logical container for storing objects. Bucket names must be globally unique across all of AWS. Inside a bucket, each object is identified by a unique "Key" (the file path and name). Note that S3 has a flat structure; it does not have true hierarchical directories, though the UI simulates them using `/` prefixes.

### 4. How can you control access to objects in S3?
**Answer:** You control access using three main mechanisms:
1. **IAM Policies:** Attached to users/roles to dictate what they can do across AWS.
2. **Bucket Policies:** Attached directly to the bucket; used to grant cross-account access or enforce bucket-wide rules (like denying unencrypted uploads).
3. **ACLs (Access Control Lists):** Legacy mechanism applied at the object level (mostly disabled in modern AWS environments).

### 5. What is the difference between S3 Standard, S3 Intelligent-Tiering, and S3 One Zone-IA storage classes?
**Answer:** 
* **S3 Standard:** For frequently accessed data. High durability (3 AZs), high availability, highest storage cost, no retrieval fees.
* **S3 Intelligent-Tiering:** Uses machine learning to automatically move objects between frequent and infrequent access tiers to optimize costs without retrieval penalties.
* **S3 One Zone-IA (Infrequent Access):** Stores data in a *single* AZ. 20% cheaper than Standard-IA, but you lose the data if that specific AZ is destroyed.

### 6. How does S3 provide data durability?
**Answer:** By default (in standard storage classes), S3 provides 99.999999999% (11 9's) of durability by automatically and synchronously replicating your objects across at least three physical Availability Zones within the AWS region before returning a `200 OK` success message to the client.

### 7. What is Amazon S3 Glacier used for?
**Answer:** S3 Glacier is an extremely low-cost storage class specifically designed for long-term data archiving and digital preservation (e.g., keeping financial records for 7 years for compliance). Data stored in Glacier cannot be accessed instantly; retrieval times range from 1 minute (Expedited) to 12 hours (Bulk).

### 8. How can you secure data in Amazon S3?
**Answer:** 
* **In Transit:** Enforce HTTPS via Bucket Policies (checking for `"aws:SecureTransport": "true"`).
* **At Rest:** Enable Server-Side Encryption using Amazon S3-managed keys (SSE-S3) or AWS KMS-managed keys (SSE-KMS).
* **Immutability:** Use **S3 Object Lock** (WORM model - Write Once, Read Many) to prevent hackers or ransomware from deleting backups.

### 9. What is S3 Versioning?
**Answer:** S3 Versioning keeps multiple variants of an object in the same bucket. If a user accidentally deletes `file.txt` or overwrites it with bad data, S3 retains the previous versions. Deleting a file simply places a "Delete Marker" over it, allowing you to easily restore the file. (Note: Versioning increases costs since you pay for all versions).

### 10. What is a Pre-Signed URL in S3?
**Answer:** By default, all S3 objects are private. A Pre-Signed URL is a dynamically generated URL (created using AWS SDKs/IAM credentials) that grants temporary, time-bound access (e.g., valid for 15 minutes) to download or upload a specific object without requiring the user to have AWS credentials.

### 11. How can you optimize costs in Amazon S3?
**Answer:** You use **S3 Lifecycle Policies**. For example, you can create a rule that says: "Keep data in S3 Standard for 30 days. After 30 days, move it to S3 Standard-IA (cheaper storage). After 365 days, archive it to S3 Glacier Deep Archive (cheapest storage). After 7 years, permanently delete it."

### 12. What is S3 Cross-Region Replication (CRR)?
**Answer:** CRR automatically and asynchronously copies objects uploaded to a source bucket in one region (e.g., US-East) to a destination bucket in another region (e.g., EU-West). It is heavily used for disaster recovery, compliance (keeping data separated geographically), and reducing latency for global users. (Requires Versioning to be enabled).

### 13. How can you automate the movement of objects between different storage classes?
**Answer:** You automate this entirely using **S3 Lifecycle Rules**. You define a prefix (e.g., `logs/`) and configure transition actions based on the age of the object (e.g., Transition to Glacier after 90 days).

### 14. What is the purpose of S3 Event Notifications?
**Answer:** S3 Event Notifications are the backbone of event-driven architectures. You can configure a bucket to automatically trigger an AWS Lambda function, send a message to an SQS queue, or publish to an SNS topic the exact moment a specific event occurs (like `s3:ObjectCreated:Put`).

### 15. What is the AWS Snowball device?
**Answer:** AWS Snowball is a ruggedized, physical data transport briefcase sent to your corporate office by AWS. If you need to migrate 50 Terabytes of data to S3, doing it over the internet could take months. You copy the data locally to the Snowball via your LAN, ship it back to AWS, and they plug it directly into S3, completing the migration in days.

### 16. What is Amazon S3 Select?
**Answer:** Normally, if you need one specific row of data from a 5GB CSV file in S3, you have to download the entire 5GB file. **S3 Select** allows you to push simple SQL-like queries (`SELECT * FROM S3Object WHERE Name='John'`) directly to the S3 infrastructure. S3 filters the data on the backend and only returns the matching 5KB of data, massively saving bandwidth and compute time.

### 17. What is the difference between Amazon S3 and Amazon EBS?
**Answer:** 
* **S3 (Object Storage):** Serverless, infinite capacity, accessed over the internet via HTTP/REST APIs. Ideal for files and backups. You cannot run an OS on it.
* **EBS (Block Storage):** A physical/virtual hard drive that must be attached to a specific running EC2 instance via the local network. Ideal for databases and Operating Systems.

### 18. How can you enable server access logging in Amazon S3?
**Answer:** You enable **S3 Server Access Logging** in the bucket properties and specify a different target S3 bucket to receive the logs. AWS will deliver text files containing details of every single API request (IP address, IAM user, object requested, timestamp) made against the bucket, which is crucial for security audits.

### 19. What is S3 Transfer Acceleration?
**Answer:** If you have users in Australia trying to upload large files to an S3 bucket in Virginia, internet routing can be slow and unreliable. S3 Transfer Acceleration routes the user's upload to the closest **Amazon CloudFront Edge Location** in Australia, and then routes the data over AWS's optimized, dedicated global network backbone to Virginia, drastically increasing upload speeds.

### 20. How can you replicate data between S3 buckets within the same region?
**Answer:** You use **Same-Region Replication (SRR)**. Similar to CRR, SRR automatically replicates objects between buckets in the same region. It is typically used to aggregate logs from multiple different AWS accounts into a single centralized compliance bucket within the same region.
