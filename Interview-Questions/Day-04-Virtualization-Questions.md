# Day 4: Virtualization & Infrastructure - Interview Questions

These questions test your fundamental understanding of hardware, virtualization, and how cloud providers actually work under the hood.

---

### Q1: What is a Server, and how is it different from a personal computer?
**Interview Answer:**  
"A server is a high-performance computer designed to provide services, applications, or data to other client computers over a network. Unlike a personal laptop, a server is built with enterprise-grade hardware to run 24/7, handle thousands of simultaneous connections, and is typically housed in a highly controlled data center."

---

### Q2: What is a Virtual Machine (VM)?
**Interview Answer:**  
"A Virtual Machine is a software-defined computer that runs on top of physical hardware. It has its own dedicated operating system, virtual CPU, memory, and storage, but it shares the underlying physical server's resources with other VMs. This allows us to run multiple isolated applications on a single physical server, maximizing efficiency."

---

### Q3: What is a Hypervisor and why is it important?
**Interview Answer:**  
"A hypervisor is the software that creates, manages, and isolates virtual machines. It sits between the physical hardware and the VMs, securely allocating physical CPU, RAM, and storage to each virtual instance. Without hypervisors, modern cloud computing (like AWS EC2) would be impossible because we wouldn't be able to share physical server resources efficiently."

---

### Q4: Explain the difference between a Physical Machine and a Virtual Machine.
**Interview Answer:**  
"A physical machine is the actual, tangible hardware sitting in a data center. A virtual machine is a software emulation of a computer running on that hardware. In the past, companies wasted money dedicating one physical machine to one application. Today, we use virtualization to pack dozens of virtual machines onto a single physical machine, drastically reducing costs."

---

### Q5: What is a vCPU?
**Interview Answer:**  
"A vCPU stands for Virtual CPU. When we provision a virtual machine in a cloud environment like AWS, we don't get direct access to a physical CPU core. Instead, the hypervisor allocates a vCPU, which represents a share of the underlying physical CPU's processing power assigned specifically to our VM."

---

### Q6: What is the difference between a Public IP and a Private IP?
**Interview Answer:**  
"A Public IP is a globally unique address that is routable and accessible over the public internet. A Private IP is used strictly for internal communication within a private network (like an AWS VPC) and cannot be reached directly from the outside world. We use Private IPs for secure backend server communication, and Public IPs for servers that need to serve web traffic to users."

---

### Q7: What is SSH and why do DevOps engineers use it?
**Interview Answer:**  
"SSH, or Secure Shell, is an encrypted network protocol used to securely connect to and manage remote servers over an unsecured network like the internet. As a DevOps engineer, I use SSH daily to log into remote Linux servers to deploy applications, check logs, and troubleshoot issues without needing physical access to the data center."

---

### Q8: How would you summarize what a server is if you wanted to sound like a senior engineer?
**Interview Answer:**  
"A server is a compute instance designed to provide services over a network. It typically runs a minimal operating system like Linux to maximize resources, uses allocated vCPUs, RAM, and SSD storage to process requests, communicates via Private and Public IP addresses, and is accessed and managed remotely using encrypted protocols like SSH. In modern cloud architecture, these servers are dynamically provisioned virtual machines, such as AWS EC2 instances."

---

### Q9: What is the difference between a Type 1 and Type 2 Hypervisor?
**Interview Answer:**  
"A Type 1, or Bare-Metal hypervisor, is installed directly onto the physical server hardware without a base operating system—this is what cloud providers like AWS use for maximum performance. A Type 2, or Hosted hypervisor, runs as an application on top of a host operating system (like Windows or macOS), which is what we use on our local laptops like VirtualBox."

---

### Q10: What port does SSH use by default, and how do you secure it?
**Interview Answer:**  
"SSH uses Port 22 by default. To secure it, we completely disable password authentication and instead use SSH Key Pairs (a Public and Private key). Furthermore, in a cloud environment like AWS, we restrict Port 22 in the Security Group so that only specific, trusted IP addresses can even attempt to connect to the server."

---

### Q11: What is the difference between Vertical Scaling and Horizontal Scaling?
**Interview Answer:**  
"Vertical scaling, or scaling up, means adding more power (CPU, RAM) to an existing server. It's limited by the maximum capacity of the underlying physical hardware. Horizontal scaling, or scaling out, means adding more servers to distribute the traffic load. As a DevOps engineer, horizontal scaling is highly preferred because we can use cloud auto-scaling to add or remove servers dynamically based on traffic, ensuring infinite scalability and high availability without downtime."

---

### Q12: What is a Load Balancer and why is it necessary for Horizontal Scaling?
**Interview Answer:**  
"If we horizontally scale an application across five identical servers, users can't manually guess which server's IP to connect to. A Load Balancer sits in front of these servers, acting as a single entry point. It receives all incoming user traffic and intelligently distributes it across the five backend servers, ensuring no single server becomes overwhelmed and that the application remains highly available."

---

### Q13: What is DNS?
**Interview Answer:**  
"DNS stands for Domain Name System. It essentially acts as the internet's phonebook, translating human-readable domain names like `google.com` into the machine-readable Public IP addresses that servers use to communicate. This ensures that users don't have to memorize complex strings of numbers just to access a website."


---

### Q14: What is the difference between User Space and Kernel Space?
**Interview Answer:**  
"The operating system is divided into two areas for security. The Kernel Space is where the core of the OS runs, with unrestricted access to the CPU, RAM, and hardware. User Space is where normal applications like Docker, Nginx, or Python run. Applications in User Space cannot access hardware directly; they must make a System Call (Syscall) to politely ask the kernel to perform hardware tasks on their behalf."

---

### Q15: What is a Zombie Process, and how do you kill it?
**Interview Answer:**  
"A Zombie Process is a child process that has finished executing and died, but its parent process hasn't read its exit status yet. It uses no CPU or memory, but it takes up a slot in the process table. Because it's already dead, you cannot kill a zombie process directly. To remove it, you must either wait for the parent to read the status, or you must forcefully kill the parent process itself."

---

### Q16: Why might a Linux server show 95% RAM usage, but the system is actually perfectly healthy?
**Interview Answer:**  
"Linux intentionally uses almost all free, unused RAM to cache frequently accessed disk files (known as the Page Cache) to dramatically speed up read operations. If you run `free -h`, the 'Used' column might look dangerously high, but the 'Available' column will show the true amount of RAM that can instantly be reclaimed if an application actually needs it."

---

### Q17: What is the OOM Killer and why is it important in containerized environments?
**Interview Answer:**  
"The Out-Of-Memory (OOM) Killer is a kernel feature that activates when the server completely runs out of RAM. To prevent the entire OS from crashing, it calculates a score and mercilessly kills the process consuming the most memory. In environments like Docker and Kubernetes, if a container exceeds its memory limit, the OS triggers the OOM Killer on that specific container, resulting in an `OOMKilled` exit status."

---

### Q18: What are Namespaces and Cgroups, and how do they relate to Docker?
**Interview Answer:**  
"Namespaces and Cgroups are native Linux kernel features that make containers possible. Namespaces provide isolation by restricting what a process can *see* (giving it a private process tree, network stack, and mount points). Cgroups (Control Groups) provide resource limiting by restricting what a process can *use* (capping its CPU and RAM). Docker is fundamentally just a user-friendly tool that manages these two features to run isolated processes."


---
**[➡️ Next: Day 5 - AWS EC2 Questions](./Day-05-AWS-EC2-Questions.md)**
