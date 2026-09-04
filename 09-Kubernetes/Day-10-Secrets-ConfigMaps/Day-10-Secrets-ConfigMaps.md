# Day 10: Secrets, ConfigMaps, and Resource Limits

Welcome to Day 10! Today we are learning how to pass data to our Pods securely, and how to prevent our Pods from consuming too much CPU or Memory on our Worker Nodes.

**The General Workflow for Data Injection:**
As noted in class, this is a 2-step process:
1. We create the object (Secret or ConfigMap) using a YAML file or an ad-hoc command.
2. We pass this value inside our Pod definition.

---

## 🔐 1. Secrets
Secrets are used to store **sensitive data** that your application needs, such as:
- Usernames and Passwords
- API Keys
- Database URLs
- SSH Key Pairs and SSL Certificates

**How it works:** Kubernetes encrypts Secret data using **Base64 algorithm**. 
*(Note: Both Secrets and ConfigMaps have a strict maximum size limit of **1MB** per file).*

### 💻 Lab 1A: Creating a Secret
Let's create two text files on our machine containing dummy credentials, and then convert them into a Kubernetes Secret object using an ad-hoc command.

```bash
cd secrets
ls
echo "root" > username.txt
echo "password" > password.txt
ls
# now we created the username and password file

# Create the Secret object
> [!WARNING]  
> Make sure to specify the TYPE of secret (in this case, `generic`). If you just run `kubectl create secret mysecret`, the command will fail!

kubectl create secret generic mysecret --from-file=username.txt --from-file=password.txt 

kubectl get secrets
kubectl describe secret mysecret
```

### 💻 Lab 1B: Using the Secret in a Pod (Volume Mount)
Once the Secret exists in Kubernetes, we can pass it to our Pod. The first way is to mount it as a Volume.

Create `pod_secret_vol.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myvolsecret
spec:
  containers:
    - name: c1
      image: centos
      command: ["/bin/bash", "-c", "while true; do echo Hello-devops; sleep 5; done"]
      volumeMounts:
        - name: testsecret
          mountPath: "/tmp/mysecrets"

  volumes:
    - name: testsecret
      secret:
        secretName: mysecret
```

**Test it:**
> [!NOTE]  
> Make sure to include a space `-- ls` so kubectl knows it is a command and not a flag!

```bash
kubectl apply -f pod_secret_vol.yml
kubectl get pods
kubectl exec myvolsecret -- ls /tmp/mysecrets
```

### 💻 Lab 1C: Using the Secret (Environment Variable)
The second way to pass a secret is to inject it directly as an Environment Variable.

Create `pod_env.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myenvsecret
spec:
  containers:
    - name: c1
      image: centos
      command: ["/bin/bash", "-c", "while true; do echo Hello-devops; sleep 5; done"]
      env:
        - name: MYENVUSER
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: username.txt
```

**Test it:**
> [!NOTE]  
> Ensure you use the exact pod name defined in the YAML (`myenvsecret`) when running the exec command.

> [!NOTE]  

> Use the `--all` flag to clear out old pods before testing.

```bash
kubectl delete pods --all
kubectl apply -f pod_env.yml
kubectl exec myenvsecret -- env
```

---

## 📄 2. ConfigMaps
ConfigMaps are used to store **non-sensitive data** like:
- Database Host IP Addresses
- Ports
- General `.conf` or `.properties` files
- Certificates (As mentioned in notes, though sometimes stored in Secrets too!)

### 💻 Lab 2: Creating and Using a ConfigMap
Create a file named `sample.conf` on your machine (using the exact syntax from class):
```text
{{
name: siva
org: abc
db_name: xyz
db_port:1299
}}
```

Now, create the ConfigMap object in Kubernetes:
> [!NOTE]  
> Make sure to provide a name for your ConfigMap (like `myconfig`) in the create command.

```bash
kubectl create configmap myconfig --from-file=sample.conf
kubectl get cm
kubectl describe cm myconfig
```

Create `pod_config.yml` to mount this config file:
> [!NOTE]  
> There are 2 ways to pass ConfigMaps: Volume Mounts and Environment Variables (`env`). We will focus on the Volume mount method here.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myvolconfig
spec:
  containers:
    - name: c1
      image: centos
      command: ["/bin/bash", "-c", "while true; do echo Hello-devops; sleep 5 ; done"]
      volumeMounts:
        - name: testconfigmap
          mountPath: /etc/config

  volumes:
    - name: testconfigmap
      configMap:
        name: myconfig
        items:
          - key: sample.conf
            path: sample.conf
```

**Test it:**
> [!NOTE]  
> Double check your pod names and mount paths when running exec commands to avoid errors.

```bash
kubectl apply -f pod_config.yml
kubectl get pods
kubectl exec myvolconfig -- ls /etc/config
kubectl exec myvolconfig -- cat /etc/config/sample.conf
```

---

## ⚖️ 3. Resource Limits & Requests
Pods can be greedy. If a Pod consumes too much CPU or Memory, it can crash the entire Worker Node. We can restrict this by defining **Requests** and **Limits**.

- **Requests:** The *minimum* amount of resources the Pod needs to start. (Kubernetes uses this to decide which Node to schedule the Pod on).
- **Limits:** The *maximum* amount of resources the Pod is allowed to consume. If it tries to use more CPU, it will be throttled. If it uses more Memory, it will be OOM (Out of Memory) Killed!

**Measurements:**
Like Health Checks, Limits and Requests are just *additional properties* of your Pod. We apply them in terms of Pods.
- `m` = millicores (CPU). `100m` means 0.1 CPU cores.
- `Mi` = Mebibytes (Memory). 

> [!WARNING]
> **Storage Math Cheat Sheet:** Ensure you do not mix up your storage units! Here is the standard table you should memorize:
> - `1 kb = 1024 bytes`
> - `1 mb = 1024 kb`
> - `1 gb = 1024 mb`
> - `1 tb = 1024 gb`

### 💻 Lab 3: Restricting Resources
Create `limit_restrict.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resources
spec:
  containers:
    - name: resource
      image: centos
      command: ["/bin/bash", "-c", "while true; do echo Hello-devops; sleep 5; done"]
      resources:
        requests:
          memory: "64Mi"
          cpu: "100m"
        limits:
          memory: "200Mi"
          cpu: "200m"
```
```bash
kubectl apply -f limit_restrict.yml
```

---

## 🏆 Putting It All Together
Congratulations! You have now learned all the major properties of a Pod. Here is what a fully professional, production-ready Deployment object looks like, combining **Replicas, Ports, Resources, Probes, and Volumes**!

*(Check out `deploy_complete.yml` in this folder to see the final master code!)*

---

## ?? 4. Zero-to-Hero Bonus: Interview Gotchas
Since you asked if there is anything else you need to know, here are three massive real-world concepts your teacher skipped, but you **must** know for production and interviews:

> [!CAUTION]
> **Gotcha 1: Secrets are NOT truly encrypted by default!**
> It is often mistakenly taught that Secrets use Base64 to encrypt data. **Base64 is NOT encryption; it is just encoding!** Anyone can decode a Base64 string in 2 seconds on Google. In a real production cluster, you must enable **Encryption at Rest (KMS)** in your Kubernetes configuration so the secrets are actually encrypted inside the database (etcd).

> [!TIP]
> **Gotcha 2: The Auto-Update Trick**
> If you mount a ConfigMap or Secret as a **Volume**, and then you edit the ConfigMap later, Kubernetes will automatically update the file inside the running Pod without restarting it! 
> HOWEVER, if you inject the ConfigMap/Secret as an **Environment Variable**, it will NEVER auto-update. You must manually restart the Pod to get the new variables.

> [!IMPORTANT]
> **Gotcha 3: Throttling vs Killing (CPU vs Memory)**
> In the Resources section, you learned about Limits. 
> - CPU is a **compressible** resource. If your Pod hits the CPU limit, Kubernetes will just throttle it (slow it down). It won't kill it.
> - Memory is an **incompressible** resource. If your Pod hits the Memory limit, Kubernetes has no choice but to terminate it immediately. This is the famous **OOMKilled** (Out Of Memory Killed) error!
