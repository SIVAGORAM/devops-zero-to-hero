# AWS Identity and Access Management (IAM) Interview Questions

AWS IAM is the absolute core of AWS security. These questions test your knowledge of Authentication vs Authorization, Role-Based Access Control (RBAC), and the Principle of Least Privilege.

### 1. What is AWS Identity and Access Management (IAM)?
**Answer:** AWS IAM is a free, global web service that allows you to securely control access to AWS resources. It serves as the authentication and authorization backbone of AWS, determining exactly *who* can access the account and exactly *what* APIs they are allowed to execute.

### 2. What are the key components of AWS IAM?
**Answer:** The core components are:
* **Users:** Individuals or applications requiring access.
* **Groups:** Collections of users (to simplify permission management).
* **Roles:** Temporary credentials assumable by users, AWS services, or federated identities.
* **Policies:** JSON documents defining the exact permissions.

### 3. How does AWS IAM work?
**Answer:** IAM works by evaluating JSON Policies attached to Principals (Users/Roles). When an entity makes an API request to AWS (e.g., `ec2:RunInstances`), IAM intercepts the request, reads all policies attached to the entity, evaluates the explicit Allows and Denies, and then either permits or rejects the API call.

### 4. What is the difference between Authentication and Authorization in AWS IAM?
**Answer:** 
* **Authentication** is verifying *who* you are (e.g., logging in with a Username, Password, and MFA token, or using Access Keys).
* **Authorization** is determining *what* you are allowed to do once authenticated (e.g., verifying if your attached IAM Policy contains `"Effect": "Allow"` for the `s3:DeleteBucket` action).

### 5. How can you secure your AWS account using IAM?
**Answer:** By strictly enforcing the **Principle of Least Privilege** (never using `*` wildcard permissions), mandating strong password policies, requiring Multi-Factor Authentication (MFA) for all human users, rotating programmatic access keys every 90 days, and entirely locking away the AWS Root Account credentials.

### 6. How do IAM Users differ from IAM Roles?
**Answer:** 
* **IAM Users** possess static, long-term credentials (a fixed password and permanent Access Keys).
* **IAM Roles** do not have permanent credentials. Instead, an entity "assumes" the role via the STS (Security Token Service), which issues highly secure, temporary, short-lived credentials (expiring in 1 to 12 hours) that cannot be easily stolen or leaked.

### 7. What is an IAM Policy?
**Answer:** An IAM policy is a formal JSON document that explicitly lists permissions. It consists of statements containing four main elements: **Effect** (Allow/Deny), **Action** (the specific API, like `s3:GetObject`), **Resource** (the specific ARN, like `arn:aws:s3:::my-bucket/*`), and optionally, **Condition** (e.g., only allow if the IP is from the corporate VPN).

### 8. What is the AWS Management Console?
**Answer:** The AWS Management Console is the graphical web interface used to interact with AWS services. IAM users use their username, password, and account alias to log in. In modern enterprise environments, access to the console is often handled via AWS IAM Identity Center (SSO) rather than local IAM users.

### 9. How does IAM manage programmatic Access Keys?
**Answer:** IAM generates an **Access Key ID** (like a username) and a **Secret Access Key** (like a password). These are used by developers locally or by CI/CD pipelines to authenticate API requests via the AWS CLI or SDKs. The secret key is only shown *once* upon creation and must be stored securely.

### 10. What is the purpose of IAM Groups?
**Answer:** IAM Groups implement Role-Based Access Control (RBAC). Instead of attaching a "Developer" policy to 50 individual users, you attach the policy to a "Developers" Group and place the users inside it. When a developer moves to a different department, you simply change their group, ensuring clean and scalable permission management.

### 11. What is the role of an IAM Policy Document?
**Answer:** The policy document is the absolute source of truth for authorization. AWS evaluates the JSON structure. If an action is not explicitly allowed in a policy document attached to the user, the action is implicitly denied by default. 

### 12. How can you grant permissions to an IAM user?
**Answer:** You can attach policies in three ways:
1. **Managed Policies:** (Best Practice) Attaching a standalone AWS-managed or Customer-managed policy to the user or their group.
2. **Inline Policies:** Embedding a JSON policy directly inside the specific user (discouraged, hard to scale).

### 13. How can you delegate permissions to AWS services using IAM Roles?
**Answer:** This is a crucial security practice. Instead of embedding an Access Key inside an EC2 instance to read from S3, you create an **IAM Instance Profile (Role)** with an S3 Read policy. You attach this Role to the EC2 instance. The AWS infrastructure automatically injects temporary credentials into the instance's metadata, making it highly secure.

### 14. What is Cross-Account Access in AWS IAM?
**Answer:** It is a secure way to allow a user in Account A (Dev Account) to access resources in Account B (Prod Account) without creating a new user in Account B. Account B creates a Role with a "Trust Policy" allowing Account A to assume it. The user in Account A uses the `sts:AssumeRole` API to temporarily cross the boundary.

### 15. How does IAM support Identity Federation?
**Answer:** Federation allows users to log into AWS using their existing corporate credentials. IAM trusts an external Identity Provider (IdP) like Active Directory (via SAML 2.0) or Google Workspace (via OIDC). Upon successful login at the corporate portal, AWS STS issues temporary IAM Role credentials to the user.

### 16. What is the purpose of the IAM Access Advisor?
**Answer:** IAM Access Advisor is an auditing tool. It reviews CloudTrail logs and shows you exactly when a user or role last accessed an AWS service. This allows security engineers to confidently delete unused permissions and tighten policies to meet the Principle of Least Privilege without breaking applications.

### 17. How does IAM enforce the Principle of Least Privilege?
**Answer:** By forcing administrators to define exactly what is allowed. Instead of granting `s3:*` (Full S3 Access), a good IAM engineer writes a policy granting only `s3:PutObject` and restricts it to a specific Resource `arn:aws:s3:::financial-data/*`, ensuring the user cannot read files or delete the bucket.

### 18. What is the difference between IAM Policies and Resource-Based Policies?
**Answer:** 
* **IAM (Identity-Based) Policies:** Attached to a User/Role. They answer "What can *this person* do in AWS?"
* **Resource-Based Policies:** Attached directly to an AWS resource (e.g., an S3 Bucket Policy, KMS Key Policy, or SQS Queue Policy). They answer "Who is allowed to access *this specific resource*?"

### 19. How can you implement Multi-Factor Authentication (MFA) in IAM?
**Answer:** You can require MFA at the user level (using Google Authenticator, a YubiKey, or SMS). For maximum security, you can write an IAM Policy Condition (`"Bool": {"aws:MultiFactorAuthPresent": "true"}`) that actively blocks access to critical actions (like terminating production EC2 instances) unless the user logged in using MFA.

### 20. What is the IAM Policy Evaluation Logic?
**Answer:** The IAM evaluation engine follows a strict hierarchy when evaluating an API request:
1. **Explicit Deny:** If *any* policy explicitly denies the action, the request is immediately blocked (Denies always trump Allows).
2. **Explicit Allow:** If there is no explicit deny, the engine checks for an explicit allow. If found, the request is approved.
3. **Implicit Deny:** If there is neither an explicit allow nor an explicit deny, the request is blocked by default.
