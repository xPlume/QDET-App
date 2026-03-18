# This file is not required for the login to work
# It's an extention giving us more control over the login view

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils.decorators import method_decorator


class CustomLoginView(LoginView):
	template_name = 'login/login.html'
	
	# if login is valid
	def form_valid(self, form):
		user = form.get_user()
		messages.success(self.request, f"Welcome back {user.username}!", extra_tags="success")
		return super().form_valid(form)
	#def form_valid
	
	
	# if login form is invalid
	def form_invalid(self, form):
		messages.error(self.request, "Invalid username or password. Please try again.", extra_tags="danger")
		return super().form_invalid(form)
	# def
#class