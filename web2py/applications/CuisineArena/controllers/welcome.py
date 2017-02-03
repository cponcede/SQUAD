# -*- coding: utf-8 -*-
# try something like
def landingpage(): 
	if request.vars.name:
		#here's where I'm going to put the variables keyur gives me
		#in the form: session.variable_name = request.vars.variable_name
		session.name = request.vars.name
		redirect(URL('cuisinearena', 'arena'))
	else:
		return dict()
