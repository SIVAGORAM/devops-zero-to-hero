# Day 04: Docker Port Mapping and Volumes

Welcome to Day 04! Today we tackle two essential pillars of Docker: **Port Mapping** (connecting your container to the outside world) and **Volumes** (saving your data permanently). Let's go from Zero to Hero!

## 1. Port Mapping (Networking)

### The Problem: Isolation
By default, **containers are 100% isolated**. They are closed boxes.
Imagine you install an NGINX web server directly on your Ubuntu EC2 host machine:
```bash
sudo su
apt install nginx -y
cd /var/www/html # Add some custom HTML here
```
If you go to your AWS Security Group and open Port 80, anyone on the internet can see your website by typing your EC2 IP address. 

However, if you run NGINX *inside a Docker Container*, that application is locked inside the container. Even if Port 80 is open on AWS, you cannot access the container's application because the EC2 instance doesn't know how to route the traffic into the sealed container.

### The Solution: Port Mapping
Port Mapping (`-p`) creates a bridge between your EC2 Host Machine and the Docker Container. 

**The Syntax:** `-p HOST_PORT:CONTAINER_PORT`

### Real-Time Practical 1: NGINX
Let's launch an NGINX container and map its internal port 80 to our EC2 host's port 80.
```bash
docker run -d --name c1 -p 80:80 nginx
```
Now, if you hit your EC2 IP address in the browser, you will see the NGINX default page!

### Real-Time Practical 2: Jenkins & Port Conflicts
Let's try hosting Jenkins, a popular CI/CD tool that runs on port 8080.
```bash
docker run -d --name jenkins jenkins/jenkins
```
If you try to access `http://<EC2_IP>:8080/`, it will fail because we forgot to map the port! Let's stop and remove it:
```bash
docker stop jenkins
docker rm jenkins
```

Now, let's do it correctly with port mapping:
```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
```
*(Make sure to open Port 8080 in your AWS Security Group!)*

**What if the Host Port is already in use?**
A single port on your host machine can only be used by one application at a time. If port 8080 is already occupied, you have two options:
1. **Kill the blocking process:** Run `lsof -i :8080` to find the Process ID (PID), then kill it: `kill -9 <PID>`.
2. **Use a different Host Port:** Just map a new, available host port to the container's 8080 port:
   ```bash
   docker run -d --name jenkins02 -p 9090:8080 jenkins/jenkins:lts
   ```
   Now, users can access Jenkins via `http://<EC2_IP>:9090`!

### Real-Time Practical 3: Node-RED
To prove you can host anything, let's run Node-RED:
```bash
docker run -p 1880:1880 nodered/node-red 
```
Open port 1880 in your AWS Security Group, and you have a live Node-RED server!

---

## 2. A Quick Note on Logs
Containers are **ephemeral** (temporary). If you delete the container, everything inside it is destroyed.
There are 2 types of logs generated inside containers:
1. **Application Logs:** (e.g., Python or Java errors).
2. **Server Logs:** (e.g., NGINX access logs).
Because containers wipe out data when they die, we use **Volumes** to save these logs and other data permanently!

---

## 3. Docker Volumes (Folder Mapping)

### The Problem: Ephemeral Containers
If you run a database container, save 1,000 records, and then remove the container (`docker rm`), your 1,000 records are permanently lost.

### The Solution: Volumes
Volumes allow us to map a folder *inside* the container to a folder *on the EC2 Host's hard drive*. This means the data is physically saved on the host, outside of the container's isolated filesystem.

### Real-Time Practical: Folder Mapping
Let's share a folder between our EC2 Host and a CentOS container using the `-v` (volume) flag.

**The Syntax:** `-v HOST_FOLDER_PATH:CONTAINER_FOLDER_PATH`

**Step 1: Start Container 1 (c1) with a mapped volume**
```bash
docker run --name c1 -it -v /tmp/host:/tmp/cont centos7 /bin/bash
```
**Step 2: Create a file INSIDE the container**
```bash
cd /tmp/cont
touch dummy
pwd
exit
```
*(By typing `exit`, you killed the container. The container is asleep, but the data is perfectly safe!)*

**Step 3: Check the EC2 Host machine**
```bash
cd /tmp/host
ls
```
You will see the `dummy` file sitting safely on your EC2 host machine! Let's create another file from the host:
```bash
touch 123
```

**Step 4: Start the container again and check**
```bash
docker start c1
docker attach c1
cd /tmp/cont
ls
```
You will see both `dummy` and `123`! 

**Step 5: Share the volume with a second container (c2)**
```bash
docker run --name c2 -it -v /tmp/host:/tmp/cont centos /bin/bash
cd /tmp/cont
ls
touch 12
exit
```
Now, `c1`, `c2`, and your EC2 host all share the exact same folder! This is incredibly useful for copying SSL certificates or sharing configuration files between different applications.

---

## 4. The 3 Types of Volumes

There are three ways to implement volumes in Docker. Let's understand the theory and practical execution of each:

### 1. Bind Mounts (Folder Mapping)
- **Theory:** You explicitly provide an exact path on the host machine. You control exactly where the files are stored on the EC2 instance.
- **When to use:** When you need to share specific, existing files from the host machine into the container (like configuration files or SSL certificates).
- **Practical Command:** 
  ```bash
  docker run -d --name c1 -v /tmp/host_folder:/tmp/container_folder centos
  ```
  *(This maps the specific `/tmp/host_folder` on your EC2 instance to the container).*

### 2. Anonymous Volumes
- **Theory:** You only provide the container path. You do NOT specify a host path. Docker automatically generates a random, complex hash string for the folder name and stores it deep inside `/var/lib/docker/volumes/` on the EC2 host.
- **When to use:** It is rarely used in production. If the container is deleted, it is extremely difficult to find where Docker saved that random folder to recover your data.
- **Practical Command:** 
  ```bash
  docker run -d --name db1 -v /var/lib/mysql mysql
  ```
  *(Notice there is no `:` splitting the host and container. You only specify the container's path).*

### 3. Named Volumes
- **Theory:** Instead of a complex host path, you simply provide a human-readable name. Docker creates a secure folder in its dedicated volume directory and manages it for you.
- **When to use:** This is the **Best Practice** for storing persistent data (like databases) because it is highly secure, easy to manage, and persists easily across multiple containers.
- **Practical Commands:** 
  First, you create the volume:
  ```bash
  docker volume create my_database_data
  ```
  Then, you attach it to a container:
  ```bash
  docker run -d --name db2 -v my_database_data:/var/lib/mysql mysql
  ```
  *(Docker securely manages the connection between `my_database_data` and the container).*
