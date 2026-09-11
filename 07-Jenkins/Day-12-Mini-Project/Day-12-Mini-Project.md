# Jenkins Day 12: End-to-End Mini Project (Real-World Pipeline)

Welcome to a real-world Jenkins pipeline - a mini project tailored for freshers to get hands-on experience with CI/CD. In today’s fast-paced DevOps world, mastering tools like Jenkins, Git, Maven, SonarQube, Nexus, and Slack is essential. This blog will guide you through a step-by-step pipeline setup that mirrors industry practices.

## 🏗️ Architecture
![Pipeline Architecture](./architecture-diagram.png)

## 🧩 Pipeline Stages
![Pipeline Stages](./stages-diagram.png)

Let’s break down the pipeline into stages, each serving a unique purpose in the CI/CD process:

**🧑‍💻 Stage 1: Code (Git)**
Our journey begins by fetching the latest source code from a Git repository. This is the heart of any DevOps workflow -—→ version-controlled, collaborative, and reliable.

**🔍 Stage 2: CQA - Code Quality Analysis (SonarQube)**
Before jumping into builds, we perform a static code analysis using SonarQube. This helps detect code smells, bugs, and security vulnerabilities early in the pipeline.

**🏗️ Stage 3: Build & Unit Test (Maven)**
We compile the code and run unit tests using Maven, ensuring that everything works as expected before proceeding. This is a crucial step to catch any build-time issues.

**📦 Stage 4: Artifact (Nexus)**
Once the build is successful, we package the application and upload the artifact to Nexus, a repository manager that acts as a centralized storage for build artifacts.

**🚀 Stage 5: Deploy (Tomcat)**
In this stage, the application is deployed to a staging or test environment. You can customize this depending on your infra, for this demo, we kept it light and focused.
![Tomcat Manager](./tomcat-manager.png)

**📢 Stage 6: Post Build Actions (Slack Notification)**
After everything is done, we notify the team on Slack with a success or failure message -- making communication seamless and transparent.

---

## 💻 Practical Implementation of Project

Here i need 3 servers:
![AWS Instances](./aws-instances.png)

**Jenkins**
- AMI = Amazon Linux Kernel 5.10
- Instance type = t2.micro
- EBS = 8 GB
- Security Groups = SSH, 8080

**Tomcat**
- AMI = Amazon Linux Kernel 5.10
- Instance type = t2.micro
- EBS = 8 GB
- Security Groups = SSH, 8080

**Nexus & Sonarqube**
- AMI = Amazon Linux Kernel 5.10
- Instance type = t2.medium
- EBS = 22 GB
- Security Groups = SSH, 8081, 9000

---

## 🛠️ Let's Launch 3 Servers
Setup all the tools on their respective servers using the following scripts.

### 1. `jenkins.sh`
```bash
#STEP-1: INSTALLING GIT 
yum install git  -y

#STEP-2: GETTING THE REPO (jenkins.io --> download -- > redhat)
sudo wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

#STEP-3: DOWNLOAD JAVA17 AND JENKINS
yum install java-17-amazon-corretto -y
yum install jenkins -y

#STEP-4: RESTARTING JENKINS (when we download service it will on stopped state)
systemctl start jenkins.service
systemctl enable jenkins.service
systemctl status jenkins.service
```
![Jenkins Dashboard](./jenkins-dashboard.png)

### 2. `tomcat.sh`
```bash
yum install java-17-amazon-corretto -y
wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.104/bin/apache-tomcat-9.0.104.tar.gz
tar -zxvf apache-tomcat-9.0.104.tar.gz
sed -i '56  a\<role rolename="manager-gui"/>' apache-tomcat-9.0.104/conf/tomcat-users.xml
sed -i '57  a\<role rolename="manager-script"/>' apache-tomcat-9.0.104/conf/tomcat-users.xml
sed -i '58  a\<user username="tomcat" password="admin@123" roles="manager-gui, manager-script"/>' apache-tomcat-9.0.104/conf/tomcat-users.xml
sed -i '59  a\</tomcat-users>' apache-tomcat-9.0.104/conf/tomcat-users.xml
sed -i '56d' apache-tomcat-9.0.104/conf/tomcat-users.xml
sed -i '21d' apache-tomcat-9.0.104/webapps/manager/META-INF/context.xml
sed -i '22d'  apache-tomcat-9.0.104/webapps/manager/META-INF/context.xml
sh apache-tomcat-9.0.104/bin/startup.sh
```

### 3. `sonar.sh`
```bash
cd /opt/
wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-8.9.6.50800.zip
unzip sonarqube-8.9.6.50800.zip
yum install java-17-amazon-corretto -y
useradd sonar
chown sonar:sonar sonarqube-8.9.6.50800 -R
chmod 777 sonarqube-8.9.6.50800 -R
su - sonar

#run this on server manually
#sh /opt/sonarqube-8.9.6.50800/bin/linux-x86-64/sonar.sh start
#echo "user=admin & password=admin"
```

### 4. `nexus.sh`
```bash
sudo yum update -y
sudo yum install wget -y
sudo yum install java-17-amazon-corretto-jmods -y
sudo mkdir /app && cd /app
sudo wget https://download.sonatype.com/nexus/3/nexus-3.79.1-04-linux-x86_64.tar.gz
sudo tar -xvf nexus-3.79.1-04-linux-x86_64.tar.gz
sudo mv nexus-3.79.1-04 nexus
sudo adduser nexus
sudo chown -R nexus:nexus /app/nexus
sudo chown -R nexus:nexus /app/sonatype*
sudo sed -i '27  run_as_user="nexus"' /app/nexus/bin/nexus
sudo tee /etc/systemd/system/nexus.service > /dev/null << EOL
[Unit]
Description=nexus service
After=network.target

[Service]
Type=forking
LimitNOFILE=65536
User=nexus
Group=nexus
ExecStart=/app/nexus/bin/nexus start
ExecStop=/app/nexus/bin/nexus stop
User=nexus
Restart=on-abort

[Install]
WantedBy=multi-user.target
EOL
sudo chkconfig nexus on
sudo systemctl start nexus
sudo systemctl enable nexus
sudo systemctl status nexus
```

---

## 📦 Create a repository in nexus
![Nexus Welcome Dashboard](./nexus-welcome.png)
- SELECT REPOSITORIES
![Nexus Repositories Admin](./nexus-admin-repositories.png)
![Nexus Repositories List](./nexus-repositories-list.png)
- SELECT CREATE-REPOSITORY
- SELECT MAVEN2(HOSTED)
![Nexus Create Maven Hosted](./nexus-create-maven-hosted.png)
- GIVE REPOSITORY NAME AS `myrepo` and deployment policy as `Allow redeploy` and click on create repositories
- now you can see our repository created in dashboard

After setting all the tools using above scripts, now we have to integrate with Jenkins. Lets install the following plugins to deploy an application.
![Jenkins Plugins](./jenkins-plugins.png)

---

## 🔍 SonarQube Integration
After installing all the plugins, Lets integrate sonarqube.
![SonarQube Dashboard](./sonar-dashboard.png)

1. go to **manage jenkins** » **system** » and search for **SonarQube servers**
![Jenkins SonarQube Config](./jenkins-sonar-config.png)
2. **Name:** `mysonar`
3. **Server URL:** `sonarqube server url`
4. For credentials, click on add
5. **kind:** `secret text`

Now it will ask the secret. To get the secret go to sonarqube dashboard and select your profile and click on **My Account**.
- Go to security tab
- Enter any token-name and click on Generate
![Generate Token](./sonar-token-generate.png)
- copy the token and paste it on credentials tab on jenkins
![Copy Token](./sonar-token-copy.png)
- Now click on add and select the credentials

Now lets go to **manage jenkins** » **tools**. After adding maven and sonar tools, just click on save.

---

## 💬 Slack Integration
1. Create a Free slack account
2. Enter your company name
![Slack Workspace](./slack-create-workspace.png)
3. Click on Next
![Slack Your Name](./slack-step3-name.png)
4. Click on next
5. Add your teammate mail id’s
![Slack Teammates](./slack-step5-teammates.png)
6. Enter project name
![Slack Project Name](./slack-step6-project.png)
7. Select the free limited version
![Slack Free Version](./slack-step7-free.png)

Now click on your company name (Mini-Project) » **Tools & Settings** » **Manage apps**
![Slack Manage Apps Menu](./slack-menu-manage-apps.png)
- Now search for **jenkins CI**
![Slack Manage Apps Search](./slack-jenkins-app-search.png)
- Now click on **add to slack**
![Slack Manage Apps Add](./slack-jenkins-app-add.png)
- Now select the channel
![Slack Channel Select](./slack-jenkins-app-channel.png)
- click on **Add Jenkins CI Integration**

From the step-3 copy the **Team subdomain & Token**.
![Slack Jenkins Token Step](./slack-jenkins-app-token-step.png)
Go back to Jenkins and manage jenkins and search for slack:
![Slack Jenkins Global Settings](./slack-jenkins-global-settings.png)
- **Workspace:** `miniproject-cao6485`
- **Credentials** ——> **kind:** `Secret` (add that token here)

---

## 🔑 Nexus and Tomcat Credentials
Now add tomcat and nexus credentials.
1. go to **manage jenkins** » **credentials** » **system** » **Global credentials (unrestricted)**
2. Click on **Add Credentials**
![Jenkins Sonar Credential](./jenkins-credential-sonar.png)
3. click on **Create**
4. Click on **Add Credentials** again
![Jenkins Tomcat Credential](./jenkins-credential-tomcat.png)
5. Click on **Add Credentials** again
![Jenkins Nexus Credential](./jenkins-credential-nexus.png)
6. click on **Create**, you can see the list of credentials like this
![Jenkins Credentials All](./jenkins-credentials-all.png)

---

## 📜 Full Pipeline Code

After adding the credentials, you can write the pipeline like this:

```groovy
pipeline {
    agent any
    tools {
        maven "mymaven"
    }
    stages {
        stage('Code') {
            steps {
                git "https://github.com/devops0014/one.git"
            }
        }
        stage ("CQA") {
            steps {
                withSonarQubeEnv('mysonar') {
                    sh '''
                        mvn sonar:sonar \
                        -Dsonar.projectKey=MyProject \
                        -Dsonar.host.url=<your-sonar-url> \
                        -Dsonar.login=<enter-your-token>
                    '''
                }
            }
        }
        stage ("Build") {
            steps {
                sh 'mvn clean package'
            }
        }
        stage ("Artifact") {
            steps {
                nexusArtifactUploader artifacts: [[artifactId: 'myweb', classifier: '', file: 'target/myweb-8.7.3.war', type: '8.7.3']], credentialsId: 'nexus', groupId: 'in.javahome', nexusUrl: '<your-nexus-url>', nexusVersion: 'nexus3', protocol: 'http', repository: 'myrepo', version: '8.7.3'
            }
        }
        stage ("Deploy") {
            steps {
                deploy adapters: [tomcat9(credentialsId: 'tomcat', path: '', url: '<your-tomcat-url>')], contextPath: 'myapp', war: 'target/*.war'
            }
        }
        post {
            always {
                echo 'Slack Notifications'
                slackSend (
                    channel: '<your-channel-name>', message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} \n build ${env.BUILD_NUMBER} \n More info at: ${env.BUILD_URL}"
                )
            }
        }
    }
}
```

PIPELINE OUTPUT:
![Pipeline Stage View](./jenkins-pipeline-stage-view.png)
![Pipeline Output](./pipeline-output-stage-view.png)

SONAR OUTPUT:
![Sonar Output](./sonar-output-passed.png)

NEXUS OUTPUT:
![Nexus Output](./nexus-output-artifact.png)

TOMCAT OUTPUT:
![Tomcat Output](./tomcat-output-app.png)

SLACK NOTIFICATION:
![Slack Notification](./slack-notification-output.png)

**And that’s a wrap! 🎉**
Through this mini Jenkins pipeline project, you’ve touched key DevOps concepts and tools — from source control and quality checks to builds, artifact management, and team communication.

---
*this is day:-12 of jenkines end to end mini project once check this notes end to to n deeply we we missing anything add them use previous notes if u want if any user read this notes they can able to understnad withotua any confusion they can understand the read all they can able to implement by reading this document they can implement end to end jenkins pipeline without any confuison i given you some of the image use them remaming images i will give u by next so make it update end to end deeply perfect project notes withotu any confuson and errors*
