# Deploy and Expose Your First App to AWS

In this hands-on project, we will take a sample Node.js application, test it locally, and then deploy it manually to an AWS EC2 instance. We will also configure AWS Security Groups to expose the application to the public internet.

---

## Part 1: Test the Application Locally

Before deploying an application to the cloud, a DevOps engineer should always verify that it runs successfully on their local machine.

### Step 1: Clone the Application
Open your terminal and clone the sample repository provided for this session:
```bash
git clone https://github.com/verma-kunal/AWS-Session
cd AWS-Session
```

### Step 2: Open the Code
Open the project in Visual Studio Code (or your preferred editor) to inspect the files:
```bash
code .
```

### Step 3: Setup Environment Variables
Most applications require environment variables for configuration. Create a `.env` file in the root directory:
```bash
touch .env
```
Open the `.env` file and fill in the required details provided in the session (e.g., `PORT`, API keys, etc.).

### Step 4: Install Dependencies and Run
Node.js applications use `npm` to manage dependencies. Install them and start the server:
```bash
npm install
npm run start
```
*You should see output indicating the server has started on port 3000.* 
Open your browser and navigate to `http://localhost:3000` to verify the application works locally.

---

## Part 2: Provision Infrastructure on AWS

Now that we know the app works, let's provision a server in AWS to host it.

### Step 1: Create an IAM User (Security Best Practice)
Never use your AWS Root Account for daily tasks!
1. Log into the **AWS Management Console**.
2. Search for **IAM** (Identity and Access Management).
3. Click on **Users** -> **Add users**.
4. Provide a username and enable **Console access** with a custom password.
5. In the permissions step, select **Attach policies directly**.
6. Search for `AmazonEC2FullAccess` (for this lab), attach it, and click **Create user**.
7. Log out of the root account and log back in using the new IAM user's sign-in URL.

### Step 2: Launch an EC2 Instance
1. In the AWS Console, search for **EC2**.
2. Click **Instances** -> **Launch instances**.
3. **Name:** `demo-nodejs`
4. **AMI (OS):** Select `Ubuntu` (the most common OS for modern web servers).
5. **Instance Type:** Select `t2.micro` (this is Free Tier eligible).
6. **Key Pair:** Select an existing key pair or create a new one (e.g., `demo.pem`). **Make sure to download and save it safely!**
7. **Network Settings:** Ensure **Allow SSH traffic** is checked.
8. Click **Launch instance**.

Once the instance state shows **Running**, click on the instance ID and copy the **Public IPv4 address**.

---

## Part 3: Deploy the Application to EC2

We now have a blank Ubuntu server running in AWS. We need to SSH into it, install the required software, and run our code.

### Step 1: Connect via SSH
Open your terminal (or MobaXterm/Git Bash) and SSH into the server using your downloaded key pair. *Remember to provide the correct path to your `.pem` file.*
```bash
ssh -i demo.pem ubuntu@<your-ec2-public-ip>
```
*Type `yes` when asked to confirm the server's fingerprint.*

### Step 2: Install Required Software
Your new server does not have Git or Node.js installed. Let's install them:
```bash
# Update the package manager
sudo apt update

# Install Node.js and npm
sudo apt install nodejs -y
sudo apt install npm -y

# Verify installations
node -v
npm --version
git --version
```

### Step 3: Clone and Configure the Application
Now, repeat the steps you did locally, but on the cloud server!
```bash
# Clone the repository
git clone https://github.com/verma-kunal/AWS-Session
cd AWS-Session

# Create and configure the environment variables
touch .env
vim .env
```
*(Press `i` to enter Insert Mode. Add your environment variables such as `PORT=3000`, static directory paths, and secret keys. Press `Esc` then `:wq` to save and exit).*

### Step 4: Run the Application
```bash
npm install
npm run start
```
*Your application is now running on the EC2 instance on port 3000!*

---

## Part 4: Expose the Application to the Internet

If you try to visit `http://<your-ec2-public-ip>:3000` in your browser right now, it will time out. Why? Because the **AWS Security Group** (firewall) is blocking port 3000 by default.

### Step 1: Update the Security Group
1. Go back to the AWS EC2 Console.
2. Select your `demo-nodejs` instance.
3. At the bottom of the screen, click on the **Security** tab.
4. Click on the Security Group ID (it will look like `sg-0abcd1234...`).
5. Click **Edit inbound rules**.
6. Click **Add rule**:
   - **Type:** Custom TCP
   - **Port range:** `3000`
   - **Source:** `0.0.0.0/0` (This allows traffic from anywhere on the internet).
7. Click **Save rules**.

### Step 2: Verify the Deployment
Open your browser and navigate to:
```text
http://<your-ec2-public-ip>:3000
```
**Congratulations!** You have successfully deployed a Node.js application to AWS and exposed it to the world.

---
**[Previous: Day 6 - AWS CLI & IaC](../05-AWS/Day-06-AWS-CLI-and-IaC.md)** | **[Next: Day 7 (Part 1) - Linux Foundations](../02-Linux/Day-07-Part-1-Linux-Foundations.md)**
