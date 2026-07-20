# Day 2: SDLC & Pipeline Basics - Interview Questions

Here are simple, conversational answers for foundational SDLC and Pipeline concepts to help you ace your interviews.

---

### Q1: What is SDLC?
**Interview Answer:**  
"SDLC stands for Software Development Life Cycle. It is the structured, step-by-step process that development teams use to plan, design, build, test, and deploy software. As a DevOps engineer, my goal is to automate the 'build, test, and deploy' phases of this lifecycle to make software delivery as fast and safe as possible."

---

### Q2: Why is SDLC important?
**Interview Answer:**  
"Without SDLC, building software is like building a house without a blueprint—it leads to chaos, delays, and bugs. SDLC provides a clear roadmap. It ensures quality and reduces risks so that the final product actually meets the customer's needs."

---

### Q3: Which SDLC phases involve a DevOps Engineer the most?
**Interview Answer:**  
"While DevOps culture encourages collaboration across the entire lifecycle, my technical daily work is heavily focused on the Build, Testing, Deployment, and Maintenance (Monitoring) phases. I build the CI/CD pipelines that connect these phases automatically so developers can focus purely on writing code."

---

### Q4: What is Git and how is it different from GitHub?
**Interview Answer:**  
"Git is the actual version control software that runs locally on my computer. It tracks changes to the code and allows me to undo mistakes. GitHub, on the other hand, is a cloud platform that hosts those Git repositories on the internet, allowing multiple developers to collaborate, share code, and trigger automated pipelines."

---

### Q5: What is Version Control?
**Interview Answer:**  
"Version control is a system that records changes to a file or set of files over time. In a team environment, it prevents developers from overwriting each other's work. More importantly, it acts as a 'save point' so we can easily roll back to a working version if a new feature accidentally breaks the application in production."

---

### Q6: What is a Build?
**Interview Answer:**  
"A build is the process of taking the raw source code written by developers and converting it into a final, runnable application. This often involves compiling code, downloading dependencies, and packaging everything together. In DevOps, I automate this entire process using CI tools like Jenkins or GitHub Actions so nobody has to build code manually."

---

### Q7: What is Continuous Integration (CI)?
**Interview Answer:**  
"Continuous Integration is a practice where every time a developer pushes new code to a central repository like GitHub, an automated pipeline immediately builds the code and runs tests against it. This ensures that bugs are caught instantly, keeping the main codebase clean and stable at all times."

---

### Q8: What is Agile and how does it relate to DevOps?
**Interview Answer:**  
"Agile is a software development methodology that focuses on delivering software in small, rapid iterations rather than one massive release. While Agile dramatically sped up the *development* process, it caused a bottleneck in *operations* because manual deployments couldn't keep up. DevOps was born to solve this bottleneck by automating deployment and testing, allowing Operations to keep pace with Agile Development."

---

### Q9: What is the difference between a Monolith and Microservices?
**Interview Answer:**  
"A monolithic application is built as a single, unified codebase—if one small component fails, the entire application can crash. Microservices architecture breaks the application down into small, independent services communicating via APIs. As a DevOps engineer, microservices are crucial because they allow us to deploy, scale, and update individual parts of the application independently using container tools like Docker and Kubernetes."

---

### Q10: What is the difference between Continuous Delivery and Continuous Deployment?
**Interview Answer:**  
"Both represent the 'CD' in CI/CD. Continuous Delivery means the code is automatically built, tested, and prepared for release, but a human must manually click 'approve' to send it to the live production environment. Continuous Deployment means there is no human intervention at all—if the code passes all automated tests, it deploys straight to production. Because of the high risk, most enterprise companies stick to Continuous Delivery."


---
**[⬅️ Previous: Day 1 - DevOps Basics Questions](./00-Introduction-Questions.md)** | **[➡️ Next: Day 3 - Roles & Agile Questions](./Day-03-Roles-Questions.md)**
