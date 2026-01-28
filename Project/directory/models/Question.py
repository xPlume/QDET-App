from django.db import models

from django.conf import settings
from login.models import ActiveUserManager
User = settings.AUTH_USER_MODEL

class Question(models.Model):
	
	question = models.CharField(null=False, default=None, max_length=516)
	uploader = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	
	objects = ActiveUserManager(user_field='uploader')
	all_objects = models.Manager()
	
	def __str__(self):
		return f"{self.question}"
	#def __str__
	
#class Question
