# Day 7: Linux Basics & System Monitoring - Interview Questions

These questions test your understanding of Linux architecture and essential troubleshooting commands.

---

### Q1: Why is Linux preferred over Windows in DevOps and Cloud environments?
**Interview Answer:**  
"Linux is preferred because it is free, open-source, and highly secure. Unlike Windows, which relies heavily on a resource-intensive Graphical User Interface (GUI), Linux is typically run as a lightweight Command Line Interface (CLI). This makes Linux incredibly fast, highly stable for long-running servers, and perfectly suited for shell scripting and automation, which is the core of DevOps."

---

### Q2: What is the Linux Kernel?
**Interview Answer:**  
"The Linux Kernel is the absolute core of the operating system. It acts as the bridge between the software applications and the physical hardware. It is responsible for critical tasks like memory management, CPU scheduling, process management, and device drivers."

---

### Q3: What is a Shell (like Bash)?
**Interview Answer:**  
"A Shell is a command-line interpreter. It provides the user interface for Linux. When a user types a command like `ls` into the terminal, the Shell (such as Bash) takes that command, interprets it, and passes it to the Linux Kernel to execute. Bash stands for Bourne Again Shell and is the standard shell for most Linux distributions."

---

### Q4: If a production server is running slowly, what commands would you use to troubleshoot it?
**Interview Answer:**  
"To diagnose a slow server, I would start by running `top` to get a real-time view of system performance, checking for any specific processes consuming too much CPU or memory. Then, I would use `free -g` to check if we are running out of RAM, and `df -h` to ensure the hard drive isn't full, as a full disk can severely impact server performance."

---

### Q5: What is the difference between `rm` and `rm -r`?
**Interview Answer:**  
"The `rm` command is used to delete individual files. However, it cannot delete directories. To delete a directory and all of the files and subdirectories inside it, you must use `rm -r`, which stands for recursive remove. It is a powerful command that should be used carefully, as Linux does not have a 'Recycle Bin' by default."
