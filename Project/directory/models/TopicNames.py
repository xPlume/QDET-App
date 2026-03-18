from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

class TopicNames(models.Model):
	
	name = models.CharField(null=False, default=None, max_length=63)
	user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	
	def __str__(self):
		return f"{self.name} by {self.user.username}"
	#def __str__
	
#class Topics
