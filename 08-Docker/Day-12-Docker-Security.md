# Day 12: Docker Security & Resource Limits (Zero to Hero)

## ⚠️ The Problem: The "Noisy Neighbor" and the "Root Hacker"

When you deploy Docker to a production server, you face two massive risks:

1. **The Noisy Neighbor:** By default, a Docker container has **unlimited access** to the host machine's CPU and Memory. If one of your containers has a memory leak or gets stuck in an infinite loop, it can consume 100% of the server's resources, causing every other container on the server to crash!
2. **The Root Hacker:** By default, processes inside a Docker container run as the **`root` user**. Because containers share the host's operating system kernel, if a hacker breaks into your container, they might be able to exploit the kernel and gain `root` access to your entire physical server!

## 🛡️ Part 1: Resource Limits (Caging the Noisy Neighbor)

To prevent a single container from taking down your entire EC2 instance, Docker uses Linux **cgroups** (Control Groups) to strictly limit CPU and Memory usage.

### Limiting Memory
You can set a hard limit on how much RAM a container can use. If the container tries to exceed this limit, Docker will automatically kill it (OOM - Out of Memory Kill) to protect the host server.

```bash
# Limits the container to a maximum of 512 Megabytes of RAM
docker run -d --name web --memory="512m" nginx
```

### Limiting CPU
You can restrict how much processing power a container is allowed to consume. 

```bash
# Limits the container to use a maximum of 1.5 CPUs (Cores)
docker run -d --name web --cpus="1.5" nginx
```

### The "Hero" Deployment Command
When deploying to production, a DevOps engineer always combines these limits:
```bash
docker run -d --name secure_web --memory="512m" --cpus="1.0" -p 80:80 nginx
```

---

## 🔒 Part 2: Docker Security (Locking out the Hackers)

Securing your containers is an absolute priority in DevOps. Here are the three golden rules of Docker security.

### Rule 1: NEVER Run as Root!
As mentioned, containers run as `root` by default. You must explicitly tell Docker to run your application as a standard, unprivileged user. You do this directly inside your `Dockerfile`.

**❌ The Bad Dockerfile (Runs as Root):**
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "app.js"]
```

**✅ The Hero Dockerfile (Runs as a standard user):**
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install

# Create a brand new, non-root user group and user
RUN groupadd -r myappuser && useradd -r -g myappuser myappuser

# Tell Docker to switch to this user BEFORE running the application!
USER myappuser

CMD ["node", "app.js"]
```
Now, even if a hacker exploits a vulnerability in `app.js`, they are trapped inside the container as `myappuser`. They do not have the permissions to install malware or break out of the container!

### Rule 2: Make the File System Read-Only
If a hacker gets into your container, the first thing they will try to do is download a script or modify your configuration files. You can stop this instantly by forcing the container's file system to be entirely **Read-Only**.

```bash
docker run -d --name web --read-only -p 80:80 nginx
```
With the `--read-only` flag, no one (not even the application itself) can write new files or modify existing ones inside the container! *(Note: If your application legitimately needs to write temporary files, you must mount a specific volume or tmpfs for it).*

### Rule 3: Scan Your Images for Vulnerabilities (CVEs)
Before you push your image to Docker Hub or deploy it to production, you must check it for known security vulnerabilities (like outdated libraries or exposed passwords).

You can use a free, industry-standard tool like **Trivy** or the built-in **Docker Scout** to scan your image.

```bash
# Using the built-in Docker scanner
docker scout cves my_custom_image:latest
```
This command will analyze every single layer of your image and print out a report of any Critical or High-level security threats so you can fix them before going live.

---

## 🏆 The Grand Finale

Congratulations! By mastering Resource Limits and Security Protocols, you have completed the final step in your journey. 

You now understand how to Architect, Build, Optimize, Orchestrate, and Secure containerized applications. You are officially a **Docker Hero!** 🦸‍♂️🦸‍♀️
