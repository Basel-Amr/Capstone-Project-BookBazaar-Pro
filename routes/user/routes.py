from flask import Blueprint, jsonify, request
from controllers import user_controller as userclt

user_bp = Blueprint('user', __name__)


# Get all the users
@user_bp.route('/', methods=['GET'])
def get_users():
    return userclt.get_all_users()

# Add a new user
@user_bp.route('/', methods=['POST'])
def add_new_user():
    """
    Endpoint to add a new user to the database.
    
    Expected JSON format for the request:
    {
        "UserName": "John Doe",
        "Email": "John@gmail.com",
        "Password": "user1223",
        "Role" : 'admin' or 'customer',
        "Created_At" : "1998-12-12",
        "CountryID": 1
    }
    """
    try:
        # Get the user data from the request
        user_data = request.get_json()

        # Call the controller to add the user
        response = userclt.add_user(user_data)  # Pass user_data to add_user
        return response  # Return the response from add_user
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete a user
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    """
    API endpoint to delete a user by ID.
    """
    return userclt.delete_user(user_id)

# Get a user by ID
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id_route(user_id):
    """
    API endpoint to retrieve a user by ID.
    """
    return userclt.get_user_by_id(user_id)

# Update a user by ID
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    """
    API endpoint to update a user's details by ID.
    """
    data = request.json
    return userclt.update_user(user_id, data)