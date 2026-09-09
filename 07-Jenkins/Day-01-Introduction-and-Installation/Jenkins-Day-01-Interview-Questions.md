# 🎤 Jenkins Day 1: Interview Questions

This document contains a dedicated list of CI/CD and Jenkins interview questions from Day 1, focusing heavily on the critical differences between Continuous Delivery and Continuous Deployment, as well as scenario-based questions and AWS networking concepts.

---

## 🚀 Core Concepts: Delivery vs Deployment

**1. What is Continuous Delivery?**
**Answer:** Continuous Delivery is a software development practice where code changes are automatically built, tested, and prepared for release. The application is kept in a **deployable state**, but the final production deployment may require a **manual approval**.
*Flow:* `Git -> Build -> Test -> Deploy to UAT -> Manual Approval -> Production`

**2. What is Continuous Deployment?**
**Answer:** Continuous Deployment is a practice where code changes that successfully pass the required build and testing stages are **automatically deployed to production** without any manual approval.
*Flow:* `Git -> Build -> Test -> Deploy to UAT -> Tests Pass -> Automatically Deploy to Production`

**3. What is the exact difference between Continuous Delivery and Continuous Deployment?**
**Answer:** 
- **Continuous Delivery:** Application is ready for release. Production deployment can require a manual approval gate. Focus is on being ready.
- **Continuous Deployment:** Application is automatically released. No manual production approval in the normal flow. Focus is on automated deployment.

**4. Does Continuous Delivery mean production deployment is always manual?**
**Answer:** No. Continuous Delivery simply means the software is continuously brought to a **deployable/releasable state**. An organization may choose to manually approve production deployment (e.g. clicking a button), but the defining idea is that the software is ready for release.

**5. What is the main benefit of Continuous Deployment?**
**Answer:** The main benefit is that validated code can reach production quickly and automatically. It reduces manual deployment work and enables frequent releases to the end user.

**6. Why would a company choose Continuous Delivery instead of Continuous Deployment?**
**Answer:** A company may require manual approval before production because of regulatory requirements, business approvals, security audits, risk management, compliance, or planned release windows (e.g. only releasing on weekends).

**7. Can Continuous Delivery and Continuous Deployment use the same CI pipeline?**
**Answer:** Yes. The build and testing (CI) portions can be exactly the same. The major difference is only the final production release step (Manual Gate vs Automated).

---

## 🛣️ Pipelines and Gates

**8. What is a deployment gate or approval gate?**
**Answer:** An approval gate is a control point in a CI/CD pipeline where a person (like a Release Manager) or a predefined condition must approve the application before it proceeds to the next stage, commonly Production.

**9. Where does Continuous Integration fit into CI/CD?**
**Answer:** Continuous Integration focuses primarily on automatically building and testing code changes. Continuous Delivery/Deployment extends the CI pipeline toward release and deployment.

**10. Explain CI/CD with DEV, TEST, UAT and PROD.**
**Answer:** A typical pipeline moves an application through multiple environments. 
- With Delivery: `UAT -> Manual Approval -> PROD`. 
- With Deployment: `UAT -> Automated Validation -> PROD`.

---

## 🎭 Scenario-Based Interview Questions

**11. Your application passed all tests. The company requires a manager to approve the production release. Is this Continuous Delivery or Continuous Deployment?**
**Answer:** This is Continuous Delivery, because the application has been automatically validated and is ready for production, but a manual approval is required before the production release.

**12. Your application passes all automated tests and Jenkins automatically deploys it to production. What is this?**
**Answer:** This is Continuous Deployment.

**13. A developer pushes code to GitHub. Jenkins builds it and runs tests. Is this Continuous Deployment?**
**Answer:** No. This is primarily Continuous Integration. If the pipeline continued and automatically deployed the application to production, then it would become Continuous Deployment.

**14. Jenkins builds and tests an application and automatically deploys it to DEV, but production requires approval. What approach is this?**
**Answer:** This is consistent with Continuous Delivery. The pipeline automates the delivery process, but production release has a manual approval gate.

**15. Why is Continuous Deployment considered more automated than Continuous Delivery?**
**Answer:** Because Continuous Deployment completely removes the manual production release step. The pipeline automatically moves successfully validated changes into production without human intervention.

---

## 🏆 The "Very Important" Interview Question

**16. What is the difference between Delivery and Deployment?**
**Answer:** 
"Continuous Delivery means we automatically build, test, and prepare the application so that it is always ready for release, but production release may require a manual approval. Continuous Deployment goes one step further by automatically deploying successfully validated changes to production without manual intervention."

---

## 🌐 AWS Networking & Jenkins Port Questions

*(Added from the earlier notes so you have all Day 1 questions in one place!)*

**17. What is the default port of Jenkins?**
**Answer:** 8080.

**18. Why did you open port 8080 in the AWS EC2 Security Group?**
**Answer:** Jenkins runs on port 8080 by default, so I added an inbound TCP Custom rule for port 8080 in the EC2 Security Group (firewall) to allow access to the Jenkins web interface from the internet.

**19. How do you access Jenkins running on a remote EC2 server?**
**Answer:** `http://<server-public-ip>:8080`

**20. Why do we use the IP address combined with port 8080?**
**Answer:** The IP address identifies the physical physical EC2 server, while port 8080 identifies the specific network service (Jenkins) listening on that server.

---

## 🧠 One-Line Memory Tricks
- **CI =** Build & Test
- **Continuous Delivery =** Ready to Release
- **Continuous Deployment =** Automatically Release
- **Jenkins =** Automates the Pipeline
