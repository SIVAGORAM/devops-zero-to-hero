# AWS Transit Gateway & Advanced Networking Interview Questions

As cloud footprints grow, managing point-to-point VPC peering becomes an administrative nightmare. These questions test your knowledge of Hub-and-Spoke networking, hybrid connectivity, and global routing.

### 1. What is AWS Transit Gateway?
**Answer:** AWS Transit Gateway (TGW) is a highly available, scalable regional network transit hub. It allows you to connect thousands of Amazon VPCs and your on-premises data centers through a single, central gateway, entirely eliminating the need for complex point-to-point peering architectures.

### 2. What problem does Transit Gateway solve compared to VPC Peering?
**Answer:** VPC Peering is non-transitive. If you have 100 VPCs that all need to talk to each other, you have to create and manage 4,950 individual peering connections (a full mesh). With Transit Gateway, you use a "Hub and Spoke" model. You attach all 100 VPCs to the single Transit Gateway, requiring only 100 connections.

### 3. Is AWS Transit Gateway a regional or global service?
**Answer:** Transit Gateway is a **regional** service. All VPCs attached to a specific Transit Gateway must reside in the same AWS Region. 

### 4. How do you connect VPCs in different regions using Transit Gateway?
**Answer:** You create a Transit Gateway in Region A and another Transit Gateway in Region B. You then create a **Transit Gateway Peering Connection** between the two gateways. Traffic routes securely across the AWS global private network backbone.

### 5. What are Transit Gateway Attachments?
**Answer:** To connect a resource to a TGW, you create an attachment. Supported attachments include:
* VPCs
* AWS Site-to-Site VPN connections
* AWS Direct Connect gateways
* Transit Gateway Peering connections (cross-region)
* Connect attachments (SD-WAN appliances using GRE tunnels)

### 6. How does routing work in an AWS Transit Gateway?
**Answer:** A Transit Gateway contains one or more **Transit Gateway Route Tables**. When a packet arrives from an attachment (like a VPC), the TGW evaluates the route table associated with that attachment to determine which downstream attachment to send the packet to.

### 7. How can you isolate environments using Transit Gateway Route Tables?
**Answer:** By using multiple route tables, you can create isolated routing domains (VRFs). For example, you can create a "Dev Route Table" and a "Prod Route Table". Dev VPCs can only talk to other Dev VPCs, and Prod VPCs can only talk to Prod VPCs, but both might have a route to a "Shared Services Route Table" to access a central logging server.

### 8. What is the difference between a Transit Gateway and a Transit VPC?
**Answer:** A "Transit VPC" was an old, legacy workaround where engineers installed third-party router software (like Cisco CSR) on EC2 instances to act as a hub. It was expensive to license, hard to manage, and limited by EC2 bandwidth. AWS Transit Gateway is a fully managed, native cloud service that replaces this pattern.

### 9. What is ECMP (Equal-Cost Multi-Path) routing in Transit Gateway?
**Answer:** A standard AWS Site-to-Site VPN tunnel is limited to 1.25 Gbps. If your corporate data center needs 5 Gbps of bandwidth, you can create multiple VPN tunnels to the Transit Gateway and enable ECMP. The TGW will balance the traffic across all the active tunnels, aggregating the bandwidth. (Standard Virtual Private Gateways do not support ECMP).

### 10. How do you integrate AWS Direct Connect with Transit Gateway?
**Answer:** You cannot attach a Direct Connect Dedicated Connection directly to a TGW. You must first create an **AWS Direct Connect Gateway**, associate your Direct Connect connections to it, and then attach the Direct Connect Gateway to the Transit Gateway. This allows your on-premise data center to reach thousands of VPCs.

### 11. Can a VPC have overlapping CIDR blocks if they are connected to a Transit Gateway?
**Answer:** No. Just like VPC Peering, if VPC A and VPC B have the exact same IP address range (e.g., `10.0.0.0/16`), routing is impossible because the Transit Gateway will not know which VPC the IP belongs to. IP addresses must be globally unique across your network.

### 12. How does Transit Gateway handle Multicast traffic?
**Answer:** AWS Transit Gateway is one of the only AWS networking services that natively supports Multicast routing. You can configure a Multicast Domain in the TGW to allow one source (like a financial market data feed) to simultaneously stream data to thousands of subscriber EC2 instances.

### 13. What is the Transit Gateway Network Manager?
**Answer:** Network Manager provides a centralized, global dashboard to visualize and monitor your entire AWS global network. It builds topological graphs, geographical maps, and monitors the health and performance of all your Transit Gateways, VPNs, and Direct Connects worldwide.

### 14. What is Appliance Mode in Transit Gateway?
**Answer:** If you place a third-party virtual firewall (like a Palo Alto) in a centralized "Security VPC", traffic from VPC A to VPC B is routed through the firewall. Because firewalls are stateful, symmetric routing is required. Enabling **Appliance Mode** on the Security VPC attachment guarantees that the Transit Gateway sends the return traffic back to the exact same firewall instance that inspected the initial request, preventing dropped packets.

### 15. How do you configure VPC Route Tables to use a Transit Gateway?
**Answer:** Inside the individual VPC's Route Table, you add a route where the Destination is the CIDR block of the target network (e.g., `10.5.0.0/16`) and the Target is the Transit Gateway ID (e.g., `tgw-12345`).

### 16. What is the maximum bandwidth of a VPC attachment to a Transit Gateway?
**Answer:** A single VPC attachment can burst up to **50 Gbps** of bandwidth.

### 17. How do you share a Transit Gateway across multiple AWS Accounts?
**Answer:** The Networking Account creates the Transit Gateway. They then use **AWS Resource Access Manager (RAM)** to share the TGW with other accounts or an entire AWS Organization. The other accounts can then attach their local VPCs directly to the shared central Transit Gateway.

### 18. What is a Blackhole Route in a Transit Gateway?
**Answer:** A Blackhole route is an explicit rule in a TGW route table used to drop traffic. If you want to absolutely ensure that the "Dev VPC" can never reach the "Finance VPC", you can create a route for the Finance CIDR block and set the target to "Blackhole." The TGW will instantly discard those packets.

### 19. How do you secure data in transit across a Transit Gateway?
**Answer:** Traffic routed between VPCs through a Transit Gateway stays on the AWS global private network. Furthermore, traffic between EC2 instances (on modern Nitro instance types) is automatically encrypted at the hardware level before it leaves the host, ensuring security without overhead.

### 20. What is the cost model for AWS Transit Gateway?
**Answer:** You pay an hourly charge for every attachment (VPC, VPN, DX) connected to the Transit Gateway. You also pay a data processing fee per Gigabyte for all traffic that flows through the Transit Gateway.
