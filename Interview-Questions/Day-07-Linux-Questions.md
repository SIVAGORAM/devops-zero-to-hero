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

---

### Q6: How do you view the most recent errors in a massive 50GB log file without crashing the server?
**Interview Answer:**  
"You should never open a massive log file using a text editor like `vi` or `nano` because it will try to load the entire file into RAM, which will severely impact or crash the server. Instead, I use the `tail` command, specifically `tail -n 100 /var/log/syslog` to view only the last 100 lines. I can also use `tail -f` to 'follow' the live output of the log, or use `grep "error" /var/log/syslog` to instantly search the entire file for specific error messages."

---

### Q7: What is the purpose of the `chmod` and `chown` commands in Linux?
**Interview Answer:**  
"In Linux, file security is based on ownership and permissions. `chown` (Change Owner) is used to change which user and group officially owns a file or directory. `chmod` (Change Mode) is used to modify the read, write, and execute (rwx) permissions of that file for the owner, the group, and everyone else. A classic example is running `chmod 600` on an SSH private key to ensure only the owner can read it."

---

### Q8: What is the `sudo` command and why is it necessary?
**Interview Answer:**  
"The `sudo` command stands for 'Super User Do'. It allows a standard user to execute a command with administrative (root) privileges. In Linux, regular users are restricted from modifying system configurations or installing global software to prevent accidental or malicious damage. Whenever I need to perform administrative tasks, like editing a configuration file in the `/etc` directory, I must prefix my command with `sudo`."

---

### Q9: How do you install software on a Linux server without a graphical interface?
**Interview Answer:**  
"In Linux, software is installed using command-line Package Managers that fetch software from official, secure repositories. The tool you use depends on the Linux distribution. If I am working on an Ubuntu or Debian server, I use the `apt` package manager (for example, `sudo apt install docker`). If I am managing an Amazon Linux or Red Hat server, I use the `yum` package manager."


---
**[Next: Day 8 - Shell Scripting Questions](./Day-08-Shell-Scripting-Questions.md)**
