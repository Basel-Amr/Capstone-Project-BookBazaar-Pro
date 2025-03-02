from flask import Blueprint, jsonify, request
from controllers import review_controller as reviewclt

review_bp = Blueprint('review', __name__)

# Route to add a review
@review_bp.route("/", methods=["POST"])
def add_review_route():
    return reviewclt.add_review_controller()

# Route to get all reviews
@review_bp.route("/all", methods=["GET"])
def get_all_reviews_route():
    return reviewclt.get_all_reviews_controller()


@review_bp.route('/book/<book_id>', methods=['GET'])
def get_reviews_by_book_id_route(book_id):
    """
    Get reviews by book ID.
    """
    reviews = reviewclt.get_reviews_by_book_id_controller(book_id)
    if reviews:
        return jsonify(reviews), 200
    return jsonify({"error": "No reviews found for this book"}), 404


# Route for getting a review by its ID
@review_bp.route('/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    review = reviewclt.get_review_by_id_controller(review_id)
    if review:
        return jsonify(review)
    return jsonify({"error": "Review not found"}), 404

# Route for updating a review by its ID
@review_bp.route('/<review_id>', methods=['PUT'])
def update_review(review_id):
    updated_data = request.get_json()
    updated_review = reviewclt.update_review_controller(review_id, updated_data)
    if updated_review:
        return jsonify(updated_review)
    return jsonify({"error": "Review not found or unable to update"}), 404

@review_bp.route('/<review_id>', methods=['DELETE'])
def delete_review_route(review_id):
    """
    Delete a review by review ID.
    """
    success = reviewclt.delete_review_controller(review_id)
    if success:
        return jsonify({"message": "Review deleted successfully"}), 200
    return jsonify({"error": "Review not found or failed to delete"}), 404
