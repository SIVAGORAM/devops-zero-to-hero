# Day 25: Infrastructure as Code & Introduction to Terraform

Welcome to Module 07! Today we are diving into **Infrastructure as Code (IaC)** and the industry-standard tool for provisioning infrastructure: **Terraform** (developed by HashiCorp).

---

## 1. The Problem: The Hybrid Cloud Dilemma

**Scenario:** 
Imagine you are a DevOps engineer working at a massive enterprise like Flipkart. The company runs 300 different applications. 
To ensure high availability and avoid vendor lock-in, Flipkart uses a **Hybrid Cloud Model**:
- **AWS** (for specific storage/compute services)
- **Azure** (for specific enterprise integrations)
- **GCP** (Google Cloud Platform, for AI/Data)
- **Physical On-Premise Servers** (for highly sensitive data)

**The Challenge:**
One day, your manager asks you to automate the creation of 100 virtual machines across all these different platforms. 

If you try to use cloud-specific tools, you would have to learn and write code in multiple different languages:
- For AWS, you must learn **AWS CFT (CloudFormation Templates)**.
- For Azure, you must learn **Azure ARM (Azure Resource Manager)**.
- For On-Premise (OpenStack), you must learn **Heat Templates**.

*Problem:* Learning, maintaining, and migrating hundreds of automation scripts across 4 different proprietary languages is an absolute nightmare for DevOps engineers.

---

## 2. The Solution: Terraform

To avoid all these issues, we do not learn all the proprietary tools. Instead, we learn **Terraform**.

**What Terraform Offers:**
- **One Universal Tool:** Terraform allows you to automate infrastructure across *multiple* cloud providers using just a single language. 
- **Cloud Agnostic:** If you write a script to create a server in AWS today, you can migrate that infrastructure to Azure tomorrow with minimal code changes. You don't have to rewrite everything from scratch in a new language.

---

## 3. Core Concepts Explained

### Infrastructure as Code (IaC)
Instead of logging into the AWS Console and clicking buttons to create 100 EC2 machines manually, you write a configuration script. When you execute the script, all 100 servers are created automatically, instantly, and identically. 

### API as Code
What does Terraform actually do under the hood?
An **API (Application Programming Interface)** is how two software systems talk to each other. Every cloud provider (AWS, Azure, GCP) has an API. 

Terraform acts as a universal translator. It takes the **"API as Code"** approach.
1. You write your infrastructure requirements in Terraform's simple language (HCL - HashiCorp Configuration Language).
2. Terraform's core engine reads your code.
3. Terraform automatically translates your code into the specific, complex API calls required by AWS, Azure, or GCP, and executes them on your behalf.

### Bottom Line
As a DevOps engineer, you do not need to memorize AWS CloudFormation, Azure ARM, or OpenStack Heat Templates. **You just learn Terraform.**

---
**[Previous: Day 24 - Advanced Ansible](../06-Ansible/Day-24-Advanced-Ansible-Mastery.md)** | **[Next: Day 26 - Terraform Zero to Hero](./Day-26-Terraform-Zero-to-Hero.md)**
