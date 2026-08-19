# Day-21: AWS ECR (Elastic Container Registry)

## Introduction to Containers & ECR

Before we dive into ECR, let's quickly recap what a **Container** is. 
A container is a lightweight, standalone, executable package that contains everything your application needs to run: the code, runtime, system tools, libraries, and settings.

### What is AWS ECR?
**ECR** stands for **Elastic Container Registry**. It is a fully managed container registry provided by AWS that makes it easy for developers to store, manage, and deploy Docker container images.

> [!TIP]
> **The Power of "E" (Elastic):** Whenever you see an AWS service starting with "E" (like EC2, EKS, ECR), it means the service is **Elastic**. This means it is highly scalable and highly available by nature. AWS automatically increases the capacity of these services in the background to accommodate any amount of resources you throw at it!

---

## AWS ECR vs DockerHub
Both ECR and DockerHub are container registries used to store Docker images so they can be shared and downloaded. However, there are a few major differences every DevOps engineer must know:

| Feature | DockerHub | AWS ECR |
| :--- | :--- | :--- |
| **Default Visibility** | **Public** by default. Anyone in the world can easily pull your images unless you explicitly pay for private repos. | **Private** by default. It is designed for enterprise security, though you can create public repos if needed. |
| **Security & Access** | Uses standard DockerHub usernames and passwords/tokens. | Deeply integrated with **AWS IAM**. You can restrict exactly which users/roles can push or pull images. |
| **Ecosystem Integration**| Standalone service. | Integrates seamlessly with AWS services like **ECS, EKS, CodeBuild, and Lambda**. |
| **Cost** | Free for public repos, paid for private limits. | **Not Free.** You pay for the storage space your images consume and the data transfer out. |

---

## Hands-On Lab: Pushing an Image to ECR

Let's build a repository and push a Docker image to it securely!

### Prerequisites
To push an image from your local computer to AWS, you must have:
1. Docker installed and running on your machine.
2. The **AWS CLI** (or AWS Tools for PowerShell) installed.
3. An **IAM User** configured on your terminal with permissions to access ECR (e.g., `AmazonEC2ContainerRegistryFullAccess`).

### Step 1: Create the ECR Repository
1. Log into the AWS Console and search for **ECR (Elastic Container Registry)**.
2. Click **Get Started** (or Create repository).
3. **Visibility settings:** Select **Private**.
4. **Repository name:** `demo-app-repo`
5. **Tag immutability:** **Enable it.** *(This prevents developers from accidentally overwriting an existing image tag, ensuring that `v1.0` always remains the exact same code!)*
6. **Scan on push:** **Enable it.** *(This is a massive security feature. Whenever a developer pushes an image, AWS automatically scans it for known software vulnerabilities!)*
7. Click **Create repository**.

### Step 2: View the Push Commands
Once the repository is created:
1. Click on your newly created `demo-app-repo`.
2. In the top right corner, click on the **View push commands** button. AWS provides you with the exact terminal commands needed to push your image!

### Step 3: Authenticate and Push (PowerShell Example)
If you are using Windows PowerShell, you will run the following commands (replace the AWS account ID and region with your own):

**1. Authenticate your Docker client:**
*This command uses the AWS Tools for PowerShell to grab a secure, temporary password and log your local Docker daemon into AWS.*
```powershell
(Get-ECRLoginCommand).Password | docker login --username AWS --password-stdin 420943511113.dkr.ecr.eu-north-1.amazonaws.com
```

**2. Build your Docker Image:**
*Navigate to a folder containing a `Dockerfile` and build it. (Skip this if you already have an image).*
```powershell
docker build -t demo-ecr .
```

**3. Tag your Image:**
*You must tag your local image so Docker knows exactly which AWS URL to push it to.*
```powershell
docker tag demo-ecr:latest 420943511113.dkr.ecr.eu-north-1.amazonaws.com/demo-app-repo:latest
```

**4. Push the Image to ECR:**
*Finally, push the image into the cloud!*
```powershell
docker push 420943511113.dkr.ecr.eu-north-1.amazonaws.com/demo-app-repo:latest
```

If you refresh your AWS Console, you will now see your Docker image safely stored, scanned for vulnerabilities, and ready to be deployed to an EKS cluster or ECS service!
