# 🌟BookBazaar Library Management System
![Logo](static/sprints_logo.png)

## Overview
BookBazaar is a robust and scalable library management system designed to streamline operations for managing books, users, sales, inventory, and reviews. Built using the **Model-View-Controller (MVC)** architecture, the project incorporates **Flask** for API development, **SQLite** for data persistence, and a user-friendly interface for interaction.

## Features
- **User Management:** Add, update, delete, and fetch user profiles.
- **Book Inventory:** Manage book details, stock levels, and warehouse locations.
- **Sales Tracking:** Record and retrieve sales data.
- **Author Management:** Store and update author details.
- **Discount System:** Create and apply discounts for specific books or users.
- **Country Database:** Manage and retrieve information about countries and regions.
- **Review System:** Collect and manage user reviews for books.

## Project Architecture
The system follows the **MVC Design Pattern**:
1. **Model:** Handles data logic and database operations.
2. **View:** Represents HTML templates or JSON responses.
3. **Controller:** Processes requests and connects Models with Views.

### Project Structure
```
BookBazaar/
├── app.py                    # Main application entry point
├── Config/
│   └── db_config.py          # Database configuration and connection handling
├── Model/
│   ├── user_model.py         # User data logic
│   ├── sale_model.py         # Sales data logic
│   ├── review_model.py       # Reviews data logic
│   ├── inventory_model.py    # Inventory data logic
│   ├── discount_model.py     # Discount data logic
│   ├── country_model.py      # Country data logic
│   ├── book_model.py         # Book data logic
│   └── author_model.py       # Author data logic
├── Controllers/
│   ├── user_controller.py    # User API logic
│   ├── sale_controller.py    # Sales API logic
│   ├── review_controller.py  # Reviews API logic
│   ├── inventory_controller.py # Inventory API logic
│   ├── discount_controller.py # Discount API logic
│   ├── country_controller.py  # Country API logic
│   ├── book_controller.py     # Book API logic
│   └── author_controller.py   # Author API logic
├── Routes/
│   ├── author/author.py       # Author routes
│   ├── book/book.py           # Book routes 
│   ├── country/country.py     # Country routes
│   ├── discount/discount.py   # Discount routes
│   ├── inventory/inventory.py # Inventory routes 
│   ├── main/routes.py         # Main routes 
│   ├── review/review.py       # Review routes
│   ├── sales/sales.py         # Sales routes 
│   └── user/user.py           # User routes
├── Static/
│   ├── styles.css        # CSS for web interface
│   └── logo.png          # Project logo
│
├── Templates/
│   ├── base.html             # Base template
│   ├── index.html            # Main dashboard
│   └── other HTML files...   # Individual pages
|__
```

## How to Run the Project

### 1. Prerequisites
- **Python 3.8+** installed on your system.
- Install the required Python libraries:
  ```bash
  pip install flask flask-sqlalchemy
  ```

### 2. Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/bookbazaar.git
   ```
2. Configure the database:
   - Ensure the SQLite database file is correctly referenced in `db_config.py`.
   - If starting fresh, run the script to create tables:
     ```bash
     python Config/db_config.py
     ```

### 3. Run the Application
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to:
   ```text
   http://127.0.0.1:5000/
   ```

### 4. API Endpoints
The REST API offers the following endpoints:

#### Users
- **GET /users**: Fetch all users.
- **GET /users**: Fetch all users.
- **GET /users/int:user_id**: Fetch a user record by ID.
- **PUT /users/int:user_id:** Update a user record.
- **DELETE /users/int:user_id**: Delete a user record

#### Books
- **GET /books**: Fetch all books.
- **POST /books**: Add a new book.
- **GET /books/int:book_id**: Fetch a book record by ID.
- **PUT /books/int:book_id**: Update a book record.
- **DELETE /books/int:book_id**: Delete a book record.

#### Sales
- **GET /sales**: Fetch all sales.
- **POST /sales**: Add a new sale.
- **GET /sales/int:sale_id**: Fetch a sales record by ID.
- **PUT /sales/int:sale_id**: Update a sales record.
- **DELETE /sales/int:sale_id**: Delete a sales record.

#### Countries
- **GET /countries**: Fetch all countries.
- **POST /countries**: Add a new country.
- **GET /countries/int:country_id**: Fetch a country record by ID.
- **PUT /countries/int:country_id**: Update a country record.
- **DELETE /countries/int:country_id**: Delete a country record.

#### Discounts
- **GET /discounts**: Fetch all discounts.
- **POST /discounts**: Add a new discount.
- **GET /discounts/int:discount_id**: Fetch a discount record by ID.
- **PUT /discounts/int:discount_id**: Update a discount record.
- **DELETE /discounts/int:discount_id**: Delete a discount record.

#### Reviews
- **GET /reviews**: Fetch all review records.
- **POST /reviews**: Add a new review.
- **GET /reviews/int:review_id**: Fetch a review record by ID.
- **PUT /reviews/int:review_id**: Update a review record.
- **DELETE /reviews/int:review_id**: Delete a review record.

## Contributing
We welcome contributions! Please fork the repository and submit a pull request for review.

