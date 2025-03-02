from flask import Blueprint, jsonify, request
from controllers import author_controller as authorclt

author_bp = Blueprint('author', __name__)

# Get all the authors
@author_bp.route('/', methods=['GET'])
def get_authors():
    return authorclt.get_all_authors()

# Add a new author
@author_bp.route('/', methods=['POST'])
def add_new_author():
    """
    Endpoint to add a new user to the database.
    
    Expected JSON format for the request:
    {
        "First_Name": "John",
        "Last_Name": "Doe",
        "Bio": "egyptian author",
        "Bith_Date" : "1998-12-12",
        "CountryID": 1
    }
    """
    try:
        # Get the author data from the request
        author_data = request.get_json()

        # Call the controller to add the user
        response = authorclt.creat_new_author(author_data)  # Pass author_data to add_user
        return response  # Return the response from add_user
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete an author
@author_bp.route('/<int:author_id>', methods=['DELETE'])
def delete_author_route(author_id):
    """
    API endpoint to delete a author by ID.
    """
    return authorclt.delete_author(author_id)

# Get an author by ID
@author_bp.route('/<int:author_id>', methods=['GET'])
def get_author_by_id_route(author_id):
    """
    API endpoint to retrieve a author by ID.
    """
    return authorclt.get_author_by_id(author_id)

# Update an author by ID
@author_bp.route('/<int:author_id>', methods=['PUT'])
def update_author_route(author_id):
    """
    API endpoint to update a author's details by ID.
    """
    data = request.json
    return authorclt.update_author(author_id, data)
