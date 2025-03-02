import sqlite3
import json
import pymongo
import json
import subprocess
import os
from pymongo import MongoClient
from time import sleep
# Database connection function
def connect_to_database(db_name="bookbazaar.db"):
    """
    Connects to the SQLite database.

    Args:
        db_name (str): The name of the SQLite database file (default: "bookbazaar.db").

    Returns:
        connection (sqlite3.Connection): The connection object to the database, or None if the connection fails.
    """
    try:
        connection = sqlite3.connect(db_name)
        connection.row_factory = sqlite3.Row  # Return rows as dictionaries
        print("✅ Successfully connected to the database")
        return connection
    except sqlite3.Error as e:
        print(f"❌ Error while connecting to the database: {e}")
        return None

# Close database connection
def close_connection(connection):
    """
    Closes the database connection.

    Args:
        connection (sqlite3.Connection): The connection object to the database.
    """
    if connection:
        connection.close()




## Check if MongoDB is running, if not, start it
def start_mongodb():
    """Ensure MongoDB is running by attempting to start it."""
    try:
        # Check if MongoDB is already running (we try to connect first)
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.server_info()  # If this doesn't raise an exception, MongoDB is running
        print("MongoDB is already running.")
    except pymongo.errors.ServerSelectionTimeoutError:
        print("MongoDB not running. Starting MongoDB...")
        # Run the MongoDB server using subprocess
        try:
            subprocess.Popen(["mongod", "--dbpath", "/data/db", "--bind_ip", "127.0.0.1"])
            print("MongoDB started successfully.")
            sleep(5)  # Give MongoDB time to start up
        except Exception as e:
            print(f"Error starting MongoDB: {e}")
            raise

# Load JSON data from file
def load_json_data():
    try:
        with open("bookbazaar_reviews.json", "r") as file:
            data = json.load(file)
            print(f"Loaded data from JSON: {data[:2]}")  # Print first 2 records to check data load
            return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

# Establish MongoDB connection
def get_db_connection():
    """Establish connection to MongoDB."""
    try:
        # Ensure MongoDB is running
        start_mongodb()

        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['bookbazaar_reviews']
        if db is None:
            raise Exception("Failed to connect to the database.")
        print("Successfully connected to MongoDB!")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# Insert data into MongoDB (ensure it's only done once for setup)
def insert_data_to_db():
    db = get_db_connection()
    if db:
        reviews_data = load_json_data()
        if reviews_data:
            try:
                db.Reviews.insert_many(reviews_data)
                print(f"Successfully inserted {len(reviews_data)} reviews into the database.")
            except Exception as e:
                print(f"Error inserting data into MongoDB: {e}")

# db_config.py

import json

# Function to load reviews data from the local JSON file
def load_reviews_data():
    """Load reviews data from the JSON file."""
    try:
        with open('bookbazaar_reviews.json', 'r') as file:
            data = json.load(file)
        # Normalize _id to a string
        for review in data:
            if isinstance(review.get("_id"), dict) and "$oid" in review["_id"]:
                review["_id"] = review["_id"]["$oid"]
        return data
    except Exception as e:
        print(f"Error loading reviews data: {e}")
        return []
    
def save_reviews_data(reviews):
    """
    Save the updated reviews list to the JSON file.
    """
    try:
        with open("bookbazaar_reviews.json", "w") as file:
            json.dump(reviews, file, indent=4)
    except Exception as e:
        print(f"Error saving reviews to bookbazaar_reviews.json: {e}")
