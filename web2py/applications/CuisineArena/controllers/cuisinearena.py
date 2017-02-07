#Controller for the Arena

import random

def arena():
    # Hard-coded in the random cuisine to serve to the user. Eventually, use the existing information to choose cuisines to serve.

    cuisine1 = random.choice(session.cuisines)
    cuisine2 = random.choice(session.cuisines)
    while (cuisine2 == cuisine1):
        cuisine2 = random.choice(session.cuisines)

    photos = db((db.image.title == cuisine1) | (db.image.title == cuisine2)).select()

    if len(photos) != 2:
        combo = cuisine1 + " AND " + cuisine2
        photos2 = db().select(db.image.ALL, orderby=db.image.title)
        return dict(images = photos2, ratings = session.cuisineRatings, test = combo)
    else:

        if not session.first:
            session.first = True
            base_ELO = 1000
            session.cuisineRatings = {cuisine:base_ELO for cuisine in session.cuisines}
            return dict(images = photos, ratings = session.cuisineRatings, test = "first")
        else:
            if request.vars.done:
                # Hard-coding in dictionary of cuising ratings so I can use them in results.py
                # session.cuisineRatings = {'japanense':0.9, 'chinese':0.7, 'italian': 0.8}
                redirect(URL('results', 'list'))
            else:
                if request.vars:
                    chosen_title = request.vars.keys()[0]
                    if ".y" in chosen_title or ".x" in chosen_title:
                        chosen_title = chosen_title[:-2]
                    return dict(images = photos, ratings = session.cuisineRatings, test = chosen_title)
                else:
                    return dict(images = photos, ratings = session.cuisineRatings, test = "hi")


def download():
    return response.download(request, db)
