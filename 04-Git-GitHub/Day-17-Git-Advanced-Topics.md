# Day 17: Advanced Git Concepts & Troubleshooting

As a DevOps engineer, you won't just be committing code; you will be rescuing broken repositories, resolving conflicts, and managing secrets. Today we cover the advanced tools you need to troubleshoot Git.

---

## 1. The `.gitignore` File

You should never commit everything in your directory. Things like compiled binaries, temporary logs, and **passwords/API keys** must be kept out of version control.

- **How it works:** You create a file named exactly `.gitignore` in the root of your repository.
- Inside it, you list the files or folders you want Git to completely ignore.

**Example `.gitignore`:**
```text
# Ignore log files
*.log

# Ignore Node.js dependencies
node_modules/

# CRITICAL: Ignore environment variables and secrets!
.env
```
*DevOps Rule:* If you accidentally commit an AWS Access Key to a public GitHub repo, bots will find it in seconds and start mining cryptocurrency on your AWS account. Always use `.gitignore`.

---

## 2. Resolving Merge Conflicts

A **Merge Conflict** happens when two developers edit the *exact same line* of the *exact same file*, and Git doesn't know whose changes to keep.

**How to resolve it:**
1. Git will pause the merge and output a CONFLICT warning.
2. If you open the conflicting file, Git inserts markers:
```text
<<<<<<< HEAD
sum=$(( $1 + $2 ))
=======
sum=$(( $a + $b ))
>>>>>>> feature/new-math
```
3. You manually delete the markers (`<<<<<<<`, `=======`, `>>>>>>>`) and keep only the code you actually want.
4. Run `git add <file>` and `git commit` to finalize the merge.

---

## 3. Git Stash (Temporary Saves)

Imagine you are halfway through writing a new feature, but suddenly your manager asks you to fix a critical bug on the `main` branch. Your current code is broken, so you can't commit it yet. 

- **`git stash`:** Takes all your uncommitted changes and "hides" them in a temporary clipboard, returning your working directory to a clean state.
- Now you can switch branches, fix the bug, and come back.
- **`git stash pop`:** Takes the hidden changes out of the clipboard and applies them back to your working directory so you can finish your work.

---

## 4. Undoing Mistakes: Revert vs Reset

We learned `git reset --hard` earlier, but there are safer ways to undo mistakes.

### Git Reset
- Alters the commit history. It moves the branch pointer backward, effectively erasing commits as if they never happened.
- **Danger:** Never `git reset` commits that have already been pushed to GitHub. If other developers have pulled those commits, resetting them will cause massive conflicts.

### Git Revert
- Does **not** alter history. Instead, it creates a *brand new commit* that does the exact opposite of the target commit (e.g., if the old commit added a line, the revert commit deletes that line).
- **Safe:** Because it moves forward in history, it is 100% safe to use on public branches.

---

## 5. Fetch vs Pull

When you want to get the latest code from GitHub:

- **`git fetch`:** Downloads the latest commits and branches from GitHub into your local `.git` database, but it *does not* merge them into your working files. It lets you safely inspect what changed.
- **`git pull`:** Does a `git fetch` AND automatically runs a `git merge` to apply the changes to your actual working directory.

---

## Git Module Complete!
You have now finished the entire Git & GitHub syllabus. You are ready to manage source code like a senior DevOps engineer!

---
**[Previous: Day 16 - Advanced Branching](./Day-16-Advanced-Git-Branching-and-Merging.md)** | **[Next: Module 05 - AWS Cloud](../05-AWS/Day-05-AWS-EC2-Basics.md)**
