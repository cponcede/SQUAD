#Controller for the Arena
def arena():
    # Right now passing all of the images in the database. Eventually should only pass the 2 images to be displayed.
    photos = db().select(db.image.ALL, orderby=db.image.title)

    if not session.first:
		session.first = True
		return dict(images = photos)
    else:
        if request.vars.done:
            # Hard-coding in dictionary of cuising ratings so I can use them in results.py
            session.cuisineRatings = {'japanense':0.9, 'chinese':0.7, 'italian': 0.8}
            redirect(URL('results', 'list'))
        else:
            if request.vars.left:
                return dict(images = photos)
            else:
                return dict(images = photos)

def download():
    return response.download(request, db)
