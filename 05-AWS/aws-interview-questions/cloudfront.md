# Amazon CloudFront Interview Questions

Amazon CloudFront is the backbone of global content delivery and performance optimization in AWS. These questions test your knowledge of caching, latency reduction, and edge security.

### 1. What is Amazon CloudFront?
**Answer:** Amazon CloudFront is a fast, highly secure, and programmable Content Delivery Network (CDN) service provided by AWS. It securely accelerates the delivery of static and dynamic web content, video streams, and APIs to users globally with low latency and high transfer speeds.

### 2. How does CloudFront work?
**Answer:** CloudFront caches copies of your content in physical data centers located all over the world (Edge Locations). When a user requests content, CloudFront intelligently routes the request to the Edge Location closest to the user. If the content is cached, it is delivered instantly (a cache hit), drastically reducing latency and offloading traffic from your origin server.

### 3. What are Edge Locations in CloudFront?
**Answer:** Edge Locations are specialized, globally distributed AWS data centers that are specifically built to run CloudFront and Route 53. They store cached content closer to the end users, minimizing the physical distance data must travel across the internet.

### 4. What types of distributions are available in CloudFront?
**Answer:** Historically, CloudFront offered Web Distributions (for standard HTTP/HTTPS content) and RTMP Distributions (for Adobe Flash media streaming). However, RTMP distributions are now deprecated, and modern CloudFront uses standard Web Distributions optimized for both static assets and HTTP-based live video streaming (like HLS/DASH).

### 5. How can you ensure that content in CloudFront is updated?
**Answer:** When you update a file on your server, CloudFront will continue serving the old cached version until it expires. To force an immediate update, you can create an **Invalidation** request in CloudFront to purge the specific file from all Edge Locations globally, forcing them to fetch the fresh content from the origin.

### 6. Can you use custom SSL certificates with CloudFront?
**Answer:** Yes, to serve your website securely via HTTPS using your own domain name (e.g., `https://www.mycompany.com`), you can provision a free SSL/TLS certificate using AWS Certificate Manager (ACM) and attach it directly to your CloudFront distribution.

### 7. What is an Origin in CloudFront?
**Answer:** An Origin is the authoritative source or "backend" where your original content lives. Common origins include an Amazon S3 bucket (for static websites), an Application Load Balancer, an EC2 instance, or even an external on-premises HTTP web server.

### 8. How can you control who accesses content in CloudFront?
**Answer:** To protect premium or private content (like paid video courses or software downloads), you can use CloudFront **Signed URLs** or **Signed Cookies**. These provide temporary, cryptographically signed access to specific files that expire after a set time limit, preventing unauthorized sharing.

### 9. What are Cache Behaviors in CloudFront?
**Answer:** Cache Behaviors define exactly how CloudFront handles different types of requests based on URL path patterns. For example, you can create a behavior for `*.jpg` files with a long TTL (cache duration), and a different behavior for `/api/*` that forwards all headers, cookies, and query strings directly to the backend without caching.

### 10. How can you integrate CloudFront with other AWS services?
**Answer:** CloudFront integrates seamlessly with Amazon S3 for static hosting, Application Load Balancers (ALB) and EC2 for dynamic web applications, AWS WAF (Web Application Firewall) for security, and Lambda@Edge to run custom serverless code directly at the Edge Locations.

### 11. How can you analyze CloudFront distribution performance?
**Answer:** You can enable CloudFront Standard Access Logs, which stream detailed logs of every user request to an Amazon S3 bucket. You can then use Amazon Athena to query the logs, or view built-in CloudFront visual reports to analyze cache hit ratios, popular objects, and viewer geography.

### 12. What is the purpose of CloudFront Behaviors?
**Answer:** They allow you to apply granular routing and caching rules. A single CloudFront distribution can have multiple origins. Behaviors allow you to say: "Send all `/images/*` traffic to my S3 bucket origin, and send all `/checkout/*` traffic to my Application Load Balancer origin."

### 13. Can CloudFront be used for dynamic content?
**Answer:** Absolutely. While traditionally known for static images and videos, CloudFront heavily accelerates dynamic content (like APIs or login pages) by utilizing the dedicated AWS global network backbone, reducing the number of internet hops between the user and your origin server.

### 14. What is a Distribution in CloudFront?
**Answer:** A Distribution is the core configuration unit in CloudFront. It ties together your Origins, your Cache Behaviors, your SSL certificates, and your custom domain names into a single, deployable CDN endpoint (which looks like `d111111abcdef8.cloudfront.net`).

### 15. How does CloudFront handle cache expiration?
**Answer:** CloudFront relies on Time to Live (TTL) settings. You configure Minimum, Maximum, and Default TTLs in the Cache Behavior, but ultimately CloudFront respects the `Cache-Control` HTTP headers returned by your origin server to determine exactly how many seconds an object should stay in the cache.

### 16. What are the benefits of using CloudFront with Amazon S3?
**Answer:** Placing CloudFront in front of S3 provides massive benefits: It drastically reduces global latency for users, enables HTTPS on custom domains (which S3 doesn't support natively), and significantly lowers your AWS bill, as data transfer out of CloudFront is cheaper than data transfer directly out of S3.

### 17. Can CloudFront be used for both HTTP and HTTPS content?
**Answer:** Yes, but best practice dictates enforcing HTTPS. You can configure CloudFront Cache Behaviors with a "Viewer Protocol Policy" set to `Redirect HTTP to HTTPS`, ensuring all users communicate with your application over a secure, encrypted connection.

### 18. How can you measure the performance of CloudFront distributions?
**Answer:** In addition to Access Logs, CloudFront emits near real-time operational metrics to Amazon CloudWatch. You can monitor the Total Requests, Bytes Downloaded, 4xx/5xx Error Rates, and set up CloudWatch Alarms if the error rate spikes unexpectedly.

### 19. What is Origin Shield in CloudFront?
**Answer:** Origin Shield is an advanced caching layer positioned between the Edge Locations and your Origin server. If hundreds of Edge Locations suddenly have a cache miss, they normally all hit your origin at once. Origin Shield collapses these requests into a single request, massively reducing the load on your backend database/server.

### 20. How can CloudFront improve security?
**Answer:** CloudFront acts as a massive shield against DDoS attacks. Because it sits at the edge of the AWS network, it natively integrates with AWS Shield to absorb massive volumetric attacks (like SYN floods) before they ever reach your EC2 instances. You can also attach AWS WAF to block SQL injections and cross-site scripting attacks.
