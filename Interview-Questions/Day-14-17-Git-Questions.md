# Day 14-17: Git & GitHub - Interview Questions

---

### Q1: What is the difference between a Centralized Version Control System (SVN) and a Distributed Version Control System (Git)?
**Answer:**  
In a centralized system, there is a single master server containing the repository. Developers check out files from this central server. If the server goes down, collaboration stops. In a distributed system like Git, every developer's machine contains a full clone of the entire repository history. Developers can commit, branch, and view logs entirely offline, and there is no single point of failure.

### Q2: What actually happens when you run `git init`?
**Answer:**  
`git init` transforms a standard directory into a Git repository by creating a hidden `.git` folder. This folder acts as the database for version control, containing all the objects, branches, configuration files, and commit histories. If you delete the `.git` folder, the repository loses all its tracking and reverts back to a normal directory.

### Q3: Explain the difference between `git merge` and `git rebase`. When would you use each?
**Answer:**  
`git merge` takes two distinct branches and combines them by creating a new, dedicated "merge commit". This preserves the exact historical timeline of when branches were created and merged, but it can make the git log messy. 
`git rebase` takes the commits from a feature branch and replays them at the tip of the target branch (like `main`), creating a perfectly linear history without a merge commit. You use `rebase` to keep histories clean, but you should never rebase a public branch that other developers are currently working on because it rewrites commit IDs.

### Q4: What is `git cherry-pick`?
**Answer:**  
`git cherry-pick` is a command that allows you to select a specific commit from one branch by its commit ID and apply it directly to your current branch. It is highly useful when you only want a specific bug fix from a feature branch without merging the entire feature.

### Q5: What is the difference between `git clone` and a GitHub Fork?
**Answer:**  
`git clone` is a Git CLI command that downloads a copy of a remote repository onto your local computer. A Fork is a GitHub-specific concept that creates a complete copy of someone else's repository into your own personal GitHub cloud account. You typically Fork an open-source repo (where you don't have write access), clone your Fork locally, make changes, and then submit a Pull Request back to the original owner.

### Q6: Walk me through your daily workflow using Git commands.
**Answer:**  
1. I start by pulling the latest code from the remote branch to ensure I'm up to date: `git pull origin main`.
2. I create a new feature branch: `git checkout -b feature/xyz`.
3. I write my code and then check what changed using `git status` and `git diff`.
4. I stage the files using `git add .`
5. I commit the snapshot with a descriptive message: `git commit -m "Implemented xyz feature"`.
6. Finally, I push my branch to GitHub: `git push origin feature/xyz` and open a Pull Request for code review.

### Q7: Explain the difference between `git pull` and `git fetch`.
**Answer:**  
`git fetch` only downloads the latest meta-data and commit history from the remote repository to your local `.git` database, but it does not modify your working directory. `git pull` is a combination command: it runs `git fetch` and then immediately runs `git merge` to integrate those changes directly into your current working branch.

### Q8: What is a Merge Conflict and how do you resolve it?
**Answer:**  
A merge conflict occurs when Git cannot automatically merge two branches because they have conflicting changes on the exact same lines of a file. To resolve it, I open the conflicting files, locate the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), manually edit the code to the desired final state, remove the markers, stage the file with `git add`, and finalize the merge with a `git commit`.

### Q9: How do you undo a commit that has already been pushed to a public remote repository? (Reset vs Revert)
**Answer:**  
If a commit is already pushed and shared with other developers, you should **never** use `git reset`, because it rewrites the commit history and will cause sync issues for everyone else. Instead, you must use `git revert <commit-id>`. This creates a brand new commit that safely inverts the changes of the bad commit, moving the history forward instead of rewriting the past.

### Q10: What is the purpose of `git stash`?
**Answer:**  
`git stash` is used to temporarily save uncommitted changes in your working directory without making a formal commit. It reverts your working directory back to a clean state. This is extremely useful if you are in the middle of working on a feature but suddenly need to switch branches to fix a critical bug. Once the bug is fixed, you return to your feature branch and use `git stash pop` to reapply your unfinished work.

---
**[Previous: Day 11-13 - Networking Questions](./Day-11-13-Networking-Questions.md)**
