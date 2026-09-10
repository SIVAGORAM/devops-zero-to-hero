# Jenkins Day 10: Parameters, Variables, and ThinBackup

Welcome to Day 10! As you build more complex pipelines, hardcoding values (like branch names or cloud providers) becomes a major bottleneck. Today, we will master **Parameters** and **Variables** to make our pipelines dynamic and reusable. 

Finally, we will implement **ThinBackup** to ensure we never lose our Jenkins data if disaster strikes.

Let's dive in from zero to hero!

---

## 🚀 STEP 0: Launch Jenkins
Before starting, launch the instance for the Jenkins by giving all the details and install the Jenkins in the server similar to previous classes. Login to your Jenkins and install the plugins, fill all the details, and click on start using Jenkins.

---

## 🎛️ 1. Parameters in Jenkins

### The Problem: Hardcoding Branches
Go to pipelines: write the script of pipeline give the repo url and write the script pipeline syntax configure all the thing and build. After sometime your manager comes and asks for a change in the branch. You are going and changing the branch name and again building. Again and again if you want to change the branch name this is manual work!

### The Solution: Parameterized Projects
To make it automated we have an option. Go to general and check that box:- **This project is parameterised**. For passing we use this like a menu for building.

### Implementing a Parameterized Pipeline
1. Go to your Job configuration.
2. Under the **General** tab, check the box: **This project is parameterised**.
3. Click **Add Parameter** and select **Choice Parameter**.
   - **Name:** `mybrnach`
   - **Choices:** (inside this give all the branches)
     ```text
     main
     master
     azure
     gcp
     master
     ```
4. Save it. Now go to the pipeline syntax script and give this as a variable there.

```groovy
pipeline {
    agent any

    stages {
        stage("Code") {
            steps {
                git branch: '$mybrnach', url: 'https://github.com/sivagoram/one.git'
            }
        }
    }
}
```

Now go to **Build with Parameters**, you will see the field with the `mybrnach`. Select the branch and click on build. Whatever you select, that branch code will come and build!

---

### String Parameters
Before, if you don't know the branch name, you have another option called **strong parameter** (String Parameter).
1. Go to general click on add parameters.
2. Select the string parameters.
3. Give the name: `mybrnach` and click on save.
4. Go to build with parameters:- type `main` and click on build. It will call it and build it like that you can enter the branch name. This parameter is very important, understand them!

### Other Parameters
- **Multi-line String Parameters:** To pass multiple lines use multiline string parameters for passing multiple line string parameters.
- **File Parameters:** From your laptop local to get into your ci server you will use this file parameters, configure it and select it, you will see that file in your server.

---

## 🧩 2. Variable Assignment and Calling

Variable assignment and calling: inside the `agent any` you should declare the environment and declare the variable. Inside the stages or steps assign call the variable using the `$` and variable name.

### Basic Variable Assignment
```groovy
pipeline {
    agent any

    environment {
        course = "DevOps"
    }

    stages {
        stage('MyStage') {
            steps {
                echo "I am learning $course"
            }
        }
    }
}
```

### Passing Multiple Variables
```groovy
pipeline {
    agent any

    environment {
        course = "DevOps"
        cloud = "AWS"
        duration = 4
    }

    stages {
        stage('MyStage') {
            steps {
                echo "I am learning $course with $cloud from last $duration months"
            }
        }
    }
}
```

---

## 🌐 3. Types of Variables (Global vs Local)

It is critical to deeply understand the scope of your variables. 

### Global Variables
Variables declared in an `environment` block at the very top of the `pipeline` are **GLOBAL**. They can be accessed by *all* stages.

### Local Variables
Variables declared in an `environment` block inside a specific `stage` are **LOCAL**. They can *only* be accessed within that specific stage.

### Understanding the Scope
```groovy
pipeline {
    agent any

    // GLOBAL variable
    environment {
        cloud = "AWS"
    }

    stages {

        stage("Code") {
            environment {
                // LOCAL variable
                course = "DevOps"
            }

            steps {
                echo "I am learning $course from $cloud"
            }
        }

        stage("Build") {
            steps {
                echo "Cloud is $cloud"

                // course is NOT available here
                // because course is local to Code stage
            }
        }
    }
}
```

### How it Works (Visualized)
```text
GLOBAL: cloud = "AWS" (Available everywhere)
          ↓
          ┌─────────────────────┐
          │ Code Stage          │
          │ course = "DevOps"   │ ← LOCAL
          │                     │
          │ $cloud  → AWS       │
          │ $course → DevOps    │
          └─────────────────────┘
                    ↓
          ┌─────────────────────┐
          │ Build Stage         │
          │                     │
          │ $cloud → AWS        │
          │ $course → ❌ Error! │
          └─────────────────────┘
```

> [!IMPORTANT]  
> **Interview Question:** What is the difference between global and local environment variables in Jenkins?  
> **Answer:** A global environment variable is defined at the pipeline level and can be accessed by all stages. A local environment variable is defined inside a particular stage and is available only within that stage.

### System-Wide Global Variables
You can access local and global variables inside the pipeline. If you want to access these variables in some other pipelines, you should go to managing instance, then go to the system, check the box environment variables, click on add and add the name and value there.

Like that you can add and use them in any pipeline. Wherever you use that keyword name with `$` symbol you will get it in that pipeline. In any pipelines you can access this globally!

### Default Jenkins Variables
By default we have some default variables. Jenkins provides them automatically. To see a list of them, run the `printenv` command:

```groovy
pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                sh 'printenv'
            }
        }
    }
}
```
Go to console logs for output to see the massive list of variables available to you! 

If you want to print the job name and jenkins urls:
```groovy
pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                echo "my job name is $JOB_NAME and url is $JENKINS_URL"
            }
        }
    }
}
```

---

## 💾 4. ThinBackup and Restore

All information about the Jenkins whatever we downloaded like builds, plugins installed, like more everything is stored in some path:
```bash
cd /var/lib/jenkins
ll
```

Everything is stored here. If anything is deleted this is issues! So I am taking this backup automatically. If anything is deleted I can restore from the backup. Let's implement it practically!

### Step 1: Install the Plugin
For this you need a plugin download it.
1. Go to **Manage Jenkins** to **Plugins**.
2. Search for **ThinBackup**, select it, and download it.

### Step 2: Configure the Backup Directory
Before we configure Jenkins, we must create a directory on the Linux server to store the backups, and give Jenkins ownership of it.
Go to your Jenkins server terminal:
```bash
cd /opt/
ll
mkdir mybackup

# By default owner is root user
chown -R jenkins:jenkins mybackup
```

### Step 3: Configure ThinBackup
1. Go to **Manage Jenkins** again.
2. Click on **System**.
3. Search for **ThinBackup Configuration**.
4. **Backup directory:** Enter `/opt/mybackup` (where you need to store this backup).
5. Go down after giving the path of the directory, move down.
6. Tick that box: **Move old backup to zip files** (to save the storage old backups in zip files).
7. Click **Save**.

### Step 4: Taking a Backup
1. Now go to **Manage Jenkins**.
2. Go down click on **ThinBackup**.
3. Click on **Backup Now**.
4. Inside your default backups you can see that backup file in your server terminal:
   ```bash
   cd /opt/mybackup
   ll
   ```
   *Logs representation:* `/var/lib/Jenkins/data ----backup-----> /opt/mybackups/data`

If you made some changes, again you went to thinbackup and taken the backup, now go to the path where it storing. You can see that old data is stored in zip file, new data in folder automatically to save memory because we tick that option called move old backup to zip files!

### Step 5: Restoring a Backup
Let's simulate a disaster. Go to your main data directory and delete the critical `config.xml` file!
```bash
cd /var/lib/jenkins
rm -f config.xml
```

To restore it:
1. Go back to the dashboard.
2. Under **ThinBackup**, click on **Restore**.
3. Select the most recent backup from the dropdown.
4. Click **Restore**. Your `config.xml` is back safely!

### Step 6: Automating the Backup
Can we make this backup automatic without any manual work? Yes!
1. Go to **Manage Jenkins** -> **System**.
2. Go to **Backup schedule for full backups**.
3. Provide a cron syntax schedule.
4. Save it. Jenkins will now run backups automatically based on your schedule!
