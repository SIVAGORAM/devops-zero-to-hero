# Amazon Elastic Container Registry (ECR) Interview Questions

Amazon ECR is the standard image repository for AWS container workloads. These questions test your knowledge of Docker, image security, and integration with services like ECS and EKS.

### 1. What is Amazon Elastic Container Registry (ECR)?
**Answer:** Amazon ECR is a fully managed, highly available, and secure Docker container registry provided by AWS. It allows developers and CI/CD systems to easily store, manage, share, and deploy container images and OCI (Open Container Initiative) artifacts.

### 2. How does Amazon ECR work?
**Answer:** ECR acts as the central hub for your containerized applications. A CI/CD pipeline (like AWS CodeBuild) compiles your code into a Docker image and pushes it to an ECR repository. Compute services like Amazon ECS, Amazon EKS, or AWS Fargate then pull those images from ECR to run the actual application containers.

### 3. What are the key features of Amazon ECR?
**Answer:** Key features include native integration with AWS IAM for strict access control, automated image vulnerability scanning (via AWS Inspector), cross-region and cross-account replication, Lifecycle Policies for cost management, and high availability backed by Amazon S3.

### 4. What is a Docker container image?
**Answer:** A Docker image is a read-only, lightweight, standalone, executable package of software. It contains absolutely everything needed to run an application: the compiled code, runtime environment (e.g., Node.js), system tools, libraries, and configuration settings, ensuring the application runs identically on any environment.

### 5. How do you push Docker images to Amazon ECR?
**Answer:** 
1. Authenticate your Docker CLI to ECR using the `aws ecr get-login-password` command.
2. Build your image using `docker build -t my-app .`.
3. Tag the image with the ECR repository URI using `docker tag`.
4. Push the image using `docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/my-app:latest`.

### 6. How can you pull Docker images from Amazon ECR?
**Answer:** After authenticating the Docker client via the AWS CLI (`aws ecr get-login-password`), you simply run `docker pull <aws_account_id>.dkr.ecr.<region>.amazonaws.com/my-app:latest` to download the image to your local machine or build server.

### 7. What is the significance of Amazon ECR Lifecycle Policies?
**Answer:** Docker images are large and consume S3 storage space. If a CI/CD pipeline pushes a new image every hour, your storage costs will skyrocket. Lifecycle Policies automate cost management by deleting old, untagged, or stale images (e.g., "Delete any untagged image older than 14 days").

### 8. How does Amazon ECR support image vulnerability scanning?
**Answer:** ECR integrates with Amazon Inspector (Basic or Enhanced scanning). You can configure ECR to "Scan on Push," meaning the moment a developer uploads a new Docker image, ECR automatically scans the OS and application dependencies for known Common Vulnerabilities and Exposures (CVEs) and reports them in the AWS console.

### 9. How can you ensure private and secure image storage in Amazon ECR?
**Answer:** ECR repositories are private by default. Security is enforced using standard AWS IAM policies and ECR Resource-Based Policies (similar to S3 bucket policies). You explicitly grant permissions indicating exactly which IAM roles (e.g., the ECS Task Execution Role) are allowed to execute `ecr:BatchGetImage`.

### 10. How does Amazon ECR integrate with Amazon ECS?
**Answer:** ECR and ECS are tightly integrated. In your ECS Task Definition, you simply provide the ECR image URI. When ECS spins up a new task, the ECS Agent uses its IAM Task Execution Role to securely authenticate to ECR, pull the image, and launch the container without needing manual Docker logins.

### 11. What are ECR Lifecycle Policies?
**Answer:** They are JSON-formatted rules attached to a repository that automate the cleanup of images. A rule contains a selection criteria (e.g., `tagStatus: untagged`, `countType: imageCountMoreThan`, `countNumber: 50`) and an action (`expire`). This ensures you only keep the last 50 deployment images and delete the rest.

### 12. Can you use Amazon ECR for multi-region deployments?
**Answer:** Yes. ECR supports Cross-Region Replication. You can configure a registry setting so that when a CI/CD pipeline pushes an image to `us-east-1`, ECR automatically and asynchronously copies that image to an ECR repository in `eu-west-1`. This drastically reduces container startup time (latency) for global ECS/EKS clusters.

### 13. What is Amazon ECR Public?
**Answer:** While standard ECR is strictly private, **ECR Public** (and the ECR Public Gallery) allows you to host container images that anyone in the world can download anonymously without AWS credentials. It is AWS's direct competitor to Docker Hub, used for distributing open-source software.

### 14. How can you improve image build and deployment speed using Amazon ECR?
**Answer:** Docker images are built in layers. If you configure your CI/CD pipeline to pull the previous image from ECR and use it as a cache (`--cache-from`), Docker will only build and push the layers that actually changed (e.g., the application code), rather than rebuilding large base OS layers every time.

### 15. What is the Amazon ECR Docker Credential Helper?
**Answer:** It is a standalone utility (`amazon-ecr-credential-helper`) that makes it easier to use Docker with ECR. Instead of having to manually run the long `aws ecr get-login-password` command before every push/pull, the credential helper automatically intercepts Docker commands and fetches temporary AWS IAM credentials on the fly.

### 16. How does Amazon ECR support image versioning?
**Answer:** ECR uses Image Tags for versioning. You can tag images with semantic versions (e.g., `v1.0.2`), git commit hashes (e.g., `a1b2c3d`), or simply `latest`. Additionally, ECR supports **Image Tag Mutability**—you can configure a repository to be "Immutable," preventing a developer from accidentally overwriting an existing production tag.

### 17. Can you use Amazon ECR with Kubernetes?
**Answer:** Yes. Amazon EKS integrates with ECR out of the box. For self-hosted Kubernetes clusters, you can use ECR by generating a Kubernetes `ImagePullSecret` containing an ECR authorization token, allowing your Kubelets to securely pull images from AWS.

### 18. How does Amazon ECR handle image replication?
**Answer:** Replication is configured at the registry level. You can set up **Cross-Region** replication (e.g., syncing from Virginia to Frankfurt) and **Cross-Account** replication (e.g., pushing from a central "Shared Services" AWS account out to dozens of separate Production AWS accounts).

### 19. What is the cost structure of Amazon ECR?
**Answer:** ECR is priced purely on usage. You pay for the amount of data stored per month (storage cost in GBs) and the amount of data transferred OUT of ECR to the internet or across regions (bandwidth cost). Data transferred from ECR to EC2/ECS within the *same* AWS region is completely free.

### 20. How can you ensure high availability for images in Amazon ECR?
**Answer:** High availability is handled automatically by AWS. ECR is built on top of the Amazon S3 infrastructure, meaning all uploaded container images are automatically replicated across multiple Availability Zones within the region, providing 99.999999911% durability and exceptional availability.
