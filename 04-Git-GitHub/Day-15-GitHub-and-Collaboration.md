# Day 15: GitHub, SSH & Collaboration

Yesterday we learned how to version code locally. Today we learn how to share it using GitHub.

---

## 1. Creating and Pushing to a Remote Repository

To share your code, you need a remote distributed system like GitHub, Bitbucket, or GitLab.

1. Go to github.com and log in.
2. Click **New Repository**.
3. Give it a name (e.g., `calculator-app`) and description.
4. Choose **Public** (anyone can see it) or **Private** (only you and invited collaborators can see it).
5. Click **Create Repository**.

### Linking Local to Remote
Your local `calculator-app` has no idea GitHub exists. You must link them:
```bash
git remote add origin <github-repo-url>
git push -u origin main
```
This pushes your local `.git` history up to GitHub.

---

## 2. Authentication: HTTPS vs SSH

When you interact with GitHub from your CLI, GitHub needs to know who you are.

### HTTPS Method
Uses your GitHub username and a Personal Access Token (PAT). You run `git clone https://github.com/...` and it prompts you for credentials.

### SSH Method (The DevOps Standard)
SSH uses cryptography to silently authenticate you without typing a password every time.

**How to set up SSH for GitHub:**
1. Generate the Public/Private Key pair on your computer:
```bash
ssh-keygen -t rsa -b 4096
```
*(Press Enter for all defaults to save it in `~/.ssh/id_rsa`)*

2. View your Public Key:
```bash
cat ~/.ssh/id_rsa.pub
```
3. Copy the entire output.
4. Go to **GitHub Settings** -> **SSH and GPG keys** -> **New SSH key**.
5. Paste the key and save. Now you can use `git clone git@github.com...` and push seamlessly!

---

## 3. Clone vs Fork

As a DevOps engineer, you will often need to download existing codebases. There are two distinct ways to do this:

### Git Clone
- Downloads a direct copy of a repository to your local machine.
- If it is your company's private repo, you clone it, make a branch, and push directly back to it.

### Git Fork
- A **Fork** is a GitHub-specific concept. It creates a complete, separate copy of someone else's repository into *your* personal GitHub account.
- **Why use it?** If you find an open-source project (like Kubernetes) that you do not have permission to push to, you **Fork** it to your account first. Then you `git clone` your *fork* to your laptop, make changes, push to your fork, and finally submit a "Pull Request" to the original creator asking them to merge your changes.

---

## 4. The Standard Developer Workflow

The daily routine for a developer/DevOps engineer looks like this:
```bash
# 1. Pull the latest code from the remote server so you are up to date
git pull origin main

# 2. Make your code changes in the editor
vim calculator.sh

# 3. See what you changed
git diff

# 4. Stage and Commit
git add calculator.sh
git commit -m "Added multiplication feature"

# 5. Push to GitHub
git push origin main
```
*Note: You can chain commands using `&&` like this:* `git add . && git commit -m "fix" && git push`

---
**[Previous: Day 14 - Git Basics](./Day-14-Git-Basics-and-Lifecycle.md)** | **[Next: Day 16 - Advanced Branching & Merging](./Day-16-Advanced-Git-Branching-and-Merging.md)**
