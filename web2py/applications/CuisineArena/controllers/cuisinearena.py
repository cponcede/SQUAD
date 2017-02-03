#Controller for the Arena
def arena():
	if not session.first:
		session.first = True 
		return dict()
	else:
		if request.vars.done:
			redirect(URL('results', 'list'))
		else:
			if request.vars.left:
				return dict()
			else:
				return dict()



