# Day 20: Kubeconfig & Upgrading the Kubernetes Cluster

Welcome to Day 20! Today we are mastering the two most common administrative tasks in a Kubernetes Engineer's day-to-day life: managing access to multiple clusters using the `kubeconfig` file, and safely upgrading a live cluster without bringing down customer applications.

---

## 🔑 1. Understanding Kubeconfig

### What is a Kubeconfig file?
The `kubeconfig` file is the master key to your Kubernetes cluster. It does not use simple usernames and passwords; instead, it contains cryptographic certificates and credentials required to authenticate you securely.

- **Default Location:** `~/.kube/config`
- **Default File:** The one created by `kubeadm` is the Administrator file.

### Inside the Kubeconfig File
Every time you run a command like `kubectl get pods`, `kubectl` secretly opens your kubeconfig file to figure out who you are and where the cluster is. A Kubeconfig is divided into 3 main sections:

1. **`users:`** Who are you? (Contains your client certificates or AWS IAM tokens).
2. **`clusters:`** Where is the cluster? (Contains the API Server IP address and the cluster's CA certificate).
3. **`contexts:`** The Glue! A context binds a **User** to a **Cluster** and sets a default **Namespace** (e.g., "Log me into the Production Cluster, as Siva, in the QA Namespace").

*(Yes, you can have multiple kubeconfig files, or one massive file with 10 different clusters inside it!)*

### Switching Between Clusters (Contexts)
If you manage Dev, QA, and Prod clusters, you don't want to type long commands every time. You use Contexts!

```bash
# 1. See all the contexts (clusters) you have access to:
kubectl config get-contexts

# 2. See which context you are currently logged into:
kubectl config current-context

# 3. Switch your CLI instantly to a different cluster:
kubectl config use-context <context-name>
```

### Passing Custom Kubeconfig Files
If someone sends you a temporary kubeconfig file (e.g., `siva-temp.yaml`), you don't have to overwrite your main `~/.kube/config` file.

**Method 1: Pass it directly in the command (Tedious)**
```bash
kubectl get pods --kubeconfig=/path/to/siva-temp.yaml
```

**Method 2: Export it as an Environment Variable (Pro-Tip)**
```bash
export KUBECONFIG=/path/to/siva-temp.yaml
kubectl get pods  # It automatically uses the new file!
```

---

## ⚙️ 2. Upgrading a Kubernetes Cluster (Zero Downtime)

Upgrading a cluster is dangerous. If you do it wrong, you destroy the cluster. In the real world (and in interviews), you upgrade the Master Nodes first, and then the Worker Nodes.

### Step 1: The Golden Rule - Back up ETCD!
Before you touch *anything*, you must back up the ETCD database. If the upgrade corrupts your cluster, this backup is your only lifeline to restore it.

*(As requested, here is the exact real-world command to back up ETCD!)*
```bash
# You must use ETCD V3 API to take a snapshot backup
ETCDCTL_API=3 etcdctl snapshot save /tmp/etcd-backup.db \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

### Step 2: Upgrading the Master Node (Control Plane)
You upgrade the master components one by one. While the Master Node is being upgraded, the API server will go down temporarily. 
- **What happens to the apps?** Nothing! The pods on your Worker Nodes keep running perfectly and serving customers.
- **What is the catch?** You cannot create *new* pods or edit deployments while the Master is down.

**The Version Skew Rule (Crucial for Interviews):**
The `kube-apiserver` must ALWAYS be the highest version. 
If your API Server is on `v1.30`, your Controller Manager, Scheduler, and Kubelet can be on `v1.30`, `v1.29`, or `v1.28`. They can NEVER be higher than the API server (e.g., they cannot be on `v1.31`).

### Step 3: Upgrading the Worker Nodes
You never upgrade all Worker Nodes at the same time, because that would kill all customer applications. You upgrade them one by one using a process called Cordon and Drain.

| Command | What it does | Real-World Impact |
| :--- | :--- | :--- |
| **`kubectl cordon <node>`** | Marks the node as "Unschedulable". | Existing pods stay running, but the Scheduler will not place any *new* pods on this node. |
| **`kubectl drain <node>`** | Gracefully evicts all pods from the node. | Kills the pods on this machine, but forces the ReplicaSet to immediately recreate them on other healthy worker nodes! |
| **(Upgrade OS/Kubelet)** | Run your `apt-get upgrade` commands. | The machine is safely updated while empty. |
| **`kubectl uncordon <node>`** | Marks the node as "Schedulable" again. | The node rejoins the cluster and can accept pods again! |

---

## 🏆 3. Summary & What's Next?

If you have mastered Days 1 through 20, you are officially in the top percentage of Kubernetes engineers. You understand Pods, Deployments, Services, RBAC, Architecture, Kubeadm Setup, and Cluster Upgrades. 

If you want to push yourself even further into advanced territory, here are the topics you should research next:
- **Service Accounts:** Like IAM Roles for Pods (instead of humans).
- **CoreDNS:** How Pods discover each other by name instead of IP.
- **Network Policies:** K8s Firewalls (blocking Pod A from talking to Pod B).
- **Service Mesh (Istio):** Advanced traffic routing and mTLS encryption.
- **CRDs (Custom Resource Definitions):** Extending K8s to understand custom objects.
- **Helm:** The Package Manager for Kubernetes (like `apt` or `yum`, but for deploying huge K8s apps).

---

## 🧠 4. Zero-to-Hero Bonus: Interview Gotchas

> [!CAUTION]
> **Gotcha 1: "What happens to the cluster if the Master Node goes offline during an upgrade?"**
> Tell the interviewer: *"The existing worker nodes and pods will continue to serve customer traffic completely uninterrupted. The data plane is unaffected. However, the control plane is frozen: we cannot deploy new applications, scale up, or automatically recover if a worker node crashes until the Master Node comes back online."*

> [!TIP]
> **Gotcha 2: "Can I just restart the worker node to upgrade it?"**
> Tell the interviewer: *"Absolutely not. If you restart a node abruptly, you cause downtime. You must always run `kubectl drain <node>` first. This gracefully forces the ReplicaSets to shift all workloads to other healthy nodes before the machine shuts down."*

> [!IMPORTANT]
> **Gotcha 3: "What is the difference between Cordon and Drain?"**
> This is a classic interview question! 
> - **Cordon** just puts a "Do Not Enter" sign on the node. No *new* pods can enter, but existing pods stay exactly where they are.
> - **Drain** puts up the "Do Not Enter" sign AND kicks everybody out (gracefully moving them to other nodes).
