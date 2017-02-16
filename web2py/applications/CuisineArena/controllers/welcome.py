# -*- coding: utf-8 -*-
# try something like
def landingpage():
    session.numMatchups = 0
    if request.vars.signin:
        redirect(URL('welcome', 'signin'))
    elif request.vars.signup:
        redirect(URL('welcome', 'signup'))
    else:
        return dict()

def signin():
    if request.vars.username:
        user = db.user(db.user.username == request.vars.username)
        if user:
            if user.password == request.vars.password:
                session.name = request.vars.username
                session.cuisines = ["Indian","Italian","Mexican","Barbecue","Burgers","Chinese","Japanese","American_(New)","Pizza","Salad","Sandwiches","Seafood","Sushi","American_(Traditional)","Vietnamese"]
                base_ELO = 1500
                session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
                session.cuisineCounts = {cuisine:0 for cuisine in session.cuisines}
                session.previousCuisines = ["",""]
                redirect(URL('welcome', 'preferences'))
            else:
                return dict(message='Password is incorrect', rows=db().select(db.user.ALL), user=user, password=user.password) #right now just returns to signin page
        else:
            return dict(message='No such user', rows=db().select(db.user.ALL)) #right now just returns to singin page
    else:
        return dict()

def signup():
    if request.vars.username:
        try:
            db.user.insert(username=request.vars.username, password=request.vars.password)
        except Exception, e:
            db.rollback()
            return dict(message='Invalid SignUp', exception = e, rows=db().select(db.user.ALL)) #right now this just returns to signup maybe should change
        else:
            db.commit()
            session.name = request.vars.username
            session.cuisines = ["Indian","Italian","Mexican","Barbecue","Burgers","Chinese","Japanese","American_(New)","Pizza","Salad","Sandwiches","Seafood","Sushi","American_(Traditional)","Vietnamese"]
            base_ELO = 1500
            session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
            session.cuisineCounts = {cuisine:0 for cuisine in session.cuisines}
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
