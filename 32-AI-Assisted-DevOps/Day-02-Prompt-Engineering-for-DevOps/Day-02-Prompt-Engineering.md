# Day 02: Prompt Engineering Masterclass for DevOps 🗣️

> **Goal:** By the end of this Day 2 lesson, you should understand how to communicate with AI/LLMs effectively and use prompt engineering to generate better Bash scripts, Kubernetes YAML, Terraform, CI/CD configurations, regex, troubleshooting steps, documentation, and DevOps automation.

---

## 📚 Table of Contents
1. What is Prompt Engineering?
2. How a Prompt Works
3. Why Prompt Engineering Matters for DevOps
4. Anatomy of a Good Prompt
5. Context
6. Instructions
7. Examples
8. Output Format
9. Zero-Shot Prompting
10. Few-Shot Prompting
11. Few-Shot Example
12. Few-Shot Prompting for DevOps
13. Multi-Shot / N-Shot Prompting
14. Chain-of-Thought Prompting
15. CoT DevOps Example
16. Zero-Shot vs Few-Shot vs Multi-Shot vs CoT
17. Tokens
18. Token Efficiency
19. Temperature
20. Max Tokens
21. Prompt Quality and Cost
22. DevOps Prompt Engineering
23. Bad Prompt vs Good Prompt
24. A Strong DevOps Prompt Structure
25. Practical 1 — Kubernetes Manifest
26. Practical 2 — Bash Script Generation
27. Improving the Bash Prompt
28. Why the Improved Prompt Is Better
29. Practical 3 — Few-Shot DevOps Prompt
30. Practical 4 — Kubernetes Troubleshooting
31. Practical 5 — Terraform
32. Practical 6 — CI/CD
33. Prompt Engineering for Regex
34. Prompt Engineering for Bash Debugging
35. Prompt Engineering for Logs
36. Prompt Engineering for Incident Management
37. Prompt Engineering for Kubernetes YAML
38. Organizational Prompting Standards
39. Prompting as an Organizational Interface
40. Prompt Iteration
41. A Simple Rule
42. Prompt Engineering Framework
43. Reusable DevOps Prompt Templates
44. DevOps Prompt Template — Troubleshooting
45. DevOps Prompt Template — Code Generation
46. DevOps Prompt Template — Code Review
47. DevOps Prompt Template — Kubernetes
48. DevOps Prompt Template — Terraform
49. DevOps Prompt Template — CI/CD
50. Practical Exercise — Compare Prompt Quality
51. The Most Important Prompting Lesson
52. Day 2 Mini Challenge
53. Day 2 Practical Workflow
54. Prompt Engineering Best Practices
55. The Golden Prompt Formula
56. Day 2 — Master Mental Model
57. Interview Questions
58. Advanced DevOps Prompting Concepts
59. Final Cheat Sheet

---

## 1. What is Prompt Engineering?
Prompt engineering is the practice of designing clear, precise and structured instructions for an AI model so that it produces the desired output.

In simple terms:
`Better Prompt ↓ Better Context ↓ Better AI Understanding ↓ Better Output`

Instead of simply asking:
> Create Kubernetes deployment.

we provide enough information for the AI to understand exactly what we want:
> Generate only a Kubernetes Deployment manifest.
> 
> Requirements:
> - Application: nginx
> - Replicas: 3
> - Container port: 80
> - Image: nginx:1.27
> - Do not include explanations.
> - Do not include kubectl commands.
> - Return only valid YAML.

The second prompt gives the AI much stronger instructions.

---

## 2. How a Prompt Works
The basic flow is:
```text
                INPUT
                  │
                  ▼
             ┌─────────┐
             │  PROMPT │
             └────┬────┘
                  │
                  ▼
             ┌─────────┐
             │AI / LLM │
             └────┬────┘
                  │
                  ▼
               OUTPUT
```

The objective is:
`Prompt → LLM → Desired Output`

The quality of the prompt strongly influences how useful the output is.

---

## 3. Why Prompt Engineering Matters for DevOps
As a DevOps engineer, you frequently work with: Linux, Bash, Python, Docker, Kubernetes, Terraform, Ansible, Jenkins, GitHub Actions, AWS, Azure, GCP, Monitoring, Logs, Networking, CI/CD, Infrastructure as Code.

AI can assist with many of these tasks.
`Human ↓ Prompt ↓ LLM ↓ Bash Script`
or
`DevOps Requirement ↓ Prompt ↓ LLM ↓ Kubernetes YAML`
or
`Incident ↓ Logs + Metrics ↓ Prompt ↓ LLM ↓ Possible Root Cause ↓ Suggested Remediation`

Therefore, knowing how to communicate requirements to an AI model becomes an important DevOps skill.

---

## 4. Anatomy of a Good Prompt
A strong prompt generally contains four important components:
1. Context
2. Instructions
3. Examples
4. Output Format

Think of it as:
```text
┌───────────────────────┐
│       CONTEXT         │
├───────────────────────┤
│     INSTRUCTIONS      │
├───────────────────────┤
│       EXAMPLES        │
├───────────────────────┤
│     OUTPUT FORMAT     │
└───────────────────────┘
```
Not every prompt requires all four, but understanding them allows you to construct much better prompts.

---

## 5. Context
Context tells the AI what situation it is working in.

Without Context:
> Check the health of the machine.

With Context:
> I am a DevOps engineer managing Ubuntu virtual machines. I need a Bash script to check CPU, memory and disk utilization.

DevOps Context Example:
> I am working as a DevOps engineer.
> Environment:
> - Ubuntu 24.04
> - Docker
> - Kubernetes
> - AWS EC2
> - Bash
> 
> I need to troubleshoot a Kubernetes application.

Now the AI knows the environment in which the solution should operate.

---

## 6. Instructions
Instructions tell the AI what exactly it should do.

Example:
> Generate a Bash script that checks CPU, memory and disk utilization.

You can make the instruction more precise:
> Generate a Bash script that:
> 1. Checks CPU utilization.
> 2. Checks memory utilization.
> 3. Checks root disk utilization.
> 4. Determines whether the VM is healthy.
> 5. Supports an "explain" command-line argument.

The second version removes ambiguity.

---

## 7. Examples
Examples are extremely useful when you want the AI to follow a particular pattern.

Suppose your organization has a standard Bash script format:
```bash
#!/bin/bash
######
# Author: Siva Goram
# Version: v1
# Date: 2026-09-12
######
docker --version
```

Now you want a script to retrieve the Terraform version.
Provide the example first, then ask:
> Now create a Bash script to fetch the Terraform version using the same format.

The AI can infer your preferred structure from the example.

---

## 8. Output Format
This is one of the most important parts of prompt engineering. Sometimes the AI gives you too much information.

Prompt:
> Generate Kubernetes deployment resources.

The AI might return: Explanation, Architecture, Deployment YAML, Service YAML, Commands, Troubleshooting, Additional recommendations. But perhaps you only need YAML.

So specify:
> Generate only the Kubernetes Deployment manifest.
> Do not provide: Explanation, kubectl commands, Troubleshooting, Additional resources.
> Return only valid YAML.

Now the output is much more controlled.

---

## 9. Zero-Shot Prompting
Zero-shot prompting means asking the AI to perform a task without providing examples.
`Prompt ↓ LLM ↓ Output`

**Example:**
> Generate a Kubernetes Deployment manifest for nginx with 3 replicas.

When Should You Use Zero-Shot?
When the task is familiar, straightforward, and the expected format is standard. You don't need an organizational-specific style.

---

## 10. Few-Shot Prompting
Few-shot prompting means giving the AI a small number of examples before asking it to perform a new task.

The structure is:
`Example 1 -> Example 2 -> Example 3 ↓ New Task ↓ LLM ↓ Output following the pattern`
This is especially useful when you want the model to follow a specific style or format.

---

## 11. Few-Shot Example
Suppose we want names in a specific format.

> Example 1: Create a random name which starts with B.
> Answer: Random name for alphabet B is Batman.
>
> Example 2: Create a random name which starts with S.
> Answer: Random name for alphabet S is Superman.
>
> Now: Create a random name which starts with A.

The AI infers the desired structure:
> Random name for alphabet A is Aquaman.

---

## 12. Few-Shot Prompting for DevOps
This is where few-shot prompting becomes very useful. Suppose your organization follows a standard Bash script format.

> Example 1: Fetch the Docker version.
> Expected output: (Standard script header + docker --version)
>
> Example 2: Fetch the Terraform version.
> Expected output: (Standard script header + terraform --version)
>
> New Task: Fetch the versions of all processes installed on an Ubuntu virtual machine.
> Follow exactly the same scripting and documentation style shown in the examples. Return only the Bash script.

---

## 13. Multi-Shot / N-Shot Prompting
Multi-shot prompting is an extension of few-shot prompting. Instead of giving only a couple of examples, you provide multiple examples and more context.

The more examples you provide, the more information the model has about the desired pattern.

**DevOps Example:**
Provide examples of your company's Deployment, Service, ConfigMap, Secret, Ingress, HPA, then ask:
> Create a new Kubernetes application manifest following the same conventions.

---

## 14. Chain-of-Thought Prompting
Chain-of-Thought (CoT) prompting is a technique intended to improve performance on complex reasoning tasks by encouraging the model to work through a problem systematically.

Basic idea:
`Problem ↓ Reasoning / Analysis ↓ Conclusion`

For DevOps, this can be useful for: Troubleshooting, Root cause analysis, Debugging, Architecture decisions, Complex failures, Dependency analysis.

---

## 15. CoT DevOps Example

Suppose:
> My Kubernetes pod is in CrashLoopBackOff. Help me troubleshoot it step-by-step.
> Start by identifying what information I should collect, then explain how to interpret the results, and finally provide likely remediation steps.

A useful response may guide you through checking pod status, logs, describe pod, events, probes, image config, identify root cause, and apply remediation.

---

## 16. Zero-Shot vs Few-Shot vs Multi-Shot vs CoT
| Technique | Examples | Best Use |
|-----------|----------|----------|
| Zero-Shot | 0 | Simple/familiar tasks |
| Few-Shot | Few | Specific output style |
| Multi-Shot | Many | Complex organizational patterns |
| CoT | Reasoning-oriented | Complex troubleshooting/reasoning |

---

## 17. Tokens
A token is a unit of text processed by an AI model. A token is not necessarily equal to one word.

Why Do DevOps Engineers Care About Tokens?
Because AI APIs commonly charge based partly on the amount of text processed.
`Input tokens + Output tokens ↓ Total token usage`

More tokens → potentially higher cost.
Fewer tokens → potentially lower cost.

---

## 18. Token Efficiency
Suppose you send:
> Please kindly provide me with a very detailed and comprehensive explanation of Kubernetes Deployment resources including all possible details...

When all you actually need is:
> Generate only a Kubernetes Deployment manifest for nginx with 3 replicas. Return only YAML.

The second prompt is more efficient. This is one reason good prompt engineering can reduce unnecessary AI usage.

---

## 19. Temperature
Temperature controls the degree of randomness/variation in model output.
- **Low temperature:** More predictable / consistent output (Preferable for generating production configuration).
- **High temperature:** More variation / creativity (Preferable for brainstorming).

---

## 20. Max Tokens
Max tokens controls the maximum amount of output the model can generate, depending on the API/model interface.
- Small output requirement ↓ Lower output limit
- Large architecture/documentation requirement ↓ Higher output limit

Do not confuse Input tokens with Output token limit.

---

## 21. Prompt Quality and Cost
In an organization, AI usage can become significant when many engineers use AI every day.
`100 engineers ↓ 1000 AI requests/day ↓ Large number of tokens ↓ Significant AI infrastructure/API cost`

Therefore, organizations benefit from efficient prompting. A good prompt should be: Clear, Specific, Concise, Context-aware, Structured, Output-controlled.

---

## 22. DevOps Prompt Engineering
Now we apply prompt engineering to actual DevOps work.
Common AI-assisted DevOps tasks include: Bash, Python, Docker, Kubernetes, Terraform, Ansible, Jenkins, GitHub Actions, AWS, CI/CD, Monitoring, Logging, Troubleshooting, Regex, Documentation.

---

## 23. Bad Prompt vs Good Prompt
**Example — Kubernetes**
❌ Bad Prompt:
> Create Kubernetes deployment.

✅ Better Prompt:
> Generate a Kubernetes Deployment manifest.
> Requirements: Application nginx, Image nginx:1.27, Replicas 3, Container port 80.
> Return only valid YAML. Do not include explanations or kubectl commands.

---

## 24. A Strong DevOps Prompt Structure
Use this structure:
`ROLE ↓ CONTEXT ↓ TASK / INSTRUCTION ↓ REQUIREMENTS ↓ CONSTRAINTS ↓ EXAMPLES ↓ OUTPUT FORMAT`

---

## 25. Practical 1 — Kubernetes Manifest
Direct / zero-shot prompt:
> Generate only a Kubernetes Deployment manifest for nginx.
> Requirements: Image nginx:1.27, Replicas 3, Container port 80.
> Do not provide: Explanation, kubectl commands, Service, Ingress, Troubleshooting.
> Return only valid YAML.

---

## 26. Practical 2 — Bash Script Generation
From the Day 1 practical screenshot:
> Create a shell script where the script should analyze the health of the virtual machine based on cpu, memory and disk space... Target virtual machines are always ubuntu.

---

## 27. Improving the Bash Prompt
We can make that prompt more structured:
> You are an experienced Linux and DevOps engineer.
> Context: The target virtual machine is always Ubuntu.
> Task: Create a Bash script that checks the health of the virtual machine.
> The script must check: 1. CPU utilization 2. Memory utilization 3. Root disk utilization
> Health rule: If all below 60%, report Healthy. If any 60%+, report Not healthy.
> Command-line behavior: "explain" argument displays detailed resource usage and reason.
> Requirements: Bash, Ubuntu compatible, reliable commands.
> Output: Return only the complete Bash script.

---

## 28. Why the Improved Prompt Is Better
We added:
- Context (Ubuntu)
- Task (What to build)
- Rules (Health condition is unambiguous)
- Command-line behavior ("explain" defined)
- Requirements (Constrained implementation)
- Output (No unnecessary explanation)

---

## 29. Practical 3 — Few-Shot DevOps Prompt
Provide examples of your company's standard Bash script headers (Author, Version, Date) and then ask it to generate a new script using the same formatting and documentation style.

---

## 30. Practical 4 — Kubernetes Troubleshooting
❌ Weak Prompt: My Kubernetes pod is crashing. Fix it.
✅ Better Prompt (CoT):
> You are an experienced Kubernetes DevOps engineer. My application pod is in CrashLoopBackOff. Help me troubleshoot it step-by-step. Provide: 1. Commands to collect information. 2. What each command checks. 3. What common outputs mean. 4. Possible root causes. 5. Recommended remediation. Do not assume the root cause.

---

## 31. Practical 5 — Terraform
❌ Poor Prompt: Create Terraform for AWS.
✅ Better Prompt:
> You are an experienced Terraform and AWS engineer. Generate Terraform configuration for an AWS S3 bucket. Requirements: Use Terraform, Create one S3 bucket, Enable versioning, Add meaningful tags, Do not include unnecessary resources, Use variables where appropriate. Output: Return only the Terraform files. Separate each file using a filename heading.

---

## 32. Practical 6 — CI/CD
❌ Poor Prompt: Create GitHub Actions pipeline.
✅ Better Prompt:
> You are a DevOps engineer specializing in CI/CD. Create a GitHub Actions workflow for a Python application. Pipeline requirements: Trigger on push to main, Ubuntu runner, Checkout repo, Setup Python, Install dependencies, Run tests, Build application. Requirements: Use YAML, keep it simple, fail pipeline if tests fail. Output: Return only the workflow YAML.

---

## 33. Prompt Engineering for Regex
❌ Bad Prompt: Create regex for email.
✅ Better Prompt:
> Generate a regular expression that validates a basic email address. Requirements: username before @, domain after @, domain must contain a dot, Do not attempt to support every RFC edge case. Output: 1. Regex 2. Three valid examples 3. Three invalid examples.

---

## 34. Prompt Engineering for Bash Debugging
Provide the failing script and ask the AI to analyze the problem.
> Analyze the problem. Provide: 1. Likely cause 2. Commands to verify 3. Corrected script 4. Security considerations. Do not recommend disabling Linux security controls as the first solution.

---

## 35. Prompt Engineering for Logs
> You are an experienced SRE. Analyze the following application logs. Tasks: 1. Identify errors 2. Group similar errors 3. Identify most likely root cause 4. Identify affected components 5. Recommend investigation steps 6. Suggest remediation. Important: Do not claim certainty when logs do not provide enough evidence.

---

## 36. Prompt Engineering for Incident Management
Provide available information (CPU metrics, memory metrics, logs, LB metrics, K8s events).
> Analyze the provided information. Return: 1. Incident Summary 2. Observed Symptoms 3. Evidence 4. Possible Root Causes 5. Most Likely Cause 6. Verification Steps 7. Recommended Remediation 8. Risks of the Remediation. Do not invent missing information. Clearly distinguish facts from assumptions.

---

## 37. Prompt Engineering for Kubernetes YAML
Specify exactly what should be included (replicas, ports, requests/limits, probes, strategies) and what should NOT be included (No Service, No Ingress, No ConfigMap, No explanations).

---

## 38. Organizational Prompting Standards
An AI model may not automatically know your organization's internal conventions. Therefore, provide examples of your coding standards, naming conventions, and file structure using few-shot prompting.

---

## 39. Prompting as an Organizational Interface
Think of AI as another engineer joining your team. Tell it who you are, what environment you have, the task, the rules, and the output format.
`Organizational Standards + Prompt ↓ LLM ↓ Standardized Output`

---

## 40. Prompt Iteration
Prompt engineering is often iterative.
`Prompt v1 ↓ Output ↓ Identify Problems ↓ Improve Prompt ↓ Prompt v2 ↓ Better Output`

---

## 41. A Simple Rule
Don't ask AI to guess requirements that you already know. If you know you want Ubuntu, 3 replicas, port 8080, only YAML, and no explanation—put those requirements directly into the prompt.

---

## 42. Prompt Engineering Framework
1. DEFINE THE CONTEXT
2. DEFINE THE TASK
3. ADD REQUIREMENTS
4. ADD CONSTRAINTS
5. ADD EXAMPLES
6. DEFINE OUTPUT FORMAT

---

## 43. Reusable DevOps Prompt Template
> You are an experienced DevOps engineer.
> 
> Context: [Describe my environment]
> Task: [Describe exactly what I want]
> Requirements: [Requirement 1, 2, 3]
> Constraints: [Constraint 1, 2]
> Examples: [Provide examples if required]
> Expected output: [Explain exactly what the AI should return]
> Output restrictions: [Only code / Do not include unnecessary info]

---

## 44. DevOps Prompt Template — Troubleshooting
Provide environment, problem, observed behavior (paste error). Request possible causes, verification steps, safe remediation, potential impact, and commands. 
*Important: Do not assume facts that are not provided.*

---

## 45. DevOps Prompt Template — Code Generation
Provide task, environment, requirements, security requirements, and constraints.
*Output: Return only the required code. Before generating: Check that the code satisfies every requirement.*

---

## 46. DevOps Prompt Template — Code Review
Provide the code and request analysis on Correctness, Security, Reliability, Performance, Maintainability, Error handling, and DevOps best practices.
For each issue provide Severity, Problem, Why it matters, Recommended fix.

---

## 47. DevOps Prompt Template — Kubernetes
Provide Application, Image, Replicas, Port, Resource limits, Probes.
*Output: Return only the Kubernetes manifest. Do not include explanations or kubectl commands.*

---

## 48. DevOps Prompt Template — Terraform
Provide Cloud environment, infrastructure task, and requirements.
*Terraform requirements: Use variables, clean structure, no hardcoded sensitive values, meaningful names.*

---

## 49. DevOps Prompt Template — CI/CD
Provide Platform, Application, Pipeline requirements (Checkout, install, tests, build).
*Requirements: Fail when tests fail, keep secrets outside source code.*

---

## 50. Practical Exercise — Compare Prompt Quality
Prompt 1: "Create a Dockerfile."
Prompt 2: "Create a production-oriented Dockerfile for a Python FastAPI application. Requirements: Python 3.12, run using uvicorn, expose port 8000, non-root user. Return only the Dockerfile."

Prompt 2 is better because it contains Context, Task, Requirements, Security constraint, and Output format.

---

## 51. The Most Important Prompting Lesson
Don't think: `AI → Give me the answer`
Think: `AI ↑ Precise instructions ↑ Context ↑ Requirements ↑ Examples ↑ Output format`

---

## 52. Day 2 Mini Challenge
Create a zero-shot prompt for the Ubuntu VM health checker. Improve the prompt by adding context, requirements, constraints, and output format. Convert it to a few-shot prompt by providing an organizational standard format. Compare the outputs.

---

## 53. Day 2 Practical Workflow
`Understand Problem ↓ Build Prompt (Context, Requirements, Examples, Output Format) ↓ LLM ↓ Review Output ↓ Validate/Test ↓ Deploy`
Never blindly copy AI-generated infrastructure code into production.

---

## 54. Prompt Engineering Best Practices
1. Be Specific
2. Give Context
3. Define Constraints
4. Give Examples
5. Define Output Format
6. Don't Ask for Unnecessary Information
7. Iterate
8. Validate AI Output

---

## 55. The Golden Prompt Formula
`CONTEXT + INSTRUCTION + REQUIREMENTS + CONSTRAINTS + EXAMPLES + OUTPUT FORMAT = HIGH-QUALITY PROMPT`

---

## 56. Day 2 — Master Mental Model
                  PROMPT
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
    Context      Instructions    Examples
       │             │             │
       └─────────────┼─────────────┘
                     ▼
               Output Format
                     │
                     ▼
                    LLM
                     │
                     ▼
              Desired Output

---

## 57. Interview Questions
**Q1. What is prompt engineering?**
Prompt engineering is the practice of designing clear and structured instructions for an AI model to obtain a desired output.

**Q2. What is zero-shot prompting?**
Asking the model to perform a task without providing examples.

**Q3. What is few-shot prompting?**
Providing a small number of examples before asking the model to perform a new task.

**Q4. What is multi-shot prompting?**
Providing multiple examples and context to help the model learn a desired pattern.

**Q5. What is Chain-of-Thought prompting?**
A technique that encourages systematic reasoning on complex tasks (like troubleshooting or RCA).

**Q6. Why are examples useful?**
Examples show the AI exactly how the desired output should look.

**Q7. Why is output format important?**
Because it prevents unnecessary output (e.g., "Return only YAML").

**Q8. What are tokens?**
Tokens are units of text processed by an AI model. API usage and pricing can depend on token consumption.

**Q9. What is temperature?**
Temperature controls the randomness/variation of model output.

**Q10. What is max tokens?**
It specifies the maximum amount of output the model can generate.

**Q11. Why should DevOps engineers care about prompt engineering?**
Because AI can assist with Bash, Python, K8s, Terraform, Docker, CI/CD, RCA, etc. Better prompts produce more useful and controllable results.

---

## 58. Advanced DevOps Prompting Concepts (Beyond the Basics)

While the fundamentals cover 90% of day-to-day tasks, modern AI-Assisted DevOps Engineers must also master these advanced concepts:

### 1. Data Security and Secret Masking
**Never paste sensitive data into a public LLM.** 
Before pasting logs or configurations into a prompt, you must sanitize:
- AWS Access Keys & Secret Keys
- Database Passwords
- Private IP addresses or internal domain names (if highly sensitive)
- Personally Identifiable Information (PII) of users in logs.
**Tip:** Use placeholders like `<AWS_ACCOUNT_ID>` or `<REDACTED_PASSWORD>` before hitting send.

### 2. System Prompts (Custom Instructions)
Many AI coding tools (like GitHub Copilot, Cursor, or ChatGPT Custom Instructions) allow you to set a "System Prompt." This is a global context that runs invisibly before every prompt you send.
**Example DevOps System Prompt:**
> "You are a Senior SRE. Always write Terraform using the AWS Provider v5.0+. Always use Bash over Python for simple automation. Never suggest `chmod 777`."

### 3. Structured Data Generation (JSON/YAML)
Often, you need the AI to generate data that a script can parse (like using `jq`).
**Prompt Addition:** 
> "Output the results STRICTLY as a valid JSON array of strings. Do not include markdown formatting or backticks. My script needs to pipe this output directly into `jq`."

### 4. Self-Correction Prompting
If the AI generates a script and it fails, don't write a new prompt from scratch. Feed the error directly back into the same conversation context.
**Example:** 
> "The Bash script you generated threw this error on line 12: `unary operator expected`. Analyze why this failed in an Ubuntu 24.04 environment and provide the corrected script."

### 5. Retrieval-Augmented Generation (RAG) Awareness
AI models have a training cutoff date. If you ask about a tool released yesterday (like a brand new AWS service or a new Terraform provider feature), it will hallucinate.
**Solution:** Copy the specific section of the new official documentation and paste it at the top of your prompt.
> "Context: Here is the official documentation for the new AWS API: `<PASTE DOCS>`. Based ONLY on this documentation, write a Bash script to..."

---

## 59. Final Cheat Sheet

### Four Important Components
1. Context
2. Instructions
3. Examples
4. Output Format

### Prompting Techniques
- **Zero-Shot:** No examples
- **Few-Shot:** Few examples
- **Multi-Shot / N-Shot:** Multiple examples
- **CoT:** Systematic reasoning for complex tasks

### Important Model Concepts
Tokens, Temperature, Max Tokens.

### Golden Rule
Don't say: "Create something."
Say: "You are [ROLE]. Context: [ENVIRONMENT]. Task: [WHAT TO DO]. Requirements: [WHAT MUST BE INCLUDED]. Constraints: [WHAT MUST NOT HAPPEN]. Examples: [REFERENCE]. Output: [EXACT FORMAT]"
