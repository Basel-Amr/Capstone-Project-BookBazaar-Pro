from flask import Flask, request, jsonify
from flask import jsonify, render_template
import models.discount_model as models
# Define API routes
def get_all_discounts():
    """
    API endpoint to retrieve all discounts from the database and display them.
    """
    try:
        # Fetch discounts data from the model (which returns a pandas DataFrame)
        discount_df = models.get_discounts()

        # If the request expects HTML rendering, return the HTML template
        if 'text/html' in request.accept_mimetypes:
            return render_template('discounts.html', discounts=discount_df.to_dict(orient='records'))
        
        # Otherwise, return the data as JSON
        return jsonify(discount_df.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def creat_new_discount(discount_data):
    """
    Controller to create a new Discount.

    Args:
        discount_data (dict): The discount data received from the client.

    Returns:
        JSON: The response from the create_inventory() function.
    """
    return models.create_record(discount_data)  # Pass the received discount_data to create_discount()



# Delete an discount
def delete_discount(discount_id):
    """
    API function to delete an discount by ID.
    """
    return models.delete_record(discount_id)



def get_discount_by_id(discount_id):
    """
    API endpoint to retrieve an discount by ID.
    """
    return models.get_record_by_id(discount_id)



def update_discount(discount_id,data):
    """
    API endpoint to update an discount's information by ID.
    """
    return models.update_discount_id(discount_id, data)
