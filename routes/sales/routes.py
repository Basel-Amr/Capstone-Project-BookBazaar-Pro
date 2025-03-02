from flask import Blueprint, jsonify, request
from controllers import sale_controller as salesclt

sales_bp = Blueprint('sales', __name__)

# Get all the sales
@sales_bp.route('/', methods=['GET'])
def get_sales():
    return salesclt.get_all_sales()

# Add a new user
@sales_bp.route('/', methods=['POST'])
def add_new_sale():
    """
    Endpoint to add a new user to the database.
    
    Expected JSON format for the request:
    {
        "BookID": 2,
        "UserID": 1,
        "CountryID": 1,
        "Sales_Date" : '1990-8-8',
        "Sales_Quantity" : 34,
        "Total_Price": 15.6
    }
    """
    try:
        # Get the user data from the request
        user_data = request.get_json()

        # Call the controller to add the user
        response = salesclt.creat_new_sale(user_data)  # Pass user_data to add_user
        return response  # Return the response from add_user
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete a Sale
@sales_bp.route('/<int:sale_id>', methods=['DELETE'])
def delete_sale_route(sale_id):
    """
    API endpoint to delete a user by ID.
    """
    return salesclt.delete_sale(sale_id)

# Get a user by ID
@sales_bp.route('/<int:sale_id>', methods=['GET'])
def get_sale_by_id_route(sale_id):
    """
    API endpoint to retrieve a user by ID.
    """
    return salesclt.get_sale_by_id(sale_id)

# Update a user by ID
@sales_bp.route('/<int:sale_id>', methods=['PUT'])
def update_sale_route(sale_id):
    """
    API endpoint to update a user's details by ID.
    """
    data = request.json
    return salesclt.update_sale(sale_id, data)

