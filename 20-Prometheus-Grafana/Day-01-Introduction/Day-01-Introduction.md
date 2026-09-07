# Prometheus & Grafana Day 1: Introduction to Continuous Monitoring (Observability)

Welcome to a brand new pillar of DevOps! You have successfully mastered Kubernetes. You know how to deploy microservices, expose them, and route traffic to them. 

But **what comes next?** 

Once your application is deployed, you cannot just sit in front of your computer and manually check if the master nodes, worker nodes, and pods are healthy all day long. If a server runs out of RAM, you need a robot to detect it and send you a message.

This practice is called **Continuous Monitoring (or Observability)**.

To achieve this, we use two of the most powerful, free, open-source tools in the industry: **Prometheus** and **Grafana**. 
*(In AWS, the equivalent tool is CloudWatch, but CloudWatch is expensive and paid! Prometheus and Grafana are open-source and free!)*

---

## 🛠️ 1. The Core Tools: Who Does What?

The biggest mistake beginners make is thinking Prometheus and Grafana do the exact same thing. They are actually a team.

### 🩺 Prometheus (The Doctor)
Prometheus is the **monitoring tool**. Its only job is to check the health of your machines. 
It is a **Time Series Database (TSDB)**. This means every 5 to 10 seconds, Prometheus connects to your machines, collects data (like CPU usage), and stores it internally with a timestamp.

### 📊 Grafana (The Dashboard)
Prometheus is just a database; looking at its raw data is ugly and hard to read. 
**Grafana is the visualization tool.** It connects to Prometheus, takes all that raw data, and turns it into beautiful charts, graphs, and dashboards that humans can easily understand.

**The Workflow:** 
1. Prometheus collects and stores the raw data.
2. Grafana reads the data and draws the charts.

---

## 🕵️ 2. How Prometheus Collects Data: Exporters (The Workers)

**Does Prometheus directly connect to a machine and magically know its CPU usage?** 
**NO!** 

Prometheus needs a "worker" installed on the target machine to collect the data for it. This worker is called an **Exporter**.

1. You install an Exporter on the target machine.
2. The Exporter constantly gathers data (CPU, RAM, Disk) and exposes it on a specific Port (e.g., Port `9100`).
3. Every 5-10 seconds, Prometheus connects to that Port, pulls the data, and stores it in its time-series database.

### The 4 Types of Exporters You Must Know
You must use a different exporter depending on *what* you want to monitor!
- **Node Exporter:** Used when you want to monitor the physical hardware (Linux Servers, EC2 instances, Worker Nodes).
- **Application Exporter:** Used when you want to monitor specific apps (e.g., Jenkins Exporter, RabbitMQ Exporter, Docker Exporter).
- **Container Exporter:** Used when you want to monitor individual Pods or Containers.
- **Kubernetes Exporter:** Used to monitor the overall health of the entire Kubernetes Cluster.

---

## 🚨 3. Alertmanager: "Wake Me Up When It Breaks!"

Prometheus collects data, and Grafana visualizes it. But what happens if you are asleep and the application crashes?

Inside the Prometheus ecosystem, there is a small, highly critical utility called **Alertmanager**. 
You write **Rules** for Alertmanager. For example:
- *"Rule 1: If CPU utilization of my target reaches 90% for more than 5 minutes..."*

If a rule is breached, Alertmanager immediately fires a notification to your Slack channel or Email so you can wake up and fix the issue before customers complain!

---

## 📚 4. Study Resources & Reference Links

As provided in your class, here are the absolute best resources to visualize this architecture:

1. **Video Playlist:** [Prometheus & Grafana YouTube Masterclass](https://youtube.com/playlist?list=PLZv1rlQ0kEKj55dXsTl3p61kPTjRjoKqT&si=3WWPVrS7aeDElyFj)
2. **Architecture Blog:** [Monitoring Distributed Systems with Grafana and Prometheus](https://medium.com/@aichali42471/monitoring-distributed-systems-with-grafana-and-prometheus-f8cd3ca674cc)

---

## 🧠 5. Zero-to-Hero Bonus: Interview Gotcha!

> [!CAUTION]
> **Tomorrow's Teaser & Interview Question:**
> *"How do you integrate Prometheus with Grafana?"*
> We will cover exactly how this connection is established practically in our next class! Make sure you understand that Prometheus and Grafana are two entirely separate applications that talk to each other over a network port!
