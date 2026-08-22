# Cloud Migration Interview Questions

Cloud migration is a massive industry topic. These questions test your architectural strategy, risk management, and understanding of the famous "6 R's" of migration.

### 1. What is cloud migration?
**Answer:** Cloud migration is the complex process of moving an organization's digital assets—including applications, databases, IT resources, and workloads—from physical on-premises data centers (or from one cloud provider to another) into a cloud computing environment like AWS.

### 2. What are the common drivers for cloud migration?
**Answer:** The primary business drivers include massive cost savings (shifting from CapEx to OpEx), elasticity and scalability to handle traffic spikes, increased developer agility, high availability/disaster recovery, and unlocking access to advanced managed services (like AI/ML or serverless databases).

### 3. What are the six common cloud migration strategies (The 6 R's)?
**Answer:** The standard AWS migration framework defines the 6 R's: 
1. **Rehost** (Lift and Shift)
2. **Replatform** (Lift, Tinker, and Shift)
3. **Repurchase** (Drop and Shop / SaaS)
4. **Refactor** (Rearchitect)
5. **Retire** (Decommission)
6. **Retain** (Do nothing for now)

### 4. What is the "Lift and Shift" migration strategy (Rehost)?
**Answer:** "Lift and Shift" means taking an application and its data exactly as it exists on-premises and moving it to the cloud without making any code or architecture changes. For example, migrating an on-prem VM directly to an AWS EC2 instance. It is the fastest migration method.

### 5. How does the "Replatform" strategy differ from "Lift and Shift"?
**Answer:** "Replatforming" (or Lift, Tinker, and Shift) involves making minor architectural optimizations to gain cloud benefits without rewriting the core application code. A classic example is moving an on-prem MySQL database not to an EC2 instance, but to a fully managed **Amazon RDS** database to offload maintenance overhead.

### 6. When would you consider the "Repurchase" (Rebuy) strategy?
**Answer:** You use Repurchase when you decide to abandon your legacy custom application and move to a modern, cloud-based Software as a Service (SaaS) solution. A common example is dropping a self-hosted on-premise email server and migrating the entire company to Microsoft Office 365 or Google Workspace.

### 7. What is the "Refactor" (Rearchitect) migration strategy?
**Answer:** Refactoring is the most complex but most rewarding strategy. It involves fundamentally rewriting and rearchitecting the application code to fully utilize cloud-native features. For example, breaking down a massive monolithic application into microservices using Docker (ECS/EKS) and serverless functions (AWS Lambda).

### 8. How do you decide which cloud migration strategy to use?
**Answer:** The decision relies heavily on the organization's business goals, timeline, and budget. If they need to evacuate a data center in 2 months, **Rehost** is the only option. If they want long-term scalability and cost reduction, and have 2 years to do it, **Refactor** is the best path.

### 9. What are some key benefits of the "Refactor" (Rearchitect) strategy?
**Answer:** By going fully cloud-native, you achieve maximum elasticity (scaling to zero when not in use), drastically reduced operational overhead (no OS to patch in serverless), massive performance boosts, and optimized cloud billing.

### 10. What is the importance of a Migration Readiness Assessment (MRA)?
**Answer:** An MRA is the critical discovery phase. Before touching any code, you evaluate the organization's current IT landscape, security compliance, staff cloud skills, and business objectives. It prevents disastrous migrations by identifying technical debt and application dependencies early.

### 11. How can you minimize downtime during cloud migration?
**Answer:** I would utilize advanced deployment strategies such as **Blue-Green Deployments** or **Canary Releases** via AWS Route 53 traffic shifting. This allows me to run the on-premise and cloud environments simultaneously, routing a small percentage of traffic to the cloud to validate performance before fully cutting over.

### 12. What is data migration in the context of cloud migration?
**Answer:** Data migration is often the hardest part of cloud migration. It involves securely and consistently moving massive databases or file stores to the cloud without disrupting the live application. AWS tools like **AWS DataSync** (for files), **AWS DMS** (Database Migration Service), and **AWS Snowball** (for physical petabyte transfers) are used here.

### 13. What is the "Big Bang" migration approach?
**Answer:** The "Big Bang" approach involves a massive, coordinated cutover where all applications and data are migrated to the cloud over a single weekend. It is extremely high-risk due to potential catastrophic failures, but is sometimes necessary if tight data center lease expirations are approaching.

### 14. What is the "Staged" (Phased) migration approach?
**Answer:** A staged approach is much safer. You migrate non-critical applications or specific microservices one by one over several months. This mitigates risk, allows the team to learn from early mistakes, and builds confidence in the cloud infrastructure.

### 15. How does the "Strangler Fig" migration pattern work?
**Answer:** The Strangler Fig pattern is heavily used in **Refactoring**. Instead of rewriting a monolith all at once, you intercept traffic at an API Gateway and gradually route specific paths (e.g., `/billing`) to newly written cloud microservices. Over time, the cloud microservices "strangle" the on-prem monolith until nothing is left of it.

### 16. What role does automation play in cloud migration?
**Answer:** Automation is critical for repeatable success. By using Infrastructure as Code (Terraform/CloudFormation) and Configuration Management (Ansible), you ensure that the target cloud environment is provisioned identically and securely across Dev, Staging, and Prod without human error.

### 17. How do you ensure security during cloud migration?
**Answer:** Security is a continuous process. During transit, all data must be encrypted via VPN or AWS Direct Connect. Upon arrival in AWS, data must be encrypted at rest (KMS). Additionally, strict IAM least-privilege roles, Security Groups, and CloudTrail auditing must be established *before* the workload is moved.

### 18. How can you handle application dependencies during migration?
**Answer:** Application dependency mapping is vital. If App A relies on Database B, they must be migrated into the same network segment simultaneously to avoid massive latency issues. Tools like AWS Application Discovery Service can automatically map these hidden dependencies on-premises.

### 19. What is the "Lift and Reshape" strategy?
**Answer:** "Lift and Reshape" is a hybrid approach. You first "Lift and Shift" the application to EC2 to quickly exit the on-prem data center. Once safely in the cloud, you immediately "Reshape" it (e.g., resizing instances, moving databases to RDS, adding Auto Scaling) to optimize costs without doing a full refactor.

### 20. What is the importance of testing in cloud migration?
**Answer:** A migration isn't done just because the data moved. Rigorous testing—including User Acceptance Testing (UAT), performance/load testing to ensure cloud latency is acceptable, and security penetration testing—is absolutely mandatory before updating DNS records to point live customer traffic to the new AWS environment.
