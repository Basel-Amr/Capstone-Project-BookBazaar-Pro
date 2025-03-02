from flask import Blueprint, jsonify, request
from controllers import inventory_controller as inventoryclt

inventory_bp = Blueprint('inventory', __name__)

# Get all the inventories
@inventory_bp.route('/', methods=['GET'])
def get_inventories():
    return inventoryclt.get_all_inventories()

# Add a new inventory
@inventory_bp.route('/', methods=['POST'])
def add_new_inventory():
    """
    Endpoint to add a new inventory to the database.
    
    Expected JSON format for the request:
    {
        "BookID": 2,
        "CountryID": 1 ,
        "Stock_Quantity": 55,
        "Restock_Date" : Date,
        "Warehouse_Location" : "WarehouseA"
    }
    """
    try:
        # Get the invenotry data from the request
        inventory_data = request.get_json()

        # Call the controller to add the inventory
        response = inventoryclt.creat_new_inventory(inventory_data)  # Pass inventory_data to add_inventory
        return response  # Return the response from add_inventory
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete an inventory
@inventory_bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete_inventory_route(inventory_id):
    """
    API endpoint to delete a inventory by ID.
    """
    return inventoryclt.delete_inventory(inventory_id)

# Get an inventory by ID
@inventory_bp.route('/<int:inventory_id>', methods=['GET'])
def get_inventory_by_id_route(inventory_id):
    """
    API endpoint to retrieve an inventory by ID.
    """
    return inventoryclt.get_inventory_by_id(inventory_id)

# Update an inventory by ID
@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])
def update_inventory_route(inventory_id):
    """
    API endpoint to update a inventory's details by ID.
    """
    data = request.json
    return inventoryclt.update_inventory(inventory_id, data)
