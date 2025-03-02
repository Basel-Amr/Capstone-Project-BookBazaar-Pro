from flask import Flask, request, jsonify
from flask import jsonify, render_template
import models.book_model as models
# Define API routes
def get_all_books():
    """
    API endpoint to retrieve all books from the database and display them.
    """
    try:
        # Fetch books data from the model (which returns a pandas DataFrame)
        book_df = models.get_books()

        # If the request expects HTML rendering, return the HTML template
        if 'text/html' in request.accept_mimetypes:
            return render_template('books.html', Books=book_df.to_dict(orient='records'))
        
        # Otherwise, return the data as JSON
        return jsonify(book_df.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def creat_new_book(book_data):
    """
    Controller to create a new book.

    Args:
        book_data (dict): The book data received from the client.

    Returns:
        JSON: The response from the create_user() function.
    """
    return models.create_record(book_data)  # Pass the received user_data to create_user()



# Delete a book
def delete_book(book_id):
    """
    API function to delete an book by ID.
    """
    return models.delete_record(book_id)



def get_book_by_id(book_id):
    """
    API endpoint to retrieve an book by ID.
    """
    return models.get_record_by_id(book_id)



def update_book(book_id,data):
    """
    API endpoint to update a book's information by ID.
    """
    return models.update_book_id(book_id, data)
