# -*- coding: utf-8 -*-
from yelpsearch import YelpSearch

# The YelpSearch module exists in modules/yelpsearch.py
yelpAPI = YelpSearch()

def list():
    # Inside of session variable should be a Dictionary<String, Double> that maps from cuisine name -> rating
    # cuisineRatings = session.cuisineRatings
    
    # Inside of session should also be location preferences
    # zipCode = session.zipCode
    # maxDistance = session.maxDistance
    
    # Retrieve price preferences from session
    # pricePrefs = session.pricePrefs
    
    # Pass all of the above information to resultsmodel.py to get back a list of restaurants and information about each.
    # Weirdly, Yelp API not filtering categories correctly.
    # https://github.com/Yelp/yelp-python for querying the Yelp API
    results = yelpAPI.get_restaurants('94305', 40000, {'japanese':9.0}, {'$':True, '$$':False, '$$$':False}) # TODO: add arguments for price/location and all that
        
    # Return that dictionary to results/list.html, which will use this info to fill out the view.
    return dict(message="This is the view for viewing a list of restaurant results", search_results = results)
    
def restaurant():
    # Message resultsmodel.py to get info on that restaurant
    # Return response dicitonary from resultsmodel.py
    # results/restaurant.html will use this to fill out the view with info about that restaurant
    msg = "You are viewing results for " + request.vars['name']
    return dict(message=msg)
