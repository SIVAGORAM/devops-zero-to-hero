# Install EKS

Please follow the prerequisites doc before this.

## Install using Fargate

```bash
eksctl create cluster --name demo-cluster --region us-east-1 --fargate
```

## Delete the cluster

```bash
eksctl delete cluster --name demo-cluster --region us-east-1
```
