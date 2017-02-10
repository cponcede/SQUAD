#Controller for the Arena

import random
import math
from copy import deepcopy

def arena():
    # Hard-coded in the random cuisine to serve to the user. Eventually, use the existing information to choose cuisines to serve.
    cuisine1 = random.choice(session.cuisines)
    cuisine2 = random.choice(session.cuisines)
    while (cuisine2 == cuisine1 or cuisine2 == session.previousCuisines[0] or cuisine2 == session.previousCuisines[1]):
        cuisine2 = random.choice(session.cuisines)

    photos = db((db.image.title == cuisine1) | (db.image.title == cuisine2)).select(orderby=db.image.title)

    if not session.first:
        session.first = True
        session.previousCuisines[0] = cuisine1
        session.previousCuisines[1] = cuisine2
        return dict(images = photos, ratings = [], test = "first")
    else:
        if request.vars.done:
            finalRatings = {}
            minRating = session.cuisineRatings[min(session.cuisineRatings, key=session.cuisineRatings.get)]
            maxRating = session.cuisineRatings[max(session.cuisineRatings, key=session.cuisineRatings.get)]
            for key in session.cuisineRatings.keys():
                row = db(db.image.title == key).select(db.image.foursquareId)
                finalRatings[row[0]['foursquareId']] = (1.0*session.cuisineRatings[key] - 1.0*minRating)/(1.0*maxRating - 1.0*minRating)
            # Only show results for cuisines in the top 25% of results. (We can change this number later based on results)
            session.finalRatings = dict((k, v) for k, v in finalRatings.items() if v > 0.75)
            redirect(URL('results', 'list'))
        else:
            if request.vars:
                chosen_cuisine = request.vars.keys()[0]
                if ".y" in chosen_cuisine or ".x" in chosen_cuisine:
                    chosen_cuisine = chosen_cuisine[:-2]

                updateElo(session.previousCuisines[0],session.previousCuisines[1],chosen_cuisine)

                ratings_list = [(key, value) for key,value in session.cuisineRatings.items()]
                ratings_list = sorted(ratings_list, key=lambda x: x[1], reverse = True)
                combo = cuisine1 + " " + cuisine2

                session.previousCuisines[0] = cuisine1
                session.previousCuisines[1] = cuisine2
                return dict(images = photos, ratings = ratings_list, test = chosen_cuisine)
            else:
                # First time the page is loaded.
                session.previousCuisines[0] = cuisine1
                session.previousCuisines[1] = cuisine2
                return dict(images = photos, ratings = [], test = "First")

def updateElo(cuisine1,cuisine2, winner):
    K = 32

    p1_elo = session.cuisineRatings[cuisine1]
    p2_elo = session.cuisineRatings[cuisine2]
    t1 = math.pow(10,(float(p1_elo)/400))
    t2 = math.pow(10,(float(p2_elo)/400))
    exp1 = t1/(t1+t2)
    exp2 = t2/(t1+t2)
    score1 = 1
    score2 = 0
    if winner == cuisine2:
        score1 = 0
        score2 = 1
    p1_new = p1_elo + K*(score1 - exp1)
    p2_new = p2_elo + K*(score2 - exp2)

    session.cuisineRatings[cuisine1] = p1_new
    session.cuisineRatings[cuisine2] = p2_new


def download():
    return response.download(request, db)
