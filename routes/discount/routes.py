from flask import Blueprint, jsonify, request
from controllers import discount_controller as discountclt

discount_bp = Blueprint('discount', __name__)

# Get all the discounts
@discount_bp.route('/', methods=['GET'])
def get_discounts():
    return discountclt.get_all_discounts()

# Add a new discount
@discount_bp.route('/', methods=['POST'])
def add_new_discount():
    """
    Endpoint to add a new discount to the database.
    
    Expected JSON format for the request:
    {
        "Description": "Summer Sale",
        "Value": 0.25,
        "Valid_From": "2024-1-2",
        "Valid_To": "2024-1-10",
        "Created_At": "2024-1-1",
        "BookID": 1,
        "UserID": 2,
    }
    """
    try:
        # Get the discount data from the request
        discount_data = request.get_json()

        # Call the controller to add the discount
        response = discountclt.creat_new_discount(discount_data)  # Pass discount_data to add_discount
        return response  # Return the response from add_country
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete an discount
@discount_bp.route('/<int:discount_id>', methods=['DELETE'])
def delete_discount_route(discount_id):
    """
    API endpoint to delete a discount by ID.
    """
    return discountclt.delete_discount(discount_id)

# Get an discount by ID
@discount_bp.route('/<int:discount_id>', methods=['GET'])
def get_discount_by_id_route(discount_id):
    """
    API endpoint to retrieve an discount by ID.
    """
    return discountclt.get_discount_by_id(discount_id)

# Update an discount by ID
@discount_bp.route('/<int:discount_id>', methods=['PUT'])
def update_discount_route(discount_id):
    """
    API endpoint to update a discount's details by ID.
    """
    data = request.json
    return discountclt.update_discount(discount_id, data)
