# Day 07: Dockerfiles in the Real World (Node.js & Python)

Welcome to Day 07! Yesterday, we learned the individual instructions of a Dockerfile. Today, we put them together to containerize two real-world applications: a **Node.js API** and a **Python Banking App**. 

By the end of today, you will understand exactly how Developers and DevOps engineers package code into deployable artifacts!

---

## 🏗️ 1. The Build Process (A Quick Primer)

Before we containerize, you must understand how code becomes a running application. Different languages use different package managers (Build Tools) to download dependencies and build executable artifacts:
- **Node.js** $\rightarrow$ Uses `npm`
- **Python** $\rightarrow$ Uses `pip`
- **Java** $\rightarrow$ Uses `maven` or `gradle`
- **C/C++** $\rightarrow$ Uses `cmake`

When we write a Dockerfile, we are essentially telling Docker which build tool to run to generate our final executable (the deployable artifact).

**The Phone Factory Analogy:** Think of the source code as raw metal and glass. The Build Tool (`npm`, `pip`) is the factory machine. The final Executable/Artifact/Binary file is the fully assembled smartphone (deployable product). The Dockerfile simply automates the factory!

---

## 🟢 2. Practical 1: Containerizing a Node.js Application

Let's build a simple Node.js web server from scratch and then containerize it.

### Step 1: Create the Local App
Log into your EC2 instance and switch to the root user (`sudo su`). Let's create the app locally first.
```bash
mkdir my-node-app
cd my-node-app
npm init -y
npm install express
```
Now, create the application file:
```bash
vi index.js
```
Paste this exact code, save, and exit:
```javascript
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
    res.send("Hello, Docker!");
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
```
*(You can test it locally by running `node index.js`, then press `Ctrl+C` to stop it).*

### Step 2: Write the Dockerfile
Now, let's containerize it. In the same folder, create a file named exactly `Dockerfile`.
```bash
vi Dockerfile
```
Paste the following instructions. **Read the comments carefully to understand *why* we write each line:**
```dockerfile
# 1. Base Image: Use the official Node.js image with pre-installed 'npm'
FROM node:16

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Cache Trick: Copy ONLY the package files first
# Why? If dependencies haven't changed, Docker will cache the 'npm install' step, saving massive time!
COPY package*.json ./

# 4. Install the dependencies inside the container using the build tool
RUN npm install

# 5. Copy the actual application code (index.js) into the container
COPY . .

# 6. Documentation: Expose the port the app runs on
EXPOSE 3000

# 7. Start Command: How to launch the app when the container wakes up
CMD ["node", "index.js"]
```

### Step 3: Build & Run
Let's build the image and spin up the container!
```bash
docker build -t my-node-app .
docker run -d -p 3000:3000 my-node-app
```
**Important:** Go to your AWS Security Group and open **Port 3000**. Hit your EC2 IP address in the browser on port 3000, and you will see "Hello, Docker!" running natively from the container!

---

## 🐍 3. Practical 2: Containerizing a Python (Flask) Application

Now let's do the exact same workflow for a Python application. Notice how the Dockerfile structure remains almost exactly the same, but the *tools* change!

### Step 1: Create the Local App
```bash
cd ~
mkdir my-banking-app && cd my-banking-app
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip
```

Create the Python file:
```bash
vi app.py
```
Paste this code, save, and exit:
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', title="Banking App - Home")

@app.route('/about')
def about():
    return render_template('about.html', title="Banking App - About")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Create the HTML templates:
```bash
mkdir templates
cd templates

# Create home.html
echo "<h1>Welcome to the Bank</h1>" > home.html

# Create about.html
echo "<h1>About us</h1>" > about.html

cd ..
```

### Step 2: Write the Dockerfile
Create the `Dockerfile` inside `my-banking-app`.
```dockerfile
# 1. Base Image: Use the official lightweight Python image
FROM python:3.9-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy all code (app.py and the templates folder) into the container
COPY . .

# 4. Use the Python build tool (pip) to install the required framework
RUN pip install flask

# 5. Documentation: Expose the Flask port
EXPOSE 5000

# 6. Start Command
CMD ["python", "app.py"]
```

### Step 3: Build & Run
```bash
docker build -t banking-app .
docker run -d -p 5000:5000 banking-app
```
**Important:** Go to your AWS Security Group and open **Port 5000**. Hit your EC2 IP address in the browser, and your Banking App is live!

---

## 🧠 4. Deep Dive: Docker in the SDLC & Best Practices

At the end of class, we discussed some critical high-level concepts for interviews.

### Where do Dockerfiles fit into the Agile SDLC?
In a standard Software Development Life Cycle (Agile), the Dockerfile sits squarely in the **Build Phase** (Continuous Integration).
1. **Code:** Developers write the code (`index.js`).
2. **Build (The Dockerfile):** A CI/CD pipeline (like Jenkins) reads the Dockerfile, runs the dependencies, and outputs a static, deployable Docker Image (the Artifact).
3. **Deploy:** The container orchestration system (like Kubernetes) takes that Image and runs it across hundreds of servers.

### Multi-Stage Dockerfiles (Advanced Concept)
Sometimes, building an application requires heavy tools (like compilers) that you don't actually need to *run* the app. 
A **Multi-stage Dockerfile** uses multiple `FROM` instructions. The first stage builds the executable using heavy tools, and the second stage copies *only* the final executable into a tiny, lightweight production image. This keeps your images incredibly small and secure!

### Dockerfile Best Practices
1. **Always use specific tags:** Never use `FROM node:latest`. Always pin the version like `FROM node:16` to prevent unexpected breaking changes.
2. **Order matters for Caching:** Always copy your dependency files (like `package.json`) and run your installations (`npm install`) **before** copying the rest of your source code. If you change a single line of your source code, Docker won't have to rebuild the entire dependency tree!
3. **Minimize Layers:** Combine multiple `RUN` commands using `&&` to reduce the number of layers in the final image.
