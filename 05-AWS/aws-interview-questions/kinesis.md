# Amazon Kinesis (Streaming Data) Interview Questions

Real-time data ingestion is a specialized skill. These questions test your knowledge of shards, streaming analytics, and dealing with big data at scale.

### 1. What is Amazon Kinesis?
**Answer:** Amazon Kinesis is a platform for collecting, processing, and analyzing real-time, streaming data. It allows you to ingest massive amounts of data (like website clickstreams, financial transactions, or IoT telemetry) and process it within seconds, rather than waiting for nightly batch jobs.

### 2. What are the four core services under the Amazon Kinesis umbrella?
**Answer:** 
1. **Kinesis Data Streams:** Captures and stores massive streams of custom data.
2. **Kinesis Data Firehose:** Automatically loads streaming data into data lakes/stores.
3. **Kinesis Data Analytics:** Analyzes streaming data in real-time using standard SQL.
4. **Kinesis Video Streams:** Captures and processes live video streams.

### 3. What is a Kinesis Data Stream?
**Answer:** A Data Stream is a highly durable, real-time buffer. Producers (like mobile apps) push data records into the stream continuously. Consumers (like EC2 instances or Lambda functions) read from the stream to process the records in real-time.

### 4. What is a Shard in Kinesis Data Streams?
**Answer:** A stream is composed of one or more Shards (the base throughput unit). 
* Each shard supports 1 MB/sec or 1,000 records/sec for **Writes** (Producers).
* Each shard supports 2 MB/sec for **Reads** (Consumers). 
To scale a stream, you add (split) more shards.

### 5. What is the Kinesis Partition Key?
**Answer:** When a producer sends data to Kinesis, it specifies a Partition Key (e.g., `user_id` or `device_id`). Kinesis hashes this key to determine exactly which Shard the data will be sent to. This guarantees that all data for a specific user is routed to the exact same shard, maintaining strict ordering.

### 6. What is the data retention period in Kinesis Data Streams?
**Answer:** By default, data records are stored durably for **24 hours**. You can extend this retention period up to a maximum of **365 days**, allowing consumers to replay historical data if needed.

### 7. How does Kinesis Data Firehose differ from Kinesis Data Streams?
**Answer:** 
* **Data Streams:** Requires you to write custom Consumer code (e.g., Lambda) to read the data, scale the shards, and handle errors.
* **Firehose:** Fully managed delivery. You do not manage shards or write consumer code. It simply takes the incoming streaming data, batches it (e.g., every 60 seconds), optionally converts it to Parquet, and dumps it directly into Amazon S3, Redshift, or OpenSearch.

### 8. What is the Kinesis Producer Library (KPL)?
**Answer:** The KPL is a highly optimized Java library used by producers. It performs automatic **Batching** (combining multiple records into one API call) and **Aggregation** (packing multiple user records into a single Kinesis record) to massively increase throughput and reduce costs.

### 9. What is the Kinesis Client Library (KCL)?
**Answer:** The KCL is a consumer application library that simplifies reading from a stream. It automatically handles load balancing across multiple consumers, manages shard splits/merges, and tracks the exact read progress (using a DynamoDB table for checkpointing) so it knows where to resume if a consumer crashes.

### 10. Can you query Kinesis Data Streams in real-time?
**Answer:** Yes, using **Kinesis Data Analytics**. It connects directly to your Data Stream and allows you to write standard SQL queries (e.g., calculating a moving average of stock prices over a 10-second sliding window) and instantly output the results to a dashboard or a database.
