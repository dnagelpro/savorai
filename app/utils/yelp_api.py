import requests
import os
from math import radians, cos, sin, sqrt, atan2

YELP_API_KEY = os.getenv("YELP_API_KEY")
YELP_SEARCH_ENDPOINT = "https://api.yelp.com/v3/businesses/search"
YELP_CATEGORIES_ENDPOINT = "https://api.yelp.com/v3/categories"
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def geocode_location(city, state):
    address = f"{city}, {state}"
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(geocode_url, params=params)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            location = results[0]["geometry"]["location"]
            city_lat = location["lat"]
            city_lng = location["lng"]
            print(f"📍 Geocoded {city}, {state} to: {city_lat}, {city_lng}")
            return city_lat, city_lng

    print("❌ Geocoding failed for:", address)
    return None, None


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def search_yelp(city, state, cuisine, price=None):
    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}"
    }

    params = {
        "location": f"{city}, {state}",
        "term": cuisine,
        "limit": 30,
        "sort_by": "rating"
    }

    if price:
        params["price"] = price

    response = requests.get(YELP_SEARCH_ENDPOINT, headers=headers, params=params)

    if response.status_code == 200:
        businesses = response.json().get("businesses", [])

        city_lat, city_lng = geocode_location(city, state)
        if city_lat is None or city_lng is None:
            return [], businesses

        print("\n---- DISTANCES FROM CITY CENTER ----")
        for b in businesses:
            coords = b.get("coordinates", {})
            if "latitude" in coords and "longitude" in coords:
                dist = haversine_distance(city_lat, city_lng, coords["latitude"], coords["longitude"])
                print(f"{b['name']} → {dist:.2f} miles away")

        # Only include restaurants within 3 miles of city center
        filtered = [
            b for b in businesses
            if "latitude" in b["coordinates"] and "longitude" in b["coordinates"] and
               haversine_distance(city_lat, city_lng, b["coordinates"]["latitude"], b["coordinates"]["longitude"]) <= 3
        ]

        print(f"\n✅ Filtered results: {len(filtered)} / {len(businesses)}")
        return filtered, businesses

    else:
        print("❌ Yelp API Error (Search):", response.status_code, response.text)
        return [], []


def get_food_categories():
    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}"
    }

    response = requests.get(YELP_CATEGORIES_ENDPOINT, headers=headers)

    if response.status_code == 200:
        all_categories = response.json().get("categories", [])
        food_categories = [
            c for c in all_categories
            if "restaurants" in c.get("parent_aliases", [])
        ]
        return sorted(set([c["title"] for c in food_categories]))
    else:
        print("❌ Yelp API Error (Categories):", response.status_code, response.text)
        return []
