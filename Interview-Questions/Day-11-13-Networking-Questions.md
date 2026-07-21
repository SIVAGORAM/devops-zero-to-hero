# Day 11-13: Networking for DevOps - Interview Questions

These questions test your understanding of how traffic flows from the user's browser, through the internet, and securely into your application servers.

---

### Q1: What is the difference between TCP and UDP? When would you use each?
**Interview Answer:**  
"TCP (Transmission Control Protocol) is connection-oriented and highly reliable. It uses a 3-way handshake to establish a connection and guarantees data delivery by re-sending dropped packets. It's used for HTTP, SSH, and database connections. UDP (User Datagram Protocol) is connectionless and fast, but unreliable because it doesn't guarantee delivery. It is used for real-time applications like video streaming or DNS queries where speed is more important than perfect accuracy."

---

### Q2: You have a database in AWS. Should you give it a Public IP or a Private IP, and why?
**Interview Answer:**  
"A database should always be assigned a Private IP and placed in a private subnet. Giving a database a Public IP exposes it directly to the public internet, dramatically increasing the surface area for a brute-force or DDoS attack. Instead, the database should only be accessible internally via its Private IP from our application servers."

---

### Q3: What happens when a user types `google.com` into their browser? (Explain DNS)
**Interview Answer:**  
"First, the browser checks its local cache. If the IP isn't found, it queries a DNS Resolver (like an ISP or Google's 8.8.8.8). The resolver queries the Root DNS servers, which direct it to the TLD servers for `.com`, which finally direct it to Google's Authoritative Name Server. The Name Server returns the A Record (the IPv4 address) back to the browser, allowing the browser to establish a TCP connection to that IP address."

---

### Q4: Explain the difference between an A Record and a CNAME Record.
**Interview Answer:**  
"An A (Address) Record maps a domain name directly to a specific IPv4 address (e.g., `myapp.com -> 192.168.1.5`). A CNAME (Canonical Name) Record maps a domain name to another domain name (e.g., `www.myapp.com -> myapp.com`). We use CNAMEs frequently in the cloud to point our domains to AWS Load Balancers, which give us a dynamic DNS name rather than a static IP address."

---

### Q5: What is the difference between a Layer 4 and Layer 7 Load Balancer?
**Interview Answer:**  
"A Layer 4 Load Balancer operates at the Transport layer, routing traffic based purely on IP addresses and TCP/UDP ports. It is extremely fast but cannot inspect the traffic. A Layer 7 Load Balancer operates at the Application layer. It can inspect the actual HTTP/HTTPS traffic, allowing us to route requests based on URL paths (e.g., sending `/api` traffic to one server cluster and `/images` to another)."

---

### Q6: What is a NAT Gateway and why do we need it?
**Interview Answer:**  
"A NAT (Network Address Translation) Gateway is a service that allows servers in a private network (which have no public IPs) to securely reach out to the public internet to download updates or patches. The NAT Gateway sits in a public subnet, takes the request from the private server, swaps the private IP for its own public IP, and forwards the request to the internet, keeping the private server completely hidden from inbound internet traffic."

---

### Q7: Explain the difference between Stateful and Stateless firewalls (Security Groups vs NACLs).
**Interview Answer:**  
"AWS Security Groups act as stateful firewalls at the instance level. If a stateful firewall allows an incoming request, it automatically allows the outbound response, regardless of outbound rules. Network ACLs (NACLs) act as stateless firewalls at the subnet level. If a stateless firewall allows an incoming request, you must explicitly write an outbound rule allowing the return traffic, otherwise, the response is blocked."

---
**[⬅️ Previous: Day 10 - Advanced Linux Questions](./Day-10-Advanced-Linux-Questions.md)**
