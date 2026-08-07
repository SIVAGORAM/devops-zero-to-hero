# Project Management Tools for DevOps

When you join a company for your very first week as a DevOps Engineer, you won't immediately start writing Terraform scripts or deploying Docker containers. **The first thing you do is understand the company's Project Management structure.** 

You need to know how the team organizes their work, tracks bugs, shares knowledge, and handles emergency incidents. Today, we cover the core methodologies and tools you will use every single day in the real world.

---

## 1. Agile Methodology

Agile is a project management philosophy. Instead of building a massive product for a whole year and delivering it at the end (the old "Waterfall" method), Agile focuses on delivering small, working pieces of the product every 1 to 2 weeks (called **Sprints**).

As a DevOps engineer, you will participate in the 5 core steps of Agile:

1. **Evaluation of Current Processes:**
   - *What is it?* You map out the starting point. You need to understand the "Actual State" of the company's infrastructure before you try to change anything.
2. **Suggestions for Optimization:**
   - *What is it?* Once you understand the current state, you suggest improvements. You pick the right combination of technologies (like choosing Terraform over AWS CFT) to optimize the workflow.
3. **Application Design (With the Client):**
   - *What is it?* You choose the technologies and review options with the client. In Agile, the client is involved from the very beginning. Their continuous feedback is **VITAL**.
4. **Construction and Implementation:**
   - *What is it?* You deliver working developments to the end-user on a weekly basis. The end-user operates the software, tests it, and requests changes immediately.
5. **Evaluation and Monitoring:**
   - *What is it?* Once deployed, you track KPIs (Key Performance Indicators) and generate metrics to prove that the new process is actually working better than the old one.

---

## 2. The Core DevOps Tools

### A. Jira (Issue & Task Tracking)
**Jira** (made by Atlassian) is the most popular Agile project management tool in the world. 
Instead of your manager sending you an email saying "Fix the server", they create a **Ticket** (or Issue) in Jira. You will use Jira to track your daily tasks, see what your teammates are working on, and manage Sprints.

**Action Item (Zero to Hero Task):**
1. Go to Google and search for **"Download Jira - Atlassian Dashboard"**.
2. Click on the free trial.
3. Select any product from the dropdown (like Jira Software).
4. Generate a trial license and create a dummy project.
5. *Play around with it!* Create a task, move it to "In Progress", and move it to "Done". Getting familiar with this UI now will make your first week on the job significantly easier.

### B. Confluence (Knowledge Sharing)
**Confluence** (also by Atlassian) is like Wikipedia for your company. 
It is a Knowledge Sharing platform. When you create a brilliant Ansible playbook, you don't just leave it on your laptop; you write a documentation page in Confluence explaining how it works. It is the central hub for all technical docs, runbooks, and architectural diagrams. *(Note: Some companies use Microsoft SharePoint for this same purpose).*

### C. ServiceNow (Incident & Change Management)
**ServiceNow** is a massive enterprise IT service tool. As a DevOps engineer, you will use two main modules:
1. **Incident Management:** If a production server crashes at 2:00 AM, an "Incident" ticket is automatically created in ServiceNow. You use this ticket to track how and when you fixed the outage.
2. **Change Management:** You cannot just push code to Production whenever you feel like it. You must submit a "Change Request" in ServiceNow explaining what you are changing, the risks involved, and your rollback plan. Managers will review and approve this before you can deploy.

---
*Summary: Mastering these tools is just as important as mastering code. Communication and organization are the hallmarks of a Senior DevOps Engineer!*
