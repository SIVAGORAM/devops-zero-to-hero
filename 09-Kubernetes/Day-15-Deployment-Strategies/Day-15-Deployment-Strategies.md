# Day 15: Deployment Strategies

Welcome to Day 15! Today we are tackling **Deployment Strategies**. 

As a DevOps Engineer, deploying an application isn't just about getting it running; it is about *how* you transition users from the old version of the app to the new version. Do you shut everything down at once? Do you shift traffic gradually? These techniques are called Deployment Strategies.

![Deployment Strategies Comparison](file:///D:/Devops/Devops/09-Kubernetes/Day-15-Deployment-Strategies/deployment-strategies.png)

---

## 🏗️ 1. Modern vs Traditional Deployments

Before Docker and Kubernetes, traditional deployments were incredibly painful. Developers would compile a `.jar` or `.war` file, and DevOps engineers would manually stop the live server, copy the file over, and restart the server. This always caused massive downtime for users.

**Modern Deployments** are container-based. Instead of replacing files on a server, we replace entire Pods. Our goals are:
- **Zero Downtime:** Users should never see a 404 error during an update.
- **Rollback Safety:** If the new version crashes, we must instantly revert to the old version.
- **Velocity:** We want to deploy updates multiple times a day effortlessly.

---

## 🚀 2. The 4 Main Strategies

### Strategy A: Recreate
- **How it works:** Deletes all the old Pods (v1) entirely before spinning up the new Pods (v2). 
- **Pros:** Extremely simple. Avoids database schema conflicts because v1 and v2 never run at the same time.
- **Cons:** Complete downtime! Users cannot access the app while v1 is dead and v2 is still booting.
- **Use Case:** Development environments only. **Never use this in Production!**

### Strategy B: Ramped (Rolling Update)
- **How it works:** Deletes one v1 Pod, creates one v2 Pod, and waits for it to become healthy before moving to the next.
- **Pros:** Zero downtime.
- **Cons:** Rollback takes a bit of time since it has to happen pod-by-pod. 
- **Use Case:** This is the **default strategy in Kubernetes!** Suitable for most QA and Production workloads.

### Strategy C: Blue-Green
- **How it works:** You deploy a complete set of v2 Pods (Green) alongside your fully running v1 Pods (Blue). Once the Green environment is fully booted and tested, you instantly switch the Service router to point to Green.
- **Pros:** Zero downtime, and instant rollback! If Green fails, you just point the Service back to Blue in 1 second.
- **Cons:** Requires double the infrastructure resources temporarily (you run 10 pods instead of 5).

### Strategy D: Canary
- **How it works:** You route 90% of your users to the old version, and 10% of your users to the new version. If the new version works perfectly, you slowly increase the percentage until everyone is on the new version.
- **Pros:** Incredible safety. If the new version has a critical bug, it only affects 10% of users.

---

## 💻 3. Real-World Labs

### Lab 1: Recreate Strategy
Create `deploy_recreate.yml`. Notice the `strategy: type: Recreate` block.
```bash
kubectl apply -f deploy_recreate.yml
kubectl get pods --watch
```
*To test this, modify the YAML file and change the image to `v2`. When you apply it, you will see all pods terminate instantly before new ones are created!*

### Lab 2: Rolling Update Strategy
Create `rollingupdate.yml`. Because this is the Kubernetes default, you do not need to explicitly declare a strategy!
```bash
kubectl apply -f rollingupdate.yml
kubectl get pods --watch
```
*Change the image to `v2` and apply it. Watch closely: it will terminate one pod and create one pod simultaneously!*

### Lab 3: Blue-Green Deployment
In this lab, we use a Service to instantly switch traffic.

1. Deploy the old version: `kubectl apply -f deploy_blue.yml`
2. Create the router pointing to Blue: `kubectl apply -f service.yml`
3. Deploy the new version in the background: `kubectl apply -f deploy_green.yml`

At this point, you have two full deployments running, but users are only hitting Blue.
**To perform the switch:** Open `service.yml`, change the selector label from `myapp-blue` to `myapp-green`, and reapply it:
```bash
kubectl apply -f service.yml
```
*Traffic is instantly shifted to the Green deployment with zero downtime!*

### Lab 4: Canary Deployment
To create a Canary deployment natively in Kubernetes, we use two Deployments that share the **exact same Service label selector** (`app: myapp-canary`). The traffic percentage is determined by the number of replicas!

1. Deploy the stable version (4 replicas = 80% traffic): `kubectl apply -f deploy_canary_stable.yml`
2. Deploy the canary version (1 replica = 20% traffic): `kubectl apply -f canary_new.yml`

Because a shared Service will load-balance evenly across all 5 pods, 1 out of 5 users (20%) will randomly hit the new Canary version!

---

## 📚 4. Further Reading

To master deployment strategies, check out these excellent external resources provided in class:
- [StackOverflow: Canary Release Strategy vs Blue-Green](https://stackoverflow.com/questions/23746038/canary-release-strategy-vs-blue-green)
- [Medium: Implementing Canary Deployment in Kubernetes](https://medium.com/@muppedaanvesh/implementing-canary-deployment-in-kubernetes-0be4bc1e1aca)

---

## ?? 5. Zero-to-Hero Bonus: Interview Gotchas
Since you are mastering Kubernetes Deployments end-to-end, here are three massive real-world concepts about Deployment Strategies that you **must** know for production environments and senior-level interviews!

> [!CAUTION]
> **Gotcha 1: The Native Limits of Canary Deployments**
> In the lab above, we achieved a Canary rollout by using a 4-to-1 replica ratio (80% vs 20%). However, native Kubernetes is very primitive. It can only route traffic blindly based on replica counts. 
> In a real enterprise, you might want to route *exactly* 1% of traffic, or route traffic based on HTTP Headers (e.g., only users with a specific cookie get the new version). To achieve this, you cannot use native Kubernetes! You must use an **Ingress Controller** (like NGINX) or a **Service Mesh** (like Istio/Linkerd).

> [!TIP]
> **Gotcha 2: Controlling the Speed of Rolling Updates**
> When Kubernetes performs a Rolling Update, it doesn't just guess how fast to do it. You can strictly control the speed and safety using two parameters in your YAML:
> - maxSurge: How many *extra* pods can be created above your desired replica count during the update.
> - maxUnavailable: How many pods are allowed to be temporarily offline during the update.
> *(Interview Tip: If you set maxUnavailable: 0, you guarantee that your users never experience a drop in capacity during the rollout!)*

> [!IMPORTANT]
> **Gotcha 3: Nobody does this manually in Production!**
> In our Blue-Green lab, you manually changed a label in service.yml and ran kubectl apply to switch traffic. In modern DevOps, this is completely automated! 
> Enterprises use advanced GitOps tools like **Argo Rollouts** or **Flagger**. These tools automatically shift the traffic, monitor Prometheus for 500 HTTP errors, and automatically rollback to the old version if the new version fails�with zero human intervention!
