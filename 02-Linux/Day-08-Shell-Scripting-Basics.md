# Day 8: Shell Scripting Zero to Hero (Part 1)

In Day 7, we learned basic Linux commands. Today, we learn how to chain those commands together to create **Shell Scripts**, the foundation of DevOps automation.

---

## 1. Manual Work vs Automation

**Manual Work:**
Your manager asks you to create a file. You type `touch file.txt`. 
*Problem:* What if your manager asks you to create 1,000 files, install software on 1,000 servers, and check the CPU usage of all of them? Typing commands one by one is impossible, slow, and error-prone.

**Automation (Shell Scripting):**
Instead of executing commands repeatedly, we write a text file containing a sequence of Linux commands. The computer executes all the commands in the file automatically, saving time, effort, and cost.

---

## 2. What is a Shell Script?

A Shell Script is simply a text file containing a list of commands. Think of it as a recipe. Instead of telling the computer every single step manually every day, you write the recipe once, and the computer cooks it perfectly every time.

### Creating Your First Script
1. Create a file with a `.sh` extension:
   ```bash
   touch first-script.sh
   ```
   *(Note: Linux doesn't actually care about file extensions, but `.sh` is the industry standard so engineers know it's a script).*

2. Edit the file using `vi first-script.sh` and add commands.

---

## 3. The "Shebang" (`#!/bin/bash`)

The very first line of almost every shell script is called the **Shebang**.
```bash
#!/bin/bash
```
The shebang tells Linux exactly *which* interpreter should be used to read the file. 

### Common Shebangs:
- `#!/bin/bash`: Uses the **Bourne Again Shell (Bash)**. This is the industry standard for DevOps. It supports advanced features like arrays, loops, and functions.
- `#!/bin/sh`: Uses the system's default POSIX shell. Often used for maximum portability across older UNIX systems.
- `#!/bin/dash`: A highly lightweight, incredibly fast shell used by Ubuntu for fast system startups.

*(Note: On many modern Linux systems, `/bin/sh` is actually just a **symbolic link** (a shortcut) pointing to `/bin/dash` or `/bin/bash`).*

---

## 4. Executing a Script & "Permission Denied"

There are two ways to execute a shell script:

**Method 1 (Passing file to the interpreter):**
```bash
sh first-script.sh
```
This works immediately, because the `sh` program is just reading your text file as input.

**Method 2 (Executing the file directly - Industry Standard):**
```bash
./first-script.sh
```
If you try this immediately, Linux will throw an error: `-bash: ./first-script.sh: Permission denied`.

### Why "Permission Denied"?
Linux is a highly secure operating system. By default, when you create a text file, Linux assumes it is just text. It intentionally blocks the file from running as a program to prevent viruses.

### The Fix: `chmod` (Change Mode)
To tell Linux "This file is safe, allow it to execute as a program," you must change its permissions.

Linux permissions are represented by numbers:
- **4** = Read (`r`)
- **2** = Write (`w`)
- **1** = Execute (`x`)

Permissions are given to three groups: **Owner | Group | Others**.

To give the Owner, Group, and Others full Read (4) + Write (2) + Execute (1) access (4+2+1 = 7), you run:
```bash
chmod 777 first-script.sh
```
Now, if you run `./first-script.sh`, it will execute perfectly!
*(Warning: `chmod 777` is a security risk in production because it gives everyone full access. In the real world, you typically use `chmod 755`).*

---

## 5. Comments, Echo, and Variables

Before writing full scripts, you must know three foundational concepts:

### Comments (`#`)
Any line starting with a `#` (except the shebang) is completely ignored by the computer. DevOps engineers use comments to explain what a complex script is doing so other engineers can understand it.
```bash
# This script installs the Nginx web server
```

### Echo
The `echo` command prints text to the screen. It is crucial for providing feedback so the user knows what the script is currently doing.
```bash
echo "Starting system update..."
```

### Variables
Variables are used to store data so you can reuse it later in the script.
```bash
# Define a variable (CRITICAL: There must be NO SPACES around the equals sign!)
USER_NAME="Siva"
ENVIRONMENT="Production"

# Use the variable by placing a $ in front of it
echo "Hello $USER_NAME, deploying to $ENVIRONMENT"
```

### Command Line Arguments (`$1`, `$2`)
If you want to pass data into your script when you execute it (e.g., `./script.sh Siva`), you use special built-in positional variables:
- `$0`: The name of the script itself.
- `$1`, `$2`: The first and second arguments passed to the script.
- `$@`: All arguments passed to the script.
```bash
# Example: If you run `./script.sh Production`
echo "Deploying the application to the $1 environment..."
```

### Command Substitution (`$()`)
If you want to run a Linux command and save its exact output into a variable, you wrap the command in `$()`. This is called Command Substitution.
```bash
# Save the output of the 'date' command into a variable
CURRENT_DATE=$(date)
echo "The script was executed on: $CURRENT_DATE"
```

### Output Redirection (`>` and `>>`)
When you run a script, the output prints to your screen. In DevOps, we usually want to save that output into a log file so we can review it later.
- `>` (Overwrite): Writes the output to a file. If the file already exists, it completely overwrites it.
- `>>` (Append): Adds the output to the end of a file without deleting the old data.
```bash
# Append the output of the script to a log file
./script.sh >> /var/log/my-script.log
```

---

## 6. Automating Scripts with Cron Jobs

You wrote a shell script and it works perfectly. But if you have to manually type `./script.sh` every single day at 2 AM, it is not truly automated!

To run scripts on an automatic schedule, Linux uses a built-in time-based job scheduler called **Cron**.
- You configure it by typing `crontab -e` in the terminal.
- A Cron expression uses 5 asterisks `* * * * *` representing (Minute, Hour, Day of Month, Month, Day of Week).

```bash
# Example: Run the backup script every day exactly at 2:00 AM
0 2 * * * /home/ubuntu/backup-script.sh
```
This is the ultimate goal of shell scripting: Write the code once, schedule it with Cron, and let the server do the work forever.

---

## 7. Example: A Real Shell Script

Let's write a script that creates a folder, moves into it, and creates two files.

```bash
#!/bin/bash

# Announce what we are doing
echo "Creating the application directory..."

# Create a folder
mkdir my-app

# Move into the folder
cd my-app

# Create two files
touch index.html style.css
```

---

## 🎯 Day 8 Summary
Shell scripting is how DevOps engineers manage fleets of thousands of virtual machines. You create a `.sh` file, declare the interpreter using a **Shebang** (`#!/bin/bash`), grant the file execute permissions using **`chmod`**, and execute it directly using `./script.sh`.


---
**[⬅️ Previous: Day 7 - Linux Basics](./Day-07-Linux-Basics.md)**
