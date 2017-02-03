# -*- coding: utf-8 -*-
from restaurantsearch import RestaurantSearch

# The YelpSearch module exists in modules/yelpsearch.py
restaurant_search = RestaurantSearch()

def list():
    # Inside of session variable should be a Dictionary<String, Double> that maps from cuisine name -> rating
    # cuisineRatings = session.cuisine_ratings

    # Inside of session should also be location preferences
    # zip_code = session.zip_code
    # maxDistance = session.max_distance

    # Retrieve price preferences from session
    # pricePrefs = session.price_prefs

    # Pass all of the above information to restaurantsearch.py and get results back.
    results = restaurant_search.get_restaurants('94305', 40000, {'japanese':9.0}, {'$':True, '$$':False, '$$$':False, '$$$$':False})

    # Return that dictionary to results/list.html, which will use this info to fill out the view.
    return dict(message="This is the view for viewing a list of restaurant results", search_results = results)

def restaurant():
    # Get restaurant_id of the clicked on restaurant from the View
    # restaurant_id = request._vars['id']

    # Pass restaurant_id to restaurantsearch.py to get back a dictionary of info about that restaurant
    restaurant_details = restaurant_search.get_restaurant_details('fake_restaurant_id')
    msg = "You are viewing results for " + restaurant_details['name']
    return dict(message=msg)
