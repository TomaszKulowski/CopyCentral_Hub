# CopyCentral Hub

## Table of Contents
   1. [Description](#description)
   2. [Online Demo](#online-demo)
   3. [Applications](#applications)
   4. [Setup](#setup)
      1. [Docker](#docker)
         1. [Using Pre-Built Docker Images from Docker Hub](#using-pre-built-docker-images-from-docker-hub)
         2. [Building Docker Images Manually](#building-docker-images-manually)
      2. [Local Setup](#local-setup)


## Description

CopyCentral Hub is a web application developed using Django,
designed specifically for managing service orders.
The application offers a range of features to streamline order-related processes,
including managing users, customers, devices, employees, history, information, notifications,
and other relevant aspects.


## Online Demo

You can try out a live version of the application for testing purposes at the following link:

- [CopyCentral Hub](http://copycentralhub.com)

**Login credentials for the demo:**
- **Username:** admin
- **Password:** admin

Please note that all data on the demo server is reset every hour, so any changes made will not persist.


## Applications

- **authentication**: Manages users and authentication.
- **customers**: Manages customer information.
- **devices**: Manages devices.
- **employees**: Manages employees.
- **history**: Records and manages action history.
- **informations**: Stores and manages various information.
- **notifications**: Handles notifications to users.
- **order_management**: Manages the order process.
- **order_review**: Allows for reviewing and evaluating orders.
- **orders**: Manages orders.
- **services**: Manages available services in the system.


## Setup

### Docker

Ensure that Docker is installed on your machine.
You can download and install Docker from the [official Docker website](https://www.docker.com/get-started).

Follow these steps to set up and run the Dockerized application:

#### Using Pre-Built Docker Images from Docker Hub

1. **Download `compose_images.yml`**

   Obtain the `compose_images.yml` file, which contains the Docker Compose configuration for the application.

2. **Create Environment Files**

   Create two environment files in the root directory of your project:

   - `.env.prod`: This file should contain production environment variables.
   Use the `.env.prod.example` file as a reference to configure it.

   - `.env-prod.db`: This file should contain database-specific environment variables.
   Use the `.env-prod.db.example` file as a reference to configure it.

3. **Run Docker Compose**

   Once you have the environment files in place, you can start the Docker containers with the following command:

   ```bash
   docker-compose -f compose_images.yml up
   ```

4. **Access the Application**

   After running the above command, the application should be up and running.
   You can access it by entering http://localhost in your web browser.


#### Building Docker Images Manually

If you prefer to build the Docker images yourself, follow these additional steps:

1. **Clone the Repository**

   Clone the project repository to your local machine:

   ```bash
   git clone https://github.com/TomaszKulowski/CopyCentral_Hub.git
   cd CopyCentral_Hub
   ```

2. **Create Environment Files**

   Create two environment files in the root directory of your project:

   - `.env.prod`: This file should contain production environment variables.
   Use the `.env.prod.example` file as a reference to configure it.

   - `.env-prod.db`: This file should contain database-specific environment variables.
   Use the `.env-prod.db.example` file as a reference to configure it.

3. **Run Docker Compose**

   Use the compose.yml file provided in the repository to build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```
   This command will build the Docker images from the source code and start the containers.

4. **Access the Application**

   After running the above command, the application should be up and running.
   You can access it by entering http://localhost in your web browser.


### Local Setup
Follow these steps to set up the application without using Docker:

1. **Prerequisites**

   Make sure you have the following prerequisites installed before setting up the project:
      - Python 3.11 or higher

2. **Clone the Repository**
   ```bash
   git clone https://github.com/TomaszKulowski/CopyCentral_Hub.git
   cd CopyCentral_Hub
   ```

3. **Create Environment Files**

   Create two environment files in the root directory of your project:

   - `.env.prod`: This file should contain production environment variables.
   Use the `.env.prod.example` file as a reference to configure it.

   - `.env-prod.db`: This file should contain database-specific environment variables.
   Use the `.env-prod.db.example` file as a reference to configure it.

4. **Install Dependencies**

   Install the necessary dependencies using the following command:
   ```
   pip install -r requirements.txt
   ```

5. **Run Development Server**

   Run the development server with:
   ```
   python manage.py runserver 0.0.0.0:80
   ```

6. **Access the Application**

   After running the above command, the application should be up and running.
   You can access it by entering http://localhost in your web browser.

