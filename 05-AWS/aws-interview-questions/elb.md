# Elastic Load Balancers (ELB) Interview Questions

Elastic Load Balancers act as the traffic cops of AWS. These questions test your knowledge of Layer 4 vs Layer 7 routing, cross-zone balancing, and achieving zero-downtime high availability.

### 1. What is an Elastic Load Balancer (ELB)?
**Answer:** An Elastic Load Balancer is a highly available, managed AWS service that automatically distributes incoming application or network traffic across multiple targets (such as EC2 instances, containers, or Lambda functions) spread across multiple Availability Zones, ensuring fault tolerance and high availability.

### 2. What are the three types of Elastic Load Balancers available in AWS?
**Answer:** 
1. **Application Load Balancer (ALB):** Layer 7 (HTTP/HTTPS) routing.
2. **Network Load Balancer (NLB):** Layer 4 (TCP/UDP) routing for extreme performance.
3. **Gateway Load Balancer (GWLB):** Layer 3 routing, specifically used for deploying and scaling third-party virtual firewalls and intrusion prevention systems.

### 3. What is the main difference between Application Load Balancer (ALB) and Network Load Balancer (NLB)?
**Answer:** ALB operates at the Application Layer (Layer 7 of the OSI model) and can inspect the actual content of the HTTP request to make intelligent routing decisions (like path-based routing). NLB operates at the Transport Layer (Layer 4); it only looks at IP addresses and ports, allowing it to process millions of requests per second at ultra-low latencies.

### 4. What are some key features of the Application Load Balancer (ALB)?
**Answer:** ALB supports advanced Layer 7 features including:
* **Path-Based Routing:** (e.g., routing `/images/*` to an ECS cluster and `/api/*` to EC2 instances).
* **Host-Based Routing:** (e.g., routing `api.example.com` to one target group and `web.example.com` to another).
* Native support for HTTP/2, WebSockets, and integration with AWS WAF (Web Application Firewall) for security.

### 5. When should you use a Network Load Balancer (NLB)?
**Answer:** You use an NLB when you need to load balance non-HTTP traffic (like a custom TCP protocol, database traffic, or UDP-based VoIP systems). It is also the only load balancer that provides a **static IP address** per Availability Zone, which is required if your clients need to whitelist a fixed IP in their corporate firewalls.

### 6. What is a Target Group in Elastic Load Balancing?
**Answer:** A Target Group is a logical grouping of the actual compute resources (EC2 instances, ECS tasks, or Lambda functions). The Load Balancer accepts the incoming traffic on a "Listener" port, evaluates the rules, and then forwards the traffic to the specified Target Group.

### 7. How does health checking work in Elastic Load Balancers?
**Answer:** The ELB continuously sends regular pings (e.g., an HTTP GET request to `/health`) to all targets in the target group. If a target fails to respond with a `200 OK` status consecutively, the ELB marks it as "Unhealthy" and immediately stops routing user traffic to it until it recovers.

### 8. How can you route requests to different Target Groups based on URL paths in an ALB?
**Answer:** You configure **Listener Rules**. You create a rule on the port 443 Listener that states: `IF Path is /checkout/* THEN Forward to target-group-billing`. `ELSE IF Path is /blog/* THEN Forward to target-group-wordpress`. This allows a single ALB to serve multiple microservices.

### 9. What is Cross-Zone Load Balancing?
**Answer:** By default, if AZ-A has 2 instances and AZ-B has 8 instances, an ELB without cross-zone balancing will send 50% of traffic to AZ-A (overloading those 2 instances). **Cross-Zone Load Balancing** ensures that the load balancer node in one AZ can route traffic directly to backend instances in *any* AZ, guaranteeing perfectly even traffic distribution across all 10 instances.

### 10. How can you enable SSL/TLS encryption for traffic between clients and the load balancer?
**Answer:** You use **AWS Certificate Manager (ACM)** to provision a free, auto-renewing SSL/TLS certificate. You attach this certificate to the HTTPS (Port 443) Listener on your ALB. This allows the ALB to perform "SSL Termination," decrypting the traffic at the load balancer level and sending plain HTTP to the backend targets to save CPU cycles on your servers.

### 11. Can you use an Elastic Load Balancer (ELB) with resources outside AWS?
**Answer:** Yes. You can create a Target Group and register the **IP Addresses** of your on-premises servers (connected via AWS Direct Connect or Site-to-Site VPN). This allows an ALB/NLB to distribute traffic hybridly across both AWS EC2 instances and your physical data center.

### 12. What is a Sticky Session, and how can you enable it in Elastic Load Balancers?
**Answer:** Sticky Sessions (Session Affinity) ensure that a specific user's requests are consistently routed to the exact same backend EC2 instance for the duration of their session (useful if the application stores shopping cart data in local RAM). You enable this at the Target Group level, and the ALB issues a cookie to the client to track the session.

### 13. What is the purpose of Pre-Warming in Elastic Load Balancers?
**Answer:** ELBs automatically scale to handle massive traffic, but this scaling takes 1–5 minutes. If you expect an instant, massive spike in traffic (e.g., a Super Bowl ad or a flash sale), the ELB might drop packets before it scales. You can contact AWS Support to "pre-warm" the ELB, forcing it to scale to maximum capacity before the event begins.

### 14. How does Elastic Load Balancer support IPv6?
**Answer:** You can configure ALBs and NLBs as "Dualstack." This assigns both an IPv4 and an IPv6 address to the load balancer, allowing modern mobile clients and IoT devices to connect natively over IPv6, while still supporting legacy IPv4 traffic.

### 15. What is Connection Draining (Deregistration Delay), and when is it useful?
**Answer:** When an instance becomes unhealthy or an Auto Scaling Group attempts to terminate it, Connection Draining pauses the termination for a specified period (e.g., 300 seconds). The ELB stops sending *new* requests to the instance, but allows *in-flight* requests (like a large file download) to complete successfully before the server is killed.

### 16. How can you enable Access Logs for Elastic Load Balancers?
**Answer:** You can enable Access Logs in the Load Balancer attributes and specify an Amazon S3 bucket. The ALB will deliver detailed log files (containing the client IP, request path, HTTP response code, and processing time) to S3, which you can then analyze using Amazon Athena for auditing or troubleshooting.

### 17. What is the purpose of an Idle Timeout setting in Elastic Load Balancers?
**Answer:** The idle timeout (default 60 seconds) is the maximum time a connection can remain open with no data transmitted. If a backend EC2 instance takes longer than 60 seconds to process a massive database query and return a response, the ALB will close the connection and return an HTTP 504 Gateway Timeout error to the user.

### 18. Can you associate Elastic IP addresses with Elastic Load Balancers?
**Answer:** You **cannot** assign an Elastic IP to an Application Load Balancer (ALB); it only provides a dynamic DNS name (e.g., `my-alb-123.us-east-1.elb.amazonaws.com`). However, you **can** assign an Elastic IP to a Network Load Balancer (NLB), giving it a fixed static IP address per Availability Zone.

### 19. How can you configure Health Checks for targets in Elastic Load Balancers?
**Answer:** In the Target Group settings, you define the Protocol (HTTP), the Port (80), and the Path (e.g., `/health-check.php`). You also configure the Interval (ping every 30 seconds), the Timeout (wait 5 seconds for a response), and the Thresholds (mark healthy after 2 successes, mark unhealthy after 2 consecutive failures).

### 20. Can you use Elastic Load Balancers to distribute traffic across regions?
**Answer:** No, ELBs are strictly regional services; they can only distribute traffic across Availability Zones within a single AWS region. To route traffic globally across multiple AWS regions (e.g., US-East and EU-West), you must place **Amazon Route 53** (with Geolocation or Latency-based routing) or **AWS Global Accelerator** in front of your regional ELBs.
