# Day 8: Shell Scripting Basics - Interview Questions

These questions test your understanding of how Linux interprets and executes scripts, as well as file permissions.

---

### Q1: Why do we use Shell Scripting in DevOps?
**Interview Answer:**  
"In DevOps, we often manage hundreds or thousands of servers. Doing administrative tasks manually-like creating users, installing software, rotating logs, or monitoring CPU usage-is inefficient and prone to human error. Shell scripting allows us to automate these repetitive tasks by writing a sequence of commands in a file that the operating system executes automatically, ensuring speed and consistency."

---

### Q2: What is a 'Shebang' and why is it important in a shell script?
**Interview Answer:**  
"The Shebang, written as `#!` followed by an absolute path (like `#!/bin/bash`), is placed on the very first line of a script. It tells the Linux operating system which interpreter it should use to parse and execute the rest of the file. Without a shebang, the system might try to execute the script using a default shell that doesn't support the syntax used in the script, leading to unexpected errors."

---

### Q3: What is the difference between `#!/bin/sh` and `#!/bin/bash`?
**Interview Answer:**  
"`#!/bin/bash` specifically invokes the Bourne Again Shell (Bash), which is the industry standard for DevOps and supports advanced scripting features like arrays, loops, and custom functions. `#!/bin/sh` invokes the default POSIX-compliant shell on the system. While `sh` is more portable across different UNIX platforms, it lacks many of the advanced programming features that Bash provides."

---

### Q4: You wrote a shell script named `deploy.sh`. When you try to run it using `./deploy.sh`, you get a "Permission Denied" error. Why did this happen and how do you fix it?
**Interview Answer:**  
"By default, when you create a new file in Linux, it is not granted 'execute' permissions for security reasons. The operating system blocks the file from running as a program. To fix this, I need to use the `chmod` command to add execute permissions. Typically, I would run `chmod +x deploy.sh` or use numerical values like `chmod 755 deploy.sh` to allow the owner to read, write, and execute the file."

---

### Q5: Explain what the command `chmod 777` does, and why it is dangerous in production.
**Interview Answer:**  
"In Linux permissions, 4 stands for Read, 2 for Write, and 1 for Execute. A 7 means the user has Read, Write, and Execute permissions (4+2+1). The three digits in `777` represent the Owner, the Group, and Others. Therefore, `chmod 777` grants full read, write, and execute permissions to literally everyone on the system. This is a massive security vulnerability in production, as any unauthorized user could modify or execute malicious code within that file."

---

### Q6: What is the correct syntax for declaring and using a variable in a Bash shell script, and what is a common beginner mistake?
**Interview Answer:**  
"In Bash, you declare a variable by writing the name, an equals sign, and the value, making absolutely sure there are **no spaces** around the equals sign (for example: `APP_ENV="production"`). To use or reference that variable later, you prepend it with a dollar sign, such as `echo "Deploying to $APP_ENV"`. A very common beginner mistake is putting spaces around the equals sign (`APP_ENV = "production"`), which causes Bash to throw an error because it mistakenly thinks `APP_ENV` is a command."

---

### Q7: How do you pass external arguments to a shell script and access them inside the script?
**Interview Answer:**  
"You pass arguments to a shell script by typing them separated by spaces after the script name when executing it, such as `./deploy.sh production`. Inside the script, you access these arguments using special positional parameters: `$1` for the first argument, `$2` for the second, and so on. The variable `$0` holds the name of the script itself, and `$@` represents all the arguments that were passed."

---

### Q8: What is Command Substitution in a shell script and how is it written?
**Interview Answer:**  
"Command substitution allows you to execute a Linux command and capture its standard output so it can be used as a value-usually to store inside a variable. The modern syntax is to wrap the command inside `$()`. For example, `CURRENT_DATE=$(date)` will execute the `date` command and store the resulting output string directly into the `CURRENT_DATE` variable."

---

### Q9: How do you save the output of a shell script to a file instead of displaying it on the terminal?
**Interview Answer:**  
"To save the output of a script to a file, you use I/O (Input/Output) redirection. Using a single bracket `>` will redirect the standard output to a file and completely overwrite any existing contents. Using double brackets `>>` will append the standard output to the end of the file. For example, running `./deploy.sh >> deployment.log` is commonly used to maintain a continuous, historical log of script executions without losing previous data."

---

### Q10: You wrote a shell script to back up a database. How do you ensure it runs completely automatically every night at 2 AM?
**Interview Answer:**  
"To automate the execution of a script on a schedule, I would use a Linux Cron Job. By running the `crontab -e` command, I can add a scheduled task using the standard 5-field cron syntax (Minute, Hour, Day, Month, Day of Week). To run a script daily at exactly 2 AM, I would add the line `0 2 * * * /path/to/backup.sh`. The cron daemon runs silently in the background and will execute the script perfectly on schedule without any manual intervention."


---

### Q11: What is `set -x` used for in a shell script?
**Interview Answer:**  
"It enables debug mode. When a script runs with `set -x`, it prints each command and its expanded arguments to the terminal before executing it. This makes it much easier to trace the script's execution flow and identify exactly where it might be failing."

---

### Q12: What is the purpose of the `set -e` command?
**Interview Answer:**  
"By default, if a command inside a shell script fails, the script will just continue executing the next commands. `set -e` changes this behavior so that the script exits immediately if any command returns a non-zero (failure) exit status. This is critical in production to prevent a script from executing further steps when an earlier, foundational step has already failed."

---

### Q13: Why is `set -o pipefail` recommended for production scripts?
**Interview Answer:**  
"In a standard bash pipeline (e.g., `cmd1 | cmd2`), bash only returns the exit status of the very last command. If `cmd1` fails but `cmd2` succeeds, the pipeline is considered successful. Adding `set -o pipefail` ensures that the entire pipeline fails if *any* command within it fails, dramatically improving error detection."

---

### Q14: What is the difference between the `ps` and `ps -ef` commands?
**Interview Answer:**  
"`ps` on its own only shows the processes associated with the current terminal session or user. `ps -ef`, on the other hand, displays a detailed, full-format list of all running processes across the entire system, making it essential for system-wide monitoring."

---

### Q15: How does the pipe (`|`) operator work in Linux?
**Interview Answer:**  
"The pipe operator takes the standard output of the command on its left and sends it directly as the standard input to the command on its right. This allows us to chain simple commands together to perform complex tasks, such as `ps -ef | grep postgres`."

---

### Q16: What is the `awk` command primarily used for?
**Interview Answer:**  
"`awk` is a powerful text-processing tool. In DevOps, we frequently use it to extract specific columns from structured text output, filter records, or format data. For example, `awk '{print $2}'` easily extracts the second column (like a Process ID) from a line of text."

---

### Q17: What is the key difference between `curl` and `wget`?
**Interview Answer:**  
"While both can transfer data over the network, `curl` is primarily designed for sending HTTP requests (like GET or POST) and interacting with REST APIs, outputting the response to the terminal by default. `wget` is primarily designed for downloading files directly to disk."

---

### Q18: What actually happens under the hood when you press `Ctrl + C` in a terminal?
**Interview Answer:**  
"Pressing `Ctrl + C` sends a `SIGINT` (Signal Interrupt) signal to the currently running foreground process. This tells the operating system to interrupt and gracefully stop the process."

---

### Q19: What is a Process ID (PID) and why is it important?
**Interview Answer:**  
"A PID is a unique numerical identifier assigned by the Linux kernel to every active process. It is important because if we need to manage a process-such as monitoring its resource usage with `top` or forcefully terminating it with a `kill -9` command-we must reference it by its PID."

---

### Q20: How can you intercept signals like `Ctrl + C` inside a shell script to perform cleanup before exiting?
**Interview Answer:**  
"You can use the `trap` command. By defining a trap (e.g., `trap 'rm -rf /tmp/files' SIGINT`), you can instruct the script to catch specific signals and execute a command or function (like cleaning up temporary files) before the script actually terminates."

---
**[Previous: Day 7 - Linux Questions](./Day-07-Linux-Questions.md)**
