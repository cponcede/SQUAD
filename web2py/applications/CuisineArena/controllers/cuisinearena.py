#Controller for the Arena

import random
import math
from copy import deepcopy

def arena():
    # Hard-coded in the random cuisine to serve to the user. Eventually, use the existing information to choose cuisines to serve.
    idealMatchupNumber = 20
    matchupPercent = str(float(session.numMatchups)/idealMatchupNumber*100)[0:2] + "%"
    if matchupPercent[-2] == ".":
        matchupPercent = matchupPercent[0] + matchupPercent[-1]
    if idealMatchupNumber <= session.numMatchups:
        matchupPercent = "100%"

    cuisine1, cuisine2 = cuisineServer()
    session.cuisineCounts[cuisine1] = session.cuisineCounts[cuisine1] + 1
    session.cuisineCounts[cuisine2] = session.cuisineCounts[cuisine2] + 1

    photos = db((db.image.title == cuisine1) | (db.image.title == cuisine2)).select(orderby=db.image.title)

    if not session.first:
        session.first = True
        session.previousCuisines[0] = cuisine1
        session.previousCuisines[1] = cuisine2
        return dict(images = photos, ratings = [], matchupProgress = (matchupPercent, session.numMatchups), test = "first")
    else:
        if request.vars.done:
            finalRatings = {}
            minRating = session.cuisineRatings[min(session.cuisineRatings, key=session.cuisineRatings.get)]
            maxRating = session.cuisineRatings[max(session.cuisineRatings, key=session.cuisineRatings.get)]
            for key in session.cuisineRatings.keys():
                row = db(db.image.title == key).select(db.image.foursquareId, db.image.title)
                if maxRating == minRating:
                    finalRatings[row[0]['foursquareId']] = (row[0]['title'], 1.0)
                else:
                    finalRatings[row[0]['foursquareId']] = (row[0]['title'], (1.0*session.cuisineRatings[key] - 1.0*minRating)/(1.0*maxRating - 1.0*minRating))
            # Only show results for cuisines in the top 25% of results. (We can change this number later based on results)
            session.finalRatings = dict((k, v) for k, v in finalRatings.items() if v[1] > 0.75)
            #update the cuisine rankings in the model
            if session.group:
                groupRow = db((db.userGroup.username == session.name)).select().first()
                groupRow.update_record(completed=True)
            for cuisine in session.cuisineRatings:
                rating = session.cuisineRatings[cuisine]
                cuisine_row = db((db.cuisine.username == session.name) & (db.cuisine.cuisine == cuisine)).select().first()
                cuisine_row.update_record(rating = rating)

            redirect(URL('results', 'list'))
        else:
            if request.vars:
                session.numMatchups = session.numMatchups + 1
                chosen_cuisine = request.vars.keys()[0]
                if ".y" in chosen_cuisine or ".x" in chosen_cuisine:
                    chosen_cuisine = chosen_cuisine[:-2]

                updateElo(session.previousCuisines[0],session.previousCuisines[1],chosen_cuisine)

                ratings_list = [(key, value) for key,value in session.cuisineRatings.items()]
                ratings_list = sorted(ratings_list, key=lambda x: x[1], reverse = True)
                combo = cuisine1 + " " + cuisine2

                session.previousCuisines[0] = cuisine1
                session.previousCuisines[1] = cuisine2
                return dict(images = photos, ratings = ratings_list, matchupProgress = (matchupPercent, session.numMatchups), test = chosen_cuisine)
            else:
                # First time the page is loaded.
                session.previousCuisines[0] = cuisine1
                session.previousCuisines[1] = cuisine2
                return dict(images = photos, ratings = [], matchupProgress = (matchupPercent, session.numMatchups), test = "First")

def cuisineServer():
    zeroCuisines = [cuisine for cuisine,count in session.cuisineCounts.items() if count == 0]
    cuisine1 = ""
    cuisine2 = ""
    if len(zeroCuisines) == 1:
        cuisine1 = zeroCuisines[0]
        cuisine2 = random.choice(session.cuisines)
        while (cuisine2 == cuisine1 or cuisine2 in session.previousCuisines):
            cuisine2 = random.choice(zeroCuisines)
    elif len(zeroCuisines) >= 2:
        cuisine1 = random.choice(zeroCuisines)
        cuisine2 = random.choice(zeroCuisines)
        while (cuisine2 == cuisine1 or cuisine2 in session.previousCuisines):
            cuisine2 = random.choice(zeroCuisines)

    if cuisine1 == "":
        adjElo = {cuisine:(elo-min(session.cuisineRatings.values())) for cuisine,elo in session.cuisineRatings.items()}
        minCuisine = [cuisine for cuisine,elo in adjElo.items() if elo == 0.0][0]
        adjElo[minCuisine] = adjElo[minCuisine] + 10.0
        adjElo = [(cuisine,(elo/sum(adjElo.values()))) for cuisine,elo in adjElo.items()]

        cdfElo = []
        eloSum = 0.0
        for cuisine, elo in adjElo:
            cdfElo.append((cuisine, eloSum + elo))
            eloSum = eloSum + elo
        cdfElo = sorted(cdfElo, key=lambda x: x[1])
        randCuisineFloat = random.uniform(0, 1)
        #print(cdfElo)

        for cuisine, elo in cdfElo:
            if randCuisineFloat <= elo:
                cuisine1 = cuisine
                break

        randCuisineFloat2 = random.uniform(0, 1)
        for cuisine, elo in cdfElo:
            if randCuisineFloat2 <= elo:
                cuisine2 = cuisine
                break

        while (cuisine2 == cuisine1 or cuisine2 in session.previousCuisines):
            randCuisineFloat2 = random.uniform(0, 1)
            for cuisine, elo in cdfElo:
                if randCuisineFloat2 <= elo:
                    cuisine2 = cuisine
                    break

        #print(randCuisineFloat, cuisine1, randCuisineFloat2, cuisine2)

    return (cuisine1, cuisine2)

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
