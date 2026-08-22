# Amazon EKS Interview Questions

Amazon Elastic Kubernetes Service (EKS) is the enterprise standard for running Kubernetes on AWS. These questions test your knowledge of K8s architecture, Node Groups, and AWS integration.

### 1. What is Amazon EKS?
**Answer:** Amazon Elastic Kubernetes Service (EKS) is a fully managed, certified Kubernetes conformant service that makes it easy to deploy, manage, and scale containerized applications on AWS without needing to install or operate your own Kubernetes Control Plane.

### 2. How does Amazon EKS work?
**Answer:** EKS provisions and scales the Kubernetes Control Plane (API server, etcd) across multiple AWS Availability Zones to ensure high availability. Users then provision "Worker Nodes" (EC2 instances or Fargate) which connect to this managed Control Plane to run the actual application pods.

### 3. What is Kubernetes?
**Answer:** Kubernetes (K8s) is an open-source container orchestration platform originally designed by Google. It automates the deployment, scaling, healing, and management of complex, microservice-based containerized applications across massive clusters of hosts.

### 4. What are the key features of Amazon EKS?
**Answer:** EKS provides a highly available Control Plane, seamless integration with AWS IAM for authentication, native VPC networking using the Amazon VPC CNI plugin, automated version upgrades, and support for both EC2 Managed Node Groups and Serverless AWS Fargate.

### 5. What is a Kubernetes Cluster?
**Answer:** A Kubernetes cluster consists of two main parts:
1. **The Control Plane:** The master node that makes global decisions about the cluster (managed by AWS in EKS).
2. **The Data Plane (Nodes):** The worker machines (EC2/Fargate) that actually run the containerized applications (Pods).

### 6. How do you create a Kubernetes cluster in Amazon EKS?
**Answer:** While you can use the AWS Console, the industry standard is to use Infrastructure as Code (like Terraform's EKS module) or the officially supported CLI tool, `eksctl`. These tools automate the creation of the VPC, the EKS Control Plane, and the Worker Node Groups.

### 7. What are Kubernetes Nodes?
**Answer:** Nodes are the physical or virtual worker machines in a cluster. In EKS, a Node is usually an Amazon EC2 instance. It runs the `kubelet` (the agent that communicates with the Control Plane) and a container runtime (like `containerd` or Docker) to execute Pods.

### 8. How does Amazon EKS manage Kubernetes Control Plane updates?
**Answer:** EKS allows you to trigger an in-place upgrade of the Control Plane version via the AWS Console or CLI. AWS manages the complex process of rolling out new API servers and updating the underlying `etcd` database with zero downtime to your running applications.

### 9. What is the difference between Amazon EKS and Amazon ECS?
**Answer:** Amazon ECS is AWS's proprietary, simplified container orchestrator—great for deep AWS integration and ease of use. Amazon EKS runs open-source Kubernetes, which has a much steeper learning curve but offers ultimate flexibility, an massive open-source ecosystem (Helm, Istio), and multi-cloud portability (no vendor lock-in).

### 10. How can you scale applications in Amazon EKS?
**Answer:** 
* **Horizontal Pod Autoscaler (HPA):** Automatically scales the number of Pods up or down based on CPU/Memory metrics.
* **Cluster Autoscaler (or Karpenter):** Automatically provisions new EC2 Worker Nodes when there are pending Pods that cannot fit onto the existing Nodes.

### 11. What is the role of Amazon EKS Managed Node Groups?
**Answer:** Managed Node Groups automate the provisioning and lifecycle management of EC2 worker nodes. Instead of manually configuring EC2 Auto Scaling Groups and user-data scripts to join the cluster, EKS handles the node creation, draining, and upgrading for you via a single API call.

### 12. How does Amazon EKS handle networking?
**Answer:** EKS natively uses the **Amazon VPC CNI (Container Network Interface) plugin**. This means every single Pod receives a real, routable private IP address directly from the underlying AWS VPC subnet, completely avoiding complex overlay networks and ensuring high network performance.

### 13. What is a Kubernetes Pod in Amazon EKS?
**Answer:** A Pod is the smallest, most basic deployable object in Kubernetes. A Pod represents a single instance of a running process and encapsulates one or more tightly coupled Docker containers that share the same storage volume, network IP, and port space.

### 14. How does Amazon EKS integrate with AWS services?
**Answer:** 
* **IAM:** Uses IAM Roles for Service Accounts (IRSA) to grant specific Pods access to AWS APIs (like S3).
* **ELB:** Uses the AWS Load Balancer Controller to automatically provision ALBs/NLBs when you define Kubernetes Ingress or Service objects.
* **EBS/EFS:** Uses CSI drivers to dynamically provision persistent storage volumes for Pods.

### 15. Can you run multiple Kubernetes clusters on Amazon EKS?
**Answer:** Yes, you can spin up dozens of isolated EKS clusters in a single AWS account. However, to save costs (since you pay ~$73/month just for the Control Plane), many enterprises prefer to run a single large cluster and use **Kubernetes Namespaces** and RBAC to isolate different teams (multi-tenancy).

### 16. What is the difference between a Kubernetes Deployment and a StatefulSet?
**Answer:** 
* **Deployment:** Used for stateless apps (like a web frontend). Pods are entirely interchangeable and scale randomly.
* **StatefulSet:** Used for stateful apps (like a MongoDB database). It provides strict guarantees about the ordering and uniqueness of Pods. Each Pod gets a sticky identity (e.g., `db-0`, `db-1`) and its own dedicated persistent storage volume.

### 17. How can you secure an Amazon EKS cluster?
**Answer:** 
1. Use **IAM Roles for Service Accounts (IRSA)** instead of attaching broad IAM policies to the EC2 nodes.
2. Implement **Network Policies** (using Calico) to restrict which Pods can communicate with each other.
3. Keep the EKS API endpoint private (accessible only within the VPC).
4. Regularly scan container images in ECR before deployment.

### 18. What is a Kubernetes Operator in Amazon EKS?
**Answer:** An Operator is a software extension to Kubernetes that uses custom resources to manage complex, stateful applications automatically. For example, a Prometheus Operator doesn't just deploy Prometheus; it knows how to automatically configure it, back it up, and recover it from failure, acting like a robotic sysadmin.

### 19. How can you automate application deployments in Amazon EKS?
**Answer:** The modern DevOps standard is to use GitOps tools like **ArgoCD** or **Flux**. These tools run inside the EKS cluster, constantly monitor a Git repository containing your Kubernetes manifests (or Helm charts), and automatically sync any code changes directly to the cluster state.

### 20. How does Amazon EKS handle high availability?
**Answer:** AWS guarantees the high availability of the Control Plane by running it across at least three Availability Zones. For the Data Plane (your applications), you ensure high availability by deploying your Pods with an `AntiAffinity` configuration, forcing Kubernetes to schedule them onto distinct EC2 nodes across different AZs.
