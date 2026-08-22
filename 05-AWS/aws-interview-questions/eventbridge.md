# AWS EventBridge Interview Questions

Amazon EventBridge (formerly CloudWatch Events) is the central nervous system of AWS event-driven architectures. These questions test your knowledge of event buses, rules, and decoupling microservices.

### 1. What is Amazon EventBridge?
**Answer:** Amazon EventBridge is a serverless event bus service that makes it easy to connect applications together using data from your own applications, integrated Software-as-a-Service (SaaS) applications, and AWS services.

### 2. How does EventBridge differ from Amazon SNS?
**Answer:** While both are used to decouple applications:
* **SNS** is a Pub/Sub service that blindly pushes messages to all subscribers.
* **EventBridge** is an Event Bus that uses complex JSON pattern matching (Rules) to intelligently route specific events only to specific targets. It also natively integrates with third-party SaaS providers (like Datadog or Zendesk).

### 3. What is an Event Bus?
**Answer:** An Event Bus is a pipeline that receives events. Every AWS account has a "Default" event bus that receives all AWS infrastructure events (e.g., an EC2 instance terminating). You can also create Custom event buses for your own application events, or Partner event buses for SaaS integrations.

### 4. What is an EventBridge Rule?
**Answer:** A Rule watches for specific events on an event bus. You define an "Event Pattern" (a JSON filter). When an incoming event matches that pattern (e.g., "Source is EC2 AND State is Terminated"), the Rule routes that event to one or more Target services to take action.

### 5. What are common Targets for EventBridge Rules?
**Answer:** EventBridge can route events to over 20 different AWS targets. The most common are AWS Lambda functions (to run code), Amazon SNS topics (to send alerts), Amazon SQS queues (to buffer events), and AWS Step Functions (to trigger a workflow).

### 6. Can EventBridge run tasks on a schedule?
**Answer:** Yes. Similar to a Linux `cron` job, you can create an EventBridge Scheduled Rule. You can define a fixed rate (e.g., "Rate: 5 minutes") or a Cron expression (e.g., "Cron: 0 12 * * ? *" to run every day at noon) to trigger a Lambda function or an ECS task.

### 7. What is an EventBridge Schema Registry?
**Answer:** When building event-driven applications, developers need to know what the JSON structure of an event looks like. The Schema Registry automatically discovers, parses, and stores the schemas of events passing through your bus. Developers can then download code bindings (in Java, Python, TS) to easily map those JSON events directly into application objects.

### 8. What happens if EventBridge fails to deliver an event to a Target?
**Answer:** EventBridge provides automatic retries for up to 24 hours. If it absolutely cannot deliver the event (e.g., the target Lambda function has been deleted, or permissions are missing), you can configure EventBridge to send the failed event to a **Dead-Letter Queue (DLQ)** (an Amazon SQS queue) for manual debugging.

### 9. How do you handle Cross-Account event routing?
**Answer:** You can configure the EventBridge bus in Account A to route specific events directly to the EventBridge bus in Account B. This is critical in enterprise architectures where a central "Security Account" needs to listen for security breaches happening across dozens of other "Dev" and "Prod" accounts.

### 10. Can you modify an event before EventBridge sends it to a Target?
**Answer:** Yes, using the **Input Transformer**. Instead of sending the massive, raw JSON event from AWS, you can use the Input Transformer to extract just the EC2 Instance ID and the Timestamp, and format it into a clean, readable string (like *"Instance i-1234 terminated at 10:00 AM"*) before routing it to an SNS email topic.

### 11. What is EventBridge Archive and Replay?
**Answer:** You can configure EventBridge to Archive (save) all events that pass through a bus. If a downstream microservice crashes or a bug corrupts a database, you can use the "Replay" feature to push all historical events from the Archive back through the bus, effectively allowing the microservice to process the events again and heal the database.

### 12. How does EventBridge integrate with Third-Party SaaS providers?
**Answer:** Using Partner Event Sources. For example, if a customer opens a ticket in Zendesk, Zendesk can push an event directly into your AWS EventBridge bus securely, without you having to build complex API webhooks or manage authentication tokens.

### 13. What is the maximum size of an EventBridge event?
**Answer:** The maximum size for a single event payload is **256 KB**.

### 14. How do you secure Amazon EventBridge?
**Answer:** You use Resource-Based IAM Policies attached to the Event Bus itself. These policies dictate exactly which AWS accounts, IAM users, or AWS Organizations are allowed to `PutEvents` onto your bus, ensuring malicious actors cannot inject fake events into your architecture.

### 15. What is the difference between AWS CloudTrail and EventBridge?
**Answer:** 
* **CloudTrail** is for auditing. It records every API call made in the account and saves it to S3 (usually taking 15 minutes to deliver logs).
* **EventBridge** is for real-time automation. It triggers instantly when a state changes in AWS, allowing you to react immediately to operational issues.

### 16. How does EventBridge handle ordering?
**Answer:** EventBridge **does not** guarantee strict ordering. Because it is a highly distributed service, events may arrive at the target out of order. If strict ordering is an absolute architectural requirement, you must route the events through an **Amazon SQS FIFO Queue**.

### 17. What are EventBridge API Destinations?
**Answer:** API Destinations allow EventBridge to route events directly to external, third-party HTTP endpoints (like a Slack Webhook or an external legacy API) without needing to write a custom Lambda function to perform the HTTP POST request. EventBridge handles the authentication and rate-limiting natively.

### 18. What is the pricing model for Amazon EventBridge?
**Answer:** You pay per 1 million events published to the bus. However, all events published by AWS services (like EC2, S3, RDS state changes) to the Default event bus are completely **free**.

### 19. How can you test an EventBridge Rule without triggering actual infrastructure?
**Answer:** You can use the AWS Console to inject a "Test Event" (a mock JSON payload) against a Rule to verify that your Event Pattern matches correctly and that the Input Transformer parses the data as expected.

### 20. When would you choose EventBridge over Kinesis Data Streams?
**Answer:** You use **EventBridge** for discrete, operational events (e.g., "Order Placed", "Invoice Paid", "EC2 Terminated") where routing and decoupling are key. You use **Kinesis Data Streams** for continuous, massive telemetry data (e.g., 100,000 IoT sensor readings per second) where you need to perform real-time streaming analytics.
