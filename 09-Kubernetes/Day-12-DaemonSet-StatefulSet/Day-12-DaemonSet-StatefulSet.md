# Day 12: DaemonSets & StatefulSets

Welcome to Day 12! Today we are expanding beyond the standard Deployment object. We will learn how to deploy Pods uniquely to every single machine using **DaemonSets**, and how to manage Databases securely using **StatefulSets**.

---

## 😈 1. DaemonSets

If you have a requirement where you want to create exactly **one Pod for every one Machine (Node)** in your cluster, you must use a **DaemonSet**.

**Why do we need this?**
DaemonSets are exclusively used for cluster-wide background tasks. If you want to monitor every machine, aggregate logs from every machine, or manage network routing on every machine, you need a DaemonSet.
- *Examples:* Prometheus (Monitoring), Grafana, Fluentd (Logging).

Notice that in a DaemonSet, **we do not define `replicas`**. The number of Pods is strictly equal to the number of Worker Nodes in your cluster!

### 💻 Lab 1: Deploying a DaemonSet

Create `daemonset.yml`:
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: demodaemonset
  namespace: default
  labels:
    env: demo
spec:
  selector:
    matchLabels:
      env: demo
  template:
    metadata:
      labels:
        env: demo
    spec:
      containers:
        - name: demoset
          image: ubuntu
          command: ["/bin/bash", "-c", "while true; do echo Hello-Devops; sleep 8; done"]
```
Apply and test:
```bash
kubectl apply -f daemonset.yml
kubectl get pods -o wide
```
*(You will see exactly one Pod running on each of your Worker Nodes).*

---

## 🗄️ 2. Stateful vs Stateless Applications

Before learning about StatefulSets, you must understand the difference between Stateful and Stateless applications. If you want to deploy an application to Kubernetes, your very first question must be: *"Is this application Stateful or Stateless?"*

### Stateless Applications
- **Concept:** The application does not store data locally. All data is stored somewhere else in a remote data center or external database.
- **Examples:** Instagram frontend, Facebook web UI, general Web Servers.
- **Kubernetes Object:** If the application is Stateless, you deploy it using a standard **Deployment** and expose it using a **NodePort or LoadBalancer Service**.

### Stateful Applications
- **Concept:** Data and the application are stored together on the exact same machine locally. (If the machine dies, the data could be lost unless handled properly!)
- **Examples:** Databases (MySQL, Redis, PostgreSQL, MongoDB).
- **Kubernetes Object:** If the application is a Stateful database/backend, you must deploy it using a **StatefulSet**.

---

## 🏗️ 3. StatefulSets & Headless Services

When deploying a StatefulSet, we cannot use a standard Service (like ClusterIP) because standard services load-balance traffic randomly. When talking to a database cluster (like a Primary-Replica setup), you need to talk to a *specific* database pod. 

To achieve this, we use a **Headless Service**.

### What is a Headless Service?
A Headless Service is simply a standard Service where `clusterIP` is set to `None`. 
Instead of providing a single load-balanced IP, it creates a direct DNS record for every single individual Pod in your StatefulSet.

### 💻 Lab 2: Deploying a StatefulSet

First, create the Headless Service (`headless.yml`):
```yaml
# Headless Service
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
    - port: 80
      name: web
  clusterIP: None
  selector:
    app: nginx
```

Second, create the StatefulSet (`stateful.yml`):
*(Notice how the StatefulSet explicitly links to the `serviceName`!)*
```yaml
# Creating StatefulSet
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: webapp
spec:
  serviceName: "nginx"
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: k8s.gcr.io/nginx-slim:0.8
          ports:
            - containerPort: 80
              name: web
```

**Apply them sequentially:**
> [!IMPORTANT]
> **Observation:** Open a second terminal and run `kubectl get pods --watch`. Then, apply the YAML files. You will notice that StatefulSets create Pods strictly **one by one** (sequential creation). It will not start creating `pod-1` until `pod-0` is completely running! This is required for databases so the Primary DB can initialize before the Replica DBs connect to it.

```bash
kubectl apply -f headless.yml
kubectl get svc

kubectl apply -f stateful.yml
kubectl get sts
kubectl get pods
```

### 💻 Lab 3: Testing Stateful DNS Connectivity

StatefulSets give pods predictable, sticky names (`webapp-0`, `webapp-1`). Thanks to the Headless Service, we can reach these pods directly using the DNS format: `podname.servicename`.

Let's modify the index file inside both pods to prove we can route to them individually.
*(Note: Ensure you include the single quotes around the echo command so the redirect (`>`) happens inside the container, not on your local machine!)*

```bash
kubectl exec webapp-0 -- sh -c 'echo "this is pod-0" > /usr/share/nginx/html/index.html'
kubectl exec webapp-1 -- sh -c 'echo "this is pod-1" > /usr/share/nginx/html/index.html'
```

Now, let's curl them directly using their predictable DNS names!
```bash
# Exec into pod-0, and tell it to curl itself:
kubectl exec webapp-0 -- curl webapp-0.nginx

# Exec into pod-0, and tell it to curl pod-1:
kubectl exec webapp-0 -- curl webapp-1.nginx

# Exec into pod-1, and tell it to curl pod-0:
kubectl exec webapp-1 -- curl webapp-0.nginx
```

Congratulations! You have mastered the two most advanced deployment strategies in Kubernetes: DaemonSets and StatefulSets!

---

## ?? 4. Zero-to-Hero Bonus: Interview Gotchas
Since you are mastering Kubernetes, here are three massive real-world concepts about DaemonSets and StatefulSets that you **must** know for production environments and senior-level interviews:

> [!CAUTION]
> **Gotcha 1: StatefulSets and Storage (VolumeClaimTemplates)**
> Your notes cover the network side of StatefulSets (Headless Services), but skipped the storage side! If you mount a PVC to a standard Deployment, every single Pod shares that exact same volume. For a Database, this would cause massive data corruption! 
> StatefulSets solve this using a feature called **VolumeClaimTemplates**. When you use this, pod-0 gets its own unique olume-0, and pod-1 gets its own unique olume-1. They never share disks!

> [!TIP]
> **Gotcha 2: StatefulSet Scale-Down Safety**
> When you scale down a standard Deployment, K8s kills pods randomly. When you scale down a StatefulSet, K8s terminates them in **reverse order** (e.g., it kills pod-2, then pod-1, then pod-0). 
> Furthermore, when it kills the pod, it **DOES NOT delete the PVC data**. The data is kept safe automatically just in case you ever scale back up!

> [!IMPORTANT]
> **Gotcha 3: DaemonSets and New Nodes**
> What happens if you add a brand new Worker Node to your cluster tomorrow? You do not need to update your DaemonSet! The DaemonSet controller automatically detects the new Node and instantly schedules a new Pod onto it. It is completely hands-off!
