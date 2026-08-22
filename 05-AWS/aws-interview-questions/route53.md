# Amazon Route 53 Interview Questions

Amazon Route 53 is the highly available, global DNS service of AWS. These questions test your knowledge of domain routing, health checks, and global traffic management.

### 1. What is Amazon Route 53?
**Answer:** Amazon Route 53 is a highly available and scalable global Domain Name System (DNS) web service. It is designed to route end users to internet applications by translating human-readable names (e.g., `www.example.com`) into numeric IP addresses (e.g., `192.0.2.1`). Notably, Route 53 is the only AWS service with a 100% availability SLA.

### 2. What is DNS?
**Answer:** The Domain Name System (DNS) is the "phonebook of the internet." Humans access information online through domain names, but web browsers interact through Internet Protocol (IP) addresses. DNS translates these domain names into IP addresses so browsers can load internet resources.

### 3. How does Amazon Route 53 work?
**Answer:** When a user types a URL into their browser, the request hits a DNS Resolver, which eventually queries the Route 53 Authoritative Name Servers. Route 53 looks up the Hosted Zone for the domain, evaluates the configured routing policies, and returns the appropriate IP address or AWS resource alias back to the user.

### 4. What are the types of routing policies in Amazon Route 53?
**Answer:** Route 53 offers seven advanced routing policies:
1. Simple Routing
2. Weighted Routing
3. Latency-Based Routing
4. Failover Routing
5. Geolocation Routing
6. Geoproximity Routing (Traffic Flow)
7. Multi-Value Answer Routing

### 5. What is the purpose of the Simple Routing Policy in Route 53?
**Answer:** Simple Routing is used for a single resource that performs a given function for your domain, like a single web server that serves the `example.com` website. If you associate multiple IP addresses with a Simple record, Route 53 returns all values in a random order. Note: Simple Routing *cannot* be attached to Health Checks.

### 6. How does the Weighted Routing Policy work in Route 53?
**Answer:** Weighted Routing lets you split traffic across multiple resources in proportions that you specify (e.g., 80% to Server A, 20% to Server B). It is highly useful for A/B testing, Canary deployments, or gradually shifting traffic to a brand new application environment.

### 7. What is the Latency Routing Policy in Amazon Route 53?
**Answer:** Latency Routing ensures global users get the fastest response times. If you have an application deployed in both `us-east-1` (Virginia) and `ap-northeast-1` (Tokyo), Route 53 will evaluate the latency between the user's location and both regions, automatically routing the user to the region that provides the lowest network latency.

### 8. How does the Failover Routing Policy work?
**Answer:** Failover Routing is used to configure active-passive Disaster Recovery. You configure a Primary record (pointing to your main load balancer) and a Secondary record (pointing to a static error page on S3). Route 53 actively monitors the Primary record via Health Checks. If the primary goes down, Route 53 automatically routes all traffic to the Secondary record.

### 9. What is the Geolocation Routing Policy?
**Answer:** Geolocation Routing lets you choose the resources that serve your traffic based on the geographic location of your users (i.e., their IP address). This is critical for localization (e.g., routing users in France to a French-language server) or for enforcing strict legal compliance (e.g., ensuring EU data stays in EU servers).

### 10. What is the Multi-Value Answer Routing Policy?
**Answer:** It is similar to Simple Routing, as it returns multiple IP addresses, but with one critical addition: **Health Checks**. Route 53 checks the health of the resources and only returns the IP addresses of the healthy ones. It acts as a rudimentary, DNS-level load balancer.

### 11. How can you route traffic to an AWS resource using Route 53?
**Answer:** While standard DNS uses `A` records (IPv4) or `CNAME` records (Domain to Domain), Route 53 features a proprietary extension called an **Alias Record**. An Alias Record allows you to map your apex domain (e.g., `example.com`) directly to specific AWS resources like an Application Load Balancer, API Gateway, or S3 bucket.

### 12. Can Route 53 route traffic to non-AWS resources?
**Answer:** Yes. Route 53 functions as a standard authoritative DNS service. You can create standard `A` records pointing to the public IP addresses of servers sitting in your on-premises data center, Azure, or Google Cloud.

### 13. How can you ensure high availability using Route 53?
**Answer:** You combine advanced routing policies with **Route 53 Health Checks**. By creating a Failover Routing policy that monitors the health of an active Application Load Balancer, Route 53 can instantly and automatically failover all global traffic to a backup region if the primary region experiences an outage.

### 14. What are Health Checks in Amazon Route 53?
**Answer:** A Route 53 Health Check consists of a fleet of Route 53 servers situated globally that continuously ping your application endpoint (via HTTP/HTTPS/TCP) every 10 to 30 seconds. If a certain number of global locations agree that the endpoint is not responding, it marks the endpoint as Unhealthy.

### 15. How can you configure a custom domain for an Amazon S3 bucket using Route 53?
**Answer:** First, the S3 bucket name must *exactly* match the domain name (e.g., `www.example.com`). Second, you must enable Static Website Hosting on the bucket. Finally, in Route 53, you create an **Alias `A` Record** pointing to the S3 bucket's website endpoint.

### 16. What is the difference between a CNAME and an Alias Record?
**Answer:** A standard `CNAME` record cannot be used at the "apex" or "root" of a domain (e.g., `example.com`); it can only be used on subdomains (e.g., `www.example.com`). AWS created the **Alias Record** to solve this. Alias records map natively to AWS resources, allow root-domain routing, and are completely free (unlike CNAME queries which incur costs).

### 17. How can you migrate a domain to Amazon Route 53?
**Answer:** 
1. Create a "Hosted Zone" in Route 53.
2. Manually replicate all your existing DNS records (A, MX, TXT) from your current provider into the new Hosted Zone.
3. Update the Name Servers (NS) at your Domain Registrar to point to the four Route 53 Name Servers provided by AWS.

### 18. How does Route 53 support Domain Registration?
**Answer:** In addition to DNS management (Hosted Zones), Route 53 acts as a Domain Registrar (like GoDaddy or Namecheap). You can purchase, register, and auto-renew domain names (like `.com`, `.net`, `.io`) directly through the AWS Console.

### 19. How can you use Route 53 to set up a global website?
**Answer:** You deploy identical copies of your application in multiple regions (e.g., US, Europe, Asia). In Route 53, you create **Latency-Based Routing** records pointing to the Load Balancers in each region. This guarantees that users around the world are always directed to the server closest to them, ensuring massive performance gains.

### 20. What is Route 53 Resolver (Inbound/Outbound Endpoints)?
**Answer:** By default, resources inside a VPC can resolve public internet names and private VPC names. However, if you connect your VPC to an on-premises corporate network via VPN, they cannot resolve each other's private DNS. **Route 53 Resolver** provides endpoints that allow bidirectional DNS resolution between your AWS VPCs and your on-premises data centers.
