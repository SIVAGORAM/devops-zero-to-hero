# Day-13: AWS CI/CD & AWS CodeCommit Deep Dive

## What is CI/CD on AWS?
AWS provides a comprehensive set of CI/CD (Continuous Integration / Continuous Deployment) services that enable developers to automate and streamline their software delivery process. 

Using AWS native tools, you can implement an entire end-to-end CI/CD pipeline entirely within the AWS ecosystem without needing third-party tools.

### The 4 Pillars of AWS CI/CD:
1.  **AWS CodeCommit** (Source Control)
2.  **AWS CodeBuild** (Build & Test)
3.  **AWS CodeDeploy** (Deployment)
4.  **AWS CodePipeline** (The Orchestrator that connects them all)

---

## Traditional CI/CD vs. AWS Native CI/CD

To understand the AWS services, let's compare them to a traditional workflow you might already know.

**Traditional Architecture (e.g., deploying to Kubernetes/EC2):**
1.  **Source Code:** Hosted on **GitHub**.
2.  **Trigger:** Developer commits code to GitHub, which triggers a webhook.
3.  **Orchestrator:** **Jenkins** receives the webhook and starts the pipeline.
4.  **Build/Test:** Jenkins runs scripts to build the code, test it, and create a Docker image.
5.  **Deploy:** The image is deployed to Kubernetes or an EC2 instance.

**AWS Native Architecture:**
AWS built equivalent tools to replace this traditional stack:
*   GitHub  $\rightarrow$ **AWS CodeCommit**
*   Jenkins (Orchestrator) $\rightarrow$ **AWS CodePipeline**
*   Jenkins (Build/Test stage) $\rightarrow$ **AWS CodeBuild**
*   Deployment Script $\rightarrow$ **AWS CodeDeploy**

---

## Deep Dive: AWS CodeCommit

AWS CodeCommit is a fully-managed source control service that hosts secure Git-based repositories. It is the AWS equivalent of GitHub or GitLab. In enterprise organizations, teams often use CodeCommit to host their private repositories securely within their AWS environment.

### Advantages of CodeCommit:
*   **Fully Managed Git:** No need to manage your own Git servers.
*   **Highly Scalable:** Can handle large repositories and many files.
*   **Reliable & Secure:** Integrated heavily with AWS IAM for strict access control.

### Disadvantages of CodeCommit:
*   **Fewer Features:** It lacks the rich UI, community features, and project management tools of GitHub.
*   **AWS Restricted:** It is locked into the AWS ecosystem.
*   **Limited Integrations:** Fewer out-of-the-box integrations with third-party tools outside of AWS.

---

## Hands-On Lab: From Zero to Hero with CodeCommit

### Lab 1: Creating a Repository
1.  Log in to the **AWS Management Console**.
2.  Search for **CodeCommit**. You should see the subtext *"Store code in private Git repositories"*; click on it.
3.  Click on **Create repository**.
4.  **Repository name:** `demo-repo-cc`
5.  **Description:** `demo repo for learning code commit`
6.  *Note on Java/Python checkbox:* Only check this if you are using specific Java/Python applications, otherwise leave it unchecked.
7.  Click **Create**.

*Note: You can use the AWS UI to add or edit files one at a time. The UI also supports basic Git features like Pull Requests, Commits, Branches, and Tags (though fewer features than GitHub).*

**Important Security Warning:** 
AWS will give you a warning: *Do not use your Root User for CodeCommit.* You must create an IAM user with proper permissions to interact with CodeCommit. Let's do that next.

### Lab 2: Creating an IAM User for CodeCommit
1.  Go to the AWS search bar and search for **IAM** (Identity and Access Management).
2.  Go to **Users** and click **Add users**.
3.  **User name:** `codecommit-user-1` (or your preferred name).
4.  Check the box to **Provide user access to the AWS Management Console**.
5.  Select **I want to create an IAM user**.
6.  Choose a **Custom password** and click **Next**.
7.  Under permissions, select **Attach policies directly**.
8.  Search for `CodeCommit` and check the box next to **AWSCodeCommitPowerUser**. *(This policy grants the user full access to use CodeCommit without giving them full Administrator access).*
9.  Click **Next**, then **Create user**.

### Lab 3: Cloning and Committing Code
1.  Open an **incognito tab** (or log out) and log in to the AWS Console using the newly created IAM user credentials (Account ID, Username, and Password).
2.  Ensure you are in the correct **Region** where you created the repository.
3.  Go to **CodeCommit** and click on your repository (`demo-repo-cc`).
4.  Click on **Clone URL** and copy the **Clone HTTPS** link.

**In your local terminal:**
*(Make sure Git is installed on your computer: `git --version`)*

```bash
# Clone the repository
git clone <paste-your-codecommit-url-here>
```

*When you run this, it will prompt you for a Git username and password. You must generate HTTPS Git credentials for your IAM user from the IAM console (under the user's "Security credentials" tab) and enter them here.*

```bash
# Navigate into the repo
cd demo-repo-cc

# Create a new file
echo "Hello from AWS CodeCommit!" > hello.txt

# Add, commit, and push
git add hello.txt
git commit -m "My first commit to AWS CodeCommit"
git push
```

Go back to the CodeCommit UI in your browser, refresh the page, and you will see your `hello.txt` file successfully uploaded!
