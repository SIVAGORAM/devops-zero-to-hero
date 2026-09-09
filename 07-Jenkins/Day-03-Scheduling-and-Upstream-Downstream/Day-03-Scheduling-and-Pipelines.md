# Jenkins Day 3: Scheduling, Execute Shell, & Upstream/Downstream Jobs

Welcome to Jenkins Day 3! Today we dive deep into how to control *when* your pipelines run (Scheduling & Cron), *what* they run (Execute Shell), and *how* they connect to each other (Upstream & Downstream).

---

## 🛠️ 1. Jenkins Setup Recap & Initial Configuration

### Installing Jenkins on a Fresh EC2 Instance
If you are spinning up a new Amazon Linux 2023 server for today's lab, here is the exact script to install Java and Jenkins:

```bash
# 1. Install Java 17
yum install java-17-amazon-corretto -y
java -version

# 2. Add Jenkins Repository and Keys
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

# 3. Install and Start Jenkins
yum install jenkins -y
systemctl start jenkins
systemctl enable jenkins
systemctl status jenkins
```
*(Press `q` to exit the status screen).*

Access Jenkins via your browser: `http://<your-ip>:8080`, unlock it using the password in `/var/lib/jenkins/secrets/initialAdminPassword`, install suggested plugins, and set up your admin account.

### Setting the Timezone to IST (Asia/Kolkata)
Because we are going to schedule jobs to run at specific times, Jenkins must be in the correct Timezone!

**From the Linux Terminal:**
Check your current timezone:
```bash
timedatectl
```
Change it to IST:
```bash
timedatectl set-timezone Asia/Kolkata
systemctl restart jenkins
```

**From the Jenkins Dashboard:**
1. Go to **Profile** -> **Configure** (or Account settings).
2. Find the **Time Zone** dropdown.
3. Select `Asia/Kolkata` and click **Save**.

---

## ⏰ 2. Cron Jobs & Scheduling Syntax

Instead of manually clicking "Build Now", Jenkins can start jobs automatically using a **Cron Job**. 

### What is a Cron Job?
A cron job is a scheduled task that runs automatically at a specified time. Jenkins uses standard Unix Cron syntax to schedule its jobs. 
*(Reference: [crontab.guru](https://crontab.guru/))*

### The 5 Fields of Cron
A Jenkins cron expression contains exactly 5 fields, separated by spaces:

```text
*  *  *  *  *
|  |  |  |  |
|  |  |  |  └── Day of Week (0-6) (0 = Sunday, 1 = Monday, 6 = Saturday)
|  |  |  └───── Month (1-12)
|  |  └──────── Day of Month (1-31)
|  └─────────── Hour (0-23)
└────────────── Minute (0-59)
```

**Easy Memory Trick:** `Minute -> Hour -> Date -> Month -> Weekday` (M H DOM MON DOW)

> [!IMPORTANT]
> **Hours use 24-Hour Format!** This is the most common beginner mistake.
> 10:00 AM = 10
> 4:00 PM = 16
> 10:00 PM = 22

### What does `*` mean?
An asterisk (`*`) means **"every possible value"**. 
If you put `* * * * *`, Jenkins will literally run the job every single minute of every hour of every day!

### Practical Cron Examples
| Scenario | Cron Expression | Breakdown |
|---|---|---|
| **Every day at 10:35 AM** | `35 10 * * *` | 35th min, 10th hour, any day, any month, any weekday |
| **Every day at 5:00 PM** | `0 17 * * *` | 0th min, 17th hour (5 PM) |
| **Every Monday at 9:00 AM** | `0 9 * * 1` | 0th min, 9th hour, Monday (1) |
| **Every Sunday at 10:00 AM**| `0 10 * * 0` | 0th min, 10th hour, Sunday (0) |
| **Dec 12 at 4:45 PM** | `45 16 12 12 *` | 45th min, 16th hour, 12th day, 12th month |

*(Next steps to learn for advanced pipelines: `*/5` (every 5 mins), `H` (Hash/spread), `-` (ranges), and `,` (lists)).*

---

## ⚖️ 3. Webhook vs Poll SCM vs Build Periodically

This is a critical interview topic. There are three ways to trigger a job automatically.

### 1. Webhooks (The Best Way)
**Flow:** `Dev Commits -> GitHub instantly notifies Jenkins -> Auto Build`
- **When to use:** When you want an instant build the absolute second a developer pushes code.

### 2. Poll SCM (The Scheduled Checker)
**Flow:** `Time Schedule (e.g., 9:30 PM) -> Jenkins asks GitHub "Any new commits?" -> If YES, Auto Build`
- **When to use:** When you want Jenkins to check for new code on a schedule. If developers committed code today, it will build at 9:30 PM. If no one committed code today, it skips the build.
- **How to configure:** Check **Poll SCM** and enter your cron expression. 
- *(Note: If you enter `* * * * *` in Poll SCM, Jenkins will check GitHub every single minute for new commits!)*

### 3. Build Periodically (The Blind Runner)
**Flow:** `Time Schedule (e.g., 9:30 PM) -> Auto Build`
- **When to use:** When you want the pipeline to run at a specific time **no matter what**. It doesn't care if there are new commits or no commits. It just blindly runs the build.
- **Why use this?** Mainly used for testing purposes, daily database backups, or nightly system health checks.
- **How to configure:** Check **Build Periodically** and enter your cron expression (e.g., `25 21 12 11 3`).

> [!TIP]
> **Interview Question:** What is the difference between Webhook and Poll SCM?
> **Answer:** A webhook is event-driven; GitHub pushes a notification to Jenkins the moment code is committed, triggering an instant build. Poll SCM is schedule-driven; Jenkins wakes up on a cron schedule (like every 5 minutes) to manually check GitHub for changes. You should use one or the other, but not both!

---

## 💻 4. The Execute Shell Build Step

So far, we've only downloaded code. Now let's actually run commands on our Jenkins server using the **Execute Shell**.

1. Go to your Pipeline Configuration.
2. Scroll down to **Build Steps**.
3. Click **Add build step** and select **Execute shell**.
4. A text box will appear. You can type standard Linux commands here!

**Example Commands:**
```bash
touch ram.txt
mkdir ram_folder
timedatectl
cal
```

5. **Save** and click **Build Now**.
6. Open the **Console Output**. You will see the calendar (`cal`) print out, the timezone print out, and the file creations succeed! 
7. If you SSH into your EC2 server and navigate to `/var/lib/jenkins/workspace/<job-name>`, you will see `ram.txt` and `ram_folder` sitting right there.

---

## 🔗 5. Upstream and Downstream Jobs

In the real world, CI/CD is not one giant messy job. It is broken down into smaller, chained jobs:
`Code (Job1) ---> Build (Job2) ---> Test (Job3) ---> Deploy (Job4)`

If a job succeeds, it should automatically trigger the next job in the chain.

### Practical Lab: Chaining Jobs
1. Create 4 empty Freestyle projects: `Job1`, `Job2`, `Job3`, `Job4`.
2. Go into the configuration for **Job2**.
3. Under **Build Triggers**, select **Build after other projects are built**.
4. In the "Projects to watch" box, type `Job1` and select "Trigger only if build is stable". Save.
5. Go into the configuration for **Job3**. Tell it to build after `Job2`.
6. Go into the configuration for **Job4**. Tell it to build after `Job3`.

**The Magic Result:** 
Go to the Jenkins dashboard and manually click **Build Now** on **Job1**. 
Once Job1 finishes successfully, Job2 will start automatically. When Job2 finishes, Job3 starts. When Job3 finishes, Job4 starts!

### The Interview Definitions
- **Upstream Job:** The job that runs *before* the current job. (For `Job2`, `Job1` is the upstream job).
- **Downstream Job:** The job that runs *after* the current job. (For `Job2`, `Job3` and `Job4` are downstream jobs).
