# AWS CloudTrail Interview Questions

AWS CloudTrail is the fundamental service for security, compliance, and auditing in AWS. These questions test your knowledge of API monitoring and incident response.

### 1. What is AWS CloudTrail?
**Answer:** AWS CloudTrail is a governance, compliance, and auditing service that continuously records, monitors, and retains API calls made within your AWS account. It answers the critical security question: "Who did what, when, and from where?"

### 2. What type of information does AWS CloudTrail record?
**Answer:** CloudTrail records the exact details of an API request. The JSON log file contains the IAM User or Role identity that made the call, the timestamp, the source IP address, the specific service accessed (e.g., EC2), the action taken (e.g., `RunInstances`), and the parameters passed in the request.

### 3. How does AWS CloudTrail store its data?
**Answer:** CloudTrail aggregates the API logs and delivers them as compressed JSON files into an Amazon S3 bucket of your choosing. By storing them in S3, you have a durable, long-term archive for compliance audits.

### 4. How can you enable AWS CloudTrail for an AWS account?
**Answer:** CloudTrail is actually enabled by default upon account creation to capture 90 days of Event History. However, to retain logs permanently, you must go to the CloudTrail Console or use the AWS CLI to create a new "Trail" and configure an S3 bucket destination.

### 5. What is a CloudTrail Trail?
**Answer:** A CloudTrail Trail is the configuration that dictates how your logs are processed and delivered. You configure the trail to determine whether it applies to a single region or all AWS regions globally, and you specify the target S3 bucket and CloudWatch Logs group.

### 6. What is the purpose of CloudTrail log files?
**Answer:** CloudTrail log files are the definitive source of truth for account activity. They are used by security teams for post-incident forensic analysis, by auditors to prove compliance with frameworks like SOC2 or HIPAA, and by operations teams to troubleshoot resource state changes.

### 7. How can you access CloudTrail log files?
**Answer:** Because they are stored in an S3 bucket, you can download the raw JSON files directly. However, the most efficient way to query massive amounts of CloudTrail logs is by using **Amazon Athena**, allowing you to run standard SQL queries directly against the files in S3.

### 8. What is the difference between a Management Event and a Data Event in CloudTrail?
**Answer:** **Management Events** (Control Plane) log actions that modify the configuration of resources, like creating a VPC, terminating an EC2 instance, or modifying an IAM policy. **Data Events** (Data Plane) log high-volume actions performed *within* a resource, such as uploading an object to S3 (`PutObject`) or invoking a Lambda function.

### 9. How can you view and analyze CloudTrail logs?
**Answer:** For recent events (last 90 days), you can use the CloudTrail Event History UI in the console. For deep analysis, you can stream the logs to CloudWatch Logs and use CloudWatch Logs Insights, or query the S3 bucket using Amazon Athena.

### 10. What is CloudTrail Insights?
**Answer:** CloudTrail Insights is a machine learning feature that automatically analyzes your management events to establish a baseline of normal API activity. If it detects highly unusual patterns (e.g., an IAM user suddenly launching 50 EC2 instances when they normally launch 1), it generates an Insights event.

### 11. How can you integrate CloudTrail with CloudWatch Logs?
**Answer:** You can configure your Trail to forward events to a CloudWatch Logs group in near real-time. This allows you to create CloudWatch Metric Filters to actively look for dangerous API calls (like `DeleteTrail` or `ConsoleLogin` without MFA) and immediately trigger an SNS alert to the security team.

### 12. What is CloudTrail Event History?
**Answer:** CloudTrail Event History is a built-in feature in the AWS Console that lets you quickly search, filter, and view the last 90 days of management events in your account for free, without needing to configure an S3 bucket or Athena.

### 13. What are CloudTrail Data Events?
**Answer:** Data Events track high-volume resource operations that are usually too noisy to log by default. The most common use case is tracking object-level activity in S3 (e.g., who exactly downloaded or deleted `secret-file.txt`). Enabling Data Events incurs additional costs.

### 14. What is the purpose of CloudTrail Insights events?
**Answer:** They serve as an automated anomaly detection system. Instead of forcing security engineers to manually hunt through millions of logs looking for hackers, Insights automatically flags unusual spikes in resource provisioning or dangerous IAM modifications so the team can respond rapidly.

### 15. How can you ensure that CloudTrail logs are tamper-proof?
**Answer:** To prevent a hacker from deleting their tracks, you should enable **CloudTrail Log File Validation**. This uses cryptographic hashing (SHA-256) to ensure the logs haven't been modified or deleted. Furthermore, the destination S3 bucket should have MFA Delete and Object Lock enabled.

### 16. Can CloudTrail logs be used for compliance and auditing?
**Answer:** Yes, CloudTrail is the foundational service for AWS compliance. Because it provides an immutable, chronological record of every action taken by every user and system in the account, auditors rely on it entirely to verify internal security controls and governance policies.

### 17. How does CloudTrail support Multi-Region trails?
**Answer:** When creating a trail, best practice is to enable it for **All Regions**. This ensures that even if a malicious actor logs into a region you don't normally use (e.g., ap-northeast-1) to spin up crypto-mining EC2 instances, CloudTrail will capture the activity and send it to your central S3 bucket.

### 18. Can CloudTrail be used to monitor non-AWS services?
**Answer:** CloudTrail is explicitly designed for AWS APIs. However, developers can use the `PutEvents` API to programmatically inject custom, application-level events into CloudTrail if they want to centralize all application auditing into the CloudTrail ecosystem.

### 19. How can you receive notifications about CloudTrail events?
**Answer:** You can configure CloudTrail to publish a message to an Amazon SNS topic every time a new log file is delivered to the S3 bucket. Alternatively, you can use Amazon EventBridge (which natively consumes CloudTrail events in real-time) to trigger a Lambda function or SNS alert instantly when a specific API is called.

### 20. How can you use CloudTrail logs for incident response?
**Answer:** During a security breach, Incident Responders use CloudTrail to determine the "blast radius." They identify the compromised IAM user's Access Key, filter CloudTrail for all API calls made by that specific key, and map out exactly which data was accessed, which resources were modified, and how the attacker traversed the network.
