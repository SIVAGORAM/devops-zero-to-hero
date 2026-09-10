# Jenkins Day 7: Pipelines as Code (Zero to Hero)

Welcome to Jenkins Day 7! In our previous blogs, we learned how to use **Freestyle Jobs**. Now, it’s time to explore the enterprise standard: **Pipeline Jobs**.

> [!NOTE]
> **Server Setup Prerequisite:** 
> If you need to set up your Jenkins server, Tomcat server, or configure the Jenkins Maven plugin (`mymaven`), **please refer to the exact, easy-to-use installation scripts provided in our Day 4 and Day 6 notes!** Today, we are keeping things simple and focusing *exclusively* on mastering Jenkins Pipelines!

---

## 🏗️ 1. Introduction to Jenkins Pipelines

Software development moves fast, and keeping up means delivering updates quickly and reliably. Continuous Integration (CI) and Continuous Delivery (CD) are practices that help teams stay agile. 

### What is a Pipeline?
A Jenkins pipeline is a group of stages (like Code, Build, Test, Deploy) that are interlinked with each other to perform an action. It allows you to describe your entire CI/CD process **as code**. Instead of clicking through Jenkins menus manually, you write a script.

Jenkins pipelines simplify and enhance CI/CD processes. Whether you're a developer building an app or an operations engineer managing deployments, pipelines provide consistency and scalability. Start using Jenkins pipelines today to save time, reduce errors, and deliver value faster.

### Key Benefits of Jenkins Pipelines
- **Automation:** Pipelines let you automate tasks, saving time and reducing errors. For instance, you can automatically deploy an app to a test server after a successful build.
- **Version Control:** Pipeline scripts can be stored in the same repository as your code, ensuring changes are tracked and collaborative.
- **Error Detection:** Pipelines provide detailed logs for each stage, helping you quickly identify and fix issues.
- **Extensibility:** Jenkins pipelines integrate with popular tools like Docker, Kubernetes, and GitHub.

### Freestyle vs Pipeline Jobs
- **Freestyle Jobs:** Simple configurations done via the Jenkins UI without coding. Example: A job that checks out code from GitHub and builds it. Limitations: Hard to manage complex workflows.
- **Pipeline Jobs:** Defined entirely as code, stored in a Jenkinsfile. Flexible, scalable, and the absolute standard for modern DevOps practices in real-time environments. Example: Automating a full CI/CD process with stages for build, test, and deploy.

### The Two Types of Pipelines
1. **Declarative Pipelines:** Simple, structured, and easier to read. (This is what we use most often!)
2. **Scripted Pipelines:** Offers more flexibility but requires complex Groovy programming. Instead of `pipeline {}`, they start with a `node {}` block:
   ```groovy
   node {
       stage('Code') {
           echo 'this is stage-1'
       }
       stage('Build') {
           echo 'this is build stage.'
       }
       stage('Deploy') {
           echo 'this is deploy.'
       }
   }
   ```

### What is a `Jenkinsfile`?
A **Jenkinsfile** is a text file that contains your pipeline code. In real-time, developers store this file directly inside their GitHub repository alongside their source code. This ensures the CI/CD pipeline is version-controlled!

---

## 🧩 2. The Anatomy of a Declarative Pipeline

Every Declarative pipeline follows a strict, easy-to-remember structure. 
Think of the acronym **P.A.S.S.S**:

### Pipeline Structure and Components
1. **pipeline Block:** 
   The top-level block wraps the entire Jenkinsfile and defines the pipeline. It specifies the environment and stages of the process.
   
2. **agent any:** 
   **Purpose:** Specifies where the pipeline runs. 
   **any:** The pipeline can execute on any available agent (node) in the Jenkins setup. This provides flexibility if there are multiple agents in the environment. By default it runs on the master server.

3. **stage('Code'):** 
   **Purpose:** Represents a specific phase (like the Build phase) of the pipeline.

4. **steps:**
   `echo 'this is my first pipeline'`: Outputs a message to the Jenkins console log, simulating the build step. In a real pipeline, this step might include commands to compile code or install dependencies.

### Example Structure:
```groovy
pipeline {
    agent any
    stages {
        stage('Code') {
            steps {
                echo 'Getting the project code'
            }
        }
        stage('Build') {
            steps {
                echo 'Building the code'
            }
        }
    }
}
```

---

## 🛠️ 3. Practical Lab: Building Your First Pipelines

Let's dive into Jenkins and start coding pipelines!

### Lab A: The Basic Pipeline
1. Go to Jenkins -> **New Item**.
   - You will see features similar to freestyle jobs, but there is a brand new **Pipeline** section where you write your script.
3. Scroll down to the **Pipeline Script** section and paste this:

```groovy
pipeline {
    agent any
    stages {
        stage("code") {
            steps {
                echo "Welcome to DevOps class"
            }
        }
        stage("build") {
            steps {
                echo "Happy men's day"
            }
        }
        stage("test") {
            steps {
                echo "This is testing stage"
            }
        }
    }
}
```
Save and click **Build Now**. Go to the Console Output to see your echo statements! *(Tip: You can install the **Pipeline Stage View** plugin to see a beautiful graphical view of your stages).*

### Lab B: Executing Shell Commands
To execute Linux terminal commands in a pipeline, we use the `sh` step.

**Method 1: Single Line execution (Best Practice for Debugging)**
Create a new job named `pipeline-shell` and run this:
```groovy
pipeline {
    agent any
    stages {
        stage("code") {
            steps {
                sh 'touch deployment'
                sh 'mkdir devops'
                sh 'cal'
            }
        }
        stage("stage-2") {
            steps {
                echo "this is my second stage"
                sh 'timedatectl'
            }
        }
    }
}
```

Here is another variation executing simple commands in a single stage:
```groovy
pipeline {
   agent any
   stages {
       stage('CMD') {
           steps {
               sh 'touch file1'
               sh 'pwd'       
           }
       }
   }
}
```

> [!WARNING]
> **Checking the Workspace:** When you run this pipeline, you cannot easily view the newly created files (`deployment`, `devops`) through the Jenkins UI workspace. **To verify them:** Go to the Console Logs of the build, copy the physical workspace path listed at the top, open your server terminal, and `cd` into that exact path!
> [!TIP]
> **Real-Time Best Practice:** It is highly recommended to use a single `sh` line for every command. If a command fails, Jenkins will pinpoint the exact line, making it much easier to debug!

**Method 2: Multi-line execution**
If you must run a large script, use three single quotes `'''` to execute multiple commands at a time:
```groovy
pipeline {
    agent any
    stages {
        stage("command") {
            steps {
                sh '''
                    touch siva
                    mkdir mydevops
                    cal
                    timedatectl
                '''
            }
        }
    }
}
```

Here is another variation of a multi-line execution:
```groovy
pipeline {
    agent any
    stages {
        stage("CMD") {
            steps {
                sh '''
                    touch file2
                    pwd
                    date
                    whoami
                '''
            }
        }
    }
}
```

### Lab C: Multi-Stage Pipeline Example
This is a standard multi-stage pipeline containing Code, Build, Test, and Deploy phases:
```groovy
pipeline {
   agent any
   stages {
       stage('Hello') {
           steps {
               echo 'Hello World'
           }
       }
       stage('Test') {
           steps {
               echo 'Hello World test'
           }
       }
       stage('Deploy') {
           steps {
               echo 'Hello World deploy'
           }
       }
   }
}
```

---

## 🚀 4. Real-Time CI/CD Pipeline (Zero to Hero)

Now let's build a real pipeline that fetches code from GitHub, builds it with Maven, and deploys it to Tomcat!

> [!NOTE]
> Ensure you have configured the global Maven tool (named `mymaven`), have the **Deploy to container** plugin installed, and have a running Tomcat server (from Day 4/6).

### Using the Pipeline Syntax Generator
You don't have to memorize complex syntax! At the bottom of your pipeline script box, click **Pipeline Syntax**. 
- Select **git: Git** from the sample steps dropdown.
- Enter the Repository URL (`https://github.com/devops0014/one.git`).
- Set the Branch to `master`.
- *(Since it's a public repository, you do NOT need to provide credentials).*
- Click **Generate Pipeline Script** and copy the resulting code!

> [!TIP]
> **Gotcha:** If you recently installed the "Deploy to container" plugin and you cannot find it inside the Pipeline Syntax generator dropdown, **you must restart your Jenkins server!** It will appear after the reboot.

**Example for Private Repositories:**
If you need to pull code from a private repository, the Syntax Generator will create code including your `credentialsId` like this:
```groovy
git branch: "main", credentialsId: "github", url: 'https://github.com/devops0014/one.git'
```

### Iteration 1: Testing the Source Code Pull
Create a new Pipeline job named `newdeploy` and paste this script to verify Jenkins can pull the code:
```groovy
pipeline {
    agent any
    stages {
        stage("Code") {
            steps {
                git 'https://github.com/sivagoram/one.git'
            }
        }
    }
}
```
Save and click **Build Now**. Once this succeeds, you can proceed to the full pipeline!

### Iteration 3: Setting up the Tomcat Server
Before we can deploy, we need a running Tomcat server! To avoid confusion and make this guide completely standalone, here is the exact script to provision your Tomcat server on a new EC2 instance (`t3.micro`):

```bash
# 1. Install Java
yum install java-17-amazon-corretto -y

# 2. Download and Extract Tomcat 9
wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.112/bin/apache-tomcat-9.0.112.tar.gz
tar -zxvf apache-tomcat-9.0.112.tar.gz

# 3. Configure Tomcat Users (Injecting roles and credentials)
sed -i '56 a\<role rolename="manager-gui"/>' apache-tomcat-9.0.112/conf/tomcat-users.xml
sed -i '57 a\<role rolename="manager-script"/>' apache-tomcat-9.0.112/conf/tomcat-users.xml
sed -i '58 a\<user username="tomcat" password="admin@123" roles="manager-gui, manager-script"/>' apache-tomcat-9.0.112/conf/tomcat-users.xml
sed -i '59 a\</tomcat-users>' apache-tomcat-9.0.112/conf/tomcat-users.xml
sed -i '56d' apache-tomcat-9.0.112/conf/tomcat-users.xml

# 4. Enable Remote Access (Remove IP restrictions)
sed -i '21d' apache-tomcat-9.0.112/webapps/manager/META-INF/context.xml
sed -i '22d' apache-tomcat-9.0.112/webapps/manager/META-INF/context.xml

# 5. Start the Server
sh apache-tomcat-9.0.112/bin/startup.sh
```
*(Make sure to open port `8080` in your Security Group!)*

### Iteration 4: The Final Deployment Script
Edit the `newdeploy` script one last time. Ensure you have the **Deploy to container** plugin installed in Jenkins.
```groovy
pipeline {
    agent any

    // Call the global Maven tool we configured in Jenkins
    tools {
        maven 'mymaven'
    }

    stages {
        stage("Code") {
            steps {
                // Fetch the code from GitHub
                git 'https://github.com/devops0014/one.git'
            }
        }

        stage("Build") {
            steps {
                // Compile and Package the application
                sh 'mvn clean package'
            }
        }

        stage("Deploy") {
            steps {
                // Deploy the generated .war file to Tomcat
                deploy adapters: [tomcat9(
                    alternativeDeploymentContext: '',
                    credentialsId: 'appserver'
                )]
            }
        }
    }
}
```
Save, hit **Build Now**, and watch your pipeline seamlessly pull code, build the artifact, and deploy it to the live server completely automatically!

---

## 🗄️ 5. Pipeline Variables

Pipelines allow you to define variables using the `environment {}` block.

### Local vs Global Variables
- **Global Variables** are defined at the very top of the pipeline and can be used in *every* stage.
- **Local Variables** are defined inside a specific stage and can *only* be used inside that stage.

```groovy
pipeline {
   agent any
   
   // GLOBAL VARIABLE
   environment {
      name = "Siva"
   }
   
   stages {
       stage('one') {
           steps {
               echo "My name is $name"
           }
       }
       stage('two') {
           // LOCAL VARIABLE
           environment {
              course = "DevOps"
           }
           steps {
               echo "$name is a $course trainer"
           }
       }
   }
}
```

### Pre-defined Jenkins Variables
Jenkins has built-in variables you can access anytime. For example, to print the current build execution number:
```groovy
pipeline {
   agent any
   stages {
       stage('ENV') {
           steps {
               sh 'echo "${BUILD_ID}"'
           }
       }
   }
}
```

> [!TIP]
> **Global Jenkins Variables via UI:**
> If you want to create a variable that can be accessed by *every single pipeline job* on your server, go to **Manage Jenkins » System » Global Properties**, check **Environment variables**, and pass the key-value pairs there!
