# Day 13: Troubleshooting in Kubernetes

Welcome to Day 13! Troubleshooting is the most important skill for a DevOps engineer. To successfully troubleshoot an issue in Kubernetes, you must first deeply understand the **Lifecycle of a Pod**.

By looking at exactly which "Phase" a Pod is stuck in, you can immediately identify the root cause of the error.

---

##  1. The Pod Lifecycle (6 Phases)

Whenever you apply a manifest file (`kubectl apply -f pod.yml`), the Kubernetes Master receives the request and begins the lifecycle.

1. **Pending Phase**
   - *What is happening:* The Master is checking for resource availability across the Worker Nodes.
   - *Why it gets stuck here:* If there is not enough CPU/Memory on any node, or if the requested node does not exist, the Pod cannot be assigned. It will stay `Pending` forever.
2. **ContainerCreating Phase**
   - *What is happening:* The Pod has successfully been assigned to a Node. The `kubelet` on that node is now trying to pull the Docker image and mount the requested PVs, PVCs, and Secrets.
   - *Why it gets stuck here:* If the image name is typoed, the Docker registry (like DockerHub or AWS ECR) is down, or the PVC does not exist, the pod will hang in `ContainerCreating`.
3. **Running Phase**
   - *What is happening:* The image downloaded successfully, storage mounted correctly, and the application started.
   - *Why it fails here:* If the application crashes internally due to a code error, the Pod might show `CrashLoopBackOff` while trying to restart.
4. **Failed Phase**
   - *What is happening:* The container exited with a non-zero exit code, meaning a fatal application or network error occurred.
5. **Unknown Phase**
   - *What is happening:* The Kubernetes Master can no longer communicate with the Worker Node where the Pod is running (often due to network failure between the Master and Slave nodes).
6. **Terminating Phase**
   - *What is happening:* You ran a command to delete the Pod, and Kubernetes is gracefully shutting down the containers.

---

##  2. The Core Troubleshooting Commands

When a Pod is broken, you only need four commands to solve 99% of issues:

1. **`kubectl get pods`**
   - Tells you the current *Phase* (Status) of the Pod.
2. **`kubectl describe pod <pod-name>`**
   - **This is your best friend.** It prints a detailed list of "Events" at the bottom of the output, showing exactly *why* a Pod is stuck in Pending or ContainerCreating.
3. **`kubectl logs -f <pod-name>`**
   - Streams the raw application logs from inside the container (useful if the Pod is crashing during the Running phase).
4. **`kubectl exec -it <pod-name> -- /bin/bash`**
   - Logs you directly into the container's terminal so you can manually check files, test curl commands, and poke around.

---

##  3. Real-World Troubleshooting Labs

Let's intentionally break things and learn how to debug them using the `describe` command!

### Lab A: Resource Crunch (Pending State)
If your Pod requests more Memory or CPU than any single Worker Node has available, it cannot be scheduled.

Create `resourcecrunch.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dummy
spec:
  containers:
    - name: c1
      image: ubuntu
      command: ["/bin/bash", "-c", "while true; do echo hello-devops; sleep 4; done"]
      resources:
        requests:
          memory: 4Gi
        limits:
          memory: 6Gi
```
**Troubleshoot It:**
```bash
kubectl apply -f resourcecrunch.yml
kubectl get pods
```
Notice the Pod is stuck in `Pending`. Why?
```bash
kubectl describe pod dummy
```
*Check the "Events" at the bottom of the output. It will explicitly tell you that no nodes have enough memory available!*

### Lab B: Node Unavailability (Pending State)
If you use a `nodeSelector` to force a Pod onto a specific machine, but that machine label doesn't exist, it will hang.

Create `nodeunavailability.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dummy-node
spec:
  containers:
    - name: c1
      image: ubuntu
      command: ["/bin/bash", "-c", "while true; do echo hello-devops; sleep 4; done"]
  nodeSelector:
    mynode: demonode
```
**Troubleshoot It:**
```bash
kubectl apply -f nodeunavailability.yml
kubectl get pods
kubectl describe pod dummy-node
```
*The Events log will tell you `0/1 nodes are available: 1 node(s) didn't match Pod's node affinity/selector.`*

### Lab C: Storage Binding Issues (ContainerCreating State)
When an application requires Persistent Storage, it must bind a PVC to a PV. If they are misconfigured, the Pod will fail to create.

Create `pv.yml`:
*(This file contains a perfectly configured Pod, PV, and PVC. If you apply it, it will work perfectly.)*
```bash
kubectl apply -f pv.yml
kubectl get pods
```

**How to break it:**
Try editing `pv.yml` and changing the PVC's `storage` request to `2Gi`. The PV only has `1Gi` available! 
If you apply the broken file, the Pod will hang in `ContainerCreating`. Running `kubectl describe pod example-pod` will instantly reveal the volume binding failure!

---

##  4. Zero-to-Hero Bonus: Image Registries

During the `ContainerCreating` phase, Kubernetes downloads the Docker image from a centralized repository. If you are working in a real enterprise, you will likely encounter one of these common registries:
- **DockerHub:** The public default.
- **AWS ECR (Elastic Container Registry):** Amazon's managed, private registry.
- **JFrog Artifactory / Nexus:** On-premise enterprise registries that store both Docker images and raw application binaries (like `.jar` files).

If your Pod is stuck in `ContainerCreating` with an `ImagePullBackOff` error, it almost always means your cluster does not have the correct authentication credentials to pull from these private registries!

