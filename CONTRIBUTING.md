# Contributing Guidelines

First off, thank you for considering contributing to the **DevOps Zero to Hero** repository! This repository is designed to be a living, breathing guide for aspiring DevOps Engineers. 

We welcome contributions of all kinds: correcting typos, adding new interview questions, sharing production scripts, or improving existing documentation.

---

## How to Contribute

### 1. Reporting Bugs & Issues
If you spot an error, an outdated script, or a broken link, please open an Issue.
- Use the provided **Issue Templates** (if available).
- Clearly describe the problem and, if applicable, the solution you suggest.

### 2. Suggesting Enhancements
Want to add a new module (e.g., Azure or GCP) or a new project idea?
- Open an Issue first to discuss it with the maintainers.
- This ensures nobody duplicates work!

### 3. Contributing Code or Notes
To submit changes, follow the standard open-source fork-and-pull workflow:

1. **Fork the repository** to your own GitHub account.
2. **Clone the project** to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/devops-zero-to-hero.git
   ```
3. **Create a branch** for your feature or fix. We use standard branch naming conventions:
   - `feature/add-aws-project` (For new additions)
   - `fix/typo-in-linux-notes` (For corrections)
   - `docs/update-readme` (For documentation)
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**. Ensure your markdown formatting is clean and easy to read.
5. **Commit your changes**. We follow the **Conventional Commits** specification:
   - `feat: added a new script for Terraform`
   - `fix: corrected typo in Dockerfile`
   - `docs: updated contribution guidelines`
   ```bash
   git commit -m "feat: your descriptive commit message"
   ```
6. **Push the branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request (PR)**.
   - Navigate to the original repository and click "Compare & pull request".
   - Fill out the PR template.
   - Wait for a maintainer to review your code!

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](./CODE_OF_CONDUCT.md). We expect all contributors to maintain a professional, welcoming, and inclusive environment.

## AI Contribution Policy
As this roadmap embraces the AI era, using AI tools (like ChatGPT or GitHub Copilot) to help generate scripts or explanations is highly encouraged! However:
- **Always verify AI output.** Do not push scripts that you have not tested locally.
- **Understand the code.** You should be able to explain any AI-generated code you submit if asked during a PR review.

Thank you for helping us build the best open-source DevOps roadmap on the internet!
