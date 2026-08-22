# AWS KMS & Secrets Management Interview Questions

Data security, encryption at rest, and secret management are top priorities in enterprise DevOps. These questions test your knowledge of symmetric keys, envelope encryption, and IAM integration.

### 1. What is AWS Key Management Service (KMS)?
**Answer:** AWS KMS is a managed service that makes it easy to create, manage, and control the cryptographic keys used to encrypt your data across AWS. It uses Hardware Security Modules (HSMs) validated by FIPS 140-2 to protect the physical security of your keys.

### 2. What is a Customer Master Key (CMK)?
**Answer:** A Customer Master Key (now simply called a KMS Key) is the primary resource in KMS. It can be AWS-managed or Customer-managed. The CMK never actually leaves the KMS service unencrypted; all cryptographic operations using the CMK occur strictly within the KMS hardware.

### 3. What is Envelope Encryption?
**Answer:** KMS keys can only encrypt a maximum of 4 KB of data. To encrypt a 50 GB database, AWS uses Envelope Encryption. KMS generates a plaintext **Data Key** to encrypt the 50 GB file locally. It then uses the CMK to encrypt the Data Key. The encrypted Data Key is stored alongside the encrypted file (like an envelope).

### 4. What is the difference between AWS-Managed Keys and Customer-Managed Keys?
**Answer:** 
* **AWS-Managed Keys:** Created automatically by AWS (e.g., `aws/s3`). They are free, but you cannot manage their rotation schedule or strict access policies.
* **Customer-Managed Keys:** Created by you. Cost $1/month. You have absolute control over the Key Policy, key rotation, and cross-account access.

### 5. What is a KMS Key Policy?
**Answer:** Similar to an S3 Bucket Policy, a Key Policy is a resource-based JSON policy attached directly to the KMS Key. It defines exactly which IAM users or Roles are allowed to manage the key (administrative actions) and which are allowed to use the key (`kms:Encrypt`, `kms:Decrypt`).

### 6. Can an IAM user use a KMS key if the Key Policy explicitly denies them?
**Answer:** No. In KMS, the Key Policy is the absolute source of truth. Even if an IAM user has `AdministratorAccess` on their IAM policy, if the KMS Key Policy does not explicitly grant them access (or explicitly denies them), they cannot use or delete the key.

### 7. How does KMS Key Rotation work?
**Answer:** For Customer-Managed Keys, you can enable automatic key rotation. Once a year, KMS automatically generates new cryptographic material for the key. Old data remains decryptable using the old material, but new data is encrypted with the new material. This requires zero application code changes.

### 8. What is the `kms:GenerateDataKey` API call?
**Answer:** When an application needs to encrypt a large payload locally, it calls this API. KMS returns two things: a plaintext Data Key (to encrypt the payload) and a cipher-text Data Key (encrypted by the CMK). The application encrypts the data, throws away the plaintext key, and stores the cipher-text key next to the data.

### 9. What is the AWS Secrets Manager?
**Answer:** AWS Secrets Manager is a service designed to securely store, retrieve, and rotate sensitive database credentials, API keys, and OAuth tokens. It integrates tightly with KMS to encrypt the secrets at rest.

### 10. What is the main advantage of Secrets Manager over SSM Parameter Store?
**Answer:** The defining feature of Secrets Manager is **Automatic Secret Rotation**. It can natively integrate with an AWS Lambda function to connect to an RDS database, generate a brand new complex password, update the database, and update the secret in Secrets Manager—all automatically on a schedule (e.g., every 30 days) with zero downtime.

### 11. How do you securely pass a database password to an ECS Docker container?
**Answer:** You never hardcode it in the Dockerfile. You store the password in Secrets Manager. In the ECS Task Definition, you reference the Secret ARN. When the container starts, the ECS Agent automatically decrypts the secret and injects it into the running container as an Environment Variable.

### 12. What happens if you accidentally delete a Customer Managed KMS Key?
**Answer:** Because deleting a key means all data encrypted by it is lost forever (cryptoshredding), AWS enforces a mandatory waiting period. When you delete a key, it enters a "Pending Deletion" state for a minimum of 7 days up to 30 days. You can cancel the deletion at any time during this window.

### 13. What is Asymmetric Encryption in AWS KMS?
**Answer:** While KMS primarily uses Symmetric keys (one key encrypts and decrypts), it also supports Asymmetric keys (RSA or Elliptic Curve). These provide a public key (which can be distributed anywhere to encrypt data) and a private key (which never leaves KMS, used to decrypt data or sign digital signatures).

### 14. How can you share a KMS key across different AWS Accounts?
**Answer:** You must use a Customer-Managed Key. You update the Key Policy in Account A to explicitly allow the IAM Root user of Account B to use the key. Then, in Account B, you create an IAM Policy granting specific users the `kms:Decrypt` action against the specific Key ARN in Account A.

### 15. What is AWS CloudHSM and how does it differ from KMS?
**Answer:** CloudHSM provides dedicated Hardware Security Modules in the cloud. With KMS, you share a multi-tenant hardware pool managed by AWS. With CloudHSM, you get exclusive, single-tenant control over the FIPS 140-2 Level 3 hardware appliance, which is often required for extremely strict corporate compliance (like PCI-DSS for credit cards).

### 16. How do you audit the usage of a KMS Key?
**Answer:** AWS KMS integrates natively with **AWS CloudTrail**. Every time an application or user makes an API call like `kms:Encrypt` or `kms:Decrypt`, CloudTrail logs the identity, the timestamp, the IP address, and the specific Key ID used, making it easy to pass security audits.

### 17. What are KMS Multi-Region Keys?
**Answer:** By default, a KMS key is strictly bound to a single AWS region. Multi-Region Keys allow you to replicate a primary KMS key into multiple different AWS regions. This is critical for disaster recovery: if you replicate an encrypted S3 bucket to another region, you can decrypt the data in the backup region using the replicated key.

### 18. What is the AWS Encryption SDK?
**Answer:** It is a client-side encryption library provided by AWS. It abstracts away the complex math of Envelope Encryption. Developers use the SDK to easily encrypt data locally inside their application code *before* sending it over the network to a database or S3.

### 19. How do you import your own key material into KMS (BYOK)?
**Answer:** Bring Your Own Key (BYOK) allows you to generate a 256-bit symmetric key in your on-premises HSM and securely import it into an empty KMS key shell. The main benefit is that you can instantly delete the key material from AWS at any time, instantly rendering all data encrypted by it unreadable.

### 20. What is MAC (Message Authentication Code) in KMS?
**Answer:** KMS supports HMAC (Hash-Based Message Authentication Code) keys. These are used to generate and verify digital signatures, ensuring that a message has not been tampered with in transit and proving the authenticity of the sender.
