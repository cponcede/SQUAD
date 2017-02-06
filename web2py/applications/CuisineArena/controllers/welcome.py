# -*- coding: utf-8 -*-
# try something like
def landingpage(): 
    if request.vars.name:
        #here's where I'm going to put the variables keyur gives me
        #in the form: session.variable_name = request.vars.variable_name
        session.name = request.vars.name
        # Similar to above, am hardcoding the input from the user that we need to store in the session object.
        session.pricePrefs = {"$": True, "$$": False, "$$$": False, "$$$$": False}
        session.zipCode = '94305'
        session.maxDistanceInMiles = 30
        redirect(URL('cuisinearena', 'arena'))
    else:
        return dict()
