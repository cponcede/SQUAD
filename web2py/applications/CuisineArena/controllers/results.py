from foursquareapi import FoursquareAPI 
foursquareAPI = FoursquareAPI()

def isValidRadius(radius):
    if radius >= 10 and radius <= 60:
        return True
    return False

def list():
	print "list"
	if request.vars.price:
		priceString = ""
		for tier in request.vars.price:
			priceString = priceString + tier + ','
		priceString = priceString[:-1]
		session.pricePrefs = priceString
	if request.vars.radius:
		maxDistanceInMiles = float(request.vars.radius)
		if not isValidRadius(maxDistanceInMiles):
			return dict(message='Invalid search radius. Please choose a value in the range [10 ... 60].', priceTiers=[], searchResults=[], cuisineRatings = session.cuisineRatings)
		session.maxDistanceInMiles = maxDistanceInMiles
	results = foursquareAPI.searchForRestaurants(session.zipCode,session.maxDistanceInMiles, session.pricePrefs, session.finalRatings)
	if len(results) == 0:
		return dict(message="No results found. Try entering a different zip code or increasing the search radius.", priceTiers=priceTiers, searchResults=results, cuisineRatings=session.cuisineRatings)
	priceTiers = session.pricePrefs.split(',')    
	return dict(message="This is the view for viewing a list of restaurant results", priceTiers=priceTiers, searchResults=results, cuisineRatings=session.cuisineRatings)

def restaurant():
	restaurantId = request.vars.get('id', None)
	restaurantInfo = foursquareAPI.getRestaurantDetails(restaurantId)
	return dict(restaurantDetails=restaurantInfo)
