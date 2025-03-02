# reviews_controller.py
from flask import request, jsonify
from models.review_model import get_all_reviews, get_review_by_book_id, add_review, update_review, delete_review, get_review_by_id, get_reviews_by_book_id
from flask import render_template, request, jsonify
from config.db_config import load_reviews_data, save_reviews_data  

def add_review_controller():
    try:
        # Get the review data from the request JSON
        new_review = request.get_json()
        
        print(f"Received data: {new_review}")  # Debugging line to check incoming data
        
        # Add the review using the model
        added_review = add_review(new_review)
        
        if added_review:
            return jsonify({"message": "Review added successfully", "review": added_review}), 201
        else:
            return jsonify({"error": "Failed to add review"}), 400
    except Exception as e:
        print(f"Error adding review: {str(e)}")  # Print error to console
        return jsonify({"error": f"Error adding review: {str(e)}"}), 500

    
def get_reviews_controller():
    try:
        reviews = get_all_reviews()
        if reviews:
            return render_template("reviews.html", reviews=reviews)
        else:
            return jsonify({"error": "No reviews found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error fetching reviews: {str(e)}"}), 500

def get_all_reviews_controller():
    try:
        reviews = get_all_reviews()
        if reviews:
            # If the request expects HTML rendering, return the HTML template
            if 'text/html' in request.accept_mimetypes:
                return render_template("reviews.html", reviews=reviews)
            else:
                return jsonify({"reviews": reviews}), 200
        else:
            return jsonify({"error": "No reviews found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error fetching all reviews: {str(e)}"}), 500

def get_review_by_book_id_controller():
    try:
        book_id = request.args.get("book_id")
        if not book_id:
            return jsonify({"error": "book_id parameter is required"}), 400
        reviews = get_review_by_book_id(book_id)
        if reviews:
            return jsonify(reviews), 200
        else:
            return jsonify({"error": f"No reviews found for book_id {book_id}"}), 404
    except Exception as e:
        return jsonify({"error": f"Error fetching reviews for book_id {book_id}: {str(e)}"}), 500


def delete_review_controller(review_id):
    """
    Delete a review using the model.
    """
    return delete_review(review_id)
    

# Fetch a review by its ID
def get_review_by_id_controller(review_id):
    """
    Fetch a review by its ID from the model.
    """
    review = get_review_by_id(review_id)
    return review

# Update a review by its ID with the updated data
def update_review_controller(review_id, updated_data):
    """
    Update a review by its ID with the provided updated data from the model.
    """
    updated_review = update_review(review_id, updated_data)
    return updated_review


def get_reviews_by_book_id_controller(book_id):
    """
    Get reviews by book ID from the model.
    """
    return get_reviews_by_book_id(book_id)
