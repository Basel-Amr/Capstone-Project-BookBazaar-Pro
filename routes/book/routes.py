from flask import Blueprint, jsonify, request
from controllers import book_controller as bookclt

book_bp = Blueprint('book', __name__)

#-------------------------------------------------------Books CLASS-----------------------------------------------------------------#
# Get all the books
@book_bp.route('/', methods=['GET'])
def get_books():
    return bookclt.get_all_books()

# Add a new book
@book_bp.route('/', methods=['POST'])
def add_new_book():
    """
    Endpoint to add a new book to the database.
    
    Expected JSON format for the request:
    {
        "AuthorID": 2,
        "Title": "Book Number 1",
        "Genre": "comedy",
        "Puplication_Year" : "1998-12-12",
        "ISBN": "12325",
        "Price": 16.5,
        "Rating": 4.5,
        "Description": "newbook"
    }
    """
    try:
        # Get the book data from the request
        book_data = request.get_json()

        # Call the controller to add the book
        response = bookclt.creat_new_book(book_data)  # Pass book_data to add_book
        return response  # Return the response from add_book
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete an book
@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book_route(book_id):
    """
    API endpoint to delete a book by ID.
    """
    return bookclt.delete_book(book_id)

# Get an author by ID
@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book_by_id_route(book_id):
    """
    API endpoint to retrieve a book by ID.
    """
    return bookclt.get_book_by_id(book_id)

# Update an book by ID
@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book_route(book_id):
    """
    API endpoint to update a book's details by ID.
    """
    data = request.json
    return bookclt.update_book(book_id, data)
