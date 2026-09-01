# Day 02: Docker Architecture & Container Management

Welcome to Day 02 of Docker! Today we transition from theory to heavy practical implementation. We will uncover how Docker works under the hood, install it on an AWS EC2 instance, and master the core commands used to manage containers.

---

## 1. Deep Dive: What is a Container, Technically?

We established yesterday that a container is a "virtual box" containing your application and environment. But what is it technically?

**Technically, a container is just a process running on your host machine.**
Because it is just a running process, **you cannot create an empty container**. A process must have something to execute. Therefore, every container must be built from an **Image** (which contains the code/environment the process will run). Additionally, because it is just a process, the container directly consumes resources (CPU/RAM) from your host machine rather than artificially carving them out like a VM does.

*Recap of why we do this:*
- Solves the Dev vs. QA environment mismatch.
- Allows downloading/running multiple isolated copies of the exact same application on a single machine without port or library conflicts.

---

## 2. Docker Architecture (The 3 Core Components)

Docker operates on a Client-Server architecture. It consists of 3 main pieces:

1. **Docker Daemon (Docker Engine):** This is the heavy lifter. It is a background service (server) running on your host machine that does all the actual work of building, running, and destroying containers.
2. **Docker CLI (Client):** This is the terminal interface you type commands into. Using this, you get **observability** and the ability to communicate directly with your Docker Daemon. The CLI does not run containers; it simply sends your commands to the Docker Daemon to execute. 
3. **Docker Registry:** A centralized repository where all pre-built Images are stored. The public, default registry is **Docker Hub**. When you ask Docker to run an image, it downloads it from the registry.

### The 3 Pillars of Docker Learning
To master Docker (and eventually Kubernetes), you must master its three pillars:
1. **Container Management** (What we are doing today - running and stopping containers).
2. **Image Management** (Building custom images using Dockerfiles).
3. **Container Orchestration** (Managing thousands of containers using Kubernetes).

---

## 3. Hands-On: Installing Docker on AWS

Let's get our hands dirty and build our Docker playground!

### Step 1: Connect to your Server
Create an Ubuntu EC2 instance in AWS, grab the public IP, and SSH into it:
```bash
ssh -i "awslogin.pem" ubuntu@<YOUR_EC2_IP>
```

### Step 2: Switch to the Root User
Docker requires high-level system permissions. Always switch to the root user:
```bash
sudo su
```

### Step 3: Install Docker
*(Note: Always refer to the official [Docker Docs](https://docs.docker.com/engine/install/ubuntu/) for the latest installation scripts).*
For Ubuntu, run:
```bash
apt-get update
apt-get install docker.io -y
```

### Step 4: Verify the Installation
Run the following command to check if the Docker CLI (Client) can successfully communicate with the Docker Engine (Daemon):
```bash
docker info
```
*If you see a massive list of system details, your Docker Engine is running perfectly!*

---

## 4. Hands-On: Container Management

There are two primary ways to run a container: **Attached Mode** (you are inside the container's terminal) and **Detached Mode** (the container runs in the background). Today, we focus on Attached Mode.

### The Magic of `docker run`
When you type `docker run`, Docker automatically does 4 things in a split second:
1. Checks locally for the requested Image. If missing, it downloads it from Docker Hub.
2. Creates a brand new container and assigns it a unique ID.
3. Starts the container.
4. Attaches your terminal to the container.

### Let's run a CentOS Container!
```bash
docker run -it centos
```
*(Note: `-i` keeps it interactive, `-t` gives you a terminal).*
1. Docker will say *"Unable to find image 'centos:latest' locally"* and will download it.
2. Suddenly, your terminal prompt will change. **You are now inside the isolated container!**
3. Prove it by running Linux commands inside the container:
   ```bash
   ls
   cd /tmp
   touch my_test_file.txt
   ls
   ```
4. To leave the container and go back to your EC2 host, type:
   ```bash
   exit
   ```
*(Warning: Typing `exit` stops the container process. The container goes to sleep!)*

---

## 5. The Container Lifecycle Commands

Here are the most critical commands you will use daily to manage containers:

### 1. View Images
To see all the downloaded blueprints taking up space on your hard drive:
```bash
docker images
```

### 2. View Running Containers
To see only the containers that are currently awake and processing data:
```bash
docker ps
```

### 3. View ALL Containers (Running + Stopped)
Remember how you typed `exit` earlier? That container is sleeping. To see it, you must use the `-a` (all) flag:
```bash
docker ps -a
```
*Important Note: If you run `docker run -it centos` 10 times, Docker will create **10 entirely separate containers**. Use `docker ps -a` to see how many you've accidentally created!*

### 4. Customizing the Container Name
By default, Docker gives containers crazy, random names (like `laughing_turing`). You should always name your containers!
```bash
docker run -it --name devops centos:7
```
*(This downloads version 7 of CentOS and names the container 'devops').*

### 5. Waking up a sleeping container
If you exited a container, you can turn it back on without creating a new one:
```bash
docker start devops
# OR 
docker start <container_id>
```

### 6. Logging back into a running container
Once the container is started, attach your terminal back to it:
```bash
docker attach devops
```
