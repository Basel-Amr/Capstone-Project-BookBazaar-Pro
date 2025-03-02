from config.db_config import  connect_to_database, close_connection
import pandas as pd
from models.helper_functions import check_unique, validate_required_field

from flask import Flask, jsonify, request, render_template
import re  # Regular expression library for name validation
from models.helper_functions import map_country_names

# Get All Inventories
def get_inventories():
    """
    Endpoint to retrieve all inventories records from the database.

    Returns:
        JSON response containing all inventories, or an error message if an error occurs.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        query = '''
        SELECT * FROM Inventory
        '''
        # Fetching data from the database
        Inventory_df = pd.read_sql_query(query, connection)
        # Create a new column for Country names in the dataframe
        Inventory_df['CountryName'] = map_country_names(Inventory_df)
        # Drop CountryID col
        Inventory_df.drop(columns=['CountryID'], inplace=True)
        # Render the order profile
        close_connection(connection)
        return Inventory_df

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Add a new inventory
def create_record(inventory_data):
    """
    Add a new sale to the SQLite database.
    Args:
        inventory_data (dict): A dictionary containing the inventory details.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Validate the user data as before
        message = validate_required_field(table='Inventory', new_record=inventory_data, conn=connection)
        if message:
            return jsonify(message)
        
        query = '''
        INSERT INTO Inventory (BookID, CountryID, Stock_Quantity, Restock_Date, Warehouse_Location)
        VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (inventory_data['BookID'], inventory_data['CountryID'], inventory_data['Stock_Quantity']
                               , inventory_data['Restock_Date'],inventory_data['Warehouse_Location']))
        connection.commit()
        close_connection(connection)

        return jsonify({"message": "Inventory created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete an Inventory
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
        cursor.execute("DELETE FROM Inventory WHERE InventoryID = ?", (id,))
        if cursor.rowcount == 0:
            return jsonify({"message": f"Record with ID {id} not found."}), 404
        connection.commit()
        close_connection(connection)
        return jsonify({"message": f"Record with ID {id} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Function to search record by ID for Inventory Table
def get_record_by_id(id):
    """
    Endpoint to retrieve a record from the Inventory table by its ID.

    Args:
        id (int): The ID of the record to retrieve.

    Returns:
        JSON response containing the record data, or an error message if the record is not found.
    """
    try:
        # Connect to the database
        connection = connect_to_database()

        # Write the query to fetch the record by ID
        query = '''SELECT * FROM Inventory WHERE InventoryID = ?'''

        # Execute the query using pandas
        Inventory_df = pd.read_sql_query(query, connection, params=(id,))
        # Create a new column for Country names in the dataframe
        Inventory_df['CountryName'] = map_country_names(Inventory_df)
        # Drop CountryID col
        Inventory_df.drop(columns=['CountryID'], inplace=True)

        # Close the connection
        close_connection(connection)
        # Check if the user exists
        if not Inventory_df.empty:
            # Convert the row to a dictionary
            record = Inventory_df.iloc[0].to_dict()

            # Format and return the response
            return jsonify({
                "BookID": record["BookID"],
                "Stock_Quantity": record["Stock_Quantity"],
                "Restock_Date":record["Restock_Date"],
                "Warehouse_Location": record["Warehouse_Location"]
            }), 200
        else:
            return jsonify({"message": f"Record with ID {id} not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Function to update Inventory by id
def update_inventory_id(inventory_id, data):
    """
    Update a user's details in the database.

    Args:
        inventory_id (int): The ID of the inventory to update.
        data (dict): A dictionary containing the updated fields.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Construct the SQL query dynamically based on provided fields
        update_fields = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE Inventory SET {update_fields} WHERE InventoryID = ?"

        # Execute the update query
        cursor.execute(query, list(data.values()) + [inventory_id])

        # Commit the changes
        connection.commit()

        if cursor.rowcount == 0:
            # No rows were updated; user not found
            return jsonify({"message": f"Inventory with ID {inventory_id} not found."}), 404

        # Close the connection
        close_connection(connection)
        return jsonify({"message": f"Inventory with ID {inventory_id} updated successfully."}), 200

    except Exception as e:
        # Handle errors and return the error message
        return jsonify({"error": str(e)}), 500




