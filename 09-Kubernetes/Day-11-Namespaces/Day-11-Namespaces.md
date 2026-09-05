# Day 11: Namespaces & Resource Quotas

Welcome to Day 11! Today we are learning how to logically divide a single Kubernetes cluster into multiple virtual clusters, and how to govern those virtual clusters using Resource Quotas.

---

##  1. Introduction to Namespaces

In the real world, you do not want to spin up a brand new physical Kubernetes cluster for every single team. Instead, you create a single, massive cluster and logically divide it into "sub-clusters" called **Namespaces**.

**Why use Namespaces?**
1. **Environment Separation:** You can create separate Namespaces for `dev`, `qa`, and `prod` within the same cluster. 
2. **Team Separation:** Different teams can have their own isolated workspaces.
3. **Project/Customer Isolation:** Separate projects or even separate clients can share a cluster without their data or resources overlapping.

When you create an object inside a Namespace, you can only access it from inside that Namespace. It is isolated from the rest of the cluster!

###  Default Namespaces
If you do not specify a Namespace when creating an object, Kubernetes places it in the `default` namespace.

You can view the built-in namespaces by running:
```bash
kubectl get ns
```
You will see 4 default namespaces:
1. `default` - Where your pods go if you don't specify a namespace.
2. `kube-node-lease` - Used for node heartbeat data.
3. `kube-public` - Contains resources that should be publicly readable by all users.
4. `kube-system` - Where Kubernetes runs its own internal components (like CoreDNS or kube-proxy).

---

##  2. Creating and Using Namespaces

### Method A: Ad-Hoc Commands
You can create a namespace instantly using a single command:
```bash
kubectl create namespace dev
kubectl get ns
```

### Method B: YAML Manifest
You can also define a Namespace as a standard Kubernetes object using a YAML file.

Create `create_ns.yml`:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: qa
```
Apply it:
```bash
kubectl apply -f create_ns.yml
kubectl get ns
```
*(You will now see both the `dev` and `qa` namespaces!)*

---

##  3. Working inside Namespaces

### Deploying a Pod into a Namespace
To place a Pod into a specific namespace, you can declare it in the `metadata` of the YAML, or pass the `-n` flag via the CLI.

Create `pod.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  namespace: qa
spec:
  containers:
    - name: nginx
      image: nginx:1.14.2
      ports:
        - containerPort: 80
```
Apply it and try to find it:
```bash
# Apply the file (the -n flag here is optional since it is defined in the YAML)
kubectl apply -f pod.yml -n qa

# Try to list pods (You won't find it! It defaults to the 'default' namespace)
kubectl get pods

# Search inside the specific namespace
kubectl get pods -n qa
```

### Changing your Default Context
Typing `-n qa` on every single command gets exhausting. You can configure `kubectl` to permanently switch your terminal context to a specific namespace!

```bash
# Switch your context to the 'dev' namespace
kubectl config set-context --current --namespace=dev

# Verify which namespace your context is currently targeting
kubectl config view | grep namespace
```

---

##  4. Resource Quotas

In Day 10, we learned about Limits and Requests, which restrict the resources of a **single Pod**. 
But what if a rogue developer deploys 1,000 Pods into the `dev` namespace? It would still crash the cluster! 

To prevent this, we use a **ResourceQuota**. A ResourceQuota restricts the total, combined CPU and Memory that *all* pods inside a specific namespace are allowed to consume.

###  Lab: Triggering a Resource Quota
Let's apply a strict quota to our `dev` namespace. We will only allow a total of `100m` CPU to be requested across the entire namespace.

Create `rq.yml`:
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: myquota
  namespace: dev
spec:
  hard:
    limits.cpu: "400m"
    limits.memory: "400Mi"
    requests.cpu: "100m"
    requests.memory: "100Mi"
```
Apply it:
```bash
kubectl apply -f rq.yml
kubectl get ns
kubectl describe ns dev
```
*(You will now see the quota restrictions applied to the dev namespace!)*

### The Ultimate Test: Exceeding the Quota
Now, let's try to deploy an application that demands more resources than the Quota allows. We will deploy 6 replicas, each asking for `100m` CPU. This requires a total of `600m` CPU, which vastly exceeds our Namespace's `100m` limit!

Create `deploy.yml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mydeploy
  namespace: dev
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
          command: ["/bin/bash", "-c", "while true; do echo hello-devops; sleep 4; done"]
          resources:
            requests:
              cpu: "100m"
```
Apply the deployment and observe the results:
```bash
kubectl apply -f deploy.yml
kubectl get deploy -n dev
kubectl get pods -n dev
```

> [!IMPORTANT]
> **What Happened?**
> You will notice that Kubernetes did not spin up 6 pods. It only spun up **1 Pod**! 
> The first Pod consumed the entire `100m` CPU quota. When the ReplicaSet tried to spawn the second Pod, the Namespace's ResourceQuota blocked it.

To view the exact error blocking the remaining 5 pods, describe the ReplicaSet:
```bash
# First, get the name of your replicaset
kubectl get rs -n dev

# Then, describe it to read the Quota error logs
kubectl describe rs <name-of-your-replicaset> -n dev
```

---

## ?? 5. Zero-to-Hero Bonus: Interview Gotchas
Since you are mastering Kubernetes, here are three massive real-world concepts about Namespaces that you **must** know for production environments and senior-level interviews:

> [!CAUTION]
> **Gotcha 1: Namespaces do NOT provide Network Isolation!**
> A very common misconception is that a Pod in the dev namespace cannot talk to a Pod in the prod namespace. **This is false!** By default, any Pod in any namespace can ping and communicate with any other Pod in the cluster (they just use the DNS format <service>.<namespace>.svc.cluster.local). 
> If you want true security and network isolation between namespaces, you must implement **NetworkPolicies**!

> [!TIP]
> **Gotcha 2: Not all K8s Objects are Namespaced!**
> While Pods, Deployments, and Secrets live inside Namespaces, there are "Cluster-Scoped" objects that exist outside of all namespaces. Examples include **Nodes** and **PersistentVolumes (PVs)**. You cannot put a Node inside a dev namespace. You can see a list of non-namespaced objects by running: kubectl api-resources --namespaced=false

> [!WARNING]
> **Gotcha 3: The Danger of Deleting a Namespace**
> Be extremely careful with the command kubectl delete namespace <name>. If you delete a namespace, Kubernetes will ruthlessly and immediately terminate **every single object** (Pods, Deployments, Services, ConfigMaps, PVCs) inside of it without asking for confirmation. It is the ultimate m -rf command of Kubernetes!

