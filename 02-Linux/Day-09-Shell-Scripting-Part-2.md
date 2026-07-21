# Day 9: Shell Scripting for DevOps - Part 2

Today we learned how DevOps engineers use Shell Scripting to automate Linux administration tasks, debug scripts, monitor system health, work with processes, search logs, handle errors, and write control flow statements such as `if` and `for` loops.

Shell scripting is one of the most important skills for a DevOps Engineer because many repetitive system administration tasks can be automated using Bash scripts.

---

## 1. Revision of Previous Class

The following Linux commands were revised:
- `df`
- `free`
- `nproc`
- `top`

### 1.1 `df` - Disk Filesystem
Displays information about disk partitions.
```bash
df
# A more readable version:
df -h
```
**Example Output:**
```
Filesystem      Size Used Avail Use% Mounted on
/dev/sda1       100G 40G   60G   40% /
```
**Why DevOps Engineers Use It:**
- Check available disk space
- Monitor storage usage
- Prevent servers from running out of disk space

### 1.2 `free`
Displays RAM and swap memory.
```bash
free
# Human readable:
free -h
# Display values in GB:
free -g
```
**Example Output:**
```
Mem: 7GB
Swap: 2GB
```
**Used for:**
- Memory monitoring
- Detecting memory leaks
- Capacity planning

### 1.3 `nproc`
Displays the number of CPU processing units available.
```bash
nproc
```
**Example Output:** `8` (The system has 8 logical CPUs).
**Useful for:**
- Performance tuning
- Deciding thread counts
- Parallel execution

### 1.4 `top`
Displays real-time system statistics.
```bash
top
```
**Shows:** CPU usage, RAM usage, Running processes, Process IDs (PIDs), Load average. One of the most frequently used monitoring commands in Linux.

---

## 2. Writing Your First Node Health Script

Create a script using `vim nodehealth.sh`:

```bash
#!/bin/bash

######################################### # Author      : Siva
# Date        : 21-01-2026
# Description : Node Health Check Script
# Version     : v1
######################################### df -h
free -g
nproc
```

### Shebang (`#!/bin/bash`)
This tells Linux to execute the script using the Bash shell. Without it, the OS may not know which interpreter to use.

### Script Metadata
Always include metadata at the top of your script. This helps other developers understand who wrote the script, its purpose, creation date, and version. In real companies, every production script includes metadata.

---

## 3. Making a Script Executable

By default, a script cannot be executed directly. Grant execute permission:
```bash
chmod 777 nodehealth.sh
```
Run it:
```bash
./nodehealth.sh
```
> **Note:** In real-world environments, avoid using `chmod 777` because it gives read, write, and execute permissions to everyone. A safer option is `chmod +x nodehealth.sh` which adds only the execute permission while keeping existing permissions intact.

---

## 4. Improving Output Using `echo`

Instead of printing raw command output, display meaningful messages.
```bash
echo "Disk Usage"
df -h

echo "Memory Usage"
free -g

echo "CPU Information"
nproc
```
Output becomes much easier to understand.

---

## 5. Common Script Error

Suppose you write:
```bash
echo "Print the CPU
```
Notice that the closing quotation mark (`"`) is missing. The shell continues looking for the matching quote and reports:
`unexpected EOF while looking for matching '"'`

**Correct Version:**
```bash
echo "Print the CPU"
```
Always ensure opening quotes, closing quotes, and matching brackets have proper syntax.

---

## 6. Debugging a Shell Script

Shell scripts may fail due to syntax or logic errors. To debug them, use `set -x`.

```bash
#!/bin/bash
set -x

echo "Disk"
df -h
echo "Memory"
free -g
```

**Output:**
```
+ echo Disk
Disk
+ df -h
...
+ echo Memory
Memory
+ free -g
...
```
The `+` symbol shows each command before it executes, making it easier to identify where the script fails.

---

## 7. Other Important Debugging Options

### `set -e`
Stops the script immediately if any command fails.
Without it, if Command 2 fails, Command 3 still runs. With `set -e`, the script stops immediately at Command 2. This prevents later commands from running when an earlier step has already failed.

### `set -o pipefail`
Normally, in a pipeline (`command1 | command2 | command3`), Bash reports only the exit status of the *last* command. 
With `set -o pipefail`, the entire pipeline fails if *any* command fails. This is recommended for production scripts.

### Best Practice
At the beginning of production Bash scripts, use:
```bash
#!/bin/bash

set -e
set -o pipefail
# set -x   # Enable only during debugging
```
Enable `set -x` while troubleshooting and comment it out once the script is stable.

---

## 8. Linux Processes

Every running program in Linux is called a process (e.g., Chrome, Docker, Jenkins, PostgreSQL, Nginx). Each process has a unique identifier called a Process ID (PID).

**Viewing Processes:**
- `ps`: Displays processes associated with the current shell.
- `ps -ef`: Displays all running processes with detailed information.

**Typical output:**
```
UID    PID   PPID  CMD
root   100     1   nginx
ubuntu 250   100   postgres
```

---

## 9. Searching Processes with `grep`

Suppose your manager asks: *"Find all PostgreSQL processes."*
Instead of scanning hundreds of lines manually, use:
```bash
ps -ef | grep postgres
```
**What is grep?** `grep` searches text for matching keywords (e.g., `grep nginx`, `grep docker`).

---

## 10. Pipe Operator (`|`)

The pipe (`|`) sends the output of one command as the input to another command.
```bash
ps -ef | grep postgres
```
**Flow:**
`ps -ef` (All Processes)  `|`  `grep postgres` (Only PostgreSQL Processes)
Pipes are used extensively in Linux and DevOps to combine commands.

---

## 11. Extracting Specific Columns with `awk`

Suppose you only need the Process IDs (PIDs).
```bash
ps -ef | grep postgres | awk '{print $2}'
```
**Example Output:**
```
347
375
376
```
**What is awk?**
`awk` is a powerful text-processing tool used to extract columns, filter text, format output, and generate reports. Here, `$2` means "print the second column."

---

## 12. Interview Question on Pipes

**Question:** `date | echo "Today is"` - What is the output?
Many people expect: `Today is Wed Jan 21`
**Actual output:** `Today is`

**Why?**
`echo` ignores its standard input and simply prints its own arguments. The output from `date` is discarded because `echo` does not read from the pipe.

---

## 13. Working with Log Files

Logs are extremely important in DevOps. When applications fail, engineers first examine the logs.
```bash
cat app.log
# Search for errors:
grep ERROR app.log
```

---

## 14. Using `curl`

`curl` is used to send HTTP requests to web servers and APIs.
```bash
curl https://example.com
# Search for errors in the response:
curl https://example.com | grep ERROR
# GET request:
curl -X GET https://api.food.com
```
**Common uses:** Calling REST APIs, Testing endpoints, Monitoring services, Downloading API responses.

---

## 15. `wget`

`wget` is used to download files from the internet.
```bash
wget https://example.com/file.zip
```

### Difference Between `curl` and `wget`

| Feature | `curl` | `wget` |
|---------|--------|--------|
| **Primary Use** | Sending HTTP requests, interacting with APIs | Downloading files |
| **Output** | Displays response to terminal by default | Saves files directly to disk |
| **Methods** | Supports many HTTP methods (GET, POST, PUT, DELETE) | Mainly supports downloading content |
| **Common Use** | API testing | Downloading software, packages, backups |

---

## 16. Finding Files

```bash
find / -name pam
```
**Meaning:** Search from the root directory (`/`) to find files or directories named `pam`.

---

## 17. Switching to Root User

Become the root user:
```bash
sudo su -
```
Root has full administrative privileges. Be cautious-incorrect commands can affect the entire system.

---

## 18. If Statement

**Syntax:**
```bash
if [ condition ]
then
    commands
else
    commands
fi
```
**Example:**
```bash
a=4
b=10

if [ "$a" -gt "$b" ]
then
    echo "a is greater than b"
else
    echo "b is greater than a"
fi
```
*Note: For numeric comparisons, use operators like `-gt`, `-lt`, `-eq`, etc., rather than `>` inside `[ ]`.*

---

## 19. For Loop

Used to execute a block of code repeatedly.

**Example 1:**
```bash
for i in {1..5}
do
    echo "$i"
done
```

**Example 2:**
```bash
for file in *.log
do
    echo "$file"
done
```
*(This processes every `.log` file in the current directory).*

---

## 20. Linux Signals

A signal is a notification sent to a process indicating that an event has occurred (e.g., stop, interrupt, reload, terminate).

**Killing a Process:**
```bash
kill -9 111
```
*(Send signal 9 `SIGKILL` to forcefully terminate process 111).*

**Ctrl + C:**
Pressing `Ctrl + C` sends the `SIGINT` signal to the currently running program, interrupting it.

---

## 21. Using `trap`

The `trap` command allows a shell script to catch and respond to signals.
```bash
trap 'echo "Don'\''t use Ctrl+C"' SIGINT
```
Now, if the user presses `Ctrl + C`, the script prints the message instead of immediately terminating. This is useful for cleanup operations, temporary file removal, or graceful shutdowns.

---

## Key Commands Learned

| Command | Purpose |
|---------|---------|
| `df -h` | Display disk usage |
| `free -g` | Display memory usage in GB |
| `nproc` | Show available CPU cores/logical processors |
| `top` | Real-time system monitoring |
| `chmod +x` | Make a script executable |
| `echo` | Print text to the terminal |
| `set -x` | Debug shell scripts |
| `set -e` | Exit on command failure |
| `set -o pipefail` | Fail a pipeline if any command fails |
| `ps -ef` | List all running processes |
| `grep` | Search text for a pattern |
| `awk` | Process and extract text columns |
| `curl` | Send HTTP/API requests |
| `wget` | Download files |
| `find` | Search for files and directories |
| `sudo su -` | Switch to the root user |
| `kill -9` | Forcefully terminate a process |
| `trap` | Handle Linux signals in shell scripts |

---

## Interview Questions

1. **What is `set -x` used for?**
   It enables debug mode by printing each command before it executes, making it easier to trace script execution.

2. **What is the purpose of `set -e`?**
   It causes the script to exit immediately if any command returns a non-zero (failure) exit status.

3. **Why do we use `set -o pipefail`?**
   It ensures that a pipeline is considered failed if any command in the pipeline fails, improving error detection.

4. **What is the difference between `ps` and `ps -ef`?**
   `ps` shows processes associated with the current terminal/session. `ps -ef` displays detailed information about all running processes on the system.

5. **What does the pipe (`|`) operator do?**
   It sends the output of one command as the input to another command, allowing commands to be chained together.

6. **What is `awk` used for?**
   `awk` is used for text processing, such as extracting columns, filtering records, formatting output, and generating reports.

7. **What is the difference between `curl` and `wget`?**
   `curl` is mainly used to send HTTP requests and interact with APIs. `wget` is mainly used to download files from the internet.

8. **What happens when you press Ctrl + C?**
   The terminal sends the `SIGINT` signal to the running process, requesting that it stop.

9. **What is a Process ID (PID)?**
   A PID is a unique number assigned by the operating system to every running process.

10. **Why are shell scripts important in DevOps?**
    Shell scripts automate repetitive tasks such as server health checks, deployments, log analysis, backups, process monitoring, and system administration, making infrastructure management faster, more reliable, and less error-prone.

---
**[Next: Day 10 - Advanced Linux](./Day-10-Advanced-Linux-for-DevOps.md)**

