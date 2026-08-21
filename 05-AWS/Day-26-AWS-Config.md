# Day-26: AWS Config (Compliance and Non-Compliance)

Welcome to Day 26! Today we are diving into Governance and Compliance using **AWS Config**. 

As a DevOps Engineer, you are responsible for ensuring that all resources created in your AWS account follow your organization's security and architecture rules. If a developer launches an EC2 instance that violates a rule, you need to know about it immediately!

### 🎯 The Scenario
Your organization has defined a strict rule: **"Whenever an EC2 instance is created, Detailed Monitoring MUST be enabled by default."**
*(Detailed monitoring sends metrics to CloudWatch every 1 minute instead of every 5 minutes, allowing for faster automatic detection of issues).*

If an EC2 instance is launched without this enabled, it is considered **Out of Compliance** (Non-Compliant). We will use AWS Config and an AWS Lambda function to automatically detect these rogue instances.

---

## 1. What is AWS Config?
AWS Config is a service that enables you to assess, audit, and evaluate the configurations of your AWS resources. 
* It records configuration changes over time.
* It evaluates your resource configurations against predefined **Rules**.
* A resource is either **Compliant** (follows the rule) or **Non-Compliant** (violates the rule).

---

## 2. Setting Up AWS Config

If you are using AWS Config for the first time, you must initialize it:
1. Log in to the AWS Management Console and navigate to **AWS Config**.
2. Click **Get started**.
3. **Delivery Channel:** AWS Config needs a place to store the configuration history logs. Specify or create an Amazon S3 bucket.
4. **Resource Types to Monitor:** To save money, we only want to monitor specific resources for this lab. Uncheck all, and specifically select **Amazon EC2 Instances**.
5. Click Next and finish the setup.

---

## 3. Creating the Custom Lambda Function

AWS provides many "Managed Rules" out of the box, but as a Senior DevOps Engineer, you must know how to write **Custom Rules** using AWS Lambda.

### Step 3.1: Create the IAM Role for Lambda
Our Lambda function needs permission to read EC2 instances and report back to AWS Config.
1. Go to **IAM** $\rightarrow$ **Roles** $\rightarrow$ **Create role**.
2. Select **Lambda** as the trusted entity.
3. Attach the following four permission policies:
   * `CloudWatchFullAccess`
   * `AmazonEC2FullAccess`
   * `AWS_ConfigRole`
   * `AWSCloudTrail_FullAccess`
4. Name the role `Config-Lambda-Role` and save it.

### Step 3.2: Write the Lambda Code
1. Go to **AWS Lambda** and click **Create function**.
2. Name it `Check-EC2-Monitoring`. Runtime: **Python 3.x**.
3. Under Execution Role, select **Use an existing role** and choose the `Config-Lambda-Role` you just created.
4. Click **Create function**.
5. Navigate to the `day-26-aws-config` folder in our repository, copy the contents of `lambda_function.py`, and paste it into the Lambda code editor. Click **Deploy**.

> **What does this code do?** 
> It receives an event from AWS Config whenever an EC2 instance changes. It uses the `boto3` Python library to describe that specific EC2 instance and checks if `instance['Monitoring']['State'] == "enabled"`. If it is not, it sets the status to `NON_COMPLIANT` and sends that result back to AWS Config using `put_evaluations`.

Copy the **Function ARN** (Amazon Resource Name) from the top right of the Lambda console. You will need it in the next step.

---

## 4. Creating the AWS Config Custom Rule

Now we link AWS Config to our Lambda function!

1. Go back to the **AWS Config** console.
2. On the left navigation pane, click **Rules**.
3. Click **Add rule**.
4. Choose **Create a custom rule** (specifically *Create custom Lambda rule* if the UI offers it).
5. **Name:** `ec2-detailed-monitoring-enabled`
6. **Description:** "Checks if EC2 instances have detailed monitoring enabled."
7. **AWS Lambda function ARN:** Paste the ARN you copied from Step 3.2.
8. **Trigger type:** Select **When configuration changes**. *(This means the rule runs instantly when someone launches or modifies an EC2 instance).*
9. **Scope of changes:** Select **Resources**.
10. **Resource category:** AWS resources.
11. **Resource type:** `AWS::EC2::Instance`.
12. Click **Next** and **Save rule**.

---

## 5. Monitor and Alert (Testing the Rule)

Your AWS Config rule is now active! 

**How to test it:**
1. Go to the EC2 console and launch a new `t2.micro` instance. **Do not** enable detailed monitoring.
2. Wait a few minutes and check your **AWS Config** dashboard.
3. The dashboard will show `1 Noncompliant resource(s)`.
4. Click on the rule, and it will list the exact Instance ID of the offending EC2 instance!

If you were to go into EC2, click on that instance, go to the Monitoring tab, and click **Manage detailed monitoring $\rightarrow$ Enable**, AWS Config would automatically detect the change and update the instance's status to **Compliant**!

> [!TIP]
> **Real-World Application:** In a production environment, you would set up an Amazon SNS topic to immediately email or Slack message your Security Team whenever AWS Config detects a non-compliant resource!

---

## 6. Zero to Hero Insights (Advanced AWS Config)

To truly master AWS Config for interviews and enterprise environments, you must know about these three advanced features:

### A. Auto-Remediation (Self-Healing Security)
AWS Config doesn't just *detect* problems; it can **fix them automatically!** 
Instead of just alerting you that an EC2 instance is non-compliant, you can attach an **AWS Systems Manager (SSM) Automation Document** to your Config Rule. 
* *Example:* If Config detects an S3 bucket is public, it can trigger an SSM action to automatically block public access, fixing the security hole before a human even wakes up!

### B. Conformance Packs
If your company needs to comply with strict government or industry standards (like HIPAA, PCI-DSS, or CIS Foundations), you don't need to write hundreds of custom rules manually. AWS provides **Conformance Packs**—pre-built collections of Config rules designed specifically to audit your environment against these legal standards.

### C. Cost Management Warnings
AWS Config charges you per **Configuration Item recorded** and per **Rule evaluation**. If you turn on AWS Config for *All Resources* in a highly dynamic environment (where things are constantly created and destroyed), your AWS bill will explode! 
* *Best Practice:* Only monitor the specific resource types (like EC2, S3, IAM) that your organization explicitly requires compliance tracking for.
