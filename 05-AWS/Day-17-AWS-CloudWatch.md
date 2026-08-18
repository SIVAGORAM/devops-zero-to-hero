# Day-17: AWS CloudWatch Deep Dive

## Introduction to AWS CloudWatch
Welcome back to our "30 Days AWS Zero to Hero" series. Today, on Day 17, we will deep dive into **AWS CloudWatch**.

**What is AWS CloudWatch?**
Think of AWS CloudWatch as the gatekeeper or watchman of your AWS account. It is a powerful monitoring and observability service provided by Amazon Web Services that acts as the central hub for monitoring, alerting, reporting, and logging. It enables you to gain insights into the performance, health, and operational aspects of your AWS resources and applications. CloudWatch collects and tracks metrics, collects and monitors log files, and sets alarms to alert you on certain conditions.

### Advantages of AWS CloudWatch
* **Comprehensive Monitoring:** Monitor various AWS resources such as EC2 instances, RDS databases, Lambda functions, and more. You get a unified view of your entire AWS infrastructure.
* **Real-Time Metrics:** It provides real-time monitoring of metrics, allowing you to respond quickly to any issues or anomalies that might arise.
* **Automated Actions:** With CloudWatch Alarms, you can set up automated actions like triggering an Auto Scaling group to scale in or out based on certain conditions.
* **Log Insights:** Analyze and search log data from various AWS services, making it easier to troubleshoot problems and identify trends.
* **Dashboards and Visualization:** Create custom dashboards to visualize your application and infrastructure metrics in one place, making it easier to understand the overall health of your system.

### Problem Solving with AWS CloudWatch
CloudWatch helps address several critical challenges, including:
* **Resource Utilization:** Tracking resource utilization and performance metrics to optimize your AWS infrastructure efficiently.
* **Proactive Monitoring:** Identifying and resolving issues before they impact your applications or users.
* **Troubleshooting:** Analyzing logs and metrics to troubleshoot problems and reduce downtime.
* **Scalability:** Automatically scaling resources based on demand to ensure optimal performance and cost efficiency.

### Practical Use Cases
* **Auto Scaling:** Trigger Auto Scaling actions based on defined thresholds (e.g., CPU utilization or request counts).
* **Resource Monitoring:** Monitor EC2 instances, RDS databases, DynamoDB tables, and other AWS resources to gain insights into their performance and health.
* **Application Insights:** Track application-specific metrics to monitor the performance of your applications and identify potential bottlenecks.
* **Log Analysis:** Use CloudWatch Logs Insights to analyze log data, identify patterns, and troubleshoot issues in real-time.
* **Billing and Cost Monitoring:** Monitor your AWS billing and usage patterns, enabling you to optimize costs.

### Metrics vs. Alarms
* **Metrics:** The raw data collected over time (e.g., "The CPU is at 45%").
* **Alarms:** The trigger mechanism that acts on the metric (e.g., "If the CPU metric stays above 50% for 1 minute, send an email!").

---

## Exploring CloudWatch Features
1. Log into your AWS Console and search for **CloudWatch**.
2. In the sidebar, you will see the top features:
   * **Log Groups:** This is where everything is logged. You can see all information (success, failures) recorded for your projects.
   * **Log Insights:** A powerful querying tool to search through your logs.
   * **Metrics:** Performance graphs generated from data collected 24/7.
   * **Alarms:** Configurations to trigger actions based on metrics.

---

## Hands-On Demo: Live EC2 CPU Alerting Through SNS

To truly understand CloudWatch, let's create a server, intentionally break it by spiking the CPU, and have CloudWatch send us a real-time email alert!

### 1. Create the Target EC2 Instance
1. Go to **EC2** -> **Launch instances**.
2. **Name:** `cloudwatch-demo`
3. **OS:** `Ubuntu`
4. **Instance Type:** `t3.micro`
5. **Key pair:** Select your key pair (`awslogin.pem`).
6. Click **Launch instance**.

### 2. Enable Detailed Monitoring
By default, EC2 sends metrics to CloudWatch every **5 minutes** (Standard Monitoring). We want faster results for our demo.
1. Select your new EC2 instance.
2. Under the **Monitoring** tab, you can view the default performance graphs.
3. Click on **Manage detailed monitoring**.
4. Check the box to **Enable detailed monitoring** and click **Confirm**. 
   *(Now, metrics will be recorded and sent to CloudWatch every 1 minute!)*

### 3. SSH into the Instance
Connect to your EC2 instance using a terminal or MobaXterm:
```bash
ssh -i awslogin.pem ubuntu@<your-ec2-ip-address>
```

Clear the screen and run `top` to view real-time CPU usage. You will notice the CPU is sitting near 0%.
```bash
clear
top
```

### 4. Configure the CloudWatch Alarm and SNS Topic
Now, we need to tell CloudWatch to watch this specific instance.

1. Go to **CloudWatch** -> **Alarms** -> **Create alarm**.
2. Click **Select metric**.
3. Since we want an EC2 metric, click **EC2**.
4. Choose **Per-Instance Metrics**.
5. Search for your instance ID, select the **CPUUtilization** metric for it, and click **Select metric**.
6. **Conditions:**
   * **Statistic:** `Average`
   * **Period:** `1 minute`
   * **Threshold type:** `Static`
   * **Whenever CPUUtilization is:** `Greater/Equal`
   * **than:** `50`
7. Click **Next**.

**Configure Actions (SNS - Simple Notification Service):**
1. **Alarm state trigger:** `In alarm`
2. Select **Create new topic**.
3. **Topic name:** `cloudwatch-alerts`
4. **Email endpoints:** Provide your actual email address.
5. Click **Create topic**.
6. Click **Next**.
7. **Alarm name:** `PRIORITY: EC2 Instance CPU Reached 50 Percent`
8. **Alarm description:** `Hey team, this is an automated notification from CloudWatch to let you know that your instance CPU has spiked to 50%. Please take action.`
9. Click **Next**, review, and click **Create alarm**.

> [!WARNING]
> **Important:** Your alarm is currently in a "Pending confirmation" state. Go to your email inbox (check your Spam folder just in case), open the email from AWS SNS, and click **Confirm subscription**. The alarm is now active!

### 5. Trigger the CPU Spike!
Let's intentionally stress our server to trigger the alarm. 
1. In your EC2 SSH session, ensure Python 3 is installed:
   ```bash
   python3 --version
   ```
2. Create the spike script:
   ```bash
   nano cpu_spike.py
   ```
3. Paste the contents of `day-17-demo-codes/default-metrics-demo/cpu_spike.py` from our repository into the file and save it.
4. Run the script:
   ```bash
   python3 cpu_spike.py
   ```

Wait 1-2 minutes. The script will pin the CPU to 80%. CloudWatch will detect this, the alarm state will change to **In alarm**, and AWS will immediately fire an email to your inbox containing the custom message we wrote!

*(Note: You can verify the SNS topic by searching for "SNS" in the AWS Console to see the underlying email configuration).*

---

## Going Further: Custom Metrics
EC2 instances automatically provide *Default Metrics* (like CPU, Disk, and Network). But what if you want to track business logic, like how many people viewed a product on your web app or how long your database takes to respond?

You can push **Custom Metrics** to CloudWatch using the AWS SDK (`boto3` in Python).

We have provided a demo in the repository: `day-17-demo-codes/custom-metrics-demo/cloudwatch_metrics.py`. 
This is a Flask web server that uses `boto3` to push two custom metrics to CloudWatch every time someone visits the page:
1. **PageViews:** A simple count metric.
2. **ResponseTime:** A timer metric tracking how long the page took to load.

By tracking these custom metrics, you can create alarms that notify you if your application gets too slow or experiences a massive traffic spike!
