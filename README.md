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
3. 
   Open a new terminal, navigate to the frontend directory, and run:
   
   cd frontend
   
   npm install
   
   npm run build

   Frontend Environment Variables: Ensure that the frontend directory also contains an .env file with the following setting:
   BUILD_PATH='../client'

5. Setup Backend
   
   In the main terminal, run:
   
   docker-compose up --build

   Environment Variables: Fill out the .env file with the necessary data. (use env_example for example)

2. Access the Platform

  Open your web browser and go to http://localhost/ to access the platform.
