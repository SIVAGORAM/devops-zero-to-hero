# Day 12: Advanced Networking (DNS, Load Balancing & Proxies)

Today we cover the technologies that make the internet highly available and user-friendly.

---

## 1. DNS (Domain Name System)

Computers only understand IP addresses (`142.250.190.46`), but humans prefer names (`google.com`). DNS acts as the phonebook of the internet.

### How DNS Works (The Lookup)
1. You type `google.com` in your browser.
2. Your computer checks its local cache.
3. If not found, it queries a **DNS Resolver** (usually provided by your ISP or Google's `8.8.8.8`).
4. The Resolver asks the Root servers, then the TLD (`.com`) servers, and finally gets the IP from Google's authoritative Name Servers.

### Common DNS Records (DevOps Must-Know)
- **A Record:** Maps a domain name directly to an IPv4 address (e.g., `myapp.com` ➔ `1.2.3.4`).
- **CNAME (Canonical Name):** Maps a domain name to *another domain name* (e.g., `www.myapp.com` ➔ `myapp.com`). Very commonly used to point domains to AWS Load Balancers.
- **TXT Record:** Text notes attached to a domain, usually for verifying ownership or email security.

---

## 2. Load Balancers

If a website becomes popular, one server isn't enough. You need 10 servers. But users only go to one domain (`app.com`). A **Load Balancer** sits between the users and your servers.

### Benefits of Load Balancing:
1. **Distributes Traffic:** Prevents any single server from getting overwhelmed.
2. **High Availability:** If Server A crashes, the Load Balancer detects it via "Health Checks" and stops sending traffic there, routing everyone to Server B.

### Layer 4 vs Layer 7 Load Balancing
- **Layer 4 (Network Load Balancer):** Routes traffic based purely on IP and Port (Transport Layer). It is extremely fast but "dumb." It doesn't know what the traffic contains.
- **Layer 7 (Application Load Balancer):** Looks *inside* the HTTP traffic. It is "smart." It can say: "If the user goes to `app.com/images`, send them to the Image Servers. If they go to `app.com/api`, send them to the API Servers."

---

## 3. Proxies: Forward vs. Reverse

### Forward Proxy (Protecting the Client)
Sits in front of client computers (employees) and connects to the internet on their behalf. Used in corporate offices to block employees from visiting unauthorized websites.

### Reverse Proxy (Protecting the Server)
Sits in front of the web servers and accepts requests on their behalf. **Nginx** is the most famous reverse proxy.
- *Why use it?* It hides the real IP of your application server, provides SSL/TLS encryption (HTTPS), and caches static content (like images) to take the load off your main application.

---

## 4. NAT (Network Address Translation)

Remember that Private IPs (`10.0.0.5`) cannot route over the internet? What happens if your private backend database server needs to download a security update from the internet?

You use a **NAT Gateway**. 
The NAT Gateway has a Public IP. The private server sends its request to the NAT, the NAT replaces the private IP with its own Public IP, fetches the update from the internet, and sends it back to the private server. 

---

## 5. CLI Networking Troubleshooting Tools

When things break, use these commands:

1. **`ping google.com`**: Checks if a server is online by sending ICMP packets. (Note: Many cloud servers block ping by default for security).
2. **`curl -v http://localhost:8080`**: Tests if a web server is actually returning HTML on a specific port.
3. **`nslookup google.com`** or **`dig google.com`**: Verifies if DNS is correctly resolving your domain to the right IP.
4. **`telnet 10.0.0.5 3306`** or **`nc -vz 10.0.0.5 3306`**: Tests if a specific port (like MySQL) is open on a remote machine. *Crucial for debugging firewall issues!*
5. **`netstat -tulpn`**: Lists all open ports and listening services on your local server.

---

## 🎯 Day 12 Summary
You now understand how domains resolve to IPs using **DNS**, how traffic is scaled and routed using **Load Balancers and Reverse Proxies**, and how private servers reach the internet using **NAT**. You also have a toolkit of CLI commands to debug any network failure!
