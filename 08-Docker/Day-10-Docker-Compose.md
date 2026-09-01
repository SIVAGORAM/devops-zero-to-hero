# Day 10: Docker Compose (Zero to Hero)

## ⚠️ The Problem: "The Multi-Container Nightmare"

So far, you have learned how to build and run a single container. But what happens when you need to deploy a real-world application? 

Modern applications are rarely just one container. A typical web application requires:
1. A Frontend Container (e.g., React/Nginx)
2. A Backend API Container (e.g., Python/Node.js)
3. A Database Container (e.g., PostgreSQL/MySQL)

To start this application manually, you would have to run three massive, complex commands in your terminal, making sure you create the network first, link the volumes, and pass all the correct environment variables:

```bash
# This is a nightmare to manage manually!
docker network create my_app_net
docker run -d --name db --network my_app_net -v db_data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret mysql:5.7
docker run -d --name backend --network my_app_net -p 8080:8080 -e DB_HOST=db my_backend_api
docker run -d --name frontend --network my_app_net -p 80:80 my_frontend
```
If you reboot your server, you have to type all of that again. If you make a typo, the application breaks. 

## 🛠️ The Solution: Docker Compose

**Docker Compose** is a tool that allows you to define and manage multi-container applications using a single, simple YAML file (`docker-compose.yml`). 

Think of it as **Infrastructure as Code** for Docker. Instead of running imperative commands in the terminal, you declare exactly what your environment should look like in a file, and Docker handles spinning it all up (and tearing it down) with a single command!

---

## 🏗️ The 3 Pillars of Docker Compose

Every `docker-compose.yml` file is built around three main concepts:

1. **Services:** These are the actual containers you want to run (e.g., the database, the web server).
2. **Networks:** The private networks that allow your services to talk to each other securely. (Compose automatically creates a default bridge network for you!)
3. **Volumes:** The storage areas where your databases or apps save their persistent data.

---

## 🚀 Practical Example: Deploying WordPress & MySQL

Let's look at a real-world example. We are going to deploy a full WordPress website backed by a MySQL database. 

Create a file named `docker-compose.yml` and paste the following code into it:

```yaml
version: '3.8'

services:
  # Service 1: The Database
  db:
    image: mysql:5.7
    volumes:
      - db_data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: mysecretpassword
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress_password

  # Service 2: The Web Application
  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    ports:
      - "8000:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress_password
      WORDPRESS_DB_NAME: wordpress

volumes:
  db_data:
```

### 🧠 Code Breakdown (Line by Line)

- `version: '3.8'`: Tells Docker which version of the Compose syntax we are using.
- `services:`: The start of our container definitions.
- `db:` and `wordpress:`: These are the names of our containers. Because of Docker Networking (which we learned in Day 08), the WordPress container can literally talk to the MySQL container by just pinging the hostname `db`!
- `depends_on:`: Tells Docker to wait and start the `db` container *before* starting the `wordpress` container.
- `environment:`: Passes crucial environment variables (like passwords) directly into the container at boot time.
- `volumes:` (at the bottom): Explicitly creates a named volume called `db_data` so if the database container dies, your blog posts aren't deleted!

---

## 💻 Essential Docker Compose Commands

Once you have your `docker-compose.yml` file saved, navigate to that directory in your terminal and use these commands:

### 1. Spin Everything Up
```bash
docker-compose up -d
```
*What it does:* Reads the YAML file, downloads the images, creates the network, creates the volumes, and starts all containers in the background (`-d`). 

### 2. View Running Services
```bash
docker-compose ps
```
*What it does:* Shows only the containers that are managed by the current `docker-compose.yml` file.

### 3. View The Logs
```bash
docker-compose logs -f
```
*What it does:* Streams the terminal output (logs) of ALL your services at the same time. Crucial for troubleshooting!

### 4. Tear Everything Down
```bash
docker-compose down
```
*What it does:* Gracefully stops all containers, and deletes the containers and the default network. *(Note: It deliberately does NOT delete your volumes, protecting your data!)*

---

## 🏆 Summary

With Docker Compose, you no longer need to memorize huge CLI commands. You simply write your architecture into a file, commit it to GitHub, and anyone on your team can spin up your entire production environment by typing `docker-compose up -d`. You are now officially a Docker Hero!
