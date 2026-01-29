from django.db import models

from django.conf import settings
from login.models import ActiveUserManager
User = settings.AUTH_USER_MODEL

class Question(models.Model):
	
	context_id = models.IntegerField(blank=False, null=False)
	context = models.TextField(null=False, default=None)
	q_id = models.TextField(null=False, default=None)
	question = models.TextField(null=False, default=None)
	target_level = models.TextField(null=False, default=None)
	
	uploader = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	
	objects = ActiveUserManager(user_field='uploader')
	all_objects = models.Manager()
	
	def __str__(self):
		return f"{self.id}"
	#def __str__
	
#class Question
