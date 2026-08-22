# AWS Organizations & IAM Identity Center (SSO) Interview Questions

Enterprise AWS environments consist of hundreds of AWS accounts. These questions test your knowledge of multi-account strategies, centralized billing, and cross-account security.

### 1. What is AWS Organizations?
**Answer:** AWS Organizations is an account management service that enables you to consolidate multiple AWS accounts into a single, centrally managed organization. It provides consolidated billing, centralized security governance, and hierarchical grouping of accounts.

### 2. Why should a company use multiple AWS accounts instead of one large account?
**Answer:** Using multiple accounts provides absolute security isolation. If a "Dev" account is compromised, the "Prod" account remains safe. It also isolates API rate limits, simplifies billing (you know exactly how much the Data Science team is spending), and limits the blast radius of human error.

### 3. What is an Organizational Unit (OU)?
**Answer:** An OU is a logical container within AWS Organizations used to group AWS accounts together. You can build a hierarchy (e.g., a "Production" OU and a "Sandbox" OU). You can then attach security policies (SCPs) to the OU, which automatically apply to all accounts inside it.

### 4. What is a Service Control Policy (SCP)?
**Answer:** An SCP is a JSON policy used to centrally manage the maximum available permissions for all accounts in your Organization. It acts as an absolute guardrail. For example, you can attach an SCP to the "Sandbox" OU that explicitly denies the ability to launch expensive `p4d.24xlarge` EC2 instances, overriding any local IAM administrator permissions in those accounts.

### 5. Does an SCP grant permissions?
**Answer:** **No.** An SCP never grants permissions; it only sets a boundary. If an SCP allows `s3:*`, an IAM user still needs a standard IAM Policy attached to them that explicitly allows S3 access to actually perform the action. However, if an SCP *denies* an action, not even the root user of the member account can perform it.

### 6. What is Consolidated Billing?
**Answer:** Consolidated Billing allows you to link the billing of all member accounts to the central Management Account. You get a single monthly invoice for the entire organization. Furthermore, it pools usage across all accounts to help you qualify for volume pricing discounts (e.g., combining S3 storage across 50 accounts to hit the cheaper tier).

### 7. What is the AWS Organizations Management Account?
**Answer:** The Management Account (formerly the Master Account) is the root account that creates the Organization. It pays all the bills and has the power to create new accounts, invite existing accounts, and apply SCPs. For security reasons, you should *never* deploy application resources (like EC2 or RDS) in the Management Account.

### 8. What is AWS Control Tower?
**Answer:** AWS Control Tower is an orchestration service that sits on top of AWS Organizations. It automates the setup of a secure, multi-account AWS environment (a "Landing Zone") based on AWS best practices. It automatically configures SSO, centralizes CloudTrail logs, and deploys standard SCP guardrails with a single click.

### 9. What is AWS IAM Identity Center (formerly AWS SSO)?
**Answer:** IAM Identity Center provides a centralized portal for human users to log in to AWS. Instead of creating local IAM Users in 50 different accounts, users log into the portal once using their corporate Active Directory or Okta credentials, and they are presented with a list of AWS accounts and Roles they are authorized to access.

### 10. How does IAM Identity Center map permissions?
**Answer:** You create "Permission Sets" (which are basically IAM Policies). You then create an assignment: "Grant the 'Database Admins' AD Group access to the 'Production' AWS Account using the 'DBA' Permission Set." Identity Center automatically creates the necessary IAM Roles in the target account.

### 11. Can you move an AWS Account from one Organization to another?
**Answer:** Yes, but it is a manual process. The account must first be removed from the old Organization (which requires setting up standalone billing/credit cards for the account). Then, the new Organization sends an invite to the account, which must be accepted by the account's administrator.

### 12. What happens to IAM users in a member account if it leaves an Organization?
**Answer:** The local IAM users, roles, and policies within the member account remain completely intact and unaffected. However, any guardrails imposed by the Organization's SCPs are immediately removed.

### 13. What is CloudTrail Organizational Trail?
**Answer:** Instead of configuring CloudTrail individually in 100 different accounts (where a local rogue admin could turn it off), you create an Organizational Trail from the Management Account. It forcefully logs all API activity from every member account and delivers the logs to a secure, centralized S3 bucket that local admins cannot access or tamper with.

### 14. What are Tag Policies in AWS Organizations?
**Answer:** Tag Policies help you maintain standardized resource tags across all accounts. For example, you can enforce that every EC2 instance created in any account must have a tag key named `CostCenter` with specific allowed values (e.g., `HR`, `Engineering`).

### 15. How do you handle AWS Support plans in an Organization?
**Answer:** AWS Support is billed at the account level. If you want Enterprise Support for all accounts, it is usually managed via the Consolidated Billing in the Management Account, which aggregates the spend to calculate the support fee.

### 16. What is AWS RAM (Resource Access Manager)?
**Answer:** AWS RAM allows you to easily share specific AWS resources (like Transit Gateways, Route 53 Resolver Rules, or VPC Subnets) across multiple accounts within your AWS Organization, without having to write complex cross-account IAM policies.

### 17. Why would you share a VPC Subnet using AWS RAM?
**Answer:** In an enterprise, a central "Networking Account" creates the VPCs and subnets. They use RAM to share Subnet A with the "Dev Account" and Subnet B with the "Prod Account." The application developers can launch EC2 instances into those subnets, but they cannot delete the subnets or modify the Route Tables.

### 18. What is the "All Features" vs "Consolidated Billing Only" mode in Organizations?
**Answer:** 
* **Consolidated Billing Only:** Only provides centralized invoicing. You cannot use SCPs.
* **All Features:** Provides billing plus full security governance (SCPs, Tag Policies, cross-account service integrations). Moving from Billing to All Features requires all member accounts to approve the change.

### 19. How do you prevent a specific AWS account from leaving the Organization?
**Answer:** You can apply an SCP to the OU (or the entire root) that explicitly denies the `organizations:LeaveOrganization` action. This ensures that a compromised local administrator in a member account cannot detach the account to hide malicious activity.

### 20. How does AWS Config integrate with AWS Organizations?
**Answer:** AWS Config Multi-Account Multi-Region Data Aggregation allows the central security team to view the compliance status of every resource across all 100 AWS accounts from a single dashboard. You can also deploy Config Rules organization-wide to ensure every account enforces encrypted EBS volumes.
