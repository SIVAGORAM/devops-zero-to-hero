# Day 06: Deployments (Updates and Rollbacks)

Welcome to Day 06! Today we are looking at the absolute most important object in Kubernetes: **The Deployment**.

## 🔄 The Big Picture: CI/CD Pipeline
Before diving into Deployments, let's look at the complete flow of how an application goes from a developer's laptop to running in Kubernetes (Version 1):
`Developer -> writes Code -> pushes to GitHub -> CI/CD Build -> Docker Image -> pushed to Docker Hub -> Kubernetes pulls Image -> runs in Pods`

When Version 2 is released, this exact same pipeline runs again! But how does Kubernetes safely replace the V1 Pods with the V2 Pods? That is where Deployments come in.

## 🏗️ The Evolution of Kubernetes Objects
To understand *why* Deployments exist, we have to look at the problems we solved step-by-step over the last few days:

1. **Pods:** We started with naked Pods. 
   - *The Problem:* They cannot scale, and if they die, they don't come back.
2. **ReplicaSet:** We wrapped Pods in a ReplicaSet.
   - *The Problem Solved:* We gained Scaling and Self-Healing!
   - *The NEW Problem:* What happens when developers release Version 2 of the code? A ReplicaSet forces you to delete everything to update it, causing downtime for your customers.
3. **Deployment:** We wrap the ReplicaSet inside a Deployment object.
   - *The Problem Solved:* We gain **Rolling Updates** (updating without downtime) and **Rollbacks** (an undo button if V2 is broken!).

> [!TIP]
> **The Hierarchy of K8s:**
> `Deployment` $\rightarrow$ automatically creates $\rightarrow$ `ReplicaSet` $\rightarrow$ automatically creates $\rightarrow$ `Pods` $\rightarrow$ runs your `Containers`.

---

## 📜 1. Creating a Deployment (Version 1)

How do you write a Deployment YAML file? It is incredibly easy. 
**A Deployment uses the exact same code structure as a ReplicaSet.** You literally just change the word `kind: ReplicaSet` to `kind: Deployment`.

Let's deploy Version 1 of our application!

Create a file named `deploy.yml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mydeploy
  labels:
    app: myapp
    key: value
spec:
  replicas: 6
  selector:
    matchLabels:
      env: dev
  template:
    metadata:
      labels:
        env: dev
    spec:
      containers:
        - name: c1
          image: ubuntu
          command: ["/bin/bash", "-c", "while true; do echo 'hello-devops'; sleep 4; done"]
```

### 💻 Lab 1: Deploying Version 1
First, connect to your instance (using MobaXterm or your terminal), start your cluster, and verify we have no deployments running yet:
```bash
sudo su
minikube start --driver=docker --force
kubectl get deployment  # Proves the cluster is currently empty
```

Now, apply the file:
```bash
kubectl apply -f deploy.yml
```

Let's verify the deployment step-by-step, exactly as K8s builds it:
```bash
kubectl get deploy
kubectl get rs
kubectl get pods
```

To see everything the deployment is doing under the hood, use the describe command:
```bash
kubectl describe deploy mydeploy
```

Let's check the pods one more time, and then view the logs of your running V1 pod:
```bash
kubectl get pods
kubectl logs -f <pod-name-here>
# You will see 'hello-devops' printing to the screen.
```

---

## 🚀 2. Rolling Updates (Releasing Version 2)

Your development team just finished Version 2! They want the app to say "Welcome to DevOps K8s" instead of "hello-devops". 

Instead of deleting everything (which would cause an outage for your customers), we will perform a **Rolling Update**. A Rolling Update gracefully deletes one old pod and replaces it with a new pod, one by one, until the entire cluster is upgraded with zero downtime!

### 💻 Lab 2: Upgrading to Version 2
Open `deploy.yml` and modify the container command to represent Version 2 ("Welcome to DevOps K8s" instead of "hello-devops"):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mydeploy
  labels:
    app: myapp
    key: value
spec:
  replicas: 6
  selector:
    matchLabels:
      env: dev
  template:
    metadata:
      labels:
        env: dev
    spec:
      containers:
        - name: c1
          image: ubuntu
          command: ["/bin/bash", "-c", "while true; do echo 'Welcome to DevOps K8s'; sleep 4; done"]
```

Apply the changes:
```bash
kubectl apply -f deploy.yml
```

**Watch the magic happen:**
Run this immediately:
```bash
kubectl get pods
```
*You will see old pods transitioning to `Terminating` while new pods transition to `ContainerCreating`. It handles the transition perfectly!*

Now run this:
```bash
kubectl get rs
```
*Notice there are now **TWO** ReplicaSets!*
- The **New ReplicaSet** has 6 pods (This is Version 2 running).
- The **Old ReplicaSet** has 0 pods (This is Version 1. The Deployment didn't delete it; it kept it empty as a **Backup**!).

Check the logs of a new pod to prove V2 is live:
```bash
kubectl logs -f <new-pod-name>
# You will see 'Welcome to DevOps K8s'!
```

---

## ⏪ 3. The "Undo" Button (Rollbacks)

Imagine disaster strikes. Customers are complaining that Version 2 is completely broken. Your boss is screaming. You need to revert back to Version 1 immediately!

Because the Deployment object kept the old ReplicaSet as a backup, reverting is as easy as typing one command.

### 💻 Lab 3: Rolling Back
First, check the status of your rollout to ensure nothing is currently updating:
```bash
kubectl rollout status deployment/mydeploy
```

Next, view the history of all versions K8s has saved for you:
```bash
kubectl rollout history deployment/mydeploy
```
*You will see `REVISION 1` (Version 1) and `REVISION 2` (Version 2).*

**Execute the Rollback!** Let's go back to Revision 1:
```bash
kubectl rollout undo deployment/mydeploy --to-revision=1
```

*What happens internally:* 
Kubernetes brings down the 6 pods in the V2 ReplicaSet, and spins up 6 pods in the V1 ReplicaSet! 
If you run `kubectl rollout history` again, you will see a `REVISION 3`. Revision 3 is just a copy of Revision 1, proving you rolled back successfully.

Let's verify this by checking the history and the logs, just like we did before:
```bash
kubectl rollout history deployment/mydeploy
kubectl get pods
kubectl logs -f <new-v1-pod-name>
# You will see 'hello-devops' is back!
```

---

### ⏭️ What's Next?
A Rolling Update is just one way to upgrade an application. Tomorrow, we will look at the **4 Major Deployment Strategies**:
1. Recreate (Delete all, then create all - Causes Downtime)
2. Rolling Update (One by one - Zero Downtime)
3. Blue-Green Strategy (Running two identical environments and switching traffic)
4. Canary Strategy (Testing V2 on 10% of users before fully releasing)
