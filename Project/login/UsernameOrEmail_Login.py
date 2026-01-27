from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class UsernameOrEmailLogin(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			user = User.objects.get(
				Q(username=username) | Q(email=username)
			)
		#try
		except User.DoesNotExist:
			return None
		#except
		
		if user.check_password(password) and self.user_can_authenticate(user):
			return user
		#if
		
		return None
	#def
#class