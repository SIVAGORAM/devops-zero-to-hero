# The Ultimate Docker Commands Cheat Sheet (Zero to Hero)

This document is compiled from all 9 days of our Docker Zero to Hero curriculum. It contains every critical Docker command you need to manage the entire lifecycle of images, containers, networks, and volumes!

---

## 🚀 1. Container Lifecycle Management (Days 02 & 03)

These are the day-to-day commands you will use to create, monitor, interact with, and destroy containers.

### `docker run`
**Purpose:** Spins up a brand new Docker container from an image.
**Crucial Flags:**
- `-d` (Detached Mode): Runs the container in the background and prints the container ID.
- `-p <host_port>:<container_port>` (Port Mapping): Bridges a port on your host to the container (Day 04).
- `-v <host_dir>:<container_dir>` (Volumes): Mounts a host folder or Named Volume into the container (Day 04).
- `--name <name>`: Assigns a custom name to your container (e.g., `--name my_web_server`).
- `-it`: Runs the container in interactive terminal mode.
**Example:** `docker run -d --name web -p 80:80 -v /home/ubuntu/html:/usr/share/nginx/html nginx`

### `docker ps`
**Purpose:** Lists the actively running containers on the host machine.
**Crucial Flags:**
- `-a` (All): Lists ALL containers, including the stopped/crashed ones.
- `-q` (Quiet): Only prints the Container IDs (useful for scripting).
**Example:** `docker ps -a`

### `docker exec`
**Purpose:** Executes a new command inside an *already running* container. Used to log into a container!
**Example:** `docker exec -it my_web_server /bin/bash`

### `docker stop` & `docker start`
**Purpose:** Gracefully stops or wakes up a container.
**Example:** `docker stop my_web_server`

### `docker rm`
**Purpose:** Permanently deletes a stopped container.
**Crucial Flags:**
- `-f` (Force): Forces the deletion of a container even if it is currently running!
**Example:** `docker rm -f my_web_server`

---

## 📦 2. Image Management & Dockerfiles (Days 05, 06, 07)

Commands used to create, download, share, tag, and delete Docker Images.

### `docker images`
**Purpose:** Lists all Docker images currently downloaded and stored on your local host machine.
**Example:** `docker images`

### `docker pull`
**Purpose:** Downloads an image from Docker Hub to your local machine without running it.
**Example:** `docker pull ubuntu:20.04`

### `docker build`
**Purpose:** Reads a `Dockerfile` and automates building a custom Docker image layer by layer.
**Crucial Flags:**
- `-t <username>/<name>:<tag>` (Tag): Assigns a name and version tag to the image.
- `.` (Context): Tells Docker the Dockerfile is in the current directory.
**Example:** `docker build -t abhishekf5/my-node-app:v1.0 .`

### `docker commit`
**Purpose:** Manually creates a new image from a running container's changes (The old-school way).
**Example:** `docker commit c1 my_custom_image`

### `docker tag`
**Purpose:** Adds a metadata tag (like a shipping label) to an existing image so Docker Hub knows who owns it.
**Example:** `docker tag my_image username/my_image:v2.0`

### `docker push` & `docker login`
**Purpose:** Authenticates (`login`) and uploads (`push`) your custom image to Docker Hub to share it!
**Example:** `docker login -u <username>`
**Example:** `docker push username/my_image:v2.0`

### `docker rmi`
**Purpose:** Removes an Image from the host machine to free up disk space.
**Crucial Flags:**
- `-f` (Force): Forces deletion even if dependencies exist.
**Example:** `docker rmi -f ubuntu:latest`

---

## 💾 3. Volume & Storage Management (Day 04)

Commands for managing Named Volumes (storage entirely managed by Docker).

### `docker volume ls`
**Purpose:** Lists all Named Volumes managed by Docker on the host machine.
**Example:** `docker volume ls`

### `docker volume create`
**Purpose:** Creates a brand new Named Volume that can be mounted to containers.
**Example:** `docker volume create my_database_data`

### `docker volume rm`
**Purpose:** Deletes a Named Volume. (You cannot delete a volume currently mounted to a container).
**Example:** `docker volume rm my_database_data`

---

## 🌐 4. Networking & Inspection (Day 08)

Commands for isolating containers or bridging them together securely.

### `docker network ls`
**Purpose:** Lists all networks (bridge, host, none, and custom networks).
**Example:** `docker network ls`

### `docker network create`
**Purpose:** Creates a Custom Bridge network so containers can communicate using their Names (DNS resolution) instead of IP addresses!
**Crucial Flags:**
- `--driver bridge`: Explicitly sets the network type.
**Example:** `docker network create --driver bridge siva_network`

### `docker network connect` & `docker network disconnect`
**Purpose:** Dynamically plugs (or unplugs) a running container into a specific network.
**Example:** `docker network connect common_network N1`

### `docker inspect`
**Purpose:** Spits out a massive JSON payload of detailed metadata about a container, image, or network. Used to find the private IP addresses of containers!
**Example:** `docker inspect bridge`
**Example:** `docker inspect my_web_server`

---

## 🧹 5. Mass Cleanup & Troubleshooting (Bonus)

These commands save lives when you are troubleshooting port conflicts or cleaning up environments.

### The Mass Cleanup Command
**Purpose:** Kills and deletes EVERY SINGLE container on your EC2 host machine simultaneously. Use with extreme caution!
**Example:** `docker rm -f $(docker ps -aq)`

### Finding & Killing Port Conflicts (Linux native)
**Purpose:** If Docker says `Bind for 0.0.0.0:80 failed: port is already allocated`, use these commands to find the rogue process and kill it!
**Step 1 (Find the PID):** `lsof -i :80`
**Step 2 (Kill the PID):** `kill -9 <Process_ID>`

---

## 🏗️ 6. Docker Compose (Day 10)

Commands for orchestrating multi-container applications using a `docker-compose.yml` file.

### `docker-compose up`
**Purpose:** Reads the YAML file and spins up your entire architecture (Networks, Volumes, and Services).
**Crucial Flags:**
- `-d` (Detached): Runs the entire stack in the background.
**Example:** `docker-compose up -d`

### `docker-compose down`
**Purpose:** Gracefully stops and deletes all containers and networks defined in the YAML file. (It safely ignores Volumes by default to protect your data!).
**Example:** `docker-compose down`

### `docker-compose ps`
**Purpose:** Lists only the running containers that are managed by the current compose file.
**Example:** `docker-compose ps`

### `docker-compose logs`
**Purpose:** Streams the terminal logs for ALL services in the compose file simultaneously.
**Crucial Flags:**
- `-f` (Follow): Keeps the terminal open and actively streams new logs as they happen.
**Example:** `docker-compose logs -f`

---

## 🛡️ 7. Security & Resource Limits (Day 12)

Commands used to lock down containers and protect the host server from crashes.

### `docker run` (Security Flags)
**Purpose:** Spins up a container with strict security and resource constraints.
**Crucial Flags:**
- `--memory="<size>"`: Hard limits the amount of RAM the container can use (e.g., `512m`, `1g`).
- `--cpus="<number>"`: Limits the number of CPU cores the container can consume (e.g., `1.5`).
- `--read-only`: Forces the container's file system to be entirely read-only, preventing hackers from installing malware.
**Example:** `docker run -d --name secure_web --memory="512m" --cpus="1.0" --read-only -p 80:80 nginx`

### `docker scout cves`
**Purpose:** Scans a Docker image layer by layer for known vulnerabilities and security threats before deployment.
**Example:** `docker scout cves ubuntu:latest`

---

## 🐝 8. Docker Swarm Orchestration (Day 13)

Commands used to manage a cluster of Docker servers.

### `docker swarm init`
**Purpose:** Turns the current host machine into a Swarm Manager node.
**Example:** `docker swarm init --advertise-addr <PRIVATE_IP>`

### `docker swarm join`
**Purpose:** Adds a worker node to an existing Swarm cluster (requires the token from `init`).
**Example:** `docker swarm join --token <TOKEN> <MANAGER_IP>:2377`

### `docker service create` & `scale`
**Purpose:** Deploys and scales a container across multiple servers in the cluster.
**Example:** `docker service create --name my_web --replicas 3 -p 80:80 nginx`
**Example:** `docker service scale my_web=10`

---

## 🧽 9. Enterprise Maintenance (Day 14)

Commands to keep the host machine perfectly healthy.

### `docker system prune`
**Purpose:** The ultimate cleanup command. Deletes all stopped containers, unused networks, dangling images, and unused build cache.
**Crucial Flags:**
- `-a`: Deletes ALL unused images (not just dangling ones).
- `--volumes`: Deletes all unused named volumes.
- `-f`: Forces deletion without prompting for confirmation.
**Example:** `docker system prune -a --volumes -f`

---

## 🚀 10. Advanced Masterclass (Day 15)

Commands used by the top 1% of Docker engineers.

### `docker buildx build`
**Purpose:** Compiles a Docker image for multiple processor architectures simultaneously (e.g., ARM and AMD64).
**Example:** `docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest --push .`

### `docker context create` & `use`
**Purpose:** Links your local laptop's Docker CLI to a remote production server, allowing you to manage remote containers without SSH.
**Example:** `docker context create production --docker "host=ssh://ubuntu@<IP>"`
**Example:** `docker context use production`

---

## 🔐 11. DevSecOps & Edge Cases (Day 16)

Commands and configurations for highly specialized, secure environments.

### `DOCKER_CONTENT_TRUST`
**Purpose:** An environment variable that forces Docker to cryptographically verify the digital signature of an image before pulling or running it, preventing malware injection.
**Example:** `export DOCKER_CONTENT_TRUST=1`

### `docker run --init`
**Purpose:** Injects a tiny process manager (`tini`) into the container to run as PID 1, preventing Zombie processes from crashing Node.js or Java applications.
**Example:** `docker run -d --name web --init my_node_app`

### The Docker Socket (`docker.sock`)
**Purpose:** A volume mount used to pass control of the host's Docker engine *into* a container (Docker-in-Docker). Used heavily by CI/CD agents like Jenkins.
**Example:** `docker run -d -v /var/run/docker.sock:/var/run/docker.sock jenkins`
