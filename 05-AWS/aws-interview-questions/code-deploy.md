# AWS CodeDeploy Interview Questions

AWS CodeDeploy is a powerful deployment engine. These questions test your knowledge of deployment strategies, lifecycle hooks, and zero-downtime rollouts across EC2, Lambda, and ECS.

### 1. What is AWS CodeDeploy?
**Answer:** AWS CodeDeploy is a fully managed deployment service that automates software deployments to a variety of compute services such as Amazon EC2, AWS Fargate, AWS Lambda, and even your on-premises servers. It eliminates the need for manual, error-prone software installations.

### 2. How does CodeDeploy work?
**Answer:** CodeDeploy requires an `appspec.yml` file that defines exactly *what* files to copy and *what* scripts to run. It coordinates the rollout by pulling the new application revision (usually from S3 or GitHub), deploying it to the target instances, tracking the success of lifecycle events, and rolling back if health checks fail.

### 3. What are the deployment strategies supported by CodeDeploy?
**Answer:** CodeDeploy supports several deployment types depending on the compute platform:
* **In-Place Deployment:** Stops the application on each instance, installs the new code, and restarts it (Causes slight downtime/reduced capacity).
* **Blue/Green Deployment:** Provisions a brand new environment (Green) with the new code, shifts traffic over at the Load Balancer level, and then destroys the old environment (Blue). (Enables zero-downtime).

### 4. Explain the Blue-Green deployment strategy in CodeDeploy.
**Answer:** In a Blue/Green deployment, the current production environment is "Blue." CodeDeploy provisions an exact clone of your environment, "Green," and deploys the new code there. Once the Green environment passes health checks, CodeDeploy updates your Application Load Balancer (ALB) to instantly route 100% of user traffic to Green. Blue is then kept as a safe rollback backup before being terminated.

### 5. How does CodeDeploy handle rollbacks?
**Answer:** You can configure CodeDeploy for **Automated Rollbacks**. If a deployment fails (e.g., an installation script exits with an error) or if a predefined CloudWatch Alarm is triggered (e.g., CPU spikes to 100% during the rollout), CodeDeploy immediately stops the deployment and automatically redeploys the last known good version of the application.

### 6. Can you use CodeDeploy for serverless deployments?
**Answer:** Yes, CodeDeploy natively supports AWS Lambda. Instead of replacing code on a server, it manages traffic shifting. Using alias routing, CodeDeploy can gradually shift traffic (e.g., 10% per minute) from the old Lambda function version to the new version, allowing for safe, monitored rollouts.

### 7. What is an Application Revision in CodeDeploy?
**Answer:** An Application Revision is an archive file (usually a `.zip` or `.tar`) stored in Amazon S3 or GitHub. It contains your compiled application source code, static assets, and the all-important `appspec.yml` file, along with any Bash/PowerShell scripts required for the installation.

### 8. How can you integrate CodeDeploy with your CI/CD pipeline?
**Answer:** CodeDeploy is the final stage in AWS CodePipeline. After the "Source" stage pulls code and the "Build" stage compiles the artifact, CodePipeline hands that finalized artifact to the "Deploy" stage. CodeDeploy then takes that artifact and pushes it out to your EC2 fleet, ECS cluster, or Lambda functions automatically.

### 9. What is a Deployment Group in CodeDeploy?
**Answer:** A Deployment Group is a specific set of compute resources targeted for a deployment. For EC2, a deployment group is usually defined by AWS Tags (e.g., Deploy to all instances tagged `Environment=Production`) or linked directly to an Auto Scaling Group. You configure deployment strategies and rollback alarms at the Deployment Group level.

### 10. How can you ensure zero downtime during application deployments?
**Answer:** For true zero-downtime, you must use a **Blue/Green Deployment** or an **In-Place "One at a Time"** deployment *behind a Load Balancer*. In the latter, CodeDeploy tells the Load Balancer to drain traffic from a single instance, updates the instance, verifies health checks, registers it back with the Load Balancer, and moves to the next instance.

### 11. Explain how you can manage deployment configuration in CodeDeploy.
**Answer:** Deployment Configurations define the pacing of your rollout. For EC2, you can use AWS-managed configurations like `CodeDeployDefault.OneAtATime`, `HalfAtATime`, or `AllAtOnce`. For Lambda/ECS, you can use Canary configurations (e.g., `Canary10Percent5Minutes` - shift 10% of traffic, wait 5 minutes, then shift the remaining 90%).

### 12. How can you handle database schema changes during deployments?
**Answer:** Managing databases via CodeDeploy is risky. The best practice is to decouple database migrations from the code deployment. You should write application code that is forward-and-backward compatible with the database schema. Database changes (using tools like Flyway or Liquibase) should be run in a separate pipeline step *before* CodeDeploy rolls out the new application code.

### 13. Describe a scenario where you would use the Canary deployment strategy.
**Answer:** You use Canary deployments for high-risk updates. For a massive e-commerce site updating its checkout microservice (Lambda/ECS), you use a `Canary10Percent15Minutes` strategy. This routes 10% of real users to the new code while 90% stay on the old code. You monitor error rates for 15 minutes. If no alarms fire, CodeDeploy shifts the rest of the traffic.

### 14. How does CodeDeploy handle instances with different capacities?
**Answer:** CodeDeploy doesn't care about instance capacity; it cares about health. If you are deploying via an Auto Scaling Group behind an Application Load Balancer, CodeDeploy relies on the ALB health checks to ensure an instance (regardless of size) is capable of serving traffic before moving on to deploy to the next target.

### 15. What are hooks in CodeDeploy?
**Answer:** Hooks are specific lifecycle event triggers defined in the `appspec.yml` file. They allow you to execute custom Bash/PowerShell scripts at exact moments during the deployment. Common hooks include `BeforeInstall` (to stop the old application), `AfterInstall` (to fix file permissions), and `ApplicationStart` (to start the new service).

### 16. How does CodeDeploy ensure consistent deployments across instances?
**Answer:** For EC2 and On-Premises deployments, you must install the **CodeDeploy Agent** on every target server. The agent constantly polls the CodeDeploy service for instructions. When a deployment starts, the agent pulls the revision, executes the `appspec.yml` hooks, and reports the pass/fail status back to the central CodeDeploy service.

### 17. What is the difference between an EC2 deployment and a Lambda deployment in CodeDeploy?
**Answer:** EC2 deployments rely on the `appspec.yml` to run OS-level shell scripts (installing files, restarting systemd services) via the CodeDeploy Agent. Lambda deployments do not use agents or scripts; their `appspec.yml` simply specifies the new Lambda version, and CodeDeploy manages API-level traffic shifting (Linear or Canary) between the old and new version aliases.

### 18. How can you monitor the progress of a deployment in CodeDeploy?
**Answer:** You can view real-time progress in the AWS Console, which shows exactly which lifecycle hook (e.g., `BeforeInstall`, `ApplicationStart`) each specific instance is currently executing. You can also view the raw stdout/stderr logs of your bash scripts directly in the console if a deployment fails.

### 19. Can CodeDeploy deploy applications across multiple regions?
**Answer:** A single CodeDeploy deployment is region-specific. However, you can easily deploy to multiple regions by using AWS CodePipeline. You simply configure your pipeline with multiple deployment stages (e.g., `Deploy-US-East-1` followed by `Deploy-EU-West-1`), triggering separate regional CodeDeploy projects.

### 20. What is the role of the CodeDeploy agent?
**Answer:** The CodeDeploy agent is a small software package running as a daemon/service on EC2 instances or on-premises servers. It authenticates with AWS via IAM roles, securely downloads the application revision from S3/GitHub, executes the scripts defined in the `appspec.yml`, and acts as the vital communication link reporting success or failure back to the AWS console.
