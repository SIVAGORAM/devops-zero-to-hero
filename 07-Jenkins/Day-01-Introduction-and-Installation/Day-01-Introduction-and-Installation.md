# Jenkins Day 1: Introduction to CI/CD and Jenkins Setup

Welcome to the beating heart of DevOps: **CI/CD and Jenkins!**

Today we learn how to take all the manual work out of software delivery. Instead of a developer begging an operations engineer to manually build and test their code, we build a **Pipeline** to do it automatically.

*(Note: "CI/CD" translates perfectly from your voice notes: Continuous Integration and Continuous Deployment/Delivery!)*

---

## 🔁 1. What is CI/CD?

CI/CD is a set of practices used to automate the entire lifecycle of an application, from the moment a developer writes code, to the moment it reaches the end user in production.

The main goal is to deliver software **faster, more reliably, and with less manual work**.

### 🧩 Continuous Integration (CI)
Continuous Integration focuses on the initial phases of the pipeline: **Integrating, Building, and Testing.**

Whenever a developer pushes code to Git (GitHub), the CI pipeline automatically:
1. Detects the new code.
2. Builds the code into an Artifact (like a `.jar` or Docker image).
3. Runs Automated Tests (Unit tests, Integration tests).

**Why do we need CI?**
Without CI, developers work in isolation. When they finally merge their code at the end of the month, everything breaks (Integration Hell). With CI, code is tested *every single time* they push, catching bugs instantly!

**Easy Memory Trick:** `CI = Integrate (Build + Test)`

---

## 🚀 2. Continuous Delivery vs. Continuous Deployment (CD)

This is the most common interview question. Pay close attention!

Both extend the pipeline toward the delivery phase, taking the successfully tested artifact and deploying it to environments (DEV -> TEST -> UAT -> PROD). 

### Continuous Delivery
The application is automatically built, tested, and prepared so that it is **ready for production**, but the final push to Production requires a **Manual Approval** (e.g., a Release Manager clicking a button).

```text
CODE -> BUILD -> TEST -> DEPLOY TO STAGING -> ACCEPTANCE TESTS -> [ MANUAL APPROVAL ] -> PROD
```

### Continuous Deployment
The application is automatically built, tested, and deployed straight to Production without ANY human intervention. If the automated tests pass, the code goes live immediately!

```text
CODE -> BUILD -> TEST -> DEPLOY TO STAGING -> ACCEPTANCE TESTS -> [ AUTOMATIC DEPLOY ] -> PROD
```

> [!IMPORTANT]
> **Golden DevOps Rule:**
> Continuous Delivery vs Continuous Deployment is **NOT** determined by DEV vs PROD environments. The distinction is entirely about **whether the final release requires a manual approval or is 100% automated.**
> - **Delivery:** Production is ready, but release requires approval.
> - **Deployment:** Successful changes automatically reach production.

---

## 🏭 3. Understanding the Pipeline and Artifacts

### The Pipeline
A CI/CD Pipeline is simply a sequence of automated **Stages**.
`Stage 1 (Code) -> Stage 2 (Build) -> Stage 3 (Test) -> Stage 4 (Deploy)`

### The Artifact
An artifact is the final output produced by the "Build" stage. It is the packaged version of the application that will be deployed to the servers.
- Examples: `.jar`, `.war`, `.zip`, Docker Image.

### Environments
A typical application is promoted through multiple environments:
- **DEV (Development):** Where initial automated tests run.
- **TEST:** Where deeper automated and manual QA testing occurs.
- **UAT (User Acceptance Testing):** Where the business or client tests the app to ensure it meets requirements.
- **PROD (Production):** The live environment with real users.

---

## 🎩 4. What is Jenkins?

To build these pipelines, we need a tool. **Jenkins is an open-source automation server written in Java.**

Originally called *Hudson* (created at Sun Microsystems), it was renamed to Jenkins. It is the most widely used tool for executing CI/CD workflows.

### How does Jenkins work?
Think of Jenkins as an automation engine. It sits in the middle of your workflow, listening to GitHub. When GitHub gets new code, Jenkins automatically triggers the pipeline (Build -> Test -> Deploy).

### The Power of Plugins
Jenkins itself is just a bare engine. Its true power comes from **Plugins**. 
Plugins allow Jenkins to talk to almost any DevOps tool in existence (Git, Maven, Docker, AWS, Terraform, SonarQube, Slack).

---

## 🛠️ 5. Practical Lab: Installing Jenkins on AWS EC2

Let's build our own Jenkins server in the cloud!

### Step 1: Launch an EC2 Instance
1. Log in to AWS Console.
2. Launch a new EC2 instance (Amazon Linux 2023 or Ubuntu).
3. **Important:** Jenkins requires at least 2GB of RAM. Do not use a `t2.micro` if possible (it might freeze). Use `t2.small` or `t3.small`.
4. **Security Group:** By default, Jenkins runs on port **8080**. You MUST create an Inbound Rule in your Security Group allowing Custom TCP Port `8080` from `0.0.0.0/0`.

### Step 2: Connect and Install Dependencies
Connect to your EC2 instance via SSH and switch to root:
```bash
sudo su
```

Because Jenkins is written in Java, we must install Java first:
```bash
yum install java-17-amazon-corretto -y
java -version
```

### Step 3: Install Jenkins
Add the official Jenkins repository and import the security key:
```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
```

Install the Jenkins package:
```bash
yum install jenkins -y
```

Start and enable the Jenkins service so it runs automatically:
```bash
systemctl start jenkins
systemctl enable jenkins
systemctl status jenkins
```

### Step 4: Unlock the Jenkins Web UI
Open your web browser and navigate to your EC2 instance's Public IP on port 8080:
```text
http://<your-ec2-public-ip>:8080
```

You will see a screen asking for the "Initial Admin Password". Jenkins locks the dashboard by default for security.

Go back to your terminal and run:
```bash
cat /var/lib/jenkins/secrets/initialAdminPassword
```
Copy that random string of text, paste it into the browser, and click **Continue**.

### Step 5: Final Setup
1. Click **"Install suggested plugins"** (Jenkins will download the most common plugins like Git and Pipeline).
2. Create your First Admin User (Fill out Username, Password, Full Name, Email).
3. Save and Finish!

Congratulations! You have successfully built a Jenkins CI/CD Automation Server from scratch!
