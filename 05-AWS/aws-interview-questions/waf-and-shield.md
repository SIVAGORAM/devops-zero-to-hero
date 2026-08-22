# AWS WAF & Shield (Security) Interview Questions

Protecting public-facing infrastructure from DDoS attacks and SQL injections is critical. These questions test your knowledge of Layer 7 application security and perimeter defense.

### 1. What is AWS WAF?
**Answer:** AWS Web Application Firewall (WAF) is a Layer 7 security service that helps protect your web applications and APIs against common web exploits and bots that could affect availability, compromise security, or consume excessive resources.

### 2. Where can you deploy AWS WAF?
**Answer:** AWS WAF cannot be attached directly to an EC2 instance. It must be attached to an edge or routing service. Supported services include:
* Amazon CloudFront (Global)
* Application Load Balancer (ALB) (Regional)
* Amazon API Gateway (Regional)
* AWS AppSync (Regional)

### 3. What types of attacks does AWS WAF protect against?
**Answer:** WAF inspects the incoming HTTP/HTTPS headers and body. It protects against OWASP Top 10 vulnerabilities, specifically **SQL Injection (SQLi)**, **Cross-Site Scripting (XSS)**, HTTP flood attacks, and malicious bot scraping.

### 4. What are Web ACLs and Rules in AWS WAF?
**Answer:** A Web Access Control List (Web ACL) is a container for Rules. A Rule defines inspection criteria (e.g., "Does the User-Agent contain 'BadBot'?"). If a request matches a Rule, WAF takes an Action: **Allow**, **Block**, or **Count** (monitor without blocking).

### 5. What are AWS Managed Rules for WAF?
**Answer:** Instead of writing complex Regex rules manually to catch every known SQL injection variant, AWS provides Managed Rule Groups. These are pre-configured sets of rules curated by the AWS Threat Intelligence team (or third parties like Fortinet/F5) that automatically update to block the latest zero-day vulnerabilities.

### 6. What is AWS Shield?
**Answer:** AWS Shield is a managed Distributed Denial of Service (DDoS) protection service that safeguards applications running on AWS. It operates at Layer 3 (Network) and Layer 4 (Transport), protecting against SYN floods and UDP reflection attacks.

### 7. What is the difference between AWS Shield Standard and AWS Shield Advanced?
**Answer:** 
* **Shield Standard:** Enabled automatically and free for all AWS customers. It protects against 96% of common, large-scale DDoS attacks.
* **Shield Advanced:** Costs $3,000/month. It provides tailored detection for your specific application, 24/7 direct access to the AWS DDoS Response Team (DRT), and **cost protection** (AWS refunds you if a DDoS attack causes your EC2 auto-scaling bill to spike).

### 8. How do AWS WAF and AWS Shield work together?
**Answer:** AWS Shield provides perimeter defense at Layer 3/Layer 4 to stop massive volumetric attacks (flooding the network with junk packets). AWS WAF provides Layer 7 defense, stopping sophisticated, smaller-scale attacks like an attacker sending thousands of complex SQL queries to purposefully exhaust your database CPU.

### 9. What is Rate-Based Rule in AWS WAF?
**Answer:** A rate-based rule tracks the rate of requests for each originating IP address. If an IP address exceeds the threshold you define (e.g., more than 100 requests per 5 minutes), AWS WAF automatically blocks further requests from that IP until the rate drops below the threshold. It is essential for stopping HTTP floods and brute-force login attempts.

### 10. How can you block traffic from specific countries using WAF?
**Answer:** You can create a Geo-Match rule. AWS WAF evaluates the source IP address of the request, determines its country of origin, and can instantly drop the packet. For example, an internal US corporate application can explicitly block all traffic originating from outside North America.

### 11. Can AWS WAF inspect HTTPS traffic?
**Answer:** Yes. Because WAF is deployed on the CloudFront distribution or ALB (which terminate the SSL/TLS connection using ACM certificates), the WAF engine is able to inspect the decrypted, plain-text HTTP payload before it is forwarded to your backend servers.

### 12. What is AWS Firewall Manager?
**Answer:** If you have 50 AWS accounts in an AWS Organization, configuring WAF manually in every account is a nightmare. AWS Firewall Manager allows you to centrally define a master WAF policy (e.g., "All ALBs must have the SQL Injection rule applied") and automatically pushes that rule out to all ALBs across all 50 AWS accounts.

### 13. How do you test a new WAF rule without accidentally breaking your website?
**Answer:** You set the Rule Action to **"Count"**. WAF evaluates traffic against the rule, but instead of blocking it, it just logs the match to CloudWatch. You review the logs for a few days to ensure legitimate users (false positives) aren't triggering the rule. Once confident, you flip the action to **"Block"**.

### 14. What are IP Sets in AWS WAF?
**Answer:** An IP Set is a reusable list of IP addresses or CIDR blocks. You can create an IP Set containing the IP addresses of your corporate VPN and use it in a WAF rule to bypass security checks for internal employees, or use a third-party IP Set of known malicious IP addresses to block them outright.

### 15. How do you monitor blocked requests in AWS WAF?
**Answer:** WAF natively integrates with Amazon CloudWatch for aggregate metrics. For deep forensics, you enable WAF Logging to an **S3 Bucket, Kinesis Data Firehose, or CloudWatch Logs**. The logs contain the full HTTP headers, source IP, and the exact WAF rule that triggered the block.

### 16. What is WAF Bot Control?
**Answer:** AWS WAF Bot Control is a managed rule group that gives you visibility and control over pervasive bot traffic. It can distinguish between "Good Bots" (like Google SEO scrapers) and "Bad Bots" (like content scrapers or inventory hoarders) and block the bad ones to save server capacity.

### 17. How quickly do AWS WAF rules propagate?
**Answer:** When you update a Web ACL rule, the change propagates globally across all Amazon CloudFront edge locations usually within 1 to 2 minutes, allowing you to react incredibly quickly to a zero-day exploit.

### 18. What is the WAF capacity (WCU) limit?
**Answer:** WAF uses Web ACL Capacity Units (WCUs) to measure the computing resources required to evaluate your rules. A simple IP block might cost 1 WCU, while a complex Regex rule might cost 25 WCUs. By default, a single Web ACL is limited to **1,500 WCUs**, preventing you from writing rules so complex they introduce latency.

### 19. How does AWS Shield Advanced mitigate DDoS attacks?
**Answer:** During an attack, Shield Advanced automatically deploys inline mitigations. It uses advanced routing techniques (like BGP Anycast) to absorb the massive traffic spike across AWS's massive global network backbone, isolating the attack at the edge so it never reaches your actual VPC or EC2 instances.

### 20. Does AWS WAF protect resources hosted outside of AWS?
**Answer:** Yes, if you use Amazon CloudFront as a CDN for your on-premises web servers. By attaching AWS WAF to the CloudFront distribution, all incoming internet traffic is scrubbed by WAF at the AWS Edge before it is forwarded to your on-premises data center.
