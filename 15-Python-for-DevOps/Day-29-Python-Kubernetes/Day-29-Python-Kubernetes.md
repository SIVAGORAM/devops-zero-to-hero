# Python Day 29: Python + Kubernetes

Welcome to **Day 29**! 
Kubernetes is the industry standard for Container Orchestration. While developers use `kubectl` to manage their apps, DevOps engineers use the **Kubernetes Python Client** to automate the cluster, build custom auto-scalers, and create self-healing infrastructure.

---

## 1. Connecting to the Cluster
There are two ways to authenticate Python with a Kubernetes cluster.

1. **Running locally on your laptop (DevOps Scripting):**
   ```python
   from kubernetes import config
   config.load_kube_config() # Reads ~/.kube/config
   ```

2. **Running *inside* a Kubernetes Pod (Automated Controllers):**
   ```python
   from kubernetes import config
   config.load_incluster_config() # Uses the Pod's ServiceAccount token
   ```

---

## 2. API Groups: CoreV1 vs AppsV1
Kubernetes has hundreds of resources. The Python client splits them into different API objects.
- `client.CoreV1Api()`: Used for core resources (Pods, Services, ConfigMaps, Secrets, Namespaces).
- `client.AppsV1Api()`: Used for workloads (Deployments, StatefulSets, DaemonSets, ReplicaSets).

---

## 3. DevOps Automation: Cluster Health Checking
A common DevOps task is scanning all namespaces to find Pods that have crashed or are stuck in a `Pending` state.

```python
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()

print("Scanning for broken Pods...")
# list_pod_for_all_namespaces is perfect for cluster-wide sweeps
pods = v1.list_pod_for_all_namespaces()

for pod in pods.items:
    if pod.status.phase not in ["Running", "Succeeded"]:
        print(f"ALERT: {pod.metadata.namespace}/{pod.metadata.name} is in state: {pod.status.phase}")
```

---

## 4. DevOps Automation: Auto-Scaling Deployments
You don't need to type `kubectl scale` manually. Python can instantly scale up deployments if it detects heavy traffic.

```python
from kubernetes import client, config

config.load_kube_config()
apps_v1 = client.AppsV1Api()

deployment_name = "nginx-deployment"
namespace = "default"

# 1. Fetch the Deployment object
deployment = apps_v1.read_namespaced_deployment(name=deployment_name, namespace=namespace)

# 2. Modify the desired replicas
print(f"Current Replicas: {deployment.spec.replicas}. Scaling to 5...")
deployment.spec.replicas = 5

# 3. Patch the Deployment in the API Server
apps_v1.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)
print("Scale command issued successfully!")
```

---

## 5. DevOps Automation: Log Analysis
If an alert fires, your Python script can automatically fetch the logs of the broken pod and search for `ERROR` strings, attaching them to a Jira ticket or Slack message!

```python
from kubernetes import client, config
from kubernetes.client.rest import ApiException

config.load_kube_config()
v1 = client.CoreV1Api()

try:
    logs = v1.read_namespaced_pod_log(name="broken-pod", namespace="default")
    for line in logs.splitlines():
        if "ERROR" in line:
            print(f"Found Error: {line}")
except ApiException as e:
    print(f"K8s API Error: {e.reason} ({e.status})")
```

---

## 6. Advanced DevOps: Restarting a Deployment (Rolling Update)
There is no "restart" API endpoint in Kubernetes. To restart a Deployment (just like `kubectl rollout restart`), a DevOps engineer must patch the Pod template's annotations with a new timestamp. This forces Kubernetes to gracefully cycle the pods!

```python
from kubernetes import client, config
from datetime import datetime

config.load_kube_config()
apps_v1 = client.AppsV1Api()

# The payload to trigger a rolling update
patch_body = {
    "spec": {
        "template": {
            "metadata": {
                "annotations": {
                    "kubectl.kubernetes.io/restartedAt": datetime.utcnow().isoformat()
                }
            }
        }
    }
}

apps_v1.patch_namespaced_deployment(name="nginx-deployment", namespace="default", body=patch_body)
print("Rolling update triggered!")
```

---

## 7. Advanced DevOps: Executing Commands inside Pods (`stream`)
Sometimes you need a script to check a file or run a diagnostic tool *inside* a container. You can use the `kubernetes.stream` module to execute commands.

```python
from kubernetes import client, config
from kubernetes.stream import stream

config.load_kube_config()
v1 = client.CoreV1Api()

# Equivalent to: kubectl exec my-pod -- ls -la /app
exec_command = ["ls", "-la", "/app"]

response = stream(
    v1.connect_get_namespaced_pod_exec,
    "my-pod",
    "default",
    command=exec_command,
    stderr=True, stdin=False, stdout=True, tty=False
)

print(f"Command Output:\n{response}")
```

---

## 🧑‍💻 Practice Exercises
We have created `day29_kubernetes_automation.py` in this folder. 
It contains a complete **Kubernetes DevOps CLI Tool**. It implements three massive operational scenarios: 
1. **Cluster Health Check** (`python script.py health`)
2. **Automated Scaling** (`python script.py scale <deployment> <replicas>`)
3. **Log Analyzer** (`python script.py analyze <pod>`)
