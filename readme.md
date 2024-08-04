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
   5. [Admin Panel](#admin-panel)
      1. [Admin Panel Features](#admin-panel-features)
   6. [Application Features](#application-features)
      1. [Main Page](#main-page)
      2. [Features for Office Staff/Order Managers](#features-for-office-stafforder-managers)
      3. [Features for All Employees](#features-for-all-employees)
   7. [Testing](#testing)
      1. [Data Generation Commands](#data-generation-commands)
      2. [Coming Soon](#coming-soon)


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

#### Using Pre-Built Docker Images from Docker Hub

1. **Download `compose_images.yml`**

   Obtain the `compose_images.yml` file from the repository.
   You can find it [here](https://github.com/TomaszKulowski/CopyCentral_Hub/blob/main/compose_images.yml).

2. **Create Environment Files**

   Create two environment files in the root directory of your project:

   - `.env.prod`: This file should contain production environment variables.
   Use the [`.env.prod.example`](https://github.com/TomaszKulowski/CopyCentral_Hub/blob/main/.env.prod-example)
   file as a reference to configure it.

   - `.env-prod.db`: This file should contain database-specific environment variables.
   Use the [`.env-prod.db.example`](https://github.com/TomaszKulowski/CopyCentral_Hub/blob/main/.env.prod.db-example)
   file as a reference to configure it.

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
   Use the [`.env.prod.example`](https://github.com/TomaszKulowski/CopyCentral_Hub/blob/main/.env.prod-example)
   file as a reference to configure it.

   - `.env-prod.db`: This file should contain database-specific environment variables.
   Use the [`.env-prod.db.example`](https://github.com/TomaszKulowski/CopyCentral_Hub/blob/main/.env.prod.db-example)
   file as a reference to configure it.

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
   Use the [`.env.prod.example`](https://github.com/TomaszKulowski/CopyCentral_Hub/blob/main/.env.prod-example)
   file as a reference to configure it.

   - `.env-prod.db`: This file should contain database-specific environment variables.
   Use the [`.env-prod.db.example`](https://github.com/TomaszKulowski/CopyCentral_Hub/blob/main/.env.prod.db-example)
   file as a reference to configure it.

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


## Admin Panel

For administrative tasks, such as managing users, viewing application data, and configuring the system,
you can access the admin panel.

- **Admin Panel URL:** [http://localhost/admin](http://localhost/admin)

**Default Admin Credentials for Demo:**
- **Username:** admin
- **Password:** admin

### Admin Panel Features

In the admin panel, you can perform the following tasks:

- **User Management**
  - Manage users
  - Send password reset links to users' emails

- **Employee Management**
  - Add and remove employees
  - Each employee is associated with a user account and has additional details such as
  department, phone number, and a CSS color for map orders

- **Information Section**
  - Enter and manage information displayed on the main page of the application

- **Notifications**
  - **Notification Settings**
    - Configure SMS notification settings, requiring an SMS API server with parameters such as
    auth token, phone number, and message
    - Enter the SMS server details, auth token, message template,
    notification type (currently only new order notifications are supported),
    and delay time (interval for checking new orders for each employee)
  - **Notification Logs**
    - View sent notifications

- **Orders**
  - **Regions**
    - Manage regions for orders
  - **Short Descriptions**
    - Manage brief descriptions of orders

To access the admin panel, navigate to `/admin` after starting the application
and log in with the provided credentials. For production use, make sure to update the admin password
and configure appropriate permissions.


## Application Features

### Main Page

The main page displays information added in the admin panel's **Informations** section.
From the main page, you can access settings to:
- Change the language (supported languages: Polish and English)
- Toggle between dark mode and light mode

### Features for Office Staff/Order Managers

- **Order Management**
  - **Main Section**: Displays all active orders with filtering and searching capabilities.
  - **Employees Orders**: Shows all orders assigned to a specific employee with options to reorder.
  - **Regions Orders**: Orders are categorized by region.
  - **Orders Settlement**: Provides necessary data for invoicing and order settlement.
  - **Orders Map**: A map view of orders with pins indicating order locations.
  The color of each pin corresponds to the employee's color set in the admin panel.
  Orders with incorrectly loaded addresses are shown at coordinates (0,0).

- **Order Review**
  - **Main Section**: Contains all completed/cancelled/settled orders.
  Orders can be approved or marked for review as 'to review'.
  - **Orders for Review**: Displays orders marked as 'to review'.

### Features for All Employees

- **My Orders**
  - Displays active orders assigned to the logged-in employee.

- **Service Orders**
  - Shows all orders in the application, including completed, settled, and cancelled ones.
  - Allows for order searching.
  - Each order includes:
    - Client and payer selection
    - Order details with information about the date of addition and modification
    - Options to assign an employee, change order type, priority, status, select region,
    add a brief description, additional information, and capture the signature and name of the person
    receiving the order
    - Detailed order information including device information, fault description, performed services,
    and an attachment section for PDF files or images
  - In browsing mode, you can:
    - Download the order report in PDF format
    - Send the PDF report to the client’s email
    - Check the order change history

- **Services**
  - A collection of services and pricing for orders.
  - **Brands List**: Enter device brands.
  - **Models List**: Enter device models.
  - Services can be added to the above data or listed as basic services without specific brands or models.
  - In browsing mode, you can view the change history of a service.

- **Customers**
  - Manages clients added to the database.
  - Each customer has a **Additional Addresses List** section for additional addresses.
  - In browsing mode, you can view the change history and all orders associated with a customer.

- **Devices**
  - Displays serviced devices.
  - In browsing mode, you can view the change history of a device
  and check the order history where the device data was recorded.


## Testing

Automated tests are crucial to ensure the stability and reliability of the application.
We are currently in the process of developing comprehensive test suites for CopyCentral Hub.

### Available Now

To facilitate testing, we currently provide a set of factories designed to generate fake data:

- **UserFactory**
- **CustomerFactory**
- **AdditionalAddressFactory**
- **DeviceFactory**
- **EmployeeFactory**
- **InformationFactory**
- **NotificationFactory**
- **OrderReviewFactory**
- **OrderServiceFactory**
- **RegionFactory**
- **ShortDescriptionFactory**
- **OrderFactory**
- **BrandFactory**
- **ModelFactory**
- **ServiceFactory**

These factories can be used to create instances of your models populated with synthetic data.
This setup allows for effective testing and development without the need for manual data entry.

### Data Generation Commands

To efficiently populate your database with fake data, we provide several management commands.
The `-n` option specifies the number of objects to be created.

#### Commands

- `python manage.py add_fake_customers -n <number>`  
  Adds `<number>` fake customer records.


- `python manage.py add_fake_customers_with_address -n <number>`  
  Adds `<number>` fake customer records, each with an associated address.


- `python manage.py add_fake_devices -n <number>`  
  Adds `<number>` fake device records.


- `python manage.py add_fake_employees -n <number>`  
  Adds `<number>` fake employee records.


- `python manage.py add_fake_informations -n <number>`  
  Adds `<number>` fake information records.


- `python manage.py add_fake_notifications -n <number>`  
  Adds `<number>` fake notification records.


- `python manage.py add_fake_order_reviews -n <number>`  
  Adds `<number>` fake order review records.


- `python manage.py add_fake_orders -n <number>`  
  Adds `<number>` fake order records.


- `python manage.py add_fake_services -n <number>`  
  Adds `<number>` fake service records.


### Coming Soon

The testing framework and test cases will be available soon. Stay tuned for updates!

