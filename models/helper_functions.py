from config.db_config import connect_to_database, close_connection
from flask import Flask, jsonify, request, render_template

# Country List
Country_List = ['Egypt', 'Saudi Arabia', 'Lebanon', 'United States', 'France', 
                'Germany', 'United Kingdom', 'Japan', 'China', 'India']

# Mapping of country names to CountryIDs (assuming CountryID is an integer and starts from 1)
country_map = {
    'Egypt': 1, 'Saudi Arabia': 2, 'Lebanon': 3, 'United States': 4, 
    'France': 5, 'Germany': 6, 'United Kingdom': 7, 'Japan': 8, 'China': 9, 'India': 10}



# Helper function to map CountryID to CountryName
def map_country_names(dataframe):
    """
    Maps CountryID in a DataFrame to corresponding CountryName.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the 'CountryID' column.

    Returns:
        pd.Series: A Series with mapped CountryName values.
    """
    reverse_map = {v: k for k, v in country_map.items()}  # Reverse the country_map
    return dataframe['CountryID'].map(reverse_map)

# Helper function to check if a record exists
def check_unique(table, column, value):
    """
    Checks if a record with a specific value exists in the specified table and column.

    Args:
        table (str): The table name to search in.
        column (str): The column name to check.
        value (str): The value to search for.

    Returns:
        bool: True if the record doesn't exist, False if it exists.
    """
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE {column} = ?", (value,))
    result = cursor.fetchone()
    close_connection(connection)
    return result is None

# Function to get columns from a table
def get_columns_from_table(table_name, conn):
    cursor = conn.cursor()
    # For SQLite, you can use PRAGMA table_info
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]  # Column names are in the second position of the tuple
    return columns

def get_primary_key(table, conn):
    """
    Get the primary key column for the given table.

    Args:
        table (str): The table name.
        conn (Connection): The database connection object.

    Returns:
        str: The name of the primary key column.
    """
    query = f"PRAGMA table_info({table})"
    cursor = conn.cursor()
    cursor.execute(query)
    columns = cursor.fetchall()

    # Find and return the column name of the primary key
    for column in columns:
        if column[5] == 1:  # The 6th item (index 5) is 1 if it's the primary key
            return column[1]  # Return the column name
    return None  # Return None if no primary key is found


def validate_required_field(table, new_record, conn):
    """
    Validate that all required fields are present in the new record, excluding the primary key.

    Args:
        table (str): The name of the table to check against.
        new_record (dict): The new record to validate.
        conn (Connection): The database connection object.

    Returns:
        dict or None: Returns a dictionary with an error message if required fields are missing,
                      or None if all required fields are present.
    """
    try:
        # Get all columns from the specified table
        required_fields = get_columns_from_table(table, conn)
        
        # Get the primary key column name (assuming there's a function to get it)
        primary_key = get_primary_key(table, conn)

        # Exclude the primary key from the list of required fields
        required_fields = [field for field in required_fields if field != primary_key]
        
        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in new_record]
        
        # If there are missing fields, return an error message with the list of missing fields
        if missing_fields:
            return {"error": f"Missing required field(s): {', '.join(missing_fields)}"}
        
        # If all required fields are present, return None to proceed
        return None

    except Exception as e:
        return {"error": f"An error occurred while validating fields: {str(e)}"}