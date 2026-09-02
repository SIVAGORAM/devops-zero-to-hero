# Day 04: Advanced Pods, Labels, and Selectors (Zero to Hero)

Welcome to Day 04! Yesterday we learned how to create a basic Pod. Today, we are going to learn how to pass data into a Pod, and more importantly, how to organize and search through hundreds of Pods using the most critical organizational tool in Kubernetes: **Labels and Selectors**.

---

## 🌍 1. Passing Environment Variables to a Pod

Sometimes, your application needs secret keys, database passwords, or configuration paths to run correctly. We pass these using **Environment Variables (`env`)**.

Let's create `pod4.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-pod
spec:
  containers:
  - name: ubuntu-container
    image: ubuntu
    command: ["/bin/bash", "-c", "while true; do echo hello-devops; sleep 4; done"]
    # Here is how we pass environment variables into the container!
    env:
    - name: USER_NAME
      value: "Siva"
    - name: HOME_DIR
      value: "/home/ubuntu"
```

**How to verify it works:**
```bash
kubectl apply -f pod4.yml

# We use the 'env' Linux command inside the container to list all variables
kubectl exec env-pod -- env
```
*You will see `USER_NAME=Siva` and `HOME_DIR=/home/ubuntu` printed in your terminal!*

---

## 🏷️ 2. The Power of Labels and Selectors

**The Dynamic IP Problem:** Remember how every Pod gets a unique internal IP address? If you delete a Pod and K8s recreates it (Self-Healing), **the new Pod gets a completely different IP address!** Because IPs constantly change, we cannot rely on them to find or connect Pods together. We need a different, permanent way to identify Pods.

Imagine you are shopping on an E-Commerce store like Amazon or Flipkart. You search for "Shoes". You get 10,000 results. To find what you actually want, you use **Filters** (Brand = Puma, Color = Black).

In Kubernetes, when you run a massive enterprise cluster, you will have hundreds or thousands of Pods running simultaneously. You need a way to filter them. 

- **Labels:** These are the key-value pairs (sticky notes) you attach to a Pod when you create it (e.g., `env: dev`, `tier: frontend`).
- **Selectors:** This is the filter you type in your terminal to search for specific Labels.

### 📝 Lab 1: Creating Multiple Pods in One File
Instead of creating 3 different YAML files, you can put multiple Pod definitions into a single file by separating them with three dashes `---`.

Create `labels.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dev-pod
  labels:
    env: dev
spec:
  containers:
  - name: c1
    image: ubuntu
    command: ["/bin/bash", "-c", "sleep 3600"]
---
apiVersion: v1
kind: Pod
metadata:
  name: qa-pod
  labels:
    env: testing
spec:
  containers:
  - name: c1
    image: ubuntu
    command: ["/bin/bash", "-c", "sleep 3600"]
---
apiVersion: v1
kind: Pod
metadata:
  name: prod-pod
  labels:
    env: prod
spec:
  containers:
  - name: c1
    image: ubuntu
    command: ["/bin/bash", "-c", "sleep 3600"]
```

Apply the file to create all 3 Pods at once:
```bash
kubectl apply -f labels.yml
```

*(Note: If you edit `labels.yml` and run `apply` again, Kubernetes is smart enough to just update the existing pods rather than deleting and recreating them!)*

---

## 🔍 3. Filtering Pods using Selectors

Now that we have hundreds of pods, let's learn how to filter them using the `-l` (label) flag in our `kubectl` commands.

First, let's see all pods and their attached labels:
```bash
kubectl get pods --show-labels
```

### Type 1: Equality-Based Operators (`=` and `!=`)
These are simple exact matches.

**List only the development pods:**
```bash
kubectl get pods -l env=dev
# (Alternative syntax: kubectl get pods --selector env=dev)
```

**List all pods that are NOT development:**
```bash
kubectl get pods -l env!=dev
```

### Type 2: Set-Based Operators (`in` and `notin`)
These are advanced operators that let you search for multiple values at once.

**List pods that are either `prod` OR `testing`:**
```bash
kubectl get pods -l "env in (prod, testing)"
```

**List pods that are NOT in `production`:**
```bash
kubectl get pods -l "env notin (prod)"
```

**List pods that simply HAVE the `env` label (regardless of its value):**
```bash
kubectl get pods -l env
```
*(This is the **`exists`** operator. It just checks if the label key exists).*

**List pods that DO NOT HAVE the `env` label:**
```bash
kubectl get pods -l '!env'
```
*(This is the **`does not exist`** operator).*

---

## 🧠 4. Advanced Selectors: The Logic Gates (AND / OR)

In interviews, you might be asked to combine multiple conditions. To master this, you must understand basic Boolean Logic Gates (AND / OR) in a simple way.

### The `AND` Gate (Multiplication)
In an `AND` condition, **every single filter must be True**. If even one filter is False, the pod is rejected.
Think of it like multiplication:
- `True (1) x True (1) = True (1)`
- `True (1) x False (0) = False (0)`

*In Kubernetes, separating conditions with a comma `,` acts as an AND gate.*
```bash
# Show pods where (env == dev) AND (name == siva)
kubectl get pods -l env=dev,name=siva
```

### The `OR` Gate (Addition)
In an `OR` condition, **if ANY filter is True, the pod is accepted**. 
Think of it like addition:
- `True (1) + False (0) = True (1)`
- `False (0) + False (0) = False (0)`

*In Kubernetes, the `in` operator acts as an OR gate.*
```bash
# Show pods where (env == development) OR (env == siva)
kubectl get pods -l "env in (development, siva)"
```

### Combining AND / OR for Ultimate Filtering!
You can combine these logic gates to perform incredibly complex queries across thousands of pods:
```bash
# Show pods where (env is PROD or QA) AND (name is Siva or Ram)
kubectl get pods -l "env in (prod, testing), name in (siva, ram)"
```

---

## 🏷️ 5. Modifying Labels on the Fly (Imperative)

What if you want to add a label to a Pod *after* it has already been created, without editing the YAML file? You can do this imperatively from the terminal!

**Add a new label (`name=siva`) to the `prod-pod`:**
```bash
kubectl label pods prod-pod name=siva
```

**Overwrite an existing label (change `name=siva` to `name=ram`):**
By default, Kubernetes will throw an error if you try to change a label that already exists. You must use the `--overwrite` flag to force the change!
```bash
kubectl label pods prod-pod name=ram --overwrite
```

Verify your changes:
```bash
kubectl get pods --show-labels
```

### 🧹 Cleanup
Delete all pods in the cluster to keep your environment clean:
```bash
kubectl delete pods --all
```
