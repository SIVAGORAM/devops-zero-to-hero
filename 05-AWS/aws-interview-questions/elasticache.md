# Amazon ElastiCache (Redis & Memcached) Interview Questions

Database performance at scale requires caching. These questions test your knowledge of in-memory datastores, caching strategies, and the differences between Redis and Memcached.

### 1. What is Amazon ElastiCache?
**Answer:** Amazon ElastiCache is a fully managed, in-memory caching service provided by AWS. It allows you to seamlessly set up, run, and scale popular open-source compatible in-memory data stores in the cloud to build data-intensive apps or boost the performance of existing databases.

### 2. What are the two engines supported by ElastiCache?
**Answer:** ElastiCache supports two open-source caching engines: **Redis** and **Memcached**.

### 3. What are the primary differences between Redis and Memcached?
**Answer:** 
* **Memcached:** Extremely simple, multi-threaded, purely in-memory key-value store. If the node reboots, data is lost permanently. Used strictly for simple caching.
* **Redis:** Single-threaded, supports complex data structures (Lists, Sets, Hashes), supports data persistence (saving to disk), supports High Availability (Multi-AZ replication), Pub/Sub messaging, and geospatial indexes.

### 4. When would you choose Memcached over Redis?
**Answer:** You should choose Memcached only if you need the absolute simplest model possible, require large multi-threaded performance on a single node, and do not care about data loss, replication, or high availability. (Note: For 95% of modern AWS architectures, Redis is the recommended choice).

### 5. What is the typical architecture pattern for using ElastiCache?
**Answer:** The **Lazy Loading** (or Cache-Aside) pattern. When an application needs data, it first checks ElastiCache (Cache Hit). If the data isn't there (Cache Miss), the application queries the primary RDS database, returns the data to the user, and simultaneously writes the data into ElastiCache so future queries are fast.

### 6. What is the "Write-Through" caching strategy?
**Answer:** In Write-Through, every time the application writes or updates data in the primary RDS database, it synchronously updates the data in ElastiCache as well. This ensures the cache is never stale, but it adds latency to write operations and caches data that might never be read.

### 7. How does ElastiCache for Redis achieve High Availability?
**Answer:** By using **Redis Replication Groups**. AWS provisions a Primary (Read/Write) node in one Availability Zone, and up to 5 Replica (Read-Only) nodes in different AZs. If the Primary node fails, ElastiCache automatically detects the failure and promotes one of the Replicas to become the new Primary (Multi-AZ Failover).

### 8. What is Redis Cluster Mode?
**Answer:** In standard Redis, all data must fit into the RAM of a single Primary node. If you have terabytes of cache data, you enable **Cluster Mode**. Cluster Mode shards (partitions) your data across multiple Primary nodes (up to 500 shards). This allows you to scale out memory and write capacity horizontally.

### 9. How do you scale ElastiCache for Redis?
**Answer:** 
* **Read Scaling:** Add more Read Replicas (up to 5 per shard).
* **Write/Memory Scaling:** Change the node type (Vertical Scaling) OR enable Cluster Mode and add more Shards (Horizontal Scaling).

### 10. How does ElastiCache secure data?
**Answer:** 
* **Network:** Nodes are placed in private VPC subnets; access is controlled via Security Groups.
* **In-Transit:** Supports TLS/SSL encryption for data moving over the network.
* **At-Rest:** Supports encryption using AWS KMS keys.
* **Authentication:** Redis supports `AUTH` tokens and native IAM Role-Based Authentication.

### 11. What is Redis Append Only File (AOF)?
**Answer:** AOF is a persistence mechanism in Redis. It logs every single write operation received by the server. If the node crashes and reboots, Redis replays the AOF log to completely reconstruct the dataset in memory, preventing data loss. (Note: AOF impacts performance and Multi-AZ replication is generally preferred for HA in AWS).

### 12. How do you handle cache evictions when memory is full?
**Answer:** You configure an Eviction Policy in the Parameter Group. The most common is **LRU (Least Recently Used)**, which deletes the keys that haven't been accessed in the longest time to make room for new data. Another option is **LFU (Least Frequently Used)**.

### 13. What is a Cache TTL (Time to Live)?
**Answer:** When writing a key to ElastiCache, you should set an expiration time (TTL). For example, `SET user_profile 123 EX 3600`. After 3600 seconds (1 hour), Redis automatically deletes the key. This ensures the cache doesn't grow infinitely and guarantees that stale data is eventually refreshed from the database.

### 14. Can ElastiCache for Redis be used as a primary database?
**Answer:** While Redis supports persistence and replication, it is an in-memory datastore, making RAM highly expensive per GB compared to SSD storage. While it *can* be used as a primary database for transient data (like gaming leaderboards or active user sessions), critical persistent data should reside in DynamoDB or RDS.

### 15. What is the Redis Pub/Sub feature?
**Answer:** Redis supports a Publisher/Subscriber messaging paradigm. Clients can subscribe to "Channels". When a publisher sends a message to a channel, Redis instantly pushes that message to all connected subscribers. It is extremely fast and often used for real-time chat rooms or live sports scoreboards.

### 16. How do you backup an ElastiCache Redis cluster?
**Answer:** ElastiCache allows you to take manual or automated daily snapshots of your Redis cluster. The snapshot captures the entire in-memory dataset, saves it as an `.rdb` file, and stores it durably in Amazon S3. You can use this snapshot to restore a new cluster later.

### 17. What is ElastiCache Serverless?
**Answer:** ElastiCache Serverless is a newer deployment option where you do not choose node types, manage shards, or configure replicas. AWS automatically scales memory, compute, and network bandwidth instantly based on application traffic. You pay only for the exact GBs of data stored and the number of requests processed.

### 18. How do you migrate data from an external Redis server into ElastiCache?
**Answer:** You can export an `.rdb` snapshot file from your self-hosted Redis server, upload it to an Amazon S3 bucket, and then create a new ElastiCache Redis cluster, instructing AWS to "Seed" the new cluster using the `.rdb` file from S3.

### 19. Can ElastiCache instances be accessed from the public internet?
**Answer:** No, by design. ElastiCache nodes do not have public IP addresses and are strictly designed to be accessed by EC2 instances or Lambda functions residing within the same Amazon VPC. To access them from outside, you must use a VPN or an EC2 bastion host.

### 20. What is Amazon MemoryDB for Redis?
**Answer:** While ElastiCache for Redis is primarily a *cache* (meaning data loss during failovers is possible), **Amazon MemoryDB** is a Redis-compatible, durable, primary database. It uses a highly durable distributed transaction log (similar to Aurora) to guarantee Multi-AZ data durability, making it safe to use as your single source of truth without needing an RDS backend.
