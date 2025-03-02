# app.py
# import flask
from flask import Flask
# import routes blueprints
from routes.author.routes import author_bp
from routes.book.routes import book_bp
from routes.country.routes import country_bp
from routes.discount.routes import discount_bp
from routes.inventory.routes import inventory_bp
from routes.main.routes import main_bp
from routes.review.routes import review_bp
from routes.sales.routes import sales_bp
from routes.user.routes import user_bp

app = Flask(__name__)
app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(author_bp, url_prefix='/authors')
app.register_blueprint(book_bp, url_prefix='/books')
app.register_blueprint(sales_bp, url_prefix='/sales')
app.register_blueprint(inventory_bp, url_prefix='/inventory')
app.register_blueprint(country_bp, url_prefix='/country')
app.register_blueprint(discount_bp, url_prefix='/discount')
app.register_blueprint(review_bp, url_prefix='/reviews')

if __name__ == '__main__':
    app.run(debug=False)
