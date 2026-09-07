# Prometheus & Grafana Day 2: Installation and Integration

Welcome to Day 2! Today we are moving from theory to practice. We are going to completely install the Prometheus and Grafana stack and integrate them so we can start visualizing data.

---

## 🏗️ 1. Ways to Install Prometheus & Grafana

There are 4 main ways to install this stack in the real world:
1. **Raw YAML Files:** Very hard to manage. *Not Recommended.*
2. **Helm Charts:** Uses 2-3 commands to deploy the entire stack to a K8s cluster. *(Highly Recommended in Production)*.
3. **Operators:** The advanced, automated version of Helm charts.
4. **Docker Containers:** Running them as lightweight containers on a Linux machine. **(We are doing this today!)**

---

## 🛠️ 2. Practical Lab: Docker Installation

For this lab, we are going to spin up an AWS EC2 instance and run both Prometheus and Grafana as Docker containers.

> [!WARNING]
> **Prerequisite:** Go to your AWS root account and launch an EC2 instance. 
> **Important:** You must use **t2.medium** or **t2.large**. A t2.micro does not have enough CPU/RAM for monitoring tools and will crash!

### Step 1: Install Docker on the EC2 Instance
Connect to your EC2 instance (via MobaXterm or SSH) and run:
```bash
sudo apt update -y

# Install Docker
sudo apt install docker.io -y

# Verify Installation
docker --version
```

### Step 2: Configure Prometheus
Prometheus needs a configuration file to tell it *what* to monitor. We are going to tell it to monitor itself as a test!
```bash
# Create a folder for the config
mkdir -p ~/prometheus && cd ~/prometheus

# Create the configuration file
cat <<EOF > prometheus.yml
global:
  scrape_interval: 15s     # How often should it pull data? Every 15 seconds!

scrape_configs:
  - job_name: 'prometheus' # The name of our test job
    static_configs:
      - targets: ['localhost:9090']  # Look at its own port!
EOF
```

### Step 3: Run the Prometheus Container
We will mount the configuration file we just created directly into the container using a Volume (`-v`).
```bash
sudo docker run -d --name=prometheus \
  -p 9090:9090 \
  -v ~/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

### Step 4: Run the Grafana Container
Grafana doesn't need a config file to start. We just pull the image and open port 3000!
```bash
sudo docker run -d --name=grafana \
  -p 3000:3000 \
  grafana/grafana
```

> [!TIP]
> **Verification:** Open your browser and go to:
> Prometheus: `http://<YOUR_EC2_PUBLIC_IP>:9090`
> Grafana: `http://<YOUR_EC2_PUBLIC_IP>:3000` 
> *(Make sure Ports 9090 and 3000 are open in your AWS Security Group!)*

---

## 🔗 3. Integrating Prometheus and Grafana

Right now, Grafana is completely empty. We need to tell Grafana to fetch data from our Prometheus database.

1. Open Grafana at `http://<YOUR_EC2_PUBLIC_IP>:3000`
2. **Login:** The default username and password are both `admin`.
3. In the left menu, go to **Connections > Data Sources**.
4. Click **"Add data source"** and select **Prometheus**.
5. In the URL field, enter your Prometheus server address: `http://<YOUR_EC2_PUBLIC_IP>:9090`
6. Scroll to the bottom and click **Save & Test**. You should see a green checkmark!

---

## 🎨 4. Importing Beautiful Dashboards

Building a dashboard from scratch takes hours. Luckily, Grafana has a massive community that builds dashboards for you! You just need the **Dashboard ID**.

1. Go back to the Grafana homepage, click **Dashboards**, and click **New > Import**.
2. Enter the Dashboard ID (e.g., `1860`) and click **Load**.
3. Select your **Prometheus** data source from the dropdown.
4. Click **Import**!

*Boom! You instantly have a beautiful, professional-grade monitoring dashboard.*

### Essential Grafana Dashboard IDs (Memorize These!)
- `1860`: Prometheus Stats
- `11074`: Node Exporter Full (For monitoring EC2/Linux CPU/RAM)
- `315` or `179`: Kubernetes Cluster Monitoring
- `893`: Docker Monitoring
- `10000`: AWS EC2 Monitoring
- `7362`: MySQL Monitoring
- `11310`: Nginx Monitoring
