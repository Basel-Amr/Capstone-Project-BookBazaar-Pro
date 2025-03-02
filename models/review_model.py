# review_model.py
import json
from bson import ObjectId
from config.db_config import load_reviews_data, save_reviews_data  
from bson import ObjectId
from flask import render_template, request, jsonify


def get_all_reviews():
    """
    Fetch all reviews from the JSON data.
    """
    try:
        reviews = load_reviews_data()
        # Convert _id to string
        for review in reviews:
            review['_id'] = str(review['_id'])
        return reviews
    except Exception as e:
        print(f"Error loading reviews: {e}")
        return []

def get_review_by_book_id(book_id):
    """
    Get reviews for a specific book by book_id.
    """
    try:
        reviews = load_reviews_data()
        book_reviews = [review for review in reviews if review['book_id'] == book_id]
        return book_reviews
    except Exception as e:
        print(f"Error fetching reviews for book_id {book_id}: {e}")
        return []

def get_review_by_id(review_id):
    """Fetch a review from the database (JSON file) by its review_id."""
    try:
        reviews = load_reviews_data()
        review = next((r for r in reviews if str(r['_id']) == review_id), None)
        return review
    except Exception as e:
        print(f"Error fetching review with id {review_id}: {e}")
        return None


def add_review(review_data):
    """Add a new review to the database (JSON file)."""
    try:
        reviews = load_reviews_data()
        new_review = {
            "_id": str(ObjectId()),  # Generate a new unique ID
            "book_id": review_data["book_id"],
            "comment": review_data["comment"],
            "rating": review_data["rating"],
            "author": review_data.get("author", ""),
            "title": review_data.get("title", ""),
            "user": review_data.get("user", ""),
        }
        
        print(f"Adding review: {new_review}")  # Debugging line
        
        reviews.append(new_review)
        save_reviews_data(reviews)
        
        return new_review  # Return the new review
    except Exception as e:
        print(f"Error adding new review: {e}")  # Print error to console
        return None




def update_review(review_id, updated_data):
    """Update a review by its review_id."""
    try:
        reviews = load_reviews_data()
        for review in reviews:
            if str(review['_id']) == review_id:
                review.update(updated_data)
                save_reviews_data(reviews)
                return review
        return None  # Review not found
    except Exception as e:
        print(f"Error updating review with id {review_id}: {e}")
        return None


def delete_review(review_id):
    """Delete a review by its review_id."""
    try:
        reviews = load_reviews_data()
        updated_reviews = [r for r in reviews if str(r['_id']) != review_id]
        if len(updated_reviews) < len(reviews):  # Review was deleted
            save_reviews_data(updated_reviews)
            return True
        return False  # Review not found
    except Exception as e:
        print(f"Error deleting review with id {review_id}: {e}")
        return False

def get_reviews_by_book_id(book_id):
    """
    Fetch reviews for a specific book by its book_id.
    """
    try:
        reviews = load_reviews_data()
        book_reviews = [review for review in reviews if review['book_id'] == book_id]
        return book_reviews
    except Exception as e:
        print(f"Error fetching reviews for book_id {book_id}: {e}")
        return []