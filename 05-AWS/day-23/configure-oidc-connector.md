# commands to configure IAM OIDC provider 

```bash
export cluster_name=demo-cluster
```

```bash
oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5) 
```

## Check if there is an IAM OIDC provider configured already

```bash
aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4
```

If not, run the below command:

```bash
eksctl utils associate-iam-oidc-provider --cluster $cluster_name --approve
```
