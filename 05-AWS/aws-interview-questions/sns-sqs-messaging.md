# AWS SQS & SNS (Messaging & Decoupling) Interview Questions

Decoupling microservices is a core tenet of modern cloud architecture. These questions test your knowledge of message queues, pub/sub models, and asynchronous processing.

### 1. Why is decoupling important in cloud architecture?
**Answer:** Decoupling ensures that if one component of an architecture fails (e.g., a database processing orders), the other components (e.g., the web servers receiving orders) can continue to function independently without bringing down the entire system. It prevents cascading failures.

### 2. What is Amazon SQS?
**Answer:** Amazon Simple Queue Service (SQS) is a fully managed message queuing service. It allows you to decouple distributed systems by acting as a temporary buffer. A "Producer" sends messages into the queue, and a "Consumer" retrieves and processes them asynchronously.

### 3. What is Amazon SNS?
**Answer:** Amazon Simple Notification Service (SNS) is a fully managed Pub/Sub (Publisher/Subscriber) messaging service. A Publisher sends a single message to an SNS "Topic", and SNS instantly fans out (pushes) that message to multiple Subscribers (like SQS queues, Lambda functions, or email/SMS).

### 4. What is the fundamental difference between SQS and SNS?
**Answer:** 
* **SQS is a Pull (Polling) model:** The consumer application must actively ask the queue "Do you have any messages for me?"
* **SNS is a Push model:** The topic immediately pushes the message out to all registered subscribers the moment it arrives.

### 5. What are the two types of SQS Queues?
**Answer:** 
1. **Standard Queue:** Unlimited throughput, but guarantees "at-least-once" delivery (meaning duplicates can occur) and "best-effort" ordering (messages might arrive out of order).
2. **FIFO Queue (First-In-First-Out):** Guarantees strict ordering and "exactly-once" processing, but is limited to 3,000 messages per second (with batching).

### 6. What is the SQS Visibility Timeout?
**Answer:** When a consumer polls a message from SQS, the message remains in the queue but becomes "invisible" to other consumers for a set period (default 30 seconds). If the consumer successfully processes the message, it must explicitly delete it. If the consumer crashes and fails to delete it before the timeout expires, the message becomes visible again for another consumer to process.

### 7. What is SQS Short Polling vs. Long Polling?
**Answer:** 
* **Short Polling:** Returns immediately, even if the queue is empty. Costs more money because it generates millions of empty API requests.
* **Long Polling (WaitTimeSeconds > 0):** The consumer waits (up to 20 seconds) for a message to arrive before returning an empty response. This massively reduces API calls and saves money.

### 8. What is a Dead Letter Queue (DLQ)?
**Answer:** If a message is malformed (e.g., bad JSON) and crashes the consumer application every time it tries to process it, the message will go back into the queue endlessly. To prevent this infinite loop, you configure a `maxReceiveCount`. After failing X times, SQS automatically moves the "poison pill" message to a DLQ so developers can inspect it manually.

### 9. What is the maximum message size in SQS and SNS?
**Answer:** The maximum payload size for a single message in both SQS and SNS is **256 KB**. If you need to send larger messages (e.g., a 10MB PDF), you use the **SQS Extended Client Library**, which uploads the PDF to S3 and sends an SQS message containing only the S3 URL pointer.

### 10. How long can a message remain in an SQS queue?
**Answer:** By default, messages are retained for 4 days. However, you can configure the Message Retention Period to be anywhere from 1 minute up to a maximum of **14 days**.

### 11. What is the "Fan-Out" architecture pattern?
**Answer:** It is a pattern combining SNS and SQS. You publish a single message to an SNS Topic. That Topic has three different SQS queues subscribed to it. SNS instantly replicates (fans out) the message to all three queues, allowing three independent microservices to process the exact same event asynchronously.

### 12. How does SNS Message Filtering work?
**Answer:** By default, an SNS topic sends every message to every subscriber. With Message Filtering, you apply a JSON filter policy to a subscription. For example, a queue processing returns only receives messages where the attribute `"order_type" = "return"`, completely ignoring standard purchase events.

### 13. How can you encrypt messages in SQS and SNS?
**Answer:** You enable Server-Side Encryption (SSE) using AWS KMS. When a producer sends a message, KMS encrypts it at rest. When a consumer with the proper IAM and KMS decrypt permissions retrieves it, it is decrypted seamlessly.

### 14. What is a Delay Queue in SQS?
**Answer:** A Delay Queue lets you postpone the delivery of new messages. If you set a delay of 60 seconds, any message sent to the queue remains completely invisible to consumers for the first 60 seconds.

### 15. How do you handle strict ordering in an SQS FIFO queue with multiple customers?
**Answer:** You use a **Message Group ID**. If you have 1,000 customers sending messages, you don't want Customer A's massive backlog to delay Customer B's messages. By setting the Message Group ID to the `customer_id`, SQS ensures strict ordering *within* that specific customer's group, but processes different customer groups in parallel.

### 16. What is SQS Message Deduplication?
**Answer:** In a FIFO queue, if a producer accidentally sends the exact same message twice due to a network retry, SQS uses the `MessageDeduplicationId` (or a SHA-256 hash of the body) to recognize the duplicate. It will automatically discard the duplicate if it arrives within a 5-minute deduplication window.

### 17. Can an SNS Topic trigger an AWS Lambda function directly?
**Answer:** Yes. SNS can invoke a Lambda function asynchronously. The Lambda function receives the SNS message payload as the input event and executes the code immediately.

### 18. What happens if an SNS Subscriber is offline?
**Answer:** SNS has built-in delivery retries. If an HTTP endpoint subscriber is temporarily offline, SNS will back off and retry delivering the message for up to 23 days. However, for guaranteed delivery, it is best practice to have SNS push to an SQS queue instead.

### 19. How do you monitor the backlog of an SQS queue?
**Answer:** You monitor the **`ApproximateNumberOfMessagesVisible`** metric in Amazon CloudWatch. This metric is frequently used to trigger EC2 Auto Scaling Groups—if the queue suddenly has 10,000 messages, the ASG scales out to launch more EC2 consumer instances to process the backlog.

### 20. Can an SQS Queue trigger a Lambda function?
**Answer:** Yes, via an **Event Source Mapping**. The Lambda service constantly polls the SQS queue on your behalf. When messages arrive, it batches them (e.g., 10 messages at a time) and synchronously invokes your Lambda function to process the batch.
