# Day 07: Services (Networking in Kubernetes)

Welcome to Day 07! We have mastered Deployments, ReplicaSets, and Pods. But there is a massive problem we haven't solved yet: **How do we actually access our application?**

## 🚨 The Networking Problem
Every Pod in Kubernetes is automatically assigned a unique IP address. However, Pods are **ephemeral** (temporary). They can be created and deleted at any time. 

If a Pod crashes and the ReplicaSet recreates it, the new Pod gets a completely different IP address! 
- *Problem 1:* How can you remember hundreds of constantly changing IP addresses? (In realtime we have 1000's of IPs!)
- *Problem 2:* How can a Frontend application reliably connect to a Backend database if the database's IP address changes every day?

## 🛡️ The Solution: The Service Object
To solve this, Kubernetes introduces the **Service Object**. 

A Service sits on top of your Deployment. It provides a single, static **Virtual IP (VIP)** (often referred to as an Elastic IP in cloud environments) that never changes, even if the Pods underneath it die and are recreated. You no longer need to remember Pod IPs; you only talk to the Service!

There are 5 types of Services in K8s, but today we will master the 3 most important ones:
1. **ClusterIP**
2. **NodePort**
3. **LoadBalancer**
4. **Headless** *(Advanced, we will cover later)*
5. **Ingress** *(Advanced, we will cover later)*

---

## 🏗️ Step 1: Deploying the Application
Before we can create a Service, we need an application for the Service to point to! Let's create a standard Nginx deployment.

Create `pods.yml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-page
spec:
  replicas: 4
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: web-page
          image: nginx:latest
          ports:
            - containerPort: 80
```

Apply it to your cluster:
```bash
kubectl apply -f pods.yml
kubectl get deploy
kubectl get pods
```

---

## 🔒 Type 1: ClusterIP
**What is it?** This is the default Service type. It creates a Virtual IP that is **strictly internal**. 
**Why use it?** You use this when you want Pods to talk to other Pods *inside* the cluster securely (e.g., your Frontend Pod talking to your Backend Pod). Nobody from the outside internet can access a ClusterIP.

Create `clusterip.yml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
```

> [!IMPORTANT]  
> **The Two Golden Rules of Services:**
> 1. **Labels MUST Match:** Look at `selector: app: frontend`. The Service uses Labels and Selectors to route traffic. If the Service selector does not perfectly match the labels on your Pods, the traffic will go nowhere!
> 2. **Ports MUST Match:** Look at `targetPort: 80`. This must exactly match the `containerPort: 80` that your application is exposing inside the Pod!

Apply and test it:
```bash
kubectl apply -f clusterip.yml
kubectl get svc   # 'svc' stands for Services
```
*You will see a CLUSTER-IP address generated. Because it is internal, you can only test it by logging into a pod or using a temporary curl pod from inside the cluster:*
```bash
# Example internal test
curl <your-cluster-ip>
```

---

## 🚪 Type 2: NodePort
**What is it?** What if you want to access your application from your web browser, outside of the cluster? A NodePort opens a specific port (between **30000 - 32767**) on every single Slave/Worker Node in your cluster!
**Why use it?** It is mostly used for internal organization testing or debugging. It is not recommended for production because giving users IP addresses with weird port numbers (like `http://192.168.1.5:31245`) is unprofessional.

*Under the hood: A NodePort Service automatically creates a ClusterIP for internal routing, and uses a component called `kube-proxy` to handle the networking!*

*(Note: You can simply modify your existing `clusterip.yml` file by changing the type to `NodePort`, or use the dedicated file below!)*

Create `service-nodeport.yml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

Apply and test it:
```bash
kubectl apply -f service-nodeport.yml
kubectl get svc
```
*Look at the PORT(S) column. You will see something like `80:31456/TCP`. You can now open your web browser and go to `<Any-Worker-Node-IP>:31456` to see your Nginx page!*

---

## 🌐 Type 3: LoadBalancer
**What is it?** This is the industry standard for production. When you create this Service in a cloud environment (like AWS EKS), it automatically talks to the cloud provider and provisions a real, physical Load Balancer (like an AWS Network Load Balancer).
**Why use it?** You use this when you want to expose your application to the public internet using a clean, professional URL.

Create `service-loadbalancer.yml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

Apply it:
```bash
kubectl apply -f service-loadbalancer.yml
kubectl get svc
```
*Note: If you run this on a local Minikube cluster, the EXTERNAL-IP will stay in `<pending>` forever, because Minikube cannot magically spawn a physical AWS Load Balancer! You must practice LoadBalancers by creating your own EKS cluster on AWS.*

---

### 🏋️ Practice Exercise
To master this, try recreating the flow from scratch yourself:
```bash
vi deploy2.yml      # Create a new deployment
vi service.yml      # Create a service for it
kubectl apply -f deploy2.yml
kubectl get svc     # Verify the service attached properly
```

---

### 💡 Summary Cheat Sheet
- **ClusterIP:** Inside the cluster only (Frontend $\rightarrow$ Backend).
- **NodePort:** Access the application **inside your organization** (Internal QA Testing on weird ports).
- **LoadBalancer:** Expose your application **outside your organization** to the public internet using a clean URL.
