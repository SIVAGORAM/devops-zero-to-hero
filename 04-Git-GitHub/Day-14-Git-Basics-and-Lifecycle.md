# Day 14: Version Control & Git Basics

Welcome to the Git & GitHub module! In the real world, multiple developers work on the same application simultaneously. We need a way to share, merge, and track every single modification made to the code over time. This is the job of a Version Control System (VCS).

---

## 1. What is Version Control?

A Version Control System records changes to a file or set of files over time so that you can recall specific versions later. 

### Centralized vs Distributed Systems

In the past, tools like **CVS** and **SVN** were popular. They are **Centralized Version Control Systems (CVCS)**.
- **How it works:** There is one central server containing all versioned files. Developers check out files from that central place.
- **The Problem:** If the central server goes down for an hour, nobody can collaborate or save versioned changes. If the central hard disk corrupts, you lose everything.

Today, **Git** is the industry standard. Git is a **Distributed Version Control System (DVCS)**.
- **How it works:** Every developer's computer doesn't just check out the latest snapshot of the files; they fully mirror the entire repository (including its full history). 
- **The Benefit:** If the server dies, any client repository can be copied back up to the server to restore it. You can commit, branch, and view history completely offline!

---

## 2. Git vs GitHub

- **Git** is the tool/software installed on your local computer. It manages versions locally using the CLI.
- **GitHub** is a cloud-hosted service (a website). It acts as the remote distributed server where developers upload their local Git repositories to collaborate with others.

---

## 3. The `.git` Folder (How Git works internally)

When you turn a standard folder into a Git repository, Git creates a hidden directory called `.git`.

```bash
mkdir calculator-app
cd calculator-app
git init
```

The `git init` command initializes a completely new, empty repository. If you type `ls -a`, you will see the `.git` folder. 
**Crucial:** This `.git` folder is the brain of your repository. Everything is tracked as objects inside this folder. If you delete `.git`, your code remains, but all your version history is instantly destroyed.

---

## 4. The Git Lifecycle & Essential Commands

Git has three main states that your files can reside in:
1. **Working Directory:** The actual files you see and edit on your computer.
2. **Staging Area:** A pre-commit holding area. You gather the changes you want to include in your next commit here.
3. **Local Repository (.git):** The database where Git permanently stores the committed snapshots.

### Practical Workflow

**1. Check the Status**
```bash
git status
```
Shows you which files are untracked (new), modified, or staged ready for commit.

**2. View what changed**
```bash
git diff
```
Shows the exact line-by-line differences between the code right now and the last commit.

**3. Stage the files**
```bash
git add .
```
The `.` means "add all files in the current directory." This moves files from the Working Directory into the Staging Area.

**4. Commit the snapshot**
```bash
git commit -m "this is my first version"
```
This takes everything in the Staging Area and permanently saves it in the `.git` database with a unique ID (a SHA-1 hash) and a message.

**5. View History**
```bash
git log
```
Shows all your past commits, their IDs, who made them, and when.

**6. Time Travel (Undoing)**
If you make a terrible mistake and want to permanently erase recent commits and go back to a specific past version:
```bash
git log  # (Copy the commit ID you want to go back to)
git reset --hard <commit-id>
```
*Warning: `--hard` destroys all uncommitted changes in your working directory!*

---
**[Previous: Day 13 - Networking Security](../03-Networking/Day-13-Networking-Security-and-Cloud.md)** | **[Next: Day 15 - GitHub & Collaboration](./Day-15-GitHub-and-Collaboration.md)**
