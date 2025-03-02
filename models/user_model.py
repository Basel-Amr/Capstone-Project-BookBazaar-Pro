from config.db_config import  connect_to_database, close_connection
import pandas as pd
from models.helper_functions import check_unique, validate_required_field

from flask import Flask, jsonify, request, render_template
import re  # Regular expression library for name validation

# Country List
Country_List = ['Egypt', 'Saudi Arabia', 'Lebanon', 'United States', 'France', 
                'Germany', 'United Kingdom', 'Japan', 'China', 'India']

# Mapping of country names to CountryIDs (assuming CountryID is an integer and starts from 1)
country_map = {
    'Egypt': 1, 'Saudi Arabia': 2, 'Lebanon': 3, 'United States': 4, 
    'France': 5, 'Germany': 6, 'United Kingdom': 7, 'Japan': 8, 'China': 9, 'India': 10
}


# Get All Users
def get_users():
    """
    Fetches all users from the database and returns a pandas DataFrame.
    """
    try:
        # Connect to the database
        connection = connect_to_database()
        # Write the query
        query = '''SELECT * FROM Users'''
        # Execute the query
        Users_df = pd.read_sql_query(query, connection)
        
        # Create a new column for Country names in the dataframe
        Users_df['CountryName'] = Users_df['CountryID'].map({v: k for k, v in country_map.items()})
        
        # Drop CountryID column
        Users_df.drop(columns=['CountryID'], inplace=True)
        
        # Close the connection
        close_connection(connection)
        
        return Users_df
    except Exception as e:
        print(f"Error fetching users: {e}")
        raise e
    
# Add a new user
def create_user(user_data):
    """
    Add a new user to the SQLite database.
    Args:
        user_data (dict): A dictionary containing the user details.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Validate the user data as before
        message = validate_required_field(table='Users', new_record=user_data, conn=connection)
        if message:
            return jsonify(message)
        
        if not re.match("^[A-Za-z ]+$", user_data['UserName']):
            return jsonify({"error": "The 'UserName' field must only contain alphabetic characters and spaces."}), 400
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", user_data['Email']):
            return jsonify({"error": "Invalid email format."}), 400
        
        if not check_unique("Users", "Email", user_data['Email']):
            return jsonify({"message": "Email already exists. Please use a unique email."}), 400
        
        query = '''
        INSERT INTO Users (UserName, Email, Password, Role, CountryID)
        VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (user_data['UserName'], user_data['Email'], user_data['Password'], user_data['Role'], user_data['CountryID']))
        connection.commit()
        close_connection(connection)

        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete a user
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
        cursor.execute("DELETE FROM Users WHERE UserID = ?", (id,))
        if cursor.rowcount == 0:
            return jsonify({"message": f"Record with ID {id} not found."}), 404
        connection.commit()
        close_connection(connection)
        return jsonify({"message": f"Record with ID {id} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Function to search record by ID for Users Table
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
        query = '''SELECT * FROM Users WHERE UserID = ?'''

        # Execute the query using pandas
        users_df = pd.read_sql_query(query, connection, params=(id,))

        # Close the connection
        close_connection(connection)

        # Check if the user exists
        if not users_df.empty:
            # Convert the row to a dictionary
            record = users_df.iloc[0].to_dict()

            # Format and return the response
            return jsonify({
                "UserID": record["UserID"],
                "UserName": record["UserName"],
                "Email": record["Email"],
                "Role": record["Role"],
                "CountryID": record["CountryID"],
                "Created_At": record["Created_At"],
            }), 200
        else:
            return jsonify({"message": f"Record with ID {id} not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Function to search users by name or email
def search_users():
    """
    Search for users by name or email.
    Args:
        query (str): The search query parameter.
    Description:
        This endpoint searches for users by name or email using a case-insensitive search.
    Returns:
        JSON: A list of matching users.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        search_query = request.args.get('query')
        if not search_query:
            return jsonify({"error": "Query parameter is required"}), 400  # 400: Bad Request
        cursor.execute("SELECT * FROM Users WHERE UserName LIKE ? OR Email LIKE ?", 
                       ('%' + search_query + '%', '%' + search_query + '%'))
        users = cursor.fetchall()
        close_connection(connection)
        if not users:
            return jsonify({"error": "No users found matching the search criteria"}), 404  # 404: Not Found

        # Convert users list to a dictionary format
        user_list = [{"UserID": user[0], "UserName": user[1], "Email": user[2], "Role": user[3], "CountryID": user[4]} for user in users]
        return jsonify(user_list), 200  # 200: OK
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # 500: Internal Server Error

# Function to update record by id
def update_user_id(user_id, data):
    """
    Update a user's details in the database.

    Args:
        user_id (int): The ID of the user to update.
        data (dict): A dictionary containing the updated fields.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Construct the SQL query dynamically based on provided fields
        update_fields = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE Users SET {update_fields} WHERE UserID = ?"

        # Execute the update query
        cursor.execute(query, list(data.values()) + [user_id])

        # Commit the changes
        connection.commit()

        if cursor.rowcount == 0:
            # No rows were updated; user not found
            return jsonify({"message": f"User with ID {user_id} not found."}), 404

        # Close the connection
        close_connection(connection)
        return jsonify({"message": f"User with ID {user_id} updated successfully."}), 200

    except Exception as e:
        # Handle errors and return the error message
        return jsonify({"error": str(e)}), 500
