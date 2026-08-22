# AWS Lambda Interview Questions

AWS Lambda is the cornerstone of Serverless computing on AWS. These questions test your knowledge of event-driven architecture, concurrency limits, and cold starts.

### 1. What is AWS Lambda?
**Answer:** AWS Lambda is a serverless, event-driven compute service. It allows you to run code for virtually any type of application or backend service without provisioning, patching, or managing servers. You only pay for the exact compute time you consume, down to the millisecond.

### 2. How does AWS Lambda work?
**Answer:** You upload your code (a deployment package) to AWS. Lambda sits idle, costing nothing. When a configured event occurs (e.g., an HTTP request via API Gateway, or a new file uploaded to S3), Lambda instantly provisions a secure container, executes your code, returns the result, and then spins the container down.

### 3. What are the key benefits of using AWS Lambda?
**Answer:** The primary benefits are zero server maintenance (no OS to patch), continuous and automatic scaling (from 1 request a day to 10,000 requests a second), sub-second metering (making it highly cost-effective), and native integration with almost every other AWS service to build event-driven architectures.

### 4. What types of events can trigger AWS Lambda functions?
**Answer:** Lambda can be triggered synchronously (e.g., via API Gateway, Application Load Balancer), asynchronously (e.g., S3 object creation, SNS notifications, EventBridge rules), or via a poll-based model (e.g., reading messages from an SQS queue or DynamoDB Streams).

### 5. How is concurrency managed in AWS Lambda?
**Answer:** Concurrency is the number of in-flight executions running at the exact same time. By default, AWS sets a soft limit of 1,000 concurrent executions per region per account. If traffic spikes beyond this, Lambda will throttle the requests. You can manage this by setting **Reserved Concurrency** (guaranteeing a specific function always has capacity) or **Provisioned Concurrency** (keeping functions warm).

### 6. What is the maximum execution duration for a single AWS Lambda invocation?
**Answer:** The absolute maximum execution time (timeout) for a single Lambda invocation is **15 minutes** (900 seconds). If your task takes longer than 15 minutes, you should use AWS Step Functions, AWS Batch, or Amazon ECS instead.

### 7. How do you pass data to and from AWS Lambda functions?
**Answer:** Data is passed to the function via the `event` object (a JSON payload containing the trigger details). The `context` object provides runtime information (like the remaining execution time). The function returns data by passing a JSON payload back to the caller (synchronous) or sending it to a configured Destination (asynchronous).

### 8. Can AWS Lambda functions communicate with external resources?
**Answer:** Yes. By default, Lambda functions have internet access and can make API calls to external third-party services (like Stripe or Twilio) or other AWS services using the AWS SDKs.

### 9. What are AWS Lambda Layers?
**Answer:** Layers are a distribution mechanism for libraries, custom runtimes, and other function dependencies. Instead of packaging heavy libraries (like `numpy` or `pandas`) into every single Lambda deployment package, you put them in a Layer. Multiple Lambda functions can reference the same Layer, drastically reducing deployment package size and build times.

### 10. How can you handle errors in AWS Lambda functions?
**Answer:** Inside the code, you use standard `try-catch` blocks. For infrastructure-level errors on asynchronous invocations (e.g., the function crashes due to bad data), Lambda automatically retries the event twice. If it fails a third time, you can configure Lambda to send the failed event to a **Dead Letter Queue (DLQ)** (SQS or SNS) for manual debugging.

### 11. Can AWS Lambda functions access the internet if placed inside a VPC?
**Answer:** By default, yes. However, if you attach a Lambda function to a private VPC subnet (to access a private RDS database), it **loses** default internet access. To restore internet access, you must route the subnet's traffic through a **NAT Gateway** located in a public subnet.

### 12. What are the execution environments available for AWS Lambda functions?
**Answer:** AWS natively provides managed runtimes for Node.js, Python, Java, Go, Ruby, and .NET. If you want to use a language that isn't officially supported (like Rust or PHP), you can use the **Custom Runtime API** or deploy your Lambda function as a **Docker Container Image** (up to 10GB in size).

### 13. How can you configure environment variables for AWS Lambda functions?
**Answer:** You can set key-value environment variables in the AWS Console or via IaC (Terraform/CloudFormation). These variables are injected into the runtime environment (e.g., `os.environ` in Python) allowing you to pass database connection strings or feature flags without hardcoding them. (Sensitive variables should be encrypted using AWS KMS).

### 14. What is the difference between Synchronous and Asynchronous invocation?
**Answer:** 
* **Synchronous:** The client (e.g., API Gateway) waits for the Lambda function to finish processing and expects a real-time response.
* **Asynchronous:** The client (e.g., Amazon S3) drops the event into an internal Lambda queue and immediately disconnects. Lambda processes the event in the background and does not return a response to the client.

### 15. What is the AWS Lambda Event Source Mapping?
**Answer:** Event Source Mapping is a Lambda resource that reads from an event stream or queue (specifically Amazon SQS, Kinesis, or DynamoDB Streams) and synchronously invokes a Lambda function with batches of those records. Lambda manages the polling infrastructure for you automatically.

### 16. How can you manage permissions for AWS Lambda functions?
**Answer:** There are two distinct permission models:
1. **Execution Role:** An IAM Role assumed by the Lambda function itself, granting it permission to access *other* AWS resources (like reading from S3 or writing to CloudWatch).
2. **Resource-Based Policy:** An IAM policy attached directly to the Lambda function, granting *other* services (like API Gateway or S3) permission to trigger the function.

### 17. What is AWS Step Functions?
**Answer:** AWS Step Functions is a serverless state machine and orchestration service. Because a single Lambda function cannot run longer than 15 minutes or easily handle complex branching logic, Step Functions allow you to chain multiple Lambda functions together visually, handling retries, delays, and state management effortlessly.

### 18. How can you automate the deployment of AWS Lambda functions?
**Answer:** Because zipping up code and dependencies manually is tedious, the industry standard is to use the **AWS Serverless Application Model (SAM)**, the **Serverless Framework**, or **Terraform**. These tools compile your code, package it, upload it to S3, and deploy the CloudFormation stack automatically via a CI/CD pipeline.

### 19. Can AWS Lambda functions connect to on-premises resources?
**Answer:** Yes. You configure the Lambda function to connect to your AWS VPC. If that VPC is connected to your corporate data center via an AWS Site-to-Site VPN or AWS Direct Connect, the Lambda function can securely query your on-premises legacy databases.

### 20. What is the "Cold Start" issue in AWS Lambda?
**Answer:** A Cold Start occurs when a Lambda function is invoked after being idle, or during a massive traffic spike requiring a new concurrent instance. AWS has to download the code, spin up a new container, and boot the runtime (e.g., the Java JVM), which can add several seconds of latency. You can completely eliminate cold starts by purchasing **Provisioned Concurrency**, which keeps instances pre-warmed and ready to respond in double-digit milliseconds.
