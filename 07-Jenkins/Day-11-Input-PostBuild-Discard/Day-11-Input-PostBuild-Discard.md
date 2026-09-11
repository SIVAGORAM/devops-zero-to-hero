# Jenkins Day 11: Pipeline Inputs, Post Build Actions & Old Build Management

Welcome to Day 11! Today we will elevate our Jenkins pipelines by introducing manual deployment approvals, post-build state management, email notifications, storage optimization, and port modifications.

Let's master this end-to-end!

---

## 🚀 STEP 0: Server Setup
Create the instance with all requirements and connect it or login to it. Inside this machine, install Jenkins as we have done in the previous classes. Use that! 
1. Access the dashboard in browser `ipaddress:port`.
2. Login to Jenkins and install the suggested plugins.
3. In the plugins, download the **Pipeline Stage View** plugin to visualize your pipeline properly.

Create the job:
1. Go to pipeline.
2. Write the basic pipeline script.

---

## ✋ 1. Pipeline Input (Manual Approvals)

### Continuous Delivery vs. Continuous Deployment
Deployment happens automatically. I don't want the automatic deployment! In realtime we need to get approval from the release manager. In the script you can add that. What is the different between continuous deployment and delivery?

When manual approval is required before deployment, it is called **Continuous Delivery**.

In the script you can add that manual pause using the `input` block:

```groovy
pipeline {
    agent any

    stages {
        stage('Code') {
            steps {
                echo 'This is Code Stage'
            }
        }
        stage('Build') {
            steps {
                echo 'This is Build Stage'
            }
        }
        stage('Test') {
            steps {
                echo 'This is Test Stage'
            }
        }
        stage('Deploy') {
            input {
                message 'Can I Deploy?'
            }
            steps {
                echo 'This is Deploy Stage'
            }
        }
    }
}
```
Here it will ask for approve or decline. If the release manager approve it going to deployment, if you decline it will not deploy. You can check the logs who is approver who is declines like that logs.

---

## 📧 2. Post Build Actions (Pipeline State)

If my pipeline success, or fail or abort we need to receive the mail ---> pipeline state using the postbuild actions.

In the pipeline we have multiple stages after completing this all stages send me the mail like we should configure in the pipeline script. For success, failure, abort:

### Jenkins Post Conditions
The `post` block is used to execute actions *after* the pipeline or stage completes.

```text
post
 │
 ├── success
 │     └── Runs when pipeline succeeds (This will be printed when your pipeline is successful)
 │
 ├── failure
 │     └── Runs when pipeline fails (This will be printed when your pipeline fails)
 │
 ├── aborted
 │     └── Runs when pipeline is cancelled (This will be printed when your pipeline is cancelled)
 │
 └── always
       └── Runs regardless of the result (This will be printed anyway)
```

### Full Pipeline Script with Post Conditions
```groovy
pipeline {
    agent any

    stages {
        stage('Code') {
            steps {
                echo 'This is Code Stage'
            }
        }
        stage('Build') {
            steps {
                echo 'This is Build Stage'
            }
        }
    }

    post {
        success {
            echo "My Pipeline is success"
        }
        failure {
            echo "My Pipeline failed"
        }
        aborted {
            echo "My Pipeline is cancelled"
        }
        always {
            echo "This will be printed anyways"
        }
    }
}
```

Once check is this script is correct or not.

---

## ✉️ 3. Integrating Email Notifications

Now lets integrate the email notification for this:

### Step 1: Install Plugin and Configure Gmail
1. For this we need a plugin. Go to **Manage Jenkins**, go to **Plugins** search for: **Email Extension Template** and install it.
2. Next go to **Manage Jenkins**, go to **System** go to last you will see **Email Notification**.
3. **SMTP server:** `smtp.gmail.com`
4. Click on **Advanced**.
5. Tick that **Use SMTP authentication**.
   - **Username:** `siva@gmail.com` (give your gmail here).
   - **Password:** Now go to your gmail, go to your account search for app password login here. Give the app name, click on create. Copy the token you got. Paste that password token in the password section of the email notification section we are doing.
6. Tick the **Use SSL**.
7. **SMTP port:** `465`
8. **Reply to address:** `siva@gmail.com`
9. You can test the configuration. Once check this test email. Click on **Save**.

### Step 2: Add Email to Pipeline Script
From the pipeline syntax also you will get the syntax, from there also you generate the pipeline syntax. Now go to your pipeline script add this script at end:

```groovy
pipeline {
    agent any

    stages {
        stage('Code') { steps { echo 'This is Code Stage' } }
        stage('Build') { steps { echo 'This is Build Stage' } }
        stage('Test') { steps { echo 'This is Test Stage' } }
        stage('Deploy') {
            input { message 'Can I Deploy?' }
            steps { echo 'This is Deploy Stage' }
        }
    }

    post {
        always {
            mail to: 'siva@gmail.com',
                 subject: "PIPELINESTATUS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} \n build ${env.BUILD_NUMBER} \n More info at: ${env.BUILD_URL}"
        }
    }
}
```

---

## 🗑️ 4. Discard Old Builds

Everytime we have multiple build per day, for one week or month you will get 100's of builds. You need only latest 5 build then you should configure this, in that case:

1. Go to **Configure**, go to **General** select the **Discard old builds**.
2. **No of days to keep builds:** `3`
3. **Max of build to keep:** `7`

You will see the latest 7 builds, after 3 days this also deletes!

> [!WARNING]
> In future if we need this then from the ThinBackup you can get this. Before doing this take the ThinBackup.

---

## ⚙️ 5. Changing Port Numbers

### How to change the Jenkins port number:
Go to this path:
```bash
cd /usr/lib/systemd/system
ll
```
You can see the `jenkins.service`.
```bash
vim jenkins.service
```
Find the `Environment="JENKINS_PORT=8080"`. Change this to your required port number, I will change it to `Environment="JENKINS_PORT=1234"`. Save and continue.

```bash
systemctl daemon-reload
```
This is background services running it restarting:
```bash
systemctl restart jenkins
```

Now go to aws console in security groups add this port number in inbound rules.
Now to browser:- `ipaddress:1234`
You can access the Jenkins dashboard!

### Can we change the Tomcat port number?
Inside the `server.xml`. Mention this in detailed if we are missing anything please add them!
1. Go to the Tomcat configuration directory:
   ```bash
   cd /opt/tomcat/conf
   ```
2. Open the `server.xml` file:
   ```bash
   vim server.xml
   ```
3. Search for the Connector port configuration (usually around line 69). Change `port="8080"` to `port="9090"`:
   ```xml
   <Connector port="9090" protocol="HTTP/1.1"
              connectionTimeout="20000"
              redirectPort="8443" />
   ```
4. Save the file and restart your Tomcat server:
   ```bash
   /opt/tomcat/bin/shutdown.sh
   /opt/tomcat/bin/startup.sh
   ```
5. Open port `9090` in your AWS Security Group. You can now access Tomcat on `ipaddress:9090`.

---

## 📖 6. Types of Pipelines

Type of pipelines:
1. Scripted pipelines
2. Declarative pipelines

In realtime we use declarative pipelines. Scripted pipelines is old way of writing the pipelines no one will use this. Understand this both types.

---

*This is day-11 of jenkins class in today we class we discussed Jenkins Pipeline:- Input, Post Build actions and Discard old builds please update the repo notes if any user reads this they can able to understand deeply without any confusion make them zero to hero.*
