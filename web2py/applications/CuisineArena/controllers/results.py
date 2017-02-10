from foursquareapi import FoursquareAPI 
foursquareAPI = FoursquareAPI()

def list():
    results = foursquareAPI.searchForRestaurants(session.zipCode,session.maxDistanceInMiles,
        session.pricePrefs, session.finalRatings)
    # Return that dictionary to results/list.html, which will use this info to fill out the view.
    return dict(message="This is the view for viewing a list of restaurant results", searchResults=results, cuisineRatings=session.cuisineRatings)

def restaurant():
    restaurantId = request.vars.get('id', None)
    restaurantInfo = foursquareAPI.getRestaurantDetails(restaurantId)
    return dict(restaurantDetails=restaurantInfo)
