# Cloud Migration Interview Questions

Cloud migration is a massive industry topic. These questions test your architectural strategy, risk management, and understanding of the famous "6 R's" of migration.

### 1. What is cloud migration?
**Answer:** Cloud migration is the complex process of moving an organization's digital assets—including applications, databases, IT resources, and workloads—from physical on-premises data centers (or from one cloud provider to another) into a cloud computing environment like AWS.

### 2. What are the common drivers for cloud migration?
**Answer:** The primary business drivers include massive cost savings (shifting from CapEx to OpEx), elasticity and scalability to handle traffic spikes, increased developer agility, high availability/disaster recovery, and unlocking access to advanced managed services (like AI/ML or serverless databases).

### 3. What are the seven cloud migration strategies (The 7 R's)?
**Answer:** The modern AWS migration framework defines the 7 R's: 
1. **Rehost** (Lift and Shift)
2. **Replatform** (Lift, Tinker, and Shift)
3. **Repurchase** (Drop and Shop / SaaS)
4. **Refactor** (Rearchitect)
5. **Relocate** (Hypervisor-level lift and shift, e.g., VMware Cloud on AWS)
6. **Retire** (Decommission)
7. **Retain** (Do nothing for now)

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

### 10. What is the AWS Cloud Adoption Framework (CAF)?
**Answer:** AWS CAF helps organizations build a comprehensive approach to cloud computing throughout the IT lifecycle. It breaks migration readiness into 6 Perspectives: Business, People, Governance, Platform, Security, and Operations. This ensures the company doesn't just focus on technology, but also prepares its HR, finance, and security teams for the cloud transition.

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

### 19. What is the AWS Migration Acceleration Program (MAP)?
**Answer:** MAP is a comprehensive cloud migration program that provides financial incentives (AWS Credits) to help organizations offset the "double-bubble" cost of maintaining on-premises hardware while simultaneously building AWS infrastructure. It follows a strict 3-phase methodology: Assess, Mobilize, and Migrate & Modernize.

### 20. What is the importance of testing in cloud migration?
**Answer:** A migration isn't done just because the data moved. Rigorous testing—including User Acceptance Testing (UAT), performance/load testing to ensure cloud latency is acceptable, and security penetration testing—is absolutely mandatory before updating DNS records to point live customer traffic to the new AWS environment.

### 21. What is AWS Migration Hub?
**Answer:** AWS Migration Hub provides a single location to track the progress of application migrations across multiple AWS and partner solutions. It allows you to monitor the status of all your migrations in one centralized dashboard, preventing you from losing track of hundreds of moving servers.

### 22. When would you use AWS DataSync versus the AWS Snow Family?
**Answer:** Use **AWS DataSync** when you have a fast, reliable internet connection (or Direct Connect) and need to continuously sync network file systems (NFS/SMB) directly into S3 or EFS. Use the **AWS Snow Family** (Snowcone, Snowball, Snowmobile) for offline data transfer when you have massive petabyte-scale datasets where migrating over the internet would take months.

### 23. What are the common pitfalls of a Cloud Migration?
**Answer:** Common pitfalls include "migrating zombies" (lifting and shifting over-provisioned servers without right-sizing them first), ignoring software licensing rules (moving physical core-bound licenses to shared EC2 instances), and underestimating data egress costs between chatty microservices placed in different Availability Zones.

### 24. How does the AWS Well-Architected Framework apply to migration?
**Answer:** The framework is applied during the final "Optimize" phase of migration. Once the application is running in AWS, an architect reviews it against the six pillars (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, and Sustainability) to continually modernize and improve the workload.

### 25. What is AWS Application Migration Service (MGN)?
**Answer:** AWS MGN is the primary service for the "Rehost" (Lift and Shift) strategy. It works by installing an agent on your physical or virtual servers, which then performs continuous, block-level replication of the hard drives directly into an AWS staging area, allowing for near-zero downtime cutovers to EC2.

### 26. How do you migrate a monolithic application without downtime?
**Answer:** You use the **Strangler Fig Pattern**. Instead of rewriting the entire monolith at once, you place an API Gateway in front of it. You extract one feature (e.g., "Billing") and rewrite it as a cloud-native microservice. You route only `/billing` traffic to the new microservice and the rest to the monolith. You repeat this until the monolith is fully "strangled" and retired.

### 27. What is the difference between AWS Application Discovery Service and AWS Migration Evaluator?
**Answer:** Both are used in the planning phase, but for different audiences. **Migration Evaluator** is for executives; it analyzes CPU/RAM usage to build a financial business case and TCO (Total Cost of Ownership). **Application Discovery Service (ADS)** is for engineers; it maps network dependencies to ensure you don't migrate a web server but accidentally leave its connected database on-premises.

### 28. What is the AWS Schema Conversion Tool (SCT)?
**Answer:** When performing a *heterogeneous* database migration (e.g., moving from an on-premise Oracle DB to Amazon Aurora PostgreSQL), the AWS Database Migration Service (DMS) can move the data, but it cannot convert the structure. You must run SCT first to automatically convert the source database schema, views, and stored procedures into a format compatible with the target engine.

### 29. What is VMware Cloud on AWS and which migration strategy does it represent?
**Answer:** VMware Cloud on AWS allows you to run your existing VMware vSphere environments natively on AWS bare-metal infrastructure. It represents the **"Relocate"** migration strategy, allowing sysadmins to lift-and-shift entire data centers to AWS in days without changing their hypervisor, operational tools, or network settings.

### 30. What happened to AWS Server Migration Service (SMS)?
**Answer:** AWS Server Migration Service (SMS) is deprecated. AWS officially replaced it with the **AWS Application Migration Service (MGN)**. MGN is faster, uses continuous block-level replication (instead of SMS's snapshot-based approach), and allows for much smaller cutover windows.
