# AWS Global Accelerator & Network Performance Interview Questions

Delivering fast, reliable experiences to a global user base requires advanced networking. These questions test your knowledge of BGP Anycast and bypassing the public internet.

### 1. What is AWS Global Accelerator?
**Answer:** AWS Global Accelerator is a networking service that improves the availability and performance of your applications with global users. It provides two static IP addresses that act as a fixed entry point to your application endpoints in a single or multiple AWS Regions.

### 2. How does Global Accelerator improve performance?
**Answer:** Normally, if a user in Tokyo accesses a server in Virginia, their traffic hops through dozens of public internet routers, causing latency and packet loss. Global Accelerator routes the user's traffic to the nearest AWS Edge Location in Tokyo, and then securely routes the traffic over the dedicated, fiber-optic **AWS Global Private Network** backbone directly to Virginia, massively reducing latency.

### 3. What is the difference between Amazon CloudFront and Global Accelerator?
**Answer:** 
* **CloudFront** is a Content Delivery Network (CDN) designed to cache HTTP/HTTPS (Layer 7) static assets (images, videos) at the edge.
* **Global Accelerator** does not cache anything. It operates at Layer 4 (TCP/UDP) and simply optimizes the network routing path. It is ideal for non-HTTP traffic like gaming (UDP), IoT MQTT, or Voice over IP.

### 4. How does Global Accelerator use BGP Anycast?
**Answer:** BGP Anycast allows AWS to announce the same two Static IP addresses from multiple AWS Edge Locations worldwide. When a user tries to connect to that IP, the internet naturally routes them to the physically closest edge location, ensuring optimal onboarding onto the AWS network.

### 5. What are Endpoint Groups in Global Accelerator?
**Answer:** You configure Endpoint Groups for each AWS region your application is deployed in (e.g., one for us-east-1, one for eu-west-1). Within those groups, you add the actual endpoints (Application Load Balancers, Network Load Balancers, or EC2 instances).

### 6. How does Global Accelerator handle Disaster Recovery?
**Answer:** Global Accelerator continuously monitors the health of your application endpoints. If the primary region (e.g., US) goes down, Global Accelerator instantly and automatically re-routes all global user traffic to the healthy endpoints in your backup region (e.g., Europe) without relying on DNS propagation delays.

### 7. Why is Global Accelerator better than Route 53 for failover?
**Answer:** Route 53 relies on DNS. If you change a DNS record to failover to a new region, client devices and ISP resolvers often cache the old IP address (ignoring TTLs), meaning users can't access the site for hours. Because Global Accelerator provides Static IPs that never change, failover happens instantly at the AWS routing layer—the client never needs to resolve a new IP.

### 8. Can you use Global Accelerator to protect backend IP addresses?
**Answer:** Yes. Because clients only ever communicate with the two Static Anycast IP addresses provided by Global Accelerator, the actual public IP addresses of your underlying Application Load Balancers or EC2 instances are completely hidden from the internet, protecting them from direct DDoS attacks.

### 9. What is Client IP Preservation in Global Accelerator?
**Answer:** Normally, proxy services strip the original user's IP address. Global Accelerator preserves the original source IP address of the client all the way through to the backend Application Load Balancer or EC2 instance, allowing your application to perform accurate Geo-IP lookups or security filtering.

### 10. Does AWS Global Accelerator provide DDoS protection?
**Answer:** Yes. By default, Global Accelerator is protected by AWS Shield Standard, which defends against massive volumetric DDoS attacks at the edge before the traffic even reaches your VPC.
