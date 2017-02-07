# -*- coding: utf-8 -*-
# try something like
def landingpage():
    if request.vars.signin:
        redirect(URL('welcome', 'signin'))
    elif request.vars.signup:
        redirect(URL('welcome', 'signup'))
    else:
        return dict()

def signin():
    if request.vars.username:
        #TODO: validate username and password
        session.name = request.vars.username
        session.pricePrefs = {"$": True, "$$": False, "$$$": False, "$$$$": False}
        session.zipCode = '94305'
        session.maxDistanceInMiles = 30
        session.cuisines = ["Indian","Italian","Mexican","Asian_Fusion","Barbecue","Burgers","Chinese","Japanese","American_(New)","Pizza","Salad","Sandwiches","Seafood","Sushi","American_(Traditional)","Vietnamese"]
        base_ELO = 1500
        session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
        session.previousCuisines = ["",""]
        redirect(URL('cuisinearena', 'arena'))
    else:
        return dict()

def signup():
    if request.vars.username:
        #TODO:store signup data in database
        #TODO:error checking here or in HTML?
        session.name = request.vars.username
        session.pricePrefs = {"$": True, "$$": False, "$$$": False, "$$$$": False}
        session.zipCode = '94305'
        session.maxDistanceInMiles = 30
        session.cuisines = ["Indian","Italian","Mexican","Asian_Fusion","Barbecue","Burgers","Chinese","Japanese","American_(New)","Pizza","Salad","Sandwiches","Seafood","Sushi","American_(Traditional)","Vietnamese"]
        base_ELO = 1500
        session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
        session.previousCuisines = ["",""]
        redirect(URL('cuisinearena', 'arena'))
    else:
        return dict()
