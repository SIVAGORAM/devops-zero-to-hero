# AWS API Gateway Interview Questions

Amazon API Gateway is the front door for Serverless applications. These questions test your knowledge of API design, caching, rate limiting, and securing endpoints via Custom Authorizers.

### 1. What is Amazon API Gateway?
**Answer:** Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure REST, HTTP, and WebSocket APIs at any scale. It acts as the "front door" for applications to access data or business logic running on AWS Lambda, EC2, or anywhere else.

### 2. What types of APIs can you build with API Gateway?
**Answer:** 
1. **REST APIs:** Feature-rich, highly customizable, supports API keys, caching, and complex request/response transformations.
2. **HTTP APIs:** A newer, lightweight, faster, and up to 71% cheaper alternative to REST APIs, ideal for simple Lambda proxy integrations.
3. **WebSocket APIs:** Maintains persistent, stateful, two-way communication between clients and backend services (ideal for real-time chat apps).

### 3. What are the three Endpoint Types in API Gateway?
**Answer:** 
* **Edge-Optimized:** Routes requests to the nearest CloudFront Edge Location, reducing latency for global users.
* **Regional:** Intended for clients located in the same AWS region as the API, preventing unnecessary hops to edge locations.
* **Private:** Only accessible from entirely within an Amazon VPC via VPC Endpoints; strictly blocked from the public internet.

### 4. How does API Gateway integrate with AWS Lambda?
**Answer:** The most common pattern is the **Lambda Proxy Integration**. When a client makes an HTTP request, API Gateway wraps the entire request (headers, query parameters, body) into a massive JSON object and passes it to the Lambda function. The Lambda function processes it and returns a JSON object containing the HTTP status code, headers, and body.

### 5. How can you secure an API in API Gateway?
**Answer:** You can secure APIs using:
* **IAM Permissions:** Require callers to sign requests with AWS SigV4.
* **Amazon Cognito User Pools:** Native integration to validate JWT tokens.
* **Lambda Custom Authorizers:** A Lambda function that executes before your API, executing custom logic to validate a third-party OAuth token (like Auth0 or Okta).
* **API Keys & Usage Plans:** To throttle and monetize third-party developer access.

### 6. What is API Caching in API Gateway?
**Answer:** You can provision a cache (from 0.5 GB to 237 GB) on your API endpoint. When a client requests a specific URL, API Gateway caches the backend response for a specified TTL (Time to Live). Future requests are served directly from the API Gateway cache, massively reducing the load (and cost) on your backend Lambda or RDS databases.

### 7. How do you handle Cross-Origin Resource Sharing (CORS) in API Gateway?
**Answer:** If your frontend React app is hosted on `example.com` but calls an API on `api.com`, the browser will block it unless CORS is enabled. You enable CORS in API Gateway, which automatically creates an `OPTIONS` mock method that returns the `Access-Control-Allow-Origin` headers to the browser, allowing the real `GET`/`POST` request to proceed.

### 8. What is Throttling and Rate Limiting in API Gateway?
**Answer:** To protect backend systems from DDoS attacks or being overwhelmed, API Gateway enforces a default account-level limit of 10,000 requests per second (RPS). You can configure lower limits per specific route (e.g., the `/login` route is limited to 100 RPS) to prevent backend databases from crashing.

### 9. What are Usage Plans and API Keys?
**Answer:** If you are building a public API (like weather data), you can issue API Keys to third-party developers. You associate these keys with a **Usage Plan**, which dictates rate limits (10 requests per second) and quotas (10,000 requests per month). If they exceed the quota, API Gateway returns an HTTP 429 Too Many Requests error.

### 10. Can API Gateway transform requests and responses?
**Answer:** Yes (only in REST APIs). Using **Apache Velocity Template Language (VTL)**, API Gateway can intercept a client's incoming XML request and transform it into JSON before passing it to Lambda. It can also transform the backend's JSON response back into XML before returning it to the client.

### 11. What is an API Gateway Stage?
**Answer:** A Stage is a logical reference to a lifecycle state of your API, such as `dev`, `v1`, or `prod`. When you make changes to an API, they are not live until you explicitly "Deploy" them to a Stage. The stage name becomes part of the URL path (e.g., `api.example.com/v1/users`).

### 12. What are Stage Variables?
**Answer:** Stage Variables act like environment variables for API Gateway. For example, you can set a Stage Variable named `lambda_alias`. In the `dev` stage, it points to the `DEV` alias of your Lambda function. In the `prod` stage, it points to the `PROD` alias, allowing you to use a single API definition to route to different environments.

### 13. Can API Gateway route traffic directly to AWS services without Lambda?
**Answer:** Yes. This is called an **AWS Service Integration**. For example, you can configure API Gateway to accept an HTTP POST request and drop the payload directly into an Amazon SQS queue, Kinesis stream, or DynamoDB table without requiring a Lambda function to act as a middleman, saving latency and money.

### 14. What is a Canary Release Deployment in API Gateway?
**Answer:** A Canary Deployment allows you to safely test a new API version. You deploy the new changes to the `prod` stage, but configure the Canary to only route 10% of user traffic to the new version. If CloudWatch metrics look healthy, you can promote the Canary to handle 100% of the traffic.

### 15. How do you monitor and debug API Gateway?
**Answer:** You enable **CloudWatch Execution Logs** (to see the detailed step-by-step routing and VTL transformations) and **CloudWatch Access Logs** (to see who is calling the API, similar to Nginx logs). You can also enable **AWS X-Ray** tracing to visually see exactly how long API Gateway took to pass the request to Lambda.

### 16. What is Request Validation in API Gateway?
**Answer:** You can define a JSON Schema Model for your API endpoints. Before API Gateway even wakes up your backend Lambda function, it validates the incoming request against the schema. If the client forgot to include a required `email` parameter in the body, API Gateway immediately rejects it with a 400 Bad Request, saving you Lambda compute costs.

### 17. How do WebSocket APIs differ from REST APIs in API Gateway?
**Answer:** REST is stateless and unidirectional (client requests, server responds). WebSocket is stateful and bidirectional. Once a client connects, API Gateway maintains a persistent socket. The server can push data down to the client at any time (e.g., a live sports score update) without the client needing to poll.

### 18. What happens if your backend service takes 40 seconds to respond?
**Answer:** API Gateway has a strict, hard-coded **Integration Timeout of 29 seconds**. If your backend Lambda or EC2 instance takes 30 seconds to process a request, API Gateway will cut the connection at 29 seconds and return an HTTP 504 Gateway Timeout error to the client. Long-running tasks must be handled asynchronously.

### 19. How do you configure a custom domain name for API Gateway?
**Answer:** You request a free SSL certificate in AWS Certificate Manager (ACM). In API Gateway, you attach the ACM certificate to a Custom Domain Name (e.g., `api.mycompany.com`). Finally, you create an Alias record in Route 53 pointing to the API Gateway domain target.

### 20. What is mutual TLS (mTLS) in API Gateway?
**Answer:** Standard TLS ensures the client trusts the server. mTLS ensures the server *also* cryptographically trusts the client. API Gateway can be configured to require clients to present a valid X.509 client certificate issued by a trusted Certificate Authority before the HTTP connection is even established. Used heavily in highly secure B2B financial APIs.
