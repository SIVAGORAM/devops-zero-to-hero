# Day 14: Troubleshooting Part 02 (CrashLoops & OOMKilled)

Welcome to Day 14! In Part 01, we learned how to troubleshoot Pods that get stuck in the `Pending` or `ContainerCreating` phases. Today, we are focusing on the most infamous error in Kubernetes: what happens when a Pod successfully reaches the `Running` phase, but then instantly crashes!

---

##  1. CrashLoopBackOff

If you ever run `kubectl get pods` and see the status `CrashLoopBackOff`, it means your application inside the container started, encountered a fatal error, and died. 

Because Kubernetes is a self-healing system, it immediately tries to restart the container to fix it. If the container keeps crashing immediately upon startup, Kubernetes will eventually back off and wait longer between restart attempts. This infinite loop of crashing and restarting is called **CrashLoopBackOff**.

### Common Causes of CrashLoopBackOff:
1. **Application Code Errors:** A fatal exception in your code (e.g., a missing environment variable, database connection refused, or syntax error).
2. **Image Misconfiguration:** The Docker image is missing a required start command (`CMD` or `ENTRYPOINT`), or the command provided in the YAML is broken.
3. **Out of Memory (OOM):** The application requires more memory to start than the Kubernetes `limits` allow it to use.

> [!NOTE]  
> If the container engine itself cannot even start the container (for example, due to a broken volume mount path), you will see **RunContainerError** instead of CrashLoopBackOff.

---

##  2. OOMKilled (Out of Memory)

**OOM** stands for **Out Of Memory**. This is a highly common interview question!

If your application exceeds the `memory` limit defined in the Pod's YAML (or the namespace's ResourceQuota), Kubernetes will mercilessly terminate the container to protect the Worker Node from crashing. 

When this happens, the Pod status will briefly show `OOMKilled`. Kubernetes will then immediately try to recreate it. If the application demands that same amount of memory upon startup again, it will be `OOMKilled` again, leading straight into a `CrashLoopBackOff`!

### How to resolve OOM errors:
1. Optimize your application code to consume less memory.
2. Increase the memory `limits` in the Pod's YAML definition.
3. If blocked by a namespace quota, you must increase the memory quota of the entire namespace.

---

##  3. Lab: Forcing an OOMKilled Error

Let's intentionally trigger an `OOMKilled` error by using a Linux stress-testing image!

Create `crashloop-1.yml`:
*(Notice that the container is strictly limited to `200Mi` of memory, but the `stress` command is forcefully attempting to consume `250M` of memory!)*
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: testpod
spec:
  containers:
    - name: c00
      image: polinux/stress
      command: ["stress"]
      args: ["--vm", "1", "--vm-bytes", "250M", "--vm-hang", "1"]
      resources:
        requests:
          memory: "100Mi"
        limits:
          memory: "200Mi"
```

**Troubleshoot It:**

Open a second terminal to watch the pods in real-time, then apply the file:
```bash
# Watch the pods spawn and crash in real-time!
kubectl get pods --watch

# Apply the file
kubectl apply -f crashloop-1.yml
```

Once you see the pod enter the `CrashLoopBackOff` state, you can use the following commands to investigate exactly why it died.

###  Debugging Commands

**1. Check live resource usage:**
*(Note: This requires the Kubernetes Metrics Server to be installed in your cluster).*
```bash
kubectl top pod testpod
```

**2. Check the previous container's logs:**
When a pod is constantly restarting, standard `kubectl logs` might show you an empty screen because the current container just booted up 1 second ago! To see the logs of the container that *just crashed*, use the `--previous` flag!
```bash
kubectl logs -f testpod --previous
```

**3. Read the exact termination reason:**
Run the describe command and look at the `State:` and `Last State:` sections under the container details. You will clearly see `Reason: OOMKilled`.
```bash
kubectl describe pod testpod
```

---

## ?? 4. Zero-to-Hero Bonus: Advanced Error States
Since you are mastering Kubernetes Troubleshooting end-to-end, here are four massive real-world error states that you **must** know for production environments and senior-level interviews. These are the errors that separate juniors from seniors!

> [!CAUTION]
> **1. The Evicted State**
> What happens if a Worker Node physically runs out of Disk Space or Memory at the OS level? The kubelet panics and starts ruthlessly terminating Pods to save the machine. These Pods are marked as Evicted. 
> *Fix:* You must either delete unused files on the Node, or add more Worker Nodes to the cluster and let the ReplicaSet reschedule the pods elsewhere.

> [!TIP]
> **2. CreateContainerConfigError**
> Your Pod is stuck and hasn't even reached the Running phase. Why? This error almost always means you told the Pod to mount a Secret or ConfigMap that **does not exist** (or is typoed) in that specific Namespace! 
> *Fix:* Run kubectl describe pod and check the events. Create the missing Secret/ConfigMap and the Pod will instantly fix itself.

> [!IMPORTANT]
> **3. The Silent Killer: Empty Endpoints**
> Your Pod is Running perfectly. Your Service is deployed perfectly. But when you hit the URL, you get "Connection Refused". What is wrong? 
> **99% of the time, your Service's selector labels do not match your Pod's labels!** 
> *Fix:* Run kubectl get endpoints <service-name>. If the endpoints list is empty, it means the Service couldn't find any Pods matching its label selector. Fix the typo in the YAML labels!

> [!WARNING]
> **4. CrashLoopBackOff (Liveness Probe Failure)**
> Sometimes your code is completely bug-free and memory is perfectly fine, but you still get a CrashLoopBackOff. Why? 
> If your application takes 30 seconds to boot up, but your **Liveness Probe** starts checking after 5 seconds, the probe will fail. Kubernetes will assume the container is broken and kill it before it finishes booting!
> *Fix:* Increase the initialDelaySeconds in your Liveness Probe!

