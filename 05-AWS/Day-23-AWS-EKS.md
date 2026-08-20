# Day-23: AWS EKS (Elastic Kubernetes Service) Deep Dive

## Introduction
Welcome to Day 23! Today we are tackling one of the most powerful and widely-used services in modern DevOps: **Amazon Elastic Kubernetes Service (EKS)**. By the end of this guide, you will understand the fundamentals of EKS, how it compares to managing your own Kubernetes cluster, and exactly how to deploy your first application onto it.

---

## Table of Contents
1. [Understanding Kubernetes Fundamentals](#1-understanding-kubernetes-fundamentals)
   - 1.1 EKS vs. Self-Managed Kubernetes: Pros and Cons
2. [Setting up your AWS Environment for EKS](#2-setting-up-your-aws-environment-for-eks)
   - 2.1 Creating an AWS Account and Setting up IAM Users
   - 2.2 Configuring the AWS CLI and kubectl
   - 2.3 Preparing Networking and Security Groups for EKS
3. [Launching your First EKS Cluster](#3-launching-your-first-eks-cluster)
4. [Deploying Applications on EKS](#4-deploying-applications-on-eks)

---

## 1. Understanding Kubernetes Fundamentals

Kubernetes (K8s) is the industry standard for container orchestration. However, managing it yourself can be a nightmare. Let's compare letting AWS manage it (EKS) versus managing it yourself on EC2 instances.

### 1.1 EKS vs. Self-Managed Kubernetes: Pros and Cons

#### EKS (Amazon Elastic Kubernetes Service)
**Pros:**
* **Managed Control Plane:** EKS manages the Kubernetes control plane (API server, controller manager, etcd). AWS handles upgrades, patches, and high availability automatically!
* **Automated Updates:** EKS cluster versions are automatically updated securely.
* **AWS Integration:** Seamlessly integrates with AWS IAM (for auth), VPC (networking), and ALBs (Load Balancers).
* **Security & Compliance:** Built-in compliance standards for enterprise security.

**Cons:**
* **Cost:** You pay an hourly rate (~$0.10/hr) just for the control plane, plus the cost of worker nodes.
* **Less Control:** You cannot access the underlying control plane nodes or modify certain backend configurations.

#### Self-Managed Kubernetes on EC2
**Pros:**
* **Cost-Effective:** You can run it entirely on cheaper Spot instances with no extra control plane fee.
* **Ultimate Flexibility:** Full SSH access and control over every component.

**Cons:**
* **High Complexity:** You must manually configure etcd backups, API scaling, and high availability.
* **Maintenance Overhead:** Upgrading Kubernetes versions manually is dangerous and time-consuming.

---

## 2. Setting up your AWS Environment for EKS

Before deploying EKS, you must prepare your AWS environment securely.

### 2.1 Creating an AWS Account and Setting up IAM Users
1. Create an AWS Account and log into the Management Console.
2. Navigate to **IAM (Identity and Access Management)**.
3. Click **Add user**, give them **Programmatic access**, and attach Administrator or EKS-specific policies.
4. Save the generated **Access Key ID** and **Secret Access Key** securely.

### 2.2 Configuring the AWS CLI and kubectl
*See our `day-23-code/Prerequisite.md` file for full installation links.*

1. **Configure AWS CLI:** Open your terminal and run:
   ```bash
   aws configure
   ```
   *Enter your Access Key, Secret Key, and Default Region.*

2. **Configure kubectl for EKS:** 
   Once your cluster is created, you link it to your local machine using:
   ```bash
   aws eks update-kubeconfig --name <your-cluster-name> --region <your-region>
   ```

### 2.3 Preparing Networking and Security Groups for EKS
A secure EKS cluster requires strict networking:
1. **VPC:** Create an Amazon VPC with both Public and Private subnets spread across multiple Availability Zones.
2. **Security Groups:** 
   - Define inbound rules (e.g., deny all by default, allow specific CIDR blocks).
   - Define outbound rules (allow EKS worker nodes to reach the internet to pull Docker images).
3. **Internet Gateway (IGW):** Attach an IGW to your VPC and update the Route Tables (`0.0.0.0/0`) so your worker nodes can communicate externally.
4. **IAM Policies:** Your worker nodes need an IAM Role with policies allowing them to pull images from ECR and interact with EC2/Auto Scaling.

---

## 3. Launching your First EKS Cluster

The easiest way to launch an EKS cluster is using the official command-line tool: `eksctl`.

Navigate to our `day-23-code/installing-eks.md` notes for the exact commands.
To create a serverless Fargate EKS cluster, you simply run:
```bash
eksctl create cluster --name demo-cluster --region us-east-1 --fargate
```
*Note: This command automatically provisions the VPC, Subnets, and Security Groups in the background using CloudFormation! It takes about 15-20 minutes.*

---

## 4. Deploying Applications on EKS

Now that our cluster is running, let's deploy an NGINX sample application!

### Step 1: Examine the YAML files
Navigate to the `day-23-code` folder in our repository. You will find:
* `deploy.yaml`: This Kubernetes Deployment file tells EKS to spin up 3 replicas of the `nginx` container.
* `service.yaml`: This creates a Kubernetes Service to route traffic to your 3 NGINX containers over port 80.

### Step 2: Deploy the Application
Run the following commands in your terminal:
```bash
# 1. Deploy the pods
kubectl apply -f deploy.yaml

# 2. Deploy the networking service
kubectl apply -f service.yaml

# 3. Verify they are running
kubectl get pods
kubectl get svc
```

---

## Advanced Topics & Add-Ons

To take your EKS cluster to the next level (making it production-ready), check out the advanced guides we have placed in the `day-23-code` folder:

1. **OIDC Connector (`configure-oidc-connector.md`):** Learn how to allow your Kubernetes pods to assume AWS IAM Roles securely.
2. **AWS Load Balancer Controller (`alb-controller-add-on.md`):** Learn how to automatically provision AWS Application Load Balancers (ALBs) when you deploy Kubernetes Ingress resources.
3. **The 2048 Game Demo (`2048-app-deploy-ingress.md`):** A fun, real-world deployment of the popular 2048 game using an ALB Ingress and Fargate profiles!
