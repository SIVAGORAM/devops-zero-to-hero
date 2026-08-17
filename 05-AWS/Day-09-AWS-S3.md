# Day 09: AWS S3 Buckets Deep Dive

Welcome to Day 9! Today we are diving into Amazon S3 (Simple Storage Service). 

S3 is considered the easiest service in AWS to learn, yet it solves one of the most critical and common problems in computing: **Storage**. 

---

## 1. What is Amazon S3?

Amazon S3 is a cloud storage service provided by AWS that allows you to store and retrieve any amount of data from anywhere on the web. 

It is built to be:
- **Highly Available**
- **Scalable** (virtually unlimited storage)
- **Secure**
- **Cost-Effective**
- **High Performing**

### What can you store in S3?
There are absolutely **no restrictions** on file types. You can store photos, movies, Excel sheets, and folders. 

**DevOps Use Cases:**
As a DevOps engineer, you won't be storing family photos here. Instead, you will use S3 for:
- Application log files (e.g., keeping logs from the last 30 days for debugging).
- Massive Database Backups.
- Storing userdata and backups for massive e-commerce sites (like Flipkart or Amazon).

### The "11 9's" of Durability
AWS guarantees `99.999999999%` durability. This means if you store 10 million objects in S3, you can expect to lose a single object once every 10,000 years. If an entire AWS data center goes down, your files are completely safe because S3 automatically replicates your data across multiple Availability Zones in the background.

---

## 2. Core S3 Concepts

### S3 is a Global Service
Unlike EC2 or VPCs which are locked to a specific Region, S3 is a **Global Service**. 
Because it uses standard HTTP protocols to make files accessible from the web, **Bucket Names must be globally unique**. If someone in the world has named their bucket `app-1-payments-prod`, you cannot use that name. You must choose a unique name (e.g., `app-1-payments-prod-example.com`).

### Objects vs. Files
In the world of S3, everything you upload is called an **Object**. 
There is no limit to how many objects you can put in a single bucket, but a *single object* cannot be larger than **5 TB**. 
> [!TIP]
> If you are uploading a massive file (like a 100GB database backup), always use **Multipart Uploads**. If your network drops at 99%, Multipart Upload will just resume the failed chunk instead of restarting from zero.

---

## 3. Hands-On Lab: Mastering S3 Step-by-Step

Let's get our hands dirty and build a complete S3 architecture.

### Step 1: Create an S3 Bucket
1. Log into the AWS Console and search for **S3**.
2. Click **Create bucket**.
3. **Bucket name:** Enter a globally unique name (e.g., `siva-app-payments-prod-123`). 
4. **Region:** Select the region closest to your users to ensure maximum speed.
5. Keep **Block Public Access settings** checked (this is the secure default).
6. *(Optional)* Note that you can enable **Bucket Versioning** and rely on the **Default Encryption** that S3 automatically applies.
7. Click **Create bucket**.

*Congratulations! You now have infinite storage. You can instantly start uploading files from your computer using the "Upload" button.*

---

### Step 2: Create an IAM User for S3 Access
In the real world, you do not use your Root Account to access S3. You create an IAM User with specific permissions.

1. Go to the **IAM** Dashboard.
2. Click **Users** -> **Create user**.
3. **User name:** `demo-s3-bucket-user`
4. Check the box to **Provide user access to the AWS Management Console**.
5. Select **I want to create an IAM user** and choose a Custom password. Click Next.
6. Click **Attach policies directly**.
7. Search for `AmazonS3FullAccess` and select it.
8. Click **Create user**. 
*You can now log in securely as this user to manage your buckets!*

---

### Step 3: Bucket Policies & Security (JSON)
S3 provides incredibly granular security. You can write JSON "Bucket Policies" to explicitly Deny or Allow traffic. *(Tip: You can use the **AWS S3 Policy Generator** tool to build these JSON files automatically!)*

*Security Best Practice:* S3 encrypts data at rest by default. You should also ensure data in transit is encrypted by enforcing SSL/TLS for data transfers.

For example, to restrict a bucket so that **ONLY** the root account owner can access it (and deny everyone else, even if they have links), you would go to the **Permissions** tab of your bucket, click **Edit Bucket Policy**, and paste this exact JSON:

*(Note: Replace `your-bucket-name` and `AWS_ACCOUNT_ID` with your real details)*
```json
{
  "Version": "2012-10-17",
  "Id": "RestrictBucketToIAMUsersOnly",
  "Statement": [
    {
      "Sid": "AllowOwnerOnlyAccess",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::your-bucket-name/*",
        "arn:aws:s3:::your-bucket-name"
      ],
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalArn": "arn:aws:iam::AWS_ACCOUNT_ID:root"
        }
      }
    }
  ]
}
```

**Understanding this JSON line by line:**
- **`"Version"`**: The date format of the AWS policy language. Always use `2012-10-17` for modern AWS policies.
- **`"Effect": "Deny"`**: This tells AWS that this rule is a strict "Block" rule.
- **`"Principal": "*"`**: The asterisk (`*`) means "everyone in the world."
- **`"Action": "s3:*"`**: This targets *all* possible actions in S3 (reading, writing, deleting).
- **`"Resource"`**: This points to exactly *what* is being protected (your specific bucket, and the files `/*` inside it).
- **`"Condition"`**: This is the loophole! It blocks everyone **except** (`StringNotEquals`) the person whose ID matches your root account (`aws:PrincipalArn`).

---

### Step 4: Hosting a Serverless Static Website
S3 isn't just for storing backups—it can actually run your website! Because websites are just HTML/CSS files, S3 can serve them over the internet without needing a server (like EC2 or Nginx).

**1. Enable Static Website Hosting**
1. Go to your Bucket -> **Properties** tab.
2. Scroll to the very bottom to **Static website hosting** and click **Edit**.
3. Select **Enable**.
4. Hosting type: **Host a static website**.
5. Index document: Type `index.html`.
6. Click **Save changes**. 
*(AWS will now give you a Website URL, but if you click it, you will get an "Access Denied" error!)*

**2. Make the Bucket Public**
To allow people on the internet to see your website, you must unblock public access.
1. Go to the **Permissions** tab.
2. Under **Block public access (bucket settings)**, click **Edit**.
3. Uncheck **Block *all* public access** and Save.

**3. Apply the Public Read Policy**
Now, you must explicitly tell AWS that it is okay for strangers on the internet to read your website files.
1. Still in the **Permissions** tab, click **Edit** on **Bucket policy**.
2. Paste this JSON *(Replace `<Bucket-Name>` with your exact bucket name)*:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::<Bucket-Name>/*"
            ]
        }
    ]
}
```

**Understanding this JSON line by line:**
- **`"Effect": "Allow"`**: This rule is granting permission instead of blocking it.
- **`"Principal": "*"`**: It grants this permission to *everyone* on the public internet.
- **`"Action": ["s3:GetObject"]`**: This is critical. It ONLY allows people to "Get" (read) objects. They cannot upload, delete, or edit your website.
- **`"Resource"`**: It applies this public read access to all files (`/*`) inside your specific bucket.

3. Click **Save changes**.

**4. Upload the Code and Test!**
1. We have provided an example `index.html` file in the `day09-s3-website-demo` folder in this repository.
2. Click **Upload** in your bucket and upload that `index.html` file.
3. Go back to your **Properties** tab, scroll to the bottom, and click your **Static Website URL**.
4. You should now see your beautiful, serverless website live on the internet! 

---

## 4. Advanced Features (For Future Exploration)
S3 is packed with enterprise features. As you grow as a DevOps Engineer, you will encounter:
- **Versioning:** Just like Git for your files. If you accidentally overwrite a file, you can restore the old version.
- **Server Access Logging:** Tracks exactly who is logging into your bucket and what they are doing.
- **Event Notifications:** Triggers an AWS Lambda function automatically whenever a new file is uploaded (e.g., automatically resizing an image the moment a user uploads it).
- **Storage Classes:** Moving older files to cheaper, colder storage (like S3 Glacier) to save massive amounts of money.
- **Tags:** Adding metadata labels to your files so you can easily identify, group, and track costs for them.
- **Object Lock:** Prevents an object from being deleted or overwritten for a fixed amount of time (crucial for legal/compliance reasons).
