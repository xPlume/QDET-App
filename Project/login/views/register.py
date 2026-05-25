from django.shortcuts import render, redirect
from django.contrib.auth import login
from login.forms import CustomUserCreationForm
from login.activate_account_token import account_activation_token
from .email_activation import send_activation_email
from login.decorators import not_logged_in

from django.contrib import messages

@not_logged_in
def register(request):
	
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST, request.FILES)
		
		if form.is_valid():
			
			
			# On production, please remove the following comments
			# The goal of that code is to verify an email before validating the account
			"""
			# Save user but don't log them in
			user = form.save(commit=False)
			user.is_active = False  # Set user as inactive until email verification
			user.save()
			
			# Send verification email
			send_activation_email(request, user, form)
			
			messages.success(request, "Check your emails to activate your account.", extra_tags="success")
			return redirect('index')
			"""
			
			# On development, just create the account (no email verification)
			user = form.save()
			messages.success(request, "Your account has been created! Please login.", extra_tags="success")
			return redirect('login')
			
		#if
		else:
			messages.error(request, form.errors, extra_tags="danger")
		#
		
	#if
	else:
		form = CustomUserCreationForm()
	#else
	
	
	template_name = "login/register.html"
	context = {
		'form': form,
	}
	
	return render(request, template_name, context)
	
	
#def register