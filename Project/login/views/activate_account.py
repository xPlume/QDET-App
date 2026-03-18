from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from login.activate_account_token import account_activation_token

from django.contrib import messages
from login.decorators import not_logged_in

@not_logged_in
def activate_account(request, uidb64, token):
	
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = get_user_model().objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
		user = None
	#except 
	
	
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		
		messages.success(request, "Your account was validated! You may now login.", extra_tags="success")
		return redirect('login')
	else:
		messages.success(request, "Activation invalid.", extra_tags="danger")
		return redirect('register')
	#else
	
#def 