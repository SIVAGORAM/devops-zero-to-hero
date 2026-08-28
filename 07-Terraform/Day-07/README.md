# Day 07: Terraform Vault Integration & Secrets Management

Welcome to Day 07! Today we dive into the most advanced and critical topic for enterprise security: **Secrets Management**. 
By the end of this lab, you will learn how to build a **HashiCorp Vault** server from scratch and integrate it with Terraform so that you *never* have to hardcode a password again.

*(Note: HashiCorp Vault is incredibly versatile. Beyond Terraform, you can seamlessly integrate it with **Ansible, CI/CD pipelines, and Kubernetes**!)*

---

## 🔒 4 Ways to Secure Terraform (Theory)

Before Vault, how did we handle sensitive data (like database passwords or API keys)? 
Here are the 4 common approaches:

1. **The `sensitive` Attribute**: You can add `sensitive = true` to a Terraform variable. This stops Terraform from printing the password to the terminal screen, but it *still* saves it in plain text inside the `terraform.tfstate` file!
   ```hcl
   variable "aws_access_key_id" {
     sensitive = true
   }
   ```
2. **Environment Variables**: You can temporarily save a password to your laptop's memory. Terraform can read it using `source = "env://..."`.
   ```bash
   export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
   ```
   ```hcl
   variable "aws_access_key_id" {
     source = "env://AWS_ACCESS_KEY_ID"
   }
   ```
3. **Encrypted Remote Backend**: Storing your state file in S3 with encryption (like we did in Day 04) ensures that even if passwords are in the state file, hackers can't read the file itself. *(Note: State files can be encrypted using secure remote backends like Terraform Cloud or S3)*.
4. **The Ultimate Solution (Secret Management System)**: Using a dedicated vault (like **HashiCorp Vault** or AWS Secrets Manager). Instead of giving Terraform a password, you configure Terraform to read the secret directly from the Vault.
   ```hcl
   data "vault_generic_secret" "aws_access_key_id" {
     path = "secret/aws/access_key_id"
   }
   ```

---

## 🏗️ Hands-On Lab: Zero to Hero Vault Integration

Today, we are going to build an actual HashiCorp Vault server, put a secret inside it, and write Terraform code to fetch it! 

### Step 1: Build the Vault Server (EC2)
1. Go to your AWS Console and launch an **Ubuntu EC2 Instance**.
2. **CRITICAL:** Edit the Security Group (Inbound Rules) and open **Custom TCP Port `8200`** to the internet (`0.0.0.0/0`). Vault uses this port to communicate!
3. Connect to your instance via SSH: `ssh -i yourkey.pem ubuntu@<EC2_IP>`

### Step 2: Install HashiCorp Vault
Once logged into your Ubuntu EC2 instance, run these exact commands to install Vault:
```bash
sudo apt update && sudo apt install gpg -y
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update
sudo apt install vault -y
```

### Step 3: Start the Vault Server
Run this command to turn Vault on in "dev mode" and expose it to the internet on port 8200:
```bash
vault server -dev -dev-listen-address="0.0.0.0:8200"
```
*(Leave this terminal window open! Vault will print a **Root Token** to the screen. Copy this token, you need it for the next step).*

### Step 4: Create a Secret (Vault UI)
1. Open your web browser and go to `http://<YOUR_EC2_IP>:8200`.
2. Paste the **Root Token** you copied to log in.
3. Click on **Secrets Engines** -> **Enable new engine** -> Select **KV** -> Click **Enable Engine**. (Keep the path as `kv`).
4. Click **Create secret**.
   - **Path**: `test_secret`
   - **Secret Data (Key)**: `username`
   - **Secret Data (Value)**: `siva2003`
5. Click **Save**. *Your secret is now locked in the vault!*

---

## 🔑 Step 5: Connecting Terraform to Vault (AppRole)

Terraform is a machine, not a human. It cannot type a username and password into a website. To let Terraform talk to Vault, we must create a machine-to-machine login called an **AppRole** (similar to an IAM Role in AWS).

*(Note: If you look in the Vault UI under Access -> Enable new method -> AppRole, you can enable it there, but you **cannot** actually create the roles from the user interface. You must use the terminal!)*

1. Open a **second, brand new terminal window** on your laptop and SSH into your EC2 instance again.
2. Tell this new terminal where the Vault is located:
   ```bash
   export VAULT_ADDR='http://0.0.0.0:8200'
   ```
3. Enable AppRole Authentication:
   ```bash
   vault auth enable approle
   ```
4. Create a Policy (This tells Vault exactly what Terraform is allowed to read):
   ```bash
   vault policy write terraform - <<EOF
   path "*" { capabilities = ["list", "read"] }
   path "secrets/data/*" { capabilities = ["create", "read", "update", "delete", "list"] }
   path "kv/data/*" { capabilities = ["create", "read", "update", "delete", "list"] }
   path "secret/data/*" { capabilities = ["create", "read", "update", "delete", "list"] }
   path "auth/token/create" { capabilities = ["create", "read", "update", "list"] }
   EOF
   ```
5. Attach the Policy to a new AppRole named "terraform":
   ```bash
   vault write auth/approle/role/terraform \
       secret_id_ttl=10m \
       token_num_uses=10 \
       token_ttl=20m \
       token_max_ttl=30m \
       secret_id_num_uses=40 \
       token_policies=terraform
   ```
6. **Generate your Credentials (Crucial Step!)**:
   Run these two commands and save the outputs! Terraform needs them!
   - Get your **Role ID**: `vault read auth/approle/role/terraform/role-id`
   - Get your **Secret ID**: `vault write -f auth/approle/role/terraform/secret-id`

---

## 🚀 Step 6: The Terraform Code

Now look at the `main.tf` file in this `Day-07` folder!
1. Replace `<YOUR_EC2_IP>` with the public IP of your Vault server.
2. Replace `<YOUR_ROLE_ID>` and `<YOUR_SECRET_ID>` with the credentials you generated in Step 5.
3. Run `terraform init` and `terraform apply`.

**What happens?**
Terraform will use the Role ID and Secret ID to securely log into Vault, fetch the secret (`siva2003`), and attach it as a tag to a brand new AWS EC2 instance without you EVER typing "siva2003" into your Terraform code! 

**You are now officially implementing industry-grade Secrets Management!**
