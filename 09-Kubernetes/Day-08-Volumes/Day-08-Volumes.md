# Day 08: Kubernetes Volumes (Data Persistence)

Welcome to Day 08! Today we tackle one of the most critical topics in Kubernetes: **Storage and Data**.

## 🚨 The Problem: Data Loss
We know that containers are extremely lightweight, but they have a very short lifespan. Pods are **temporary** in nature. 

If your application (like a database) writes logs or saves user data inside a container, and that container is deleted, **all the data is permanently deleted with it!** 

## 🛡️ The Solution: Volumes (Folder Mapping)
To protect our data, Kubernetes uses **Volumes**. 

A Volume is simply **Folder Mapping**. You create a folder somewhere safe (outside the container), and you establish a connection to a folder *inside* the container. 
- Whatever data the container writes is saved to the safe folder.
- If the container is deleted, the data remains safely in the external folder! When a new container spins up, it simply reconnects to the old folder and picks up right where it left off.

There are 3 main types of volumes you need to know. Let's break them down from zero to hero!

---

## 📁 1. emptyDir Volume

**What is it?** This volume is created *inside the Pod itself*. It starts completely empty (`emptyDir: {}`).
**When do you use it?** You use this when you have **two or more containers inside a single Pod** that need to share files with each other temporarily.
**The Catch:** Because the volume is attached to the Pod, **if the Pod gets deleted, the data is still deleted!**

### 💻 Lab 1: emptyDir in Action
Let's create a Pod with two containers (`c1` and `c2`) sharing an `emptyDir` volume.

Create `emptydir.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: emptydirvolume
spec:
  containers:
    - name: c1
      image: centos
      command: ["/bin/bash", "-c", "sleep 1000"]
      volumeMounts:
        - name: xchange
          mountPath: "/tmp/xchange"

    - name: c2
      image: centos
      command: ["/bin/bash", "-c", "sleep 1000"]
      volumeMounts:
        - name: xchange
          mountPath: "/tmp/data"

  volumes:
    - name: xchange
      emptyDir: {}
```
> [!IMPORTANT]
> **How it works:** Notice both containers have a `volumeMounts` section pointing to the name `xchange`. Container 1 mounts it to `/tmp/xchange`, and Container 2 mounts it to `/tmp/data`. They are now linked!

**Test it:**
```bash
kubectl apply -f emptydir.yml
kubectl get pods

# 1. Log into Container 1 and create a file
kubectl exec emptydirvolume -c c1 -- touch /tmp/xchange/file1

# 2. Check Container 1 to see the file
kubectl exec emptydirvolume -c c1 -- ls /tmp/xchange

# 3. Check Container 2 to see the file!
kubectl exec emptydirvolume -c c2 -- ls /tmp/data
```
*You will see the file exists in both containers! If you delete the pod (`kubectl delete -f emptydir.yml`), the file is gone forever.*

---

## 🖥️ 2. hostPath Volume

**What is it?** Instead of putting the volume inside the Pod, we map a folder from the Pod directly to the **Host Machine** (The physical Worker Node your Pod is running on). 
**When do you use it?** When you need data to survive a Pod crash. It creates 2-way communication between the Node and the Pod.

### 💻 Lab 2: hostPath in Action

Create `hostpath.yml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myvolhostpath
spec:
  containers:
    - name: testc
      image: centos
      command: ["/bin/bash", "-c", "sleep 10000"]
      volumeMounts:
        - name: testvolume
          mountPath: /tmp/hostpath
  volumes:
    - name: testvolume
      hostPath:
        path: /tmp/data
```

**Test it:**
```bash
kubectl apply -f hostpath.yml
kubectl get pods -o wide     # Shows which Host Node it is running on

# Check the folder inside the pod
kubectl exec myvolhostpath -- ls /tmp/hostpath
```
*If you create a file inside the Pod at `/tmp/hostpath`, you can literally SSH into your Host Node, go to `/tmp/data`, and the file will be sitting right there!*

> [!WARNING]
> **The Flaw with hostPath:** What if the Host Machine (Worker Node 1) crashes? Kubernetes will recreate the Pod on Worker Node 2. But the data is stuck on Worker Node 1! To fix this, we need **Centralized Storage**.

---

## ☁️ 3. Centralized Storage (AWS EBS & Persistent Volumes)

To ensure data is never lost, no matter which Node a Pod runs on, we use network storage. While NFS (Network File Storage) exists, the modern industry standard is using Cloud Storage like **AWS EBS** (Elastic Block Store).

To connect K8s to AWS EBS, we use a two-step process: **PV** and **PVC**.

### Step A: The Persistent Volume (PV)
**What is it?** The PV is the actual physical hard drive in the cloud. It brings the EBS volume under the control of Kubernetes.

1. Go to AWS Console $\rightarrow$ EC2 $\rightarrow$ Volumes $\rightarrow$ Create Volume.
2. Copy the Volume ID (e.g., `vol-069912088ba16d52`).

Create `pv.yml`:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: myebs-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  awsElasticBlockStore:
    volumeID: vol-069912088ba16d52
    fsType: ext4
```
Apply it:
```bash
sudo su
kubectl apply -f pv.yml
kubectl get pv
```

### Step B: The Persistent Volume Claim (PVC)
**What is it?** A PVC is a "request" or "claim" made by an application for storage. It is like a ticket. Your application (Deployment) doesn't talk to the PV directly; it talks to the PVC, and the PVC binds to the PV.

Create `pvc.yml`:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myebs-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```
Apply it:
```bash
kubectl apply -f pvc.yml
kubectl get pvc
```

### Step C: Using it in a Deployment!
Now, instead of creating a folder on the host machine, we just tell our Deployment to use the `PVC` we just created!

Create `deploy.yml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp-container
          image: nginx
          volumeMounts:
            - name: ebs-volume
              mountPath: /usr/share/nginx/html
      volumes:
        - name: ebs-volume
          persistentVolumeClaim:
            claimName: myebs-pvc
```

Apply it:
```bash
kubectl apply -f deploy.yml
kubectl get pods
```

**Congratulations!** You now have a highly available Pod backed by a centralized, enterprise-grade AWS EBS volume. If that Pod is deleted, or the entire Worker Node explodes, the EBS volume is completely safe!
