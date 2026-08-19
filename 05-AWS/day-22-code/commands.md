# ECR and Docker Commands

Run these commands to authenticate, build, and push your Docker image to Amazon ECR. 
*(Replace `<region>`, `<account-id>`, and `<repo-name>` with your actual AWS values).*

**1. Login to ECR**
```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
```

**2. Build the Docker image**
```bash
docker build -t <account-id>.dkr.ecr.<region>.amazonaws.com/<repo-name>:latest .
```

**3. Push the Docker image to ECR**
```bash
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/<repo-name>:latest
```
