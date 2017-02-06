from factualsearch import FactualSearch

factualAPI = FactualSearch()

def list():
    zipCode = session.zipCode
    maxDistance = session.maxDistance
    pricePrefs = session.pricePrefs
    cuisineRatings = session.cuisineRatings
    results = factualAPI.searchForRestaurants(session.zipCode, session.maxDistance, session.pricePrefs, session.cuisineRatings)
    # Return that dictionary to results/list.html, which will use this info to fill out the view.
    return dict(message="This is the view for viewing a list of restaurant results", results=results)

def restaurant():
    restaurantId = request.vars.get('id', -1) # URL parameter is the factual ID of the chosen restaurant
    restaurantInfo = factualAPI.getRestaurantDetails(restaurantId)
    msg = "You are viewing results for " + restaurantInfo['name']
    return dict(message=msg, details=restaurantInfo)
