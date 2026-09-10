# Jenkins Day 5: Maven Deep Dive (Zero to Hero)

Welcome to Jenkins Day 5! In Day 4, we used Maven inside Jenkins via a plugin to build our Java application. Today, we are stepping out of Jenkins for a moment to take a **deep dive into Maven itself**. 

As a DevOps engineer, you don't write Java code, but you *must* understand how Maven structures a project and how its lifecycle commands work!

---

## 🛠️ 1. Maven Installation (For Learning Purposes)

> [!NOTE]
> **Real-Time Scenario:** In the real world, you almost NEVER manually install Maven directly on the CI server via `yum`. You use Jenkins Plugins (Global Tool Configuration) to manage Maven versions safely. We are only installing it here manually on our EC2 instance to practice and understand how the tool works under the hood!

Run this on your Linux terminal to install Java and Maven:
```bash
# 1. Install Java 17
yum install java-17-amazon-corretto -y

# 2. Install Maven
yum install maven -y
```

---

## 🏗️ 2. Creating a Maven Project

Maven uses "Archetypes" (blueprints) to generate the skeletal structure of a Java project.

### The Command:
```bash
mvn archetype:generate
```

When you run this, Maven will ask you a series of questions to configure your project. You can press `Enter` to choose the default numbers, but you must provide two critical pieces of information:
- **`groupId:`** `siva` *(Usually represents the company or team name)*
- **`artifactId:`** `devops` *(Represents the specific project/application name)*

### The Project Structure
Run the `ll` command after generation:
```bash
ll
cd devops
```
You will see a new folder named after your `artifactId` (`devops`). If you look inside this folder, you will see two very important things:

1. **`src/` (Source Folder):**
   ```bash
   cd src
   ```
   - This is where the developers write their actual code.
   - Specifically, `main` (`src/main/`) holds the actual code, and `test` (`src/test/`) holds the unit tests.

2. **`pom.xml` (Project Object Model):**
   - **This is the most important file in Maven!** 
   - It contains all the project configurations and **dependencies** required to build and test the application.
   - Developers are responsible for updating this file, but as a DevOps engineer, you must know what it is and how to read it.

---

## ⚙️ 3. The Maven Core Commands

Once the project is created, you must navigate into the project directory (`cd devops`) to run Maven commands against the `pom.xml`.

Here are the absolute core commands you need to know:

### 1. `mvn compile`
- **What it does:** Compiles the raw Java source code into executable bytecode.
- **The Result:** It generates a brand new folder called `target/`. 
```bash
cd target
cat app.class
```
*(You will see the compiled output of the application!)*

### 2. `mvn test`
- **What it does:** Runs the unit tests written by the developers to check for bugs.
- **The Result:** It generates extra testing reports and folders inside the `target/` directory.

### 3. `mvn package`
- **What it does:** Bundles your compiled code and all your dependencies together.
- **The Result:** It creates the final deployable artifact (the `.jar` or `.war` file) inside the `target/` directory!

### 4. `mvn install`
- **What it does:** Reads the `pom.xml` file and installs all the required dependencies locally so the application can run.

### 5. `mvn clean`
- **What it does:** Deletes the entire `target/` directory.
- **The Result:** It completely clears out all previous builds, compiled classes, test results, and artifacts, giving you a fresh slate for the next build.

---

## 🔄 4. The Maven Lifecycle Cascade (Crucial Interview Concept)

You do not need to run every command one by one (`mvn compile`, then `mvn test`, then `mvn package`).

Maven operates on a **Lifecycle Cascade**. If you call a command further down the lifecycle, **Maven will automatically run every step before it!**

Look at this cascade:
- **`mvn test`** ➔ Runs: `Compile + Test`
- **`mvn package`** ➔ Runs: `Compile + Test + Package`
- **`mvn install`** ➔ Runs: `Compile + Test + Package + Install`

*(This is why in Day 4, our Jenkins pipeline only needed to run `clean package`! It automatically handled compiling and testing before packaging the `.war` file).*
