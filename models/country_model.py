from config.db_config import  connect_to_database, close_connection
import pandas as pd
from models.helper_functions import check_unique, validate_required_field

from flask import Flask, jsonify, request, render_template
import re  # Regular expression library for name validation
from models.helper_functions import map_country_names

# Get All Countries
def get_countries():
    """
    Retrieve all countries records from the database.

    Returns:
        pd.DataFrame: A DataFrame containing all countries data.
    """
    try:
        connection = connect_to_database()
        
        # Query to fetch all countries
        query = "SELECT * FROM Countries"
        
        # Fetching data into a DataFrame
        Country_df = pd.read_sql_query(query, connection)
        
        close_connection(connection)
        return Country_df

    except Exception as e:
        # Log the exception for debugging
        print(f"Error in get_countries: {e}")
        raise
    
# Add a new country
def create_record(country_data):
    """
    Add a new Country to the SQLite database.
    Args:
        country_data (dict): A dictionary containing the country details.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Validate the user data as before
        message = validate_required_field(table='Countries', new_record=country_data, conn=connection)
        if message:
            return jsonify(message)
        
        query = '''
        INSERT INTO Countries (Country_Name, Region)
        VALUES (?, ?)
        '''
        cursor.execute(query, (country_data['Country_Name'], country_data['Region']))
        connection.commit()
        close_connection(connection)

        return jsonify({"message": "Country created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete an Country
def delete_record(id):
    """
    Endpoint to delete a record from the Inventory table by its ID.

    Args:
        id (int): The ID of the record to delete.

    Returns:
        JSON response indicating success or error.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Countries WHERE CountryID = ?", (id,))
        if cursor.rowcount == 0:
            return jsonify({"message": f"Record with ID {id} not found."}), 404
        connection.commit()
        close_connection(connection)
        return jsonify({"message": f"Record with ID {id} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Function to search record by ID for Country Table
def get_record_by_id(id):
    """
    Endpoint to retrieve a record from the Country table by its ID.

    Args:
        id (int): The ID of the record to retrieve.

    Returns:
        JSON response containing the record data, or an error message if the record is not found.
    """
    try:
        # Connect to the database
        connection = connect_to_database()

        # Write the query to fetch the record by ID
        query = '''SELECT * FROM Countries WHERE CountryID = ?'''

        # Execute the query using pandas
        Country_df = pd.read_sql_query(query, connection, params=(id,))

        # Close the connection
        close_connection(connection)
        # Check if the user exists
        if not Country_df.empty:
            # Convert the row to a dictionary
            record = Country_df.iloc[0].to_dict()

            # Format and return the response
            return jsonify({
                "Country_Name": record["Country_Name"],
                "Region": record["Region"]
            }), 200
        else:
            return jsonify({"message": f"Record with ID {id} not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Function to update Country by id
def update_country_id(country_id, data):
    """
    Update a country's details in the database.

    Args:
        country_id (int): The ID of the country to update.
        data (dict): A dictionary containing the updated fields.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Construct the SQL query dynamically based on provided fields
        update_fields = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE Countries SET {update_fields} WHERE CountryID = ?"

        # Execute the update query
        cursor.execute(query, list(data.values()) + [country_id])

        # Commit the changes
        connection.commit()

        if cursor.rowcount == 0:
            # No rows were updated; user not found
            return jsonify({"message": f"Inventory with ID {country_id} not found."}), 404

        # Close the connection
        close_connection(connection)
        return jsonify({"message": f"Inventory with ID {country_id} updated successfully."}), 200

    except Exception as e:
        # Handle errors and return the error message
        return jsonify({"error": str(e)}), 500




