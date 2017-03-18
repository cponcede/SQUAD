from foursquareapi import FoursquareAPI 
foursquareAPI = FoursquareAPI()

def list():
	results = foursquareAPI.searchForRestaurants(session.zipCode,session.maxDistanceInMiles, session.pricePrefs, session.finalRatings)
	groupId = db((db.userGroup.username == session.name)).select().first().groupId
	groupRows = db((db.userGroup.groupId == groupId)).select()
	completedNames = [row.username for row in groupRows if row.completed]
	inProgressNames = [row.username for row in groupRows if not row.completed]

	if len(results) == 0:
	    return dict(message="No results found. Try entering a different zip code or increasing the search radius.", searchResults=results, cuisineRatings=session.cuisineRatings, completed = completedNames, inProgress = inProgressNames, group=session.group)
	else:
		return dict(message="This is the view for viewing a list of restaurant results", searchResults=results, cuisineRatings=session.cuisineRatings, completed = completedNames, inProgress = inProgressNames, group=session.group)

def restaurant():
	restaurantId = request.vars.get('id', None)
	restaurantInfo = foursquareAPI.getRestaurantDetails(restaurantId)
	return dict(restaurantDetails=restaurantInfo)
