# Day-12: Infrastructure as Code (IaC) with AWS CloudFormation (CFT)

## Introduction to Infrastructure as Code (IaC)
Traditionally, infrastructure was provisioned manually by clicking through the AWS Management Console or running individual CLI commands. As your architecture grows, this becomes difficult to track, reproduce, and manage.

**Infrastructure as Code (IaC)** is the process of managing and provisioning cloud resources through machine-readable definition files (scripts/code) rather than physical hardware configuration or interactive configuration tools.

**Principles of IaC:**
1. **Declarative:** You define *what* you want the final state to look like (e.g., "I need an S3 bucket with versioning enabled"). In simple terms: **what you see in the code is what you have in the infrastructure.** The IaC tool figures out *how* to achieve that state.
2. **Version Controlled:** Since your infrastructure is just code (text files), you can store it in Git, track changes over time, and collaborate with your team.
3. **Repeatable:** You can deploy the exact same environment in multiple regions or accounts without manual errors.

### The Flow of IaC
There are two ways to look at how IaC acts as a middleman:

**General IaC Flow (Multi-Cloud):**
```text
User -----> IaC Tool (e.g., Terraform or "SivaTool") -----> Cloud (AWS, Azure, GCP)
```
*(The IaC tool acts as the intermediate manager between the user and the cloud provider).*

**AWS CloudFormation Flow:**
```text
User (gives YAML, JSON) -----> AWS CFT -----> AWS API Calls -----> AWS Cloud (Infrastructure Created)
```

*(Note: Once you have your YAML template, you can submit it to AWS CFT via the AWS UI, the AWS CLI, or even an automation server like Jenkins. You can Create new stacks or Import existing resources).*

---

## AWS CLI vs. AWS CFT

| Feature | AWS CLI (Command Line Interface) | AWS CFT (CloudFormation Templates) |
| :--- | :--- | :--- |
| **Best For** | Short, quick administrative tasks and simple scripts. | Creating and managing complex, multi-tier infrastructure. |
| **Approach** | Imperative (You execute specific commands step-by-step). | Declarative (You define the desired end-state in a file). |
| **State Management** | None. You have to manually track what was created. | Built-in. CFT remembers what it created and manages the "Stack". |

---

## AWS CloudFormation vs. Terraform

Both are popular IaC tools, but they have key differences:

*   **AWS CloudFormation (CFT):** Native to AWS. It is tightly integrated with all AWS services and is completely free to use (you only pay for the resources it creates). It only works for AWS.
*   **Terraform (by HashiCorp):** Cloud-agnostic. Terraform can provision resources on AWS, Azure, Google Cloud (GCP), and many other providers using the same toolset.
    *   *Note: Learning Terraform is highly recommended for modern DevOps engineers because many organizations use a multi-cloud strategy.*

---

## CloudFormation Templates: YAML vs. JSON

CloudFormation supports two formats for writing templates: **JSON** and **YAML**.

**Why you should always use YAML:**
1.  **Readability:** YAML is much cleaner and easier for humans to read.
2.  **Comments:** In YAML-formatted templates, you can include inline comments by using the `#` symbol. In JSON-formatted templates, comments are **not supported**. JSON, by design, doesn't include a syntax for comments. However, if you need to include explanatory notes in JSON, you can add a `Metadata` attribute.
3.  **Less Syntax:** YAML uses indentation instead of curly braces `{}` and commas `,`, making it less prone to syntax errors.

*Important: In YAML, **indentation is critical**. Always use spaces (not tabs) to indent your code correctly!*

### JSON vs YAML Example

**JSON Structure:**
```json
{
  "AWSTemplateFormatVersion" : "version date",
  "Description" : "JSON string",
  "Metadata" : {
    // template metadata
  },
  "Parameters" : {
    // set of parameters
  },
  "Rules" : {
    // set of rules
  },
  "Mappings" : {
    // set of mappings
  },
  "Conditions" : {
    // set of conditions
  },
  "Transform" : {
    // set of transforms
  },
  "Resources" : {
    // set of resources
  },
  "Outputs" : {
    // set of outputs
  }
}
```

**YAML Structure:**
```yaml
---
AWSTemplateFormatVersion: '2010-09-09'
Description: A sample CloudFormation template with YAML comments.

# Resources section
Resources:
  MyEC2Instance: 
    Type: AWS::EC2::Instance
    Properties: 
      # Linux AMI
      ImageId: ami-1234567890abcdef0 
      InstanceType: t2.micro
      KeyName: MyKey
```

---

## Template Anatomy (Standards)

An AWS CloudFormation template consists of several optional sections, but **Resources is the only mandatory section**.

Here is the standard structure of a YAML template:

```yaml
---
AWSTemplateFormatVersion: '2010-09-09' # The version date of the template format

Description: 
  A brief description of what this template does.

Metadata:
  # Extra information or configuration for the template

Parameters:
  # Values to pass into your template at runtime (e.g., InstanceType, EnvironmentName)

Rules:
  # Validates the parameters passed to the template

Mappings:
  # A lookup table (e.g., mapping an AWS Region to a specific AMI ID)

Conditions:
  # Logic to determine if certain resources should be created (e.g., if Env == 'Prod', create a larger DB)

Transform:
  # Used for serverless applications (AWS SAM)

Resources: # MANDATORY: This is where you define your actual AWS resources (EC2, S3, VPC, etc.)
  # set of resources

Outputs:
  # Values that are returned after the stack is created (e.g., the URL of a Load Balancer or the ID of an S3 bucket)
```

---

## Hands-On: Creating an S3 Bucket from Zero to Hero

### Step 1: Setting up your Environment (Tips & Tricks)
Before writing code, make sure you have the right tools to make your life easier. If you use **VS Code**, download these extensions:
1.  **YAML** (by Red Hat): Provides YAML syntax highlighting and validation.
2.  **AWS Toolkit**: Helps with AWS services and CloudFormation code completion.

### Step 2: Writing the Template
How do you know what to write? **Always refer to the official AWS CloudFormation Documentation!**
1. Search Google for `AWS CloudFormation Template Reference`.
2. Look for the "AWS resource and property types reference".
3. Search for the service you want (e.g., `AWS::S3::Bucket`).
4. The documentation provides the exact syntax and examples!

Create a file on your local machine named `template.yaml` and paste the following code:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: A simple S3 bucket created using CloudFormation
Resources:
  MyS3Bucket: # This is a logical ID used within the template
    Type: 'AWS::S3::Bucket'
    Properties:
      BucketName: "demo-cft-bucket-siva-12345" # MUST be globally unique
```

### Step 3: Deploying the Template (Creating a Stack)
1. Go to the **AWS Management Console** and search for **CloudFormation**.
2. Click **Create stack** > **With new resources (standard)**.
3. You will see three options for the prerequisite: 
   *   **Template is ready** (Upload your own file)
   *   **Use a sample template**
   *   **Create template in designer** (A drag-and-drop UI to generate basic resource code).
4. *Optional:* If you are a beginner, you can select **Create template in designer**, drag an `AWS::S3::Bucket` onto the canvas, and it will auto-generate the basic code for you.
5. Once your `template.yaml` code is ready, select **Template is ready**.
6. Under **Specify template**, you have two choices:
   *   **Amazon S3 URL:** If you stored your template in an S3 bucket, provide the link here.
   *   **Upload a template file:** Select this to upload the file directly from your local laptop.
7. Choose **Upload a template file**, select your `template.yaml` file, and click **Next**.
6. Give your stack a name (e.g., `MyFirstS3Stack`) and click **Next**.
7. Keep clicking **Next** through the options and finally click **Submit**.
8. Wait for the status to change to **CREATE_COMPLETE**.

Congratulations! You just created infrastructure using code! Go to the S3 console, and you will see your new bucket. 
*(Note: CloudFormation actually saves a copy of your uploaded template into a hidden S3 bucket automatically for future use).*

### Step 4: Delete the Stack
To understand the full lifecycle, let's delete the stack we just created before moving on to the Drift lab.
1. Select your stack (`MyFirstS3Stack`) and click **Delete**.
2. CloudFormation will automatically delete the S3 bucket and clean up all resources it created.

---

## Drift Detection

What happens if you create an S3 bucket using CloudFormation, but then someone goes into the AWS Console UI and manually changes a setting? 

This is called **Drift**. The actual state of the resource in AWS has "drifted" away from the desired state defined in your code. To understand this better, let's do a real-time example.

### Let's Test Drift Detection:

**1. Create a Bucket with Versioning Enabled**
Referencing the AWS documentation, let's write a template that has versioning explicitly enabled:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: A simple S3 bucket with versioning
Resources:
  MyS3Bucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      BucketName: "demo-cft-bucket-siva-12345"
      VersioningConfiguration:
        Status: Enabled
```
Upload this `template.yaml` to CloudFormation and create a new stack. Wait for it to complete.

**2. Create the Drift (Manual UI Change)**
1. Go to your **S3 Console**, find the newly created bucket.
2. Click on the bucket, go to **Properties**, and manually **Suspend/Disable Bucket Versioning**. 
*(We are doing this to check the drift mechanism).*

**3. Detect the Drift in CFT**
1. Go back to the **CloudFormation** console.
2. Select your stack.
3. Click on **Stack actions** (top right) and select **Detect drift**.
4. Wait a few seconds, then look at the **Drift status**. It will change to **DRIFTED** because you made changes in the S3 bucket by disabling versioning.
5. Click on **View drift results**, and then click **View drift details** to see exactly what was modified outside of the template.

*(Always remember: To fix a drift, you should update your CFT code and deploy the update, rather than making manual UI changes!)*
