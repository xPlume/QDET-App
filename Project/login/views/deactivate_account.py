from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages

from django.contrib.auth import get_user_model
User = get_user_model()

"""
Instead of outright deleting accounts, we deactivate them.
If a user wants their account fully deleted, an admin should
do it through the admin panel.
"""

def deactivate_account(request, user_id):
	
	user = get_object_or_404(User, id=user_id, is_active=True)
	
	# Checking access permission
	current_user_id = request.user.id
	if (user.id != current_user_id):
		messages.error(request, "You aren't allowed to access this page.", extra_tags="danger")
		return redirect('library')
	#if
	
	
	if request.method == 'POST':
		user.is_active = False
		user.save()
		logout(request)
		
		messages.success(request, f"Your account has been deleted.", extra_tags="success")
		return redirect("index")
	#if
	
	template_name = "users/deactivate_account.html"
	context = {
		"user": user,
	}
	
	return render(request, template_name, context)
	
	
#def deactivate_account