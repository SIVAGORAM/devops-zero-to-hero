# Day 06: Automating Image Creation with Dockerfiles

Welcome to Day 06! Yesterday, we learned how to create a custom Docker Image manually by starting a container, logging into it, making changes, and using `docker commit`. 

While that is great for learning, **we never do that in the real world.** Manual work is slow, tedious, and prone to human error. Today, we learn the 3rd and final way to create images: **Automated Image Creation using Dockerfiles.**

A Dockerfile is simply a text document containing all the commands a user could call on the command line to assemble an image. 

---

## 🏗️ 1. The Core Instructions

In a Dockerfile, the instructions (the action words) are always written in **CAPITAL LETTERS**, followed by the arguments in lowercase. 

Here are the most critical instructions you will use every day:

| Instruction | What it does | Example |
| :--- | :--- | :--- |
| **FROM** | Defines the base image. This **must** be the very first instruction in every Dockerfile. | `FROM ubuntu` |
| **RUN** | Executes Linux operating system commands (like installing packages) during the image *build* phase. | `RUN apt install -y vim` |
| **COPY** | Copies files or directories from your EC2 Host machine directly into the Docker Image. | `COPY index.html /var/www/html/` |
| **ADD** | Very similar to COPY, but has extra features (it can extract `.tar` files automatically or copy from a URL). | `ADD https://example.com/file.txt /app/` |
| **WORKDIR** | Changes the directory inside the image. (Exactly like running the `cd` command). | `WORKDIR /var/www/html` |
| **EXPOSE** | Documents the port that the container will listen on. (Note: This is just documentation, you still need `-p` to actually map it). | `EXPOSE 80` |
| **USER** | Sets the specific user that will run the following commands (for security purposes). | `USER siva` |
| **ENV** | Sets environment variables inside the container. | `ENV DB_PORT=3306` |
| **MAINTAINER** | Defines the author/owner of the Dockerfile. | `MAINTAINER siva@example.com` |

---

## ⚔️ 2. The Interview Classic: CMD vs ENTRYPOINT

Both `CMD` and `ENTRYPOINT` are used to define the **very first command** that executes when the container wakes up. But they behave very differently. If you go to a DevOps interview, you *will* be asked this difference.

### 1. CMD (Command)
- **Theory:** Provides a default executable.
- **The Catch:** If the user provides a command when running `docker run`, **the user's command will OVERRIDE the CMD.**
- **Example:** If your Dockerfile has `CMD ["/bin/bash"]`, and the user types `docker run my_image ls`, the container will run `ls` and completely ignore `/bin/bash`.

### 2. ENTRYPOINT
- **Theory:** Makes the container run like a strict executable.
- **The Catch:** It **CANNOT be overridden** by the user. Anything the user types at the end of `docker run` is simply passed as an *argument* to the Entrypoint.
- **Example:** If your Dockerfile has `ENTRYPOINT ["sleep"]`, and the user types `docker run my_image 10`, the container will execute `sleep 10`.

---

## 🛠️ 3. Hands-On: Your First Dockerfile

Let's automate what we did yesterday. 

**Important Rule:** The file must be named exactly `Dockerfile` with a capital 'D' and **no file extension** (not `.txt`, not `.sh`).

### Step 1: Create the file
```bash
sudo su
vi Dockerfile
```

### Step 2: Write the instructions
Paste this code into the file, save, and exit:
```dockerfile
FROM ubuntu
RUN apt update
RUN apt install -y vim
RUN touch index.html
```

### Step 3: Build the Image
We use the `docker build` command. 
*(Remember: `docker commit` creates images from running containers. `docker build` creates images from Dockerfiles).*

**Syntax:** `docker build -t <image_name> <path_to_dockerfile>`
```bash
docker build -t test_image .
```
*(The `.` at the end is absolutely critical. It tells Docker "the Dockerfile is in my present working directory").*

### ⚡ The Power of Caching
If you immediately run `docker build -t test2 .` again, you will notice it finishes in 1 second! 
Why? Because Docker images are built in **layers**. Docker's Daemon is smart enough to realize that none of the instructions changed, so it just reused the cached layers from the memory!

---

## 🔐 4. Hands-On: The USER Instruction

By default, Docker runs everything as the `root` user. This is a massive security risk. Let's create an image that creates a user and switches to it.

1. Wipe your old Dockerfile: `> Dockerfile`
2. Open it: `vi Dockerfile` and paste:
```dockerfile
FROM ubuntu
RUN useradd -m siva
USER siva
RUN whoami
```
3. Build it: `docker build -t secure_image .`
When you watch the build process on your screen, you will see the `whoami` command output `siva` instead of `root`!

---

## 🚀 5. Advanced Practical: Automating a Web Server (Apache)

Let's write a real-world Dockerfile. We will install an Apache web server, change the directory, copy a local HTML file into the container, expose port 80, and start the server!

1. Create a quick custom webpage on your host machine:
```bash
echo "<h1>Welcome to my Automated Server!</h1>" > index.html
```
2. Open your Dockerfile (`vi Dockerfile`) and paste this beautiful automated script:
```dockerfile
FROM ubuntu
RUN apt update
RUN apt install -y apache2
WORKDIR /var/www/html
RUN rm -f index.html
COPY index.html /var/www/html/
EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]
```
*(The `CMD` instruction here tells Apache to run in the foreground so the container doesn't immediately exit and die).*

3. Build the Masterpiece!
```bash
docker build -t my_web_server .
```

4. Run the Container using Port Mapping!
```bash
docker run -d --name web -p 80:80 my_web_server
```

Now, go to your browser and hit your EC2 IP Address. You will see your custom web server running beautifully! 

You just went from Zero to Hero in Docker Automation!
