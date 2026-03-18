from django.shortcuts import get_object_or_404, redirect
from functools import wraps
from django.contrib import messages

from directory.models import Question

from django.contrib.auth import get_user_model
User = get_user_model()

from django.utils.translation import gettext_lazy as _

# Making sure only book owners can access certain views
def question_creator(function):
	
	@wraps(function)
	def wrap(request, *args, **kwargs):
		
		# Get the current question
		question_id = kwargs.get('question_id')
		question = get_object_or_404(Question, id=question_id)
		
		# Get the currently logged-in user ID
		current_user_id = request.user.id
		
		# Get the user ID of the uploader
		uploader = question.uploader_id
		
		if (current_user_id == uploader):
			return function(request, *args, **kwargs)
		#if
		else:
			messages.error(request, "You are not allowed to access this page.", extra_tags="danger")
			return redirect('index')
		#else
		
	#def wrap
	
	return wrap
	
#def