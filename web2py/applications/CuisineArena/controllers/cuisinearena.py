#Controller for the Arena
def arena():
    if not session.first:
		session.first = True
		return dict()
    else:
        if request.vars.done:
            # Hard-coding in dictionary of cuising ratings so I can use them in results.py.
            # The keys are Foursquare category IDs.
            # We need to add a database that contains cuisine names and associated cuisine IDs
            session.cuisineRatings = {'4bf58dd8d48988d111941735':0.9, '4bf58dd8d48988d145941735':0.7, '4bf58dd8d48988d110941735': 0.8}
            redirect(URL('results', 'list'))
        else:
            if request.vars.left:
                return dict()
            else:
                return dict()
