# AWS Elastic Beanstalk Interview Questions

AWS Elastic Beanstalk is the original Platform-as-a-Service (PaaS) on AWS. These questions test your understanding of rapid deployment, environment management, and abstracting infrastructure.

### 1. What is AWS Elastic Beanstalk?
**Answer:** AWS Elastic Beanstalk is an easy-to-use Platform-as-a-Service (PaaS) that abstracts away the underlying AWS infrastructure. Developers simply upload their application code, and Elastic Beanstalk automatically handles the provisioning of EC2 instances, load balancing, auto-scaling, and application health monitoring.

### 2. How does Elastic Beanstalk work?
**Answer:** Under the hood, Elastic Beanstalk uses AWS CloudFormation to build the infrastructure. It creates an environment with an Auto Scaling Group, an Elastic Load Balancer, and Security Groups. It then deploys your application code onto the EC2 instances using a pre-configured runtime environment.

### 3. What languages and platforms does Elastic Beanstalk support?
**Answer:** Elastic Beanstalk supports a wide variety of platforms natively, including Java (Tomcat), .NET (IIS), PHP, Node.js, Python, Ruby, and Go. It also supports Single Container, Multicontainer, and preconfigured Docker environments.

### 4. What is an Elastic Beanstalk Environment?
**Answer:** In Elastic Beanstalk, an "Application" is merely a logical folder. Inside that application, you create "Environments." An environment is the actual running infrastructure (servers, load balancers). You typically create distinct environments for `myapp-dev`, `myapp-qa`, and `myapp-prod`.

### 5. How does Elastic Beanstalk handle updates and deployments?
**Answer:** Elastic Beanstalk offers several deployment policies depending on your downtime tolerance:
* **All at Once:** Fastest, but causes downtime.
* **Rolling:** Deploys in batches, maintaining partial capacity.
* **Rolling with Additional Batch:** Spins up new instances first, ensuring 100% capacity is maintained during the rollout.
* **Immutable:** Spins up an entirely new Auto Scaling group for the new code, swapping them only if successful.

### 6. Can you customize the infrastructure in Elastic Beanstalk?
**Answer:** Yes. While Elastic Beanstalk abstracts the infrastructure, it does not hide it. You can fully customize the environment (e.g., changing EC2 instance types, modifying Load Balancer listeners, or tweaking Auto Scaling rules) through the AWS Console, the EB CLI, or `.ebextensions` configuration files.

### 7. How can you monitor the health of an Elastic Beanstalk environment?
**Answer:** Elastic Beanstalk integrates natively with Amazon CloudWatch. It provides an "Enhanced Health Reporting" dashboard that aggregates metrics (CPU, latency, HTTP 4xx/5xx errors) from the Load Balancer and EC2 instances, grading the environment color-coded status (Green, Yellow, Red).

### 8. What is the Elastic Beanstalk Command Line Interface (EB CLI)?
**Answer:** The EB CLI is a dedicated command-line tool specifically designed for developers. It simplifies daily workflows, allowing developers to type `eb create` to spin up a new environment, or `eb deploy` to push local code changes to AWS in seconds without using the AWS console.

### 9. How does Elastic Beanstalk handle automatic scaling?
**Answer:** Elastic Beanstalk utilizes Amazon EC2 Auto Scaling. You configure "Scaling Triggers" (for example, triggering a scale-out if the `NetworkOut` metric exceeds 6MB or if `CPUUtilization` exceeds 75%). The environment will automatically add or remove EC2 instances to match user demand.

### 10. Explain the difference between Single Instance and Load Balanced environments.
**Answer:** 
* **Single Instance Environment:** Uses one EC2 instance and assigns an Elastic IP to it. There is no Load Balancer. It is used for cheap development or testing.
* **Load Balanced, Auto Scaling Environment:** Places an Application Load Balancer in front of an Auto Scaling Group containing multiple EC2 instances. This is required for highly available Production workloads.

### 11. How does Elastic Beanstalk support rolling back deployments?
**Answer:** Elastic Beanstalk maintains an "Application Version" history in Amazon S3. If a new deployment crashes your application, you can quickly navigate to the Application Versions screen in the console, select the previous stable version, and click "Deploy" to roll back the environment.

### 12. Can Elastic Beanstalk deploy applications to multiple Availability Zones?
**Answer:** Yes. When configuring a Load Balanced environment, Elastic Beanstalk automatically distributes your EC2 instances evenly across multiple Availability Zones (AZs) within the chosen region, ensuring that if one entire data center fails, your application remains online.

### 13. How can you handle environment-specific configurations in Elastic Beanstalk?
**Answer:** The best practice is to use `.ebextensions`—special YAML or JSON configuration files stored in an `.ebextensions/` folder in your source code. These files allow you to execute custom scripts, modify OS settings, install Linux packages, or define AWS resources (like an SQS queue) dynamically during deployment.

### 14. Describe how you would configure environment variables in Elastic Beanstalk.
**Answer:** You can define environment variables (called "Environment Properties" in EB) via the AWS Console under the "Software" configuration settings. These properties are passed directly to your application's OS runtime (e.g., accessible via `process.env.DB_HOST` in Node.js), keeping sensitive data out of your source code.

### 15. Can Elastic Beanstalk deploy applications stored in containers?
**Answer:** Yes. If you provide a `Dockerfile` in your source bundle, or a `Dockerrun.aws.json` file pointing to an image in Amazon ECR or Docker Hub, Elastic Beanstalk will provision EC2 instances, install the Docker daemon, and run your containerized application.

### 16. How can you automate deployments to Elastic Beanstalk?
**Answer:** You integrate it with AWS CodePipeline. You set up a pipeline where the "Source" stage is your GitHub repo, and the "Deploy" stage uses the native Elastic Beanstalk deployment provider. Every time a developer merges code to the `main` branch, it automatically deploys to the Beanstalk environment.

### 17. What is the difference between an Environment URL and a CNAME in Elastic Beanstalk?
**Answer:** When you create an environment, AWS automatically assigns it a long, random Environment URL (e.g., `myapp-env.eba-xyz123.us-east-1.elasticbeanstalk.com`). A CNAME is a DNS record you create in Amazon Route 53 to map your own custom, friendly domain name (like `api.mycompany.com`) to that underlying Elastic Beanstalk URL.

### 18. Can Elastic Beanstalk be used for serverless applications?
**Answer:** No. Elastic Beanstalk is strictly a server-based PaaS; it provisions and runs real Amazon EC2 instances under the hood. If you want to deploy a truly serverless application where you manage zero infrastructure, you should use AWS Lambda or AWS Fargate.

### 19. What are Worker Environments in Elastic Beanstalk?
**Answer:** A Worker Environment is designed to process long-running background tasks asynchronously (e.g., processing a video file). Instead of a Load Balancer, a Worker Environment uses an Amazon SQS Queue. A daemon running on the EC2 instances automatically pulls messages from the queue and sends them via HTTP POST to your application code.

### 20. How can you back up and restore an Elastic Beanstalk environment?
**Answer:** Elastic Beanstalk computes are stateless, so the EC2 instances don't need backing up. Your application state is stored in your database (e.g., Amazon RDS). You ensure RDS automated backups are enabled. Furthermore, you can save your entire Elastic Beanstalk configuration as a "Saved Configuration" to instantly spin up an identical clone of the environment if disaster strikes.
