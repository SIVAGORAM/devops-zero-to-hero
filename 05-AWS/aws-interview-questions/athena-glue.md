# Amazon Athena & AWS Glue (Analytics & ETL) Interview Questions

Data Engineering and Analytics are increasingly overlapping with DevOps. These questions test your ability to query S3 directly and manage serverless data pipelines.

### 1. What is Amazon Athena?
**Answer:** Amazon Athena is an interactive, serverless query service that makes it easy to analyze data directly in Amazon S3 using standard SQL. You don't need to provision any databases or load the data into a warehouse; you just point Athena at your S3 bucket and run queries.

### 2. How is Amazon Athena priced?
**Answer:** Athena charges based on the amount of data scanned per query (e.g., $5 per Terabyte of data scanned). It does not charge for compute time. 

### 3. How can you reduce the cost and improve the performance of Athena queries?
**Answer:** You should compress your data, partition your data (e.g., organizing S3 folders by `year/month/day/`), and convert your data into columnar formats like **Parquet** or **ORC**. Because Athena charges per byte scanned, querying a columnar, compressed, and partitioned file will scan massively less data than querying raw CSVs.

### 4. What is AWS Glue?
**Answer:** AWS Glue is a fully managed, serverless ETL (Extract, Transform, and Load) service. It makes it simple and cost-effective to categorize your data, clean it, enrich it, and move it reliably between various data stores and data streams.

### 5. What is the AWS Glue Data Catalog?
**Answer:** The Glue Data Catalog is a persistent metadata store. It acts as a central repository to store structural and operational metadata for all your data assets. Services like Amazon Athena, Amazon EMR, and Amazon Redshift Spectrum use the Data Catalog to understand where the data in S3 is and what its schema (columns/types) looks like.

### 6. What is an AWS Glue Crawler?
**Answer:** A Crawler is a program that automatically connects to a data store (like an S3 bucket or an RDS database), progresses through a prioritized list of classifiers to determine the schema of your data, and then creates metadata tables in the AWS Glue Data Catalog.

### 7. How does Athena integrate with AWS Glue?
**Answer:** Athena natively uses the AWS Glue Data Catalog to store and retrieve table metadata. When you run a query in Athena, it uses the Glue Catalog to know exactly where the data lives in S3 and what the schema of that data is before executing the SQL.

### 8. What formats can Athena query natively?
**Answer:** Athena can query CSV, JSON, ORC, Apache Parquet, and Avro formats natively.

### 9. What is a typical use case for Athena in a DevOps environment?
**Answer:** Querying logs. AWS services like CloudTrail, Application Load Balancers, and VPC Flow Logs deliver massive amounts of raw JSON/CSV log data to S3. DevOps engineers use Athena to run instant SQL queries against those logs to investigate security incidents or debug application errors without needing to set up an Elasticsearch cluster.

### 10. Can Athena query databases other than S3?
**Answer:** Yes. Using **Amazon Athena Federated Query**, you can deploy data source connectors (which run as AWS Lambda functions) to run SQL queries across data stored in relational, non-relational, object, and custom data sources (like querying DynamoDB or external APIs directly from Athena).
