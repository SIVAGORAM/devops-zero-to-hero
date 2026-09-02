# Day 03: Kubernetes Objects, Pods, and YAML (Zero to Hero)

Before we dive into writing code, let's briefly ground ourselves with a recap of what we've learned so far. You now know that **Kubernetes (K8s)** is an orchestration tool that automates the management of **Microservices**. You know that the **Master Node** acts as the brain, commanding the **Worker Nodes** to provide **Self-Healing** and **High Availability (24/7 Uptime)**.

But how do we actually tell the Master Node what to do? The answer is **Kubernetes Objects**.

---

## 📦 1. What is a Kubernetes Object?
In Kubernetes, an "Object" is simply a record of intent. When you create an object, you are telling the Kubernetes Master Node: *"Here is my desired state. Make it happen and keep it that way."*

There are many types of objects in K8s (Deployments, Services, Secrets), but today we are focusing on the very first, and most fundamental object: **The Pod**.

### What is a Pod? (Deep Dive)
If you remember one rule from this course, remember this: **Kubernetes DOES NOT run containers directly.**

Instead, Kubernetes wraps your container inside a virtual box called a **Pod**. 
Think of it like a pea pod in nature. The green shell is the Kubernetes Pod, and the peas inside are your Docker containers.

- **The 1:1 Rule:** By default, 90% of the time, one Pod will contain exactly ONE container. 
- **Multi-Container Pods:** Can you put multiple containers in one Pod? Yes! Sometimes two containers are so tightly coupled they must share the exact same lifecycle and storage (we will do this in Lab 3).
- **Networking:** Every time a Pod is created, Kubernetes assigns it a **unique internal IP address**. If Pod A wants to talk to Pod B, it uses that IP address! *(Note: This IP is strictly for internal cluster communication, not for the outside internet).*

---

## 📜 2. Writing Kubernetes YAML Files
To create these Objects, we write configuration files using **YAML** (Yet Another Markup Language). 

YAML relies strictly on **indentation (spaces)** to define Parent and Child relationships. If your spacing is wrong, Kubernetes will throw an error!

Every single Kubernetes YAML file must contain these **4 required root fields**:

1. `apiVersion:` Which version of the Kubernetes API you are using to create this object.
2. `kind:` What type of object are you trying to create? (e.g., `Pod`, `Deployment`, `Service`).
3. `metadata:` Data that helps uniquely identify the object, like its `name` and `labels`.
4. `spec:` The "Specification". This is where you declare your desired state (e.g., what image to use, what ports to open).

---

## 💻 Lab 1: Creating Your First Pod (Nginx)

First, make sure your Minikube cluster is running:
```bash
sudo su
minikube status
minikube start --driver=docker --force
```

Create a file named `pod.yml`:
```bash
vi pod.yml
```
Paste the following code:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server-pod
  labels:
    app: web-server
    environment: production
spec:
  containers:
  - name: nginx-container
    image: nginx:latest
    ports:
    - containerPort: 80
```

### 🧠 Code Breakdown:
- `apiVersion: v1`: We are using the stable v1 API.
- `kind: Pod`: We are telling the Master Node to create a Pod object.
- `metadata.name`: We are explicitly naming this pod `web-server-pod`.
- `metadata.labels`: Labels are like sticky notes attached to the pod. Later, Kubernetes will use these labels to connect this Pod to other services.
- `spec.containers`: Notice the `-` symbol? This indicates a list! We are creating a list of containers inside this Pod.
- `- name: nginx-container`: The name of the specific container *inside* the pod.
- `image: nginx:latest`: The exact Docker image the Worker Node must download from Docker Hub.
- `containerPort: 80`: This tells Kubernetes that the container inside is listening on port 80.

### 🏃‍♂️ Running the Commands:

**1. Give the YAML to the Master Node:**
```bash
kubectl apply -f pod.yml
```
*What happens internally:* `kubectl` sends your YAML file to the Master Node's API Server. The Master checks if resources are available, and if so, commands a Worker Node to download the Nginx image and start the Pod!

**2. Check if the Pod is running:**
```bash
kubectl get pods
```

**3. Get deep details (including the unique IP Address!):**
```bash
kubectl get pods -o wide
```

**4. Delete the Pod:**
```bash
kubectl delete -f pod.yml
```
*What happens internally:* The Master Node gracefully terminates the Pod and deletes it from the cluster.

---

## 🐛 Lab 2: Debugging a Pod (Ubuntu Loop)

What happens if a Pod crashes or behaves weirdly? You need to know how to troubleshoot!

Create `pod2.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dummy-pod
spec:
  containers:
  - name: ubuntu-container
    image: ubuntu 
    # We pass a Linux command to keep the Ubuntu container running forever
    command: ["/bin/bash", "-c", "while true; do echo hello-devops; sleep 4; done"]
```

Apply it to the cluster:
```bash
kubectl apply -f pod2.yml
```

### 🧰 The 3 Ultimate Troubleshooting Commands:

**1. Find out WHY a pod failed to start:**
```bash
kubectl describe pod dummy-pod
```
*What it does:* Prints a massive wall of text detailing every single event in the Pod's lifecycle. If you typed the image name wrong, the exact error will be at the very bottom of this output!

**2. Check the Application Logs:**
```bash
kubectl logs -f dummy-pod
```
*What it does:* Streams the terminal output of the container. You will see "hello-devops" printing every 4 seconds! Press `Ctrl+C` to exit.

**3. "SSH" inside the running Pod:**
```bash
kubectl exec -it dummy-pod -- /bin/bash
```
*What it does:* Drops you directly into the terminal of the running Ubuntu container! Try typing `ps -ef` to see your running processes. Type `exit` to leave.

*(Don't forget to clean up: `kubectl delete -f pod2.yml`)*

---

## 👯 Lab 3: The Multi-Container Pod

Sometimes, you need two containers in the exact same Pod. Let's create a Pod that holds both Nginx AND Ubuntu.

Create `pod3.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-pod
spec:
  containers:
  # Container 1
  - name: c1-nginx
    image: nginx:latest
  
  # Container 2
  - name: c2-ubuntu
    image: ubuntu
    command: ["/bin/bash", "-c", "while true; do echo hello-devops; sleep 4; done"]
```

Apply it:
```bash
kubectl apply -f pod3.yml
kubectl get pods
```
Look closely at the `READY` column. It will say `2/2` instead of `1/1`. This proves there are two containers running happily inside a single Pod!

### Troubleshooting Multi-Container Pods
Because there are *two* containers in `multi-pod`, if you type `kubectl logs multi-pod`, Kubernetes will throw an error because it doesn't know *which* container's logs you want to see!

You must use the `-c` (container) flag to specify exactly which one you want:
```bash
# View logs for the Ubuntu container
kubectl logs -f multi-pod -c c2-ubuntu

# Enter the terminal of the Nginx container
kubectl exec -it multi-pod -c c1-nginx -- /bin/bash 
```

---

## 💡 Pro-Tip: The VS Code Extension
Writing YAML completely from scratch is error-prone. 

Go to the Extensions tab in VS Code and search for **"Kubernetes" by Microsoft**. Install it.
Now, when you create a `.yml` file and start typing `Pod`, the extension will automatically auto-complete the entire `apiVersion`, `kind`, `metadata`, and `spec` structure for you! This is how professionals write YAML fast.
