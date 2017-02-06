#Controller for the Arena
def arena():
    if not session.first:
		session.first = True
		return dict()
    else:
        if request.vars.done:
            # Hard-coding in dictionary of cuising ratings so I can use them in results.py
            session.cuisineRatings = {'japanese':0.9, 'chinese':0.7, 'italian': 0.8}
            redirect(URL('results', 'list'))
        else:
            if request.vars.left:
                return dict()
            else:
                return dict()
