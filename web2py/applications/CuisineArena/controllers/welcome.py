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
		#TODO: validate username and password
		session.name = request.vars.username
		redirect(URL('cuisinearena', 'arena'))
	else:
		return dict()

def signup():
	if request.vars.username:
		#TODO:store signup data in database
        #TODO:error checking here or in HTML?
		session.name = request.vars.username
		redirect(URL('cuisinearena', 'arena'))
	else:
		return dict()
