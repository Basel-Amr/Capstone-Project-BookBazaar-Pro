from flask import Flask, request, jsonify
from flask import jsonify, render_template
import models.inventory_model as models
# Define API routes
def get_all_inventories():
    """
    API endpoint to retrieve all inventories from the database and display them.
    """
    try:
        # Fetch inventories data from the model (which returns a pandas DataFrame)
        inventory_df = models.get_inventories()

        # If the request expects HTML rendering, return the HTML template
        if 'text/html' in request.accept_mimetypes:
            return render_template('inventory.html', Inventories=inventory_df.to_dict(orient='records'))
        
        # Otherwise, return the data as JSON
        return jsonify(inventory_df.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def creat_new_inventory(inventory_data):
    """
    Controller to create a new inventory.

    Args:
        inventory_data (dict): The inventory data received from the client.

    Returns:
        JSON: The response from the create_inventory() function.
    """
    return models.create_record(inventory_data)  # Pass the received inventory_data to create_inventory()



# Delete an inventory
def delete_inventory(inventory_id):
    """
    API function to delete an inventory by ID.
    """
    return models.delete_record(inventory_id)



def get_inventory_by_id(inventory_id):
    """
    API endpoint to retrieve an inventory by ID.
    """
    return models.get_record_by_id(inventory_id)



def update_inventory(inventory_id,data):
    """
    API endpoint to update an inventory's information by ID.
    """
    return models.update_inventory_id(inventory_id, data)
