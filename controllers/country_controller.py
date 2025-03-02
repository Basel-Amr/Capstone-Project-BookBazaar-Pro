from flask import Flask, request, jsonify
from flask import jsonify, render_template
import models.country_model as models
# Define API routes
def get_all_countries():
    """
    API endpoint to retrieve all countires from the database and display them.
    """
    try:
        # Fetch countires data from the model (which returns a pandas DataFrame)
        country_df = models.get_countries()

        # If the request expects HTML rendering, return the HTML template
        if 'text/html' in request.accept_mimetypes:
            return render_template('countries.html', countries=country_df.to_dict(orient='records'))
        
        # Otherwise, return the data as JSON
        return jsonify(country_df.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def creat_new_country(country_data):
    """
    Controller to create a new Country.

    Args:
        country_data (dict): The country data received from the client.

    Returns:
        JSON: The response from the create_inventory() function.
    """
    return models.create_record(country_data)  # Pass the received country_data to create_country()



# Delete an country
def delete_country(country_id):
    """
    API function to delete an country by ID.
    """
    return models.delete_record(country_id)



def get_country_by_id(country_id):
    """
    API endpoint to retrieve an country by ID.
    """
    return models.get_record_by_id(country_id)



def update_country(country_id,data):
    """
    API endpoint to update an country's information by ID.
    """
    return models.update_country_id(country_id, data)
