# Comprehensive Kubernetes Interview Questions

*Note: This document contains an exhaustive, consolidated list of real-world Kubernetes interview questions categorized by topic. No answers are provided here—this is designed as a self-assessment checklist before an interview.*

## 1. KUBERNETES BASICS
- What is Kubernetes?
- What is Kubernetes and what is the use of it?
- What do you mean by Kubernetes?
- Why do we use Kubernetes?
- What are the advantages of using Kubernetes?
- Why is Kubernetes so popular? What are the advantages of using Kubernetes over other orchestration platforms?
- What is a Pod in Kubernetes?
- What is a container and what is a Pod?
- How do Pods work?
- How do Pods communicate with each other?
- How does Pod-to-Pod communication happen?
- How do Pod-A and Pod-B communicate within the cluster?
- How do you access other Pods in a cluster?
- How do you get the IP address of a Pod?
- What is the command to check the IP address in Docker and Kubernetes?
- How do you check how many Pods are running?
- How do you check the logs of a Pod?
- How do you check the logs of a Pod or Deployment?
- How do you check Kubernetes logs and Docker logs?
- How do you restart a Pod?
- What information do you get when you run the Pod inspect command?
- How do you check the activities performed by a container while creating a Pod?
- What are the possible reasons if a Pod is in Pending state?
- What are the issues faced during Pod creation and how would you solve them?
- If Pods are not coming up in a Kubernetes cluster, what may be the reasons and how would you solve them?
- If a Pod is continuously crashing, what could be the issue and how would you debug it?
- What are the different ways a container can get crashed?
- What are the possible reasons for CrashLoopBackOff?
- If a Pod fails with a CrashLoopBackOff error, how would you resolve it?
- What is Pod eviction and what are the reasons for Pod eviction?
- How will you prevent Pods from failure?
- If one container goes down when two containers are running inside a Pod, will it affect the other running container?
- If a node fails, what happens to the Pods running on that node?
- If a worker node is detached from the cluster, can we schedule a Pod to that node?
- How do you validate a Kubernetes cluster?
- What command do you use to check cluster CPU and memory?
- Is there any port requirement for Kubernetes?
- What are the Kubernetes components?
- Describe Kubernetes architecture and explain the use of each component.
- What is the Kubernetes architecture?
- What are the control plane components in Kubernetes?
- What is a Controller Node?
- What is the API Server?
- What is Kubelet?
- What is kube-proxy in Kubernetes?
- What is the difference between Docker and Kubernetes?
- What is the difference between Minikube and eksctl?
- What other Docker orchestration tools have you worked with?
- Is there any other tool or service that can be used apart from Kubernetes?
- What is Kubernetes and Microservices?

## 2. KUBERNETES SETUP
- How do you set up Kubernetes?
- How do you configure the Master and Worker Nodes?
- Which Kubernetes setup is used in your work environment?
- Have you worked with Google Kubernetes Engine (GKE), Amazon EKS, or Azure AKS?
- What are the major differences between GKE, EKS, and AKS?
- How many Master Nodes and Worker Nodes do you have?
- Why do you use 3 Master Nodes in production?
- What happens if one Master Node goes down? What is the impact?
- How many Worker Nodes do you have in your organization?
- How many Pods have you created for your project?
- How do you set up a Kubernetes cluster using kubeadm?
- How do you initialize the Master Node using kubeadm?
- How do you generate the token for Worker Nodes to join the cluster?
- How do you join a Worker Node to the Kubernetes cluster?
- What network plugin have you used with kubeadm?
- Which network plugin are you using?
- How do you install Calico in a Kubernetes cluster?
- How do you create a Kubernetes cluster using AWS EKS?
- What is the command to create an AWS EKS cluster?

## 3. PODS
- What is a Pod?
- What is the difference between a Pod and a Deployment?
- How do Pods communicate with each other?
- How do you get the IP of a Pod?
- How do you restart a Pod?
- What are the possible reasons for a Pod being in Pending state?
- What are the reasons for a Pod not coming up?
- What are the issues you may face during Pod creation?
- How do you debug a Pod that is not starting?
- What are the different ways a container can crash?
- If a Pod is continuously crashing, how do you troubleshoot it?
- What is CrashLoopBackOff?
- What are the possible reasons for CrashLoopBackOff?
- What is Pod eviction?
- What are the reasons for Pod eviction?
- How do you get Pod logs?
- How do you check the activities performed by a container while creating a Pod?
- How do you get detailed information about a Pod?
- What information do you get from kubectl describe pod?
- What is a static Pod in Kubernetes?
- What is the difference between a Static Pod and a Dynamic Pod?
- How do you create a Static Pod?
- How do you schedule a Pod on a particular Node?
- How do you deploy a Pod to a particular Worker Node?
- How do you schedule a Pod on a specific Node?
- How do you make sure that a Pod runs on a specific Node?
- How do you schedule all Pods from one Node to another Node?
- What happens to Pods when a Worker Node fails?

## 4. DEPLOYMENT
- What is a Deployment?
- What is the use of a Deployment?
- What are the types of Deployment strategies?
- What is the difference between a Pod and a Deployment?
- What is the difference between Deployment and ReplicaSet?
- What is the difference between Deployment and StatefulSet?
- Why would you use a Deployment instead of directly creating a ReplicaSet?
- Can we directly create a ReplicaSet in Kubernetes?
- If you do not create a Deployment and directly use a ReplicaSet, is it possible? Why is Deployment commonly used?
- How do you define replicas in Kubernetes?
- Where do you define the number of replicas and how does it work?
- How do you increase the number of replicas using a command?
- How do you make sure that two Pods are always available during a rolling update?
- How do you perform a rolling update?
- How do you rollback a Deployment?
- How do you write a Deployment manifest file?
- What are the steps to create a Deployment?
- How do you deploy a microservice in Kubernetes?
- If you have one Master Node and 10 Worker Nodes and you need one Pod on every Worker Node, how would you do it?
- If you have two microservices and one needs to run on t2.large while the other needs to run on m7g.large, how would you achieve this?
- If you created 3 replicas but only 2 Pods were created, how would you know why the third Pod was not created?
- If a Pod fails and you forgot to mention the replicas, how would you resolve the issue?
- If you need only 3 Worker Nodes to run Pods at any given time, how would you achieve this?

## 5. REPLICASET / REPLICATION CONTROLLER
- What is a ReplicaSet?
- What is the difference between Replication Controller and ReplicaSet?
- What is the difference between Deployment and ReplicaSet?
- Can we directly create a ReplicaSet in Kubernetes?
- Why is Deployment preferred over directly using a ReplicaSet?
- Can we create a ReplicaSet without creating a Deployment?
- How do you define replicas?
- How does ReplicaSet maintain the desired number of Pods?
- If you specify 3 replicas and only 2 Pods are running, how will you identify the problem?
- How will you know if a required Pod was not created without manually checking continuously?
- How do you add replicas using a command?
- What is an RC (Replication Controller)?
- Why do we use Replication Controller?
- What is the difference between Replication Controller and ReplicaSet?
- What is the difference between a ReplicaSet and replicas?

## 6. KUBERNETES SERVICES
- What is a Service in Kubernetes?
- What are the types of Kubernetes Services?
- What is the purpose of a Kubernetes Service?
- Explain the different Service types in Kubernetes.
- How do Pods communicate internally using a Service?
- How do you expose Pods internally?
- How do you expose an application to the external world?
- What is the difference between NodePort and LoadBalancer?
- What is NodePort?
- What is the purpose of a NodePort Service?
- How do you change a NodePort Service into a ClusterIP Service without changing the manifest file?
- How does a Service know which Pod it should redirect traffic to?
- What is a Service Endpoint?
- What is the difference between a Service and an Endpoint?
- How do you configure a Service?
- How do you configure a Deployment and Service?
- How do you write a YAML file for Deployment and Service?
- What are the steps to create a Deployment and Service?
- How do you expose a particular microservice?
- How do you route traffic to a specific microservice?

## 7. SERVICE ACCOUNT
- What is a ServiceAccount in Kubernetes?
- Why do we use ServiceAccounts?
- Have you ever created a ServiceAccount in Kubernetes?
- How do you configure a ServiceAccount?

## 8. NETWORKING
- What is Kubernetes networking?
- How do Pods communicate with each other?
- How does Pod-to-Pod communication happen?
- How do two Pods in different subnets communicate?
- How do Pods communicate across different Nodes?
- How do Pod-A and Pod-B communicate within a cluster?
- How do you access another Pod in the cluster?
- How do you expose Pods internally?
- How do you expose an application externally?
- How does communication happen between two Kubernetes clusters?
- How do two clusters communicate with each other?
- Which network plugin are you using?
- What is Calico?
- What is kube-proxy?
- What is a Network Policy in Kubernetes?
- How do Network Policies work?
- How will you secure your Kubernetes application?
- How will you give a route to a specified microservice?
- How do you route traffic to a particular microservice?
- What are Network Policies in Kubernetes?

## 9. LABELS, SELECTORS AND NODE SCHEDULING
- What are Labels in Kubernetes?
- What are Selectors in Kubernetes?
- What are the types of Selectors in Kubernetes?
- What is an Equality-Based Selector?
- What is a Set-Based Selector?
- What is the use of Selectors in Kubernetes?
- How does ReplicaSet use Labels and Selectors?
- How do you make sure that a Pod runs on a specific Node?
- How do you create a Pod on a particular Worker Node?
- How do you schedule a Pod on a specific Node?
- How do you deploy different microservices to different instance types?
- How would you schedule a Pod on a Node using Node Labels?
- How do you move Pods from one Node to another Node?

## 10. NAMESPACES
- What is a Namespace in Kubernetes?
- What is the purpose of using Namespaces?
- How do you switch between different Namespaces?
- How do you provide access to a Kubernetes cluster for a specific Namespace?
- How do you distribute resources within a Namespace?
- How do you restrict resources in a Namespace?
- If Pod-A is in one Namespace and Pod-B is in another Namespace, how will you establish communication between them?
- How does communication happen between different Namespaces?
- How do you provide user access to a specific Namespace?
- How do you manage resources within a Namespace?
- How do you switch Namespace with different Nodes?
- How do you manage a Kubernetes cluster?

## 11. HEALTH CHECKS
- What is a Liveness Probe?
- What is a Readiness Probe?
- What is the difference between Liveness and Readiness Probes?
- Why do we use Liveness and Readiness Probes?
- How do you configure Liveness and Readiness Probes?
- If you have two microservices with two ReplicaSets, how would you configure Liveness and Readiness Probes?
- What happens when a Liveness Probe fails?
- What happens when a Readiness Probe fails?
- What are the possible reasons for CrashLoopBackOff?
- 8.1 microservices there are 2 Replicaset, liveness probe and readiness probe.
- CrashLoopBackOff, what are the possible reasons?
- What is Readiness and Liveness?
- How to check the service is working properly or not in Kubernetes?
- How to check health check of the pods?
- About probes and types used.
- If liveness and readiness probe fails, what is the default action?
- If readiness probe error is raising, how do you resolve?
- How are you monitoring the Kubernetes cluster and the containers?

## 12. STORAGE / VOLUMES
- Which type of Volume is used for Pods?
- What are the different types of Volumes in Kubernetes?
- What is Kubernetes persistent storage?
- How do you mount NFS in a Kubernetes cluster?
- How do you connect NFS to a Kubernetes cluster?
- How does Kubernetes connect to NFS?
- How do you create a StorageClass in Kubernetes?
- How do you configure NFS with a StorageClass?
- How does Kubernetes communicate with external storage?
- What is the difference between different Kubernetes Volume types?

## 13. KUBERNETES NODE / SCHEDULING
- What is a Node in Kubernetes?
- What happens if a Node fails?
- What happens to the Pods when a Worker Node fails?
- How do you schedule a Pod on a particular Node?
- How do you schedule a Pod to a specific Worker Node?
- How do you schedule all Pods from one Node to another Node?
- How do you use Labels to schedule Pods on specific Nodes?
- How would you deploy one microservice to t2.large and another microservice to m7g.large?
- How do you make sure only specific Nodes are used for a workload?

## 14. DOCKER AND KUBERNETES
- What is the difference between Docker and Kubernetes?
- What is the difference between Docker orchestration and Kubernetes?
- How do you check Docker container logs?
- How do you check Kubernetes Pod logs?
- How do you check the IP address of a Docker container?
- How do you check the IP address of a Kubernetes Pod?
- What happens when a Docker container crashes?
- What happens when a Kubernetes Pod crashes?

## 15. AWS EKS
- What is Amazon EKS?
- How do you create an EKS cluster?
- What is the command to create an EKS cluster?
- What is the difference between EKS and a kubeadm cluster?
- What are the differences between EKS, GKE, and AKS?
- Which Kubernetes setup have you used in your work environment?
- How do you access an EKS cluster?
- How do you configure kubectl for an EKS cluster?

## 16. KUBERNETES CONFIGURATION
- What are the different ways to configure Kubernetes?
- How do you configure a Kubernetes cluster?
- How do you configure environment variables in Kubernetes?
- How do you define environment variables in Kubernetes?
- How do you pass configuration to a Pod?
- What is a ConfigMap?
- What is a Secret?
- How do you provide configuration values to containers?

## 17. KUBERNETES ARCHITECTURE / REQUEST FLOW
- Explain Kubernetes architecture.
- Explain all Kubernetes components and their responsibilities.
- What is the Control Plane?
- What is the API Server?
- What is Kubelet?
- What is Controller Manager?
- What is Scheduler?
- What is etcd?
- What is kube-proxy?
- How does a Kubernetes request flow through the cluster?
- If an end user accesses an application, how does the request reach the particular Pod?
- How does the Kubernetes Service route traffic to the correct Pod?
- What happens internally when you create a Pod?
- What activities are performed by Kubernetes when a Pod is created?
- What happens internally when you deploy an application in Kubernetes?

## 18. DEPLOYMENT + SERVICE PRACTICAL QUESTIONS
- Write a Deployment manifest file.
- Write a Service manifest file.
- Write YAML for Deployment and Service.
- Explain the steps to create a Deployment and Service.
- How do you deploy an Nginx application in Kubernetes?
- How do you expose an Nginx application?
- How do you expose a Deployment using a Service?
- How do you expose an application externally?
- How do you rollback a Deployment?
- How do you update the number of replicas?
- How do you perform a rolling update?
- How do you check the status of a Deployment?
- How do you check Deployment logs?
- How do you troubleshoot a Deployment when Pods are not running?

## 19. REAL-TIME SCENARIO QUESTIONS
- If you have 3 Pods running and 2 more need to be created, but one Pod is not created, how will you troubleshoot it?
- If you created 3 replicas but only 2 Pods are running, how will you identify the reason?
- If a Pod fails and you forgot to mention replicas, how would you resolve the issue?
- If a Pod is continuously crashing, what could be the issue and how would you debug it?
- If a Pod is in Pending state, what are the possible reasons?
- If a Pod is in CrashLoopBackOff, what are the possible reasons and how would you resolve it?
- If a Node goes down, what happens to the Pods running on that Node?
- If one Master Node goes down in a 3-Master production cluster, what happens?
- If an application is running in multiple Pods, how does Kubernetes distribute traffic?
- If two microservices need to communicate with each other, how would you configure communication?
- If two Pods are running in different Namespaces, how would they communicate?
- If two Pods are running on different Nodes, how would they communicate?
- If two Pods are running in different subnets, how would they communicate?
- If you need one microservice to run only on t2.large Nodes and another only on m7g.large Nodes, how would you achieve it?
- If you need one Pod on every Worker Node, how would you achieve it?
- If you need to run a maximum of 3 Pods on specific Worker Nodes, how would you achieve it?
- How would you move workloads from one Node to another Node?
- How would you expose a microservice internally?
- How would you expose a microservice externally?
- How would you secure communication between microservices?
- How would you restrict communication between Pods using Network Policies?
- How would you troubleshoot a Service that is not forwarding traffic to Pods?
- How would you troubleshoot a Pod that is running but the application is not accessible?
- How would you troubleshoot a Pod that is not getting scheduled?
- How would you troubleshoot a Pod that is repeatedly restarting?

## 20. COMMON KUBERNETES COMMAND QUESTIONS
- What command is used to validate the Kubernetes cluster?
- What command is used to check Nodes?
- What command is used to check Pods?
- What command is used to check Pods in all Namespaces?
- What command is used to check Pod logs?
- What command is used to describe a Pod?
- What command is used to get the IP address of a Pod?
- What command is used to check Services?
- What command is used to check Deployments?
- What command is used to check ReplicaSets?
- What command is used to check Namespaces?
- What command is used to check Node CPU and memory?
- What command is used to restart a Pod?
- What command is used to scale a Deployment?
- What command is used to rollback a Deployment?
- What command is used to create a Deployment?
- What command is used to expose a Deployment?
- What command is used to generate a kubeadm Worker Node join command?
- What command is used to initialize the Kubernetes Master Node?
- What command is used to get Kubernetes cluster information?

## 21. KUBERNETES INTERVIEW RAPID-FIRE QUESTIONS
- What is a Pod?
- What is a Deployment?
- What is a ReplicaSet?
- What is a Replication Controller?
- What is a Service?
- What is an Endpoint?
- What is a Namespace?
- What is a Node?
- What is a Static Pod?
- What is a Sidecar container?
- What is kube-proxy?
- What is Kubelet?
- What is the API Server?
- What is a Controller?
- What is a Scheduler?
- What is etcd?
- What is a ConfigMap?
- What is a Secret?
- What is a ServiceAccount?
- What is a Network Policy?
- What is a Liveness Probe?
- What is a Readiness Probe?
- What is a NodePort?
- What is a ClusterIP?
- What is a LoadBalancer?
- What is a StorageClass?
- What is a PersistentVolume?
- What is a PersistentVolumeClaim?
- What is a Namespace?
- What is a Label?
- What is a Selector?
- What is an Equality-Based Selector?
- What is a Set-Based Selector?
- What is Calico?
- What is CrashLoopBackOff?
- What is Pod eviction?
- What is rolling update?
- What is rollback?
- What is Kubernetes orchestration?
- What is the difference between Docker and Kubernetes?

## SECRETS
- What is difference between secret keys and ConfigMaps?
- Update the password in Secret without restarting the pod or deployment. Is it possible?
- How do you manage Secrets into Kubernetes? How does Kubernetes access these Secret files?
- How do you guarantee the application has access to the Secret file in Kubernetes?
- How will you manage the Secrets in EKS so that the Secrets in my organisation need to be changed every 90 days? How will you rotate the Secrets?
- What is Secret and what are the kinds you have used in Kubernetes? Explain all.
- How do you encrypt data in Secret?
- How will you protect the Secrets in a cluster? We should not store the Secrets in a Secret manifest. Give me any other option to store Secret and how will you access the Secrets to pods.
- Secret management. Explain Vault.

## CONFIGMAP
- What is the use of ConfigMap in Kubernetes?
- Difference between Secret and ConfigMap.
- What is ConfigMap and Secret? Where do you use them?
- Difference between ConfigMaps and Secrets and in how many ways can you create ConfigMaps?
- What is ConfigMap and why is it used and how to use it to access application?
- How will you inject values into K8s containers?

## PV-PVC
- Difference between PV and PVC.
- What is Persistent Volume in Kubernetes? How is the data saved in it?
- When we do PVC, we aren't able to get the PV. What would be the reason?
- Which service are you using as PV?
- Suppose we have 3 PVs in different availability zones. If we are going to create a pod using those PVs, will it create or not? What's that terminology name?
- PVC volumes: let's create a volume with 10 GB. After 2 days it is 9.5 GB full. How will you increase the PVC disk size from 10 GB to 20 GB?
- How will you give the application logs to the developer to debug any errors?
- Where will you store the application logs and how will you store them?

## DAEMONSET
- What is the use of DaemonSet in Kubernetes?
- What is DaemonSet?
- At the time of node update also, my DaemonSet should run. How will you do it? What is the command?
- One pod on one worker node, how will you do it?
- I have a DaemonSet but on one node it is duplicated (2 pods created). What is the issue?
- Suppose if we have 3 worker nodes, a pod has to run on each worker node. How will you do it?

## STATEFULSET
- What is Stateful and Stateless in Kubernetes?
- What is the advantage you get if Kubernetes is in StatefulSet?
- Difference between headful and headless service.
- What is Headless Service?
- What is the use of Headless Service in K8s?

## INIT CONTAINERS
- Init container in Kubernetes.
- What is the priority in Init Container?
- How will you make sure that the database should start first and then application?
- Before we start the main app container, we need to run some setup commands. How would you achieve this in K8s?

## AUTO-SCALING
- How to scale the pods?
- Horizontal or vertical scaling in K8s.
- How do you enable auto scaling in your EKS nodes?
- Types of auto scaling available in K8s.
- HPA?
- For scaling cluster, what all parameters would you change?
- How to ensure high availability of application in K8s?

## TAINTS & TOLERATIONS
- Taints, toleration and node affinity in K8s.
- What is taint and toleration?
- What is taint and toleration?
- Node affinity and pod affinity.

## ETCD
- If scheduler is not working, what will be the situation of your pods?
- If etcd is not working, what will be the status of your pods and will new pods be created?

## EKS / KUBERNETES CLUSTER
- EKS cluster updation.
- In K8s cluster, how do you deploy the application without root/sudo privileges?
- How do you give access to a user in K8s?
- Cluster update.
- Controller used in K8s.
- What is Control Plane in K8s?
- Explain steps involved in creating a K8s cluster.
- How many nodes have you used to create your cluster and why?
- How will you update EKS? What are all the steps you follow?
- K8s will be present on which type of subnet, public or private?
- What is annotation in K8s?
- How to update the K8s cluster?
- How will you give access of S3 bucket to a pod in K8s cluster?
- Difference between Role and ClusterRole.
- What approach will you take to update the node?
- Version of Kubernetes?
- Brief on project and K8s infrastructure.
- What are the base images you are using for microservices?
- How do you secure your K8s cluster? What is RBAC?
- How will you access the K8s cluster?
- Which cluster, EKS or kubeadm, are you using?
- If someone joined the team and I need to give the K8s cluster access to the user, how will you give it?
- How will you create highly available services? What services do you use and what are the steps?
- How to create a Kubernetes cluster? Procedure to create cluster and how do you take backup?
- How will you monitor the EKS cluster?
- Difference between EKS and ECS?
- What are the prerequisites and how do you create the EKS cluster?

## MANIFEST FILES
- Write a manifest file for deployment along with service.
- What are the components of a manifest file?
- Write the manifest file for Nginx pod.
- Write any Kubernetes manifest file.
- Which objects have you used in your manifest file for your project?
- How many applications, number of clusters, number of nodes, microservices, number of platforms maintaining in your project?
- Write a manifest file to deploy the application and expose it to the internet.
- In a manifest file, what should be defined inside the spec module?
- Commands for creating objects in K8s without using manifest files.
- I have 3 nodes and have to schedule 3-3-2 pods on each node respectively. How do you schedule?
- Write a YAML file containing a single array named configFiles, which contains an array of objects containing two fields, filename and owner, both having a string value.
- How will you launch 2 applications in a single Kubernetes cluster? If the resources are drained out, what will you do?
- If we have a K8s pod with a log file and this log file is stored in PV, and we want automated cleanup every week, how will you ensure that log files older than 30 days are deleted?
- I will give you code for 3 microservices and one AWS account. You should build an application, get it a DNS and launch it in the most cost-efficient way for demonstrating it to a client. How will you do it?

## TROUBLESHOOTING
- What troubleshooting work have you done with respect to Kubernetes cluster?
- Application is slow from one day. What are the commands you would use to check the reason and how to resolve it?
- Use case: We have a master and 10 worker nodes. At the time of maintenance, you cordon the node and again uncordon the node. Which is the key core component of the cluster having the details of the pod and node and then assigns them to the nodes?
- Use case: We have to schedule Pod-A and Pod-B in the same namespace, but they shouldn't communicate with each other. How can we restrict this by using an object?
- Pod stuck in CrashLoop. What are the measures you will take to solve the issue?
- If application in Kubernetes is not working, i.e. customers are not able to access your application, how will you solve the issue?
- Pod is in Pending state. What might be the reason?
- My website is not working and there is no Dev team available. How will you manage to keep the webpage alive?
- If Volume is full in Kube, what kind of error do you get?
- How to expose the container outside in Kube?
- Suppose you want to login to multiple clusters and you have a single credential. How to login?
- What all maintenance activities are done in K8s?
- What are the prerequisites required and commands used for particular node maintenance activity?
- Command to know cluster CPU and memory.
- How many nodes and pods are used in your project?
- What is the memory and CPU requirement for pods?
- If a pod is going down, how do you understand and debug the issue?
- Suppose I created 3 pods, only 2 pods are created. What is the issue and how will you resolve it?
- I have a Kubernetes cluster where the nodes are a mix of t4g.large and t3.large instances. My Kubernetes environment uses both kinds of nodes. I have an important service. If there is a larger disruption, I want it to be able to run on any node when required. What is the step in the build process which I need to be careful about for this particular requirement?
- Commit (GitHub) → GitLab → Runs the pipeline → Builds the image → Pushes to ECR → Runs a Helm command with proper context. The new image is installed in the cluster and starts running. But recently I am facing a trouble: when I push new code, GitHub gets the code, GitLab copies the code from GitHub properly, the pipeline runs properly, the image is pushed to ECR and I can verify that the uploaded image contains the right code and the right binary. However, when the Helm deployment happens, it succeeds but the new image is not being deployed. What can be going wrong?
- How many instances are there per deployment in your project?
- If you have 5 instances and traffic increases for some reason and servers are unable to handle the traffic, then how will you handle that situation?
- How do you decide what the default number of instances/pods required is and on what basis will you decide?
- I have changed replicas from 3 to 2 in the manifest, but still 3 pods are running. Debug the issue.
- How will you restart the pod?
- How will you increase the number of nodes in the cluster?
- Let's say the application is running on 3 pods and next month traffic may increase. How will you increase pods in order to handle traffic?
- What kind of challenges are faced in K8s?
- Which object is required to pull images into K8s? Explain.
- Tickets raised with respect to K8s in day-to-day activities.
- I am deleting a pod using the kubectl command, but it is still in Terminating state since 3 days. What might be the issue and how to resolve it?

## ADDITIONAL / ADVANCED SCENARIOS
- In Kubernetes I have an application and it should be launched by DNS name as well as by path provided. How will you launch it? What are the steps included?
- Few scenario based on BG deployment: You have changed the version but customers are still complaining that they are receiving the previous version. How will you solve the problem?
- How will you route the traffic from older version to new version?
- During deployment to EKS/ECS cluster, if pods fail, how do you come to know the pod status and troubleshoot the pods?
- I have 1 microservice and want to explore globally. How will you do it?
