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
        user = db.person(db.person.username == request.vars.username)
        if user:
            if user.password == request.vars.password:
                session.name = request.vars.username
                session.pricePrefs = '1,2'
                session.zipCode = '94305'
                session.maxDistanceInMiles = 30
                session.cuisines = ["Indian","Italian","Mexican","Asian_Fusion","Barbecue","Burgers","Chinese","Japanese","American_(New)","Pizza","Salad","Sandwiches","Seafood","Sushi","American_(Traditional)","Vietnamese"]
                base_ELO = 1500
                session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
                session.previousCuisines = ["",""]
                redirect(URL('cuisinearena', 'arena'))
            else:
                return dict(message='Password is incorrect', rows=db().select(db.person.ALL), user=user, password=user.password) #right now just returns to signin page
        else:
            return dict(message='No such user', rows=db().select(db.person.ALL)) #right now just returns to singin page
    else:
        return dict()

def signup():
    if request.vars.username:
        try:
            db.person.insert(username=request.vars.username, password=request.vars.password)
        except Exception, e:
            db.rollback()
            return dict(message='Invalid SignUp', exception = e, rows=db().select(db.person.ALL)) #right now this just returns to signup maybe should change
        else:
            db.commit()
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
