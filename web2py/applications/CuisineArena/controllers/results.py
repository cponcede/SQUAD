# -*- coding: utf-8 -*-
# try something like
def list():
    return dict(message="This is the view for viewing a list of restaurant results")

def restaurant():
    # Message resultsmodel.py to get info on that restaurant
    # Return response dicitonary from resultsmodel.py
    # results/restaurant.html will use this to fill out the view with info about that restaurant
    msg = "You are viewing results for " + request.vars['name']
    return dict(message=msg)
