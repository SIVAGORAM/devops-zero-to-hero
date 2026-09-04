# Day 09: Health Checks (Probes)

Welcome to Day 09! Today we are looking at how Kubernetes ensures your application is actually running correctly.

Assume you have a Pod, and inside your Pod, your application is running inside a container. The application is supposed to be capable of serving traffic from the internet. But what if the application crashes internally, freezes, or takes 2 minutes to boot up? Kubernetes needs a way to check on it!

For this, you need to learn **Health Checks** (also called **Probes**).

> [!NOTE]  
> Health Checks are **not** a separate Kubernetes object (like a Deployment or Service). They are an *additional property* you add directly inside your Pod's YAML under a new section called `probes`.

## ⚙️ How Health Checks Work
When you define a health check, you tell Kubernetes three things:
1. What command, script, or port number to run to check the health.
2. How frequently to check (e.g., every 5 seconds).
3. How long to wait before the first check.

**The Mechanism:**
In Kubernetes, a component called **`kubelet`** is responsible for running all these scripts and commands periodically. 
- If the check returns a code of **`0`**, `kubelet` considers the application as **Healthy**.
- If the check returns a **Non-Zero** code, it considers the application as **Unhealthy**, and it will try to replace or recreate the container!

There are two main types of health checks:
1. **Liveness Probe** (Internal Checks)
2. **Readiness Probe** (External Checks)

---

## 💓 1. Liveness Probe (Internal Check)
The Liveness Probe is used to make sure the application is working fine. Its major concept is simply asking: *"Is it working or not?"* If the application is not started or has frozen, the Liveness Probe will kill the container and recreate it.

### 💻 Lab 1A: Script-Based Liveness Probe
Let's create a Pod that runs a script. We will tell the Liveness Probe to check if a specific file (`/tmp/healthy`) exists.

Create `liveness.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    test: liveness
  name: mylivenessprobe
spec:
  containers:
    - name: liveness
      image: ubuntu
      args:
        - /bin/sh
        - -c
        - touch /tmp/healthy; sleep 1000

      # Define the health check for the container
      livenessProbe:
        exec:
          # Command Kubernetes runs periodically to check container health
          command:
            - ls
            - /tmp/healthy

        # Wait 30 seconds before running the first health check
        initialDelaySeconds: 30

        # Run the health check every 5 seconds
        periodSeconds: 5

        # Allow 30 seconds for the health check to complete
        timeoutSeconds: 30
```

**Test it:**
```bash
kubectl apply -f liveness.yml
kubectl get pods
kubectl describe pod mylivenessprobe
```
*Wait 30 seconds for the container to become fully healthy.*

**Force a Failure:**
Let's intentionally delete the file that the health check is looking for! 
*(Note: Be careful to include a space `-- rm` so kubectl knows it's the remove command and not a flag!)*
```bash
kubectl exec mylivenessprobe -- rm /tmp/healthy 
```
Now, wait a few seconds and run:
```bash
kubectl describe pod mylivenessprobe
```
*You will see that the liveness probe failed, and K8s immediately started recreating the container!*

### 💻 Lab 1B: Port-Based Liveness Probe
Instead of running a bash script, we can simply check if an application (like an Apache web server) is responding on a specific port.

Create `liveness_port.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    test: liveness
  name: mylivenessprobeurl
spec:
  containers:
    - name: c00
      image: httpd
      ports:
        - containerPort: 80

      # Liveness probe checks whether the container is healthy
      livenessProbe:
        initialDelaySeconds: 5
        periodSeconds: 5
        # HTTP endpoint to check inside the container
        httpGet:
          path: /
          port: 80
```
*Notice that instead of `exec`, we are using `httpGet`. We are checking if the Apache server is responding on port 80!*

---

## 🚦 2. Readiness Probe (External Check)
The Readiness Probe checks whether the application running inside the container is **capable of serving external traffic or requests**. 

**How it works with Services:**
If a Pod is "Ready", Kubernetes will route traffic to it. If it is NOT ready, Kubernetes will stop sending external requests/traffic to that container. 

> [!WARNING]
> **Common Misconception:** It is often mistakenly believed that if a readiness probe fails, Kubernetes will recreate the pod. **This is false!** 
> - If **Liveness** fails $\rightarrow$ Kubernetes **Restarts/Recreates** the container.
> - If **Readiness** fails $\rightarrow$ Kubernetes **DOES NOT** restart the container! It simply removes the Pod from the Service so it stops receiving internet traffic until it recovers.

> [!IMPORTANT]
> **The Flow:** To be perfectly accurate: both probes actually run at the exact same time (based on their `initialDelaySeconds`). However, conceptually it is true that a Pod must pass Readiness before it serves traffic, while Liveness constantly checks if it's alive in the background!

### 💻 Lab 2: Readiness Probe
Create `readiness.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    test: readiness
  name: myreadinessprobe
spec:
  containers:
    - name: c00
      image: httpd
      ports:
        - containerPort: 80

      # Readiness probe checks whether the container is ready to receive traffic
      readinessProbe:
        initialDelaySeconds: 5
        periodSeconds: 5
        httpGet:
          path: /
          port: 80
```

**Test it:**
```bash
kubectl apply -f readiness.yml
kubectl get pods

# Note: Ensure you use the exact pod name created above
kubectl describe pod myreadinessprobe 
```
*(If it is successful, K8s routes traffic. If it fails, K8s temporarily stops sending traffic to it).*

---

## 🏗️ 3. The Ultimate Deployment
In the real world, you don't add probes to naked Pods. You add them directly into your **Deployment** object! 

Here is what a complete, production-ready Deployment looks like with both Liveness and Readiness probes configured:

Create `deploy.yml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80

          livenessProbe:
            initialDelaySeconds: 2
            periodSeconds: 5
            httpGet:
              path: /
              port: 80

          readinessProbe:
            initialDelaySeconds: 10
            httpGet:
              path: /
              port: 80
```
*Study this code deeply end-to-end to master how Deployments and Probes work together!*
