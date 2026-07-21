# Day 11: Networking Foundations for DevOps

As a DevOps Engineer, networking is arguably the most critical and often misunderstood skill. When a microservice cannot talk to a database, or a web application is unreachable, it is almost always a networking issue. We will learn networking from a practical DevOps perspective.

---

## 1. The OSI Model (Simplified)

The OSI (Open Systems Interconnection) model explains how data travels from an application on your laptop to an application on a server across the world. It has 7 layers, but in DevOps, you only really care about three:

- **Layer 3 (Network Layer):** Deals with **IP Addresses** and Routers. How does a packet find its way across the internet?
- **Layer 4 (Transport Layer):** Deals with **Ports** and **TCP/UDP**. Once the packet reaches the correct server, which port (application) should it go to?
- **Layer 7 (Application Layer):** Deals with **HTTP/HTTPS** and DNS. This is what your web browser or API actually speaks.

---

## 2. IP Addresses (The Basics)

An IP address is a unique identifier for a machine on a network. 

### IPv4 vs IPv6
- **IPv4:** The standard format (`192.168.1.10`). It has roughly 4.3 billion combinations, which we ran out of globally.
- **IPv6:** Created to solve the shortage. Much longer and complex, but IPv4 is still heavily used internally in corporate networks and AWS.

### Public vs. Private IPs
- **Public IP:** A globally unique address routable over the internet. If you host a website, it must have a Public IP.
- **Private IP:** Used *inside* a private network (like an office network or an AWS VPC). Private IPs cannot be reached from the internet. 

*DevOps Best Practice:* Your databases and internal microservices should **only** have Private IPs to prevent hackers from reaching them directly. Only your Load Balancers should have Public IPs.

---

## 3. Subnetting & CIDR (Crucial for AWS VPCs)

When you build a network in the cloud (AWS VPC), you have to define its size using CIDR notation.

### CIDR Notation (Classless Inter-Domain Routing)
CIDR is a method for allocating IP addresses and IP routing. It looks like this: `10.0.0.0/16`.

The `/16` (the prefix) dictates how many IP addresses are available in this network.
- **`/32`**: 1 single IP address (e.g., `10.0.0.1/32` means exactly this one computer).
- **`/24`**: 256 IP addresses (Standard for a small subnet).
- **`/16`**: 65,536 IP addresses (Standard for an entire AWS VPC).

*Why it matters:* You will design networks in AWS. If you make your subnets too small (e.g., `/28` which is 16 IPs), you will quickly run out of IPs as your application auto-scales.

---

## 4. TCP vs UDP (The Transport Layer)

Once an IP routes data to the right server, Layer 4 decides *how* to deliver it.

### TCP (Transmission Control Protocol)
- **Reliable:** Requires a "3-way handshake" (SYN, SYN-ACK, ACK) to establish a connection before sending data.
- **Guarantees delivery:** If a packet drops, TCP resends it.
- **Use Cases:** Web browsing (HTTP/HTTPS), SSH, Database connections, File transfers. 99% of DevOps work involves TCP.

### UDP (User Datagram Protocol)
- **Unreliable but Fast:** Just throws data at the destination without checking if it arrived (No handshake).
- **Use Cases:** Video streaming (Zoom, Netflix), Online Gaming, DNS lookups. (If a frame of video drops, you don't resend it, you just keep playing the video).

---

## 5. Ports (The Doors to the Server)

If an IP address is a building's street address, a **Port** is a specific apartment door inside that building. A server has 65,535 ports available.

**Crucial Ports You Must Memorize:**
- **22:** SSH (Secure Shell) - Used by DevOps to log into Linux servers.
- **80:** HTTP - Unencrypted web traffic.
- **443:** HTTPS - Secure, encrypted web traffic.
- **3306:** MySQL Database default port.
- **5432:** PostgreSQL Database default port.
- **27017:** MongoDB default port.
- **8080 / 3000:** Common development ports for Node.js, Java, etc.

*DevOps Rule:* In a Cloud Firewall (AWS Security Group), **deny everything by default**. Only explicitly open the ports you need (e.g., open port 443 to the world, but only open port 22 to your office IP).

---

## ðŸŽ¯ Day 11 Summary
You now understand how machines identify each other (**IPs**), how networks are sized (**CIDR**), how data is reliably transmitted (**TCP**), and how specific applications receive that data (**Ports**). Next, we will cover DNS and Load Balancers!

---
**[⬅️ Previous: Day 10 - Advanced Linux](../02-Linux/Day-10-Advanced-Linux-for-DevOps.md)** | **[➡️ Next: Day 12 - Advanced Networking](./Day-12-Advanced-Networking.md)**

