# Day 01: Infrastructure as Code & Introduction to Terraform

Welcome to Module 07! Today we are diving into **Infrastructure as Code (IaC)** and the industry-standard tool for provisioning infrastructure: **Terraform** (developed by HashiCorp).

---

## 1. Infrastructure Before IaC

Before the advent of IaC, infrastructure management was typically a manual and time-consuming process. System administrators and operations teams had to:

1. **Manually Configure Servers:** Servers and other infrastructure components were often set up and configured manually, which could lead to inconsistencies and errors.
2. **Lack of Version Control:** Infrastructure configurations were not typically version-controlled, making it difficult to track changes or revert to previous states.
3. **Documentation Heavy:** Organizations relied heavily on documentation to record the steps and configurations required for different infrastructure setups. This documentation could become outdated quickly.
4. **Limited Automation:** Automation was limited to basic scripting, often lacking the robustness and flexibility offered by modern IaC tools.
5. **Slow Provisioning:** Provisioning new resources or environments was a time-consuming process that involved multiple manual steps, leading to delays in project delivery.

IaC addresses these challenges by providing a systematic, automated, and code-driven approach to infrastructure management. Popular IaC tools include Terraform, AWS CloudFormation, Azure Resource Manager templates and others. 

---

## 2. The Problem: The Hybrid Cloud Dilemma

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

## 3. The Solution: Terraform

To avoid all these issues, we do not learn all the proprietary tools. Instead, we learn **Terraform**.

**What Terraform Offers:**
- **One Universal Tool:** Terraform allows you to automate infrastructure across *multiple* cloud providers using just a single language. 
- **Cloud Agnostic:** If you write a script to create a server in AWS today, you can migrate that infrastructure to Azure tomorrow with minimal code changes. You don't have to rewrite everything from scratch in a new language.

### Why Terraform?
There are multiple reasons why Terraform is used over other IaC tools. Below are the main reasons:

1. **Multi-Cloud Support**: Terraform is known for its multi-cloud support. It allows you to define infrastructure in a cloud-agnostic way, meaning you can use the same configuration code to provision resources on various cloud providers (AWS, Azure, Google Cloud, etc.) and even on-premises infrastructure. This flexibility can be beneficial if your organization uses multiple cloud providers or plans to migrate between them.
2. **Large Ecosystem**: Terraform has a vast ecosystem of providers and modules contributed by both HashiCorp (the company behind Terraform) and the community. This means you can find pre-built modules and configurations for a wide range of services and infrastructure components, saving you time and effort in writing custom configurations.
3. **Declarative Syntax**: Terraform uses a declarative syntax, allowing you to specify the desired end-state of your infrastructure. This makes it easier to understand and maintain your code compared to imperative scripting languages.
4. **State Management**: Terraform maintains a state file that tracks the current state of your infrastructure. This state file helps Terraform understand the differences between the desired and actual states of your infrastructure, enabling it to make informed decisions when you apply changes.
5. **Plan and Apply**: Terraform's "plan" and "apply" workflow allows you to preview changes before applying them. This helps prevent unexpected modifications to your infrastructure and provides an opportunity to review and approve changes before they are implemented.
6. **Community Support**: Terraform has a large and active user community, which means you can find answers to common questions, troubleshooting tips, and a wealth of documentation and tutorials online.
7. **Integration with Other Tools**: Terraform can be integrated with other DevOps and automation tools, such as Docker, Kubernetes, Ansible, and Jenkins, allowing you to create comprehensive automation pipelines.
8. **HCL Language**: Terraform uses HashiCorp Configuration Language (HCL), which is designed specifically for defining infrastructure. It's human-readable and expressive, making it easier for both developers and operators to work with.

---

## 4. Core Concepts Explained

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

## 5. Getting Started (Terminology)

To get started with Terraform, it's important to understand some key terminology and concepts. Here are some fundamental terms and explanations:

1. **Provider**: A provider is a plugin for Terraform that defines and manages resources for a specific cloud or infrastructure platform. Examples of providers include AWS, Azure, Google Cloud, and many others. You configure providers in your Terraform code to interact with the desired infrastructure platform.
2. **Resource**: A resource is a specific infrastructure component that you want to create and manage using Terraform. Resources can include virtual machines, databases, storage buckets, network components, and more. Each resource has a type and configuration parameters that you define in your Terraform code.
3. **Module**: A module is a reusable and encapsulated unit of Terraform code. Modules allow you to package infrastructure configurations, making it easier to maintain, share, and reuse them across different parts of your infrastructure. Modules can be your own creations or come from the Terraform Registry, which hosts community-contributed modules.
4. **Configuration File**: Terraform uses configuration files (often with a `.tf` extension) to define the desired infrastructure state. These files specify providers, resources, variables, and other settings. The primary configuration file is usually named `main.tf`, but you can use multiple configuration files as well.
5. **Variable**: Variables in Terraform are placeholders for values that can be passed into your configurations. They make your code more flexible and reusable by allowing you to define values outside of your code and pass them in when you apply the Terraform configuration.
6. **Output**: Outputs are values generated by Terraform after the infrastructure has been created or updated. Outputs are typically used to display information or provide values to other parts of your infrastructure stack.
7. **State File**: Terraform maintains a state file (often named `terraform.tfstate`) that keeps track of the current state of your infrastructure. This file is crucial for Terraform to understand what resources have been created and what changes need to be made during updates.
8. **Plan**: A Terraform plan is a preview of changes that Terraform will make to your infrastructure. When you run `terraform plan`, Terraform analyzes your configuration and current state, then generates a plan detailing what actions it will take during the `apply` step.
9. **Apply**: The `terraform apply` command is used to execute the changes specified in the plan. It creates, updates, or destroys resources based on the Terraform configuration.
10. **Workspace**: Workspaces in Terraform are a way to manage multiple environments (e.g., development, staging, production) with separate configurations and state files. Workspaces help keep infrastructure configurations isolated and organized.
11. **Remote Backend**: A remote backend is a storage location for your Terraform state files that is not stored locally. Popular choices for remote backends include Amazon S3, Azure Blob Storage, or HashiCorp Terraform Cloud. Remote backends enhance collaboration and provide better security and reliability for your state files.

---

## 6. Install Terraform

### Windows

1. Install Terraform from the Downloads [Page](https://developer.hashicorp.com/terraform/downloads)

(or)

2. Use GitHub Codespaces (Free for 60 hours per month)

- Login to your GitHub account
- Click on the Profile Icon to the top right
- Click on "Your Codespaces" as shown in the [Image](../Images/codespaces-location.png)
- Codespaces will provide you a virtual machine with Ubuntu and VS Code by default.
- Follow the steps provided in the Downloads [Page](https://developer.hashicorp.com/terraform/downloads) for Linux.

### Linux

- Follow the steps provided in the Downloads [Page](https://developer.hashicorp.com/terraform/downloads) for Linux.

### macOS

- Follow the steps provided in the Downloads [Page](https://developer.hashicorp.com/terraform/downloads) for macOS.

---
**[Previous: Day 24 - Advanced Ansible](../../06-Ansible/Day-24-Advanced-Ansible-Mastery.md)** | **[Next: Day 02 - Terraform Zero to Hero](../Day-02/Day-02-Terraform-Zero-to-Hero.md)**
