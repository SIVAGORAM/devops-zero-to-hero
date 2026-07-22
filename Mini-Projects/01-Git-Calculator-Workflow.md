# Mini-Project 1: The Git Calculator Workflow

This project simulates a real-world developer workflow. You will create a local repository, build a simple calculator script, push it to GitHub, create a feature branch, and merge it.

---

### Step 1: Initialize the Project Locally
Open your terminal (Git Bash or Linux) and run:
```bash
mkdir calculator-project
cd calculator-project
git init
```
This creates the hidden `.git` folder. Your directory is now a Git repository.

### Step 2: Create the Base Application
Create a simple bash script:
```bash
vim calculator.sh
```
Add the following basic code:
```bash
#!/bin/bash
echo "Welcome to the Calculator"
# Addition
sum=$(( $1 + $2 ))
echo "Sum is: $sum"
```
Save and exit (`:wq`).

### Step 3: First Commit
Check the status, stage the file, and commit it to the `main` branch.
```bash
git status
git add calculator.sh
git commit -m "Initial commit: Added addition feature"
```

### Step 4: Push to GitHub
1. Go to github.com and create a new repository called `calculator-project`.
2. Link your local repo to GitHub and push:
```bash
git remote add origin git@github.com:<your-username>/calculator-project.git
git branch -M main
git push -u origin main
```

### Step 5: Create a Feature Branch
Your manager wants you to add a division feature. Do not work directly on `main`! Create a branch:
```bash
git checkout -b feature/division
```

Edit the file to add division:
```bash
vim calculator.sh
```
Add these lines at the bottom:
```bash
# Division
div=$(( $1 / $2 ))
echo "Division is: $div"
```

### Step 6: Commit and Push the Feature
```bash
git add calculator.sh
git commit -m "Added division feature"
git push origin feature/division
```

### Step 7: Merge into Main
Now that your feature is done, merge it back into the main codebase.
```bash
# Switch back to main
git checkout main

# Merge the feature branch into main
git merge feature/division

# Push the updated main branch to GitHub
git push origin main
```

### Step 8: Clean Up
In a real company, once a feature is merged, you delete the old branch to keep things clean.
```bash
git branch -d feature/division
```

---
**Congratulations!** You have just completed a professional end-to-end Git branching workflow.
