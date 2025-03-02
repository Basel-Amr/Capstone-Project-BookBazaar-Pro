from config.db_config import  connect_to_database, close_connection
import pandas as pd
from models.helper_functions import check_unique, validate_required_field

from flask import Flask, jsonify, request, render_template
import re  # Regular expression library for name validation
from models.helper_functions import map_country_names

# Get All Sales
def get_books():
    """
    Endpoint to retrieve all books records from the database.

    Returns:
        JSON response containing all books, or an error message if an error occurs.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        query = '''
        SELECT * FROM Books
        '''
        # Fetching data from the database
        Books_df = pd.read_sql_query(query, connection)
        # Render the order profile
        close_connection(connection)
        return Books_df

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Add a new sale
def create_record(book_data):
    """
    Add a new sale to the SQLite database.
    Args:
        book_data (dict): A dictionary containing the book details.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Validate the user data as before
        message = validate_required_field(table='Books', new_record=book_data, conn=connection)
        if message:
            return jsonify(message)
        
        query = '''
        INSERT INTO Books (AuthorID, Title, Genre, Publication_Year, ISBN, Price, Rating, Description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (book_data['AuthorID'], book_data['Title'], book_data['Genre'], book_data['Publication_Year'],
                               book_data['ISBN'], book_data['Price'], book_data['Rating'],book_data['Description']))
        connection.commit()
        close_connection(connection)

        return jsonify({"message": "Book created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete a Sale
def delete_record(id):
    """
    Endpoint to delete a record from the Users table by its ID.

    Args:
        id (int): The ID of the record to delete.

    Returns:
        JSON response indicating success or error.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Books WHERE BookID = ?", (id,))
        if cursor.rowcount == 0:
            return jsonify({"message": f"Record with ID {id} not found."}), 404
        connection.commit()
        close_connection(connection)
        return jsonify({"message": f"Record with ID {id} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Function to search record by ID for sales Table
def get_record_by_id(id):
    """
    Endpoint to retrieve a record from the Users table by its ID.

    Args:
        id (int): The ID of the record to retrieve.

    Returns:
        JSON response containing the record data, or an error message if the record is not found.
    """
    try:
        # Connect to the database
        connection = connect_to_database()

        # Write the query to fetch the record by ID
        query = '''SELECT * FROM Books WHERE BookID = ?'''

        # Execute the query using pandas
        books_df = pd.read_sql_query(query, connection, params=(id,))

        # Close the connection
        close_connection(connection)
        # Check if the user exists
        if not books_df.empty:
            # Convert the row to a dictionary
            record = books_df.iloc[0].to_dict()

            # Format and return the response
            return jsonify({
                "BookID": record["BookID"],
                "AuthorID": record["AuthorID"],
                "Title": record["Title"],
                "Genre":record["Genre"],
                "Publication_Year": record["Publication_Year"],
                "ISBN": record["ISBN"],
                "Price": record["Price"],
                "Rating": record["Rating"],
                "Description": record["Description"]
            }), 200
        else:
            return jsonify({"message": f"Record with ID {id} not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Function to update book by id
def update_book_id(book_id, data):
    """
    Update a user's details in the database.

    Args:
        book_id (int): The ID of the book to update.
        data (dict): A dictionary containing the updated fields.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Construct the SQL query dynamically based on provided fields
        update_fields = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE Books SET {update_fields} WHERE BookID = ?"

        # Execute the update query
        cursor.execute(query, list(data.values()) + [book_id])

        # Commit the changes
        connection.commit()

        if cursor.rowcount == 0:
            # No rows were updated; user not found
            return jsonify({"message": f"Book with ID {book_id} not found."}), 404

        # Close the connection
        close_connection(connection)
        return jsonify({"message": f"Book with ID {book_id} updated successfully."}), 200

    except Exception as e:
        # Handle errors and return the error message
        return jsonify({"error": str(e)}), 500




