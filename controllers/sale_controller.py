from flask import Flask, request, jsonify
from flask import jsonify, render_template
import models.sale_model as models
# Define API routes
def get_all_sales():
    """
    API endpoint to retrieve all users from the database and display them.
    """
    try:
        # Fetch users data from the model (which returns a pandas DataFrame)
        sales_df = models.get_sales()
        

        # If the request expects HTML rendering, return the HTML template
        if 'text/html' in request.accept_mimetypes:
            return render_template('sales.html', Sales=sales_df.to_dict(orient='records'))
        
        # Otherwise, return the data as JSON
        return jsonify(sales_df.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def creat_new_sale(user_data):
    """
    Controller to create a new user.

    Args:
        user_data (dict): The user data received from the client.

    Returns:
        JSON: The response from the create_user() function.
    """
    return models.create_record(user_data)  # Pass the received user_data to create_user()



# Delete a user
def delete_sale(sale_id):
    """
    API function to delete a user by ID.
    """
    return models.delete_record(sale_id)



def get_sale_by_id(sale_id):
    """
    API endpoint to retrieve a user by ID.
    """
    return models.get_record_by_id(sale_id)



def update_sale(sale_id,data):
    """
    API endpoint to update a user's information by ID.
    """
    return models.update_sale_id(sale_id, data)
