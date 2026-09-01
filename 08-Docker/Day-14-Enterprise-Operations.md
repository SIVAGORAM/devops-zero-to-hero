# Day 14: Enterprise Operations (CI/CD, Logging & Maintenance)

Welcome to the final frontier! When you manage Docker at an enterprise level, you are no longer manually typing commands on your laptop. You are automating deployments, managing gigabytes of logs, and keeping the servers clean.

---

## 🤖 1. CI/CD Integration (Automation)

In the real world, developers push code to GitHub, and a pipeline automatically builds the Docker image and pushes it to Docker Hub. This is called **Continuous Integration (CI)**.

Instead of running `docker build` manually, DevOps Engineers write pipeline scripts (using GitHub Actions, Jenkins, or GitLab CI) that execute the Docker commands automatically.

**Example GitHub Actions Workflow (`.github/workflows/docker.yml`):**
```yaml
name: Build and Push Docker Image
on:
  push:
    branches: [ "main" ] # Trigger when code is pushed to main
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Check out code
      uses: actions/checkout@v3
    
    - name: Log in to Docker Hub
      run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
      
    - name: Build and Push
      run: |
        docker build -t myusername/myapp:latest .
        docker push myusername/myapp:latest
```
With this file, every time a developer commits code, a robot logs into Docker Hub, builds the `Dockerfile`, and pushes the new image to the cloud!

---

## 📊 2. Advanced Logging Drivers

By default, Docker saves container logs in a standard JSON file on the host (`json-file` driver). 
**The Problem:** If you have 50 containers, checking logs manually via `docker logs` is impossible. Furthermore, if a container crashes and is deleted, its logs are deleted forever!

**The Solution:** Docker Logging Drivers. You can configure Docker to automatically forward all container logs to a centralized monitoring system like **AWS CloudWatch**, **Splunk**, or **Elasticsearch (ELK)**.

You do this by adding the `--log-driver` flag to your run command:
```bash
docker run -d \
  --name web \
  --log-driver=awslogs \
  --log-opt awslogs-region=us-east-1 \
  --log-opt awslogs-group=my-web-app \
  nginx
```
Now, even if the container is destroyed, every single access log and error is safely backed up in AWS CloudWatch!

---

## 🧹 3. Daemon Tuning & System Maintenance

If you leave a Docker server running for a year, it will eventually download hundreds of gigabytes of images, create dozens of unused networks, and leave dead containers lying around. **This will eventually consume 100% of your disk space and crash the server!**

### The Ultimate Cleanup Command
To prevent a production outage, you must schedule regular maintenance to prune (delete) unused objects.
```bash
docker system prune -a --volumes -f
```
*What it does:*
- `-a`: Deletes ALL images that are not actively being used by a running container.
- `--volumes`: Deletes all unused storage volumes.
- `-f`: Forces the deletion without asking for a [Y/N] confirmation.

DevOps engineers will set up a Linux **cron job** to run this exact command every Sunday at 3:00 AM to keep the server perfectly clean!

### Tuning the Daemon
At an enterprise level, you can configure the core Docker Engine itself by editing the `/etc/docker/daemon.json` file on the Linux host. 
Here you can tell Docker to permanently use specific DNS servers, set a default logging driver for all containers, or configure insecure private registries for corporate networks!

---

## 🎓 The End of the Journey

You have completely mastered the Docker ecosystem. From `docker run` to Orchestration, Security, and CI/CD Automation. 

You are now a true **DevOps Hero**. Go build something amazing!
