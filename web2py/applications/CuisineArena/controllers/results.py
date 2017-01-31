# -*- coding: utf-8 -*-
# try something like
def list():
    # Inside of session variable should be a Dictionary<String, Double> that maps from cuisine name -> rating
    # Inside of session should also be location and price preferences
    # Pass all of the above information to resultsmodel.py to get back a list of restaurants and information about each.
    # Return that dictionary to results/list.html, which will use this info to fill out the view.
    return dict(message="This is the view for viewing a list of restaurant results")

def restaurant():
    # Message resultsmodel.py to get info on that restaurant
    # Return response dicitonary from resultsmodel.py
    # results/restaurant.html will use this to fill out the view with info about that restaurant
    msg = "You are viewing results for " + request.vars['name']
    return dict(message=msg)
