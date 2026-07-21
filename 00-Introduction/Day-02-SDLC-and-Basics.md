# Day 2: Software Development Life Cycle (SDLC) & Core Concepts

Welcome to Day 2! Today we focus on the Software Development Life Cycle (SDLC)-the blueprint of how software is built-and introduce the core tools and concepts that make up the DevOps pipeline.

---

## 1. What is SDLC?
**Software Development Life Cycle (SDLC)** is a structured, systematic process used by software companies to plan, design, develop, test, deploy, and maintain software. 
Its ultimate goal is to deliver high-quality, reliable, secure, and bug-free applications to customers efficiently.

### Why Do We Need SDLC?
Building software without SDLC is like building a house without a blueprint. Without a clear plan:
- Developers don't know exactly what to build.
- Testers don't know what to test.
- Customers receive buggy software.
- Projects become delayed and expensive.

---

## 2. The Phases of SDLC
SDLC is a continuous cycle. When new features are requested, the cycle begins again.

### Phase 1: Planning
The team decides what to build, why to build it, budget, timeline, team members, and technologies. *(Example: Choosing React for frontend, Node.js for backend, AWS for cloud).*

### Phase 2: Requirement Analysis (Defining)
Gathering detailed requirements (e.g., Who are the users? How should payments work?). The output is often a **Software Requirements Specification (SRS)** document.

### Phase 3: Designing
Architecting the system and designing the UI/UX. *(Outputs: Wireframes, database schemas, system architecture diagrams).*

### Phase 4: Development (Building)
Developers write the actual source code (Frontend, Backend, Database logic) and store it in a Version Control System like Git.

### Phase 5: Testing (QA)
The application is tested by Quality Assurance (QA) engineers to find and fix bugs before customers use it. (Includes Functional, Integration, Performance, and Security testing).

### Phase 6: Deployment
Moving the tested application to a server so users can access it over the internet.

### Phase 7: Production
The live environment where real users interact with the application (e.g., `amazon.com`).

### Phase 8: Maintenance
Fixing production bugs, improving performance, and planning new features (which restarts the cycle).

---

## 3. DevOps in the SDLC
Where does a DevOps engineer fit in? Many beginners think DevOps only handles deployment, but DevOps engineers are heavily involved in:
**Build -> Testing -> Deployment -> Production -> Monitoring**

### How DevOps Improves SDLC
*   **Traditional Process:** Manual Builds -> Manual Testing -> Manual Deployment *(Slow, error-prone, inconsistent).*
*   **DevOps Process:** Git Push -> Automatic Build -> Automatic Testing -> Automatic Deployment -> Monitoring.
*   **Benefits:** Faster releases, fewer human errors, better software quality, and easier rollbacks.

---

## 4. Essential DevOps Pipeline Concepts
Before we build a pipeline, you must understand its components.

### What is Source Code?
Human-readable code written by developers using programming languages (Java, Python, React). It is the raw material of the application.

### What is Version Control & Git?
- **Version Control:** The process of managing changes made to source code over time. It allows you to track history, collaborate, and rollback if mistakes are made.
- **Git:** The most popular distributed Version Control System (VCS) that runs on your local computer to track these code changes.

### What is GitHub?
A cloud-based platform that stores Git repositories online. While Git runs locally, GitHub enables team collaboration, code reviews, and remote backups.

### What is a Build?
The process of converting raw source code into a runnable, deployable application. This includes compiling code, bundling files, minifying CSS/JS, and generating executable artifacts.

### What is Quality Assurance (QA)?
The process of testing the built software to ensure it works correctly and meets required quality standards before releasing it to real users.

### What is Continuous Integration (CI)?
A DevOps practice where every code change is automatically built and tested whenever a developer pushes code to a shared repository (like GitHub).
- **Goal:** Detect problems early and keep the codebase healthy without manual intervention.

### What is Continuous Delivery vs Continuous Deployment (CD)?
We always hear "CI/CD". Since CI is the first half, CD is the second half:
- **Continuous Delivery:** The code is automatically built, tested, and prepped for release. It is completely ready to go live, but a human must manually click an "Approve" button to push it to production.
- **Continuous Deployment:** There is absolutely zero human intervention. The moment a developer pushes the code, if it passes all automated tests, it goes straight to live production automatically.

---

## 5. Crucial Industry Concepts: Agile & Microservices
If you are learning DevOps, you **must** understand *why* the industry shifted to DevOps in the first place. This shift was driven by two major changes:

### Waterfall vs. Agile Methodology
Before DevOps, software was built using the **Waterfall** model:
- **Waterfall:** A rigid SDLC where each phase must finish completely before the next begins. It took months or years to release software. 
- **Agile:** A flexible SDLC where software is built in small, iterative chunks (sprints) taking 2-4 weeks. 
- **The DevOps Connection:** Agile sped up Development so much that manual Operations (deployments) couldn't keep up. DevOps was created to bridge this gap by automating deployments to match Agile's speed.

### Monolithic vs. Microservices Architecture
- **Monolith:** The entire application is written as one single, massive codebase. If one part fails, the whole application crashes, and updating it requires redeploying everything.
- **Microservices:** The application is broken down into tiny, independent services (e.g., a Payment Service, a User Service). They communicate via APIs. 
- **The DevOps Connection:** Managing and deploying 50 microservices manually is impossible. DevOps tools like Docker and Kubernetes were adopted specifically to manage, deploy, and scale these microservices.

---

## How It All Connects (The DevOps Workflow)
```text
Developer Writes Source Code
      
      
Git (Tracks Changes Locally)
      
      
GitHub (Stores Code Online)
      
      
Continuous Integration / CI (Automatic Build + Automated Tests)
      
      
Quality Assurance / QA (Verifies the Application)
      
      
Deployment -> Production -> Customers
```
This workflow is the absolute backbone of modern DevOps! As you continue your learning, tools like Jenkins, Docker, Kubernetes, and AWS will fit naturally into different stages of this pipeline.


---
**[Next: Day 3 - Roles & Agile](./Day-03-Company-Roles-and-Agile.md)**
