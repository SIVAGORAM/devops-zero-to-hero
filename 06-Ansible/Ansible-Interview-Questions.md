# Ansible Interview Questions Bank

This document contains a comprehensive list of Ansible interview questions to help you prepare for Devops roles. Try to answer these based on the notes from Days 1 through 9!

---

## 🛠️ Ansible Basics
1. Why do we need Ansible?
2. Why is Ansible called agentless?
3. How can you connect to other devices within Ansible in a secured way?
4. What is the difference between Ansible and Terraform?
5. If you are very comfortable with Ansible, how would you convince me to shift from Ansible to Terraform?
6. Where do we store the host file in Ansible?
7. Explain the Ansible architecture, prerequisites, and required software.
8. What are the prerequisites for Ansible?
9. Why is Terraform in the market when Ansible is already available?
10. If the Ansible controller machine goes down, what will happen to the remote nodes? How will you take a backup of the Ansible controller machine?
11. Why do you use Ansible if you can do configuration management through Terraform? What are the advantages?
12. How do you connect to different servers in Ansible?
13. What activities have you performed using Ansible?
14. What are the main advantages and functionalities of Ansible?
15. What are the advantages of Ansible being idempotent?
16. What makes Ansible simple to use?
17. What are Ansible modules, and how do they make Ansible simple?
18. What are the Ansible configuration files required to take control of other machines?
19. How do you configure Ansible to manage multiple target machines?
20. What are Ansible handlers? Give one example where you have used them.
21. What is an Ansible controller?
22. What are Ansible handlers, and when and where would you use them?
23. What are all the activities you have done with respect to Ansible?
24. What are the main advantages of using Ansible in a project?
25. What are blocks used for in Ansible?
26. What is the "become" directive used for in Ansible?
27. How is Ansible different from other automation tools?
28. What kind of automation would you not do with Ansible, and why?
29. Explain the Ansible architecture and how it works in detail.
30. What is the mechanism used by Ansible?
31. What is the Ansible host file, and where is it located?
32. What information does the Ansible host file contain?
33. What are Ansible facts?
34. How do you get system information from a machine using Ansible?
35. You want to run a certain command if a task fails. How would you achieve that?
36. How do you handle errors in Ansible?
37. What functionality do you use with Ansible in your project, and what are the advantages of having Ansible in your project?
38. Why do you use Ansible for deployment when Jenkins can also perform automated deployments?
39. How would you get system information of a machine using Ansible, similar to facts in Puppet?
40. How do you manage secrets in Ansible?
41. What is Ansible Vault?

---

## 🧩 Ansible Roles
42. What are Ansible roles?
43. What is an Ansible role structure?
44. What is Ansible, and what roles have you created in your organization?
45. Explain the directory layout of an Ansible role.
46. Which Ansible best practices are you familiar with? Name at least three.
47. What is the difference between Ansible Playbooks and Roles?
48. What are the default files of an Ansible role?
49. What is Ansible Tower?
50. How do you create and use roles in Ansible?
51. How would you use a role to execute different tasks on target machines with different types of operating systems?

---

## 🗂️ Ansible Inventory
52. What is an inventory file in Ansible, and how do you define one?
53. What are inventory variables?
54. How are variables defined for a host in an inventory?
55. Who manages the inventory file, and which server is used?
56. What is a group in an Ansible inventory file?
57. What are the different types of inventory in Ansible?
58. What is the purpose of `/etc/ansible/hosts`?
59. What are `group_vars` and `host_vars`?
60. How do you group two inventory files in Ansible?
61. What is a dynamic inventory file?
62. When would you use a dynamic inventory?
63. Tell me a scenario where you used a dynamic inventory in Ansible.
64. What is an identical inventory file?

---

## 📦 Ansible Modules
65. What are Ansible modules?
66. What are the different modules you have worked with?
67. Which Ansible modules have you used in your project?

---

## 📖 Ansible Playbooks
68. What is an Ansible playbook?
69. What dependencies are required to run an Ansible playbook?
70. What are the basic requirements for writing an Ansible playbook?
71. How do you pass different parameters while running an Ansible playbook?
72. Describe the following Ansible components and explain the relationship between them: Task, Module, Play, Playbook, Role.
73. How do you run an Ansible playbook if the playbook is located in another directory or location?
74. How do you instantiate/install 10 packages at a time using an Ansible playbook?
75. Write an Ansible playbook to copy a file.
76. Write an Ansible playbook to install Apache.
77. Write an Ansible playbook to configure master and slave.
78. Write an Ansible playbook for Nginx.
79. Write a playbook to deploy the file `/tmp/system_info` on all hosts except the `controllers` group, with the given content.
80. Write a playbook to install `zlib` and `vim` on all hosts if the file `/tmp/mario` exists on the system.
81. Write a single Ansible task that verifies all the files in the `files_list` variable exist on the host.
82. What would be the result of running the given Ansible task? How would you fix it?
83. What would be the result of running the following play?
84. You have 10 modules in your playbook and want to deploy only 8 out of 10 to the target machine. How would you do that?
85. How do you install `httpd` on Linux and Apache on an Ubuntu machine using a single playbook?
86. Have you written any Ansible playbook to be used with Jenkins?
87. Write a playbook that calls a role which needs to execute different tasks on target machines with different types of operating systems.
88. What options are available in Ansible where the output of the playbook can be saved to a file?

---

## 🗃️ Ansible Variables
89. How do you pass a variable file to Ansible to deploy to different environments?
90. The variable `whoami` is defined in the following places: Role defaults, Extra vars passed to CLI, Host facts, Inventory variables. According to variable precedence, which value will be used?
91. What is `group_vars` in Ansible?
92. What are the default variables we can use in an Ansible playbook?
93. How can we pass variables in an Ansible playbook?
94. What are the different ways to pass variables to an Ansible playbook?
95. How do you manage variables for different environments in Ansible?

---

## 🔁 Ansible Loops and Conditionals
96. Demonstrate conditionals in Ansible.
97. Demonstrate loops in Ansible.
98. How do you use loops in an Ansible playbook?
99. How do you use conditionals in an Ansible playbook?

---

## 🧠 Scenario-Based Questions
100. Suppose you have 10 target machines and you run a playbook on all 10 machines. If the playbook fails on the 10th target machine, what will happen to the playbook execution on the other machines?
101. You run Ansible tests and get an "idempotence test failed" error. What does it mean?
102. Why is idempotence important in Ansible?
103. How do you test your Ansible-based projects?
104. What is Molecule in Ansible, and how does it work?
105. What are Ansible Collections?
106. What are filters in Ansible? Do you have experience writing filters?
107. Write an Ansible filter to capitalize a string.
108. You want to run a task only if the previous task changed something. How would you achieve that?
109. What are callback plugins in Ansible?
110. What can you achieve by using callback plugins?
111. What is `ansible-pull`?
112. How is `ansible-pull` different from `ansible-playbook`?
113. Explain the difference between Forks, Serial, and Throttle in Ansible.
114. What are facts in Ansible?
115. How do you see all the facts of a certain host?
116. How do you securely keep secret data in Ansible?

---

## 💻 Practical / Coding Questions
117. Write an Ansible task to create the directory `/tmp/new_directory`.
118. Write an Ansible playbook to launch an LDAP server.
119. How would you launch an LDAP server using Ansible?
120. Write an Ansible playbook to copy a file to a container.
121. Write an Ansible task/playbook to run Python.
122. Write an Ansible deployment file.
123. Write an Ansible playbook to install multiple packages at the same time.
124. Write a playbook to deploy `/tmp/system_info` to all hosts except the `controllers` group.
125. Write a playbook to install `zlib` and `vim` only when `/tmp/mario` exists.
126. Write a single task to verify that all files specified in `files_list` exist on the target host.
127. Write a playbook that installs `httpd` on Linux machines and Apache on Ubuntu machines using one playbook.
128. Write a playbook that calls different roles depending on the target operating system.
129. Write an Ansible playbook that deploys only selected tasks/modules from a larger playbook.
130. Write a task to execute a command only when a previous task has made a change.
131. Write an Ansible playbook using loops.
132. Write an Ansible playbook using conditionals.
133. Write an Ansible playbook using handlers.
134. Write an Ansible playbook using variables and variable files.
135. Write an Ansible playbook using `group_vars` and `host_vars`.

---

## 🔧 File / Variable / Filter Practical Questions
136. The file `/tmp/exercise` contains:
    ```text
    Goku = 9001
    Vegeta = 5200
    Trunks = 6000
    Gotenks = 32
    ```
    With one Ansible task, change the content to:
    ```text
    Goku = 9001
    Vegeta = 350
    Trunks = 40
    ```
    How would you achieve this?
137. How would you use an Ansible task to modify specific values in a file?
138. How would you use an Ansible filter to transform string data?
139. How would you use Ansible to manage sensitive data securely?

---

## 🚀 Advanced Ansible
140. What is Ansible Vault, and why is it used?
141. How do you encrypt and decrypt secrets using Ansible Vault?
142. What is the difference between `ansible-pull` and `ansible-playbook`?
143. What are callback plugins, and how do they work?
144. What are Ansible Collections, and why are they used?
145. What is Molecule, and why would you use it for Ansible testing?
146. What is idempotency in Ansible, and how do you ensure your playbooks are idempotent?
147. How does Ansible handle failures when running against multiple target machines?
148. How can you control the number of hosts on which an Ansible playbook runs simultaneously?
149. How can you save Ansible playbook execution output to a file?
150. How do you handle secrets and sensitive information in an Ansible project?

---

## 🏗️ Ansible Basics (Part 2 / CI-CD)
151. What is Ansible Vault?
152. Explain the difference between Forks, Serial, and Throttle in Ansible.
153. What are Ansible facts? How can you see all the facts of a particular host?
154. How do you securely keep secret data in Ansible?
155. What is Ansible Galaxy?
156. How do you execute shell scripts on worker nodes using an Ansible playbook?
157. How do you manage secrets in Ansible?
158. What is a namespace in Ansible?
159. Where have you used Ansible in CI/CD activities?
160. Suppose there are 4 application servers and 4 web servers. A new code change needs to be automatically copied to these different servers using Ansible. How would you detect that new code has been generated and deploy it to the servers?
161. How would you use Jenkins with Ansible to automatically deploy a newly generated artifact?
162. How would you configure Jenkins with the Poll SCM option to detect a new code change and trigger an Ansible deployment?
163. How would you deploy the generated artifact to multiple servers using the Ansible copy module?
164. In the above deployment scenario, why would you use `serial: 1`?
165. Have you implemented any self-healing automation where an application goes down and Ansible automatically brings it back up?
166. How would you write an Ansible playbook for self-healing an application such as Tomcat?
167. How would you ensure that the self-healing deployment happens one server at a time using `serial: 1`?
