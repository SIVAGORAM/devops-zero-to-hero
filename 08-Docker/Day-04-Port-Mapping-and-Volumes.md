# Day 04: Port Mapping & Volumes (The Interview Guide)

Welcome to Day 04! Today we are tackling two concepts that confuse many beginners: **Port Mapping** and **Volumes**. 

If you understand these two concepts, you will be able to answer 90% of Docker interview questions.

Let's make this incredibly simple. Think of a Docker container as a locked, soundproof box. 
1. **Port Mapping** is how we drill a hole in the box so people can talk to the application inside (Networking).
2. **Volumes** is how we give the box a memory so that if the box is destroyed, our data is saved (Storage).

---

## 🚪 Part 1: Port Mapping (Networking)

### The Theory: Why do we need Port Mapping?
By default, **containers are 100% isolated**. 
Imagine you install an NGINX web server directly on your Ubuntu EC2 instance on Port 80. Anyone on the internet can type your IP address and see the website. 
But, if you run NGINX *inside a Docker Container*, the website is locked inside the container. Even if you type the EC2 IP address, it will fail because the EC2 instance doesn't know what is happening inside the sealed container.

**The Solution:** We use Port Mapping (`-p`) to build a bridge between your EC2 Host Machine and the Docker Container.

**The Hotel Analogy:** Think of your EC2 machine as a Hotel Reception Desk, and the Docker Container as Room 80. When a user on the internet calls the Reception Desk on port 8080, the receptionist transfers the call directly to Room 80.

### The Syntax
The magic flag is `-p HOST_PORT:CONTAINER_PORT`.
- **HOST_PORT:** The port opened on your AWS EC2 instance.
- **CONTAINER_PORT:** The port the application is actively listening to inside the container.

### Hands-On: Hosting Jenkins
Let's host Jenkins, a popular CI/CD tool that runs on port 8080.

1. **Run the Jenkins container and map the port:**
   ```bash
   docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
   ```
2. **AWS Security Group:** Go to your AWS Console, find your EC2 Security Group, and Edit Inbound Rules to **Allow Port 8080** from the internet (0.0.0.0/0).
3. **Test it:** Open your browser and go to `http://<YOUR_EC2_IP>:8080`. You will see Jenkins!

### 🚨 Interview Troubleshooting: Port Conflicts
**Interview Question:** *"You try to run a Jenkins container using `-p 8080:8080`, but Docker throws an error saying 'Port is already allocated'. What do you do?"*

**The Answer:**
*"A host port can only be used by one process at a time. Someone else is already using port 8080 on the EC2 machine. I have two options:*
*1. **Kill the blocking process:** I can run `sudo lsof -i :8080` to find the process ID, and then `kill -9 <PID>` to stop it.*
*2. **Map to a different Host Port (The Docker Way):** I can simply map an empty host port (like 9090) to the container's 8080 port by running `docker run -p 9090:8080 jenkins`. The users will just access the app via port 9090!"*

---

## 💾 Part 2: Docker Volumes (Storage)

### The Theory: Why do we need Volumes?
Containers are **Ephemeral** (temporary). If you run a database container, save 1,000 user records into it, and then run `docker rm -f`, **all 1,000 records are permanently deleted.**

**The Solution:** Volumes (Folder Mapping). 
Instead of saving data *inside* the container, we map a folder inside the container directly to a folder on the EC2 Host's hard drive. 

**The USB Analogy:** Think of a Volume like plugging a USB drive into a laptop. If the laptop (the container) explodes, your data is perfectly safe on the USB drive (the Host EC2 machine).

### Hands-On: Creating a Volume
Let's share a folder between our EC2 Host and a CentOS container using the `-v` (volume) flag.

**The Syntax:** `-v HOST_FOLDER_PATH:CONTAINER_FOLDER_PATH`

1. **Start a container with a mapped volume:**
   ```bash
   docker run --name c1 -it -v /tmp/host:/tmp/cont centos /bin/bash
   ```
2. **Create a file INSIDE the container:**
   ```bash
   cd /tmp/cont
   touch dummy_file.txt
   exit
   ```
   *(Typing `exit` stops the container. In theory, the file should be gone, right?)*
3. **Check the EC2 Host machine:**
   ```bash
   cd /tmp/host
   ls
   ```
   **Magic!** You will see `dummy_file.txt` sitting safely on your EC2 host machine! Even though the container is dead, the data survived.

*(Note: You can even spin up a completely new container `c2`, attach the exact same volume to it, and `c2` will instantly have access to `dummy_file.txt`!)*

---

## 📚 The 3 Types of Volumes (Interview Essential)

If an interviewer asks you about Volumes, you MUST mention these three types:

| Type | How it Works | When to Use It |
| :--- | :--- | :--- |
| **1. Bind Mounts** | This is what we did in the hands-on. You explicitly provide a specific folder path on the host machine (`/tmp/host`). | When you need to share specific configuration files or SSL certificates from the host machine into the container. |
| **2. Named Volumes** | You let Docker manage the host folder. You just say `-v my_database_data:/var/lib/mysql`. Docker creates a secure folder in `/var/lib/docker/volumes` automatically. | **BEST PRACTICE.** This is the safest and most recommended way to store persistent database data. |
| **3. Anonymous Volumes** | You don't provide a name or a path. You just say `-v /var/lib/mysql`. Docker generates a crazy random string for the folder name. | Rarely used. If the container is deleted, it's very hard to find the random folder to recover the data. |
