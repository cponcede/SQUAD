# factualAPI = factualAPI()

def list():
    zipCode = session.zipCode
    maxDistance = session.maxDistance
    pricePrefs = session.pricePrefs
    cuisineRatings = session.cuisineRatings
    # results = factualAPI.searchForRestaurants()
    # Return that dictionary to results/list.html, which will use this info to fill out the view.
    return dict(message="This is the view for viewing a list of restaurant results")

def restaurant():
    # Message resultsmodel.py to get info on that restaurant
    # Return response dicitonary from resultsmodel.py
    # results/restaurant.html will use this to fill out the view with info about that restaurant
    msg = "You are viewing results for " + request.vars['name']
    return dict(message=msg)
