# Day 7 (Part 3): Linux Operating System & Basics of Shell Scripting

In DevOps, 80-90% of servers run Linux. Today we cover what Linux actually is, its architecture, and the fundamental commands you will use every day as a DevOps engineer.

---

## 1. What is an Operating System (OS)?

An Operating System is the system software that manages a computer's hardware and provides a platform for applications to run. Without it, applications (like Python or Jenkins) cannot communicate with the hardware (CPU, RAM).

**Architecture Flow:**
`Application Software " Operating System " Hardware (CPU/RAM)`

### Why Linux is Used in DevOps (Linux vs Windows)
Almost every major cloud provider (AWS, Azure, GCP) uses Linux for hosting applications. 
- **Open Source & Free:** No expensive enterprise licenses.
- **Secure & Stable:** Rarely requires reboots, highly resistant to viruses.
- **CLI-First:** Mostly driven by the Command Line Interface (CLI), making it lightweight and perfect for automation. Windows is GUI-first (Graphical User Interface).

---

## 2. Linux Architecture

Linux is composed of multiple layers:

1. **User Applications:** Docker, Jenkins, Python.
2. **Shell (Bash, Zsh):** The command interpreter. It takes commands typed by the user and translates them for the OS.
3. **System Libraries (libc):** Reusable functions that applications use to interact with the OS without talking to the Kernel directly.
4. **Linux Kernel:** The absolute heart of the OS. It manages CPU scheduling, memory, process management, and talks directly to the hardware.
5. **Hardware:** CPU, RAM, Disk, Network.

### What are Linux Distributions?
Since Linux is open-source, different companies package the Linux Kernel with different tools to create their own "version" of Linux. These are called **Distributions** (or Distros).
- *Popular DevOps Distros:* Ubuntu, Amazon Linux, CentOS, Red Hat Enterprise Linux (RHEL).

---

## 3. Basic Linux Commands

Once you SSH into an EC2 instance, you must use the CLI. Here are the essentials:

### Navigation & Files
- `pwd`: **Print Working Directory.** Shows exactly where you are in the system (e.g., `/home/ubuntu`).
- `ls`: **List.** Lists all files and folders in your current directory.
- `ls -ltr`: Lists files with detailed information (permissions, owner, size, date).
- `cd <folder>`: **Change Directory.** Moves you into a folder.
- `cd ..`: Moves you *up* one directory.
- `touch <filename>`: Creates a new empty file.
- `mkdir <folder>`: **Make Directory.** Creates a new folder.
- `rm <filename>`: Deletes a file.
- `rm -r <folder>`: Recursively deletes a folder and everything inside it. *(Warning: Cannot be undone).*

### The Vi Editor (`vi`)
The default text editor in Linux.
1. Type `vi filename` to open the file.
2. Press `i` to enter **Insert Mode** (so you can type).
3. Type your text.
4. Press `Esc` to exit Insert Mode.
5. Type `:wq` and press `Enter` to **Write (save)** and **Quit**.

### Viewing & Searching Files (Crucial for Logs)
When an application crashes, you shouldn't open massive log files in `vi` (loading a 10GB log file into an editor will crash the server). Instead, use these commands:
- `cat <filename>`: Prints the entire contents of a file to the screen.
- `tail -n 50 <filename>`: Prints only the last 50 lines of a file (perfect for seeing the most recent errors). Use `tail -f` to watch the file update live.
- `grep "error" <filename>`: Searches inside a file and prints only the lines containing the specific word "error".

### File Permissions (`chmod` & `chown`)
In Linux, security is entirely based on **Permissions** (Read `r`, Write `w`, Execute `x`) and **Ownership** (User, Group).
- `chmod`: **Change Mode.** Used to change the `rwx` permissions of a file. (Example: In Day 6, we used `chmod 600 key.pem` to make our SSH key readable *only* by the owner).
- `chown`: **Change Owner.** Changes which user and group owns the file.

### Installing Software & Root Access (`sudo`, `apt`)
In Windows, you install software by downloading a `.exe` file. In Linux, you use a **Package Manager** directly from the terminal to download software from official repositories.
- **Ubuntu/Debian:** Uses the `apt` package manager.
- **Amazon Linux/CentOS:** Uses the `yum` package manager.

**The `sudo` Command (Super User Do):**
Regular users are intentionally blocked from installing software or modifying system files to prevent accidental damage. To run a command with full administrative (Root) privileges, you must type `sudo` in front of it.
```bash
# Update the package list
sudo apt update

# Install Nginx web server
sudo apt install nginx -y
```

---

## 4. System Monitoring Commands (Interview Favorites)

If a server is crashing, a DevOps engineer runs these commands immediately:

- `top`: Displays real-time system performance (running processes, CPU usage, memory, uptime). Press `q` to exit.
- `free -g`: Displays memory (RAM) usage in Gigabytes (Total, Used, Free).
- `nproc`: Displays the number of available CPU processing units (cores).
- `df -h`: Displays disk space usage in human-readable format (Gigabytes).

---

## 5. Common Linux Directory Structure

Linux does not have a "C: Drive". Everything starts at the Root `/`.

- `/bin`: Essential user commands (like `ls` and `pwd`).
- `/etc`: Configuration files for the system and applications.
- `/home`: User directories (e.g., `/home/ubuntu`).
- `/var`: Variable data, primarily **Log files** (`/var/log`).
- `/tmp`: Temporary files that are deleted on reboot.
- `/opt`: Optional software installed by the user.

---

## Day 7 Summary
The **Linux Kernel** manages hardware, while the **Shell (Bash)** allows us to interact with the Kernel using commands. DevOps engineers rely heavily on the **CLI** to navigate directories, edit files with `vi`, and monitor system health using `top`, `free`, and `df`.

---
**[Next: Day 8 - Shell Scripting](./Day-08-Shell-Scripting-Basics.md)**

