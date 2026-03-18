from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.contrib import messages
from login.decorators import not_logged_in

# Custom view for requesting password reset
@not_logged_in
def custom_password_reset(request):
	if request.method == "POST":
		form = PasswordResetForm(request.POST)
		if form.is_valid():
			form.save(
				request=request,
				use_https=request.is_secure(),
				token_generator=default_token_generator,
				from_email=None,
				email_template_name='login/password_reset_email.html',
				subject_template_name='login/password_reset_subject.txt',
			) #form.is_valid
			messages.success(request, "The email has been sent! Please check your emails to reset your password.")
			return redirect('index')
		#if form.is_valid
	#if
	else:
		form = PasswordResetForm()
	#else
	
	
	template_name = "login/password_reset_form.html"
	context = {
		"form": form,
	}
	
	return render(request, template_name, context)
#def custom_password_reset



# Custom view for password reset confirm (new password form)
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
	template_name = 'login/password_reset_confirm.html'  # Custom template
	success_url = reverse_lazy('login')  # Redirect to login page after successful reset
	
	def form_valid(self, form):
		# Call the superclass's form_valid to process the password reset
		response = super().form_valid(form)
		# Add a success message
		messages.success(self.request, "Your password has been reset successfully. You can now log in with your new password.")
		return response
	#def form_valid
#class CustomPasswordResetConfirmView