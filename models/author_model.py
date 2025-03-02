from config.db_config import  connect_to_database, close_connection
import pandas as pd
from models.helper_functions import check_unique, validate_required_field

from flask import Flask, jsonify, request, render_template
import re  # Regular expression library for name validation
from models.helper_functions import map_country_names

# Get All Sales
def get_authors():
    """
    Endpoint to retrieve all authors records from the database.

    Returns:
        JSON response containing all authors, or an error message if an error occurs.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        query = '''
        SELECT * FROM Authors
        '''
        # Fetching data from the database
        Authors_df = pd.read_sql_query(query, connection)
        # Create a new column for Country names in the dataframe
        Authors_df['CountryName'] = map_country_names(Authors_df)
        # Drop CountryID col
        Authors_df.drop(columns=['CountryID'], inplace=True)
        # Render the order profile
        close_connection(connection)
        return Authors_df

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Add a new sale
def create_record(author_data):
    """
    Add a new sale to the SQLite database.
    Args:
        author_data (dict): A dictionary containing the user details.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Validate the user data as before
        message = validate_required_field(table='Authors', new_record=author_data, conn=connection)
        if message:
            return jsonify(message)
        
        query = '''
        INSERT INTO Authors (First_Name, Last_Name, Bio, Birth_Date, CountryID)
        VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (author_data['First_Name'], author_data['Last_Name'], author_data['Bio'], author_data['Birth_Date'],author_data['CountryID']))
        connection.commit()
        close_connection(connection)

        return jsonify({"message": "Author created successfully"}), 201
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
        cursor.execute("DELETE FROM Authors WHERE AuthorID = ?", (id,))
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
        query = '''SELECT * FROM Authors WHERE AuthorID = ?'''

        # Execute the query using pandas
        authors_df = pd.read_sql_query(query, connection, params=(id,))

        # Close the connection
        close_connection(connection)
        # Check if the user exists
        if not authors_df.empty:
            # Convert the row to a dictionary
            record = authors_df.iloc[0].to_dict()

            # Format and return the response
            return jsonify({
                "AuthorID": record["AuthorID"],
                "First_Name": record["First_Name"],
                "Last_Name": record["Last_Name"],
                "Bio": record["Bio"],
                "Birth_Date": record["Birth_Date"],
                "CountryID": record["CountryID"]
            }), 200
        else:
            return jsonify({"message": f"Record with ID {id} not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Function to update sale by id
def update_author_id(author_id, data):
    """
    Update a user's details in the database.

    Args:
        author_id (int): The ID of the user to update.
        data (dict): A dictionary containing the updated fields.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Construct the SQL query dynamically based on provided fields
        update_fields = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE Authors SET {update_fields} WHERE AuthorID = ?"

        # Execute the update query
        cursor.execute(query, list(data.values()) + [author_id])

        # Commit the changes
        connection.commit()

        if cursor.rowcount == 0:
            # No rows were updated; user not found
            return jsonify({"message": f"Author with ID {author_id} not found."}), 404

        # Close the connection
        close_connection(connection)
        return jsonify({"message": f"Author with ID {author_id} updated successfully."}), 200

    except Exception as e:
        # Handle errors and return the error message
        return jsonify({"error": str(e)}), 500




