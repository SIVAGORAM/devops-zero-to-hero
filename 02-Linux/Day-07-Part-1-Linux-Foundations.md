# Day 7 (Part 1): 🚀 DevOps Foundations – OS, Linux & Basic Commands

> These notes are written from the perspective of a **senior DevOps engineer & trainer**, focusing on **real-world understanding**, not just theory.  
> If you master these basics properly, your DevOps journey will become smooth and powerful.

---

## ðŸŒ Languages & Communication Basics

### English
- Primary language used in **IT, DevOps, documentation, tools, and cloud platforms**.
- Almost all error messages, logs, manuals, and forums are in English.

### Malayalam
- A spoken language (not used in DevOps tools).
- Learning English technical terms is essential for career growth.

### Interpreter
- An **interpreter** executes code **line by line**.
- Example: Python, Bash.
- Helps in quick debugging and scripting (very important for DevOps).

---

## 🖥️ What is an Operating System (OS)?

An **Operating System** is a bridge between:
- **User**
- **Hardware**
- **Applications**

### Responsibilities of an OS:
- Process management
- Memory management
- File system management
- Network handling
- Security & permissions

---

## 🪟 GUI vs CLI

### GUI (Graphical User Interface)
- Uses mouse, icons, windows.
- Example: Windows desktop, folders, buttons.
- Easy for beginners, **not efficient for servers**.

### CLI (Command Line Interface)
- Uses commands.
- Faster, scriptable, automation-friendly.
- **100% required for DevOps & servers**.

👉 DevOps engineers **live inside CLI**.

---

## ðŸ§ Linux vs Windows

### Windows
- Mostly used on **personal laptops**.
- Heavy GUI.
- Licensed (paid).

### Linux
- Mostly used on **servers**.
- Lightweight.
- Secure.
- Highly customizable.
- Free and open-source.

---

## ðŸ§ What is Linux?

Linux is:
- An **open-source operating system**.
- **Free for lifetime**.
- Maintained by:
  - Community (free versions)
  - Companies (paid versions with support)

---

## 📦 Linux Distributions (Distros)

Linux comes in different **distributions** based on use-case.

### Popular Linux Distros:
- **Ubuntu**
- **CentOS**
- **Red Hat Enterprise Linux (RHEL)**
- **SUSE**

### Why so many distros?
- Different companies & communities customize Linux for:
  - Servers
  - Security
  - Enterprise
  - Cloud

---

## 💰 Free vs Paid Linux

### Free Linux
- Community-managed.
- No official support.
- Example: Ubuntu, CentOS Stream.

### Paid Linux
- Enterprise-level support.
- SLA (Service Level Agreement).
- Certified & stable.

### Example:
- **Red Hat** provides paid Linux support.
- If a production server fails â†’ **you contact Red Hat**.

---

## ðŸ¢ Why Companies Use Linux for Servers?

### 1ï¸âƒ£ Stability
- Servers run **24/7 without restart**.

### 2ï¸âƒ£ Performance
- Uses less memory and CPU.

### 3ï¸âƒ£ Security
- Strong permission model.
- Fewer viruses.

### 4ï¸âƒ£ Automation Friendly
- Perfect for scripting (Bash, Shell).

### 5ï¸âƒ£ Cost Effective
- No OS license cost.

👉 **Linux = Backbone of Internet**

---

## 🔴 Why Choose Red Hat (RHEL)?

- Enterprise-grade OS.
- Certified with:
  - AWS
  - Azure
  - Google Cloud
  - Kubernetes
- Professional support.
- Used by banks, MNCs, production servers.

👉 **Most DevOps jobs expect Red Hat/Linux skills**

---

## ⚡ Linux = Power of Servers

- Websites
- Cloud platforms
- Containers (Docker)
- Kubernetes clusters
- CI/CD pipelines

👉 If you know Linux deeply â†’ **you control servers**

---

## 🧰 Git Bash

### What is Git Bash?
- A Linux-like terminal for Windows.
- Used to practice:
  - Linux commands
  - Git
  - Bash scripting

👉 Download and install **Git Bash** on Windows to practice Linux commands.

---

## ðŸ“ Linux Basic Commands (Must-Know)

### 📂 Create Directory
```bash
mkdir Linux
mkdir ubuntu centos abc
```
- `mkdir` â†’ make directory.
- Can create multiple folders at once.

### âŒ Remove Directory
```bash
rmdir abc
```
- Removes empty directory only.
- If directory contains files â†’ âŒ will fail.
- ðŸ’¡ *In real servers, deleting directories must be done carefully to avoid data loss.*

### 📄 Create File
```bash
touch abc.txt
```
- Creates an empty file.
- Commonly used to create config files, logs, scripts.

Create multiple files:
```bash
touch file1.txt file2.txt file3.txt
```
- Very useful for automation & scripting.

### ðŸ—‘ï¸ Remove File
```bash
rm abc.txt
```
- Deletes file permanently.
- No recycle bin in Linux CLI.
- âš ï¸ **Warning:** `rm` is dangerous on servers. One wrong command can delete production data. Careful: `rm` deletes permanently.

### ðŸ“ƒ List Files & Directories
```bash
ls
```
- Shows files and folders inside current directory.

Detailed list:
```bash
ls -l
```
Shows:
- Permissions (who can read/write/execute)
- Owner
- File size
- Date & time
- File/Directory name

ðŸ’¡ *DevOps engineers rely heavily on `ls -l` to check permissions and ownership issues.*

### 📂 Navigation Commands

**Change Directory:**
```bash
cd Linux
```
- Moves into Linux directory.

**Go Back One Directory:**
```bash
cd ..
```
- Moves one level up. Extremely common while navigating servers.

**Present Working Directory:**
```bash
pwd
```
- Displays current location in the file system.
- Helps avoid mistakes when running commands.

### ðŸ§¹ Clear the Terminal Screen
```bash
clear
```
Shortcut: `Ctrl + L`
- Keeps terminal clean. Improves focus while working.

---

## 🎯 DevOps Mentor Advice (Very Important)

- Donâ€™t rush Linux.
- Practice commands daily.
- Understand **WHY**, not just **HOW**.
- Linux basics â†’ Shell scripting â†’ Git â†’ CI/CD â†’ Cloud â†’ Kubernetes.

👉 **Strong Linux = Strong DevOps Engineer**

---
**[➡️ Next: Day 7 (Part 2) - Linux Fundamentals](./Day-07-Part-2-Linux-Fundamentals.md)**

