# AWS Step Functions Interview Questions

As serverless architectures grow, orchestrating dozens of Lambda functions becomes impossible without a state machine. These questions test your knowledge of workflow orchestration and error handling.

### 1. What is AWS Step Functions?
**Answer:** AWS Step Functions is a fully managed serverless orchestration service. It allows you to design and execute visual workflows (state machines) that coordinate multiple AWS services (like Lambda, ECS, and SNS) into complex, step-by-step business processes.

### 2. Why use Step Functions instead of chaining Lambda functions together?
**Answer:** Chaining Lambda functions (Lambda A calls Lambda B, which calls Lambda C) is an anti-pattern. It creates tight coupling, makes debugging a nightmare, and costs more money (since Lambda A is billed while it waits for Lambda B to finish). Step Functions extract the orchestration logic out of the code, managing the state, retries, and branching visually.

### 3. What language is used to define Step Functions?
**Answer:** Step Functions are defined using **Amazon States Language (ASL)**, which is a JSON-based structured language used to define the states, the transitions between them, and the error handling logic.

### 4. What are the common types of States in Step Functions?
**Answer:** 
* **Task:** Does work (e.g., invokes a Lambda function).
* **Choice:** Adds branching logic (e.g., If Total > $100, go to Path A).
* **Wait:** Pauses the execution for a specific time.
* **Parallel:** Executes multiple branches of states simultaneously.
* **Map:** Executes a set of steps for every item in an array (like a For-Each loop).
* **Fail/Succeed:** Stops the execution with a failure or success status.

### 5. What is the difference between Standard and Express workflows?
**Answer:** 
* **Standard:** Best for long-running workflows (can run up to 1 year). Provides full visual execution history in the console. Billed per state transition.
* **Express:** Best for high-volume, fast-running workflows (must finish in 5 minutes). Does not provide visual history (logs to CloudWatch). Billed by memory and duration. Ideal for IoT data ingestion or streaming data processing.

### 6. How do Step Functions handle errors and retries?
**Answer:** Step Functions natively handle errors without writing code. You can define a `Retry` block in ASL. If a Lambda function throws a "TimeoutException", Step Functions can be configured to retry 3 times with exponential backoff. If it still fails, a `Catch` block can gracefully route the workflow to a fallback state (like sending an alert to SNS).

### 7. What is the `.waitForTaskToken` pattern?
**Answer:** This is used for human approval or external integrations. When a Task state is configured with `.waitForTaskToken`, Step Functions pauses the workflow and passes a unique token to an external service (like an email with an "Approve" button). The workflow remains paused (costing nothing) until the external service returns the token to the Step Functions API, allowing it to resume.

### 8. What is the maximum duration a Standard Step Function can run?
**Answer:** A single execution of a Standard Step Function can run for up to **1 year**, making it perfect for long-running business processes like loan approvals or manual compliance reviews.

### 9. How do you pass data between states?
**Answer:** Data is passed between states as JSON. The output of State A becomes the input of State B. You can use ASL filters (`InputPath`, `ResultPath`, `OutputPath`) to manipulate the JSON, extracting only the necessary fields before passing it to the next Lambda function to avoid exceeding payload limits.

### 10. What is a Map State?
**Answer:** A Map state is a "For-Each" loop. If your input is an array of 50 images, the Map state will spin up 50 parallel iterations of a specific workflow (e.g., invoking an Image Processing Lambda) to process all 50 images simultaneously.

### 11. What is the Distributed Map State?
**Answer:** While a standard Map state is limited to 40 concurrent iterations, a **Distributed Map** is designed to process massive datasets in S3. It can coordinate up to 10,000 parallel concurrent executions, allowing you to process millions of S3 objects or massive CSV files at unprecedented speeds.

### 12. How does Step Functions integrate with AWS services?
**Answer:** Step Functions has **Optimized Integrations** for over 200 AWS services. This means a Step Function Task can directly start an ECS Fargate container, run an Athena SQL query, or put an item into DynamoDB via direct API calls *without* needing to write a Lambda function to act as a middleman.

### 13. What is the maximum payload size that can be passed between states?
**Answer:** The maximum JSON payload size passed between states is **256 KB**. If you need to process larger payloads (like an image or a video file), you must upload the file to S3 and pass only the S3 URI string through the state machine.

### 14. How do you test Step Functions locally?
**Answer:** AWS provides **Step Functions Local**, a downloadable version of the service that runs in a Docker container on your laptop. It allows developers to test their ASL definitions and mock external AWS service responses before deploying to the cloud.

### 15. Can you trigger a Step Function from API Gateway?
**Answer:** Yes. You can create an API Gateway endpoint that uses an AWS Service Integration to directly trigger the `StartExecution` or `StartSyncExecution` API of Step Functions.

### 16. What is a Synchronous Express Workflow?
**Answer:** Normally, starting a Step Function returns an execution ID immediately (asynchronous). A Synchronous Express workflow keeps the HTTP connection open, runs the entire state machine, and returns the final output of the workflow directly back to API Gateway. This allows you to build complex backend APIs without writing a monolithic Lambda function.

### 17. How do you monitor Step Functions?
**Answer:** Step Functions automatically sends metrics to CloudWatch (Execution Time, Failures). For Standard workflows, the AWS Console provides an incredible visual graph showing exactly which path the execution took, highlighting failed states in red, and allowing you to click on any state to see the exact JSON input/output.

### 18. What is the Saga Pattern in Step Functions?
**Answer:** In microservices, distributed transactions are difficult. If a customer books a vacation, you must book a Flight, Hotel, and Car. If the Car booking fails, you must cancel the Flight and Hotel. Step Functions implements the Saga Pattern using `Catch` blocks to trigger "Compensating Transactions" (rollback workflows) to undo the previous successful steps.

### 19. How do you handle complex business logic that ASL can't do natively?
**Answer:** While ASL can do basic variable manipulation, if you need complex math, string manipulation, or data parsing, you use a **Task state** to invoke a lightweight Lambda function to execute that specific business logic, returning the clean data to the state machine.

### 20. What is the `Pass` state used for?
**Answer:** The `Pass` state simply passes its input to its output without doing any work. It is highly useful during development to mock out future steps, or to inject static JSON data/variables into the workflow using the `Result` field.
