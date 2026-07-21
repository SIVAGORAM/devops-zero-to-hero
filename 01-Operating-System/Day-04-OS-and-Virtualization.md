# Day 4: Servers, Virtualization, and Operating Systems

Welcome to Day 4! Today we transition from the theory of how software is built into the actual infrastructure it runs on. Everything a DevOps engineer does revolves around servers, virtual machines, and operating systems.

---

## 1. What is a Server?
A **Server** is a powerful computer designed to provide services, applications, or data to other computers (clients) over a network.
- **Unlike a laptop**, a server runs 24/7, handles millions of users, and is stored in massive, highly cooled facilities called **Data Centers**.
- **Real-Life Example:** When you type `amazon.com`, your browser sends a request to an Amazon server. The server processes the request and sends the webpage back to your laptop.

---

## 2. The Problem with Physical Servers
Traditionally, companies bought physical servers for specific teams (e.g., Team A gets Server 1, Team B gets Server 2). 

**The Problem: Resource Inefficiency**
- Team A might only use 10% of their server's CPU and RAM. The rest goes to waste.
- Team B might need 120% of their server's capacity and experience crashes.
- Physical servers are expensive, hard to maintain, and take weeks to purchase and install.

This inefficiency led to the greatest invention in cloud computing: **Virtualization**.

---

## 3. Virtualization & Virtual Machines (VM)
A **Virtual Machine (VM)** is a software-based computer that behaves exactly like a real physical computer. It has its own OS, CPU, RAM, and storage, but it runs *inside* a physical server.

- **Real-Life Analogy:** Think of a physical server as a massive apartment building. A Virtual Machine is a single apartment inside that building. Everyone shares the building's foundation, but each apartment is completely private.

### What is a Hypervisor?
A **Hypervisor** is the magic software installed on the physical server that makes Virtual Machines possible. It divides the physical CPU, RAM, and Storage and gives a piece to each Virtual Machine securely.

**Type 1 vs Type 2 Hypervisors (Crucial Concept):**
- **Type 1 (Bare-Metal):** Installed *directly* on the physical hardware. There is no underlying Operating System. This is what enterprise data centers and AWS use (e.g., VMware ESXi, KVM, Xen). It provides maximum performance.
- **Type 2 (Hosted):** Installed on top of an existing Operating System (like Windows or Mac). This is what you use on your personal laptop to practice (e.g., Oracle VirtualBox, VMware Workstation).

- **Without a Hypervisor:** 1 Physical Server = 1 OS = 1 Application (Huge waste).
- **With a Hypervisor:** 1 Physical Server = 50 Virtual Machines = 50 Applications (Maximum efficiency).

### AWS EC2: The Real World Example
When you log into AWS (e.g., from Hyderabad) and request an Ubuntu server with 10GB RAM in Mumbai:
1. AWS finds a physical server in Mumbai with spare capacity.
2. The Hypervisor on that physical server instantly carves out 10GB of RAM.
3. It boots up a Virtual Machine and gives you the IP address.
*Note: In AWS, a Virtual Machine is called an **EC2 Instance**.*

---

## 4. Hardware Fundamentals (CPU, RAM, Storage)

### CPU (Central Processing Unit)
The "brain" of the computer that executes instructions.
- **Core:** An independent processing unit inside a CPU. A 4-core CPU can do 4 things at once.
- **Thread:** The smallest unit of work a core can handle.
- **vCPU (Virtual CPU):** When you rent a Virtual Machine in the cloud, you are assigned vCPUs. The hypervisor translates your vCPUs into physical core power.

### RAM (Random Access Memory)
Temporary, lightning-fast memory. It stores the data for applications that are *currently running*.
- *Analogy:* Your desk space. The more desk space you have, the more books you can open at once. If RAM fills up, the server crashes.

### Storage (HDD vs SSD)
Permanent memory where files, databases, and the OS are saved even when the power is off.
- **HDD (Hard Disk Drive):** Old, mechanical, spinning disks. Cheap but slow.
- **SSD (Solid State Drive):** Flash memory with no moving parts. Extremely fast and durable. (Standard in the cloud).

### Vertical vs. Horizontal Scaling (Crucial DevOps Concept)
When your server runs out of CPU or RAM because too many users are visiting your application, you have two choices:
- **Vertical Scaling (Scale Up):** Adding more CPU and RAM to your *existing* server. (Example: Upgrading a VM from 4GB RAM to 16GB RAM). *Limitation: A single physical server can only hold so much RAM before it hits a limit.*
- **Horizontal Scaling (Scale Out):** Adding *more servers* to share the load. (Example: Going from 1 server to 5 identical servers). *This is the DevOps standard, as cloud computing allows us to spin up infinite horizontal servers using auto-scaling.*

**Wait, how do 5 servers share one website? (The Load Balancer)**
If you horizontally scale to 5 servers, how do users know which one to connect to? You place a **Load Balancer** in front of them. Users connect to the Load Balancer, and it intelligently distributes the traffic evenly across all 5 servers so no single server gets overwhelmed.

---

## 5. Operating Systems & Linux

An **Operating System (OS)** acts as the bridge between your applications and the physical hardware. (Applications " OS " Hardware).

### Why Linux is King in DevOps
While laptops use Windows or macOS, almost all cloud servers run **Linux**.
- It is free, incredibly fast, secure, stable, and has no graphical interface (GUI), meaning 100% of the server's power goes to running the application.
- **Ubuntu** is the most popular, beginner-friendly version (distribution) of Linux used in cloud environments.

---

## 6. Networking Fundamentals (IP & SSH)

### IP Addresses & DNS
A unique numerical address assigned to a device on a network so it can be found.
- **Private IP:** Used for internal communication inside a private network (e.g., `10.0.0.5`). Cannot be accessed from the internet.
- **Public IP:** A globally unique address reachable from the internet (e.g., `203.0.113.25`).

**What is DNS (Domain Name System)?**
Humans cannot easily remember IP addresses like `203.0.113.25`. **DNS** acts as the phonebook of the internet. It translates human-readable domain names (like `amazon.com`) into the underlying Public IP address of the server.

### SSH (Secure Shell)
**SSH** is a secure, encrypted protocol used to remotely connect to and control a server over the internet.
- Since data centers are thousands of miles away, DevOps engineers use SSH daily to log into Linux servers, install software, and fix issues from their laptops.
- *Command:* `ssh ubuntu@203.0.113.25`

**What is a Port?**
If an IP address is the street address of a building, a **Port** is the specific door to enter. 
- SSH always uses **Port 22**. If Port 22 is closed by a firewall (like an AWS Security Group), you cannot connect to the server, even if the IP is correct.

**Passwords vs. SSH Keys:**
In enterprise environments, you never use passwords to log into servers because they can be guessed by hackers. Instead, you use an **SSH Key Pair**:
- **Public Key:** Placed on the server (acts like a lock).
- **Private Key:** A secure file kept on your laptop (acts like the physical key). If you have the private key file, you can log in; if you don't, you are blocked.

---

## Day 4 Summary
You now understand the physical and virtual infrastructure that powers the internet. A developer writes code on their laptop, but a DevOps engineer uses **SSH** to connect to an **Ubuntu Virtual Machine (EC2)** created by a **Hypervisor**, allocating **vCPUs, RAM, and SSD storage** via a **Public IP** to serve that application to the world!

---
**[Next: Day 4 (Advanced) - OS for DevOps](./Day-04-Advanced-OS-for-DevOps.md)**

