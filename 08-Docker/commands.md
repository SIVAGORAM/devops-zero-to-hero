# The Ultimate Docker Commands Cheat Sheet (Zero to Hero)

This document serves as the master reference guide for DevOps Engineers. It contains every critical Docker command you need to manage the entire lifecycle of images, containers, and networks, explained deeply from Zero to Hero.

---

## 🚀 1. Container Management Lifecycle

These are the day-to-day commands you will use to create, monitor, interact with, and destroy containers.

### `docker run`
**Purpose:** Spins up a brand new Docker container from an image. This is actually a combination of `docker create` and `docker start`.
**Crucial Flags:**
- `-d` (Detached Mode): Runs the container in the background and prints the container ID. If you don't use this, your terminal will be hijacked by the container's output.
- `-p <host_port>:<container_port>` (Port Mapping): Bridges a port on your EC2 host to a port inside the container (e.g., `-p 80:80`).
- `-v <host_dir>:<container_dir>` (Volumes): Mounts a folder from your host into the container for persistent storage.
- `--name <name>`: Assigns a custom name to your container (e.g., `--name my_web_server`).
- `-it`: Runs the container in interactive terminal mode (useful for logging directly into a base OS like Ubuntu).
**Example:** `docker run -d --name web -p 80:80 -v /home/ubuntu/html:/usr/share/nginx/html nginx`

### `docker ps`
**Purpose:** Lists the actively running containers on the host machine.
**Crucial Flags:**
- `-a` (All): Lists ALL containers, including the ones that are stopped, crashed, or exited.
- `-q` (Quiet): Only prints the Container IDs (highly useful for scripting/automation).
**Example:** `docker ps -a`

### `docker exec`
**Purpose:** Executes a new command inside an *already running* container. Mostly used to "log in" to a container for troubleshooting.
**Example:** `docker exec -it my_web_server /bin/bash`

### `docker stop`
**Purpose:** Gracefully stops a running container by sending a `SIGTERM` signal, allowing it to shut down its processes safely.
**Example:** `docker stop my_web_server`

### `docker start`
**Purpose:** Wakes up and starts a container that was previously stopped.
**Example:** `docker start my_web_server`

### `docker rm`
**Purpose:** Permanently deletes a stopped container. By default, you cannot delete a running container.
**Crucial Flags:**
- `-f` (Force): Forces the deletion of a container even if it is currently running (sends a `SIGKILL`).
**Example:** `docker rm -f my_web_server`
**Pro-Tip (Mass Cleanup):** `docker rm -f $(docker ps -aq)` deletes EVERY container on your machine!

---

## 📦 2. Image Management

Commands used to create, download, share, and delete Docker Images.

### `docker images`
**Purpose:** Lists all Docker images currently downloaded and stored on your local host machine.
**Example:** `docker images`

### `docker pull`
**Purpose:** Downloads an image from the configured registry (Docker Hub) to your local machine without running it.
**Example:** `docker pull ubuntu:20.04`

### `docker build`
**Purpose:** Reads a `Dockerfile` and builds a custom Docker image layer by layer.
**Crucial Flags:**
- `-t <name>:<tag>` (Tag): Assigns a name and version tag to the image.
- `.` (Context): Tells Docker to look for the Dockerfile in the current directory.
**Example:** `docker build -t my-node-app:v1.0 .`

### `docker push`
**Purpose:** Uploads your custom, tagged image to the configured registry (Docker Hub) so it can be shared with the world or deployed to Kubernetes.
**Example:** `docker push abhishekf5/my-first-docker-image:latest`

### `docker rmi`
**Purpose:** Removes an Image from the host machine to free up disk space. (Note: You cannot delete an image if a container is currently using it).
**Crucial Flags:**
- `-f` (Force): Forces the deletion of the image.
**Example:** `docker rmi ubuntu:latest`

---

## 🌐 3. Networking & Advanced Commands

### `docker network`
**Purpose:** Manages Docker networks, allowing you to isolate containers or bridge them together for secure communication.
**Sub-commands:**
- `docker network ls`: Lists all networks (bridge, host, none).
- `docker network create <name>`: Creates a custom bridge network so containers can communicate using DNS (names).
- `docker network connect <network> <container>`: Dynamically plugs a running container into a network.
- `docker network disconnect <network> <container>`: Dynamically severs a container's connection to a network.
- `docker inspect <network>`: Shows detailed JSON data about a network, including the private IPs of all attached containers.

### `docker commit` (Legacy/Manual builds)
**Purpose:** Creates a new image from a running container's changes. (Usually replaced by Dockerfiles in the real world).
**Example:** `docker commit c1 my_custom_image`

### `docker login`
**Purpose:** Authenticates your local Docker client with a remote registry (Docker Hub) so you have permission to `push` private images.
**Example:** `docker login -u <username>`
