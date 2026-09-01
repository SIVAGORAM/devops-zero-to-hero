# Day 05: Image Management (Manual Creation & Docker Hub)

Welcome to Day 05! Up until now, we have been using default images provided by Docker Hub (like `centos`, `ubuntu`, `nginx`, `jenkins`). 

But in the real world, you don't run generic images. You run **your own code**. Today, we learn how to create our own custom Docker Images and share them with the world via Docker Hub.

There are two ways to create custom images:
1. **Manually** (Creating images from a running container) - *Today's focus.*
2. **Automated** (Using Dockerfiles) - *Tomorrow's focus.*

---

## 🏗️ 1. The Theory: Images as Layers

Think of a Docker image like building a house. You don't build the whole house at once; you build it in **layers**:
1. **Layer 1 (The Basement):** The Base Image (e.g., a barebones Ubuntu OS).
2. **Layer 2 (The Framing):** You run `apt update` and install some tools (like `vim`).
3. **Layer 3 (The Roof):** You add your specific application code (e.g., `index.html`).

When you extract (commit) this modified container, Docker saves all these layers together into a brand new Image!

---

## 🛠️ 2. Hands-On: The Manual Image Creation Process

Let's manually create our first custom image. We will follow a strict 5-step process.

### Step 1: Create a temporary container from a Base Image
We will start with a completely empty Ubuntu box running in the background.
```bash
docker run -d --name c1 ubuntu /bin/bash -c "while true; do echo hello; sleep 8; done"
```

### Step 2: Log into the temporary container
```bash
docker exec -it c1 /bin/bash
```

### Step 3: Perform your custom modifications
Now that we are inside, let's install `vim` and create a custom file.
```bash
apt update
apt install vim -y
vi index.html
# Add some text, save, and exit (:wq)
```

### Step 4: Exit the container
```bash
exit
```
*Our container `c1` now has our custom `index.html` inside it. Let's extract it!*

### Step 5: Extract (Commit) the Image
We use the `docker commit` command to convert the running container back into a reusable static Image.
**Syntax:** `docker commit <container_name> <new_image_name>`
```bash
docker commit c1 my_first_image
```

**Verify the Image exists:**
```bash
docker images
```
You will now see `my_first_image` in your local repository!

### 🧪 Prove it works!
Let's spin up a brand new container using our newly created image and see if our data is there:
```bash
docker run -it --name temp01 my_first_image /bin/bash
ls
cat index.html
```
*Success! Your `index.html` is permanently baked into the image.*

---

## ☁️ 3. Docker Hub: Sharing your Image with the World

Right now, `my_first_image` only exists on your specific EC2 hard drive. If the EC2 instance dies, the image is gone. 

We need to push it to a Centralized Repository: **Docker Hub**.

### Step 1: Login to Docker Hub
*(Prerequisite: Go to hub.docker.com and create a free account).*
From your EC2 terminal, run:
```bash
docker login -u <your_dockerhub_username>
```
*Enter your password when prompted. You will see "Login Succeeded".*

### Step 2: Tagging the Image (The Golden Rule)
Docker Hub has millions of images. If you just say `docker push my_first_image`, Docker Hub will reject it because it doesn't know *who* owns it. 

We use `docker tag` to add metadata to our image. It acts as a shipping label, telling Docker exactly which account repository to push it to.

**Syntax:** `docker tag <existing_image> <dockerhub_username>/<new_image_name>:<version_tag>`
```bash
docker tag my_first_image username/my_first_image:v1.0
```
Run `docker images` and you will see the newly tagged image.

### Step 3: Push the Image
Now, we push the labeled image up to the cloud! (This is very similar to `git push`).
```bash
docker push username/my_first_image:v1.0
```

### Step 4: Pushing New Versions
If you make more changes later, you don't need to create a whole new repository. You just bump the version tag!
```bash
docker tag my_first_image username/my_first_image:v2.0
docker push username/my_first_image:v2.0
```
Go to your Docker Hub dashboard in your browser, click on the repository, and you will see both the `v1.0` and `v2.0` tags safely stored in the cloud!

---

## 🚀 4. Advanced Practical: NGINX + Volumes + Port Mapping + Committing

Let's combine everything we learned in Day 04 and Day 05 into one ultimate exercise! We will host a custom login page using NGINX, map a volume, and save the final product as an image.

**Step 1: Start an NGINX container with Ports and Volumes**
```bash
docker run -d --name webpage -p 80:80 -v /home/ubuntu/webpage:/usr/share/nginx/html/ nginx
```
*(Troubleshooting: If Port 80 is occupied, use `lsof -i :80` and `kill -9 <PID>` to clear it, or use `-p 9090:80`).*

**Step 2: Add your custom code via the Volume**
Since the folder is mapped to our host, we don't even need to log into the container to change the code!
```bash
cd /home/ubuntu/webpage
vi login.html
# Add your custom Login Page HTML code, save, and exit.
```

**Step 3: Verify the Container picked it up**
```bash
docker exec -it webpage /bin/bash
cd /usr/share/nginx/html/
cat login.html
exit
```
Now, hit your EC2 IP address in your browser. You will see your beautiful custom login page!

**Step 4: Commit, Tag, and Push**
Let's save our custom web server as an image and push it to Docker Hub!
```bash
docker commit webpage custom_website
docker tag custom_website username/custom_website:v1.0
docker push username/custom_website:v1.0
```

---

## ⏭️ Looking Ahead to Day 06
While creating images manually with `docker commit` is great for learning, **we never do this in the real world**. 
Why? Because manual work is tedious, slow, and prone to human error. 

To automate this entire process from end-to-end, we write a script containing simple instructions. This is called a **Dockerfile**. We will master Dockerfiles in Day 06!
