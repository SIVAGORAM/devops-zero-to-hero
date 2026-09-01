# Day 03: Attached vs Detached Mode & Deep Dive into Containers

Welcome to Day 03! Today we are learning how Docker is used in the **real world**. In production environments, we do not stare at terminal screens watching containers run. We run them in the background. 

Today we master **Detached Mode**, understand how to peek inside background containers, and learn how to clean up our environments!

---

## 1. The Core Fundamentals (Recap & Comparisons)

Before we start running complex commands, we must have crystal-clear definitions of the components we are working with.

### What is the difference between an Image and a Container?

| Feature | Docker Image | Docker Container |
| :--- | :--- | :--- |
| **Definition** | A static, read-only template containing the application, environment, and OS libraries. | A running, executing instance of a Docker Image. |
| **State** | Dead / Static / At Rest. | Alive / Active / Running process. |
| **Analogy** | The blueprint for a house. | The actual physical house built from the blueprint. |
| **Mutability** | Cannot be changed once created (Immutable). | Can be modified, written to, or deleted (Mutable). |
| **Resources** | Only consumes hard drive space. | Consumes active resources (CPU, RAM) from the Host Machine. |
| **Dependencies** | Exists entirely on its own. | Cannot exist without an Image to build from. |

---

## 2. The Two Execution Models: Attached vs Detached

When you run a container using `docker run`, you have to choose *how* you want to run it. 

### The Differences at a Glance
| Feature | Attached Mode (Foreground) | Detached Mode (Background) |
| :--- | :--- | :--- |
| **Command Flag** | `-it` (Interactive Terminal) | `-d` (Detached) |
| **Behavior** | Terminal locks onto the container. You see its output immediately. | Container starts in the background. Terminal is immediately freed up for you. |
| **How to Exit** | Typing `exit` kills the container process. | The container runs indefinitely until you explicitly type `docker stop`. |
| **Real-World Usage** | Used for debugging or exploring an environment quickly. | **99% of daily life.** Used for running live databases, web servers, and APIs. |

### The `Attached` Mode Trap
Before mastering Detached mode, we must understand the danger of Attached mode. Imagine you run:
```bash
docker run -it --name devops centos
```
You are now inside the container. You can prove it by checking the OS version (`cat /etc/os-release`) or checking the running processes (`ps -ef`). 
But what happens when you type `exit`?
**What happened internally?**
When you type `exit` in Attached Mode, you are killing the primary process (the shell) of the container. Because a container *is* a process, when its primary process dies, **the entire container dies/stops.** 

---

## 3. Hands-On: Mastering Detached Mode

In the real world, we want containers to run silently in the background (like a web server waiting for traffic). Let's create one!

Run this exact command in your terminal:
```bash
docker run -d --name siva centos /bin/bash -c "while true; do echo hello; sleep 8; done"
```

### Let's break down EVERY keyword so you understand it perfectly:
- `docker run`: The master command. Internally it does 4 things: checks for the image, downloads it if missing, creates the container, and starts it.
- `-d`: **Detached**. Tells Docker, *"Leave this container running in the background and give me my terminal back immediately."*
- `--name siva`: Assigns a human-readable name instead of a random string. *(Note: Docker does not allow duplicate names!)*
- `centos`: The Image blueprint we are using.
- `/bin/bash`: The specific program we want the container to run when it wakes up (a bash shell).
- `-c "while true..."`: We are passing a script to the bash shell. This creates an infinite loop that prints "hello", sleeps for 8 seconds, and repeats forever.

**What happens internally?**
Docker creates the container, starts the infinite loop, and immediately releases your terminal. The container is now alive and working silently in the background!

---

## 4. How to Interact with Detached Containers

Since the container is in the background, how do we know it's actually working?

### 1. View the Logs
To see what a background container is outputting, we use the `logs` command.
```bash
docker logs -f siva
```
- `-f` (Follow): This flag tells Docker to stream the logs live. You will see "hello" print on your screen every 8 seconds! Press `Ctrl+C` to stop watching (this does NOT stop the container).

### 2. Execute a Single Command (Without Attaching)
What if you want to check the `/tmp` folder inside the background container, but you don't want to log completely into it?
```bash
docker exec siva ls /tmp
```
- `exec`: Tells Docker to execute a *secondary* process inside an already-running container. It grabs the results of `ls /tmp` and brings them back to your terminal.

### 3. Log into a Detached Container safely
Sometimes, you need to go inside the running background container to investigate.
```bash
docker exec -it siva /bin/bash
```
*What happens internally?*
You are asking Docker to open a **secondary** interactive terminal (`-it`) inside the container. 
When you type `exit` here, you are only killing this *secondary* terminal process. The primary process (the infinite loop) keeps running, meaning **the container stays alive!** This is much safer than `docker attach`.

---

## 5. The Ultimate Cleanup (Housekeeping)

Eventually, you need to destroy things. Here is exactly how to clean up your environment.

### Stopping vs Removing
- `docker stop siva`: Sends a graceful shutdown signal to the container. The container falls asleep (goes into the `Exited` state).
- `docker rm siva`: Permanently deletes the sleeping container from your hard drive. *(Note: You cannot `rm` a container that is currently running unless you use `docker rm -f` to force kill it).*
- `docker rmi centos`: Deletes the downloaded Image (blueprint) from your hard drive to save space.

### Mass Cleanup (Zero to Hero Trick!)
Over time, you will have dozens of sleeping containers and unused images. Deleting them one by one is exhausting. Use these powerful commands:

**Delete ALL containers (running or stopped) at once:**
```bash
docker rm -f $(docker ps -aq)
```
*Internal breakdown:* The inner command `docker ps -aq` generates a list of just the IDs of all containers. It passes that massive list to the `docker rm` command, which deletes them all instantly!

**Delete ALL downloaded Images at once:**
```bash
docker rmi -f $(docker images -q)
```

You are now a master of Container Execution and Lifecycle management! Ready for Day 04?
