# Prometheus & Grafana Day 3: PromQL (Prometheus Query Language)

Welcome to Day 3! Importing community Grafana dashboards (like we did on Day 2) is great for beginners. But what happens when your boss asks you to build a custom dashboard specifically for your company's proprietary microservice?

You cannot download that from the internet. You have to write the queries yourself. To do that, you must learn **PromQL**.

---

## 🧠 1. The Theory: What is PromQL?

### The "SQL for Metrics" Analogy
If you want to pull user data from a MySQL database, you write a SQL query:
`SELECT name FROM users WHERE age > 25;`

Prometheus is also a database (a Time Series Database). If you want to pull metric data from it, you write a PromQL query. 
Instead of selecting columns and rows, you are selecting **Metrics** and **Labels**.

**A basic PromQL Query looks like this:**
`http_requests_total{status="500", method="GET"}`

Let's break this down:
- `http_requests_total`: The **Metric Name**. (What are we measuring?)
- `{status="500", method="GET"}`: The **Labels**. (Filters! We only want to see GET requests that crashed with a 500 Error).

---

## ⏱️ 2. Instant Vectors vs. Range Vectors

This is the #1 most confusing topic for beginners, but it is actually incredibly simple.

### 1. Instant Vector (Right Now)
If you just type the metric name:
`http_requests_total`
Prometheus will return the exact number of requests that have happened **right at this exact millisecond**. It returns a single number.

### 2. Range Vector (Over Time)
If you add a time duration in brackets `[5m]` at the end of the metric:
`http_requests_total[5m]`
Prometheus will return a list of all the values recorded **over the last 5 minutes**. 

> [!IMPORTANT]
> You **cannot** draw a graph using an Instant Vector! A graph requires a history of data. You must use Range Vectors and mathematical functions to draw lines in Grafana.

---

## 🛠️ 3. Practical Lab: The 3 Queries You Must Memorize

If you are asked to build a dashboard or pass an interview, these are the 3 functions you will use 99% of the time.

### Query 1: The `rate()` Function (For CPU & Traffic)
Imagine your server has processed 10,000 requests total since it booted up. That number isn't very helpful. What you actually want to know is: *"How many requests are hitting my server PER SECOND right now?"*

The `rate()` function calculates the per-second average over a time range.
```promql
rate(http_requests_total{status="500"}[5m])
```
*Translation:* "Show me how many 500 Errors are happening **per second**, averaged over the last 5 minutes."

### Query 2: The `sum()` Function (Combining Pods)
If you have 10 identical Nginx Pods running, Prometheus will show you 10 different lines on your graph. If you just want to see the total traffic hitting your entire application, you wrap the query in `sum()`.
```promql
sum(rate(http_requests_total[5m]))
```
*Translation:* "Calculate the per-second traffic for every individual pod, and then add them all together into one single massive number."

### Query 3: Memory Usage (Math in PromQL)
Sometimes metrics are reported in raw Bytes. Humans can't read 10,737,418,240 Bytes easily on a graph. You can do math directly inside the query to convert it to Gigabytes!
```promql
node_memory_Active_bytes / 1024 / 1024 / 1024
```
*Translation:* "Take the active memory bytes and divide it by 1024 three times to convert it to GB."

---

## 🧠 4. Zero-to-Hero Bonus: Interview Gotchas

When an interviewer asks you about PromQL, they are testing if you actually know how the math works under the hood.

> [!CAUTION]
> **Gotcha 1: "What is the exact difference between `rate()` and `increase()` in PromQL?"**
> **Say this:** "Both operate on Range Vectors, but they return different things. `rate()` calculates the **per-second** average of the increase over the time range. `increase()` calculates the **total absolute increase** over the time range. For example, `increase(errors[5m])` might return 300 total errors, whereas `rate(errors[5m])` would return 1 error per second."

> [!TIP]
> **Gotcha 2: "If a Pod restarts, its internal counters reset to 0. Does this break the `rate()` function?"**
> **Say this:** "No! The `rate()` function is incredibly smart. It automatically detects counter resets (when a value drops from 10,000 back down to 0) and seamlessly adjusts the math so your graph doesn't show negative traffic spikes!"

> [!IMPORTANT]
> **Gotcha 3: "How do you calculate the 99th percentile (P99) response time of an API?"**
> **Say this:** "I would use a Histogram metric and the `histogram_quantile()` function. By writing `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))`, I can prove that 99% of our users are experiencing a response time faster than the output value."
