from flask import Flask, request, jsonify
from flask import jsonify, render_template
from models.user_model import (
    get_users,
    create_user,
    delete_record,
    get_record_by_id,
    search_users,
    update_user_id
)

# Define API routes
def get_all_users():
    """
    API endpoint to retrieve all users from the database and display them.
    """
    try:
        # Fetch users data from the model (which returns a pandas DataFrame)
        Users_df = get_users()

        # If the request expects HTML rendering, return the HTML template
        if 'text/html' in request.accept_mimetypes:
            print("Models users fetching!!")
            return render_template('users.html', Users=Users_df.to_dict(orient='records'))
        # Otherwise, return the data as JSON
        return jsonify(Users_df.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def add_user(user_data):
    """
    Controller to create a new user.

    Args:
        user_data (dict): The user data received from the client.

    Returns:
        JSON: The response from the create_user() function.
    """
    return create_user(user_data)  # Pass the received user_data to create_user()



# Delete a user
def delete_user(user_id):
    """
    API function to delete a user by ID.
    """
    return delete_record(user_id)



def get_user_by_id(user_id):
    """
    API endpoint to retrieve a user by ID.
    """
    return get_record_by_id(user_id)



def update_user(user_id,data):
    """
    API endpoint to update a user's information by ID.
    """
    return update_user_id(user_id, data)
