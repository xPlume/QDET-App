from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


from django.contrib.auth import get_user_model
User = get_user_model()


# Views only for non logged in users (login view, register...)
def not_logged_in(function):
	
	@wraps(function)
	def wrap(request, *args, **kwargs):
		
		current_user_username = request.user.username
		
		# Checking if there is a logged-in user
		if (current_user_username == ""):
			return function(request, *args, **kwargs)
		#if
		
		messages.error(request, "You are already logged-in! Log out to access this page.", extra_tags="danger")
		return redirect('index')
		
	#def wrap
	
	return wrap
	
#def not_logged_in

