import re

def landingpage():
    session.numMatchups = 0
    if request.vars.signin:
        redirect(URL('welcome', 'signin'))
    elif request.vars.signup:
        redirect(URL('welcome', 'signup'))
    else:
        return dict()

def signin():
    if request.vars.submited:
        user = db.user(db.user.username == request.vars.username)
        if user:
            #redirect to restart() here
            if user.password == request.vars.password:
                session.name = request.vars.username
                session.cuisines = ["Indian","Italian","Mexican","Barbecue","Burgers","Chinese","Japanese","American_(New)","Pizza","Salad","Sandwiches","Seafood","Sushi","American_(Traditional)","Vietnamese"]
                base_ELO = 1500
                session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
                session.cuisineCounts = {cuisine:0 for cuisine in session.cuisines}
                session.previousCuisines = ["",""]
                redirect(URL('welcome', 'preferences'))
            else:
                return dict(error=True, message='Password is incorrect', user=user, password=user.password) #right now just returns to signin page
        else:
            return dict(error=True, message='No such user') #right now just returns to singin page
    else:
        return dict(error=False)

def signup():
    if request.vars.submited:
        validated, message = validateSignUp(request.vars)
        if not validated:
            return dict(error=True, message=message)
        try:
            db.user.insert(username=request.vars.username, password=request.vars.password)
        except Exception, e:
            db.rollback()
            return dict(error=True, message='Invalid SignUp DATABASE FAILED') #right now this just returns to signup maybe should change
        else:
            db.commit()
            session.name = request.vars.username
            session.cuisines = ["Indian","Italian","Mexican","Barbecue","Burgers","Chinese","Japanese","American_(New)","Pizza","Salad","Sandwiches","Seafood","Sushi","American_(Traditional)","Vietnamese"]
            base_ELO = 1500
            for cuisine in session.cuisines:
                cuisineId = db(db.image.title == cuisine).select().first().id
                try:
                    db.cuisine.insert(username=session.name, cuisineId=cuisineId, cuisine=cuisine, rating=1500)
                except:
                    db.rollback()
                    return dict(error=True, message='Unable to insert row into cuisine table', exception = e, cuisine=cuisine)
                else:
                    db.commit()
            session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
            session.cuisineCounts = {cuisine:0 for cuisine in session.cuisines}
            session.previousCuisines = ["",""]
            redirect(URL('welcome', 'preferences'))
    else:
        return dict(error=False)

def validateSignUp(vars):
    if len(vars.username) == 0:
        return False, "Username can't be empty"
    elif len(vars.password) == 0:
        return False, "Password can't be empty"
    elif vars.password != vars.confirmation:
        return False, "Password does not match confirmation password"
    elif len(vars.firstname) == 0:
        return False, "First Name can't be empty"
    elif len(vars.lastname) == 0:
        return False, "Last Name can't be empty"
    elif db(db.user.username == vars.username).select().first() != None:
        return False, "Username already exists in the table"
    else:
        return True, ""

def restart():
    return dict()
  
def isValidZipCode(zipCode):
    if re.match('^\d{5}(-\d{4})?$', zipCode) == None:
        return False
    return True

def isValidRadius(radius):
    if radius >= 10 and radius <= 60:
        return True
    return False

def preferences():
    if request.vars.price or request.vars.zipcode or request.vars.radius:
        if request.vars.price:
            if request.vars.zipcode:
                if request.vars.radius:
                    zipCode = request.vars.zipcode
                    if not isValidZipCode(zipCode):
                        return {'error_msg': 'Invalid zip code provided.'}
                    session.zipCode = request.vars.zipcode
                    maxDistanceInMiles = float(request.vars.radius)
                    if not isValidRadius(maxDistanceInMiles):
                        return {'error_msg': 'Invalid search radius. Please choose a value in the range [10 ... 60].'}
                    session.maxDistanceInMiles = maxDistanceInMiles
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
