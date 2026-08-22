# Amazon Virtual Private Cloud (VPC) Interview Questions

Amazon VPC is the fundamental networking layer of AWS. These questions test your knowledge of subnets, route tables, network security (NACLs vs SGs), and hybrid cloud connectivity.

### 1. What is Amazon Virtual Private Cloud (VPC)?
**Answer:** Amazon VPC is a foundational AWS service that allows you to provision a logically isolated section of the AWS Cloud. It gives you complete control over your virtual networking environment, including selecting your own IP address range (CIDR block), creating subnets, and configuring route tables and network gateways.

### 2. What are the key components of Amazon VPC?
**Answer:** The primary building blocks of a VPC include:
* **Subnets:** Segments of the VPC IP range.
* **Route Tables:** Rules dictating where network traffic is directed.
* **Internet Gateway (IGW):** Allows communication between the VPC and the internet.
* **NAT Gateway:** Allows instances in private subnets to reach the internet securely.
* **Security Groups & Network ACLs:** Firewalls for instances and subnets.

### 3. How does Amazon VPC work?
**Answer:** When you create a VPC, you define a massive IP range (e.g., `10.0.0.0/16`). You then slice that large range into smaller Subnets (e.g., `10.0.1.0/24`) tied to specific Availability Zones. You deploy your resources (like EC2 or RDS) into these subnets, and use Route Tables to define exactly how traffic flows between subnets and the outside world.

### 4. What are VPC Subnets?
**Answer:** Subnets are subdivisions of a VPC's IP address range. They are strictly bound to a single Availability Zone (AZ). 
* **Public Subnets:** Have a Route Table that routes `0.0.0.0/0` traffic directly to an Internet Gateway.
* **Private Subnets:** Do not have a direct route to the Internet Gateway (they use a NAT Gateway instead, or have no internet access at all).

### 5. How can you connect your on-premises network to Amazon VPC?
**Answer:** You can connect hybrid environments using two main methods:
1. **AWS Site-to-Site VPN:** Uses IPsec tunnels over the public internet (fast to set up, cheaper, but relies on public internet latency).
2. **AWS Direct Connect (DX):** A dedicated, physical fiber-optic connection bypassing the public internet entirely (highly secure, ultra-low latency, but expensive and takes weeks to provision).

### 6. What is a VPC Peering connection?
**Answer:** VPC Peering is a direct, point-to-point network connection between two VPCs. It allows instances in VPC A to communicate with instances in VPC B using private IP addresses, as if they were on the exact same network. Traffic never traverses the public internet. Peering is non-transitive (A connected to B, and B connected to C, does not mean A is connected to C).

### 7. What is a Route Table in Amazon VPC?
**Answer:** A Route Table contains a set of rules (routes) that are used to determine where network traffic from your subnet or gateway is directed. Every subnet must be explicitly or implicitly associated with a Route Table. A route usually consists of a Destination CIDR (e.g., `0.0.0.0/0`) and a Target (e.g., `igw-12345`).

### 8. How do Security Groups work in Amazon VPC?
**Answer:** Security Groups act as a stateful virtual firewall assigned directly to the Elastic Network Interface (ENI) of an EC2 instance. Being "stateful" means if you allow an inbound request (e.g., Port 443), the return outbound traffic is automatically allowed, regardless of outbound rules. By default, they deny all inbound traffic and allow all outbound traffic.

### 9. What are Network Access Control Lists (NACLs) in Amazon VPC?
**Answer:** NACLs are stateless firewalls that operate at the **Subnet** level (surrounding the subnet, not the instance). Because they are "stateless," you must explicitly write rules for both inbound and outbound traffic. They are typically used as an added layer of defense to explicitly block malicious IP addresses from entering a subnet.

### 10. How can you ensure private communication between instances in Amazon VPC?
**Answer:** You place the instances in Private Subnets. You then configure the Security Groups of the Database instance to *only* accept inbound traffic on port 3306 from the specific Security Group ID of the Web Server instance, entirely blocking any other IP address or instance from communicating with the database.

### 11. What is the Default VPC in Amazon Web Services?
**Answer:** When you create an AWS account, AWS automatically provisions a Default VPC in every region (usually `172.31.0.0/16`). It comes pre-configured with an Internet Gateway, public subnets in every AZ, and a default security group. It is designed so new users can launch EC2 instances instantly without having to learn complex networking. (Enterprise best practice is to delete the default VPC and build custom ones).

### 12. Can you peer VPCs in different regions?
**Answer:** Yes, this is called **Inter-Region VPC Peering**. It allows you to connect a VPC in `us-east-1` directly to a VPC in `eu-west-1`. All traffic stays on the secure, private AWS global network backbone and never traverses the public internet.

### 13. How can you control Public and Private IP addresses in Amazon VPC?
**Answer:** Private IPs are assigned automatically from the Subnet's CIDR block via AWS DHCP. Public IPs can be controlled by enabling the "Auto-assign public IPv4 address" setting at the Subnet level. For a permanent public IP, you allocate an **Elastic IP (EIP)** and manually associate it with an instance or NAT Gateway.

### 14. What is a VPN connection in Amazon VPC?
**Answer:** An AWS Site-to-Site VPN creates a secure, IPsec-encrypted tunnel between a Virtual Private Gateway (VGW) attached to your AWS VPC and a Customer Gateway (CGW) device sitting in your on-premises data center, routing traffic securely over the public internet.

### 15. What is an Internet Gateway (IGW) in Amazon VPC?
**Answer:** An Internet Gateway is a horizontally scaled, redundant, and highly available VPC component that serves two purposes: it provides a target in your VPC route tables for internet-routable traffic, and it performs Network Address Translation (NAT) for instances that have been assigned public IPv4 addresses.

### 16. How can you ensure high availability in Amazon VPC?
**Answer:** VPCs are highly available by default because they span an entire region. To make your application highly available, you must create subnets in at least two different Availability Zones (e.g., `us-east-1a` and `us-east-1b`) and distribute your compute resources (EC2, RDS) across them.

### 17. How does Amazon VPC provide isolation?
**Answer:** VPCs are logically isolated on the AWS Nitro network infrastructure. Even if your VPC and a competitor's VPC share the same underlying physical hardware and the exact same CIDR block (e.g., `10.0.0.0/16`), AWS encapsulation ensures that network packets cannot bleed across boundaries.

### 18. Can you modify a VPC after creation?
**Answer:** You cannot change the primary CIDR block of a VPC after it is created. However, you can expand a VPC by adding up to four secondary IPv4 CIDR blocks. You can also freely add or remove subnets, route tables, and gateways at any time.

### 19. What is a default route in Amazon VPC?
**Answer:** In a Route Table, the local route (e.g., `10.0.0.0/16 -> local`) is created automatically and cannot be deleted; it allows all subnets in the VPC to communicate. A "Default Route" usually refers to adding `0.0.0.0/0` (which means "all other IP addresses") and pointing it to an Internet Gateway (for public subnets) or a NAT Gateway (for private subnets).

### 20. What is the purpose of an Amazon VPC Endpoint (PrivateLink)?
**Answer:** Normally, to communicate with AWS services like S3 or DynamoDB, your private EC2 instances must route traffic through a NAT Gateway and out to the public internet. A **VPC Endpoint** (Gateway or Interface type) creates a private connection inside your VPC directly to the AWS service, ensuring traffic never leaves the Amazon private network, enhancing security and reducing NAT gateway bandwidth costs.
