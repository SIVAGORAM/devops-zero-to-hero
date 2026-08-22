# Amazon RDS Interview Questions

Amazon Relational Database Service (RDS) is the backbone of AWS data storage. These questions test your knowledge of relational database scaling, high availability (Multi-AZ), and disaster recovery.

### 1. What is Amazon RDS?
**Answer:** Amazon RDS (Relational Database Service) is a managed PaaS (Platform as a Service) offering that simplifies the setup, operation, and scaling of relational databases in the cloud. It supports major database engines including MySQL, PostgreSQL, MariaDB, Oracle, Microsoft SQL Server, and Amazon Aurora.

### 2. How does Amazon RDS work?
**Answer:** AWS provisions an EC2 instance and an EBS volume, installs the database engine of your choice, and manages the underlying OS. Unlike running a database on a standard EC2 instance, RDS abstracts away the administrative burden; AWS automatically handles OS patching, database software updates, and daily backups.

### 3. What are the key features of Amazon RDS?
**Answer:** The primary features are Automated Backups (Point-in-Time Recovery), Multi-AZ deployments for synchronous high availability, Read Replicas for asynchronous read scaling, Automated Patching during maintenance windows, and native integration with AWS KMS for encryption at rest.

### 4. What is a Multi-AZ deployment in Amazon RDS?
**Answer:** Multi-AZ provides High Availability (Disaster Recovery), *not* scaling. AWS provisions a primary database in one Availability Zone and synchronously replicates all data to a hidden standby database in a different AZ. If the primary instance crashes, AWS automatically fails over to the standby instance by updating the DNS endpoint, usually within 60 seconds, with zero data loss.

### 5. How can you improve read performance in Amazon RDS?
**Answer:** You create **Read Replicas**. A Read Replica is an asynchronous, read-only copy of your primary database. You can route all of your heavy, read-heavy traffic (like reporting queries or analytics) to the replica, which significantly reduces the CPU and memory load on your primary writer database.

### 6. What is Amazon Aurora?
**Answer:** Amazon Aurora is AWS's flagship, enterprise-grade relational database engine that is fully compatible with MySQL and PostgreSQL. It separates the compute layer from the storage layer. The storage layer is a highly distributed, self-healing system that automatically replicates data 6 times across 3 Availability Zones, providing up to 5x the throughput of standard MySQL.

### 7. What is the purpose of an RDS Option Group?
**Answer:** Because you do not have root SSH access to the underlying RDS server, you cannot install external database plugins manually. An Option Group is a configuration construct that allows you to enable specific features on your database, such as enabling Transparent Data Encryption (TDE) for SQL Server, or adding the Memcached plugin to MySQL.

### 8. How can you encrypt data in Amazon RDS?
**Answer:** 
* **At Rest:** You enable encryption at creation time. AWS uses the Key Management Service (KMS) to encrypt the underlying EBS volumes, automated backups, Read Replicas, and snapshots.
* **In Transit:** You use SSL/TLS. AWS provides a root certificate that your application uses to securely encrypt the SQL connection string to the RDS endpoint.

### 9. What is a DB Parameter Group in Amazon RDS?
**Answer:** A Parameter Group acts as a "container" for database engine configuration values. Instead of SSH-ing into the server to edit the `my.cnf` or `postgresql.conf` files, you modify settings (like `max_connections` or `innodb_buffer_pool_size`) in the Parameter Group and apply it to your database instance.

### 10. How can you monitor Amazon RDS instances?
**Answer:** You monitor basic metrics (CPU, Freeable Memory, Read/Write IOPS) using **Amazon CloudWatch**. For deep database performance tuning, you enable **Enhanced Monitoring** (which provides OS-level metrics in real-time) and **Performance Insights** (which provides a visual dashboard to easily identify which specific SQL queries are causing database bottlenecks).

### 11. What is the difference between Amazon RDS and Amazon DynamoDB?
**Answer:** Amazon RDS is a **Relational (SQL)** database designed for complex queries, joins, and strict ACID transactions (e.g., financial systems). Amazon DynamoDB is a **Non-Relational (NoSQL)** database designed for massive horizontal scaling, single-digit millisecond latency, and flexible, schema-less data structures (e.g., user profiles, high scores).

### 12. How can you take backups of Amazon RDS databases?
**Answer:** 
* **Automated Backups:** AWS automatically takes daily snapshots and continuously backs up transaction logs, allowing you to perform Point-in-Time Recovery (PITR) to any exact second in the last 35 days.
* **Manual Snapshots:** User-initiated full backups that are kept permanently until you explicitly delete them (often used before major application upgrades).

### 13. Can you change the DB instance type for an existing Amazon RDS instance?
**Answer:** Yes. You can vertically scale your database (e.g., upgrading from a `db.t3.medium` to a `db.m5.xlarge`). However, this action requires a brief period of downtime as AWS shuts down the database, moves the EBS volume to a larger physical server, and reboots it. 

### 14. What is the purpose of an RDS Read Replica?
**Answer:** Read Replicas are strictly used for **Scaling** (handling more traffic), not high availability. If your web application has a 90% read / 10% write ratio, you can create up to 15 Read Replicas and distribute the read traffic across them. A Read Replica can also be explicitly promoted to become a standalone database if needed.

### 15. How can you replicate data between Amazon RDS and on-premises databases?
**Answer:** You use the **AWS Database Migration Service (DMS)**. DMS can replicate data continuously between heterogeneous databases (e.g., Oracle to PostgreSQL) or homogeneous databases (e.g., On-prem MySQL to RDS MySQL) with near-zero downtime.

### 16. What is the maximum storage capacity for an Amazon RDS instance?
**Answer:** For standard RDS engines (MySQL, PostgreSQL, MariaDB, Oracle), the maximum storage limit is **64 TB**. For Amazon Aurora, the storage volume automatically grows in 10 GB increments as your data grows, up to a maximum of **128 TB**.

### 17. How can you restore an Amazon RDS instance from a snapshot?
**Answer:** You select the manual snapshot or the automated Point-in-Time Recovery timestamp. AWS will provision a **brand new RDS instance** with a new DNS endpoint using the data from the snapshot. You cannot restore a snapshot directly over an existing, running database.

### 18. What is the significance of the RDS DB Subnet Group?
**Answer:** A DB Subnet Group tells RDS exactly which VPC and which subnets the database is allowed to use. For High Availability (Multi-AZ), the Subnet Group *must* contain at least two subnets located in two different Availability Zones. Best practice dictates these should always be **Private Subnets**.

### 19. How does Amazon RDS handle automatic backups?
**Answer:** During the daily maintenance window you specify, RDS creates a storage volume snapshot. Throughout the day, it continuously uploads database transaction logs to S3 every 5 minutes. The combination of the daily snapshot and the transaction logs allows for granular Point-in-Time Recovery.

### 20. Can you run custom bash scripts or install custom software on Amazon RDS instances?
**Answer:** No. Amazon RDS is a managed service, meaning you do not get root or SSH access to the underlying OS. If your architecture absolutely requires custom agents, highly specialized database plugins, or OS-level configurations, you cannot use RDS; you must install the database manually on a standard **Amazon EC2 instance**.
