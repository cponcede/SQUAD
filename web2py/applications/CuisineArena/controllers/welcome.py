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
        #session.pricePrefs = '1,2'
        #session.zipCode = '94305'
        #session.maxDistanceInMiles = 30
        session.cuisines = ["Indian","Italian","Mexican","Barbecue","Burgers","Chinese","Japanese","American_(New)","Pizza","Salad","Sandwiches","Seafood","Sushi","American_(Traditional)","Vietnamese"]
        base_ELO = 1500
        session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
        session.previousCuisines = ["",""]
        redirect(URL('welcome', 'preferences'))
    else:
        return dict()

def signup():
    if request.vars.username:
        #TODO:store signup data in database
        #TODO:error checking here or in HTML?
        session.name = request.vars.username
        #session.pricePrefs = {"$": True, "$$": False, "$$$": False, "$$$$": False}
        #session.zipCode = '94305'
        #session.maxDistanceInMiles = 30
        session.cuisines = ["Indian","Italian","Mexican","Asian_Fusion","Barbecue","Burgers","Chinese","Japanese","American_(New)","Pizza","Salad","Sandwiches","Seafood","Sushi","American_(Traditional)","Vietnamese"]
        base_ELO = 1500
        session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
        session.previousCuisines = ["",""]
        redirect(URL('welcome', 'preferences'))
    else:
        return dict()

def preferences():
    if request.vars.price or request.vars.zipcode or request.vars.radius:
        if request.vars.price:
            if request.vars.zipcode:
                if request.vars.radius:
                    session.zipCode = request.vars.zipcode
                    session.maxDistanceInMiles = float(request.vars.radius)
                    priceString = ""
                    for tier in request.vars.price:
                        priceString = priceString + tier + ','
                    priceString = priceString[:-1]
                    session.pricePrefs = priceString
                    redirect(URL('cuisinearena','arena'))
                else:
                    return {'error_msg': 'Error: No radius to search was provided.'}
            else:
                return {'error_msg': 'Error: No zipcode was provided'}
        else:
            return {'error_msg': 'Error: No price tiers were selected.'}
    else:
        return {'error_msg': ''}
