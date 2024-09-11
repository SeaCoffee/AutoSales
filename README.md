# AutoSales
Car Sales Platform
# AutoSales Platform

Welcome to the AutoSales Platform! This repository contains the code for a comprehensive car sales platform with various features for buying and selling vehicles.

## Features

- **User Registration and Authentication**: Secure user accounts with registration and login functionality using [Simple JWT](https://github.com/django-rest-framework-simplejwt/django-rest-framework-simplejwt).
- **Car Listings**: Browse a wide range of vehicles with detailed descriptions and images.
- **Advanced Search**: Filter cars by make, model, price, year, and location.
- **User Chats**: Real-time user chats based on WebSockets for discussing listings.
- **User Profiles**: Create and manage user profiles.
- **Expandable Functionality**: Future-proof design allowing the addition of car dealerships as sellers.
- **User Roles**: Support for different user roles including basic and premium accounts.
- **Currency Support**: Handles three currencies, updated daily using Celery.
- **Premium Statistics**: Provides premium users with statistics such as average car price in the region and country, and ad views stats.
- **Email Notifications**: Sends notifications to users and managers using Celery, ensuring timely updates and communication.
- **Ad Moderation**: Monitors and filters ads for offensive language to maintain a respectful and safe environment.


## Setup and Installation

1. **Clone the Repository**

   git clone https://github.com/SeaCoffee/AutoSales
   
   cd AutoSales

2. Setup Frontend
 
   Open a new terminal, navigate to the frontend directory, and run:
   
   cd frontend
   
   npm install
   
   npm run build

   Frontend Environment Variables: Ensure that the frontend directory also contains an .env file with the following setting:
   BUILD_PATH='../client'

3. Setup Backend
   
   In the main terminal, run:
   
   docker-compose up --build

   Environment Variables: Fill out the .env file with the necessary data. (use env_example for example)

4. Access the Platform

   Open your web browser and go to http://localhost/ to access the platform.

   Note: After registration, all users except superusers and platform managers will have their accounts activated via email. To ensure proper testing,
   please use a valid email address to receive the confirmation email.

6. Before superuser create, ensure that you fill out the 'role' table in the database:

  INSERT INTO role (name, created_at, updated_at)
   VALUES 
   ('buyer', NOW(), NOW()),
   ('seller', NOW(), NOW()),
   ('manager', NOW(), NOW()),
   ('admin', NOW(), NOW());

   
7. To populate the database with initial data for currencies, car brands, and models, use the following SQL statements.
   
   To populate the currency table with basic currency information, use this SQL query. This will insert records for USD, EUR, and UAH:
   
   INSERT INTO currency (currency_code, rate, created_at, updated_at)
   VALUES 
   ('USD', 1.0, NOW(), NOW()),
   ('EUR', 0.85, NOW(), NOW()),
   ('UAH', 36.6, NOW(), NOW());
   
   To insert car brands into the brand table, use the following query:

   INSERT INTO brand (name, created_at, updated_at) 
   VALUES 
   ('Toyota', NOW(), NOW()), 
   ('Honda', NOW(), NOW());

   To add car models and link them to their respective brands in the model_name table, use the following query. The brand_id should match the corresponding brand in the brand table:
   
   INSERT INTO model_name (brand_id, name, created_at, updated_at) 
   VALUES 
   (1, 'Corolla', NOW(), NOW()), 
   (2, 'Civic', NOW(), NOW());

   Important Notes:
   - brand_id in the model_name table refers to the corresponding id of the brand in the brand table.
   - currency_code is the unique code for the currency, such as 'USD', 'EUR', 'UAH'.
   - rate is the exchange rate relative to the base currency (e.g., 1.0 for USD).


