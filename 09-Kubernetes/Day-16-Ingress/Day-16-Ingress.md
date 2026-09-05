# Day 16: Ingress & Ingress Controllers

Welcome to Day 16! So far, we have been using `NodePort` or `LoadBalancer` Services to expose our applications to the outside world. But in a modern microservices architecture, this approach creates a massive, expensive problem. 

Today, we solve that problem using **Ingress**.

---

##  1. The School Analogy

To understand Ingress, imagine your Kubernetes Cluster is a **School**.
- **The Classrooms:** The individual applications running inside (Pods).
- **The Security Guard:** The **Ingress Controller**. They stand at the main gate of the school.
- **The Rulebook:** The **Ingress Resource**. It tells the security guard exactly where to send visitors.

If a parent wants to visit the Staff Room, they walk up to the Security Guard (Ingress Controller) at the main gate. The guard checks their rulebook (Ingress Resource). If the parent has permission, the guard escorts them directly to the Staff Room.

In Kubernetes: The user hits a single DNS name. The Ingress Controller catches the request, reads the Ingress Resource rules, and routes the user to the correct internal `ClusterIP` Service based on the URL path!

---

##  2. Why use Ingress? (The Microservices Problem)

Imagine you are building Flipkart. Flipkart is not one massive application; it is broken down into dozens of microservices:
- A service for the Homepage (`/`)
- A service for Mens Clothing (`/men`)
- A service for Womens Clothing (`/women`)
- A service for Mobiles (`/mobiles`)

If we used the old method, we would have to create a separate `type: LoadBalancer` Service for *every single one* of these microservices. 
On AWS, every LoadBalancer costs money. If you have 50 microservices, **you will be paying AWS for 50 separate physical Load Balancers!**

**The Solution:**
Instead, we create **ONE** AWS LoadBalancer (the Ingress Controller). We expose all of our internal microservices using free, internal `ClusterIP` services. The Ingress Controller acts as a smart router, taking all the incoming traffic from the single LoadBalancer and routing it to the correct internal ClusterIP based on the URL!

---

##  3. Real-World Lab: Path-Based Routing

Let's simulate our E-Commerce website. We will create a namespace, deploy our app, expose it internally, and then use Ingress to route traffic based on URL paths (`/men` and `/women`).

### Step 1: Create the Namespace
```bash
kubectl create namespace ecommerce
```

### Step 2: Deploy the Application
Create `deployment.yml`:
*(Notice we are deploying into the `ecommerce` namespace!)*
```bash
kubectl apply -f deployment.yml
```

### Step 3: Expose it Internally (ClusterIP)
Create `service-clusterip.yml`. This makes the application reachable inside the cluster, but perfectly hidden from the internet.
```bash
kubectl apply -f service-clusterip.yml
```

### Step 4: Install the Security Guard (Ingress Controller)
By default, Kubernetes does not come with an Ingress Controller installed. You have to install a third-party one. The most popular in the world is the **NGINX Ingress Controller**.

Run this command to install the Controller into your cluster. (Under the hood, this will automatically talk to AWS and provision your single, shared LoadBalancer!):
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# Wait a minute, then get the AWS LoadBalancer DNS name it generated:
kubectl get svc -n ingress-nginx
```

### Step 5: Give the Guard the Rules (Ingress Resource)
Create `ingress.yml`. 
*(Note: In a true microservices setup, `/men` and `/women` would route to completely different backend Services. For this lab, we are routing them all to the same `myapp-service` to demonstrate how path-based routing works).*

**Crucial Step:** You must open `ingress.yml` and replace the `host:` URL with the actual AWS LoadBalancer DNS name you generated in Step 4!

```bash
kubectl apply -f ingress.yml
```

###  Understanding the Ingress YAML Code
In interviews, you might be asked to write or explain an Ingress YAML file. It looks huge, but it's actually incredibly simple once you break it down:
- **`annotations` (rewrite-target: /):** This is a magic trick for the NGINX controller. It tells NGINX to strip away the `/men` or `/women` from the URL before sending it to the backend pod, so your pod just sees a normal request to its root `/`.
- **`host:`** This is the domain name the user types into their browser (in this lab, our AWS LoadBalancer URL).
- **`path: /men` & `pathType: Prefix`:** This means "if the URL starts with `/men` (like `/men/shirts` or `/men/shoes`), catch it."
- **`backend:`** This tells the controller exactly where to send the caught traffic (in our case, to port 80 of the internal `myapp-service`).

You can now open a browser, paste your LoadBalancer URL, and try appending `/men` or `/women` to the end of it! The NGINX Ingress Controller is handling the traffic routing flawlessly.

---

##  4. Zero-to-Hero Bonus: Interview Deep Dive

If you are interviewing for a Senior DevOps role, you must be able to speak deeply about the underlying architecture of Ingress.

> [!TIP]
> **What is a Reverse Proxy?**
> An Ingress Controller (like NGINX) is fundamentally a **Reverse Proxy**. 
> A standard proxy protects *clients* (like a VPN hiding your laptop's IP from the internet). A **Reverse Proxy** protects *servers* (it sits in front of your internal web servers, intercepts all incoming internet traffic, and decides which internal server gets the request). 

> [!CAUTION]
> **Advantages of Ingress (Beyond just saving money)**
> Saving money on LoadBalancers is great, but Ingress provides massive enterprise benefits:
> 1. **SSL/TLS Termination:** Instead of configuring SSL certificates on 50 different microservices, you configure your SSL certificate *once* on the Ingress Controller. It decrypts the HTTPS traffic at the main gate, and sends unencrypted HTTP traffic to your internal Pods to save them CPU power!
> 2. **Advanced Traffic Management:** You can set rate-limiting (preventing DDoS attacks) or IP whitelisting directly at the Ingress level.
> 3. **Sticky Sessions:** Ensuring a specific user's requests always get routed to the exact same Pod (crucial for older Stateful applications).

> [!IMPORTANT]
> **4. Host-Based Routing vs Path-Based Routing**
> In the lab above, we used **Path-Based Routing** (lipkart.com/men). However, Ingress is equally famous for **Host-Based Routing** (Subdomains). 
> For example, you can write an Ingress rule that says: If the user visits pi.flipkart.com, route them to the Backend API Service. If they visit shop.flipkart.com, route them to the Frontend Service. You can run 50 different websites on a single AWS LoadBalancer just by using different host: definitions in your Ingress YAML!

> [!CAUTION]
> **5. Multiple Security Guards (IngressClass)**
> What if your school is so big it needs two security guards? One for the front gate (Public Internet) and one for the back gate (Internal Employee VPN). 
> In enterprise environments, you often run *multiple* Ingress Controllers (e.g., an external NGINX controller, and an internal NGINX controller). When you create your Ingress YAML, how does Kubernetes know *which* controller should read it? 
> You use a field called **ingressClassName**. This tells Kubernetes exactly which controller should apply your rules!

> [!NOTE]
> **6. The Future: Kubernetes Gateway API**
> If you want to blow away an interviewer, mention the **Gateway API**. 
> While Ingress is the current standard, Kubernetes is actively replacing it with the new Gateway API. Why? Because Ingress puts all the rules (Hosts, Paths, TLS) into one massive file, which creates conflicts between Developers (who want to manage paths) and Admins (who want to manage SSL/Ports). The Gateway API separates these responsibilities, providing the ultimate modern traffic routing solution!

