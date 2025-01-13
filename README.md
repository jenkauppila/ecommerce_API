# E-Commerce App

## Table of Contents
- [E-Commerce App](#e-commerce-app)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
  - [Authors](#authors)
  - [Collaborators](#collaborators)
  - [API Screenshots](#api-screenshots)

## Introduction
This E-Commerce App is a web application created for my Module 3 project at [Coding Temple](https://www.codingtemple.com). It was designed to facilitate the online shopping experience at a coffee shop, and is loosely based on the 1990's - early 2000's sitcom, [FRIENDS](https://www.imdb.com/title/tt0108778/). 

The app allows you to add, modify and delete users, orders and products (inventory), as well as add products to individual orders and run various "reporting" (GET) requests to return the content of the various tables included in the database. 

The app is built using Flask, SQLAlchemy, and Marshmallow for the backend, and it connects to a MySQL database.

## Features
- Users: add, modify, delete
- Orders: add, modify, delete
- Products: add, modify, delete
- Add/Remove products from orders
- "Reporting" (GET requests) for all DB tables 

## Installation
To install and run the E-Commerce App locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/jenplanque/ecommerce_API.git
    cd ecommerce_API
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

## Prerequisites
- Python 3.9 or higher
- MySQL database
- Flask
- SQLAlchemy
- Marshmallow

## Usage
1. Start the Flask development server:
    ```bash
    flask run
    ```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Use the provided endpoints to interact with the application (e.g., register a new user, add products, place orders).



## Authors
- [Jen Planque](https://github.com/jenplanque)

## Collaborators
A big shout out to some of my very favorite people at Coding Temple, without who's ongoing support this project wouldn't be possible:
- [Katelyn Mehner](https://github.com/kmehner)
- [Dave Kidd](https://github.com/codingTempleDave)
- Daniel Erazo

## API Screenshots
Home Page:
![Home Page](screenshots/1-API_main.png) 

GET All Users:
![User Requests](screenshots/2-All_users.png) 

GET All Orders:
![Order Requests](screenshots/3-All_orders.png) 

GET All Products:
![Product Requests](screenshots/4-All_products.png) 