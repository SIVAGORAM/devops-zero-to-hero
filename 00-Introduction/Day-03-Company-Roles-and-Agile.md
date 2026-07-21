# Day 3: Software Company Roles & Agile Workflows

Before diving into complex DevOps tools like Kubernetes and AWS, you must first understand how a software product is built in the real world and who builds it. 

A software company is like a hospital. A hospital doesnâ€™t only have doctorsâ€”it relies on receptionists, nurses, pharmacists, and lab technicians working together to treat a patient. Similarly, building software requires multiple distinct roles working together as a team.

---

## 1. How a Product is Built (The Roles)

Imagine you joined Amazon as a DevOps Engineer and are assigned specifically to the **Amazon Fresh** product team. You are a crucial piece of a much larger machine.

Here is the exact lifecycle of how a feature moves from an idea to reality, and who is responsible at each step:

### Business Analyst (BA)
- **Role:** The BA is the first person who interacts with the customer or stakeholder to understand what they want, the business goals, and the problems to solve.
- **Output:** They create a **Business Requirements Document (BRD)**.

### Product Manager (PM)
- **Role:** Defines the product vision, strategy, priorities, and roadmap. They decide *what* should be built and *why* it's important.

### Product Owner (PO)
- **Role:** Converts the high-level business requirements into actionable development tasks. They create Epics and User Stories, and manage the team's backlog.

### UI/UX Designer
- **Role:** Creates the visual design (colors, layouts, buttons) and the overall user experience using tools like Figma or Adobe XD.

### Software Architect
- **Role:** Designs the technical structure (High-Level Design / Low-Level Design). They choose the tech stack (e.g., React, Node.js, PostgreSQL, AWS).

### Developers
- **Frontend Developers:** Build the UI (React, HTML, CSS).
- **Backend Developers:** Build the APIs, authentication, and core business logic.
- **Database Developers (DBA):** Design the database tables, relationships, and queries.

### QA (Quality Assurance) Engineers
- **Role:** Test the application for bugs, speed, and security before it reaches customers. If bugs are found, they send them back to the developers.

### Security Engineers (DevSecOps)
- **Role:** Protect the application by securing APIs, scanning for vulnerabilities, and managing access (IAM).

### â­ DevOps Engineer (You!)
- **Role:** You ensure the software built by the developers can be tested, deployed, and operated efficiently. 
- **Example Task:** When a developer finishes coding a new feature, you write the CI/CD pipeline that automatically pulls the code, builds it, tests it, creates a Docker container, and deploys it to Kubernetes.

### Release Manager
- **Role:** Coordinates teams and schedules software releases to minimize risk.

### Site Reliability Engineer (SRE)
- **Role:** Takes over once the application is in production. They monitor uptime, handle incidents, and optimize performance to ensure the site never goes down.

### Technical Writer
- **Role:** Creates API documentation, user manuals, and installation guides.

---

## 2. How Work is Managed: Jira & Agile

### What is Jira?
Jira is the industry standard project management and issue-tracking tool. In a real job, you won't just "guess" what to doâ€”you will receive specific tasks assigned to you on a Jira board.

**The Jira Hierarchy:**
1. **Epic:** A massive feature (e.g., *User Authentication*).
2. **Story:** A smaller requirement (e.g., *User Login Screen*).
3. **Task / Sub-task:** The actual technical work assigned to you (e.g., *Write Jenkins pipeline for Login Service*).

### Agile & Scrum Methodology
Software is no longer built using the slow "Waterfall" method where it takes a year to release a product. Modern companies use **Agile**.

- **Agile:** Developing software in small, frequent, iterative chunks.
- **Scrum:** The most popular Agile framework. It involves a Product Owner, a Scrum Master, Developers, QA, and DevOps engineers working as one unit.
- **Sprint:** A fixed period (usually 2 weeks) where the team commits to completing a specific set of User Stories.
- **Sprint Planning:** A meeting before the sprint to decide *what* work will be done and *who* will do it. As a DevOps engineer, you will estimate how long infrastructure tasks will take.
- **Daily Standup:** A quick 15-minute daily meeting where every team member answers three questions: *What did I do yesterday? What am I working on today? Are there any blockers in my way?*
- **Backlog Refinement (Grooming):** A meeting held during the sprint to review future user stories and ensure they are clear and ready for the *next* sprint.
- **Sprint Review (Demo):** A meeting at the end of the sprint where the team demonstrates the newly built working software to stakeholders and customers.
- **Sprint Retrospective (Retro):** A meeting after the sprint to discuss what went well, what went wrong, and how to improve.

### Scrum vs. Kanban (The DevOps Reality)
While software developers usually use **Scrum** (working in strict 2-week sprints), DevOps and SRE teams often prefer **Kanban**. 
- **Why?** DevOps work is highly unpredictable. If a production server crashes or a security vulnerability is found, you cannot wait for the "next sprint" to fix it. Kanban uses a continuous flow board (To Do âž” In Progress âž” Done) without fixed 2-week time limits, making it perfect for reactive operational work and rapid bug fixes.

---

## ðŸŽ¯ Day 3 Summary
- Software products are built by cross-functional teams, not by a single engineer. Every role relies on the others.
- A DevOps Engineer works closely with Developers, QA, Architects, and Security teams to automate builds, deployments, and infrastructure.
- **Jira** is the standard tool used to organize and track your daily work via Epics, Stories, and Tasks.
- Modern software companies use **Agile (Scrum)** to deliver software continuously in 2-week **Sprints**.

---
**[⬅️ Previous: Day 2 - SDLC & Basics](./Day-02-SDLC-and-Basics.md)** | **[➡️ Next: Day 4 - OS & Virtualization](../01-Operating-System/Day-04-OS-and-Virtualization.md)**

