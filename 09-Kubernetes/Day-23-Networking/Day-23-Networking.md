# Day 23: Internal Networking (CoreDNS & Network Policies)

Welcome to Day 23! Today we are mastering the absolute core of Kubernetes internal networking. If you ever have an interview question about "How does Pod A talk to Pod B?", this is the lesson that will give you the perfect answer.

---

## 🌐 1. CoreDNS (The Internal Phonebook)

### The "Phonebook" Analogy
Imagine you want to call your friend Siva. You don't memorize his 10-digit phone number, because what if he changes his phone number tomorrow? Instead, you just open your Contacts app, search "Siva", and hit call. The phonebook does the translation for you.

Kubernetes Pods die and get recreated constantly. Every time a Pod is recreated, it gets a **brand new IP address**. 
If your Frontend Pod is hardcoded to talk to the Database Pod at `10.0.1.50`, your app will completely break the second the Database Pod restarts and gets `10.0.1.51`.

**The Solution:** Kubernetes runs a built-in DNS server called **CoreDNS**.
Instead of using IP addresses, your Frontend just makes a request to `http://database-service`. 
CoreDNS acts as the phonebook, instantly translating `database-service` into the exact IP address of the currently healthy Database Pod!

### Practical Understanding
CoreDNS runs as a deployment in the `kube-system` namespace. You can actually see it running:
```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

When you create a Service named `my-backend`, CoreDNS automatically creates a DNS record for it.
The fully qualified domain name (FQDN) looks like this:
`my-backend.default.svc.cluster.local`

*(If your pods are in the same namespace, they can just use the short name: `my-backend`!)*

---

## 🛑 2. Network Policies (Internal Firewalls)

### The "Bouncer" Analogy
By default, Kubernetes is an "Open House". Every Pod can talk to every other Pod across any namespace. 

Imagine a 3-tier architecture: `Frontend -> Backend -> Database`.
If a hacker compromises your `Frontend` pod (maybe through a vulnerability in your website), they can completely bypass the Backend and talk directly to your `Database` pod to steal your data!

**Network Policies are the internal "Bouncers" (Firewalls) of Kubernetes.**
You write a Network Policy that explicitly says: *"The Database is ONLY allowed to accept traffic from the Backend. If the Frontend tries to talk to the Database, DROP the traffic."*

### Practical Lab: Building an Internal Firewall

Let's build a secure 3-tier architecture. 
*Note: Network Policies require a CNI that supports them (like Calico, which we installed on Day 19!).*

**1. Create the 3 Pods (Frontend, Backend, Database):**
Notice how we are assigning specific `labels` to each pod. Network policies use labels to identify who is who!
*(Check the physical YAML files in this directory!)*
```bash
kubectl apply -f frontend.yaml
kubectl apply -f backend.yaml
kubectl apply -f database.yaml
```

**2. Create the Network Policy (The Bouncer):**
We want to protect the `database`. We will create a policy that says: "Only allow traffic to the Database IF the traffic comes from a pod labeled `role: backend`."
```bash
cat <<EOF > db-network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: protect-database
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: database      # <--- Who are we protecting? The Database!
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: backend   # <--- Who is allowed to enter? ONLY the Backend!
    ports:
    - protocol: TCP
      port: 3306
EOF
kubectl apply -f db-network-policy.yaml
```

**3. The Result:**
- If the `backend` tries to `curl` the `database` on port 3306: **SUCCESS (HTTP 200)**.
- If the `frontend` tries to `curl` the `database` on port 3306: **TIMEOUT (Connection Dropped)**.

---

## 🧠 3. Zero-to-Hero Bonus: Interview Gotchas

When an interviewer asks you about Networking, use these exact answers to prove your senior-level knowledge:

> [!CAUTION]
> **Gotcha 1: "How do two Pods in completely different namespaces communicate with each other?"**
> **Never say:** "They use the Pod IP address."
> **Say this:** "By default, pods can communicate across namespaces freely. I would use the fully qualified domain name (FQDN) via CoreDNS. If Pod A is in the `dev` namespace, it can reach Pod B in the `qa` namespace by calling `http://service-b.qa.svc.cluster.local`."

> [!TIP]
> **Gotcha 2: "We applied a Network Policy but it is completely ignoring our rules and all traffic is still allowed. What is wrong?"**
> **Say this:** "Network Policies are completely ignored if your cluster's CNI (Container Network Interface) does not support them! If you are using a basic CNI like Flannel, Network Policies will silently fail. You MUST use a CNI like **Calico** or **WeaveNet** to enforce Network Policies."

> [!IMPORTANT]
> **Gotcha 3: "How do you completely isolate a namespace so no other namespace can talk to it?"**
> **Say this:** "I would create a default-deny Network Policy. I create a policy that targets an empty `podSelector: {}` in that namespace with no `Ingress` rules defined. This acts as a blank blanket that blocks all incoming traffic to the entire namespace, forcing developers to explicitly whitelist connections!"
