# Amazon ECS Interview Questions

Amazon Elastic Container Service (ECS) is the native AWS container orchestrator. These questions test your knowledge of container lifecycle management, Fargate serverless compute, and networking.

### 1. What is Amazon ECS?
**Answer:** Amazon Elastic Container Service (Amazon ECS) is a highly scalable, high-performance, fully managed container orchestration service provided by AWS. It allows you to easily run, manage, and scale Docker containers across a cluster of EC2 instances or via serverless AWS Fargate.

### 2. How does Amazon ECS work?
**Answer:** ECS abstracts away the complexity of managing a cluster management engine (like Kubernetes). You define your application requirements in a JSON blueprint (Task Definition), and the ECS scheduler automatically decides where to place the containers across your cluster based on CPU/Memory availability and placement constraints.

### 3. What is a container in the context of Amazon ECS?
**Answer:** A container is a standardized unit of software. It is a lightweight, standalone, executable package that contains everything needed to run an application (code, runtime, system tools, libraries) guaranteeing that it will run exactly the same regardless of the underlying host OS.

### 4. What is a Task Definition in Amazon ECS?
**Answer:** A Task Definition is the fundamental blueprint for your application, written in JSON. It tells ECS which Docker image to pull (e.g., from ECR), how much CPU/Memory to allocate, which IAM roles to assume, which ports to open, and where to send the container logs (e.g., CloudWatch).

### 5. How are Tasks and Services related in Amazon ECS?
**Answer:** A **Task** is the actual running instantiation of a Task Definition (the running containers). A **Service** is a higher-level construct that ensures a specified number of Tasks are constantly running. If a Task crashes, the Service scheduler automatically spins up a replacement to maintain the desired count.

### 6. What is the difference between Amazon ECS and AWS Fargate?
**Answer:** ECS is the *orchestrator*, while EC2 and Fargate are the *compute providers*. If you run ECS on **EC2**, you must manage, patch, and scale the underlying virtual machines yourself. If you run ECS on **AWS Fargate**, AWS completely manages the underlying servers; you only pay for the exact CPU/Memory your containers consume.

### 7. How can you schedule Tasks in Amazon ECS?
**Answer:** You can schedule tasks in two main ways:
1. **Replica Services:** Maintains a specific number of long-running tasks (e.g., a web server).
2. **Scheduled/Standalone Tasks:** Triggered by Amazon EventBridge (like a cron job) to run a batch processing script once, then terminate.

### 8. What is the purpose of the Amazon ECS Cluster?
**Answer:** An ECS Cluster is a logical boundary or grouping of compute resources (EC2 instances or Fargate capacities) and the tasks that run on them. It provides isolation; for example, you might have one cluster for "Production" and a completely separate cluster for "Staging."

### 9. How can you scale containers in Amazon ECS?
**Answer:** You use **Service Auto Scaling**. You can set up Target Tracking policies (e.g., "Keep average CPU utilization at 70%"). When traffic spikes, Application Auto Scaling automatically increases the "Desired Count" of tasks in your ECS Service to handle the load.

### 10. What is the Amazon ECS Agent?
**Answer:** The ECS Container Agent is a Go-based process running on every EC2 instance within an ECS cluster. It acts as the communication bridge, registering the EC2 instance with the ECS Control Plane and executing the commands to start, stop, or monitor Docker containers locally. (Note: Fargate manages this agent invisibly).

### 11. What is the difference between a Task and a Container Instance in Amazon ECS?
**Answer:** A **Task** is your running application (the Docker containers). A **Container Instance** is the physical or virtual underlying server (the EC2 instance) that the Task is actually running on.

### 12. How can you manage container secrets in Amazon ECS?
**Answer:** You never hardcode secrets in the Task Definition. Instead, you store them in **AWS Secrets Manager** or **SSM Parameter Store**. In the Task Definition, you reference the Secret ARN. When the task starts, ECS securely injects the secret directly into the container as an environment variable using the Task Execution IAM Role.

### 13. What is the purpose of Amazon ECS Capacity Providers?
**Answer:** Capacity Providers intelligently manage the scaling of the underlying EC2 infrastructure. Instead of manually configuring EC2 Auto Scaling Groups to match your container needs, Capacity Providers use **ECS Cluster Auto Scaling** to automatically provision new EC2 instances precisely when your pending tasks need more compute power.

### 14. Can you use Amazon ECS to orchestrate non-Docker workloads?
**Answer:** No. ECS is specifically built for Docker containers (or compatible OCI containers). If you need to orchestrate non-containerized applications (like standard binaries or WAR files), you would use AWS Elastic Beanstalk or AWS CodeDeploy to EC2.

### 15. How does Amazon ECS integrate with other AWS services?
**Answer:** ECS is deeply integrated into the AWS ecosystem:
* **ECR:** Pulls container images.
* **ALB/NLB:** Distributes traffic to tasks.
* **IAM:** Provides granular security via Task Roles.
* **CloudWatch:** Centralizes logs (awslogs driver) and metrics.

### 16. What is the difference between the Fargate and EC2 launch types in Amazon ECS?
**Answer:** 
* **EC2 Launch Type:** You have root SSH access to the underlying servers, you can run Daemon tasks (one task per instance), and you can use Spot Instances cheaply.
* **Fargate Launch Type:** Serverless. No SSH access. You don't pick instance types; you just declare task CPU/Memory. Extremely low operational overhead.

### 17. How can you manage container networking in Amazon ECS?
**Answer:** The modern standard is the `awsvpc` network mode. This gives every single ECS Task its own dedicated Elastic Network Interface (ENI) and its own private IP address directly from the VPC subnet. This allows you to attach standard AWS Security Groups directly to the Task, providing EC2-level security isolation for containers.

### 18. What is the purpose of the Amazon ECS Task Placement Strategy?
**Answer:** (Only applicable to the EC2 launch type). It determines how tasks are distributed across your instances. 
* **Binpack:** Packs tasks tightly onto the fewest instances to save money.
* **Spread:** Spreads tasks evenly across all Availability Zones or instances for high availability.

### 19. What is the role of the ECS Service Scheduler?
**Answer:** The Service Scheduler monitors the health of your tasks (usually via the Application Load Balancer health checks). If a task crashes or becomes unhealthy, the scheduler deregisters it from the load balancer, kills the container, and schedules a brand new task to replace it, ensuring the "Desired Count" is always met.

### 20. How can you ensure high availability in Amazon ECS?
**Answer:** First, ensure your ECS Cluster spans at least three Availability Zones. Second, configure your ECS Service with a Desired Count > 1 and a "Spread" placement strategy. Finally, place an Application Load Balancer in front of the service to distribute traffic across the healthy tasks in different AZs.
