# Day-19: AWS Cost Optimization (Real-Time Project)

## Why Cost Optimization is Crucial for DevOps Engineers

When mid-level companies or startups build on-premises infrastructure, they face massive overhead: buying physical servers, renting data center space, and paying administration teams to monitor everything 24/7. 

To escape this overhead, organizations move to the Cloud (AWS). The cloud is significantly cheaper **ONLY if you use it efficiently**. 

### The Problem with Cloud Environments
As a DevOps engineer, you will quickly notice that developers (IAM users) create resources rapidly to test new features. A common scenario:
1. A developer creates an **EC2 instance**.
2. An **EBS Volume** (hard drive) is automatically created and attached to it.
3. The developer realizes the data on the volume is important, so they take an **EBS Snapshot** (a backup of the volume).
4. Eventually, the project is deprecated. The developer deletes the EC2 instance (which automatically deletes the attached volume).
5. **The Mistake:** The developer forgets to delete the EBS Snapshot! 

AWS will keep charging your organization for this orphaned ("stale") snapshot forever. If 50 developers do this over a year, your AWS bill will skyrocket!

### The DevOps Solution
As a DevOps engineer, it is your job to track these orphaned resources and either alert the team or delete them automatically. Today, we will use an **Event-Driven Serverless** architecture to solve this problem!

**Architecture Flow:** 
`AWS CloudWatch (Trigger)` $\rightarrow$ `AWS Lambda (Python/Boto3)` $\rightarrow$ `AWS API` $\rightarrow$ `Delete Stale EBS Snapshots`

---

## Hands-On Project: Stale EBS Snapshot Cleaner

### Step 1: Simulate the Problem
Let's act like the careless developer and create the orphaned snapshot.
1. Go to the AWS Console and search for **EC2**.
2. Click **Launch instance**.
3. **Name:** `test-ec2`
4. **OS:** `Ubuntu`
5. **Instance Type:** `t3.micro`
6. Select your key pair and click **Launch instance**.
7. Go to the **Volumes** section in the left sidebar. Note the Volume ID that was automatically created for your new instance.
8. Go to the **Snapshots** section. Click **Create snapshot**.
9. Select **Volume** and choose the Volume ID from step 7. Add a description and click **Create snapshot**.
10. **Now, act like the developer:** Go back to your EC2 instance, select it, and click **Terminate (Delete)**.
11. Check the Snapshots section again. The snapshot is still there! AWS is now charging you for it.

### Step 2: Create the Lambda Function
Let's build the automation to clean this up.
1. Search for **Lambda** in the AWS Console.
2. Click **Create function**.
3. Select **Author from scratch**.
4. **Function name:** `cost-opti-ebs-snapshorts`
5. **Runtime:** `Python` (Lambda natively supports the `boto3` AWS SDK).
6. Click **Create function**.

### Step 3: Insert the Code
1. In the Lambda code editor, paste the contents of `ebs_stale_snapshosts.py` (located in the `day-19-code/` folder of our repository).
   * **What does this code do?** It fetches all your EBS snapshots. It then fetches all currently running EC2 instances. If a snapshot belongs to a volume that no longer exists (or isn't attached to a running instance), it deletes the snapshot!
2. Click **Deploy** to save the code.

### Step 4: Real-World Debugging
Click the **Test** button. Create a new event named `testevent` and click **Test** again. **It will fail!** Here is why, and how to fix it:

#### Error 1: Task timed out after 3.00 seconds
By default, Lambda restricts execution time to 3 seconds to save you money. Our script takes longer because it talks to multiple AWS APIs.
**Fix:**
1. Go to the **Configuration** tab in your Lambda function.
2. Click on **General configuration** -> **Edit**.
3. Increase the **Timeout** to `10 seconds`.
4. Click **Save**. *(Note: Keep timeouts as low as possible in production to avoid paying for stuck loops!)*

#### Error 2: UnauthorizedOperation (Permissions)
Lambda does not have permission to delete snapshots by default.
**Fix:**
1. Go to the **Configuration** tab -> **Permissions**.
2. Click on the **Role name** (it will open the IAM console).
3. Click **Add permissions** -> **Attach policies**.
4. Since there is no pre-built policy for this specific exact mix, click **Create policy**.
5. Select the **EC2** service.
6. Under actions, filter for and check: 
   * `DescribeSnapshots`
   * `DescribeInstances`
   * `DescribeVolumes`
   * `DeleteSnapshot`
7. Under Resources, select **All**.
8. Click **Next**, name the policy (e.g., `EBS-Snapshot-Cleaner-Policy`), and click **Create policy**.
9. Go back to your IAM Role, attach this newly created policy, and close IAM.

### Step 5: Test and Verify!
Go back to your Lambda function and click **Test** again.
Check the Execution Results. You will see a green success message:
`Deleted EBS snapshot snap-0123456789abcdef0 as its associated volume was not found.`

If you go back to your EC2 dashboard, the stale snapshot will be completely gone! 

---

## Going Further: Scheduling the Automation
Right now, you have to manually click the "Test" button. To make this truly automated:
1. Go to **AWS CloudWatch** (or Amazon EventBridge).
2. Create a **Rule** (Schedule).
3. Set the frequency (e.g., run every day at midnight).
4. Set the Target as your `cost-opti-ebs-snapshorts` Lambda function.

Congratulations! You have just implemented a highly requested, real-world DevOps cost-optimization project!
