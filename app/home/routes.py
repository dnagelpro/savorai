from flask import Blueprint, render_template
from app.utils.yelp_api import get_food_categories

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def home():
    # Fetch the available cuisine categories from Yelp
    categories = get_food_categories()
    return render_template('home.html', categories=categories)
