from config.db_config import  connect_to_database, close_connection
import pandas as pd
from models.helper_functions import check_unique, validate_required_field

from flask import Flask, jsonify, request, render_template
import re  # Regular expression library for name validation

# Get All Discounts
def get_discounts():
    """
    Retrieve all discounts records from the database.

    Returns:
        pd.DataFrame: A DataFrame containing all discounts data.
    """
    try:
        connection = connect_to_database()
        
        # Query to fetch all countries
        query = "SELECT * FROM Discounts"
        
        # Fetching data into a DataFrame
        Discount_df = pd.read_sql_query(query, connection)
        
        close_connection(connection)
        return Discount_df

    except Exception as e:
        # Log the exception for debugging
        print(f"Error in get_discounts: {e}")
        raise
    
# Add a new discount
def create_record(discount_data):
    """
    Add a new Discount to the SQLite database.
    Args:
        discount_data (dict): A dictionary containing the discount details.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Validate the user data as before
        message = validate_required_field(table='Discounts', new_record=discount_data, conn=connection)
        if message:
            return jsonify(message)
        
        query = '''
        INSERT INTO Discounts (Description, Value, Valid_From, Valid_To, Created_At, BookID, UserID)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (discount_data['Description'], discount_data['Value'],discount_data['Valid_From'],discount_data['Valid_To'],
                               discount_data['Created_At'],discount_data['BookID'],discount_data['UserID']))
        connection.commit()
        close_connection(connection)

        return jsonify({"message": "Discount created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete an Discount
def delete_record(id):
    """
    Endpoint to delete a record from the Discount table by its ID.

    Args:
        id (int): The ID of the record to delete.

    Returns:
        JSON response indicating success or error.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Discounts WHERE DiscountID = ?", (id,))
        if cursor.rowcount == 0:
            return jsonify({"message": f"Record with ID {id} not found."}), 404
        connection.commit()
        close_connection(connection)
        return jsonify({"message": f"Record with ID {id} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Function to search record by ID for Discount Table
def get_record_by_id(id):
    """
    Endpoint to retrieve a record from the Discount table by its ID.

    Args:
        id (int): The ID of the record to retrieve.

    Returns:
        JSON response containing the record data, or an error message if the record is not found.
    """
    try:
        # Connect to the database
        connection = connect_to_database()

        # Write the query to fetch the record by ID
        query = '''SELECT * FROM Discounts WHERE DiscountID = ?'''

        # Execute the query using pandas
        Discount_df = pd.read_sql_query(query, connection, params=(id,))

        # Close the connection
        close_connection(connection)
        # Check if the user exists
        if not Discount_df.empty:
            # Convert the row to a dictionary
            record = Discount_df.iloc[0].to_dict()

            # Format and return the response
            return jsonify({
                "DiscountID": record["DiscountID"],
                "Description": record["Description"],
                "Value": record["Value"],
                "Valid_From": record["Valid_From"],
                "Valid_To": record["Valid_To"],
                "Created_At": record["Created_At"],
                "BookID": record["BookID"],
                "UserID": record["UserID"]
            }), 200
        else:
            return jsonify({"message": f"Record with ID {id} not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Function to update Discount by id
def update_discount_id(discount_id, data):
    """
    Update a discount's details in the database.

    Args:
        discount_id (int): The ID of the discount to update.
        data (dict): A dictionary containing the updated fields.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Construct the SQL query dynamically based on provided fields
        update_fields = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE Discounts SET {update_fields} WHERE DiscountID = ?"

        # Execute the update query
        cursor.execute(query, list(data.values()) + [discount_id])

        # Commit the changes
        connection.commit()

        if cursor.rowcount == 0:
            # No rows were updated; user not found
            return jsonify({"message": f"Inventory with ID {discount_id} not found."}), 404

        # Close the connection
        close_connection(connection)
        return jsonify({"message": f"Inventory with ID {discount_id} updated successfully."}), 200

    except Exception as e:
        # Handle errors and return the error message
        return jsonify({"error": str(e)}), 500




