from flask import Flask, request, jsonify
from flask import jsonify, render_template
import models.author_model as models
# Define API routes
def get_all_authors():
    """
    API endpoint to retrieve all authors from the database and display them.
    """
    try:
        # Fetch users data from the model (which returns a pandas DataFrame)
        author_df = models.get_authors()
        

        # If the request expects HTML rendering, return the HTML template
        if 'text/html' in request.accept_mimetypes:
            return render_template('authors.html', Authors=author_df.to_dict(orient='records'))
        
        # Otherwise, return the data as JSON
        return jsonify(author_df.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def creat_new_author(author_data):
    """
    Controller to create a new user.

    Args:
        author_data (dict): The author data received from the client.

    Returns:
        JSON: The response from the create_user() function.
    """
    return models.create_record(author_data)  # Pass the received user_data to create_user()



# Delete a user
def delete_author(author_id):
    """
    API function to delete an author by ID.
    """
    return models.delete_record(author_id)



def get_author_by_id(author_id):
    """
    API endpoint to retrieve an author by ID.
    """
    return models.get_record_by_id(author_id)



def update_author(author_id,data):
    """
    API endpoint to update an author's information by ID.
    """
    return models.update_author_id(author_id, data)
