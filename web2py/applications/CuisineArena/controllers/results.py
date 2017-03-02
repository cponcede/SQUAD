from foursquareapi import FoursquareAPI 
foursquareAPI = FoursquareAPI()

def list():
    results = foursquareAPI.searchForRestaurants(session.zipCode,session.maxDistanceInMiles,
        session.pricePrefs, session.finalRatings)
    if len(results) == 0:
        return dict(message="No results found. Try entering a different zip code or increasing the search radius.", searchResults=results, cuisineRatings=session.cuisineRatings)
        
    return dict(message="This is the view for viewing a list of restaurant results", searchResults=results, cuisineRatings=session.cuisineRatings)

def restaurant():
    restaurantId = request.vars.get('id', None)
    restaurantInfo = foursquareAPI.getRestaurantDetails(restaurantId)
    return dict(restaurantDetails=restaurantInfo)
