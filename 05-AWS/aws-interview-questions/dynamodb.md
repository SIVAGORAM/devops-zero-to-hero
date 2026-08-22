# Amazon DynamoDB Interview Questions

Amazon DynamoDB is the premier serverless NoSQL database in AWS. These questions test your understanding of highly scalable data modeling, partitioning, and read/write capacity management.

### 1. What is Amazon DynamoDB?
**Answer:** Amazon DynamoDB is a fully managed, serverless, proprietary NoSQL database service provided by AWS. It provides single-digit millisecond performance at any scale, making it ideal for mobile, web, gaming, and IoT applications requiring massive throughput and low latency.

### 2. How does Amazon DynamoDB work?
**Answer:** DynamoDB is a managed service, meaning there are no servers to provision or patch. You simply create a table, define a primary key, and start reading/writing data. Under the hood, AWS automatically replicates your data synchronously across three distinct Availability Zones for extremely high durability and availability.

### 3. What types of data models does Amazon DynamoDB support?
**Answer:** DynamoDB supports a key-value data model (where each item is a simple key and a JSON-like payload) and a wide-column document data model (where items can have nested attributes up to 32 levels deep). It is incredibly flexible compared to rigid relational SQL databases.

### 4. What are the key features of Amazon DynamoDB?
**Answer:** Key features include serverless operation (no instances to manage), Auto Scaling capacity, Global Tables for multi-region active-active replication, DynamoDB Streams for event-driven architectures, Point-in-Time Recovery (PITR) for backups, and native support for ACID transactions.

### 5. What is the Primary Key in Amazon DynamoDB?
**Answer:** The primary key uniquely identifies an item in a table. It can be a **Simple Primary Key** (composed of just a Partition Key, like `UserID`) or a **Composite Primary Key** (composed of a Partition Key and a Sort Key, like `UserID` and `OrderDate`).

### 6. How does Partitioning work in Amazon DynamoDB?
**Answer:** As your table grows in size or throughput, DynamoDB automatically divides your data into discrete chunks called **Partitions** (physical SSDs under the hood). It uses an internal hash function on your Partition Key to determine exactly which physical partition should store a specific item.

### 7. What is the difference between a Partition Key and a Sort Key in DynamoDB?
**Answer:** The **Partition Key** determines the physical physical location (partition) of the data. The **Sort Key** determines the physical sorting order of items that share the same partition key. Together, they allow you to run powerful queries (e.g., "Get all orders for UserID=123 where OrderDate is greater than 2023").

### 8. How can you query data in Amazon DynamoDB?
**Answer:** You have two options: 
1. **Query:** Highly efficient. It directly targets a specific Partition Key to find data instantly.
2. **Scan:** Highly inefficient. It reads every single item in the entire table to filter results. Scans consume massive amounts of read capacity and should be avoided in production.

### 9. What are Secondary Indexes in Amazon DynamoDB?
**Answer:** Secondary Indexes allow you to query data using attributes other than your primary key. 
* **Global Secondary Index (GSI):** Spans the entire table, can have a completely different partition and sort key, and can be created at any time.
* **Local Secondary Index (LSI):** Shares the same partition key as the base table but has a different sort key. It *must* be created when the table is created.

### 10. What is Eventual Consistency in DynamoDB?
**Answer:** When you write data, DynamoDB replicates it across 3 AZs. An **Eventually Consistent Read** (the default, which is cheaper) might return slightly stale data if it hits an AZ that hasn't received the replication yet (usually takes milliseconds). A **Strongly Consistent Read** guarantees you get the absolute latest data, but consumes twice the read capacity.

### 11. How can you ensure data durability in Amazon DynamoDB?
**Answer:** You don't have to do anything; DynamoDB inherently guarantees durability by automatically synchronously replicating all write operations across multiple Availability Zones before acknowledging the write as successful.

### 12. Can you change the schema of an existing Amazon DynamoDB table?
**Answer:** DynamoDB is "schema-less." Except for the primary key (which cannot be changed after table creation), you do not need to pre-define columns. Item A can have 2 attributes, while Item B in the same table can have 50 attributes. You can dynamically add new attributes on the fly.

### 13. What is the capacity mode in Amazon DynamoDB?
**Answer:** DynamoDB offers two billing/capacity modes:
* **Provisioned:** You specify exactly how many Read Capacity Units (RCUs) and Write Capacity Units (WCUs) you need. Cheaper for predictable, steady workloads.
* **On-Demand:** You pay per actual read/write request. Best for unpredictable, spiky, or brand-new workloads.

### 14. How can you automate the scaling of Amazon DynamoDB tables?
**Answer:** If using Provisioned capacity, you enable **Application Auto Scaling**. You set target utilization (e.g., 70%), and AWS will automatically increase your RCUs and WCUs during traffic spikes and scale them back down during quiet periods to save money.

### 15. What is DynamoDB Streams?
**Answer:** DynamoDB Streams is a time-ordered sequence of item-level changes (Inserts, Updates, Deletes) in a table. It is critical for event-driven architecture; you can configure an AWS Lambda function to trigger automatically whenever a record changes in the database (e.g., sending a welcome email when a new user is inserted).

### 16. How can you back up Amazon DynamoDB tables?
**Answer:** DynamoDB offers two methods:
* **On-Demand Backups:** Manual full backups stored in S3 for long-term archival.
* **Point-in-Time Recovery (PITR):** When enabled, it continuously backs up the table for 35 days, allowing you to rewind and restore the table to any exact second in the past (crucial for recovering from accidental developer deletions).

### 17. What is the purpose of the DynamoDB Accelerator (DAX)?
**Answer:** DAX is a fully managed, highly available, in-memory cache specifically built for DynamoDB. It reduces read response times from milliseconds to **microseconds** (millionths of a second) and drastically reduces Read Capacity Unit (RCU) costs for read-heavy applications.

### 18. How can you implement transactions in Amazon DynamoDB?
**Answer:** DynamoDB supports ACID transactions via the `TransactWriteItems` and `TransactGetItems` APIs. This allows developers to make synchronous, "all-or-nothing" updates across multiple items or even multiple tables (e.g., transferring money from Account A to Account B, failing completely if either update fails).

### 19. What is the difference between Amazon DynamoDB and Amazon S3?
**Answer:** DynamoDB is a NoSQL database optimized for microsecond retrieval of structured/semi-structured data (like user profiles or high-score leaderboards). Amazon S3 is an object storage service designed for storing massive, unstructured files (like gigabyte video files, images, or backups).

### 20. What are Global Tables in Amazon DynamoDB?
**Answer:** Global Tables provide a fully managed, multi-region, active-active database. You specify the regions (e.g., US-East and EU-West), and DynamoDB automatically replicates all data between them. This allows users in Europe to read/write to the European table with ultra-low latency, while data syncs globally in the background.
