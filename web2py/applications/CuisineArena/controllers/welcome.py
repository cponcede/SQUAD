import re
import requests
import smtplib
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

GOOGLE_MAPS_API_KEY = 'AIzaSyC5lZdS271NXjMuUooVStlcRGSj09FPpdU'

def isValidEmail(email):
    return re.match("[^@]+@[^@]+\.[^@]+", email) != None

def landingpage():
    session.name = None
    session.numMatchups = 0
    if request.vars.signin:
        user = db.user(db.user.username == request.vars.signin)
        if user:
            if user.password == request.vars.signinpassword:
                session.name = request.vars.signin
                session.new_user = False
                redirect(URL('welcome', 'preferences'))
            else:
                print 'wrong password'
                return dict(error=True, message='Password is incorrect', rows=db().select(db.user.ALL), user=user, password=user.password) #right now just returns to signin page
        else:
            print 'no user'
            return dict(error=True, message='No such user', rows=db().select(db.user.ALL)) #right now just returns to singin page
    elif request.vars.submited:
        validated, message = validateSignUp(request.vars)
        if not validated:
            return dict(error=True, message=message)
        try:
            db.user.insert(username=request.vars.signup, password=request.vars.password)
        except Exception, e:
            db.rollback()
            return dict(error=True, message='Invalid SignUp DATABASE FAILED', exception = e, rows=db().select(db.user.ALL)) #right now this just returns to signup maybe should change
        else:
            db.commit()
            session.name = request.vars.signup
            session.cuisines = ["Indian","Italian","Mexican","Barbecue","Burgers","Chinese","Japanese","American_(New)","Pizza","Salad","Sandwiches","Seafood","Sushi","American_(Traditional)","Vietnamese"]
            base_ELO = 1500
            session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
            session.cuisineCounts = {cuisine:0 for cuisine in session.cuisines}
            session.previousCuisines = ["",""]
            session.new_user = True
            for i,cuisine in enumerate(session.cuisineRatings): #THIS IS A CUISINE ID BUG BUT I GOTTA GO TO CLASS
                db.cuisine.insert(username=session.name, cuisineId=i, cuisine=cuisine, rating=base_ELO)
            redirect(URL('welcome', 'preferences'))
    else:
        return dict(error=False)

def validateSignUp(vars):
    if len(vars.signup) == 0:
        return False, "Username can't be empty"
    elif len(vars.password) == 0:
        return False, "Password can't be empty"
    elif vars.password != vars.confirmation:
        return False, "Password does not match confirmation password"
    elif len(vars.firstname) == 0:
        return False, "First Name can't be empty"
    elif len(vars.lastname) == 0:
        return False, "Last Name can't be empty"
    elif db(db.user.username == vars.signup).select().first() != None:
        return False, "Username already exists in the table"
    elif isValidEmail(vars.email) == False:
        return False, "Email not valid"
    else:
        return True, ""

def reset():
    if request.vars.reset or request.vars.no_reset:
        session.cuisines = ["Indian","Italian","Mexican","Barbecue","Burgers","Chinese","Japanese","American_(New)","Pizza","Salad","Sandwiches","Seafood","Sushi","American_(Traditional)","Vietnamese"]

        if request.vars.reset:
            session.previousCuisines = ["",""]
            session.cuisineCounts = {cuisine:0 for cuisine in session.cuisines}

            #
            base_ELO = 1500
            session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
        else: #request.vars.no_reset:
            #these may be a bug talk to keyur about the possibility trying to include these from their prior session?
            session.previousCuisines = ["",""] 
            rows = db(db.cuisine.username == session.name).select()
            session.cuisineRatings = {row.cuisine:float(row.rating) for row in rows}
            temp_counts = {cuisine:int(abs(rating-1500)) for cuisine,rating in session.cuisineRatings.items()}

            reset_counts = {}
            for cuisine,rating in temp_counts.items():
                if rating != 0:
                    reset_counts[cuisine] = 1
                else:
                    reset_counts[cuisine] = rating
            session.cuisineCounts = reset_counts

        redirect(URL('cuisinearena', 'arena'))
    else:
        return dict(message="")

def isValidZipCode(zipCode):
    if re.match('^\d{5}(-\d{4})?$', zipCode) == None:
        return False
    return True

def isValidRadius(radius):
    if radius >= 10 and radius <= 60:
        return True
    return False

def getZipCode():
    response = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key=' + GOOGLE_MAPS_API_KEY)
    loc = response.json()['location']
    lat = loc['lat']
    lng = loc['lng']
    requestString = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(lat) + ',' + str(lng) + '&key=' + GOOGLE_MAPS_API_KEY
    secondResponse = requests.post(requestString).json()['results'][0]
    for component in secondResponse['address_components']:
        if 'postal_code' in component['types']:
            zipCode = component['long_name']
            if not isValidZipCode(zipCode):
                return {'error_msg': 'Invalid zip code provided.'}
            session.zipCode = zipCode
            print("GEOZIP = " + zipCode)
            return zipCode

def joinGroup():
    if request.vars.groupId:
        session.groupId = request.vars.groupId
    if session.name:
        if request.vars.groupId:
            groupId = session.groupId
            password = request.vars.password
            groupRow = db((db.userGroup.username == session.name)).select()
            if len(groupRow) == 0:
                db.userGroup.insert(username = session.name, groupId = session.groupId, completed = False)
            redirect(URL('cuisinearena', 'arena'))
        else:
            return dict() #handlelogin
    elif request.vars.groupId:
        return dict(group=session.groupId, message="")
    else:
        user = db.user(db.user.username == request.vars.signin)
        if user:
            if user.password == request.vars.signinpassword:
                groupRow = db((db.group1.groupId == session.groupId)).select().first()
                db.userGroup.insert(username = session.name, groupId = session.groupId, completed = False)
                session.name = request.vars.signin
                session.new_user = False
                session.zipCode = groupRow.zipcode
                session.maxDistanceInMiles = groupRow.distance
                session.group = True
                session.pricePrefs = groupRow.price
                redirect(URL('welcome', 'reset'))
            else:
                return dict(group=session.groupId, message='No such password')
        else:
            return dict(group=session.groupId, message='No such user') #right now just returns to singin page

def handleEmails(emails, groupId, password):
    fromaddr = "cuisinearena@gmail.com"


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("cuisinearena@gmail.com", "chrisponce")
    i = 1
    for email in emails:
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = email  
        msg['Subject'] = "Join Our CuisineArena Group"
        body = "https://limitless-shore-47477.herokuapp.com/CuisineArena/welcome/joinGroup?groupId=%s" % (groupId)
        msg.attach(MIMEText(body, 'plain')) 
        text = msg.as_string()
        server.sendmail(fromaddr, email, text)

    server.quit()

def preferences():
    if request.vars.price or request.vars.zipcode or request.vars.radius:
        if request.vars.price:
            if request.vars.zipcode:
                if request.vars.radius:
                    # User current location
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
                    session.group = False
                    if request.vars.group == 'group':
                        session.group = True
                        if request.vars.create == 'create':
                            groupId = request.vars.createGroupId
                            groupPass = request.vars.createPassword
                            if len(groupId) == 0:
                                return {'error_msg': 'Error: Group Id cannot be empty'}
                            elif db(db.group1.groupId == groupId).select().first():
                                return {'error_msg': 'Error: Group Id already exists'}
                            emails = request.vars.emails.split()
                            for email in emails:
                                if not isValidEmail(email):
                                    return {'error_msg': 'Error: Email: \'%s\' is invalid.' % email} 
                            db.group1.insert(groupId = groupId, password = groupPass, zipcode=zipCode, distance=maxDistanceInMiles, price=priceString)
                            if len(emails) > 0:
                                handleEmails(emails, groupId, groupPass)
                            #handle emails later
                        else:
                            groupId = request.vars.joinGroupId
                            groupPass = request.vars.joinPassword
                            row = db(db.group1.groupId == groupId).select().first()
                            if row == None:
                                return {'error_msg': 'Error: Group Id for joining a group does not exist.'}
                            elif row.password != groupPass:
                                return {'error_msg': 'Error: Incorrect Group Password, keyur.'}
                        db.userGroup.insert(username = session.name, groupId = groupId, completed = False)
                    if session.new_user:
                        redirect(URL('cuisinearena', 'arena'))
                    else:
                        redirect(URL('welcome','reset'))
                else:
                    return {'error_msg': 'Error: No radius to search was provided.'}
            else:
                return {'error_msg': 'Error: No location was provided'}
        else:
            return {'error_msg': 'Error: No price tiers were selected.'}
    else:
        return {'error_msg': ''}
