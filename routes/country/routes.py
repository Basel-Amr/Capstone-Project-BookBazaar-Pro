from flask import Blueprint, jsonify, request
from controllers import country_controller as countryclt

country_bp = Blueprint('country', __name__)
# Get all the countires
@country_bp.route('/', methods=['GET'])
def get_countries():
    return countryclt.get_all_countries()

# Add a new country
@country_bp.route('/', methods=['POST'])
def add_new_country():
    """
    Endpoint to add a new country to the database.
    
    Expected JSON format for the request:
    {
        "CountryName": "Egypt",
        "Regoin": "Africa 
    }
    """
    try:
        # Get the country data from the request
        country_data = request.get_json()

        # Call the controller to add the country
        response = countryclt.creat_new_country(country_data)  # Pass country_data to add_country
        return response  # Return the response from add_country
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete an country
@country_bp.route('/<int:country_id>', methods=['DELETE'])
def delete_country_route(country_id):
    """
    API endpoint to delete a country by ID.
    """
    return countryclt.delete_country(country_id)

# Get an country by ID
@country_bp.route('/<int:country_id>', methods=['GET'])
def get_country_by_id_route(country_id):
    """
    API endpoint to retrieve an country by ID.
    """
    return countryclt.get_country_by_id(country_id)

# Update an country by ID
@country_bp.route('/<int:country_id>', methods=['PUT'])
def update_country_route(country_id):
    """
    API endpoint to update a country's details by ID.
    """
    data = request.json
    return countryclt.update_country(country_id, data)

