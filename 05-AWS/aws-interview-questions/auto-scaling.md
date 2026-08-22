# AWS Auto Scaling Interview Questions

Auto Scaling is essential for cloud elasticity. These questions test your knowledge of scaling policies, Auto Scaling Groups (ASG), and handling traffic spikes.

### 1. What is Amazon EC2 Auto Scaling?
**Answer:** Amazon EC2 Auto Scaling is a service that automatically adds (scales out) or removes (scales in) EC2 instances according to conditions you define. It ensures that you have the correct number of EC2 instances available to handle the load for your application, improving fault tolerance and reducing costs.

### 2. What is an Auto Scaling Group (ASG)?
**Answer:** An Auto Scaling Group is a logical collection of EC2 instances treated as a single unit for scaling and management purposes. You define the Minimum, Maximum, and Desired capacity of the group.

### 3. What is a Launch Template?
**Answer:** A Launch Template specifies the configuration of the EC2 instances that the ASG will launch. It includes the Amazon Machine Image (AMI) ID, instance type, security groups, key pairs, and user-data scripts. (It replaces the older, deprecated "Launch Configurations").

### 4. What is the difference between Minimum, Maximum, and Desired Capacity?
**Answer:** 
* **Minimum:** The absolute lowest number of instances the ASG will run. (Prevents the app from going offline).
* **Maximum:** The absolute highest number of instances the ASG can scale up to. (Prevents runaway cloud bills).
* **Desired:** The number of instances the ASG is currently trying to maintain based on current traffic.

### 5. How does Auto Scaling handle unhealthy instances?
**Answer:** The ASG continuously performs health checks on instances. If an instance fails the EC2 status check or the attached Elastic Load Balancer (ELB) health check, the ASG automatically marks it as unhealthy, terminates it, and launches a brand new replacement instance to maintain the desired capacity.

### 6. What is a Target Tracking Scaling Policy?
**Answer:** Target Tracking is the most common modern scaling policy. You choose a metric (e.g., Average CPU Utilization) and set a target value (e.g., 50%). The ASG automatically calculates and adjusts the number of instances required to keep the average CPU at exactly 50%.

### 7. What is Step Scaling vs Simple Scaling?
**Answer:** 
* **Simple Scaling:** Waits for a CloudWatch alarm, scales the instance count, and then waits for a mandatory "Cooldown Period" before evaluating again.
* **Step Scaling:** Evaluates the *size* of the alarm breach. If CPU hits 60%, it adds 1 instance. If CPU instantly hits 90%, it knows to aggressively add 4 instances immediately without waiting for a cooldown.

### 8. What is Scheduled Scaling?
**Answer:** Scheduled Scaling allows you to scale based on predictable time schedules rather than reactive metrics. For example, if you know traffic spikes every Friday at 9:00 AM, you can schedule the ASG to scale out to 10 instances at 8:45 AM to pre-warm the environment.

### 9. What is an Auto Scaling Cooldown Period?
**Answer:** A cooldown period (default 300 seconds) is a pause after a scaling activity completes. It gives the newly launched EC2 instance time to boot up, install software, and start handling traffic before the ASG evaluates if it needs to launch *another* instance. This prevents the ASG from over-scaling (launching too many instances too quickly).

### 10. How do you integrate an Auto Scaling Group with an Elastic Load Balancer (ELB)?
**Answer:** You attach the ASG to the ELB's Target Group. As the ASG dynamically launches new instances, it automatically registers their IP addresses with the Target Group. When scaling in, it automatically deregisters them, ensuring the Load Balancer always knows where to route traffic.

### 11. What is Connection Draining (Deregistration Delay) during a scale-in event?
**Answer:** When the ASG decides to terminate an instance to scale in, Connection Draining ensures the ELB stops sending *new* requests to the instance, but waits a specified time (e.g., 5 minutes) for existing, in-flight requests (like a large file download) to finish before the instance is actually killed.

### 12. What is an ASG Lifecycle Hook?
**Answer:** Lifecycle Hooks allow you to pause an instance as it launches or terminates. For example, during scale-in (termination), a lifecycle hook can pause the termination for up to an hour so you can run a custom script to securely backup log files to S3 before the instance is permanently destroyed.

### 13. Can an Auto Scaling Group span multiple AWS Regions?
**Answer:** No. An Auto Scaling Group is a regional construct. However, it *should* span multiple Availability Zones (AZs) within that single region to ensure high availability and fault tolerance.

### 14. How does Auto Scaling balance instances across Availability Zones?
**Answer:** The ASG attempts to distribute instances evenly across all specified AZs. If one AZ has 4 instances and another has 2, the next time a scale-out event occurs, the ASG will launch the new instance in the AZ with only 2 instances to restore balance.

### 15. What happens if an entire Availability Zone goes down?
**Answer:** If an AZ goes offline, the ASG will notice that the instances in that AZ are failing health checks. It will automatically attempt to launch replacement instances in the remaining healthy Availability Zones to restore the desired capacity.

### 16. What is Predictive Scaling?
**Answer:** Predictive Scaling uses Machine Learning to analyze 14 days of historical traffic patterns. It then predicts future traffic spikes and proactively scales out the ASG *before* the spike occurs, completely eliminating the "cold start" latency of reactive scaling.

### 17. How can you mix On-Demand and Spot instances in a single ASG?
**Answer:** Using an **Auto Scaling Fleet** (or Mixed Instances Policy in the Launch Template), you can configure the ASG to maintain a baseline of On-Demand instances (for stability) while fulfilling any extra scaled-out capacity using cheap Spot Instances (to save up to 90% on costs).

### 18. What is a Termination Policy?
**Answer:** When an ASG scales in, it must decide *which* instance to kill. The default Termination Policy is to kill the instance in the AZ with the most instances (to maintain balance), and then kill the instance using the oldest Launch Template. You can customize this (e.g., "OldestInstance" or "NewestInstance").

### 19. Can you use Auto Scaling for services other than EC2?
**Answer:** Yes. AWS offers **Application Auto Scaling**, which applies the exact same scaling logic to Amazon ECS tasks, DynamoDB read/write capacity, Aurora Replicas, and EKS nodes.

### 20. What is Instance Scale-In Protection?
**Answer:** If you have an EC2 instance in an ASG that is currently processing a critical 4-hour batch job, you don't want the ASG to terminate it during a routine scale-in event. You can enable "Scale-In Protection" on that specific instance, forcing the ASG to terminate a different instance instead.
