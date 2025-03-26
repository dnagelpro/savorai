from flask import Blueprint, render_template, request
from app.utils.yelp_api import search_yelp
from app.utils.openai_parser import parse_query
import os

results_bp = Blueprint('results_bp', __name__)

@results_bp.route('/results', methods=['POST'])
def results():
    # Capture form inputs
    city = request.form.get('city', '').strip()
    state = request.form.get('state', '').strip()
    cuisine = request.form.get('cuisine', '').strip()
    price = request.form.get('price', '').strip()

    # If AI box was used and other fields are still empty
    if not city or not state or not cuisine:
        ai_query = request.form.get('ai_query', '').strip()
        if ai_query:
            print("💬 AI Query received:", ai_query)
            city, state, cuisine, price_from_ai = parse_query(ai_query)

            # Only override empty fields
            if not city: city = ''
            if not state: state = ''
            if not cuisine: cuisine = ''
            if not price: price = price_from_ai

    print(f"🔍 Final search params → City: {city}, State: {state}, Cuisine: {cuisine}, Price: {price}")

    # Call Yelp API
    restaurants, raw_results = search_yelp(city, state, cuisine, price)

    # Handle fallback if no local matches
    message = ""
    if not restaurants:
        message = f"No restaurants found within 3 miles of {city}, {state}. Showing nearby results instead."
        restaurants = raw_results

    # Google Maps markers
    map_data = [
        {
            'lat': r['coordinates']['latitude'],
            'lng': r['coordinates']['longitude'],
            'name': r['name'],
            'address': r['location']['address1'],
            'rating': r['rating'],
            'url': r['url']
        }
        for r in restaurants if r.get('coordinates')
    ]

    return render_template(
        'results.html',
        city=city,
        state=state,
        cuisine=cuisine,
        restaurants=restaurants,
        map_data=map_data,
        message=message,
        google_maps_api_key=os.getenv('GOOGLE_MAPS_API_KEY')
    )
